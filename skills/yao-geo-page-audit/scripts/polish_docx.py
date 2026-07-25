#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-page-audit
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Apply Kami-style typography and spacing to generated Word reports.

The script edits DOCX XML directly so the skill does not depend on python-docx.
"""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
ET.register_namespace("w", NS["w"])

BRAND = "1B365D"
NEAR_BLACK = "141413"
DARK_WARM = "3D3D3A"
TAG_BLUE = "EEF2F7"
SERIF = "Source Han Serif SC"
SANS = "Source Han Sans SC"
MONO = "Menlo"


def w_tag(name: str) -> str:
    return f"{{{NS['w']}}}{name}"


def set_attr(element: ET.Element, name: str, value: str) -> None:
    element.set(w_tag(name), value)


def ensure(parent: ET.Element, tag: str) -> ET.Element:
    child = parent.find(f"w:{tag}", NS)
    if child is None:
        child = ET.SubElement(parent, w_tag(tag))
    return child


def child_val(parent: ET.Element, tag: str) -> str:
    child = parent.find(f"w:{tag}", NS)
    if child is None:
        return ""
    return child.get(w_tag("val"), "")


def set_rpr(rpr: ET.Element, *, font: str, size_half_pt: str, color: str, bold: bool = False) -> None:
    rfonts = ensure(rpr, "rFonts")
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        set_attr(rfonts, key, font)

    color_el = ensure(rpr, "color")
    set_attr(color_el, "val", color)

    sz = ensure(rpr, "sz")
    set_attr(sz, "val", size_half_pt)
    sz_cs = ensure(rpr, "szCs")
    set_attr(sz_cs, "val", size_half_pt)

    b = rpr.find("w:b", NS)
    b_cs = rpr.find("w:bCs", NS)
    if bold:
        if b is None:
            b = ET.SubElement(rpr, w_tag("b"))
        if b_cs is None:
            b_cs = ET.SubElement(rpr, w_tag("bCs"))
    else:
        if b is not None:
            rpr.remove(b)
        if b_cs is not None:
            rpr.remove(b_cs)


def set_style(styles_root: ET.Element, style_id: str, *, font: str, size_half_pt: str, color: str) -> None:
    style = styles_root.find(f".//w:style[@w:styleId='{style_id}']", NS)
    if style is None:
        return
    rpr = ensure(style, "rPr")
    set_rpr(rpr, font=font, size_half_pt=size_half_pt, color=color, bold=False)
    ppr = ensure(style, "pPr")
    spacing = ensure(ppr, "spacing")
    set_attr(spacing, "before", "160" if style_id != "Heading1" else "0")
    set_attr(spacing, "after", "100")
    set_attr(spacing, "line", "276")
    set_attr(spacing, "lineRule", "auto")


def polish_styles(xml: bytes) -> bytes:
    root = ET.fromstring(xml)
    set_style(root, "Normal", font=SANS, size_half_pt="20", color=NEAR_BLACK)
    set_style(root, "BodyText", font=SANS, size_half_pt="20", color=NEAR_BLACK)
    set_style(root, "Heading1", font=SERIF, size_half_pt="40", color=BRAND)
    set_style(root, "Heading2", font=SERIF, size_half_pt="30", color=BRAND)
    set_style(root, "Heading3", font=SERIF, size_half_pt="25", color=BRAND)
    set_style(root, "SourceCode", font=MONO, size_half_pt="18", color=DARK_WARM)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def paragraph_style(paragraph: ET.Element) -> str:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        return ""
    return child_val(ppr, "pStyle")


def set_paragraph_spacing(paragraph: ET.Element, *, heading: bool) -> None:
    ppr = ensure(paragraph, "pPr")
    spacing = ensure(ppr, "spacing")
    set_attr(spacing, "before", "160" if heading else "0")
    set_attr(spacing, "after", "120" if heading else "80")
    set_attr(spacing, "line", "276")
    set_attr(spacing, "lineRule", "auto")


def polish_run(run: ET.Element, style: str, *, header: bool = False) -> None:
    rpr = ensure(run, "rPr")
    if style.startswith("Heading"):
        size = {"Heading1": "40", "Heading2": "30", "Heading3": "25"}.get(style, "24")
        set_rpr(rpr, font=SERIF, size_half_pt=size, color=BRAND, bold=False)
    elif header:
        set_rpr(rpr, font=SANS, size_half_pt="17", color=BRAND, bold=True)
    elif style in {"SourceCode", "VerbatimChar"}:
        set_rpr(rpr, font=MONO, size_half_pt="18", color=DARK_WARM, bold=False)
    else:
        set_rpr(rpr, font=SANS, size_half_pt="20", color=NEAR_BLACK, bold=False)


def shade_cell(cell: ET.Element, fill: str) -> None:
    tc_pr = ensure(cell, "tcPr")
    shd = ensure(tc_pr, "shd")
    set_attr(shd, "fill", fill)


def polish_document(xml: bytes) -> bytes:
    root = ET.fromstring(xml)

    for sect_pr in root.findall(".//w:sectPr", NS):
        pg_sz = ensure(sect_pr, "pgSz")
        set_attr(pg_sz, "w", "11906")
        set_attr(pg_sz, "h", "16838")
        pg_mar = ensure(sect_pr, "pgMar")
        for key, value in {
            "top": "1134",
            "right": "1247",
            "bottom": "1247",
            "left": "1247",
            "header": "708",
            "footer": "708",
            "gutter": "0",
        }.items():
            set_attr(pg_mar, key, value)

    for paragraph in root.findall(".//w:p", NS):
        style = paragraph_style(paragraph)
        set_paragraph_spacing(paragraph, heading=style.startswith("Heading"))
        for run in paragraph.findall("w:r", NS):
            polish_run(run, style)

    for table in root.findall(".//w:tbl", NS):
        rows = table.findall("w:tr", NS)
        for row_index, row in enumerate(rows):
            for cell in row.findall("w:tc", NS):
                if row_index == 0:
                    shade_cell(cell, TAG_BLUE)
                for paragraph in cell.findall(".//w:p", NS):
                    set_paragraph_spacing(paragraph, heading=False)
                    for run in paragraph.findall("w:r", NS):
                        polish_run(run, "", header=row_index == 0)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def polish_docx(path: Path) -> None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as handle:
        temp_path = Path(handle.name)

    try:
        with ZipFile(path) as source, ZipFile(temp_path, "w", ZIP_DEFLATED) as target:
            for item in source.infolist():
                data = source.read(item.filename)
                if item.filename == "word/document.xml":
                    data = polish_document(data)
                elif item.filename == "word/styles.xml":
                    data = polish_styles(data)
                target.writestr(item, data)
        shutil.move(str(temp_path), path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    args = parser.parse_args()
    polish_docx(args.docx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
