#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-execution-roadmap
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Generate four-format GEO execution roadmap reports."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as xml_escape

import markdown
from weasyprint import HTML


REQUIRED_SECTIONS = [
    "执行摘要",
    "诊断承接",
    "真实数据能力与采集计划",
    "分析完整性矩阵",
    "证据成熟度与事实底座",
    "北极星指标",
    "六个项目包",
    "90 天执行路线图",
    "国内平台差异化动作",
    "角色分工与验收指标",
    "资源预算与优先级",
    "监测闭环计划",
    "治理节奏与决策机制",
    "风险预案",
    "来源台账",
    "自检记录",
]

REQUIRED_PACKAGES = ["页面技术", "内容矩阵", "标题体系", "知识库", "外部证据", "监测闭环"]
REQUIRED_PLATFORMS = ["DeepSeek", "豆包", "千问", "Kimi", "元宝"]


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "；".join(clean(item) for item in value if clean(item))
    return str(value).strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers: list[str], rows: list[list[Any]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        output.append("| " + " | ".join(md_cell(item) for item in padded[: len(headers)]) + " |")
    return "\n".join(output)


def rows(items: Any, fields: list[tuple[str, str]]) -> list[list[str]]:
    return [[clean(item.get(key, "")) for key, _ in fields] for item in as_list(items) if isinstance(item, dict)]


def heads(fields: list[tuple[str, str]]) -> list[str]:
    return [label for _, label in fields]


def task_rows(project: dict[str, Any]) -> list[list[str]]:
    result = []
    for task in as_list(project.get("tasks")):
        if not isinstance(task, dict):
            continue
        result.append(
            [
                clean(task.get("task")),
                clean(task.get("steps")),
                clean(task.get("owner")),
                clean(task.get("deliverable")),
                clean(task.get("acceptance")),
                clean(task.get("dependency")),
            ]
        )
    return result


def role_rows(data: dict[str, Any]) -> list[list[str]]:
    result = []
    for project in as_list(data.get("project_packages")):
        if not isinstance(project, dict):
            continue
        for task in as_list(project.get("tasks")):
            if not isinstance(task, dict):
                continue
            result.append(
                [
                    clean(project.get("name")),
                    clean(task.get("owner")),
                    clean(task.get("task")),
                    clean(task.get("deliverable")),
                    clean(task.get("acceptance")),
                ]
            )
    return result


def render_markdown(data: dict[str, Any]) -> str:
    report = data.get("report", {})
    lines = [f"# {clean(report.get('title', 'GEO 综合实施方案'))}", ""]
    lines += [
        table(
            ["字段", "内容"],
            [
                ["测试对象", report.get("company", "")],
                ["官网", report.get("website", "")],
                ["测试场景", report.get("scenario", "")],
                ["目标平台", data.get("target_platforms", REQUIRED_PLATFORMS)],
                ["生成日期", report.get("date", datetime.now().strftime("%Y-%m-%d"))],
                ["输出语言", report.get("language", "中文简体")],
            ],
        ),
        "",
        "## 执行摘要",
    ]
    lines += [f"- {clean(item)}" for item in as_list(data.get("executive_summary"))]
    lines += ["", "## 诊断承接"]
    lines += [
        table(
            ["诊断发现", "实施转译"],
            rows(data.get("diagnosis_bridge", {}).get("items"), [("finding", "诊断发现"), ("translation", "实施转译")]),
        ),
        "",
        "## 真实数据能力与采集计划",
    ]
    data_acquisition = data.get("data_acquisition", {})
    real_data_fields = [
        ("data_need", "数据需求"),
        ("current_status", "当前状态"),
        ("acquisition_method", "获取方式"),
        ("source_requirement", "来源要求"),
        ("freshness_rule", "新鲜度规则"),
        ("owner", "责任角色"),
        ("acceptance", "验收口径"),
    ]
    lines += [
        table(
            ["字段", "内容"],
            [
                ["数据模式", data_acquisition.get("mode", "用户提供诊断数据 + 来源台账")],
                ["真实数据能力边界", data_acquisition.get("can_fetch_real_data", "可使用公开网页、用户授权数据和采样导入；无法绕过平台权限或承诺实时平台引用结果。")],
                ["公开来源策略", data_acquisition.get("public_source_policy", "优先官网、官方文档、投资者关系、监管披露和可追溯第三方来源。")],
                ["平台采样策略", data_acquisition.get("platform_sampling_policy", "国内 AI 平台答案需通过用户授权账号、人工采样或外部采样表导入。")],
                ["最后核验日期", data_acquisition.get("verified_at", report.get("date", datetime.now().strftime("%Y-%m-%d")))],
            ],
        ),
        "",
        table(
            ["数据需求", "状态与获取方式", "来源与新鲜度", "责任与验收"],
            [[r[0], f"{r[1]}\n方式：{r[2]}", f"{r[3]}\n新鲜度：{r[4]}", f"{r[5]}\n验收：{r[6]}"] for r in rows(data.get("real_data_plan"), real_data_fields)],
        ),
        "",
        "## 分析完整性矩阵",
    ]
    analysis_fields = [
        ("dimension", "分析维度"),
        ("current_state", "当前状态"),
        ("gap", "缺口"),
        ("action", "纳入方案的动作"),
        ("acceptance", "验收口径"),
        ("owner", "责任角色"),
    ]
    evidence_fields = [
        ("claim_or_asset", "断言/资产"),
        ("maturity", "成熟度"),
        ("source_status", "来源状态"),
        ("gap", "证据缺口"),
        ("next_action", "下一步动作"),
        ("owner", "责任角色"),
    ]
    lines += [
        table(heads(analysis_fields), rows(data.get("analysis_dimensions"), analysis_fields)),
        "",
        "## 证据成熟度与事实底座",
        table(heads(evidence_fields), rows(data.get("evidence_maturity"), evidence_fields)),
        "",
        "## 北极星指标",
    ]
    metric_fields = [("metric", "指标"), ("baseline", "基线"), ("target_30d", "30 天目标"), ("target_60d", "60 天目标"), ("target_90d", "90 天目标"), ("owner", "负责人")]
    lines += [table(heads(metric_fields), rows(data.get("north_star_metrics"), metric_fields)), "", "## 六个项目包"]

    for project in as_list(data.get("project_packages")):
        if not isinstance(project, dict):
            continue
        lines += [
            "",
            f"### {clean(project.get('name'))}",
            "",
            table(
                ["字段", "内容"],
                [
                    ["目标", project.get("goal", "")],
                    ["输入", project.get("inputs", "")],
                    ["负责人", project.get("owner", "")],
                    ["优先级", project.get("priority", "")],
                    ["资源/预算", project.get("resource_budget", "")],
                    ["交付物", project.get("deliverables", "")],
                    ["验收指标", project.get("acceptance_metrics", "")],
                    ["依赖关系", project.get("dependencies", "")],
                ],
            ),
            "",
            table(["任务", "步骤", "负责人", "交付物", "验收指标", "依赖"], task_rows(project)),
        ]

    roadmap_fields = [("phase", "阶段"), ("objective", "目标"), ("key_actions", "关键动作"), ("deliverables", "交付物"), ("acceptance", "验收口径")]
    platform_fields = [("platform", "平台"), ("focus", "执行重点"), ("question_clusters", "目标问题簇"), ("actions", "具体动作"), ("assets", "资产要求"), ("acceptance", "验收指标"), ("risk", "风险提示")]
    resource_fields = [("item", "资源项"), ("priority", "优先级"), ("resource_level", "资源投入"), ("budget_level", "预算等级"), ("timing", "时间窗口"), ("tradeoff", "取舍说明"), ("owner", "责任角色")]
    monitoring_fields = [("item", "监测项"), ("method", "方法"), ("cadence", "频率"), ("owner", "负责人"), ("acceptance", "验收指标")]
    governance_fields = [("cadence", "治理节奏"), ("participants", "参与角色"), ("decision", "决策事项"), ("inputs", "输入材料"), ("outputs", "输出物"), ("escalation", "升级条件")]
    risk_fields = [("risk", "风险"), ("trigger", "触发信号"), ("mitigation", "预案"), ("owner", "负责人"), ("acceptance", "验收指标")]
    source_fields = [("id", "编号"), ("claim", "支持断言"), ("source", "来源"), ("source_type", "来源类型"), ("evidence_level", "证据等级"), ("last_checked", "核验日期"), ("freshness", "新鲜度"), ("url", "URL")]

    lines += [
        "",
        "## 90 天执行路线图",
        table(heads(roadmap_fields), rows(data.get("roadmap"), roadmap_fields)),
        "",
        "## 国内平台差异化动作",
        table(heads(platform_fields), rows(data.get("platform_actions"), platform_fields)),
        "",
        "## 角色分工与验收指标",
        table(["项目包", "责任角色", "任务", "交付物", "验收指标"], role_rows(data)),
        "",
        "## 资源预算与优先级",
        table(heads(resource_fields), rows(data.get("resource_budget"), resource_fields)),
        "",
        "## 监测闭环计划",
        table(heads(monitoring_fields), rows(data.get("monitoring_plan"), monitoring_fields)),
        "",
        "## 治理节奏与决策机制",
        table(heads(governance_fields), rows(data.get("governance_plan"), governance_fields)),
        "",
        "## 风险预案",
        table(heads(risk_fields), rows(data.get("risk_plan"), risk_fields)),
        "",
        "## 来源台账",
        table(
            ["编号", "支持断言", "来源与类型", "证据与新鲜度", "URL"],
            [[r[0], r[1], f"{r[2]}\n类型：{r[3]}", f"{r[4]}\n核验：{r[5]}\n新鲜度：{r[6]}", r[7]] for r in rows(data.get("source_basis"), source_fields)],
        ),
        "",
        "## 自检记录",
        table(
            ["检查项", "结果"],
            [
                ["四格式文件", "生成后由 quality-report.json 复核"],
                ["真实数据", "公开来源、用户授权数据、平台采样导入、来源新鲜度和待补证缺口均有处理规则"],
                ["分析完整性", "十维分析矩阵覆盖业务目标、问题覆盖、品牌实体、页面技术、内容资产、标题体系、知识库、外部证据、平台适配、监测治理"],
                ["证据成熟度", "核心事实按 A-E 成熟度标注来源状态、缺口和补证动作"],
                ["预算治理", "资源预算、优先级、治理节奏和升级条件进入实施方案"],
                ["平台覆盖", "DeepSeek、豆包、千问、Kimi、元宝均有差异动作"],
                ["项目包覆盖", "页面技术、内容矩阵、标题体系、知识库、外部证据、监测闭环均有任务和验收指标"],
                ["承诺边界", "不承诺平台必定引用，只提升可发现性、可验证性和可抽取性"],
            ],
        ),
        "",
    ]
    return "\n".join(lines)


def section_id(index: int) -> str:
    return f"section-{index}"


def inject_section_ids(body: str) -> str:
    for index, section in enumerate(REQUIRED_SECTIONS, start=1):
        escaped = re.escape(html.escape(section))
        body = re.sub(
            rf'<h2(?:\s+id="[^"]*")?>\s*{escaped}\s*</h2>',
            f'<h2 id="{section_id(index)}">{html.escape(section)}</h2>',
            body,
            count=1,
        )
    return body


def render_sticky_nav() -> str:
    links = "".join(
        f'<a href="#{section_id(index)}">{html.escape(section)}</a>'
        for index, section in enumerate(REQUIRED_SECTIONS, start=1)
    )
    return f'<nav class="report-menu" aria-label="报告章节"><div class="report-menu__inner">{links}</div></nav>'


def render_html(markdown_text: str, title: str) -> str:
    body = inject_section_ids(markdown.markdown(markdown_text, extensions=["tables", "toc"]))
    nav = render_sticky_nav()
    css = """
    :root {
      --paper: #ffffff;
      --ivory: #faf9f5;
      --warm: #f5f4ed;
      --ink: #141413;
      --muted: #5e5d59;
      --stone: #87867f;
      --line: #e8e5da;
      --line-strong: #d1cfc5;
      --soft: #faf9f5;
      --accent: #1B365D;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    html, body { margin: 0; padding: 0; background: #ffffff; color: var(--ink); }
    body {
      font-family: "Inter", -apple-system, BlinkMacSystemFont, "Source Han Sans SC", "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
      font-size: 14px;
      line-height: 1.54;
    }
    .report-menu {
      position: sticky;
      top: 0;
      z-index: 20;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }
    .report-menu__inner {
      max-width: 1120px;
      margin: 0 auto;
      padding: 10px 42px;
      display: flex;
      gap: 8px;
      overflow-x: auto;
      scrollbar-width: thin;
    }
    .report-menu a {
      flex: 0 0 auto;
      color: var(--ink);
      text-decoration: none;
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 4px 9px;
      font-size: 12px;
      line-height: 1.35;
      background: var(--ivory);
    }
    .report-menu a:hover { border-color: var(--accent); color: var(--accent); }
    .page { max-width: 1120px; margin: 0 auto; padding: 44px 42px 68px; background: #ffffff; }
    h1, h2, h3 {
      font-family: "TsangerJinKai02", "Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", Georgia, serif;
      font-weight: 500;
      letter-spacing: 0;
    }
    h1 { margin: 0 0 22px; padding-bottom: 18px; border-bottom: 1.5px solid var(--accent); font-size: 31px; line-height: 1.18; color: var(--ink); }
    h2 { margin: 34px 0 14px; padding-left: 10px; border-left: 4px solid var(--accent); font-size: 21px; line-height: 1.25; color: var(--ink); }
    h3 { margin: 24px 0 10px; font-size: 17px; line-height: 1.3; color: var(--ink); }
    p { margin: 0 0 10px; }
    ul { margin: 8px 0 16px 1.2em; padding: 0; }
    li { margin: 4px 0; }
    table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      margin: 10px 0 22px;
      break-inside: avoid;
      background: #ffffff;
      border: 1px solid var(--line);
    }
    main > table:first-of-type {
      background: var(--ivory);
      border: 1px solid var(--line-strong);
      margin-bottom: 28px;
    }
    th, td {
      border: 1px solid var(--line);
      padding: 7px 9px;
      vertical-align: top;
      word-break: break-word;
      overflow-wrap: anywhere;
      font-size: 13px;
      line-height: 1.45;
    }
    th { background: var(--soft); color: var(--accent); font-weight: 600; text-align: left; }
    td:first-child, th:first-child { color: var(--ink); }
    code { white-space: pre-wrap; word-break: break-word; }
    @page { size: A4; margin: 18mm 16mm; background: #ffffff; }
    @media print {
      .report-menu { display: none; }
      body { font-size: 9.8pt; line-height: 1.5; background: #ffffff; }
      .page { max-width: none; padding: 0; }
      h1 { font-size: 22pt; }
      h2 { font-size: 15pt; margin-top: 22pt; }
      h3 { font-size: 12pt; }
      th, td { padding: 5pt 6pt; font-size: 8.8pt; line-height: 1.38; }
      table { page-break-inside: avoid; }
    }
    """
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{css}</style>
</head>
<body>{nav}<main class="page">{body}</main></body>
</html>
"""


DOCX_PAGE_WIDTH = 11906
DOCX_PAGE_HEIGHT = 16838
DOCX_MARGIN = 1134
DOCX_CONTENT_WIDTH = DOCX_PAGE_WIDTH - (DOCX_MARGIN * 2)


def word_breaks(text: str) -> str:
    value = clean(text)
    for token in ["/", ".", "-", "_", "?", "&", "=", "#", ":"]:
        value = value.replace(token, token + "\u200b")
    return value


def w_text(text: str) -> str:
    lines = word_breaks(text).splitlines() or [""]
    chunks = []
    for index, line in enumerate(lines):
        if index:
            chunks.append("<w:br/>")
        chunks.append(f'<w:t xml:space="preserve">{xml_escape(line)}</w:t>')
    return "".join(chunks)


def w_p(
    text: str,
    style: str | None = None,
    *,
    font_size: int | None = None,
    before: int = 0,
    after: int = 120,
    keep_next: bool = False,
) -> str:
    p_props = []
    if style:
        p_props.append(f'<w:pStyle w:val="{style}"/>')
    if keep_next:
        p_props.append("<w:keepNext/>")
    p_props.append(f'<w:spacing w:before="{before}" w:after="{after}" w:line="300" w:lineRule="auto"/>')
    r_props = []
    if font_size:
        r_props.append(f'<w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/>')
    rpr = f"<w:rPr>{''.join(r_props)}</w:rPr>" if r_props else ""
    return f"<w:p><w:pPr>{''.join(p_props)}</w:pPr><w:r>{rpr}{w_text(text)}</w:r></w:p>"


def normalize_widths(widths: list[int]) -> list[int]:
    if not widths:
        return []
    total = sum(widths)
    scaled = [max(420, round(width * DOCX_CONTENT_WIDTH / total)) for width in widths]
    diff = DOCX_CONTENT_WIDTH - sum(scaled)
    scaled[-1] += diff
    return scaled


def w_table(headers: list[str], body: list[list[str]], widths: list[int] | None = None, *, font_size: int = 17) -> str:
    if widths is None:
        widths = [DOCX_CONTENT_WIDTH // len(headers)] * len(headers)
    widths = normalize_widths(widths)

    def cell(text: str, width: int, header: bool = False) -> str:
        shade = '<w:shd w:fill="FAF9F5"/>' if header else ""
        bold = "<w:b/>" if header else ""
        size = max(font_size, 16)
        return (
            "<w:tc>"
            f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shade}<w:vAlign w:val="center"/></w:tcPr>'
            '<w:p><w:pPr><w:spacing w:before="0" w:after="60" w:line="280" w:lineRule="auto"/></w:pPr>'
            f'<w:r><w:rPr>{bold}<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>{w_text(clean(text))}</w:r>'
            "</w:p></w:tc>"
        )

    rows_xml = ["<w:tr>" + "".join(cell(item, widths[i], True) for i, item in enumerate(headers)) + "</w:tr>"]
    for row in body:
        padded = row + [""] * (len(headers) - len(row))
        rows_xml.append("<w:tr>" + "".join(cell(clean(item), widths[i]) for i, item in enumerate(padded[: len(headers)])) + "</w:tr>")
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{width}"/>' for width in widths) + "</w:tblGrid>"
    borders = (
        f'<w:tblPr><w:tblW w:w="{DOCX_CONTENT_WIDTH}" w:type="dxa"/>'
        '<w:tblLayout w:type="fixed"/>'
        '<w:tblCellMar><w:top w:w="90" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:bottom w:w="90" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:color="E8E5DA"/>'
        '<w:left w:val="single" w:sz="4" w:color="E8E5DA"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="E8E5DA"/>'
        '<w:right w:val="single" w:sz="4" w:color="E8E5DA"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="E8E5DA"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="E8E5DA"/>'
        "</w:tblBorders></w:tblPr>"
    )
    return "<w:tbl>" + borders + grid + "".join(rows_xml) + "</w:tbl>"


def kv_table(items: list[list[Any]], label_width: int = 1850) -> str:
    return w_table(["字段", "内容"], [[clean(a), clean(b)] for a, b in items], [label_width, DOCX_CONTENT_WIDTH - label_width])


def write_docx(data: dict[str, Any], output_path: Path) -> None:
    report = data.get("report", {})
    parts: list[str] = []
    parts.append(w_p(clean(report.get("title", "GEO 综合实施方案")), "Title", after=220, keep_next=True))
    parts.append(
        kv_table(
            [
                ["测试对象", report.get("company", "")],
                ["官网", report.get("website", "")],
                ["测试场景", report.get("scenario", "")],
                ["目标平台", data.get("target_platforms", REQUIRED_PLATFORMS)],
                ["生成日期", report.get("date", datetime.now().strftime("%Y-%m-%d"))],
                ["输出语言", report.get("language", "中文简体")],
            ],
            1650,
        )
    )

    parts.append(w_p("执行摘要", "Heading1", before=260, keep_next=True))
    for index, item in enumerate(as_list(data.get("executive_summary")), start=1):
        parts.append(w_p(f"{index}. {clean(item)}", after=90))

    parts.append(w_p("诊断承接", "Heading1", before=260, keep_next=True))
    parts.append(w_table(["诊断发现", "实施转译"], rows(data.get("diagnosis_bridge", {}).get("items"), [("finding", "诊断发现"), ("translation", "实施转译")]), [4550, 5088]))

    data_acquisition = data.get("data_acquisition", {})
    real_data_fields = [
        ("data_need", "数据需求"),
        ("current_status", "当前状态"),
        ("acquisition_method", "获取方式"),
        ("source_requirement", "来源要求"),
        ("freshness_rule", "新鲜度规则"),
        ("owner", "责任角色"),
        ("acceptance", "验收口径"),
    ]
    parts.append(w_p("真实数据能力与采集计划", "Heading1", before=260, keep_next=True))
    parts.append(
        kv_table(
            [
                ["数据模式", data_acquisition.get("mode", "用户提供诊断数据 + 来源台账")],
                ["真实数据能力边界", data_acquisition.get("can_fetch_real_data", "可使用公开网页、用户授权数据和采样导入；无法绕过平台权限或承诺实时平台引用结果。")],
                ["公开来源策略", data_acquisition.get("public_source_policy", "优先官网、官方文档、投资者关系、监管披露和可追溯第三方来源。")],
                ["平台采样策略", data_acquisition.get("platform_sampling_policy", "国内 AI 平台答案需通过用户授权账号、人工采样或外部采样表导入。")],
                ["最后核验日期", data_acquisition.get("verified_at", report.get("date", datetime.now().strftime("%Y-%m-%d")))],
            ],
            1700,
        )
    )
    real_data_rows = [[r[0], f"{r[1]}\n方式：{r[2]}", f"{r[3]}\n新鲜度：{r[4]}", f"{r[5]}\n验收：{r[6]}"] for r in rows(data.get("real_data_plan"), real_data_fields)]
    parts.append(w_table(["数据需求", "状态与获取方式", "来源与新鲜度", "责任与验收"], real_data_rows, [2100, 2850, 3000, 1688], font_size=16))

    analysis_fields = [
        ("dimension", "分析维度"),
        ("current_state", "当前状态"),
        ("gap", "缺口"),
        ("action", "纳入方案的动作"),
        ("acceptance", "验收口径"),
        ("owner", "责任角色"),
    ]
    evidence_fields = [
        ("claim_or_asset", "断言/资产"),
        ("maturity", "成熟度"),
        ("source_status", "来源状态"),
        ("gap", "证据缺口"),
        ("next_action", "下一步动作"),
        ("owner", "责任角色"),
    ]
    parts.append(w_p("分析完整性矩阵", "Heading1", before=260, keep_next=True))
    analysis_rows = [[r[0], f"{r[1]}\n缺口：{r[2]}", r[3], f"{r[4]}\n责任：{r[5]}"] for r in rows(data.get("analysis_dimensions"), analysis_fields)]
    parts.append(w_table(["分析维度", "状态与缺口", "纳入方案的动作", "验收与责任"], analysis_rows, [1500, 3100, 3100, 1938], font_size=16))

    parts.append(w_p("证据成熟度与事实底座", "Heading1", before=260, keep_next=True))
    evidence_rows = [[r[0], f"{r[1]}\n来源：{r[2]}", f"{r[3]}\n动作：{r[4]}", r[5]] for r in rows(data.get("evidence_maturity"), evidence_fields)]
    parts.append(w_table(["断言/资产", "成熟度与来源", "缺口与动作", "责任角色"], evidence_rows, [2350, 2400, 3500, 1388], font_size=16))

    parts.append(w_p("北极星指标", "Heading1", before=260, keep_next=True))
    for metric in as_list(data.get("north_star_metrics")):
        if not isinstance(metric, dict):
            continue
        parts.append(w_p(clean(metric.get("metric")), "Heading2", before=120, keep_next=True))
        parts.append(
            kv_table(
                [
                    ["基线", metric.get("baseline", "")],
                    ["30 天目标", metric.get("target_30d", "")],
                    ["60 天目标", metric.get("target_60d", "")],
                    ["90 天目标", metric.get("target_90d", "")],
                    ["负责人", metric.get("owner", "")],
                ],
                1700,
            )
        )

    parts.append(w_p("六个项目包", "Heading1", before=260, keep_next=True))
    for project in as_list(data.get("project_packages")):
        if not isinstance(project, dict):
            continue
        parts.append(w_p(clean(project.get("name")), "Heading2", before=160, keep_next=True))
        parts.append(
            kv_table(
                [
                    ["目标", project.get("goal", "")],
                    ["输入", project.get("inputs", "")],
                    ["负责人", project.get("owner", "")],
                    ["优先级", project.get("priority", "")],
                    ["资源/预算", project.get("resource_budget", "")],
                    ["交付物", project.get("deliverables", "")],
                    ["验收指标", project.get("acceptance_metrics", "")],
                    ["依赖关系", project.get("dependencies", "")],
                ],
                1650,
            )
        )
        compact_tasks = []
        for task in as_list(project.get("tasks")):
            if not isinstance(task, dict):
                continue
            task_text = clean(task.get("task"))
            steps = clean(task.get("steps"))
            if steps:
                task_text = f"{task_text}\n步骤：{steps}"
            compact_tasks.append([task_text, clean(task.get("owner")), clean(task.get("deliverable")), clean(task.get("acceptance"))])
        parts.append(w_table(["任务与步骤", "负责人", "交付物", "验收指标"], compact_tasks, [3250, 1600, 2050, 2738], font_size=16))

    roadmap_fields = [("phase", "阶段"), ("objective", "目标"), ("key_actions", "关键动作"), ("deliverables", "交付物"), ("acceptance", "验收口径")]
    parts.append(w_p("90 天执行路线图", "Heading1", before=260, keep_next=True))
    parts.append(w_table(heads(roadmap_fields), rows(data.get("roadmap"), roadmap_fields), [1200, 1800, 2900, 1800, 1938], font_size=16))

    parts.append(w_p("国内平台差异化动作", "Heading1", before=260, keep_next=True))
    for platform in as_list(data.get("platform_actions")):
        if not isinstance(platform, dict):
            continue
        parts.append(w_p(clean(platform.get("platform")), "Heading2", before=120, keep_next=True))
        parts.append(
            kv_table(
                [
                    ["执行重点", platform.get("focus", "")],
                    ["目标问题簇", platform.get("question_clusters", "")],
                    ["具体动作", platform.get("actions", "")],
                    ["资产要求", platform.get("assets", "")],
                    ["验收指标", platform.get("acceptance", "")],
                    ["风险提示", platform.get("risk", "")],
                ],
                1650,
            )
        )

    parts.append(w_p("角色分工与验收指标", "Heading1", before=260, keep_next=True))
    parts.append(w_table(["项目包", "责任角色", "任务", "交付物", "验收指标"], role_rows(data), [1300, 1700, 2200, 2100, 2338], font_size=16))

    resource_fields = [("item", "资源项"), ("priority", "优先级"), ("resource_level", "资源投入"), ("budget_level", "预算等级"), ("timing", "时间窗口"), ("tradeoff", "取舍说明"), ("owner", "责任角色")]
    parts.append(w_p("资源预算与优先级", "Heading1", before=260, keep_next=True))
    resource_rows = [[f"{r[0]}\n优先级：{r[1]}", f"{r[2]}\n预算：{r[3]}", f"{r[4]}\n取舍：{r[5]}", r[6]] for r in rows(data.get("resource_budget"), resource_fields)]
    parts.append(w_table(["资源项与优先级", "投入与预算", "时间窗口与取舍", "责任角色"], resource_rows, [2500, 2450, 3350, 1338], font_size=16))

    monitoring_fields = [("item", "监测项"), ("method", "方法"), ("cadence", "频率"), ("owner", "负责人"), ("acceptance", "验收指标")]
    parts.append(w_p("监测闭环计划", "Heading1", before=260, keep_next=True))
    monitoring_rows = [[r[0], f"{r[1]}\n频率：{r[2]}", r[3], r[4]] for r in rows(data.get("monitoring_plan"), monitoring_fields)]
    parts.append(w_table(["监测项", "方法与频率", "负责人", "验收指标"], monitoring_rows, [1450, 4200, 1450, 2538], font_size=16))

    governance_fields = [("cadence", "治理节奏"), ("participants", "参与角色"), ("decision", "决策事项"), ("inputs", "输入材料"), ("outputs", "输出物"), ("escalation", "升级条件")]
    parts.append(w_p("治理节奏与决策机制", "Heading1", before=260, keep_next=True))
    governance_rows = [[r[0], r[1], f"{r[2]}\n输入：{r[3]}", f"{r[4]}\n升级：{r[5]}"] for r in rows(data.get("governance_plan"), governance_fields)]
    parts.append(w_table(["治理节奏", "参与角色", "决策与输入", "输出与升级"], governance_rows, [1650, 2350, 3350, 2288], font_size=16))

    risk_fields = [("risk", "风险"), ("trigger", "触发信号"), ("mitigation", "预案"), ("owner", "负责人"), ("acceptance", "验收指标")]
    parts.append(w_p("风险预案", "Heading1", before=260, keep_next=True))
    risk_rows = [[f"{r[0]}\n触发：{r[1]}", r[2], r[3], r[4]] for r in rows(data.get("risk_plan"), risk_fields)]
    parts.append(w_table(["风险与触发", "预案", "负责人", "验收指标"], risk_rows, [2500, 3700, 1350, 2088], font_size=16))

    parts.append(w_p("来源台账", "Heading1", before=260, keep_next=True))
    for source in as_list(data.get("source_basis")):
        if not isinstance(source, dict):
            continue
        parts.append(w_p(clean(source.get("id", "来源")), "Heading2", before=120, keep_next=True))
        parts.append(
            kv_table(
                [
                    ["支持断言", source.get("claim", "")],
                    ["来源", source.get("source", "")],
                    ["来源类型", source.get("source_type", "")],
                    ["证据等级", source.get("evidence_level", "")],
                    ["核验日期", source.get("last_checked", "")],
                    ["新鲜度", source.get("freshness", "")],
                    ["URL", source.get("url", "")],
                ],
                1650,
            )
        )

    parts.append(w_p("自检记录", "Heading1", before=260, keep_next=True))
    parts.append(
        kv_table(
            [
                ["四格式文件", "生成后由 quality-report.json 复核"],
                ["真实数据", "公开来源、用户授权数据、平台采样导入、来源新鲜度和待补证缺口均有处理规则"],
                ["分析完整性", "十维分析矩阵覆盖业务目标、问题覆盖、品牌实体、页面技术、内容资产、标题体系、知识库、外部证据、平台适配、监测治理"],
                ["证据成熟度", "核心事实按 A-E 成熟度标注来源状态、缺口和补证动作"],
                ["预算治理", "资源预算、优先级、治理节奏和升级条件进入实施方案"],
                ["平台覆盖", "DeepSeek、豆包、千问、Kimi、元宝均有差异动作"],
                ["项目包覆盖", "页面技术、内容矩阵、标题体系、知识库、外部证据、监测闭环均有任务和验收指标"],
                ["承诺边界", "不承诺平台必定引用，只提升可发现性、可验证性和可抽取性"],
                ["Word 排版", "使用固定页宽、固定列宽、固定表格布局和分组窄表，避免宽表向右溢出"],
            ],
            1650,
        )
    )

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>{''.join(parts)}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/></w:sectPr></w:body>
</w:document>"""
    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="paragraph" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体"/><w:sz w:val="21"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体"/><w:color w:val="1B365D"/><w:sz w:val="36"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体"/><w:color w:val="1B365D"/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体"/><w:color w:val="141413"/><w:sz w:val="24"/></w:rPr></w:style>
</w:styles>"""
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
    word_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/_rels/document.xml.rels", word_rels)
        docx.writestr("word/document.xml", document_xml)
        docx.writestr("word/styles.xml", styles_xml)


def check_docx(path: Path) -> tuple[bool, list[str]]:
    try:
        with zipfile.ZipFile(path, "r") as docx:
            text = docx.read("word/document.xml").decode("utf-8")
    except Exception as exc:
        return False, [str(exc)]
    missing = [section for section in REQUIRED_SECTIONS if section not in text]
    return not missing, missing


def check_docx_table_geometry(path: Path) -> tuple[bool, dict[str, Any]]:
    with zipfile.ZipFile(path, "r") as docx:
        text = docx.read("word/document.xml").decode("utf-8")
    tables = re.findall(r"<w:tbl>.*?</w:tbl>", text, flags=re.DOTALL)
    oversized: list[int] = []
    missing_grid: list[int] = []
    for index, table_xml in enumerate(tables, start=1):
        grid_cols = [int(value) for value in re.findall(r'<w:gridCol w:w="(\d+)"', table_xml)]
        if not grid_cols:
            missing_grid.append(index)
            continue
        if sum(grid_cols) > DOCX_CONTENT_WIDTH:
            oversized.append(index)
    detail = {
        "table_count": len(tables),
        "auto_table_width_count": text.count('w:type="auto"'),
        "tbl_grid_count": text.count("<w:tblGrid>"),
        "tc_width_count": text.count("<w:tcW"),
        "content_width_dxa": DOCX_CONTENT_WIDTH,
        "missing_grid_tables": missing_grid,
        "oversized_tables": oversized,
    }
    passed = bool(tables) and detail["auto_table_width_count"] == 0 and not missing_grid and not oversized
    return passed, detail


def review(data: dict[str, Any], paths: dict[str, Path], md: str, html_text: str) -> dict[str, Any]:
    checks = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append({"name": name, "pass": bool(passed), "detail": detail})

    add(
        "four_format_files_exist",
        all(paths[key].exists() and paths[key].stat().st_size > 1024 for key in ["markdown", "html", "docx", "pdf"]),
        {key: {"exists": paths[key].exists(), "size": paths[key].stat().st_size if paths[key].exists() else 0} for key in ["markdown", "html", "docx", "pdf"]},
    )
    add("markdown_required_sections", all(f"## {section}" in md for section in REQUIRED_SECTIONS), REQUIRED_SECTIONS)
    package_names = [clean(item.get("name")) for item in as_list(data.get("project_packages")) if isinstance(item, dict)]
    add("six_project_packages_present", len(package_names) >= 6 and all(name in "".join(package_names) for name in REQUIRED_PACKAGES), package_names)
    platforms = [clean(item.get("platform")) for item in as_list(data.get("platform_actions")) if isinstance(item, dict)]
    add("cn_platforms_present", all(name in platforms for name in REQUIRED_PLATFORMS), platforms)
    rr = role_rows(data)
    add("role_and_acceptance_metrics_present", len(rr) >= 12 and all(row[1] and row[4] for row in rr), {"role_rows": len(rr)})
    lower_html = html_text.lower()
    add("html_no_dark_or_gradient_tokens", "gradient" not in lower_html and "rgba(" not in lower_html and "background: #0" not in lower_html, "white editorial layout")
    add("html_layout_guards", all(token in html_text for token in ["background: #ffffff", "border-collapse: collapse", "table-layout: fixed", "overflow-wrap: anywhere"]), "table and overflow guards")
    add("kami_editorial_layout_present", all(token in html_text for token in ["#1B365D", "#faf9f5", "#e8e5da", "line-height: 1.54", "border-left: 4px solid var(--accent)"]) and "rgba(" not in lower_html, "kami-inspired white editorial layout")
    add("html_sticky_menu_present", 'class="report-menu"' in html_text and "position: sticky" in html_text and html_text.count('href="#section-') >= len(REQUIRED_SECTIONS), "sticky chapter menu with section anchors")
    real_data_plan = [item for item in as_list(data.get("real_data_plan")) if isinstance(item, dict)]
    add("real_data_plan_present", len(real_data_plan) >= 4 and all(item.get("acquisition_method") and item.get("source_requirement") and item.get("freshness_rule") for item in real_data_plan), {"real_data_items": len(real_data_plan)})
    analysis_dimensions = [item for item in as_list(data.get("analysis_dimensions")) if isinstance(item, dict)]
    evidence_maturity = [item for item in as_list(data.get("evidence_maturity")) if isinstance(item, dict)]
    resource_budget = [item for item in as_list(data.get("resource_budget")) if isinstance(item, dict)]
    governance_plan = [item for item in as_list(data.get("governance_plan")) if isinstance(item, dict)]
    add("analysis_completeness_present", len(analysis_dimensions) >= 10 and all(item.get("dimension") and item.get("action") and item.get("acceptance") for item in analysis_dimensions), {"analysis_dimensions": len(analysis_dimensions)})
    add("evidence_maturity_present", len(evidence_maturity) >= 5 and all(item.get("maturity") and item.get("next_action") for item in evidence_maturity), {"evidence_items": len(evidence_maturity)})
    add("resource_budget_present", len(resource_budget) >= 4 and all(item.get("priority") and item.get("timing") for item in resource_budget), {"resource_items": len(resource_budget)})
    add("governance_plan_present", len(governance_plan) >= 3 and all(item.get("decision") and item.get("escalation") for item in governance_plan), {"governance_items": len(governance_plan)})
    source_basis = [item for item in as_list(data.get("source_basis")) if isinstance(item, dict)]
    add("source_freshness_present", bool(source_basis) and all(item.get("source_type") and item.get("evidence_level") and item.get("last_checked") and item.get("freshness") for item in source_basis), {"source_items": len(source_basis)})
    docx_ok, docx_missing = check_docx(paths["docx"])
    add("docx_valid_and_contains_sections", docx_ok, {"missing": docx_missing})
    geometry_ok, geometry_detail = check_docx_table_geometry(paths["docx"])
    add("docx_fixed_table_geometry", geometry_ok, geometry_detail)
    pdf_header = b""
    if paths["pdf"].exists():
        pdf_header = paths["pdf"].read_bytes()[:4]
    add("pdf_valid", pdf_header == b"%PDF" and paths["pdf"].stat().st_size > 10000, {"header": pdf_header.decode("latin1"), "size": paths["pdf"].stat().st_size if paths["pdf"].exists() else 0})
    add("no_platform_citation_guarantee", "不承诺平台必定引用" in md, "explicit guarantee boundary present")
    return {"overall_pass": all(item["pass"] for item in checks), "generated_at": datetime.now().isoformat(timespec="seconds"), "checks": checks}


def render(input_path: Path, output_dir: Path) -> dict[str, Any]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    basename = data.get("report", {}).get("output_basename", input_path.stem)
    title = data.get("report", {}).get("title", "GEO 综合实施方案")
    paths = {
        "markdown": output_dir / f"{basename}.md",
        "html": output_dir / f"{basename}.html",
        "docx": output_dir / f"{basename}.docx",
        "pdf": output_dir / f"{basename}.pdf",
        "quality": output_dir / "quality-report.json",
    }
    md = render_markdown(data)
    html_text = render_html(md, title)
    paths["markdown"].write_text(md, encoding="utf-8")
    paths["html"].write_text(html_text, encoding="utf-8")
    write_docx(data, paths["docx"])
    HTML(string=html_text, base_url=str(output_dir)).write_pdf(str(paths["pdf"]))
    quality = review(data, paths, md, html_text)
    quality["files"] = {key: str(path) for key, path in paths.items()}
    paths["quality"].write_text(json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8")
    return quality


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()
    quality = render(args.input, args.output_dir)
    print(json.dumps(quality, ensure_ascii=False, indent=2))
    return 0 if quality.get("overall_pass") or args.no_fail else 1


if __name__ == "__main__":
    sys.exit(main())
