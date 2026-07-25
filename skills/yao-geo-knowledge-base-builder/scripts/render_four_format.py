#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-knowledge-base-builder
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Render a GEO knowledge-base report to Markdown, HTML, PDF, and DOCX.

The renderer is intentionally conservative for client-facing reports:
- A4 page geometry with fixed table widths.
- HTML/PDF tables use fixed layout and break long tokens.
- DOCX uses manual OpenXML tables instead of pandoc defaults, so Word cannot
  auto-expand wide tables to the right.
- Source-index URL tables are rendered as two-column evidence ledgers in
  visual formats to avoid six-column squeeze.
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PAGE_WIDTH_TWIPS = 11906
PAGE_HEIGHT_TWIPS = 16838
PAGE_MARGIN_TWIPS = 1134
BODY_WIDTH_TWIPS = PAGE_WIDTH_TWIPS - PAGE_MARGIN_TWIPS * 2
ZWSP = "\u200b"
REQUIRED_SECTION_GROUPS = {
    "structured summary": ["结构化摘要"],
    "systematic knowledge-base body": ["系统化品牌知识库"],
    "real data access boundary": ["真实数据获取", "数据获取能力与限制", "真实数据获取与限制"],
    "complete entity inventory": ["完整实体清单"],
    "analysis completeness self-check": ["分析完整性自检", "方法论参考与分析完整性自检"],
    "fact-card library": ["品牌事实卡片库"],
    "prompt input pack": ["Prompt 输入包", "Prompt输入包"],
    "source index": ["来源索引"],
}


@dataclass
class Block:
    kind: str
    value: object
    level: int | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render GEO KB report four-format package.")
    parser.add_argument("--source", required=True, help="Source Markdown report.")
    parser.add_argument("--out-dir", required=True, help="Directory for deliverables.")
    parser.add_argument("--base-name", help="Output basename without extension.")
    parser.add_argument("--quality-report", help="Path for quality-report.json.")
    parser.add_argument("--preview-dir", help="Optional directory for rendered PDF preview PNGs.")
    return parser.parse_args()


def parse_markdown(text: str) -> list[Block]:
    lines = text.splitlines()
    blocks: list[Block] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        heading = re.match(r"^(#{1,4})\s+(.*)$", line)
        if heading:
            blocks.append(Block("heading", heading.group(2).strip(), len(heading.group(1))))
            i += 1
            continue

        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].startswith(">"):
                quote_lines.append(lines[i].lstrip(">").strip())
                i += 1
            blocks.append(Block("quote", "\n".join(quote_lines)))
            continue

        if line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            headers, rows = parse_table(table_lines)
            blocks.append(Block("table", {"headers": headers, "rows": rows}))
            continue

        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:].strip())
                i += 1
            blocks.append(Block("list", items))
            continue

        para_lines = [line.strip()]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if not nxt.strip() or nxt.startswith(("#", ">", "|", "- ")):
                break
            para_lines.append(nxt.strip())
            i += 1
        blocks.append(Block("paragraph", " ".join(para_lines)))
    return blocks


