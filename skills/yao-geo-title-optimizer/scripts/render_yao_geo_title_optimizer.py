#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-title-optimizer
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Render GEO Title Lab reports to Markdown, HTML, DOCX, PDF."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape as xml_escape


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
PAGE_W = 11906
PAGE_H = 16838
PAGE_MARGIN = 1134
TABLE_W = 9000
BANNED_TERMS = ["最佳", "最新", "最强", "第一", "唯一", "权威", "行业标准", "必选", "必看", "保证收录", "保证引用", "全网最全", "保姆级", "一文读懂", "看这篇就够了"]
NEUTRAL_TYPES = {"榜单型", "比较型", "决策型", "推荐型", "指南型", "评测型", "横评型", "采购建议型", "清单型", "检查表型", "避坑型"}
PROJECT_FIELDS = ["name", "module", "priority", "project_date", "region", "audience", "target_platforms", "article_types"]
TITLE_FIELDS = ["id", "title", "type", "intent", "scenario", "platform_fit", "why_it_works", "rewrite_advice", "scores"]
SCORE_FIELDS = ["intent_match", "entity_clarity", "differentiation", "citation_potential", "compliance", "freshness"]
DEPTH_REQUIRED_SECTIONS = ["data_source_audit", "platform_sampling_plan", "reference_frameworks", "analysis_dimensions", "entity_intent_matrix", "coverage_gaps", "publication_checklist"]
SECTION_SPECS = [
    ("data_source_audit", "真实数据状态与采集边界", ["数据对象", "采集方式", "状态", "使用边界"], [1700, 2500, 1700, 3100]),
    ("platform_sampling_plan", "国内 AI 平台真实采样计划", ["平台", "真实采样问题", "采样输出", "判定方法"], [1400, 3300, 2200, 2100]),
    ("reference_frameworks", "权威参考与理论依据", ["来源", "权威性", "可借鉴原则", "如何用于标题实验"], [1700, 2300, 2600, 2400]),
    ("analysis_dimensions", "系统分析维度", ["维度", "核心问题", "标题信号", "补充要求"], [1500, 2900, 2300, 2300]),
    ("entity_intent_matrix", "实体与意图矩阵", ["主体/实体", "用户意图", "场景限定", "标题表达要求"], [1700, 2300, 2300, 2700]),
    ("title_pattern_library", "标题结构模式库", ["结构", "适用场景", "标题公式", "风险边界"], [1500, 2400, 3100, 2000]),
    ("coverage_gaps", "覆盖缺口与补全建议", ["缺口", "影响", "补全动作", "优先级"], [1700, 2700, 3400, 1200]),
    ("publication_checklist", "发布前检查清单", ["检查项", "标准", "状态", "说明"], [1700, 2900, 1400, 3000]),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def load_input(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["output_stem", "report_title", "generated_at", "project", "title_candidates", "compliance_checks", "structure_map", "self_review"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Missing required input keys: {', '.join(missing)}")
    validate_report_input(data)
    return data


def validate_report_input(data: dict[str, Any]) -> None:
    project = data.get("project", {})
    missing_project = [key for key in PROJECT_FIELDS if key not in project]
    if missing_project:
        raise ValueError(f"Missing required project keys: {', '.join(missing_project)}")
    for key in ["target_platforms", "article_types"]:
        if not isinstance(project.get(key), list):
            raise ValueError(f"Project field {key} must be a list")
    if not data.get("title_candidates"):
        raise ValueError("title_candidates must contain at least one title")
    for index, item in enumerate(data["title_candidates"], 1):
        missing_title = [key for key in TITLE_FIELDS if key not in item]
        if missing_title:
            raise ValueError(f"title_candidates[{index}] missing keys: {', '.join(missing_title)}")
        missing_scores = [key for key in SCORE_FIELDS if key not in item["scores"]]
        if missing_scores:
            raise ValueError(f"title_candidates[{index}].scores missing keys: {', '.join(missing_scores)}")
        for key in SCORE_FIELDS:
            value = item["scores"][key]
            if not isinstance(value, (int, float)) or value < 0 or value > 5:
                raise ValueError(f"title_candidates[{index}].scores.{key} must be a number from 0 to 5")
    for key in ["compliance_checks", "structure_map", "self_review"]:
        if not isinstance(data.get(key), list) or not data[key]:
            raise ValueError(f"{key} must be a non-empty list")


def score_total(scores: dict[str, int | float]) -> int:
    return round(sum(float(v) for v in scores.values()) / max(len(scores) * 5, 1) * 100)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(md_escape(h) for h in headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        normalized = list(row) + [""] * (len(headers) - len(row))
        lines.append("| " + " | ".join(md_escape(cell) for cell in normalized[: len(headers)]) + " |")
    return "\n".join(lines)


def title_rows(data: dict[str, Any]) -> list[list[Any]]:
    rows = []
    for item in data["title_candidates"]:
        rows.append([item["id"], item["title"], item["type"], item["intent"], item["scenario"], item["platform_fit"], score_total(item["scores"]), item["why_it_works"], item["rewrite_advice"]])
    return rows


def score_rows(data: dict[str, Any]) -> list[list[Any]]:
    rows = []
    for item in data["title_candidates"]:
        s = item["scores"]
        rows.append([item["id"], s["intent_match"], s["entity_clarity"], s["differentiation"], s["citation_potential"], s["compliance"], s["freshness"], score_total(s)])
    return rows


def section_spec(key: str) -> tuple[str, list[str], list[int]] | None:
    for item_key, title, headers, widths in SECTION_SPECS:
        if item_key == key:
            return title, headers, widths
    return None


def optional_md_sections(data: dict[str, Any], keys: list[str] | None = None) -> list[str]:
    selected = keys or [key for key, _, _, _ in SECTION_SPECS]
    parts: list[str] = []
    for key in selected:
        spec = section_spec(key)
        rows = data.get(key)
        if not spec or not rows:
            continue
        title, headers, _ = spec
        parts.extend(["", f"## {title}", "", md_table(headers, rows)])
    return parts


def markdown_notice(data: dict[str, Any]) -> str:
    project = data.get("prepared_by", "yao-geo-title-optimizer")
    return "\n".join(
        [
            "<!--",
            "Copyright © 2026 姚金刚. All rights reserved.",
            f"Project: {project}",
            "Created by: 姚金刚",
            "Date: 2026-05-16",
            "X: https://x.com/yaojingang",
            "-->",
            "",
        ]
    )


def render_markdown(data: dict[str, Any]) -> str:
    project = data["project"]
    lines = [
        markdown_notice(data),
        f"# {data['report_title']}",
        "",
        data.get("subtitle", ""),
        "",
        "## 项目摘要",
        "",
        md_table(
            ["字段", "内容"],
            [
                ["项目名称", project["name"]],
                ["所属模块", project["module"]],
                ["优先级", project["priority"]],
                ["项目日期", project["project_date"]],
                ["地域", project["region"]],
                ["面向对象", project["audience"]],
                ["目标平台", "、".join(project["target_platforms"])],
                ["文章类型", "、".join(project["article_types"])],
                ["年份锚点", "允许" if project.get("allow_year_anchor") else "不允许"],
                ["月份锚点", "允许" if project.get("allow_month_anchor") else "不允许"],
            ],
        ),
        "",
        "## 方法摘要",
        "",
    ]
    lines.extend(f"- {item}" for item in data.get("method_summary", []))
    if data.get("scenario_selection"):
        sc = data["scenario_selection"]
        lines.extend(["", "## 测试场景选择", "", md_table(["字段", "内容"], [["测试对象", sc.get("test_object", "")], ["测试场景", sc.get("scenario", "")], ["用户问题", sc.get("user_questions", "")], ["内容目标", sc.get("content_goal", "")], ["国内平台假设", sc.get("china_platform_assumption", "")]])])
    if data.get("evidence_sources"):
        lines.extend(["", "## 公开证据表", "", md_table(["来源", "链接", "关键事实", "如何用于标题测试"], [[x["source"], x["url"], x["fact"], x["how_used"]] for x in data["evidence_sources"]])])
    lines.extend(optional_md_sections(data, ["data_source_audit", "platform_sampling_plan", "reference_frameworks", "analysis_dimensions", "entity_intent_matrix"]))
    lines.extend(
        [
            "",
            "## 国内平台适配",
            "",
            md_table(["平台", "标题侧重点", "推荐表达"], data.get("platform_adaptation", [])),
            "",
            "## 标题候选库",
            "",
            md_table(["ID", "标题", "类型", "意图", "场景", "平台适配", "总分", "理由", "改写建议"], title_rows(data)),
            "",
            "## 标题评分",
            "",
            md_table(["ID", "意图匹配", "实体清晰", "差异化", "可引用性", "合规性", "新鲜度", "总分"], score_rows(data)),
            *optional_md_sections(data, ["title_pattern_library", "coverage_gaps", "publication_checklist"]),
            "",
            "## 标题禁用词与合规检查",
            "",
            md_table(["检查项", "对象", "结果", "说明"], data["compliance_checks"]),
            "",
            "## 标题到文章结构的映射",
            "",
            md_table(["标题ID", "文章结构", "段落与证据模块", "FAQ映射"], data["structure_map"]),
            "",
            "## 自检与迭代记录",
            "",
            md_table(["类型", "发现的问题", "已修复动作"], data["self_review"]),
            "",
        ]
    )
    return "\n".join(lines)


def html_table(headers: list[str], rows: list[list[Any]], class_name: str = "") -> str:
    head = "".join(f"<th>{html.escape(str(h))}</th>" for h in headers)
    body = []
    for row in rows:
        normalized = list(row) + [""] * (len(headers) - len(row))
        body.append("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in normalized[: len(headers)]) + "</tr>")
    cls = f' class="{class_name}"' if class_name else ""
    return f'<div class="table-wrap"><table{cls}><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def html_section(section_id: str, title: str, content: str) -> str:
    return f'<section class="section" id="{section_id}"><h2>{html.escape(title)}</h2>{content}</section>'


def optional_html_sections(data: dict[str, Any], keys: list[str]) -> str:
    parts = []
    for key in keys:
        spec = section_spec(key)
        rows = data.get(key)
        if not spec or not rows:
            continue
        title, headers, _ = spec
        parts.append(html_section(key.replace("_", "-"), title, html_table(headers, rows)))
    return "".join(parts)


def nav_html(data: dict[str, Any]) -> str:
    links = [
        ("overview", "概览"),
        ("method", "方法"),
        ("scenario", "场景"),
        ("evidence", "证据"),
    ]
    for key, title, _, _ in SECTION_SPECS:
        if data.get(key):
            links.append((key.replace("_", "-"), title.replace("与", "/")))
    links.extend(
        [
            ("platform", "平台适配"),
            ("title-library", "标题库"),
            ("scorecard", "评分"),
            ("structure-map", "结构映射"),
            ("self-review", "自检"),
        ]
    )
    return '<nav class="report-nav" aria-label="报告目录"><div class="nav-inner">' + "".join(
        f'<a href="#{section_id}">{html.escape(label)}</a>' for section_id, label in links
    ) + "</div></nav>"


def render_html(data: dict[str, Any]) -> str:
    p = data["project"]
    metrics = "".join(f'<div class="metric"><span>{html.escape(k)}</span><strong>{html.escape(v)}</strong></div>' for k, v in [("所属模块", p["module"]), ("优先级", p["priority"]), ("项目日期", p["project_date"]), ("目标平台", "、".join(p["target_platforms"])), ("文章类型", "、".join(p["article_types"])), ("品牌隔离", "开启" if p.get("brand_isolation_required") else "关闭")])
    method = "".join(f"<li>{html.escape(x)}</li>" for x in data.get("method_summary", []))
    scenario_html = ""
    if data.get("scenario_selection"):
        s = data["scenario_selection"]
        scenario_html = html_section("scenario", "测试场景选择", html_table(["字段", "内容"], [["测试对象", s.get("test_object", "")], ["测试场景", s.get("scenario", "")], ["用户问题", s.get("user_questions", "")], ["内容目标", s.get("content_goal", "")], ["国内平台假设", s.get("china_platform_assumption", "")]]))
    evidence_html = ""
    if data.get("evidence_sources"):
        evidence_html = html_section("evidence", "公开证据表", html_table(["来源", "链接", "关键事实", "如何用于标题测试"], [[x["source"], x["url"], x["fact"], x["how_used"]] for x in data["evidence_sources"]]))
    nav = nav_html(data)
    depth_top = optional_html_sections(data, ["data_source_audit", "platform_sampling_plan", "reference_frameworks", "analysis_dimensions", "entity_intent_matrix"])
    depth_late = optional_html_sections(data, ["title_pattern_library", "coverage_gaps", "publication_checklist"])
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(data['report_title'])}</title>
<style>
:root{{--paper:#ffffff;--surface:#faf9f5;--wash:#f5f4ed;--ink:#141413;--text:#3d3d3a;--muted:#5e5d59;--stone:#87867f;--brand:#1B365D;--border:#e8e5da;--border-strong:#d8d3c6;--tag:#EEF2F7}}
html{{scroll-behavior:smooth}}html,body{{margin:0;background:#ffffff;color:var(--ink);font-family:"Inter","Source Han Sans SC","PingFang SC","Microsoft YaHei",Arial,sans-serif;line-height:1.52;letter-spacing:0}}
.skip-link{{position:absolute;left:16px;top:-60px;background:var(--brand);color:#fff;padding:8px 12px;border-radius:4px;z-index:30}}.skip-link:focus{{top:10px}}
.report{{width:min(1120px,calc(100vw - 36px));margin:0 auto;padding:32px 0 72px}}
.hero{{border-bottom:1.5px solid var(--brand);padding:22px 0 24px;margin-bottom:0;scroll-margin-top:88px}}.eyebrow{{color:var(--brand);font-size:12px;font-weight:600;letter-spacing:.5px;text-transform:uppercase}}h1{{font-family:"TsangerJinKai02","Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;font-size:35px;font-weight:500;line-height:1.18;margin:0 0 12px;color:var(--ink)}}.subtitle{{color:var(--muted);font-size:16px;max-width:900px;line-height:1.55}}.meta{{display:flex;flex-wrap:wrap;gap:8px 18px;color:var(--stone);font-size:12.5px;margin-top:14px}}
.report-nav{{position:sticky;top:0;z-index:20;background:var(--paper);border-bottom:1px solid var(--border);box-shadow:0 1px 0 var(--border)}}.nav-inner{{width:min(1120px,calc(100vw - 36px));margin:0 auto;display:flex;gap:7px;overflow-x:auto;padding:8px 0;white-space:nowrap}}.report-nav a{{color:var(--text);text-decoration:none;border:1px solid var(--border);border-radius:4px;padding:4px 9px;font-size:12px;background:var(--surface)}}.report-nav a:focus,.report-nav a:hover{{border-color:var(--brand);color:var(--brand);outline:none}}
.metrics{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:20px 0 26px}}.metric{{border:1px solid var(--border);border-radius:6px;padding:12px 14px;background:var(--surface);min-width:0}}.metric span{{display:block;color:var(--stone);font-size:12px}}.metric strong{{display:block;font-size:15px;font-weight:600;color:var(--ink);overflow-wrap:anywhere;word-break:break-word}}
.section{{margin:28px 0;padding-top:4px;scroll-margin-top:88px}}.section h2{{font-family:"TsangerJinKai02","Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;margin:0 0 12px;padding:0 0 8px;border-bottom:1px solid var(--border);font-size:23px;font-weight:500;color:var(--ink)}}.section h2::before{{content:"";display:inline-block;width:4px;height:18px;background:var(--brand);margin-right:8px;vertical-align:-2px}}.note{{border-left:3px solid var(--brand);background:var(--surface);padding:12px 14px;margin:12px 0;color:var(--text)}}li{{margin:4px 0;color:var(--text)}}
.table-wrap{{width:100%;overflow-x:auto;margin:12px 0 18px;border:1px solid var(--border);border-radius:6px;background:var(--paper)}}table{{width:100%;border-collapse:collapse;table-layout:fixed;background:var(--paper)}}th,td{{border:1px solid var(--border);padding:8px 9px;vertical-align:top;text-align:left;overflow-wrap:anywhere;word-break:break-word;hyphens:auto;font-size:12.5px;line-height:1.48;color:var(--text)}}th{{background:var(--surface);color:var(--brand);font-weight:600}}.title-table th:nth-child(1),.title-table td:nth-child(1){{width:52px}}.title-table th:nth-child(2),.title-table td:nth-child(2){{width:24%}}.score-table th,.score-table td{{text-align:center}}
@page{{size:A4;margin:20mm 18mm;background:#ffffff;@bottom-center{{content:"GEO Title Lab · yao-geo-title-optimizer · " counter(page);font-size:8.5pt;color:#87867f}}}}@media print{{.skip-link,.report-nav{{display:none}}.report{{width:100%;padding:0}}.table-wrap{{overflow:visible;break-inside:auto}}table{{page-break-inside:auto}}tr{{page-break-inside:auto;page-break-after:auto}}thead{{display:table-header-group}}th,td{{font-size:9.8px;padding:5.5px 6px;line-height:1.42}}.title-table th,.title-table td{{font-size:8.8px;padding:5px;line-height:1.38}}h1{{font-size:25px}}.section h2{{font-size:17px}}}}
@media(max-width:760px){{.report{{width:min(100% - 24px,1120px)}}h1{{font-size:25px}}.metrics{{grid-template-columns:1fr}}table{{min-width:760px}}}}
</style></head><body><a class="skip-link" href="#main-content">跳到正文</a>{nav}<main class="report" id="main-content"><header class="hero" id="overview"><p class="eyebrow">GEO Title Lab</p><h1>{html.escape(data['report_title'])}</h1><p class="subtitle">{html.escape(data.get('subtitle',''))}</p><div class="meta"><span>生成日期：{html.escape(data['generated_at'])}</span><span>生成器：{html.escape(data.get('prepared_by','yao-geo-title-optimizer'))}</span><span>项目：{html.escape(p['name'])}</span></div></header>
<section class="metrics">{metrics}</section>{html_section("method", "方法摘要", '<div class="note">本报告把标题优化拆成检索触发、结构理解、证据可信度和引用吸收四层，并把每个标题映射到评分、合规和文章结构。</div><ul>' + method + '</ul>')}{scenario_html}{evidence_html}{depth_top}
{html_section("platform", "国内平台适配", html_table(["平台","标题侧重点","推荐表达"], data.get("platform_adaptation", [])))}
{html_section("title-library", "标题候选库", html_table(["ID","标题","类型","意图","场景","平台适配","总分","理由","改写建议"], title_rows(data), "title-table"))}
{html_section("scorecard", "标题评分", html_table(["ID","意图匹配","实体清晰","差异化","可引用性","合规性","新鲜度","总分"], score_rows(data), "score-table"))}{depth_late}
{html_section("compliance", "标题禁用词与合规检查", html_table(["检查项","对象","结果","说明"], data["compliance_checks"]))}
{html_section("structure-map", "标题到文章结构的映射", html_table(["标题ID","文章结构","段落与证据模块","FAQ映射"], data["structure_map"]))}
{html_section("self-review", "自检与迭代记录", html_table(["类型","发现的问题","已修复动作"], data["self_review"]))}</main></body></html>"""


def word_safe(value: Any) -> str:
    text = str(value)
    if "http://" in text or "https://" in text:
        text = re.sub(r"([/?=&])", r"\1 ", text)
    text = re.sub(r"([A-Za-z0-9]{28})(?=[A-Za-z0-9])", r"\1 ", text)
    return text


def wr(text: Any, bold: bool = False, size: int | None = None, color: str | None = None) -> str:
    props = []
    if bold:
        props.append("<w:b/>")
    if size:
        props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{xml_escape(word_safe(text))}</w:t></w:r>'


def wp(text: Any, style: str = "Normal", after: int = 120, bold: bool = False, size: int | None = None, color: str | None = None, align: str | None = None) -> str:
    style_xml = f'<w:pStyle w:val="{style}"/>' if style else ""
    align_xml = f'<w:jc w:val="{align}"/>' if align else ""
    return f'<w:p><w:pPr>{style_xml}<w:spacing w:after="{after}" w:line="300" w:lineRule="auto"/>{align_xml}</w:pPr>{wr(text,bold,size,color)}</w:p>'


def wc(text: Any, width: int, header: bool = False) -> str:
    fill = '<w:shd w:fill="FAF9F5"/>' if header else ""
    return f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/><w:tcMar><w:top w:w="100" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:bottom w:w="100" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar><w:vAlign w:val="center"/>{fill}</w:tcPr>{wp(text, "TableHeader" if header else "TableCell", after=0, bold=header, align="center" if header or len(str(text)) <= 8 else None)}</w:tc>'


def wt(headers: list[str], rows: list[list[Any]], widths: list[int]) -> str:
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    border = '<w:top w:val="single" w:sz="4" w:color="E8E5DA"/><w:left w:val="single" w:sz="4" w:color="E8E5DA"/><w:bottom w:val="single" w:sz="4" w:color="E8E5DA"/><w:right w:val="single" w:sz="4" w:color="E8E5DA"/><w:insideH w:val="single" w:sz="4" w:color="E8E5DA"/><w:insideV w:val="single" w:sz="4" w:color="E8E5DA"/>'
    parts = [f'<w:tbl><w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:tblLayout w:type="fixed"/><w:tblInd w:w="0" w:type="dxa"/><w:tblBorders>{border}</w:tblBorders></w:tblPr><w:tblGrid>{grid}</w:tblGrid>']
    if headers:
        parts.append("<w:tr><w:trPr><w:tblHeader/></w:trPr>" + "".join(wc(h, w, True) for h, w in zip(headers, widths, strict=False)) + "</w:tr>")
    for row in rows:
        normalized = list(row) + [""] * (len(widths) - len(row))
        parts.append("<w:tr>" + "".join(wc(c, w) for c, w in zip(normalized[: len(widths)], widths, strict=False)) + "</w:tr>")
    parts.append("</w:tbl>" + wp("", after=160))
    return "".join(parts)


def kv(rows: list[list[Any]]) -> str:
    return wt(["字段", "内容"], rows, [1500, 7500])


def optional_docx_sections(data: dict[str, Any], keys: list[str]) -> list[str]:
    body: list[str] = []
    for key in keys:
        spec = section_spec(key)
        rows = data.get(key)
        if not spec or not rows:
            continue
        title, headers, widths = spec
        body += [wp(title, "Heading1"), wt(headers, rows, widths)]
    return body


def render_docx_xml(data: dict[str, Any]) -> str:
    p = data["project"]
    body = [wp(data["report_title"], "Title", 180), wp(data.get("subtitle", ""), "Subtitle", 220), wp(f"生成日期：{data['generated_at']}    生成器：{data.get('prepared_by','yao-geo-title-optimizer')}", "Meta", 240)]
    body += [wp("项目摘要", "Heading1"), kv([["项目名称", p["name"]], ["所属模块", p["module"]], ["优先级", p["priority"]], ["项目日期", p["project_date"]], ["地域", p["region"]], ["面向对象", p["audience"]], ["目标平台", "、".join(p["target_platforms"])], ["文章类型", "、".join(p["article_types"])], ["年份锚点", "允许" if p.get("allow_year_anchor") else "不允许"], ["月份锚点", "允许" if p.get("allow_month_anchor") else "不允许"]])]
    body.append(wp("方法摘要", "Heading1"))
    for i, item in enumerate(data.get("method_summary", []), 1):
        body.append(wp(f"{i}. {item}"))
    if data.get("scenario_selection"):
        s = data["scenario_selection"]
        body += [wp("测试场景选择", "Heading1"), kv([["测试对象", s.get("test_object", "")], ["测试场景", s.get("scenario", "")], ["用户问题", s.get("user_questions", "")], ["内容目标", s.get("content_goal", "")], ["国内平台假设", s.get("china_platform_assumption", "")]])]
    if data.get("evidence_sources"):
        body += [wp("公开证据表", "Heading1"), wt(["来源", "关键事实", "如何用于标题测试"], [[x["source"], x["fact"], x["how_used"]] for x in data["evidence_sources"]], [1800, 4300, 2900])]
    body += optional_docx_sections(data, ["data_source_audit", "platform_sampling_plan", "reference_frameworks", "analysis_dimensions", "entity_intent_matrix"])
    body += [wp("国内平台适配", "Heading1"), wt(["平台", "标题侧重点", "推荐表达"], data.get("platform_adaptation", []), [1400, 3500, 4100])]
    body += [wp("标题候选库", "Heading1"), wp("Word 版将候选标题拆为逐条卡片，避免九列表格在页面右侧溢出。", "Callout")]
    for item in data["title_candidates"]:
        body.append(wp(f"{item['id']}  {item['title']}", "Heading2"))
        body.append(kv([["类型", item["type"]], ["意图", item["intent"]], ["场景", item["scenario"]], ["平台适配", item["platform_fit"]], ["总分", score_total(item["scores"])], ["理由", item["why_it_works"]], ["改写建议", item["rewrite_advice"]]]))
    body += [wp("标题评分", "Heading1"), wt(["ID", "意图", "实体", "差异", "引用", "合规", "新鲜", "总分"], score_rows(data), [800, 1050, 1050, 1050, 1050, 1050, 1050, 900])]
    body += optional_docx_sections(data, ["title_pattern_library", "coverage_gaps", "publication_checklist"])
    body += [wp("标题禁用词与合规检查", "Heading1"), wt(["检查项", "对象", "结果", "说明"], data["compliance_checks"], [1400, 1700, 1200, 4700])]
    body += [wp("标题到文章结构的映射", "Heading1"), wt(["标题ID", "文章结构", "段落与证据模块", "FAQ映射"], data["structure_map"], [900, 1900, 3900, 2300])]
    body += [wp("自检与迭代记录", "Heading1"), wt(["类型", "发现的问题", "已修复动作"], data["self_review"], [1300, 3850, 3850])]
    body.append(f'<w:sectPr><w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/><w:pgMar w:top="{PAGE_MARGIN}" w:right="{PAGE_MARGIN}" w:bottom="{PAGE_MARGIN}" w:left="{PAGE_MARGIN}" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>')
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="{W_NS}"><w:body>{"".join(body)}</w:body></w:document>'


def styles_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="{W_NS}">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:eastAsia="Microsoft YaHei" w:hAnsi="Arial"/><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:eastAsia="Microsoft YaHei"/><w:sz w:val="21"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:b/><w:sz w:val="34"/><w:color w:val="141413"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:rPr><w:color w:val="5E5D59"/><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Meta"><w:name w:val="Meta"/><w:rPr><w:color w:val="87867F"/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:spacing w:before="260" w:after="120"/></w:pPr><w:rPr><w:b/><w:color w:val="1B365D"/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:spacing w:before="180" w:after="100"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Callout"><w:name w:val="Callout"/><w:rPr><w:color w:val="5C6B78"/><w:sz w:val="19"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TableCell"><w:name w:val="Table Cell"/><w:pPr><w:spacing w:after="0" w:line="270" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TableHeader"><w:name w:val="Table Header"/><w:pPr><w:spacing w:after="0" w:line="270" w:lineRule="auto"/></w:pPr><w:rPr><w:b/><w:color w:val="102A34"/><w:sz w:val="18"/></w:rPr></w:style>
</w:styles>'''


def write_docx(data: dict[str, Any], path: Path) -> None:
    content_types = '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'
    rels = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", render_docx_xml(data))
        z.writestr("word/styles.xml", styles_xml())
        z.writestr("word/_rels/document.xml.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')


def write_pdf(html_text: str, path: Path, base_url: Path) -> None:
    from weasyprint import HTML
    HTML(string=html_text, base_url=str(base_url)).write_pdf(str(path))


def inspect_docx(path: Path) -> dict[str, Any]:
    if not path.exists() or not zipfile.is_zipfile(path):
        return {"valid": False, "issues": ["DOCX missing or invalid"], "tables": []}
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    ns = {"w": W_NS}
    sect = root.find(".//w:sectPr", ns)
    if sect is None:
        return {"valid": False, "issues": ["DOCX missing section properties"], "tables": []}
    size = sect.find("w:pgSz", ns)
    mar = sect.find("w:pgMar", ns)
    if size is None or mar is None:
        return {"valid": False, "issues": ["DOCX missing page size or margins"], "tables": []}
    usable = int(size.attrib.get(f"{{{W_NS}}}w", PAGE_W)) - int(mar.attrib.get(f"{{{W_NS}}}left", PAGE_MARGIN)) - int(mar.attrib.get(f"{{{W_NS}}}right", PAGE_MARGIN))
    issues = []
    tables = []
    for i, tbl in enumerate(root.findall(".//w:tbl", ns), 1):
        grid = sum(int(c.attrib.get(f"{{{W_NS}}}w", 0)) for c in tbl.findall("./w:tblGrid/w:gridCol", ns))
        over = grid > usable
        if over:
            issues.append(f"table {i} exceeds usable page width")
        tables.append({"index": i, "grid_width": grid, "usable_width": usable, "overflows": over})
    return {"valid": True, "usable_width": usable, "table_count": len(tables), "tables": tables, "issues": issues}


def inspect_pdf(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"valid": False, "pages": 0, "issues": ["PDF missing"]}
    if path.read_bytes()[:4] != b"%PDF":
        return {"valid": False, "pages": 0, "issues": ["PDF header invalid"]}
    reader = None
    parser = None
    for module_name in ("pypdf", "PyPDF2"):
        try:
            module = __import__(module_name, fromlist=["PdfReader"])
            reader = module.PdfReader(str(path))
            parser = module_name
            break
        except ImportError:
            continue
        except Exception as exc:
            return {"valid": False, "pages": 0, "parser": module_name, "issues": [f"PDF parse failed: {exc}"]}
    if reader is None:
        return {"valid": False, "pages": 0, "issues": ["No PDF parser available"]}
    try:
        pages = len(reader.pages)
    except Exception as exc:
        return {"valid": False, "pages": 0, "parser": parser, "issues": [f"PDF page read failed: {exc}"]}
    issues = [] if pages > 0 else ["PDF has no pages"]
    return {"valid": not issues, "pages": pages, "parser": parser, "issues": issues}


def review(data: dict[str, Any], paths: dict[str, Path], html_text: str) -> dict[str, Any]:
    issues = []
    for key, path in paths.items():
        if not path.exists() or path.stat().st_size < 1000:
            issues.append({"severity": "blocker", "issue": f"{key} missing or too small", "path": str(path)})
    for token in ["background:#ffffff", "table-layout:fixed", "word-break:break-word", "@page", "position:sticky", "report-nav"]:
        if token not in html_text.replace(" ", ""):
            issues.append({"severity": "major", "issue": f"HTML missing layout token: {token}", "path": str(paths["html"])})
    depth = {
        "required_sections": DEPTH_REQUIRED_SECTIONS,
        "missing_sections": [key for key in DEPTH_REQUIRED_SECTIONS if not data.get(key)],
        "title_count": len(data.get("title_candidates", [])),
        "structure_map_count": len(data.get("structure_map", [])),
        "evidence_source_count": len(data.get("evidence_sources", [])),
    }
    if depth["missing_sections"]:
        issues.append({"severity": "major", "issue": "Report missing depth sections: " + ", ".join(depth["missing_sections"]), "path": str(paths["markdown"])})
    if depth["title_count"] < 6:
        issues.append({"severity": "major", "issue": "Report has fewer than 6 title candidates", "path": str(paths["markdown"])})
    if depth["structure_map_count"] < 4:
        issues.append({"severity": "major", "issue": "Report has fewer than 4 title-to-structure mappings", "path": str(paths["markdown"])})
    docx = inspect_docx(paths["docx"])
    for item in docx.get("issues", []):
        issues.append({"severity": "blocker", "issue": f"DOCX layout issue: {item}", "path": str(paths["docx"])})
    pdf = inspect_pdf(paths["pdf"])
    for item in pdf.get("issues", []):
        issues.append({"severity": "blocker", "issue": f"PDF issue: {item}", "path": str(paths["pdf"])})
    protected = [data["project"].get("target_brand", "")] + data["project"].get("competitors", [])
    for item in data["title_candidates"]:
        title = item["title"]
        for term in BANNED_TERMS:
            if term in title:
                issues.append({"severity": "major", "issue": f"Unsupported risky term in {item['id']}: {term}", "path": ""})
        if item["type"] in NEUTRAL_TYPES:
            for name in protected:
                if name and name in title:
                    issues.append({"severity": "major", "issue": f"Neutral title {item['id']} contains brand: {name}", "path": ""})
    return {"skill_id": "yao-geo-title-optimizer", "checked_at": dt.datetime.now().isoformat(timespec="seconds"), "files": {k: {"path": str(p), "exists": p.exists(), "size": p.stat().st_size if p.exists() else 0} for k, p in paths.items()}, "report_depth_checks": depth, "docx_layout_checks": docx, "pdf_checks": pdf, "issues": issues, "passed": not any(x["severity"] in {"blocker", "major"} for x in issues)}


def main() -> None:
    args = parse_args()
    data = load_input(Path(args.input))
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = data["output_stem"]
    md = out / f"{stem}.md"
    html_path = out / f"{stem}.html"
    docx = out / f"{stem}.docx"
    pdf = out / f"{stem}.pdf"
    qpath = out / "quality-report.json"
    md_text = render_markdown(data)
    html_text = render_html(data)
    md.write_text(md_text, encoding="utf-8")
    html_path.write_text(html_text, encoding="utf-8")
    write_docx(data, docx)
    write_pdf(html_text, pdf, out)
    quality = review(data, {"markdown": md, "html": html_path, "docx": docx, "pdf": pdf}, html_text)
    qpath.write_text(json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rendered Markdown: {md}")
    print(f"Rendered HTML: {html_path}")
    print(f"Rendered DOCX: {docx}")
    print(f"Rendered PDF: {pdf}")
    print(f"Quality report: {qpath}")


if __name__ == "__main__":
    main()
