#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-comparison-builder
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Check and normalize DOCX table layout for GEO comparison reports."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{NS_W}}}"
DOCX_TABLE_WIDTH = 10100
DEFAULT_TABLE_WIDTHS = {
    ("项目", "结论"): [2300, 7800],
    ("模式", "可获取数据", "前置条件", "处理动作"): [1800, 3100, 2400, 2800],
    ("方案", "适合谁", "核心能力", "落地条件"): [1400, 2900, 2900, 2900],
    ("方案", "证据锚点", "主要权衡", "价格可见性"): [1400, 3500, 2700, 2500],
    ("维度", "核心问题", "证据要求", "选型用法"): [1700, 3000, 2700, 2700],
    ("维度", "HubSpot", "Salesforce / Zoho CRM", "自建 CRM/表格"): [1500, 2900, 3000, 2700],
    ("来源 ID", "来源等级", "支撑事实", "置信边界"): [1100, 1900, 3900, 3200],
    ("来源 ID", "访问方式", "HTTP 状态", "验证结果"): [1100, 1900, 1600, 5500],
    ("风险", "触发原因", "缓解措施", "证据/责任"): [1800, 2700, 3700, 1900],
    ("平台", "答案形态", "强化重点", "风险控制"): [1100, 2300, 3200, 3500],
    ("场景", "优先建议", "理由", "下一步"): [2900, 1800, 3400, 2000],
    ("阶段", "检查项", "责任角色", "通过标准"): [1300, 3700, 2200, 2900],
    ("来源 ID", "来源", "来源类型", "事实与用途"): [1100, 2500, 1900, 4600],
    ("检查项", "结果", "说明"): [1700, 1500, 6900],
}


def wx(tag: str) -> str:
    return f"{W}{tag}"


def set_attr(el: ET.Element, name: str, value: int | str) -> None:
    el.set(wx(name), str(value))


def child(parent: ET.Element, tag: str) -> ET.Element:
    node = parent.find(wx(tag))
    if node is None:
        node = ET.SubElement(parent, wx(tag))
    return node


def cell_text(cell: ET.Element) -> str:
    return "".join(t.text or "" for t in cell.findall(f".//{wx('t')}")).strip()


