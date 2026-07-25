#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-ranking-article-builder
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

import markdown
from bs4 import BeautifulSoup
from weasyprint import HTML


CSS = """
:root {
  color-scheme: light;
  --paper: #fff;
  --ivory: #faf9f5;
  --warm-sand: #e8e6dc;
  --near-black: #141413;
  --dark-warm: #3d3d3a;
  --charcoal: #4d4c48;
  --olive: #5e5d59;
  --stone: #87867f;
  --brand: #1B365D;
  --brand-soft: #EEF2F7;
  --border: #e8e6dc;
  --border-soft: #e5e3d8;
  --ring: #d1cfc5;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; background: #fff; }
html, body { margin: 0; padding: 0; background: #fff; color: var(--near-black); }
body {
  font-family: "Inter", "Source Han Sans SC", "Noto Sans CJK SC",
    -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
  font-size: 15px;
  line-height: 1.55;
}
.report {
  max-width: 1020px;
  margin: 0 auto;
  padding: 36px 34px 68px;
  background: #fff;
}
.report-nav {
  position: sticky;
  top: 0;
  z-index: 20;
  margin: -36px -34px 30px;
  padding: 10px 34px;
  background: #fff;
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 0 var(--border-soft);
}
.report-nav__inner {
  display: flex;
  gap: 7px;
  overflow-x: auto;
  white-space: nowrap;
  scrollbar-width: thin;
}
.report-nav a {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 3px 9px;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--ivory);
  color: var(--brand);
  font-size: 12px;
  font-weight: 500;
  line-height: 1.35;
  letter-spacing: .1px;
  text-decoration: none;
}
.report-nav a:hover { background: var(--brand-soft); border-color: var(--ring); }
h1, h2, h3 {
  font-family: "TsangerJinKai02", "Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", Georgia, serif;
  font-weight: 500;
  color: var(--near-black);
  letter-spacing: 0;
  scroll-margin-top: 70px;
  break-after: avoid;
}
h1 {
  font-size: 30px;
  line-height: 1.18;
  margin: 0 0 18px;
  padding: 0 0 16px;
  border-bottom: 2px solid var(--brand);
}
h2 {
  font-size: 22px;
  line-height: 1.25;
  margin: 34px 0 12px;
  padding-left: 10px;
  border-left: 4px solid var(--brand);
  border-radius: 2px;
}
h3 {
  font-size: 17px;
  line-height: 1.3;
  margin: 24px 0 8px;
  color: var(--dark-warm);
}
p { margin: 0 0 13px; color: var(--near-black); }
ul, ol { margin: 4px 0 15px 1.25em; padding: 0; }
li { margin: 4px 0; }
li::marker { color: var(--brand); }
a { color: var(--brand); text-decoration: none; overflow-wrap: anywhere; }
strong { color: var(--near-black); font-weight: 600; }
.table-wrap {
  width: 100%;
  overflow-x: auto;
  margin: 14px 0 24px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: #fff;
}
table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  background: #fff;
  font-size: 13px;
  line-height: 1.45;
}
th, td {
  border: 0;
  border-bottom: 1px solid var(--border-soft);
  padding: 9px 10px;
  vertical-align: top;
  overflow-wrap: anywhere;
  word-break: break-word;
}
th {
  background: var(--ivory);
  border-bottom: 2px solid var(--brand);
  color: var(--charcoal);
  font-weight: 600;
  text-align: left;
}
tr:last-child td { border-bottom: 0; }
blockquote {
  border-left: 3px solid var(--brand);
  margin: 16px 0;
  padding: 8px 14px;
  background: var(--ivory);
  color: var(--olive);
  border-radius: 3px;
}
code {
  font-family: "JetBrains Mono", "SF Mono", ui-monospace, Consolas, monospace;
  font-size: .92em;
  background: var(--ivory);
  border: 1px solid var(--border-soft);
  padding: 1px 4px;
  border-radius: 3px;
}
@page { size: A4; margin: 20mm 22mm 22mm 22mm; background: #fff; }
@media print {
  html, body { background: #fff; }
  body { font-size: 10pt; line-height: 1.55; }
  .report { max-width: none; padding: 0; background: #fff; }
  .report-nav { display: none; }
  h1 { font-size: 22pt; line-height: 1.2; }
  h2 { font-size: 15pt; line-height: 1.25; margin-top: 24pt; }
  h3 { font-size: 12pt; line-height: 1.3; margin-top: 18pt; }
  table { font-size: 8.8pt; line-height: 1.38; }
  th, td { padding: 5pt 6pt; }
  h2, h3, tr { break-inside: avoid; page-break-inside: avoid; }
}
"""

