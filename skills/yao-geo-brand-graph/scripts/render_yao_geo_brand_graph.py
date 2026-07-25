#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-brand-graph
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


CONFIDENCE = {"官方事实", "第三方证据", "媒体描述", "用户反馈", "推断", "待确认"}
PRIVACY = {"公开", "已授权", "匿名化", "待确认", "不可公开"}
CORE_TYPES = {"品牌", "产品", "服务", "功能", "技术", "行业", "用户", "场景", "案例", "证据", "地点", "时间"}

WORD_PAGE_WIDTH = 16838
WORD_PAGE_HEIGHT = 11906
WORD_MARGIN = 720
WORD_CONTENT_WIDTH = WORD_PAGE_WIDTH - WORD_MARGIN * 2
WORD_TABLE_WIDTH = 14400
WORD_WEIGHTS = {
    "ID": 2.0,
    "类型": 0.8,
    "名称": 2.0,
    "别名": 2.4,
    "说明": 4.2,
    "来源": 1.1,
    "可信等级": 1.2,
    "隐私状态": 1.1,
    "主体": 2.1,
    "关系": 0.9,
    "客体": 2.1,
    "方向": 3.2,
    "证据": 1.0,
    "规范实体": 2.0,
    "易混项": 2.0,
    "处理方式": 4.0,
    "依据": 1.4,
    "平台": 1.0,
    "意图": 1.6,
    "测试问题": 4.2,
    "期望命中实体": 3.0,
    "常见风险": 3.2,
    "通过标准": 3.2,
    "目标资产": 1.6,
    "需补强关系": 3.0,
    "证据缺口": 3.0,
    "优先级": 0.9,
    "验收口径": 3.5,
    "来源类型": 1.1,
    "标题": 2.3,
    "定位符": 3.5,
    "日期": 1.6,
    "事实主张": 4.2,
    "核验状态": 1.2,
    "用途": 2.2,
    "等级": 1.1,
    "定义": 3.5,
    "允许用途": 3.0,
    "限制": 3.0,
    "Subject": 2.0,
    "Predicate": 1.2,
    "Object": 2.0,
    "Evidence": 1.2,
    "参考": 1.2,
    "权威来源": 2.0,
    "适用边界": 3.2,
    "落地规则": 3.6,
    "链接": 2.8,
    "维度": 1.4,
    "检查问题": 3.0,
    "当前结论": 3.3,
    "风险": 2.8,
    "补强动作": 3.4,
    "覆盖对象": 2.4,
    "当前证据": 3.0,
    "缺口": 3.0,
    "实体类型": 1.2,
    "覆盖状态": 1.4,
    "代表实体": 3.0,
    "补强建议": 3.4,
    "关系类型": 1.4,
    "方向规则": 2.8,
    "证据要求": 2.8,
    "当前覆盖": 2.6,
    "质量动作": 3.4,
    "Schema对象": 1.8,
    "页面事实": 3.2,
    "可进入JSON-LD": 1.4,
    "约束说明": 3.4,
    "内容资产": 1.6,
    "应承载实体关系": 3.2,
    "现状判断": 3.0,
    "生产要求": 3.4,
    "验收方式": 3.0,
    "监测对象": 1.8,
    "平台/渠道": 1.6,
    "样本问题/触发": 3.4,
    "指标": 2.0,
    "频率": 1.4,
    "纠偏动作": 3.3,
    "检查项": 2.8,
    "状态": 1.0,
    "证据/说明": 4.2,
    "来源ID": 0.9,
    "证据标题": 2.4,
    "URL状态": 1.0,
    "页面标题": 3.2,
    "最后核验": 1.7,
    "真实数据判断": 3.4,
    "处理建议": 3.4,
}