def parse_table(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    def split_row(row: str) -> list[str]:
        row = row.strip().strip("|")
        return [cell.strip() for cell in row.split("|")]

    if len(lines) < 2:
        return [], []
    headers = split_row(lines[0])
    rows = [split_row(line) for line in lines[2:]]
    return headers, rows


def is_source_index(headers: list[str]) -> bool:
    normalized = {normalize_header(h) for h in headers}
    return "url" in normalized and ("来源id" in normalized or "source id" in normalized)


def normalize_header(header: str) -> str:
    return re.sub(r"\s+", " ", header.strip().lower().replace("_", " "))


def header_positions(headers: list[str]) -> dict[str, int]:
    return {normalize_header(header): idx for idx, header in enumerate(headers)}


def is_fact_card_table(headers: list[str]) -> bool:
    normalized = {normalize_header(h) for h in headers}
    return bool({"事实id", "主体"} <= normalized or {"fact id", "subject"} <= normalized)


def is_entity_inventory_table(headers: list[str]) -> bool:
    normalized = {normalize_header(h) for h in headers}
    return bool(
        {"实体id", "实体类型", "标准名称"} <= normalized
        or {"entity id", "entity type", "canonical name"} <= normalized
    )


def entity_inventory_to_compact_table(headers: list[str], rows: list[list[str]]) -> tuple[list[str], list[list[str]]]:
    positions = header_positions(headers)

    def get(row: list[str], *keys: str) -> str:
        for key in keys:
            idx = positions.get(normalize_header(key))
            if idx is not None and idx < len(row):
                return row[idx]
        return ""

    converted = []
    for row in rows:
        entity_id = get(row, "实体ID", "entity id", "id")
        entity_type = get(row, "实体类型", "entity type", "type")
        canonical_name = get(row, "标准名称", "canonical name", "name")
        aliases = get(row, "别名", "aliases", "alias")
        relationship = get(row, "关系", "relationship")
        source = get(row, "来源", "source")
        confidence = get(row, "可信等级", "confidence")
        usage_note = get(row, "使用说明", "usage note", "note")
        converted.append(
            [
                f"{entity_id}\n{entity_type}".strip(),
                f"{canonical_name}\n别名：{aliases}".strip(),
                relationship,
                " / ".join(part for part in [source, confidence] if part),
                usage_note,
            ]
        )
    return ["实体", "标准名称与别名", "关系", "来源/可信", "使用说明"], converted


def fact_card_to_compact_table(headers: list[str], rows: list[list[str]]) -> tuple[list[str], list[list[str]]]:
    positions = header_positions(headers)

    def get(row: list[str], *keys: str) -> str:
        for key in keys:
            idx = positions.get(normalize_header(key))
            if idx is not None and idx < len(row):
                return row[idx]
        return ""

    converted = []
    for row in rows:
        fact_id = get(row, "事实ID", "fact id", "id")
        subject = get(row, "主体", "subject")
        statement = get(row, "事实陈述", "statement", "claim")
        if not statement:
            attribute = get(row, "属性", "attribute")
            value = get(row, "取值", "value")
            evidence = get(row, "证据", "evidence")
            statement = "；".join(part for part in [attribute, value, evidence] if part)
        confidence = get(row, "可信/来源", "可信等级", "confidence")
        source = get(row, "来源", "来源ID", "source", "source id")
        confidence_source = " / ".join(part for part in [confidence, source] if part)
        scenario = get(row, "场景", "可用场景", "scenario", "use case")
        converted.append([fact_id, subject, statement, confidence_source, scenario])
    return ["事实ID", "主体", "事实陈述", "可信/来源", "场景"], converted


def source_index_to_evidence_table(headers: list[str], rows: list[list[str]]) -> tuple[list[str], list[list[str]]]:
    positions = header_positions(headers)

    def get(row: list[str], *keys: str) -> str:
        for key in keys:
            idx = positions.get(normalize_header(key))
            if idx is not None and idx < len(row):
                return row[idx]
        return ""

    converted = []
    for row in rows:
        source_id = get(row, "来源ID", "source id", "source_id")
        title = get(row, "标题", "title")
        publisher = get(row, "发布方", "publisher")
        source_type = get(row, "类型", "type")
        checked_at = get(row, "核验日期", "verified at", "verification date", "checked at")
        url = get(row, "URL")
        converted.append(
            [
                f"{source_id}\n{title}".strip(),
                f"发布方：{publisher}；类型：{source_type}；核验日期：{checked_at}\nURL：{url}",
            ]
        )
    return ["来源", "证据详情"], converted


def escape(text: object) -> str:
    return html_lib.escape(str(text), quote=True)


def soft_wrap_token(token: str) -> str:
    if len(token) < 34:
        return token
    if not re.search(r"(https?://|[./?=&_%:-])", token):
        return token
    return re.sub(r"([/._?=&%:-])", r"\1" + ZWSP, token)


def soft_wrap_text(text: object) -> str:
    parts = re.split(r"(\s+)", str(text))
    return "".join(soft_wrap_token(part) if not part.isspace() else part for part in parts)


def render_inline_html(text: object) -> str:
    # HTML/PDF use CSS wrapping; keep visible/copyable text unchanged.
    escaped = escape(text)
    return escaped.replace("\n", "<br>")


def anchor_id(index: int) -> str:
    return f"section-{index:02d}"


def table_widths(headers: list[str]) -> list[int]:
    col_count = len(headers)
    if col_count == 2:
        return [2200, BODY_WIDTH_TWIPS - 2200]
    if col_count == 3:
        return [1700, 3600, BODY_WIDTH_TWIPS - 5300]
    if col_count == 4:
        return [1700, 2500, 3400, BODY_WIDTH_TWIPS - 7600]
    if col_count == 5 and headers[:2] == ["事实ID", "主体"]:
        return [980, 1640, 3940, 1400, BODY_WIDTH_TWIPS - 7960]
    if col_count == 5:
        return [1450, 1800, 3450, 1280, BODY_WIDTH_TWIPS - 7980]
    equal = BODY_WIDTH_TWIPS // max(1, col_count)
    widths = [equal] * col_count
    widths[-1] += BODY_WIDTH_TWIPS - equal * col_count
    return widths


def render_html(blocks: list[Block], title: str, out_path: Path) -> None:
    body_parts: list[str] = []
    toc_items: list[tuple[int, str, str]] = []
    heading_index = 0
    for block in blocks:
        if block.kind == "heading":
            level = min(block.level or 1, 4)
            heading_index += 1
            current_anchor = anchor_id(heading_index)
            heading_text = str(block.value)
            if 1 < level <= 3:
                toc_items.append((level, current_anchor, heading_text))
            body_parts.append(f'<h{level} id="{current_anchor}">{render_inline_html(heading_text)}</h{level}>')
        elif block.kind == "quote":
            lines = str(block.value).splitlines()
            body_parts.append("<blockquote>" + "<br>".join(render_inline_html(line) for line in lines) + "</blockquote>")
        elif block.kind == "paragraph":
            body_parts.append(f"<p>{render_inline_html(block.value)}</p>")
        elif block.kind == "list":
            items = "".join(f"<li>{render_inline_html(item)}</li>" for item in block.value)  # type: ignore[arg-type]
            body_parts.append(f"<ul>{items}</ul>")
        elif block.kind == "table":
            headers = block.value["headers"]  # type: ignore[index]
            rows = block.value["rows"]  # type: ignore[index]
            if is_source_index(headers):
                headers, rows = source_index_to_evidence_table(headers, rows)
            elif len(headers) > 5 and is_entity_inventory_table(headers):
                headers, rows = entity_inventory_to_compact_table(headers, rows)
            elif len(headers) > 5 and is_fact_card_table(headers):
                headers, rows = fact_card_to_compact_table(headers, rows)
            cols_class = f"cols-{len(headers)}"
            head = "".join(f"<th>{render_inline_html(h)}</th>" for h in headers)
            row_html = []
            for row in rows:
                padded = row + [""] * (len(headers) - len(row))
                row_html.append("<tr>" + "".join(f"<td>{render_inline_html(cell)}</td>" for cell in padded[: len(headers)]) + "</tr>")
            body_parts.append(
                f'<table class="{cols_class}"><thead><tr>{head}</tr></thead><tbody>{"".join(row_html)}</tbody></table>'
            )

    toc_html = "".join(
        f'<a class="toc-link toc-level-{level}" href="#{anchor}">{render_inline_html(text)}</a>'
        for level, anchor, text in toc_items
    )

    css = """
@page {
  size: A4;
  margin: 20mm 22mm 22mm 22mm;
  background: #ffffff;
  @bottom-center {
    content: counter(page) "  ·  " string(doc-title);
    font-family: "Source Han Sans SC", "Noto Sans CJK SC", "PingFang SC", Arial, sans-serif;
    font-size: 8.5pt;
    color: #87867f;
  }
}
@page:first {
  @bottom-center { content: ""; }
}
* { box-sizing: border-box; }
:root {
  --paper: #ffffff;
  --ivory: #faf9f5;
  --brand: #1B365D;
  --near-black: #141413;
  --dark-warm: #3d3d3a;
  --charcoal: #4d4c48;
  --olive: #5e5d59;
  --stone: #87867f;
  --border: #e8e6dc;
  --border-soft: #e5e3d8;
  --tag-bg: #EEF2F7;
}
html, body { margin: 0; padding: 0; background: var(--paper); color: var(--near-black); }
body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Source Han Sans SC", "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.55;
}
.shell {
  display: grid;
  grid-template-columns: 264px minmax(0, 900px);
  gap: 32px;
  max-width: 1220px;
  margin: 0 auto;
  padding: 0 28px;
  align-items: start;
}
.toc {
  position: sticky;
  top: 0;
  max-height: 100vh;
  overflow: auto;
  padding: 28px 18px 28px 0;
  border-right: 0.5pt solid var(--border);
  background: var(--paper);
}
.toc-title {
  color: var(--brand);
  font-family: "Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", Georgia, serif;
  font-size: 12pt;
  font-weight: 500;
  margin: 0 0 14px;
  border-left: 2.5pt solid var(--brand);
  padding-left: 8px;
}
.toc-link {
  display: block;
  color: var(--charcoal);
  text-decoration: none;
  border-left: 2px solid transparent;
  padding: 5px 8px 5px 10px;
  margin: 0 0 2px;
  line-height: 1.35;
  overflow-wrap: anywhere;
  border-radius: 2px;
}
.toc-link:hover { color: var(--brand); border-left-color: var(--brand); background: var(--tag-bg); }
.toc-level-3 { padding-left: 22px; font-size: 9pt; color: var(--olive); }
.page { min-width: 0; max-width: 900px; margin: 0 auto; padding: 32px 0 46px; }
h1, h2, h3, h4 {
  font-family: "Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", Georgia, serif;
  font-weight: 500;
  line-height: 1.25;
  margin: 0 0 10px;
  page-break-after: avoid;
  break-after: avoid;
}
h1 {
  string-set: doc-title content(text);
  font-size: 23pt;
  margin-top: 0;
  margin-bottom: 18pt;
  padding-left: 9pt;
  border-left: 2.5pt solid var(--brand);
  color: var(--near-black);
  letter-spacing: 0;
}
h2 {
  font-size: 15.5pt;
  margin-top: 28pt;
  margin-bottom: 9pt;
  padding-left: 8pt;
  border-left: 2.5pt solid var(--brand);
  color: var(--near-black);
}
h3 { font-size: 12.5pt; margin-top: 18pt; margin-bottom: 6pt; color: var(--dark-warm); }
h4 { font-size: 11pt; margin-top: 14pt; margin-bottom: 5pt; color: var(--dark-warm); }
p { margin: 0 0 10pt; overflow-wrap: anywhere; word-break: break-word; color: var(--near-black); }
blockquote {
  margin: 12pt 0 18pt;
  padding: 7pt 12pt 7pt 14pt;
  border-left: 2pt solid var(--brand);
  background: var(--ivory);
  color: var(--olive);
  overflow-wrap: anywhere;
  break-inside: avoid;
}
ul { margin: 0 0 14px 1.15em; padding: 0; }
li { margin: 0 0 6px; overflow-wrap: anywhere; }
li::marker { color: var(--brand); }
table {
  width: 100%;
  max-width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  margin: 10pt 0 18pt;
  page-break-inside: auto;
  font-size: 9.1pt;
  line-height: 1.42;
  color: var(--charcoal);
}
thead { display: table-header-group; }
tr { page-break-inside: avoid; break-inside: avoid; }
th, td {
  border: 0.5pt solid var(--border);
  padding: 6pt 7pt;
  vertical-align: top;
  text-align: left;
  white-space: normal;
  overflow-wrap: anywhere;
  word-break: break-word;
  hyphens: auto;
}
th {
  background: var(--tag-bg);
  color: var(--brand);
  font-weight: 600;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Source Han Sans SC", "PingFang SC", Arial, sans-serif;
}
tbody tr:nth-child(even) td { background: #faf9f5; }
.cols-5 { font-size: 8.65pt; line-height: 1.38; }
.cols-4 { font-size: 8.95pt; }
.cols-2 { font-size: 9.3pt; }
@media (max-width: 980px) {
  .shell { display: block; padding: 0 18px; }
  .toc {
    z-index: 10;
    border-right: 0;
    border-bottom: 0.5pt solid var(--border);
    padding: 10px 0;
    max-height: 34vh;
  }
  .toc-title { margin: 0 0 6px; }
  .page { padding-top: 18px; }
}
@media print {
  .toc { display: none; }
  .shell { display: block; max-width: none; padding: 0; }
  .page { max-width: none; padding: 0; }
}
"""
    document = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>{css}</style>
</head>
<body>
  <div class="shell">
    <nav class="toc" aria-label="报告目录">
      <div class="toc-title">报告目录</div>
      {toc_html}
    </nav>
    <main class="page">
      {''.join(body_parts)}
    </main>
  </div>
</body>
</html>
"""
    out_path.write_text(document, encoding="utf-8")


def w_text(text: object) -> str:
    return escape(soft_wrap_text(text))


def run_xml(text: object, bold: bool = False, color: str = "141413", size: int = 21) -> str:
    bold_xml = "<w:b/>" if bold else ""
    return (
        "<w:r><w:rPr>"
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Songti SC"/>'
        f'<w:color w:val="{color}"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/>{bold_xml}'
        f"</w:rPr><w:t xml:space=\"preserve\">{w_text(text)}</w:t></w:r>"
    )


def paragraph_xml(text: object, style: str = "Body", bullet: bool = False) -> str:
    size = {"Title": 32, "Heading1": 27, "Heading2": 24, "Heading3": 22, "Quote": 20}.get(style, 21)
    color = "1B365D" if style in {"Title", "Heading1", "Heading2", "Heading3"} else "141413"
    bold = style in {"Title", "Heading1", "Heading2", "Heading3"}
    before = {"Title": 0, "Heading1": 260, "Heading2": 210, "Heading3": 160, "Quote": 70}.get(style, 0)
    after = {"Title": 180, "Heading1": 110, "Heading2": 90, "Heading3": 70, "Quote": 100}.get(style, 80)
    line = 336 if style in {"Title", "Heading1"} else 312
    content = f"- {text}" if bullet else str(text)
    runs = []
    parts = content.split("\n")
    for idx, part in enumerate(parts):
        runs.append(run_xml(part, bold=bold, color=color, size=size))
        if idx < len(parts) - 1:
            runs.append("<w:r><w:br/></w:r>")
    return (
        "<w:p><w:pPr>"
        f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
        "</w:pPr>"
        + "".join(runs)
        + "</w:p>"
    )


def cell_xml(text: object, width: int, header: bool = False) -> str:
    shading = '<w:shd w:fill="EEF2F7"/>' if header else ""
    size = 19 if header else 18
    color = "1B365D" if header else "141413"
    lines = str(text).split("\n")
    paragraphs = []
    for line in lines:
        paragraphs.append(
            "<w:p><w:pPr>"
            '<w:spacing w:before="0" w:after="40" w:line="276" w:lineRule="auto"/>'
            "</w:pPr>"
            + run_xml(line, bold=header, color=color, size=size)
            + "</w:p>"
        )
    return (
        "<w:tc>"
        f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shading}</w:tcPr>'
        + "".join(paragraphs)
        + "</w:tc>"
    )


def table_xml(headers: list[str], rows: list[list[str]]) -> str:
    if is_source_index(headers):
        headers, rows = source_index_to_evidence_table(headers, rows)
    elif len(headers) > 5 and is_entity_inventory_table(headers):
        headers, rows = entity_inventory_to_compact_table(headers, rows)
    elif len(headers) > 5 and is_fact_card_table(headers):
        headers, rows = fact_card_to_compact_table(headers, rows)
    widths = table_widths(headers)
    grid = "".join(f'<w:gridCol w:w="{width}"/>' for width in widths)
    borders = (
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="E8E6DC"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="E8E6DC"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="E8E6DC"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="E8E6DC"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E8E6DC"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="E8E6DC"/>'
        "</w:tblBorders>"
    )
    cell_mar = (
        "<w:tblCellMar>"
        '<w:top w:w="90" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
        '<w:bottom w:w="90" w:type="dxa"/><w:right w:w="90" w:type="dxa"/>'
        "</w:tblCellMar>"
    )
    tbl = [
        "<w:tbl>",
        "<w:tblPr>",
        f'<w:tblW w:w="{BODY_WIDTH_TWIPS}" w:type="dxa"/>',
        '<w:tblLayout w:type="fixed"/>',
        borders,
        cell_mar,
        "</w:tblPr>",
        f"<w:tblGrid>{grid}</w:tblGrid>",
    ]
    tbl.append("<w:tr>" + "".join(cell_xml(header, widths[i], header=True) for i, header in enumerate(headers)) + "</w:tr>")
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        tbl.append("<w:tr>" + "".join(cell_xml(padded[i], widths[i]) for i in range(len(headers))) + "</w:tr>")
    tbl.append("</w:tbl>")
    return "".join(tbl)


def render_docx(blocks: list[Block], out_path: Path) -> None:
    content: list[str] = []
    for block in blocks:
        if block.kind == "heading":
            level = block.level or 1
            style = "Title" if level == 1 else f"Heading{min(level - 1, 3)}"
            content.append(paragraph_xml(block.value, style=style))
        elif block.kind == "quote":
            content.append(paragraph_xml(block.value, style="Quote"))
        elif block.kind == "paragraph":
            content.append(paragraph_xml(block.value))
        elif block.kind == "list":
            for item in block.value:  # type: ignore[union-attr]
                content.append(paragraph_xml(item, bullet=True))
        elif block.kind == "table":
            content.append(table_xml(block.value["headers"], block.value["rows"]))  # type: ignore[index]

    sect = (
        "<w:sectPr>"
        f'<w:pgSz w:w="{PAGE_WIDTH_TWIPS}" w:h="{PAGE_HEIGHT_TWIPS}"/>'
        f'<w:pgMar w:top="{PAGE_MARGIN_TWIPS}" w:right="{PAGE_MARGIN_TWIPS}" '
        f'w:bottom="{PAGE_MARGIN_TWIPS}" w:left="{PAGE_MARGIN_TWIPS}" '
        'w:header="708" w:footer="708" w:gutter="0"/>'
        "</w:sectPr>"
    )
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        "<w:body>"
        + "".join(content)
        + sect
        + "</w:body></w:document>"
    )
    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Songti SC"/><w:sz w:val="21"/></w:rPr>'
        "</w:style>"
        "</w:styles>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        "</Types>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        "</Relationships>"
    )
    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'
    )

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("word/document.xml", document_xml)
        zf.writestr("word/styles.xml", styles_xml)
        zf.writestr("word/_rels/document.xml.rels", doc_rels)


def render_pdf(html_path: Path, pdf_path: Path) -> tuple[bool, str]:
    try:
        from weasyprint import HTML

        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        return True, "weasyprint"
    except Exception as exc:  # pragma: no cover - depends on local system libs
        return False, str(exc)


def pdf_page_count(pdf_path: Path) -> int | None:
    try:
        from pypdf import PdfReader

        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        return None


def render_pdf_previews(pdf_path: Path, preview_dir: Path) -> list[Path]:
    if not shutil.which("pdftoppm"):
        return []
    preview_dir.mkdir(parents=True, exist_ok=True)
    for old in preview_dir.glob("page-*.png"):
        old.unlink()
    prefix = preview_dir / "page"
    subprocess.run(["pdftoppm", "-png", "-r", "120", str(pdf_path), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    normalized_paths = []
    for raw_path in sorted(preview_dir.glob("page-*.png")):
        match = re.match(r"page-(\d+)\.png$", raw_path.name)
        if not match:
            normalized_paths.append(raw_path)
            continue
        normalized_path = preview_dir / f"page-{int(match.group(1))}.png"
        if raw_path != normalized_path:
            raw_path.rename(normalized_path)
        normalized_paths.append(normalized_path)
    return sorted(normalized_paths, key=lambda path: int(re.search(r"page-(\d+)\.png$", path.name).group(1)))


def image_right_edge_clear(image_paths: Iterable[Path]) -> tuple[bool | None, str]:
    try:
        from PIL import Image
    except Exception:
        return None, "Pillow unavailable; skipped pixel edge scan."

    offenders = []
    for path in image_paths:
        with Image.open(path).convert("RGB") as img:
            width, height = img.size
            edge = img.crop((width - 8, 0, width, height))
            non_white = 0
            pixels = edge.get_flattened_data() if hasattr(edge, "get_flattened_data") else edge.getdata()
            for pixel in pixels:
                if min(pixel) < 245:
                    non_white += 1
            if non_white > 12:
                offenders.append(f"{path.name}:{non_white}")
    if offenders:
        return False, "Right-edge ink detected: " + ", ".join(offenders[:6])
    return True, "No non-white content in the rightmost 8px of rendered PDF pages."


def inspect_docx(docx_path: Path) -> dict:
    with zipfile.ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8")
    table_count = xml.count("<w:tbl>")
    fixed_count = xml.count('w:type="fixed"')
    dxa_width_count = xml.count(f'<w:tblW w:w="{BODY_WIDTH_TWIPS}" w:type="dxa"')
    nowrap_count = xml.count("<w:noWrap")
    text_only = re.sub(r"<[^>]+>", " ", xml)
    text_only = html_lib.unescape(text_only)
    segments = re.split(r"[\s" + ZWSP + r"]+", text_only)
    longest_segment = max((len(segment) for segment in segments), default=0)
    grid_sums = []
    for tbl_xml in re.findall(r"<w:tbl>.*?</w:tbl>", xml):
        widths = [int(value) for value in re.findall(r'<w:gridCol w:w="(\d+)"', tbl_xml)]
        if widths:
            grid_sums.append(sum(widths))
    return {
        "table_count": table_count,
        "fixed_table_count": fixed_count,
        "dxa_table_width_count": dxa_width_count,
        "nowrap_count": nowrap_count,
        "longest_unbreakable_segment": longest_segment,
        "max_grid_width_twips": max(grid_sums, default=0),
        "all_grid_widths_within_body": all(width <= BODY_WIDTH_TWIPS for width in grid_sums),
    }


def inspect_markdown_structure(markdown_path: Path) -> dict:
    text = markdown_path.read_text("utf-8") if markdown_path.exists() else ""
    headings = re.findall(r"^#{1,4}\s+(.+)$", text, flags=re.MULTILINE)
    section_results = {}
    for group, candidates in REQUIRED_SECTION_GROUPS.items():
        section_results[group] = any(any(candidate in heading for candidate in candidates) for heading in headings)
    return {
        "headings": headings,
        "section_results": section_results,
        "all_required_sections_present": all(section_results.values()),
    }


def build_quality_report(paths: dict[str, Path], preview_paths: list[Path], pdf_renderer: str) -> dict:
    checks = []

    for label, path in paths.items():
        checks.append({"name": f"{label} exists and is non-empty", "passed": path.exists() and path.stat().st_size > 0, "detail": str(path)})

    html_text = paths["html"].read_text("utf-8") if paths["html"].exists() else ""
    checks.append({"name": "html has no absolute local paths", "passed": "/Users/" not in html_text, "detail": "No local path leakage."})
    checks.append({"name": "html tables force wrapping", "passed": "overflow-wrap: anywhere" in html_text and "table-layout: fixed" in html_text, "detail": "CSS includes fixed table layout and long-token wrapping."})
    checks.append({"name": "html has sticky menu", "passed": 'class="toc"' in html_text and "position: sticky" in html_text, "detail": "HTML report includes a sticky navigation menu for screen reading."})
    checks.append({"name": "html follows kami editorial tokens", "passed": "--brand: #1B365D" in html_text and "--ivory: #faf9f5" in html_text and "line-height: 1.55" in html_text, "detail": "HTML uses the kami-style ink-blue, warm neutral, and compact editorial rhythm while preserving white report background."})
    checks.append({"name": "html print mode hides sticky menu", "passed": "@media print" in html_text and ".toc { display: none; }" in html_text, "detail": "PDF/print output excludes the screen-only sticky menu."})

    markdown_info = inspect_markdown_structure(paths["markdown"]) if paths["markdown"].exists() else {}
    checks.append(
        {
            "name": "markdown contains required systematic KB sections",
            "passed": bool(markdown_info.get("all_required_sections_present")),
            "detail": markdown_info.get("section_results", {}),
        }
    )
    checks.append(
        {
            "name": "markdown contains complete entity inventory",
            "passed": bool(markdown_info.get("section_results", {}).get("complete entity inventory")),
            "detail": "Complete entity inventory section is mandatory.",
        }
    )
    checks.append(
        {
            "name": "markdown explains real data access boundary",
            "passed": bool(markdown_info.get("section_results", {}).get("real data access boundary")),
            "detail": "Reports must explain which data was actually accessible, which mode was used, and which claims remain inaccessible or pending.",
        }
    )

    docx_info = inspect_docx(paths["docx"]) if paths["docx"].exists() else {}
    checks.extend(
        [
            {"name": "docx contains fixed tables", "passed": docx_info.get("table_count", 0) == docx_info.get("fixed_table_count", -1), "detail": docx_info},
            {"name": "docx table width uses A4 body dxa", "passed": docx_info.get("table_count", 0) == docx_info.get("dxa_table_width_count", -1), "detail": docx_info},
            {"name": "docx grid widths stay inside page body", "passed": bool(docx_info.get("all_grid_widths_within_body")), "detail": docx_info},
            {"name": "docx has no nowrap cells", "passed": docx_info.get("nowrap_count", 1) == 0, "detail": docx_info},
            {"name": "docx long tokens are soft-wrapped", "passed": docx_info.get("longest_unbreakable_segment", 999) <= 80, "detail": docx_info},
        ]
    )

    page_count = pdf_page_count(paths["pdf"]) if paths["pdf"].exists() else None
    checks.append({"name": "pdf readable", "passed": bool(page_count and page_count > 0), "detail": {"pages": page_count, "renderer": pdf_renderer}})
    checks.append({"name": "pdf preview rendered", "passed": bool(preview_paths), "detail": f"{len(preview_paths)} preview page(s) generated."})
    if preview_paths:
        edge_ok, edge_detail = image_right_edge_clear(preview_paths)
        checks.append({"name": "pdf right-edge visual overflow scan", "passed": edge_ok is not False, "detail": edge_detail})

    return {"passed": all(check["passed"] for check in checks), "checks": checks}


def main() -> None:
    args = parse_args()
    source = Path(args.source)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    base_name = args.base_name or source.stem

    markdown = source.read_text(encoding="utf-8")
    blocks = parse_markdown(markdown)
    title = next((str(block.value) for block in blocks if block.kind == "heading" and block.level == 1), base_name)

    paths = {
        "markdown": out_dir / f"{base_name}.md",
        "html": out_dir / f"{base_name}.html",
        "pdf": out_dir / f"{base_name}.pdf",
        "docx": out_dir / f"{base_name}.docx",
    }
    paths["markdown"].write_text(markdown, encoding="utf-8")
    render_html(blocks, title, paths["html"])
    render_docx(blocks, paths["docx"])
    pdf_ok, pdf_renderer = render_pdf(paths["html"], paths["pdf"])
    if not pdf_ok:
        raise RuntimeError(f"PDF render failed: {pdf_renderer}")

    preview_paths: list[Path] = []
    preview_dir = Path(args.preview_dir) if args.preview_dir else None
    if preview_dir:
        preview_paths = render_pdf_previews(paths["pdf"], preview_dir)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            preview_paths = render_pdf_previews(paths["pdf"], Path(tmp))
            # The files are deleted with tmp; still enough for the edge scan now.
            quality = build_quality_report(paths, preview_paths, pdf_renderer)
            preview_paths = []

    if args.preview_dir:
        quality = build_quality_report(paths, preview_paths, pdf_renderer)

    quality_path = Path(args.quality_report) if args.quality_report else out_dir.parent / "quality-report.json"
    quality_path.write_text(json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8")
    if not quality["passed"]:
        failed = [check["name"] for check in quality["checks"] if not check["passed"]]
        raise SystemExit("Quality checks failed: " + ", ".join(failed))
    print(json.dumps({"outputs": {k: str(v) for k, v in paths.items()}, "quality": str(quality_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