DOCX_BODY_WIDTH = 9412


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-") or "geo-ranking-article"


def markdown_to_body(markdown_text: str) -> str:
    body = markdown.markdown(markdown_text, extensions=["extra", "tables", "sane_lists"], output_format="html5")
    soup = BeautifulSoup(body, "html.parser")

    for table in soup.find_all("table"):
        wrapper = soup.new_tag("div", **{"class": "table-wrap"})
        table.wrap(wrapper)

    seen: set[str] = set()
    for heading in soup.find_all(["h2", "h3"]):
        base = slugify(heading.get_text(" ", strip=True))
        unique = base
        counter = 2
        while unique in seen:
            unique = f"{base}-{counter}"
            counter += 1
        seen.add(unique)
        heading["id"] = unique

    return str(soup)


def build_nav(body_html: str) -> str:
    soup = BeautifulSoup(body_html, "html.parser")
    items: list[tuple[str, str]] = []
    for heading in soup.find_all(["h2", "h3"]):
        if heading.name == "h3":
            continue
        heading_id = heading.get("id")
        label = heading.get_text(" ", strip=True)
        if heading_id and label:
            items.append((heading_id, label))
    if not items:
        return ""
    links = "".join(f'<a href="#{html.escape(anchor)}">{html.escape(label)}</a>' for anchor, label in items)
    return f'<nav class="report-nav" aria-label="报告目录"><div class="report-nav__inner">{links}</div></nav>'


def build_html(title: str, markdown_text: str) -> str:
    body = markdown_to_body(markdown_text)
    nav = build_nav(body)
    content = f"{nav}\n    {body}" if nav else body
    return f"""<!doctype html>
<html lang="zh-Hans">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="report">
    {content}
  </main>
</body>
</html>
"""


def unescape_xml(value: str) -> str:
    return (
        value.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
        .replace("&amp;", "&")
    )


def escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def add_soft_breaks(value: str) -> str:
    return re.sub(r"([/._?=&%+-])", lambda match: match.group(1) + "\u200b", value)


def add_soft_breaks_to_long_runs(document: str) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = unescape_xml(match.group(1))
        if len(raw) < 16 or not re.search(r"https?://|[A-Za-z0-9][A-Za-z0-9_./?=&%+-]{15,}", raw):
            return match.group(0)
        return "<w:t>" + escape_xml(add_soft_breaks(raw)) + "</w:t>"

    return re.sub(r"<w:t>(.*?)</w:t>", repl, document, flags=re.S)


def text_width_score(value: str) -> float:
    value = re.sub(r"\s+", "", value)
    score = 0.0
    for char in value:
        if "\u4e00" <= char <= "\u9fff":
            score += 1.0
        elif char.isascii() and char.isalnum():
            score += 0.62
        else:
            score += 0.35
    if re.search(r"https?://|[A-Za-z0-9][A-Za-z0-9_./?=&%+-]{18,}", value):
        score *= 1.35
    return score


def extract_cell_text(cell_xml: str) -> str:
    return "".join(unescape_xml(text) for text in re.findall(r"<w:t[^>]*>(.*?)</w:t>", cell_xml, flags=re.S))