ENRICHED_SECTIONS = [
    ("authority_references", "权威参考与适用边界", ["参考", "权威来源", "适用边界", "落地规则", "链接"]),
    ("analysis_dimensions", "系统分析维度矩阵", ["维度", "检查问题", "当前结论", "风险", "补强动作"]),
    ("source_coverage_matrix", "来源覆盖矩阵", ["来源类型", "覆盖对象", "当前证据", "缺口", "可信等级"]),
    ("source_validation", "真实数据来源核验", ["来源ID", "证据标题", "URL状态", "页面标题", "最后核验", "真实数据判断", "处理建议"]),
    ("entity_coverage_matrix", "实体覆盖矩阵", ["实体类型", "覆盖状态", "代表实体", "风险", "补强建议"]),
    ("relation_audit_matrix", "关系审计矩阵", ["关系类型", "方向规则", "证据要求", "当前覆盖", "质量动作"]),
    ("schema_alignment", "Schema 与页面正文一致性", ["Schema对象", "页面事实", "可进入JSON-LD", "约束说明", "来源"]),
    ("content_alignment_plan", "内容资产对齐计划", ["内容资产", "应承载实体关系", "现状判断", "生产要求", "验收方式"]),
    ("monitoring_plan", "国内 AI 平台监测闭环", ["监测对象", "平台/渠道", "样本问题/触发", "指标", "频率", "纠偏动作"]),
    ("analysis_completeness_checklist", "分析完整性自检清单", ["检查项", "状态", "证据/说明"]),
]

