---
name: yao-geo-knowledge-base-builder
description: Build evidence-backed GEO brand knowledge bases from official sites, product pages, help centers, white papers, sales materials, media releases, certifications, and trusted third-party sources. Use when asked to generate reusable brand fact cards, FAQ, prohibited expressions, source indexes, prompt input packs, or Word/PDF/HTML/Markdown four-format Chinese GEO knowledge-base deliverables for Kimi, Qianwen, DeepSeek, Doubao, Yuanbao, content production, monitoring, page design, or customer-service preparation.
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-knowledge-base-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# yao-geo-knowledge-base-builder

把官网、产品页、帮助中心、白皮书、品牌资料、销售材料、媒体稿和资质文件，整理成可审计、可复用的 GEO 品牌知识库。

## When To Use

Use this skill when the user needs:

- a systematic GEO brand knowledge-base document with structured summary, base profile, positioning, product/service matrix, metrics, cases, timeline, differentiation, FAQ, query terms, and expression rules
- a complete brand entity inventory covering brand, company, products, services, people/teams, regions, channels, technologies, qualifications, cases, prices, competitors, sources, and pending entities
- a brand fact-card library with evidence, source, update time, confidence, and use cases
- a real-data acquisition and freshness boundary that explains which public, user-provided, authenticated, or unavailable sources were actually usable
- FAQ and prohibited-expression lists for AI answers and content teams
- prompt input packs for rankings, comparisons, explainers, title generation, content rewrite, page design, monitoring, and customer service
- a Chinese simplified four-format package: Markdown, HTML, Word, and PDF

Do not use this skill for one-off brand copywriting without source evidence, pure competitive ranking articles, page technical audits, or relationship-graph-only work.

## Workflow

1. Define the test scenario and target domestic AI platforms: Kimi, Qianwen, DeepSeek, Doubao, and Yuanbao.
2. Run the completeness reference scan in `references/authoritative-reference-framework.md` and `references/analysis-completeness-rubric.md` before writing.
3. Select the data acquisition mode in `references/source-acquisition-and-freshness.md`: public web evidence, user-provided files, authenticated workspace, manual brief, or unavailable source.
4. Collect and verify sources with official-site-first priority: homepage, product pages, pricing/catalog pages, help center, case pages, white papers, investor/news pages, and authoritative third-party sources.
5. Create a source-access ledger. Each source must state access status, publisher, URL or file name, verification date, extraction note, freshness cadence, and whether it can enter strong evidence.
6. Separate evidence tiers:
   - `A`: official current public sources or legally authoritative documents.
   - `B`: reputable third-party reports or public media with clear dates.
   - `C`: brand self-description without enough operational detail.
   - `D`: unverified or market-specific boundary items that must stay in the pending-confirmation area.
7. Extract brand entities: brand, products, services, team, regions, customers, channels, certifications, technologies, cases, prices, and timeline.
8. Build the complete entity inventory. Every entity should include entity ID, type, canonical name, aliases, parent/relationship, evidence source, confidence tier, and usage notes.
9. Build the systematic knowledge-base body before the GEO reuse layer. Follow `references/knowledge-base-architecture.md`.
10. Add a mandatory `真实数据获取与限制` module with acquisition mode, accessible sources, inaccessible sources, freshness risk, and next data-access actions.
11. Add a report-level analysis completeness self-check: reference alignment, module coverage, entity coverage, weak/missing evidence, and repair actions.
12. Build fact cards. Each card must contain subject, attribute or statement, value, evidence, source ID, update time, confidence level, and reusable scenarios.
13. Build reusable content modules: brand intro, core capabilities, product parameters, applicable scenarios, customer/case notes, FAQ, prohibited expressions, and domestic-market boundary notes.
14. Build the prompt input pack for downstream GEO skills. Strong facts and pending facts must stay separated.
15. Produce version number and update mechanism. High-volatility facts such as prices, AI features, product names, customer counts, and compliance boundaries need explicit review cadence.
16. Render Markdown, HTML, Word, and PDF using the fixed-layout renderer in `scripts/render_four_format.py`.
17. Run quality review and repair before handoff.

## Required Outputs

- GEO brand knowledge-base document
- Systematic structured knowledge-base body
- Complete brand entity inventory
- Brand fact-card library
- FAQ and prohibited-expression list
- Content-generation prompt input pack
- Source index with verification date
- Real-data access, freshness, and unavailable-source boundary
- Pending-confirmation list
- Four-format report package: `.md`, `.html`, `.docx`, `.pdf`
- `quality-report.json`

## Layout Rules

Follow `references/four-format-report-layout.md`.

Critical rules:

- White background for HTML, Word, and PDF.
- Use kami-inspired editorial rhythm while preserving the white background: ink-blue `#1B365D`, warm neutral borders, Chinese serif headings, Chinese sans body, compact 1.50-1.55 body line height, and restrained table density.
- A4 geometry for Word/PDF.
- No table wider than the printable page body.
- Word tables must use fixed OpenXML layout, `dxa` table width, and grid widths that sum to the printable body width.
- Fact-card tables default to five columns or fewer.
- Source-index URL tables render as a two-column evidence ledger in HTML/PDF/Word to prevent right overflow.
- Long URLs and long English tokens must be soft-wrapped before DOCX generation.
- No `nowrap` table cells.

## Quality Gates

Before completion, verify:

- all four deliverable files exist and are non-empty
- DOCX has fixed tables, A4 body-width `dxa` table widths, no `w:noWrap`, and no unbreakable segment longer than 80 characters
- PDF is readable, preview-rendered, and checked for right-edge visual overflow
- HTML contains no absolute local `/Users/...` paths
- sources retain date, publisher, URL, and confidence tier
- every report explains real-data access mode, unavailable sources, and freshness cadence
- the report contains the required systematic knowledge-base sections
- the report contains a complete entity inventory section
- the report contains analysis completeness self-check and reference alignment
- HTML contains a sticky menu for screen reading
- unverified domestic-market claims stay in the pending-confirmation area

## Example

The HubSpot Chinese simplified test output is under:

`examples/hubspot-demo/deliverables/`

Use the renderer like this:

```bash
python3 scripts/render_four_format.py \
  --source examples/hubspot-demo/deliverables/hubspot-demo-geo-knowledge-base.md \
  --out-dir examples/hubspot-demo/deliverables \
  --base-name hubspot-demo-geo-knowledge-base \
  --quality-report examples/hubspot-demo/quality-report.json \
  --preview-dir examples/hubspot-demo/previews
```
