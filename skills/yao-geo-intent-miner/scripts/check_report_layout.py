#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-intent-miner
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Check DOCX/PDF layout constraints for Yao GEO Intent Miner reports."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import zipfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docx", required=True)
    parser.add_argument("--pdf", required=True)
    return parser.parse_args()


def check_docx(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")

    page = re.search(r'<w:pgSz[^>]*w:w="(\d+)"[^>]*w:h="(\d+)"[^>]*/>', xml)
    margins = re.search(r'<w:pgMar[^>]*w:right="(\d+)"[^>]*w:left="(\d+)"[^>]*/>', xml)
    page_width = int(page.group(1)) if page else 16838
    right = int(margins.group(1)) if margins else 850
    left = int(margins.group(2)) if margins else 850
    content_width = page_width - left - right

    table_widths = [int(value) for value in re.findall(r'<w:tblW w:w="(\d+)"', xml)]
    grid_sums = [
        sum(int(value) for value in re.findall(r'w:w="(\d+)"', grid))
        for grid in re.findall(r"<w:tblGrid>(.*?)</w:tblGrid>", xml)
    ]
    table_count = xml.count("<w:tbl>")
    fixed_count = xml.count('<w:tblLayout w:type="fixed"/>')

    return {
        "docx_readable": True,
        "docx_content_width_dxa": content_width,
        "docx_max_table_width_dxa": max(table_widths) if table_widths else 0,
        "docx_max_grid_width_dxa": max(grid_sums) if grid_sums else 0,
        "docx_tables_fit_page_width": bool(table_widths) and max(table_widths) <= content_width and bool(grid_sums) and max(grid_sums) <= content_width,
        "docx_has_fixed_table_layout": table_count > 0 and fixed_count == table_count,
    }


def check_pdf(path: Path) -> dict:
    info = subprocess.check_output(["pdfinfo", str(path)], text=True)
    page_line = next((line for line in info.splitlines() if line.startswith("Page size:")), "")
    dims = [float(value) for value in re.findall(r"\d+\.\d+|\d+", page_line)[:2]]
    return {
        "pdf_has_header": path.read_bytes()[:5] == b"%PDF-",
        "pdf_is_landscape": len(dims) >= 2 and dims[0] > dims[1],
        "pdf_page_size": page_line,
    }


def main() -> None:
    args = parse_args()
    report = {
        "docx": args.docx,
        "pdf": args.pdf,
        "checks": {},
    }
    report["checks"].update(check_docx(Path(args.docx)))
    report["checks"].update(check_pdf(Path(args.pdf)))
    report["failed_checks"] = [name for name, passed in report["checks"].items() if isinstance(passed, bool) and not passed]
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["failed_checks"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