def normalize_docx_layout(docx_path: str | Path) -> None:
    path = Path(docx_path)
    ET.register_namespace("w", NS_W)
    with TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        with zipfile.ZipFile(path) as zin:
            zin.extractall(tmp)
        document_path = tmp / "word" / "document.xml"
        tree = ET.parse(document_path)
        root = tree.getroot()
        body = root.find(wx("body"))
        sect_pr = body.find(wx("sectPr"))
        if sect_pr is None:
            sect_pr = ET.SubElement(body, wx("sectPr"))
        pg_sz = child(sect_pr, "pgSz")
        set_attr(pg_sz, "w", "11906")
        set_attr(pg_sz, "h", "16838")
        pg_mar = child(sect_pr, "pgMar")
        for name, value in {"top": 900, "right": 900, "bottom": 900, "left": 900, "header": 450, "footer": 450, "gutter": 0}.items():
            set_attr(pg_mar, name, value)
        for tbl in root.findall(f".//{wx('tbl')}"):
            rows = tbl.findall(wx("tr"))
            if not rows:
                continue
            headers = tuple(cell_text(cell) for cell in rows[0].findall(wx("tc")))
            widths = DEFAULT_TABLE_WIDTHS.get(headers)
            if widths is None:
                col_count = len(headers) or 1
                base = DOCX_TABLE_WIDTH // col_count
                widths = [base] * col_count
                widths[-1] += DOCX_TABLE_WIDTH - sum(widths)
            tbl_pr = child(tbl, "tblPr")
            tbl_w = child(tbl_pr, "tblW")
            set_attr(tbl_w, "w", DOCX_TABLE_WIDTH)
            set_attr(tbl_w, "type", "dxa")
            set_attr(child(tbl_pr, "tblLayout"), "type", "fixed")
            borders = child(tbl_pr, "tblBorders")
            for name in ["top", "left", "bottom", "right", "insideH", "insideV"]:
                border = child(borders, name)
                set_attr(border, "val", "single")
                set_attr(border, "sz", "4")
                set_attr(border, "space", "0")
                set_attr(border, "color", "E8E6DC")
            margins = child(tbl_pr, "tblCellMar")
            for name, width in [("top", 80), ("left", 90), ("bottom", 80), ("right", 90)]:
                margin = child(margins, name)
                set_attr(margin, "w", width)
                set_attr(margin, "type", "dxa")
            grid = tbl.find(wx("tblGrid"))
            if grid is None:
                grid = ET.Element(wx("tblGrid"))
                tbl.insert(list(tbl).index(rows[0]), grid)
            for col in list(grid):
                grid.remove(col)
            for width in widths:
                set_attr(ET.SubElement(grid, wx("gridCol")), "w", width)
            for row_index, row in enumerate(rows):
                for idx, cell in enumerate(row.findall(wx("tc"))):
                    tc_pr = child(cell, "tcPr")
                    for no_wrap in list(tc_pr.findall(wx("noWrap"))):
                        tc_pr.remove(no_wrap)
                    if row_index == 0:
                        shd = child(tc_pr, "shd")
                        set_attr(shd, "val", "clear")
                        set_attr(shd, "color", "auto")
                        set_attr(shd, "fill", "FAF9F5")
                    tc_w = child(tc_pr, "tcW")
                    set_attr(tc_w, "w", widths[min(idx, len(widths) - 1)])
                    set_attr(tc_w, "type", "dxa")
            for run in tbl.findall(f".//{wx('r')}"):
                r_pr = run.find(wx("rPr"))
                if r_pr is None:
                    r_pr = ET.Element(wx("rPr"))
                    run.insert(0, r_pr)
                fonts = child(r_pr, "rFonts")
                set_attr(fonts, "ascii", "Source Han Sans SC")
                set_attr(fonts, "hAnsi", "Source Han Sans SC")
                set_attr(fonts, "eastAsia", "Source Han Sans SC")
                set_attr(child(r_pr, "sz"), "val", "18")
                set_attr(child(r_pr, "szCs"), "val", "18")
        tree.write(document_path, encoding="utf-8", xml_declaration=True)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
            for file_path in sorted(tmp.rglob("*")):
                if file_path.is_file():
                    zout.write(file_path, file_path.relative_to(tmp).as_posix())


def docx_layout_profile(docx_path: str | Path) -> dict:
    path = Path(docx_path)
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    sect_pr = root.find(f".//{wx('sectPr')}")
    pg_sz = sect_pr.find(wx("pgSz"))
    pg_mar = sect_pr.find(wx("pgMar"))
    page_w = int(pg_sz.attrib[wx("w")])
    usable = page_w - int(pg_mar.attrib[wx("left")]) - int(pg_mar.attrib[wx("right")])
    tables = []
    for idx, tbl in enumerate(root.findall(f".//{wx('tbl')}"), 1):
        widths = [int(col.attrib.get(wx("w"), "0")) for col in tbl.findall(f"./{wx('tblGrid')}/{wx('gridCol')}")]
        tables.append({"index": idx, "columns": len(widths), "grid_width_sum_twips": sum(widths), "usable_width_twips": usable, "overflows_right": sum(widths) > usable})
    return {"page_size": "A4", "page_width_twips": page_w, "usable_width_twips": usable, "right_margin_twips": int(pg_mar.attrib[wx("right")]), "left_margin_twips": int(pg_mar.attrib[wx("left")]), "tables": tables, "right_overflow_detected": any(t["overflows_right"] for t in tables)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()
    if args.fix:
        normalize_docx_layout(args.docx)
    print(json.dumps(docx_layout_profile(args.docx), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