MARKDOWN_COPYRIGHT_NOTICE = """<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-brand-graph
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Structured report_input.json")
    parser.add_argument("--output-dir", required=True, help="Directory for md/html/pdf/docx outputs")
    return parser.parse_args()


def text_join(value: Any) -> str:
    if isinstance(value, list):
        return "、".join(map(str, value))
    return "" if value is None else str(value)


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return [] if value is None else [value]


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value.lower())
    return re.sub(r"-{2,}", "-", normalized).strip("-") or "brand-graph"


def load_input(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = [
        "title",
        "brand_name",
        "scope",
        "report_date",
        "executive_summary",
        "entities",
        "relations",
        "evidence",
        "disambiguation",
        "trust_table",
        "mermaid",
        "json_ld",
        "triples",
        "page_recommendations",
        "open_issues",
    ]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError("Missing required input keys: " + ", ".join(missing))
    return data


def rows(data: dict[str, Any], key: str) -> list[list[Any]]:
    if key == "authority_references":
        return [[i.get("reference", ""), i.get("authority", ""), i.get("use_case", ""), i.get("report_rule", ""), i.get("url", "")] for i in data.get(key, [])]
    if key == "analysis_dimensions":
        return [[i.get("dimension", ""), i.get("check_question", ""), i.get("current_conclusion", ""), i.get("risk", ""), i.get("next_action", "")] for i in data.get(key, [])]
    if key == "source_coverage_matrix":
        return [[i.get("source_type", ""), i.get("covered_objects", []), i.get("current_evidence", []), i.get("gap", ""), i.get("confidence", "")] for i in data.get(key, [])]
    if key == "source_validation":
        return [[i.get("source_id", ""), i.get("evidence_title", ""), f"{i.get('validation_status', '')} {i.get('http_status', '')}".strip(), i.get("page_title", ""), i.get("checked_at", ""), i.get("real_data_judgement", ""), i.get("action", "")] for i in data.get(key, [])]
    if key == "entity_coverage_matrix":
        return [[i.get("entity_type", ""), i.get("coverage_status", ""), i.get("representative_entities", []), i.get("risk", ""), i.get("reinforcement", "")] for i in data.get(key, [])]
    if key == "relation_audit_matrix":
        return [[i.get("relation_type", ""), i.get("direction_rule", ""), i.get("evidence_requirement", ""), i.get("current_coverage", ""), i.get("quality_action", "")] for i in data.get(key, [])]
    if key == "schema_alignment":
        return [[i.get("schema_type", ""), i.get("page_fact", ""), i.get("json_ld_eligible", ""), i.get("constraint", ""), i.get("source_ids", [])] for i in data.get(key, [])]
    if key == "content_alignment_plan":
        return [[i.get("asset", ""), i.get("entity_relations", ""), i.get("current_state", ""), i.get("production_requirement", ""), i.get("acceptance", "")] for i in data.get(key, [])]
    if key == "monitoring_plan":
        return [[i.get("monitor_object", ""), i.get("platform_or_channel", ""), i.get("sample_trigger", ""), i.get("metric", ""), i.get("cadence", ""), i.get("correction_action", "")] for i in data.get(key, [])]
    if key == "analysis_completeness_checklist":
        return [[i.get("item", ""), i.get("status", ""), i.get("evidence_note", "")] for i in data.get(key, [])]
    if key == "entities":
        return [[i.get("id", ""), i.get("type", ""), i.get("name", ""), i.get("aliases", []), i.get("description", ""), i.get("source_ids", []), i.get("confidence", ""), i.get("privacy_review", "")] for i in data["entities"]]
    if key == "relations":
        return [[i.get("subject", ""), i.get("predicate", ""), i.get("object", ""), i.get("direction", ""), i.get("evidence_ids", []), i.get("confidence", ""), i.get("notes", "")] for i in data["relations"]]
    if key == "trust":
        return [[i.get("level", ""), i.get("definition", ""), i.get("allowed_use", ""), i.get("limitations", "")] for i in data["trust_table"]]
    if key == "disambiguation":
        return [[i.get("canonical", ""), i.get("aliases", []), i.get("confusable_with", []), i.get("decision", ""), i.get("evidence", "")] for i in data["disambiguation"]]
    if key == "triples":
        return [[i.get("subject", ""), i.get("predicate", ""), i.get("object", ""), i.get("evidence_ids", [])] for i in data["triples"]]
    if key == "platform":
        return [[i.get("platform", ""), i.get("query_intent", ""), i.get("test_prompt", ""), i.get("expected_entities", []), i.get("common_risk", ""), i.get("pass_criteria", "")] for i in data.get("platform_test_scenarios", [])]
    if key == "recommendations":
        return [[i.get("target_asset", ""), i.get("relationship_gap", ""), i.get("evidence_gap", ""), i.get("priority", ""), i.get("acceptance_criteria", "")] for i in data["page_recommendations"]]
    return [[i.get("id", ""), i.get("source_type", ""), i.get("title", ""), i.get("locator", ""), i.get("date", ""), i.get("claim", ""), i.get("verification_status", ""), i.get("how_used", "")] for i in data["evidence"]]


def md_table(headers: list[str], body: list[list[Any]]) -> str:
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in body:
        cells = [text_join(cell).replace("|", "\\|").replace("\n", "<br>") for cell in row]
        output.append("| " + " | ".join(cells) + " |")
    return "\n".join(output)


def render_markdown(data: dict[str, Any]) -> str:
    parts = [MARKDOWN_COPYRIGHT_NOTICE, "", f"# {data['title']}", "", f"- 品牌：{data['brand_name']}", f"- 范围：{data['scope']}", f"- 报告日期：{data['report_date']}", "", "## 执行摘要", ""]
    parts.extend(f"- {item}" for item in data["executive_summary"])
    for key, title, headers in ENRICHED_SECTIONS:
        if data.get(key):
            parts.extend(["", f"## {title}", "", md_table(headers, rows(data, key))])
    for title, headers, key in [
        ("实体清单", ["ID", "类型", "名称", "别名", "说明", "来源", "可信等级", "隐私状态"], "entities"),
        ("关系清单", ["主体", "关系", "客体", "方向", "证据", "可信等级", "说明"], "relations"),
        ("可信等级表", ["等级", "定义", "允许用途", "限制"], "trust"),
        ("消歧表", ["规范实体", "别名", "易混项", "处理方式", "依据"], "disambiguation"),
    ]:
        parts.extend(["", f"## {title}", "", md_table(headers, rows(data, key))])
    parts.extend(["", "## Mermaid 实体关系图", "", "```mermaid", data["mermaid"].strip(), "```", "", "## JSON-LD 建议", "", "```json", json.dumps(data["json_ld"], ensure_ascii=False, indent=2), "```", "", "## RDF 式三元组样例", "", md_table(["Subject", "Predicate", "Object", "Evidence"], rows(data, "triples"))])
    if data.get("platform_test_scenarios"):
        parts.extend(["", "## 国内 AI 平台测试场景", "", md_table(["平台", "意图", "测试问题", "期望命中实体", "常见风险", "通过标准"], rows(data, "platform"))])
    parts.extend(["", "## 图谱补强建议", "", md_table(["目标资产", "需补强关系", "证据缺口", "优先级", "验收口径"], rows(data, "recommendations")), "", "## 来源账本", "", md_table(["ID", "来源类型", "标题", "定位符", "日期", "事实主张", "核验状态", "用途"], rows(data, "evidence")), "", "## 待确认项", ""])
    parts.extend(f"- {item}" for item in data["open_issues"])
    return "\n".join(parts) + "\n"


def html_table(headers: list[str], body: list[list[Any]]) -> str:
    head = "".join(f"<th>{html.escape(item)}</th>" for item in headers)
    body_html = "".join("<tr>" + "".join(f"<td>{html.escape(text_join(cell))}</td>" for cell in row) + "</tr>" for row in body)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body_html}</tbody></table></div>'


def html_section(section_id: str, title: str, content: str) -> str:
    return f'<section id="{html.escape(section_id)}"><h2>{html.escape(title)}</h2>{content}</section>'


def metric_strip(data: dict[str, Any]) -> str:
    metrics = [
        ("实体", len(data["entities"])),
        ("关系", len(data["relations"])),
        ("证据", len(data["evidence"])),
        ("来源连通", sum(1 for item in data.get("source_validation", []) if item.get("reachable"))),
    ]
    return '<div class="metrics">' + "".join(f'<div class="metric"><span class="metric-value">{value}</span><span class="metric-label">{html.escape(label)}</span></div>' for label, value in metrics) + "</div>"


def render_html(data: dict[str, Any]) -> str:
    sections: list[tuple[str, str, str]] = []
    summary = "<ul>" + "".join(f"<li>{html.escape(str(item))}</li>" for item in data["executive_summary"]) + "</ul>"
    sections.append(("summary", "执行摘要", summary))
    for key, title, headers in ENRICHED_SECTIONS:
        if data.get(key):
            sections.append((key.replace("_", "-"), title, html_table(headers, rows(data, key))))
    sections.extend([
        ("entities", "实体清单", html_table(["ID", "类型", "名称", "别名", "说明", "来源", "可信等级", "隐私状态"], rows(data, "entities"))),
        ("relations", "关系清单", html_table(["主体", "关系", "客体", "方向", "证据", "可信等级", "说明"], rows(data, "relations"))),
        ("trust", "可信等级表", html_table(["等级", "定义", "允许用途", "限制"], rows(data, "trust"))),
        ("disambiguation", "消歧表", html_table(["规范实体", "别名", "易混项", "处理方式", "依据"], rows(data, "disambiguation"))),
        ("mermaid", "Mermaid 实体关系图", f"<pre>{html.escape(data['mermaid'].strip())}</pre>"),
        ("json-ld", "JSON-LD 建议", f"<pre>{html.escape(json.dumps(data['json_ld'], ensure_ascii=False, indent=2))}</pre>"),
        ("triples", "RDF 式三元组样例", html_table(["Subject", "Predicate", "Object", "Evidence"], rows(data, "triples"))),
    ])
    if data.get("platform_test_scenarios"):
        sections.append(("platform", "国内 AI 平台测试场景", html_table(["平台", "意图", "测试问题", "期望命中实体", "常见风险", "通过标准"], rows(data, "platform"))))
    sections.extend([
        ("recommendations", "图谱补强建议", html_table(["目标资产", "需补强关系", "证据缺口", "优先级", "验收口径"], rows(data, "recommendations"))),
        ("evidence", "来源账本", html_table(["ID", "来源类型", "标题", "定位符", "日期", "事实主张", "核验状态", "用途"], rows(data, "evidence"))),
        ("open-issues", "待确认项", "<ul>" + "".join(f"<li>{html.escape(str(item))}</li>" for item in data["open_issues"]) + "</ul>"),
    ])
    nav = "".join(f'<a href="#{section_id}">{html.escape(title)}</a>' for section_id, title, _ in sections)
    section_html = "".join(html_section(section_id, title, content) for section_id, title, content in sections)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(data["title"])}</title><style>:root{{--parchment:#f5f4ed;--ivory:#faf9f5;--warm-sand:#e8e6dc;--brand:#1B365D;--near-black:#141413;--dark-warm:#3d3d3a;--charcoal:#4d4c48;--olive:#5e5d59;--stone:#87867f;--border-cream:#e8e5da;--border-warm:#e0ddd2;--ring-warm:#d1cfc5;--tag-bg:#EEF2F7}}*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--parchment);color:var(--near-black);font-family:"Inter","Source Han Sans SC","PingFang SC","Microsoft YaHei",Arial,sans-serif;line-height:1.55;letter-spacing:0}}.page{{width:min(1120px,calc(100vw - 36px));margin:28px auto 72px}}header,section{{background:var(--ivory);border:1px solid var(--border-cream);border-radius:10px;padding:24px 26px;margin-top:22px;break-inside:avoid;box-shadow:0 0 0 1px var(--border-cream)}}header{{border-top:5px solid var(--brand);margin-top:0;padding:30px 32px}}.eyebrow{{margin:0 0 12px;color:var(--brand);font-size:12px;font-weight:600;letter-spacing:.3px;text-transform:uppercase}}.meta{{color:var(--olive);font-size:13px;margin:10px 0 0}}.metrics{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:20px}}.metric{{background:var(--parchment);border:1px solid var(--border-warm);border-radius:8px;padding:10px 12px;display:flex;align-items:baseline;gap:8px}}.metric-value{{font-family:"Source Han Serif SC","Songti SC",Georgia,serif;font-size:24px;font-weight:500;color:var(--brand);font-variant-numeric:tabular-nums}}.metric-label{{font-size:12px;color:var(--olive)}}.report-nav{{position:sticky;top:0;z-index:20;display:flex;gap:8px;overflow-x:auto;margin:18px 0 0;padding:10px 12px;border:1px solid var(--border-warm);border-radius:8px;background:var(--ivory);box-shadow:0 0 0 1px var(--ring-warm)}}.report-nav a{{flex:0 0 auto;color:var(--brand);text-decoration:none;border:1px solid var(--border-warm);background:var(--tag-bg);padding:6px 10px;border-radius:6px;font-size:12px;line-height:1.2;white-space:nowrap}}section{{scroll-margin-top:76px}}h1,h2{{font-family:"Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;font-weight:500;letter-spacing:0}}h1{{margin:0;font-size:40px;line-height:1.16;color:var(--near-black)}}h2{{margin:0 0 14px;font-size:22px;line-height:1.25;border-left:4px solid var(--brand);padding-left:10px;color:var(--near-black)}}ul{{margin:0;padding-left:20px}}li{{margin:5px 0;color:var(--dark-warm)}}.table-wrap{{overflow-x:auto;border:1px solid var(--border-warm);border-radius:8px;background:var(--ivory)}}table{{width:100%;border-collapse:collapse;table-layout:fixed}}th,td{{border:1px solid var(--border-warm);padding:8px 9px;text-align:left;vertical-align:top;font-size:12px;line-height:1.42;overflow-wrap:anywhere;word-break:break-word;color:var(--charcoal)}}th{{background:var(--warm-sand);color:var(--near-black);font-weight:600}}pre{{margin:0;padding:14px 16px;border:1px solid var(--border-warm);border-radius:8px;background:var(--parchment);white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;line-height:1.45;color:var(--charcoal)}}@page{{size:A4;margin:20mm 22mm;background:#f5f4ed}}@media print{{.page{{width:auto;margin:0}}header,section{{box-shadow:none}}.report-nav{{display:none}}.metrics{{grid-template-columns:repeat(4,1fr)}}th,td{{font-size:9.5px;padding:5px 6px}}h1{{font-size:28px}}h2{{font-size:17px}}}}@media (max-width:720px){{.metrics{{grid-template-columns:repeat(2,minmax(0,1fr))}}h1{{font-size:30px}}header,section{{padding:20px 18px}}}}</style></head><body><main class="page"><header><p class="eyebrow">Yao GEO Brand Entity Graph</p><h1>{html.escape(data["title"])}</h1><p class="meta">品牌：{html.escape(data["brand_name"])} | 范围：{html.escape(data["scope"])} | 日期：{html.escape(data["report_date"])}</p>{metric_strip(data)}</header><nav class="report-nav" aria-label="报告目录">{nav}</nav>{section_html}</main></body></html>'''


def split_long_token(token: str, limit: int = 20) -> list[str]:
    if len(token) <= limit or not re.search(r"[A-Za-z0-9:/._?&=#-]{14,}", token):
        return [token]
    parts: list[str] = []
    current = ""
    for char in token:
        current += char
        if (char in "/:?&=#._-" and len(current) >= 8) or len(current) >= limit:
            parts.append(current)
            current = ""
    if current:
        parts.append(current)
    return parts


def word_lines(text: str, limit: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for token in re.split(r"(\s+)", text):
        if not token:
            continue
        if token.isspace():
            if current and not current.endswith(" "):
                current += " "
            continue
        for index, part in enumerate(split_long_token(token)):
            if index and current.strip():
                lines.append(current.strip())
                current = ""
            if current and len(current) + len(part) > limit:
                lines.append(current.strip())
                current = part
            else:
                current += part
    if current.strip():
        lines.append(current.strip())
    return lines or [""]


def word_paragraph(text: str, style: str | None = None, bold: bool = False, size: int | None = None, compact: bool = False) -> str:
    spacing = "220" if compact else "300"
    ppr = f'<w:pPr><w:wordWrap/><w:spacing w:line="{spacing}" w:lineRule="auto"/></w:pPr>'
    if style:
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/><w:wordWrap/><w:spacing w:line="{spacing}" w:lineRule="auto"/></w:pPr>'
    props = []
    if bold:
        props.append("<w:b/>")
    if size:
        props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    rpr = "<w:rPr>" + "".join(props) + "</w:rPr>" if props else ""
    runs = []
    for index, line in enumerate(word_lines(str(text), 28 if compact else 90)):
        if index:
            runs.append("<w:r><w:br/></w:r>")
        runs.append(f'<w:r>{rpr}<w:t xml:space="preserve">{xe(line)}</w:t></w:r>')
    return "<w:p>" + ppr + "".join(runs) + "</w:p>"


def word_table(headers: list[str], body: list[list[Any]]) -> str:
    weights = [WORD_WEIGHTS.get(header, 1.8) for header in headers]
    widths = [max(620, int(WORD_TABLE_WIDTH * weight / sum(weights))) for weight in weights]
    widths[-1] += WORD_TABLE_WIDTH - sum(widths)
    borders = "".join(f'<w:{edge} w:val="single" w:sz="6" w:space="0" w:color="E0DDD2"/>' for edge in ["top", "left", "bottom", "right", "insideH", "insideV"])
    margin = '<w:tblCellMar><w:top w:w="80" w:type="dxa"/><w:left w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar>'
    output = ["<w:tbl>", f'<w:tblPr><w:tblW w:w="{WORD_TABLE_WIDTH}" w:type="dxa"/><w:tblBorders>{borders}</w:tblBorders>{margin}<w:tblLayout w:type="fixed"/></w:tblPr>', "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{width}"/>' for width in widths) + "</w:tblGrid>"]
    output.append("<w:tr>" + "".join(f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/><w:shd w:fill="E8E6DC"/></w:tcPr>{word_paragraph(header, bold=True, size=17, compact=True)}</w:tc>' for header, width in zip(headers, widths)) + "</w:tr>")
    for row in body:
        output.append("<w:tr>" + "".join(f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/><w:shd w:fill="FAF9F5"/></w:tcPr>{word_paragraph(text_join(cell), size=16, compact=True)}</w:tc>' for cell, width in zip(row, widths)) + "</w:tr>")
    output.append("</w:tbl>")
    return "".join(output)


def render_docx(data: dict[str, Any], path: Path) -> None:
    body = [word_paragraph(data["title"], "Title"), word_paragraph(f"品牌：{data['brand_name']} | 范围：{data['scope']} | 日期：{data['report_date']}"), word_paragraph("执行摘要", "Heading1")]
    body.extend(word_paragraph("• " + str(item)) for item in data["executive_summary"])
    for key, title, headers in ENRICHED_SECTIONS:
        if data.get(key):
            body.extend([word_paragraph(title, "Heading1"), word_table(headers, rows(data, key))])
    for title, headers, key in [
        ("实体清单", ["ID", "类型", "名称", "别名", "说明", "来源", "可信等级", "隐私状态"], "entities"),
        ("关系清单", ["主体", "关系", "客体", "方向", "证据", "可信等级", "说明"], "relations"),
        ("可信等级表", ["等级", "定义", "允许用途", "限制"], "trust"),
        ("消歧表", ["规范实体", "别名", "易混项", "处理方式", "依据"], "disambiguation"),
    ]:
        body.extend([word_paragraph(title, "Heading1"), word_table(headers, rows(data, key))])
    body.extend([word_paragraph("Mermaid 实体关系图", "Heading1"), word_paragraph(data["mermaid"].strip()), word_paragraph("JSON-LD 建议", "Heading1"), word_paragraph(json.dumps(data["json_ld"], ensure_ascii=False, indent=2)), word_paragraph("RDF 式三元组样例", "Heading1"), word_table(["Subject", "Predicate", "Object", "Evidence"], rows(data, "triples"))])
    if data.get("platform_test_scenarios"):
        body.extend([word_paragraph("国内 AI 平台测试场景", "Heading1"), word_table(["平台", "意图", "测试问题", "期望命中实体", "常见风险", "通过标准"], rows(data, "platform"))])
    body.extend([word_paragraph("图谱补强建议", "Heading1"), word_table(["目标资产", "需补强关系", "证据缺口", "优先级", "验收口径"], rows(data, "recommendations")), word_paragraph("来源账本", "Heading1"), word_table(["ID", "来源类型", "标题", "定位符", "日期", "事实主张", "核验状态", "用途"], rows(data, "evidence")), word_paragraph("待确认项", "Heading1")])
    body.extend(word_paragraph("• " + str(item)) for item in data["open_issues"])
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:background w:color="F5F4ED"/><w:body>{"".join(body)}<w:sectPr><w:pgSz w:w="{WORD_PAGE_WIDTH}" w:h="{WORD_PAGE_HEIGHT}" w:orient="landscape"/><w:pgMar w:top="{WORD_MARGIN}" w:right="{WORD_MARGIN}" w:bottom="{WORD_MARGIN}" w:left="{WORD_MARGIN}"/></w:sectPr></w:body></w:document>'
    styles = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:b/><w:sz w:val="42"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style></w:styles>'
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
        archive.writestr("_rels/.rels", '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        archive.writestr("word/_rels/document.xml.rels", '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
        archive.writestr("word/document.xml", document)
        archive.writestr("word/styles.xml", styles)


def pdf_profile(path: Path) -> dict[str, Any]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return {"pages": len(reader.pages), "text_chars": len(text.strip())}


def docx_profile(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as archive:
        document = archive.read("word/document.xml").decode("utf-8")
    grid_widths = [sum(map(int, re.findall(r'w:gridCol w:w="(\d+)"', grid))) for grid in re.findall(r"<w:tblGrid>.*?</w:tblGrid>", document)]
    max_grid = max(grid_widths or [0])
    return {
        "table_count": document.count("<w:tbl>"),
        "auto_table_count": len(re.findall(r'<w:tblW[^>]+w:type="auto"', document)),
        "max_grid_width": max_grid,
        "content_width": WORD_CONTENT_WIDTH,
        "layout_safety_margin": WORD_CONTENT_WIDTH - max_grid,
        "manual_break_count": document.count("<w:br/>"),
    }


def quality(data: dict[str, Any], paths: dict[str, Path]) -> dict[str, Any]:
    evidence_ids = {item.get("id") for item in data["evidence"]}
    entity_ids = {item.get("id") for item in data["entities"]}
    entity_types = {item.get("type") for item in data["entities"]}
    issues: list[str] = []
    warnings: list[str] = []
    missing_types = sorted(CORE_TYPES - entity_types)
    if missing_types:
        warnings.append("缺少核心实体类型：" + "、".join(missing_types))
    missing_enriched = [title for key, title, _ in ENRICHED_SECTIONS if not data.get(key)]
    if missing_enriched:
        issues.append("缺少系统化分析模块：" + "、".join(missing_enriched))
    source_validation = data.get("source_validation", [])
    if not source_validation:
        issues.append("缺少真实数据来源核验模块")
    source_validation_ids = {item.get("source_id") for item in source_validation}
    missing_source_validation = sorted(evidence_ids - source_validation_ids)
    if missing_source_validation:
        warnings.append("部分来源未做 URL 连通核验：" + "、".join(missing_source_validation))
    for entity in data["entities"]:
        if entity.get("confidence") not in CONFIDENCE:
            issues.append(f"实体可信等级无效：{entity.get('id')}")
        if entity.get("privacy_review") not in PRIVACY:
            issues.append(f"实体隐私状态无效：{entity.get('id')}")
        for source_id in as_list(entity.get("source_ids")):
            if source_id not in evidence_ids:
                issues.append(f"实体引用不存在来源：{entity.get('id')} / {source_id}")
    for relation in data["relations"]:
        if relation.get("subject") not in entity_ids or relation.get("object") not in entity_ids:
            issues.append(f"关系实体不存在：{relation.get('subject')}->{relation.get('object')}")
        if not as_list(relation.get("evidence_ids")):
            issues.append(f"关系缺少证据：{relation.get('subject')}->{relation.get('object')}")
        for evidence_id in as_list(relation.get("evidence_ids")):
            if evidence_id not in evidence_ids:
                issues.append(f"关系引用不存在证据：{evidence_id}")
    for triple in data["triples"]:
        for evidence_id in as_list(triple.get("evidence_ids")):
            if evidence_id not in evidence_ids:
                issues.append(f"三元组引用不存在证据：{evidence_id}")
    for label, path in paths.items():
        if not path.exists() or path.stat().st_size == 0:
            issues.append(f"{label} 文件缺失或为空")
    docx = docx_profile(paths["docx"])
    expected_tables = 7 + (1 if data.get("platform_test_scenarios") else 0) + sum(1 for key, _, _ in ENRICHED_SECTIONS if data.get(key))
    if docx["table_count"] < expected_tables:
        issues.append(f"DOCX 表格不足：{docx['table_count']}<{expected_tables}")
    if docx["auto_table_count"]:
        issues.append(f"DOCX 仍存在自动表宽：{docx['auto_table_count']}")
    if docx["max_grid_width"] > WORD_CONTENT_WIDTH:
        issues.append(f"DOCX 表格宽度超过正文宽度：{docx['max_grid_width']}>{WORD_CONTENT_WIDTH}")
    pdf = pdf_profile(paths["pdf"])
    if pdf["pages"] <= 0 or pdf["text_chars"] <= 100:
        issues.append("PDF 页数或文本不足")
    html_text = paths["html"].read_text(encoding="utf-8") if paths["html"].exists() else ""
    html_sticky_nav_present = "report-nav" in html_text and "position:sticky" in html_text.replace(" ", "")
    html_overflow_protection_present = "overflow-wrap:anywhere" in html_text and "word-break:break-word" in html_text.replace(" ", "")
    kami_palette_present = all(token in html_text for token in ["#f5f4ed", "#faf9f5", "#1B365D", "#e8e6dc"])
    if not html_sticky_nav_present:
        issues.append("HTML 缺少固定跟随菜单栏")
    if not html_overflow_protection_present:
        issues.append("HTML 缺少长文本防溢出规则")
    if not kami_palette_present:
        issues.append("HTML 未使用 kami paper 色板")
    if data["json_ld"].get("name") != data["brand_name"]:
        issues.append("JSON-LD name 与品牌规范名不一致")
    return {
        "skill_id": "yao-geo-brand-graph",
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "status": "pass" if not issues else "fail",
        "issues": issues,
        "warnings": warnings,
        "checks": {
            "entity_count": len(data["entities"]),
            "relation_count": len(data["relations"]),
            "evidence_count": len(data["evidence"]),
            "core_entity_types_present": sorted(entity_types & CORE_TYPES),
            "platform_test_scenario_count": len(data.get("platform_test_scenarios", [])),
            "enriched_section_count": sum(1 for key, _, _ in ENRICHED_SECTIONS if data.get(key)),
            "enriched_sections_required": [title for _, title, _ in ENRICHED_SECTIONS],
            "source_validation_count": len(source_validation),
            "source_validation_reachable_count": sum(1 for item in source_validation if item.get("reachable")),
            "four_format_outputs_checked": True,
            "html_sticky_nav_present": html_sticky_nav_present,
            "html_overflow_protection_present": html_overflow_protection_present,
            "kami_palette_present": kami_palette_present,
            "report_layout_profile": "kami-paper-long-doc",
            "docx_profile": docx,
            "pdf_profile": pdf,
            "file_sizes": {label: path.stat().st_size for label, path in paths.items() if path.exists()},
        },
    }


def main() -> None:
    args = parse_args()
    data = load_input(Path(args.input))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    base = slug(data.get("slug") or data["brand_name"]) + "-yao-geo-brand-graph"
    paths = {
        "markdown": output_dir / f"{base}.md",
        "html": output_dir / f"{base}.html",
        "pdf": output_dir / f"{base}.pdf",
        "docx": output_dir / f"{base}.docx",
    }
    paths["markdown"].write_text(render_markdown(data), encoding="utf-8")
    paths["html"].write_text(render_html(data), encoding="utf-8")
    from weasyprint import HTML

    HTML(filename=str(paths["html"])).write_pdf(str(paths["pdf"]))
    render_docx(data, paths["docx"])
    result = quality(data, paths)
    quality_path = output_dir / "quality-report.json"
    quality_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": result["status"] == "pass", "outputs": {key: str(path) for key, path in paths.items()}, "quality_report": str(quality_path)}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 2)


if __name__ == "__main__":
    main()
