---
name: yao-geo-page-audit
description: Diagnose a website page or small page set for GEO readiness with authoritative public evidence, systematic page analysis, code/content/schema fixes, and four-format Chinese report delivery.
metadata:
  owner: Yao Team
  family: geo-page-technical
  maturity: beta
  requires_web: true
  default_outputs: Word, PDF, HTML, Markdown
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-audit
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# yao-geo-page-audit

Use this skill when the user wants a GEO Page Audit, website/page GEO diagnosis, page technical audit, AI extractability audit, schema/HTML module advice, or code/content repair list for a URL.

## Job

Given a target URL or website, diagnose the homepage, a representative first-level page, and a representative second-level page when possible. Output development-ready and content-ready recommendations that improve how public pages can be discovered, parsed, cited, and summarized by search-driven AI systems. By default, analyze public page readiness and public evidence coverage only; do not estimate AI-platform recall, rankings, citation share, or internal platform behavior unless the user provides platform sampling data.

## Workflow

1. Read `references/research-foundation.md`, `references/authority-reference-model.md`, and `references/report-module-taxonomy.md`. Frame the audit as a five-stage chain: discovery, retrieval candidate, main-content extraction, evidence quality, generated citation.
2. Identify page type and sample scope. If the input is a homepage, select homepage, one representative first-level page, and one representative second-level page. State the selection basis and unresolved input gaps.
3. Build an evidence ledger. Prefer official pages, official docs, schema/source code, standards, and peer-reviewed or arXiv research before third-party commentary. Mark each finding as observed, official, standard, research, inferred, or input gap.
4. Check crawlability and renderability: status code, robots, sitemap, canonical, meta robots, mobile-first parity, JavaScript dependency, and whether primary content appears in initial HTML.
5. Check structural quality: H1-H3, `main`/`article`, summary, table of contents, FAQ, tables, lists, breadcrumbs, internal links, anchor text, accessibility headings, and schema.
6. Check content evidence: conclusions first, full entity names, data, citations, cases, dates, author/source, freshness, objectivity, price, service boundaries, regional constraints, and source accountability.
7. Check AI extractability and public-answer material coverage: key-value facts, atomic facts, comparison tables, steps, Q&A, context-independent summary, paragraph independence, entity graph, sameAs links, and chunk-level citation readiness. Convert domestic platform concerns into high-intent question material gaps, not platform recall claims.
8. Produce code-layer fixes, content-layer fixes, page-module suggestions, schema/HTML snippets, priority, owner, acceptance test, risk, and estimated cost.
9. Deliver Word, PDF, sticky-menu HTML, and Markdown from one Markdown content source. Use the `kami` editorial report style in `references/report-formatting-spec.md` and `references/output-layout-policy.md`.
10. After DOCX generation, run `scripts/polish_docx.py` to apply Kami-style Word typography, margins, and table formatting.
11. Run `scripts/review_report_layout.py` and `references/quality-gates.md` before claiming completion.

## Boundaries

- Without crawl/log access, only report front-end observable evidence. Do not infer log-level crawl frequency.
- Without AI-platform sampling data, do not analyze platform recall, ranking, answer frequency, citation share, or platform-internal weighting. Replace that section with public material coverage and high-intent question readiness.
- Distinguish user-visible content, crawler-readable content, and AI-extractable content.
- Schema must match page body facts. Do not use schema to invent facts absent from the page.
- Cite or name the evidence source for important claims. If the source is not available, label the recommendation as a hypothesis or input gap.
- Domestic answer-material adaptation should consider search results, public webpages, news pages, encyclopedia pages, WeChat public articles, documentation, and help-center pages as possible public material. Treat actual platform answer performance as optional user-supplied evidence.

## Outputs

- Page GEO diagnosis report.
- Code-layer repair checklist.
- Content-structure remodeling advice.
- Schema and HTML module suggestions.
- Evidence ledger and report completeness self-check.
- Default four-piece deliverable: Word, PDF, HTML package, Markdown.
- `quality-report.json` with artifact existence, byte size, and layout checks.
