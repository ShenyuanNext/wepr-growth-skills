#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-page-blueprint
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as xe

from weasyprint import HTML

REQ = ["title", "brand_name", "page_type", "target_question", "analysis_date", "summary_cards", "sections"]
KEYWORDS = [
    "GEO 页面设计方案",
    "输入、假设与边界",
    "真实数据接入与核验计划",
    "查询意图与 Query Fan-out 覆盖",
    "页面模块与信息架构图",
    "研究依据与页面设计原则",
    "实体关系与知识图谱字段",
    "证据区与来源台账",
    "AI 可抽取模块设计",
    "用户转化模块设计",
    "HTML 结构样例",
    "Schema 建议",
    "CMS 字段清单",
    "无障碍与页面体验要求",
    "实施验收与监测计划",
    "移动端",
    "公众号",
    "FAQPage 正文可见",
]
REPORT_NOTICE_MD = """<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-blueprint
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->"""
REPORT_NOTICE_HTML = "<!-- Copyright © 2026 姚金刚. All rights reserved. Project: yao-geo-page-blueprint. -->"

DOCX_PAGE_WIDTH = 11906
DOCX_MARGIN = 1020
DOCX_TEXT_WIDTH = DOCX_PAGE_WIDTH - DOCX_MARGIN * 2
DOCX_TABLE_WIDTH = 8800
DOCX_CELL_MARGIN = 110
SOFT_BREAK = "\u200b"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "yao-geo-page-blueprint"


