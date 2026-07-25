#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-intent-miner
# Created by: 姚金刚
# Date: 2026-05-21
# X: https://x.com/yaojingang

"""Render Yao GEO Intent Miner reports into Markdown, HTML, DOCX, and PDF."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


CONTENT_WIDTH_DXA = 15138
PAGE_WIDTH_DXA = 16838
PAGE_HEIGHT_DXA = 11906
PAGE_MARGIN_DXA = 850
REQUIRED_SECTION_KEYWORDS = [
    "执行摘要",
    "研究依据",
    "事实校准",
    "真实数据",
    "输入归一化",
    "用户角色",
    "意图地图",
    "问题簇",
    "查询重写",
    "国内 AI 平台",
    "内容资产",
    "监测 Prompt",
    "证据缺口",
    "合规",
    "落地路线",
]
PLATFORMS = {"DeepSeek", "豆包", "千问", "Kimi", "元宝"}


APPENDICES = [
    {
        "key": "question_bank",
        "title": "问题库",
        "kicker": "Appendix A",
        "headers": ["ID", "问题簇", "意图", "问题", "独立重写", "查询重写", "证据查询", "资产映射", "优先级", "合规"],
        "fields": ["question_id", "cluster", "intent_type", "question", "standalone_rewrite", "retrieval_rewrite", "evidence_query", "content_asset", "priority", "compliance_level"],
    },
    {
        "key": "scoring_matrix",
        "title": "评分矩阵",
        "kicker": "Appendix B",
        "headers": ["ID", "问题簇", "商业", "AI触发", "缺口", "植入", "证据", "竞争", "追问", "决策", "平台", "风险", "总分", "优先级"],
        "fields": ["question_id", "cluster", "business_value", "ai_answer_probability", "content_gap", "brand_insert_space", "evidence_availability", "competition_difficulty", "conversation_extension", "decision_stage_value", "platform_coverage", "compliance_risk", "weighted_score", "priority"],
    },
    {
        "key": "follow_up_chains",
        "title": "追问链路",
        "kicker": "Appendix C",
        "headers": ["链路ID", "根问题", "父问题", "追问层级", "上下文依赖", "追问问题", "独立重写", "平台适配"],
        "fields": ["chain_id", "root_question_id", "parent_question_id", "follow_up_level", "context_dependency", "follow_up_question", "standalone_rewrite", "platform_fit"],
    },
    {
        "key": "prompt_library",
        "title": "监测 Prompt 库",
        "kicker": "Appendix D",
        "headers": ["ID", "平台", "意图", "监测 Prompt", "用途", "记录字段"],
        "fields": ["prompt_id", "platform", "intent_type", "prompt", "usage", "record_fields"],
    },
    {
        "key": "data_sources",
        "title": "真实数据源状态",
        "kicker": "Appendix E",
        "headers": ["数据源ID", "类型", "提供方", "接入状态", "记录数", "时间范围", "校准用途", "下一步"],
        "fields": ["source_id", "source_type", "provider", "access_status", "record_count", "date_range", "calibration_use", "next_action"],
    },
    {
        "key": "ai_sampling_plan",
        "title": "AI 平台采样计划或结果",
        "kicker": "Appendix F",
        "headers": ["采样ID", "平台", "Prompt", "状态", "品牌提及", "引用来源", "风险标记", "下一步"],
        "fields": ["sample_id", "platform", "prompt", "status", "brand_mentioned", "cited_sources", "risk_flags", "next_action"],
    },
    {
        "key": "calibration_actions",
        "title": "数据校准动作",
        "kicker": "Appendix G",
        "headers": ["动作ID", "校准信号", "影响维度", "当前状态", "处理方式", "负责人"],
        "fields": ["action_id", "signal", "affected_dimensions", "current_status", "method", "owner"],
    },
    {
        "key": "content_topics",
        "title": "内容选题库",
        "kicker": "Appendix H",
        "headers": ["选题ID", "选题", "主问题", "目标资产", "证据需求", "优先级"],
        "fields": ["topic_id", "title", "source_question", "asset_type", "evidence_need", "priority"],
    },
    {
        "key": "faq_bank",
        "title": "FAQ 题库",
        "kicker": "Appendix I",
        "headers": ["FAQ ID", "问题", "回答边界", "证据需求", "对应资产", "合规"],
        "fields": ["faq_id", "question", "answer_boundary", "evidence_need", "target_asset", "compliance_level"],
    },
    {
        "key": "knowledge_base_entries",
        "title": "知识库条目建议",
        "kicker": "Appendix J",
        "headers": ["条目ID", "标题", "类型", "覆盖问题", "需要材料", "负责人"],
        "fields": ["entry_id", "title", "entry_type", "covered_questions", "required_materials", "owner"],
    },
    {
        "key": "evidence_sources",
        "title": "证据来源清单",
        "kicker": "Appendix K",
        "headers": ["来源", "级别", "用途", "链接", "状态"],
        "fields": ["source", "level", "use", "url", "status"],
    },
    {
        "key": "action_roadmap",
        "title": "落地路线",
        "kicker": "Appendix L",
        "headers": ["阶段", "任务", "产出", "负责人", "验收口径"],
        "fields": ["phase", "task", "deliverable", "owner", "acceptance"],
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to report_input.json")
    parser.add_argument("--output-dir", required=True, help="Directory for rendered files")
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def as_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "、".join(as_text(item) for item in value)
    if isinstance(value, dict):
        return "；".join(f"{key}: {as_text(val)}" for key, val in value.items())
    return str(value)


def anchor(value: str) -> str:
    lowered = re.sub(r"\s+", "-", value.strip().lower())
    lowered = re.sub(r"[^a-z0-9\-\u4e00-\u9fff]+", "-", lowered)
    return lowered.strip("-") or "section"


def md_escape(value: object) -> str:
    return as_text(value).replace("|", "\\|").replace("\n", " ")


def html_escape(value: object) -> str:
    return html.escape(as_text(value), quote=True).replace("\n", "<br>")


def xml_text(value: object) -> str:
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", as_text(value))
    return xml_escape(soft_wrap_long_tokens(text))


def soft_wrap_long_tokens(text: str) -> str:
    def wrap(match: re.Match[str]) -> str:
        token = match.group(0)
        return "\u200b".join(token[index : index + 18] for index in range(0, len(token), 18))

    return re.sub(r"[A-Za-z0-9_./:\-?=&%]{28,}", wrap, text)


def section_id(index: int, title: str) -> str:
    return f"section-{index}-{anchor(title)}"


def table_class(headers: list[str], rows: list[list[object]]) -> str:
    max_len = max([len(as_text(cell)) for row in rows for cell in row] + [0])
    if len(headers) >= 7 or max_len > 90:
        return "wide"
    if len(headers) >= 5 or max_len > 60:
        return "medium"
    return ""


def rows_from_items(items: list[dict], fields: list[str]) -> list[list[str]]:
    return [[as_text(item.get(field, "")) for field in fields] for item in items]


def render_markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    if not headers:
        return ""
    lines = [
        "| " + " | ".join(md_escape(head) for head in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        padded = list(row) + [""] * (len(headers) - len(row))
        lines.append("| " + " | ".join(md_escape(cell) for cell in padded[: len(headers)]) + " |")
    return "\n".join(lines)


def render_markdown(data: dict) -> str:
    lines: list[str] = [
        f"# {md_escape(data.get('title'))}",
        "",
        md_escape(data.get("subtitle")),
        "",
        f"- 品牌/项目：{md_escape(data.get('brand_name'))}",
        f"- 生成日期：{md_escape(data.get('analysis_date'))}",
        f"- 生成者：{md_escape(data.get('prepared_by'))}",
        "",
        "## 摘要指标",
        "",
    ]
    cards = data.get("summary_cards", [])
    lines.append(render_markdown_table(["指标", "结果", "说明"], [[card.get("label"), card.get("value"), card.get("note")] for card in cards]))
    lines.append("")
    for index, section in enumerate(data.get("sections", []), start=1):
        lines.extend([f"## {index:02d}. {md_escape(section.get('title'))}", ""])
        for para in section.get("paragraphs", []):
            lines.extend([md_escape(para), ""])
        table = section.get("table")
        if table:
            lines.extend([render_markdown_table(table.get("headers", []), table.get("rows", [])), ""])
    for appendix in APPENDICES:
        items = data.get(appendix["key"], [])
        if not items:
            continue
        lines.extend([f"## {appendix['title']}", "", render_markdown_table(appendix["headers"], rows_from_items(items, appendix["fields"])), ""])
    lines.append("## 生成限制")
    lines.append("")
    lines.append(md_escape(data.get("limitations", "问题集代表意图空间，不代表真实搜索量、真实 AI 答案分布或最终采购建议。")))
    lines.append("")
    return "\n".join(lines)


def render_html_table(headers: list[str], rows: list[list[object]]) -> str:
    cls = table_class(headers, rows)
    thead = "".join(f"<th>{html_escape(head)}</th>" for head in headers)
    body_rows = []
    for row in rows:
        padded = list(row) + [""] * (len(headers) - len(row))
        cells = "".join(f"<td>{html_escape(cell)}</td>" for cell in padded[: len(headers)])
        body_rows.append(f"<tr>{cells}</tr>")
    return f'<div class="table-wrap {cls}"><table><thead><tr>{thead}</tr></thead><tbody>{"".join(body_rows)}</tbody></table></div>'


def render_html(data: dict) -> str:
    sections = data.get("sections", [])
    appendix_nav = [(appendix["key"], appendix["title"]) for appendix in APPENDICES if data.get(appendix["key"])]
    nav_links = []
    for index, section in enumerate(sections, start=1):
        sid = section_id(index, section.get("title", "section"))
        nav_links.append(f'<a href="#{sid}">{index:02d} {html_escape(section.get("title"))}</a>')
    for key, title in appendix_nav:
        nav_links.append(f'<a href="#{anchor(key)}">{html_escape(title)}</a>')

    cards = []
    for card in data.get("summary_cards", []):
        cards.append(
            '<article class="summary-card">'
            f'<p class="summary-label">{html_escape(card.get("label"))}</p>'
            f'<p class="summary-value">{html_escape(card.get("value"))}</p>'
            f'<p class="summary-note">{html_escape(card.get("note"))}</p>'
            "</article>"
        )

    section_html = []
    for index, section in enumerate(sections, start=1):
        sid = section_id(index, section.get("title", "section"))
        paras = "".join(f"<p>{html_escape(para)}</p>" for para in section.get("paragraphs", []))
        table = section.get("table")
        table_html = render_html_table(table.get("headers", []), table.get("rows", [])) if table else ""
        section_html.append(
            f'<section class="section" id="{sid}">'
            f'<p class="section-kicker">Section {index:02d}</p>'
            f'<h2>{html_escape(section.get("title"))}</h2>{paras}{table_html}</section>'
        )

    appendix_html = []
    for appendix in APPENDICES:
        items = data.get(appendix["key"], [])
        if not items:
            continue
        rows = rows_from_items(items, appendix["fields"])
        appendix_html.append(
            f'<section class="section" id="{anchor(appendix["key"])}">'
            f'<p class="section-kicker">{appendix["kicker"]}</p>'
            f'<h2>{html_escape(appendix["title"])}</h2>'
            f'{render_html_table(appendix["headers"], rows)}</section>'
        )

    css = """