def compute_widths(table_xml: str, total_width: int = DOCX_BODY_WIDTH) -> list[int]:
    rows = re.findall(r"<w:tr>.*?</w:tr>", table_xml, flags=re.S)
    first = re.findall(r"<w:tc>.*?</w:tc>", rows[0], flags=re.S) if rows else []
    col_count = len(first)
    if not col_count:
        return []

    scores = [1.0] * col_count
    for row in rows:
        cells = re.findall(r"<w:tc>.*?</w:tc>", row, flags=re.S)
        for index, cell in enumerate(cells[:col_count]):
            scores[index] += min(text_width_score(extract_cell_text(cell)), 80) ** 0.72

    min_width = 760 if col_count >= 5 else 900 if col_count >= 4 else 1100
    available = total_width - min_width * col_count
    if available <= 0:
        return [total_width // col_count] * col_count

    widths = [min_width + int(available * score / sum(scores)) for score in scores]
    diff = total_width - sum(widths)
    index = 0
    while diff:
        step = 1 if diff > 0 else -1
        target = index % len(widths)
        if step > 0 or widths[target] > min_width:
            widths[target] += step
            diff -= step
        index += 1
    return widths


def patch_docx(docx_path: Path) -> None:
    border = (
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="6" w:space="0" w:color="E8E6DC"/>'
        '<w:left w:val="single" w:sz="6" w:space="0" w:color="E8E6DC"/>'
        '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="E8E6DC"/>'
        '<w:right w:val="single" w:sz="6" w:space="0" w:color="E8E6DC"/>'
        '<w:insideH w:val="single" w:sz="6" w:space="0" w:color="E8E6DC"/>'
        '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="E8E6DC"/>'
        '</w:tblBorders>'
    )
    cell_margins = (
        '<w:tblCellMar>'
        '<w:top w:w="80" w:type="dxa"/>'
        '<w:left w:w="80" w:type="dxa"/>'
        '<w:bottom w:w="80" w:type="dxa"/>'
        '<w:right w:w="80" w:type="dxa"/>'
        '</w:tblCellMar>'
    )

    with zipfile.ZipFile(docx_path) as archive:
        entries = {name: archive.read(name) for name in archive.namelist()}
    document = entries["word/document.xml"].decode("utf-8")

    page = '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1247" w:bottom="1247" w:left="1247" w:header="360" w:footer="360" w:gutter="0"/>'
    document = re.sub(
        r"<w:sectPr\b[^>]*>.*?</w:sectPr>",
        lambda match: re.sub(r"<w:pgSz\b[^>]*/>|<w:pgMar\b[^>]*/>", "", match.group(0)).replace(">", ">" + page, 1),
        document,
        flags=re.S,
    )
    document = add_soft_breaks_to_long_runs(document)

    def table_repl(match: re.Match[str]) -> str:
        table = match.group(0)
        widths = compute_widths(table)
        if not widths:
            return table

        grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{width}"/>' for width in widths) + "</w:tblGrid>"
        if "<w:tblGrid>" in table:
            table = re.sub(r"<w:tblGrid>.*?</w:tblGrid>", grid, table, count=1, flags=re.S)
        else:
            table = table.replace("</w:tblPr>", "</w:tblPr>" + grid, 1)

        index = {"value": 0}

        def cell_repl(cell_match: re.Match[str]) -> str:
            width = widths[index["value"] % len(widths)]
            index["value"] += 1
            cell = re.sub(r"<w:tcW\b[^>]*/>", "", cell_match.group(0))
            return cell.replace(
                "<w:tcPr>",
                f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/><w:vAlign w:val="top"/>',
                1,
            )

        table = re.sub(r"<w:tc>.*?</w:tc>", cell_repl, table, flags=re.S)

        def props_repl(props_match: re.Match[str]) -> str:
            props = re.sub(r"<w:tblBorders>.*?</w:tblBorders>|<w:tblCellMar>.*?</w:tblCellMar>", "", props_match.group(1), flags=re.S)
            props = re.sub(r"<w:tblW\b[^>]*/>|<w:tblLayout\b[^>]*/>|<w:jc\b[^>]*/>|<w:tblInd\b[^>]*/>", "", props)
            return (
                '<w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:jc w:val="center"/>'
                '<w:tblLayout w:type="fixed"/>'
                + props
                + border
                + cell_margins
                + "</w:tblPr>"
            )

        return re.sub(r"<w:tblPr>(.*?)</w:tblPr>", props_repl, table, count=1, flags=re.S)

    document = re.sub(r"<w:tbl>.*?</w:tbl>", table_repl, document, flags=re.S)
    entries["word/document.xml"] = document.encode("utf-8")

    tmp_path = docx_path.with_suffix(".tmp.docx")
    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in entries.items():
            archive.writestr(name, data)
    tmp_path.replace(docx_path)


def write_docx(md_path: Path, docx_path: Path) -> None:
    if not shutil.which("pandoc"):
        raise RuntimeError("pandoc is required to create Word output")
    subprocess.run(["pandoc", str(md_path), "-o", str(docx_path), "--standalone"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    patch_docx(docx_path)


def verify_outputs(output_dir: Path, slug: str, html_text: str) -> None:
    for suffix in [".md", ".html", ".pdf", ".docx"]:
        path = output_dir / f"{slug}{suffix}"
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Missing or empty output: {path}")
    for needle in ["position: sticky", "report-nav", "background: #fff", "line-height: 1.55", "border-collapse: collapse", "overflow-wrap: anywhere", "@page { size: A4", "--brand: #1B365D", "font-family: \"TsangerJinKai02\""]:
        if needle not in html_text:
            raise RuntimeError(f"HTML style check failed: {needle}")
    if "rgba(" in html_text:
        raise RuntimeError("HTML style check failed: rgba is not allowed in kami-compatible report CSS")
    with zipfile.ZipFile(output_dir / f"{slug}.docx") as archive:
        document = archive.read("word/document.xml").decode("utf-8")
    for table in re.findall(r"<w:tbl>.*?</w:tbl>", document, flags=re.S):
        widths = [int(width) for width in re.findall(r'<w:gridCol w:w="(\d+)"', table)]
        if not widths or sum(widths) > DOCX_BODY_WIDTH:
            raise RuntimeError("DOCX table width overflow check failed")
        if '<w:tblLayout w:type="fixed"' not in table:
            raise RuntimeError("DOCX fixed layout check failed")
    if document.count("<w:tblBorders>") < document.count("<w:tbl>"):
        raise RuntimeError("DOCX border check failed")


def build_index(output_dir: Path, slug: str, title: str) -> None:
    index_source = f"""# {title} - 文章包

- [Markdown]({slug}.md)
- [HTML]({slug}.html)
- [PDF]({slug}.pdf)
- [Word]({slug}.docx)
"""
    (output_dir / "index.html").write_text(build_html(title + " - 文章包", index_source), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--slug", default="")
    parser.add_argument("--title", default="")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    markdown_text = args.source.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", markdown_text, re.M)
    title = args.title or (title_match.group(1).strip() if title_match else args.source.stem)
    slug = slugify(args.slug or args.source.stem)

    md_path = args.output_dir / f"{slug}.md"
    html_path = args.output_dir / f"{slug}.html"
    pdf_path = args.output_dir / f"{slug}.pdf"
    docx_path = args.output_dir / f"{slug}.docx"

    md_path.write_text(markdown_text, encoding="utf-8")
    html_text = build_html(title, markdown_text)
    html_path.write_text(html_text, encoding="utf-8")
    HTML(string=html_text, base_url=str(args.output_dir)).write_pdf(str(pdf_path))
    write_docx(md_path, docx_path)
    build_index(args.output_dir, slug, title)
    verify_outputs(args.output_dir, slug, html_text)

    for path in [md_path, html_path, pdf_path, docx_path, args.output_dir / "index.html"]:
        print(f"generated: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