def load_data(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = [key for key in REQ if key not in data]
    if missing:
        raise ValueError(f"Missing keys: {missing}")
    for section in data["sections"]:
        if section.get("table"):
            cols = len(section["table"]["headers"])
            for row in section["table"].get("rows", []):
                if len(row) != cols:
                    raise ValueError(f"Table row mismatch: {section['title']}")
    return data


def md_table(table: dict[str, Any]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", "<br>")

    rows = [
        "| " + " | ".join(cell(header) for header in table["headers"]) + " |",
        "| " + " | ".join("---" for _ in table["headers"]) + " |",
    ]
    rows += ["| " + " | ".join(cell(value) for value in row) + " |" for row in table.get("rows", [])]
    return "\n".join(rows)


def render_md(data: dict[str, Any]) -> str:
    out = [
        REPORT_NOTICE_MD,
        "",
        f"# {data['title']}",
        "",
        data.get("subtitle", ""),
        "",
        f"- 品牌：{data['brand_name']}",
        f"- 页面类型：{data['page_type']}",
        f"- 目标问题：{data['target_question']}",
        f"- 生成日期：{data['analysis_date']}",
        "",
        "## 封面摘要",
        "",
    ]
    for card in data["summary_cards"]:
        out += [f"### {card['label']}", "", f"**{card['value']}**", "", card.get("note", ""), ""]
    for section in data["sections"]:
        out += [f"## {section['title']}", ""]
        out += [str(paragraph) + "\n" for paragraph in section.get("paragraphs", [])]
        out += [f"- {bullet}" for bullet in section.get("bullets", [])]
        if section.get("bullets"):
            out.append("")
        if section.get("table"):
            out += [md_table(section["table"]), ""]
        for block in section.get("code_blocks", []):
            out += [
                f"**{block.get('title', '代码样例')}**",
                "",
                f"```{block.get('language', '')}",
                block.get("code", ""),
                "```",
                "",
            ]
    return "\n".join(out).strip() + "\n"


def html_table(table: dict[str, Any]) -> str:
    th = "".join(f"<th>{html.escape(str(header))}</th>" for header in table["headers"])
    trs = [
        "<tr>"
        + "".join(f"<td>{html.escape(str(value)).replace(chr(10), '<br>')}</td>" for value in row)
        + "</tr>"
        for row in table.get("rows", [])
    ]
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


def render_html(data: dict[str, Any]) -> str:
    cards = "".join(
        f"<article><p>{html.escape(card['label'])}</p><h3>{html.escape(card['value'])}</h3><span>{html.escape(card.get('note', ''))}</span></article>"
        for card in data["summary_cards"]
    )
    nav: list[str] = []
    body: list[str] = []
    for index, section in enumerate(data["sections"], 1):
        sid = html.escape(section.get("id", f"s{index}"))
        title = html.escape(section["title"])
        nav.append(f'<a href="#{sid}"><b>{index:02d}</b>{title}</a>')
        parts = [f'<section id="{sid}"><p class="k">模块 {index:02d}</p><h2>{title}</h2>']
        parts += [f"<p>{html.escape(str(paragraph))}</p>" for paragraph in section.get("paragraphs", [])]
        if section.get("bullets"):
            parts.append("<ul>" + "".join(f"<li>{html.escape(str(bullet))}</li>" for bullet in section["bullets"]) + "</ul>")
        if section.get("table"):
            parts.append(html_table(section["table"]))
        for block in section.get("code_blocks", []):
            parts.append(
                f'<figure><figcaption>{html.escape(block.get("title", "代码样例"))}</figcaption><pre><code>{html.escape(block.get("code", ""))}</code></pre></figure>'
            )
        parts.append("</section>")
        body.append("\n".join(parts))

    css = (
        ':root{--paper:#fff;--ivory:#faf9f5;--warm-sand:#e8e6dc;--ink:#1B365D;--near:#141413;--dark:#3d3d3a;--olive:#5e5d59;--stone:#87867f;--border:#e8e5da;--border-strong:#d1cfc5;--tag:#EEF2F7}'
        '*{box-sizing:border-box}html,body{margin:0;background:#fff;color:var(--near);font-family:"Inter","Source Han Sans SC","PingFang SC","Microsoft YaHei",Arial,sans-serif;line-height:1.52}.page{width:min(1120px,calc(100vw - 40px));margin:0 auto;padding:46px 0 78px;background:#fff}'
        'header{padding:4px 0 30px;border-bottom:1px solid var(--border-strong)}h1,h2{font-family:"Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;font-weight:500;color:var(--near)}h1{margin:0 0 12px;font-size:42px;line-height:1.14;letter-spacing:0}header>p:not(.k){max-width:860px;margin:0 0 14px;color:var(--olive);font-size:17px;line-height:1.5}.meta{display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:18px 0 0;list-style:none}.meta li{border:1px solid var(--border);background:var(--ivory);border-radius:6px;padding:5px 10px;color:var(--dark);font-size:13px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:24px 0 18px}article{border:1px solid var(--border);border-radius:8px;background:var(--ivory);padding:16px 18px}article p{margin:0 0 7px;color:var(--ink);font-size:12px;font-weight:600}article h3{margin:0 0 7px;font-family:"Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;font-size:22px;font-weight:500;line-height:1.22;color:var(--near)}article span{color:var(--olive);font-size:13px;line-height:1.45}.toc-bar{position:sticky;top:0;z-index:20;margin:20px 0 8px;padding:12px 0 14px;border-bottom:1px solid var(--border);background:#fff}.toc-bar h2{margin:0 0 8px;padding:0;border:0;font-family:"Inter","Source Han Sans SC","PingFang SC","Microsoft YaHei",Arial,sans-serif;font-size:15px;font-weight:600;line-height:1.25;color:var(--dark)}.toc-nav{display:flex;gap:8px;overflow-x:auto;padding-bottom:2px;scrollbar-width:thin}.toc-nav a{flex:0 0 auto;display:flex;gap:8px;max-width:260px;border:1px solid var(--border);border-radius:6px;background:var(--ivory);padding:7px 10px;color:var(--dark);text-decoration:none;overflow-wrap:anywhere;white-space:normal;line-height:1.35}.toc-nav b{color:var(--ink);font-weight:600}.toc-nav a:focus{outline:2px solid var(--ink);outline-offset:2px}section{scroll-margin-top:82px;padding:30px 0 8px;border-bottom:1px solid var(--border);break-inside:avoid}.k{display:inline-block;margin:0 0 7px;border-radius:4px;background:var(--tag);padding:2px 6px;color:var(--ink);font-size:11px;font-weight:600;letter-spacing:0}h2{margin:0 0 12px;border-left:4px solid var(--ink);border-radius:2px;padding-left:10px;font-size:24px;line-height:1.22}p,li{overflow-wrap:anywhere;color:var(--dark)}p{margin:0 0 10px}ul{margin:8px 0 12px;padding-left:20px}.table-wrap{width:100%;overflow-x:auto;margin:14px 0 18px;border:1px solid var(--border-strong);border-radius:8px;background:#fff}table{width:100%;border-collapse:collapse;table-layout:fixed;background:#fff}th,td{border:1px solid var(--border);padding:8px 10px;text-align:left;vertical-align:top;overflow-wrap:anywhere;word-break:break-word;line-height:1.45;font-size:13px}th{background:#f3f0e8;color:var(--ink);font-weight:600}figure{margin:16px 0 20px;border:1px solid var(--border-strong);border-radius:8px;background:#fff;overflow:hidden}figcaption{border-bottom:1px solid var(--border);background:var(--ivory);padding:8px 10px;color:var(--ink);font-weight:600}pre{margin:0;padding:12px;overflow-x:auto;white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;line-height:1.45;background:#fff;color:var(--near)}@media(max-width:720px){.page{width:min(100vw - 24px,1120px);padding-top:24px}h1{font-size:30px}.cards{grid-template-columns:1fr}.toc-nav a{max-width:220px}th,td{min-width:140px}}@media print{@page{size:A4;margin:17mm 15mm}html,body,.page{background:#fff}.page{width:100%;padding:0}.toc-bar{position:static}article,.table-wrap,figure,tr{break-inside:avoid}}'
    )
    return (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        f"{REPORT_NOTICE_HTML}"
        f'<title>{html.escape(data["title"])}</title><style>{css}</style></head><body><main class="page"><header><p class="k">Yao GEO Page Blueprint</p><h1>{html.escape(data["title"])}</h1><p>{html.escape(data.get("subtitle", ""))}</p><ul class="meta"><li>品牌：{html.escape(data["brand_name"])}</li><li>页面类型：{html.escape(data["page_type"])}</li><li>目标问题：{html.escape(data["target_question"])}</li><li>日期：{html.escape(data["analysis_date"])}</li></ul></header><div class="cards">{cards}</div><nav class="toc-bar" aria-label="报告目录"><h2>报告目录</h2><div class="toc-nav">{"".join(nav)}</div></nav>{"".join(body)}</main></body></html>'
    )


def soft_wrap_text(value: Any) -> str:
    text = str(value)
    text = re.sub(r"([/@?&=._:#-])", r"\1" + SOFT_BREAK, text)
    text = re.sub(r"([a-z])([A-Z])", r"\1" + SOFT_BREAK + r"\2", text)
    text = re.sub(r"([A-Za-z0-9]{18})", r"\1" + SOFT_BREAK, text)
    return text


def text_units(value: Any) -> int:
    text = str(value)
    units = 0
    for char in text:
        units += 2 if ord(char) > 127 else 1
    return max(units, 1)


def compute_col_widths(headers: list[str], rows: list[list[Any]]) -> list[int]:
    col_count = len(headers)
    if col_count == 0:
        return []

    weights: list[float] = []
    for col in range(col_count):
        samples = [headers[col]] + [row[col] for row in rows]
        max_units = max(text_units(sample) for sample in samples)
        avg_units = sum(min(text_units(sample), 48) for sample in samples) / len(samples)
        weights.append(max(8.0, min(max_units * 0.68 + avg_units * 0.32, 46.0)))

    min_width = 820 if col_count >= 5 else 1100
    raw_total = sum(weights)
    widths = [max(min_width, int(DOCX_TABLE_WIDTH * weight / raw_total)) for weight in weights]
    total = sum(widths)
    if total != DOCX_TABLE_WIDTH:
        scale = DOCX_TABLE_WIDTH / total
        widths = [max(min_width, int(width * scale)) for width in widths]
        widths[-1] += DOCX_TABLE_WIDTH - sum(widths)
    return widths


def p_xml(text: str, size: float = 10.5, bold: bool = False, after: int = 90, serif: bool = False) -> str:
    bold_xml = "<w:b/>" if bold else ""
    size_val = int(round(size * 2))
    safe_text = xe(soft_wrap_text(text))
    east_asia = "Source Han Serif SC" if serif else "Microsoft YaHei"
    ascii_font = "Georgia" if serif else "Arial"
    return (
        f'<w:p><w:pPr><w:spacing w:after="{after}" w:line="276" w:lineRule="auto"/><w:wordWrap/></w:pPr>'
        f'<w:r><w:rPr><w:rFonts w:ascii="{ascii_font}" w:eastAsia="{east_asia}" w:hAnsi="{ascii_font}"/><w:sz w:val="{size_val}"/>{bold_xml}</w:rPr>'
        f'<w:t xml:space="preserve">{safe_text}</w:t></w:r></w:p>'
    )


def table_cell_xml(value: Any, width: int, head: bool = False, align: str = "left") -> str:
    fill = '<w:shd w:fill="F3F0E8"/>' if head else ""
    valign = '<w:vAlign w:val="center"/>'
    p = p_xml(str(value), 8.7 if head else 8.3, head, 55)
    if align == "center":
        p = p.replace("<w:pPr>", '<w:pPr><w:jc w:val="center"/>', 1)
    return (
        f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{valign}{fill}'
        f'<w:tcMar><w:top w:w="{DOCX_CELL_MARGIN}" w:type="dxa"/><w:left w:w="{DOCX_CELL_MARGIN}" w:type="dxa"/>'
        f'<w:bottom w:w="{DOCX_CELL_MARGIN}" w:type="dxa"/><w:right w:w="{DOCX_CELL_MARGIN}" w:type="dxa"/></w:tcMar></w:tcPr>{p}</w:tc>'
    )


def t_xml(headers: list[str], rows: list[list[Any]]) -> str:
    widths = compute_col_widths(headers, rows)
    short_headers = {"顺序", "状态", "必填", "是否进入 Schema", "版本", "核验日期", "页面类型"}

    def align_for(col_index: int) -> str:
        return "center" if headers[col_index] in short_headers else "left"

    tbl_pr = (
        f'<w:tblPr><w:tblW w:w="{DOCX_TABLE_WIDTH}" w:type="dxa"/><w:tblInd w:w="0" w:type="dxa"/>'
        '<w:tblLayout w:type="fixed"/>'
        f'<w:tblCellMar><w:top w:w="{DOCX_CELL_MARGIN}" w:type="dxa"/><w:left w:w="{DOCX_CELL_MARGIN}" w:type="dxa"/>'
        f'<w:bottom w:w="{DOCX_CELL_MARGIN}" w:type="dxa"/><w:right w:w="{DOCX_CELL_MARGIN}" w:type="dxa"/></w:tblCellMar>'
        '<w:tblBorders><w:top w:val="single" w:sz="6" w:color="E8E5DA"/><w:left w:val="single" w:sz="6" w:color="E8E5DA"/>'
        '<w:bottom w:val="single" w:sz="6" w:color="E8E5DA"/><w:right w:val="single" w:sz="6" w:color="E8E5DA"/>'
        '<w:insideH w:val="single" w:sz="6" w:color="E8E5DA"/><w:insideV w:val="single" w:sz="6" w:color="E8E5DA"/></w:tblBorders></w:tblPr>'
    )
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{width}"/>' for width in widths) + "</w:tblGrid>"
    header_row = "<w:tr>" + "".join(table_cell_xml(header, widths[index], True, align_for(index)) for index, header in enumerate(headers)) + "</w:tr>"
    body_rows = "".join(
        "<w:tr>" + "".join(table_cell_xml(value, widths[index], False, align_for(index)) for index, value in enumerate(row)) + "</w:tr>"
        for row in rows
    )
    return f"<w:tbl>{tbl_pr}{grid}{header_row}{body_rows}</w:tbl>"


def render_docx(data: dict[str, Any], path: Path) -> None:
    body = [
        p_xml(data["title"], 22, False, 160, True),
        p_xml(data.get("subtitle", ""), 11.5, False, 100),
        p_xml(f"品牌：{data['brand_name']}  页面类型：{data['page_type']}", 10.5, False, 70),
        p_xml(f"目标问题：{data['target_question']}", 10.5, False, 120),
        p_xml("封面摘要", 15.5, False, 90, True),
        t_xml(["指标", "结论", "说明"], [[card["label"], card["value"], card.get("note", "")] for card in data["summary_cards"]]),
    ]
    for section in data["sections"]:
        body.append(p_xml(section["title"], 15.5, False, 95, True))
        body += [p_xml(paragraph, 10.5, False, 75) for paragraph in section.get("paragraphs", [])]
        body += [p_xml(f"- {bullet}", 10.2, False, 55) for bullet in section.get("bullets", [])]
        if section.get("table"):
            body.append(t_xml(section["table"]["headers"], section["table"]["rows"]))
        for block in section.get("code_blocks", []):
            body += [p_xml(block.get("title", "代码样例"), 11.5, True, 60), p_xml(block.get("code", ""), 8.8, False, 80)]
    body.append(f'<w:sectPr><w:pgSz w:w="{DOCX_PAGE_WIDTH}" w:h="16838"/><w:pgMar w:top="{DOCX_MARGIN}" w:right="{DOCX_MARGIN}" w:bottom="{DOCX_MARGIN}" w:left="{DOCX_MARGIN}"/></w:sectPr>')
    doc = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{"".join(body)}</w:body></w:document>'
    content_types = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>'
    rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>'
    core = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>{xe(data["title"])}</dc:title><dc:creator>{xe(data.get("prepared_by", "yao-geo-page-blueprint"))}</dc:creator></cp:coreProperties>'
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("[Content_Types].xml", content_types)
        zip_file.writestr("_rels/.rels", rels)
        zip_file.writestr("word/document.xml", doc)
        zip_file.writestr("docProps/core.xml", core)


def docx_layout_issues(path: Path) -> list[str]:
    try:
        xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    except Exception as exc:
        return [f"DOCX 结构不可读：{exc}"]
    issues = []
    required = {
        "固定表格布局": '<w:tblLayout w:type="fixed"/>' in xml,
        "表格网格": "<w:tblGrid>" in xml,
        "单元格边距": "<w:tcMar>" in xml,
        "段落断词": "<w:wordWrap/>" in xml,
    }
    issues += [f"DOCX 缺少{label}" for label, ok in required.items() if not ok]
    issues += [f"DOCX 表格宽度超过正文宽度：{DOCX_TABLE_WIDTH}>{DOCX_TEXT_WIDTH}" if DOCX_TABLE_WIDTH > DOCX_TEXT_WIDTH else ""]
    text_nodes = re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml, flags=re.S)
    long_segments: list[str] = []
    for node in text_nodes:
        plain = html.unescape(re.sub(r"<[^>]+>", "", node))
        for token in re.findall(r"[A-Za-z0-9:/?&=._#%+-]+", plain):
            long_segments += [part for part in token.split(SOFT_BREAK) if len(part) > 28]
    if long_segments:
        issues.append(f"DOCX 存在未断开的长英文/URL片段：{len(long_segments)}处")
    return [issue for issue in issues if issue]


def review(paths: dict[str, Path]) -> dict[str, Any]:
    issues = [f"{key} 文件缺失或过小" for key, path in paths.items() if not path.exists() or path.stat().st_size < 300]
    html_text = paths["html"].read_text(encoding="utf-8")
    combined = paths["markdown"].read_text(encoding="utf-8") + html_text
    issues += [f"缺少关键词：{keyword}" for keyword in KEYWORDS if keyword not in combined]
    compact = html_text.replace(" ", "")
    issues += [f"HTML 缺少规则：{rule}" for rule in ["background:#fff", "border-collapse:collapse", "overflow-wrap", "position:sticky", 'aria-label="报告目录"', 'class="toc-bar"', "--ink:#1B365D", "--ivory:#faf9f5"] if rule not in compact]
    if "gradient" in html_text or "file://" in html_text or "/Users/" in html_text:
        issues.append("HTML 包含不允许的背景或本地路径")
    issues += docx_layout_issues(paths["docx"])
    return {
        "skill_id": "yao-geo-page-blueprint",
        "reviewed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "passed": not issues,
        "issues": issues,
        "files": {key: str(path) for key, path in paths.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    data = load_data(Path(args.input))
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    slug = slugify(data.get("slug") or data["brand_name"])
    paths = {
        "markdown": out / f"{slug}.md",
        "html": out / f"{slug}.html",
        "docx": out / f"{slug}.docx",
        "pdf": out / f"{slug}.pdf",
    }
    paths["markdown"].write_text(render_md(data), encoding="utf-8")
    html_text = render_html(data)
    paths["html"].write_text(html_text, encoding="utf-8")
    render_docx(data, paths["docx"])
    HTML(string=html_text, base_url=str(out)).write_pdf(str(paths["pdf"]))
    result = review(paths)
    review_path = out / f"{slug}-quality-review.json"
    review_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    if not result["passed"]:
        raise SystemExit(f"quality review failed: {result['issues']}")
    print(json.dumps({"outputs": {key: str(value) for key, value in paths.items()}, "review": str(review_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