:root{--parchment:#f5f4ed;--ivory:#faf9f5;--warm-sand:#e8e6dc;--ink:#141413;--dark-warm:#3d3d3a;--charcoal:#4d4c48;--muted:#5e5d59;--stone:#87867f;--line:#e8e5da;--line-strong:#d1cfc5;--brand:#1B365D;--brand-soft:#EEF2F7;--accent:#6b4f2a}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--parchment);color:var(--ink);font-family:"Inter","Source Han Sans SC","PingFang SC","Microsoft YaHei",Arial,sans-serif;font-size:14px;line-height:1.5;letter-spacing:0}
.page{width:min(1180px,calc(100vw - 44px));margin:30px auto 60px}
.hero{border:1px solid var(--line-strong);border-left:5px solid var(--brand);padding:26px 30px 24px;background:var(--ivory);border-radius:8px}
.eyebrow{margin:0 0 8px;color:var(--brand);font-size:12px;font-weight:600;letter-spacing:0;text-transform:uppercase}
h1,h2{letter-spacing:0}
h1{margin:0 0 12px;font-family:"Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;font-size:30px;line-height:1.18;font-weight:500}
h2{margin:0 0 12px;font-family:"Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;font-size:21px;line-height:1.24;font-weight:500;border-left:3px solid var(--brand);padding-left:10px}
.subtitle{max-width:960px;color:var(--muted);margin:0 0 14px;font-size:15px}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px;color:var(--muted);font-size:12px}
.meta span{border:1px solid var(--line);background:var(--brand-soft);border-radius:999px;padding:5px 10px}
.summary-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;margin:16px 0 16px}
.summary-card{border:1px solid var(--line);border-radius:8px;padding:13px 15px;background:var(--ivory);min-height:104px}
.summary-label{margin:0 0 8px;color:var(--muted);font-size:12px;font-weight:600}
.summary-value{margin:0 0 8px;font-family:"Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;color:var(--brand);font-size:21px;line-height:1.2;font-weight:500}
.summary-note{margin:0;color:var(--muted);font-size:12px}
.sticky-menu{position:sticky;top:0;z-index:20;background:var(--ivory);border:1px solid var(--line-strong);border-radius:8px;margin:0 0 18px;padding:9px 10px;box-shadow:0 0 0 1px #e8e5da}
.sticky-menu-inner{display:flex;flex-wrap:wrap;gap:7px;max-height:82px;overflow:auto}
.sticky-menu a{color:var(--brand);background:var(--brand-soft);border:1px solid #d1cfc5;border-radius:999px;padding:5px 9px;text-decoration:none;font-size:12px;line-height:1.25;white-space:nowrap}
.section{margin:16px 0;padding:18px 20px;border:1px solid var(--line);border-radius:8px;background:var(--ivory);page-break-inside:auto}
.section-kicker{margin:0 0 6px;color:var(--accent);font-size:11px;font-weight:700;letter-spacing:0;text-transform:uppercase}
p{margin:0 0 9px}
.table-wrap{width:100%;overflow-x:auto;margin:10px 0 4px;border:1px solid var(--line-strong);border-radius:6px}
table{width:100%;border-collapse:collapse;table-layout:fixed;background:var(--ivory);font-size:12px;line-height:1.28}
th,td{border:1px solid var(--line);padding:6px 7px;vertical-align:top;word-break:break-word;overflow-wrap:anywhere;hyphens:auto}
th{background:var(--brand-soft);color:var(--brand);font-weight:700;text-align:left}
tr:nth-child(even) td{background:#f5f4ed}
thead{display:table-header-group}
tr{break-inside:avoid;page-break-inside:avoid}
.wide table{font-size:9.8px;line-height:1.2}
.medium table{font-size:10.7px;line-height:1.23}
@page{size:A4 landscape;margin:12mm 10mm;background:#f5f4ed}
@media(max-width:680px){.page{width:calc(100vw - 24px);margin:16px auto 36px}.hero,.section{padding:16px}h1{font-size:24px}.sticky-menu-inner{flex-wrap:nowrap}.sticky-menu a{font-size:11px}}
@media print{body{font-size:11px}.page{width:auto;margin:0}.hero,.section{border-radius:0;page-break-inside:auto}.sticky-menu{display:none}.table-wrap{overflow:visible}table{font-size:9.4px}th,td{padding:4px 5px}.wide table{font-size:7.7px;line-height:1.16}.medium table{font-size:8.5px;line-height:1.18}}
""".strip()
    return (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{html_escape(data.get('title'))}</title><style>{css}</style></head><body><main class=\"page\">"
        '<header class="hero"><p class="eyebrow">Yao GEO Intent Miner</p>'
        f"<h1>{html_escape(data.get('title'))}</h1>"
        f"<p class=\"subtitle\">{html_escape(data.get('subtitle'))}</p>"
        '<div class="meta">'
        f"<span>品牌/项目：{html_escape(data.get('brand_name'))}</span>"
        f"<span>生成日期：{html_escape(data.get('analysis_date'))}</span>"
        f"<span>生成者：{html_escape(data.get('prepared_by'))}</span>"
        "</div></header>"
        f'<section class="summary-grid">{"".join(cards)}</section>'
        f'<nav class="sticky-menu" aria-label="报告目录"><div class="sticky-menu-inner">{"".join(nav_links)}</div></nav>'
        f'{"".join(section_html)}{"".join(appendix_html)}</main></body></html>'
    )


def w_p(text: object, style: str | None = None, bold: bool = False, size: int | None = None) -> str:
    p_pr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    r_pr_parts = []
    if bold:
        r_pr_parts.append("<w:b/>")
    if size:
        r_pr_parts.append(f'<w:sz w:val="{size}"/>')
    r_pr = f"<w:rPr>{''.join(r_pr_parts)}</w:rPr>" if r_pr_parts else ""
    return f"<w:p>{p_pr}<w:r>{r_pr}<w:t xml:space=\"preserve\">{xml_text(text)}</w:t></w:r></w:p>"


def column_widths(column_count: int) -> list[int]:
    if column_count <= 0:
        return []
    base = CONTENT_WIDTH_DXA // column_count
    widths = [base] * column_count
    widths[-1] += CONTENT_WIDTH_DXA - sum(widths)
    return widths


def w_table(headers: list[str], rows: list[list[object]]) -> str:
    widths = column_widths(len(headers))
    grid = "".join(f'<w:gridCol w:w="{width}"/>' for width in widths)
    borders = (
        '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="B7BEC8"/>'
        '<w:left w:val="single" w:sz="4" w:color="B7BEC8"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="B7BEC8"/>'
        '<w:right w:val="single" w:sz="4" w:color="B7BEC8"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="D9DDE3"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="D9DDE3"/></w:tblBorders>'
    )
    tbl_pr = f'<w:tblPr><w:tblW w:w="{CONTENT_WIDTH_DXA}" w:type="dxa"/><w:tblLayout w:type="fixed"/>{borders}</w:tblPr>'

    def row_xml(values: list[object], is_header: bool = False) -> str:
        cells = []
        padded = values + [""] * (len(headers) - len(values))
        for width, value in zip(widths, padded[: len(headers)]):
            shade = '<w:shd w:fill="EEF5F7"/>' if is_header else ""
            tc_pr = f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shade}<w:noWrap w:val="0"/></w:tcPr>'
            cells.append(f"<w:tc>{tc_pr}{w_p(value, bold=is_header, size=17 if len(headers) >= 8 else 19)}</w:tc>")
        return f"<w:tr><w:trPr><w:cantSplit/></w:trPr>{''.join(cells)}</w:tr>"

    header_row = row_xml(headers, is_header=True)
    body = "".join(row_xml(list(row)) for row in rows)
    return f"<w:tbl>{tbl_pr}<w:tblGrid>{grid}</w:tblGrid>{header_row}{body}</w:tbl>"


def render_docx_xml(data: dict) -> str:
    body: list[str] = [
        w_p(data.get("title"), style="Title"),
        w_p(data.get("subtitle")),
        w_p(f"品牌/项目：{data.get('brand_name', '')}    生成日期：{data.get('analysis_date', '')}    生成者：{data.get('prepared_by', '')}"),
        w_p("摘要指标", style="Heading1"),
        w_table(["指标", "结果", "说明"], [[card.get("label"), card.get("value"), card.get("note")] for card in data.get("summary_cards", [])]),
    ]
    for index, section in enumerate(data.get("sections", []), start=1):
        body.append(w_p(f"{index:02d}. {section.get('title', '')}", style="Heading1"))
        for para in section.get("paragraphs", []):
            body.append(w_p(para))
        table = section.get("table")
        if table:
            body.append(w_table(table.get("headers", []), table.get("rows", [])))
    for appendix in APPENDICES:
        items = data.get(appendix["key"], [])
        if not items:
            continue
        body.append(w_p(appendix["title"], style="Heading1"))
        body.append(w_table(appendix["headers"], rows_from_items(items, appendix["fields"])))
    body.append(w_p("生成限制", style="Heading1"))
    body.append(w_p(data.get("limitations", "问题集代表意图空间，不代表真实搜索量、真实 AI 答案分布或最终采购建议。")))
    sect_pr = (
        f'<w:sectPr><w:pgSz w:w="{PAGE_WIDTH_DXA}" w:h="{PAGE_HEIGHT_DXA}" w:orient="landscape"/>'
        f'<w:pgMar w:top="{PAGE_MARGIN_DXA}" w:right="{PAGE_MARGIN_DXA}" w:bottom="{PAGE_MARGIN_DXA}" w:left="{PAGE_MARGIN_DXA}" w:header="450" w:footer="450" w:gutter="0"/>'
        "</w:sectPr>"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{''.join(body)}{sect_pr}</w:body></w:document>"
    )


def render_docx(data: dict, path: Path) -> None:
    document_xml = render_docx_xml(data)
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>"""
    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:b/><w:sz w:val="34"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:rPr><w:b/><w:sz w:val="25"/></w:rPr><w:pPr><w:spacing w:before="220" w:after="100"/></w:pPr></w:style>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="Microsoft YaHei"/><w:sz w:val="20"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:line="300" w:lineRule="auto" w:after="90"/></w:pPr></w:pPrDefault></w:docDefaults>
</w:styles>"""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("word/_rels/document.xml.rels", doc_rels)
        archive.writestr("word/styles.xml", styles)
        archive.writestr("word/document.xml", document_xml)


def render_pdf(html_path: Path, pdf_path: Path) -> None:
    try:
        from weasyprint import HTML

        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        return
    except Exception:
        chromium = shutil.which("chromium") or shutil.which("google-chrome")
        if not chromium:
            raise
        subprocess.check_call(
            [
                chromium,
                "--headless",
                "--disable-gpu",
                f"--print-to-pdf={pdf_path}",
                f"file://{html_path}",
            ]
        )


def check_docx(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    page = re.search(r'<w:pgSz[^>]*w:w="(\d+)"[^>]*w:h="(\d+)"[^>]*/>', xml)
    margins = re.search(r'<w:pgMar[^>]*w:right="(\d+)"[^>]*w:left="(\d+)"[^>]*/>', xml)
    page_width = int(page.group(1)) if page else PAGE_WIDTH_DXA
    right = int(margins.group(1)) if margins else PAGE_MARGIN_DXA
    left = int(margins.group(2)) if margins else PAGE_MARGIN_DXA
    content_width = page_width - left - right
    table_widths = [int(value) for value in re.findall(r'<w:tblW w:w="(\d+)"', xml)]
    grid_sums = [
        sum(int(value) for value in re.findall(r'w:w="(\d+)"', grid))
        for grid in re.findall(r"<w:tblGrid>(.*?)</w:tblGrid>", xml)
    ]
    table_count = xml.count("<w:tbl>")
    fixed_count = xml.count('<w:tblLayout w:type="fixed"/>')
    return {
        "docx_is_readable_zip": True,
        "docx_content_width_dxa": content_width,
        "docx_max_table_width_dxa": max(table_widths) if table_widths else 0,
        "docx_max_grid_width_dxa": max(grid_sums) if grid_sums else 0,
        "docx_tables_fit_page_width": bool(table_widths) and max(table_widths) <= content_width and bool(grid_sums) and max(grid_sums) <= content_width,
        "docx_has_fixed_table_layout": table_count > 0 and fixed_count == table_count,
    }


def check_pdf(path: Path) -> dict:
    checks = {"pdf_has_header": path.read_bytes()[:5] == b"%PDF-"}
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        info = subprocess.check_output([pdfinfo, str(path)], text=True)
        page_line = next((line for line in info.splitlines() if line.startswith("Page size:")), "")
        dims = [float(value) for value in re.findall(r"\d+\.\d+|\d+", page_line)[:2]]
        checks["pdf_is_landscape"] = len(dims) >= 2 and dims[0] > dims[1]
        checks["pdf_page_size"] = page_line
    return checks


def quality_report(data: dict, paths: dict[str, Path]) -> dict:
    html_text = paths["html"].read_text(encoding="utf-8")
    section_titles = [as_text(section.get("title")) for section in data.get("sections", [])]
    section_text = " ".join(section_titles)
    prompt_platforms = {as_text(item.get("platform")) for item in data.get("prompt_library", [])}
    question_bank = data.get("question_bank", [])
    checks: dict[str, object] = {
        "markdown_report_exists": paths["markdown"].exists(),
        "html_report_exists": paths["html"].exists(),
        "docx_report_exists": paths["docx"].exists(),
        "pdf_report_exists": paths["pdf"].exists(),
        "html_has_kami_canvas": "#f5f4ed" in html_text and "#faf9f5" in html_text and "#1B365D" in html_text,
        "html_avoids_rgba": "rgba(" not in html_text,
        "html_has_sticky_menu": "position:sticky" in html_text and "sticky-menu" in html_text,
        "html_has_toc_links": html_text.count("<a href=\"#") >= len(data.get("sections", [])),
        "html_wraps_long_text": "overflow-wrap:anywhere" in html_text and "table-layout:fixed" in html_text,
        "required_sections_present": all(keyword in section_text for keyword in REQUIRED_SECTION_KEYWORDS),
        "section_count_at_least_15": len(data.get("sections", [])) >= 15,
        "data_source_status_present": bool(data.get("data_sources")),
        "ai_sampling_plan_or_results_present": bool(data.get("ai_sampling_plan")),
        "calibration_actions_present": bool(data.get("calibration_actions")),
        "question_bank_at_least_18": len(question_bank) >= 18,
        "question_bank_has_required_fields": all(
            all(item.get(field) for field in ["question_id", "cluster", "intent_type", "question", "standalone_rewrite", "retrieval_rewrite", "evidence_query", "content_asset", "priority", "compliance_level"])
            for item in question_bank
        ),
        "monitoring_prompts_cover_cn_platforms": PLATFORMS.issubset(prompt_platforms),
        "follow_up_chains_at_least_8": len(data.get("follow_up_chains", [])) >= 8,
        "scoring_matrix_at_least_question_count": len(data.get("scoring_matrix", [])) >= min(18, len(question_bank)),
        "content_topics_present": bool(data.get("content_topics")),
        "faq_bank_present": bool(data.get("faq_bank")),
        "knowledge_base_entries_present": bool(data.get("knowledge_base_entries")),
        "evidence_sources_present": bool(data.get("evidence_sources")),
        "compliance_boundaries_present": "合规" in section_text and any(as_text(q.get("compliance_level")).startswith("L") for q in question_bank),
    }
    checks.update(check_docx(paths["docx"]))
    checks.update(check_pdf(paths["pdf"]))
    failed = [name for name, passed in checks.items() if isinstance(passed, bool) and not passed]
    return {
        "report": data.get("title"),
        "generated_files": {name: str(path) for name, path in paths.items()},
        "checks": checks,
        "failed_checks": failed,
        "overall_score": 100 - len(failed) * 5,
        "layout_limits": {
            "word_page": "A4 landscape",
            "word_content_width_dxa": CONTENT_WIDTH_DXA,
            "pdf_page": "A4 landscape",
            "html_menu": "position: sticky; top: 0",
        },
    }


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = read_json(input_path)
    slug = data.get("slug") or anchor(data.get("title", "intent-miner-report"))
    paths = {
        "markdown": output_dir / f"{slug}.md",
        "html": output_dir / f"{slug}.html",
        "docx": output_dir / f"{slug}.docx",
        "pdf": output_dir / f"{slug}.pdf",
        "quality": output_dir / "quality-report.json",
    }
    paths["markdown"].write_text(render_markdown(data), encoding="utf-8")
    paths["html"].write_text(render_html(data), encoding="utf-8")
    render_docx(data, paths["docx"])
    render_pdf(paths["html"], paths["pdf"])
    (output_dir / "index.html").write_text(paths["html"].read_text(encoding="utf-8"), encoding="utf-8")
    report = quality_report(data, paths)
    paths["quality"].write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["failed_checks"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
