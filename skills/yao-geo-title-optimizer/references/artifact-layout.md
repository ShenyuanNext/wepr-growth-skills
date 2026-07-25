<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-title-optimizer
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Artifact Layout Reference

The report style follows the white-background Kami-style document standard:

- restrained white background
- clear hierarchy
- aligned table borders
- fixed table widths
- no text or table overflow
- comfortable line height
- repeatable report sections across Markdown, HTML, Word, and PDF

## Word

Word reports must use fixed A4 dimensions and fixed-width tables. Do not render the title candidate library as a nine-column table in Word. Use per-title cards or key-value blocks so titles, reasons, platform fit, and rewrite advice can wrap naturally.

The renderer must inspect the generated DOCX:

1. Read `word/document.xml`.
2. Find page width and left/right margins.
3. Compute usable width.
4. Sum each table grid width.
5. Fail quality review if any table is wider than the usable width.

## HTML And PDF

HTML and PDF can use analytical tables, but every table must be fixed-layout and wrap long text. Print CSS must define A4 page margins, table header behavior, and smaller table typography.

Long URLs, product names, and mixed Chinese-English strings should have break opportunities before PDF rendering.

HTML reports must include a sticky navigation bar with anchors for overview, method, scenario, evidence, depth analysis, title library, scorecard, structure mapping, and self-review. The nav must be hidden in print output and must not obscure anchor targets; section blocks should use `scroll-margin-top`.

Systematic reports should include depth modules before the title library so reviewers can inspect the analysis foundation before reading recommendations:

- real-data source audit
- domestic AI platform sampling plan
- authoritative reference framework
- system analysis dimensions
- entity and intent matrix
- title pattern library
- coverage gaps and completion plan
- publication checklist
