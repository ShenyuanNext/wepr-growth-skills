---
name: yao-geo-title-optimizer
description: Use when Chinese content teams need GEO title candidates, scoring, compliance review, or title-to-article mapping for articles, pages, FAQs, comparisons, and topic hubs.
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-title-optimizer
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# yao-geo-title-optimizer

Use this skill when the user needs GEO title generation, title optimization, title scoring, title compliance checks, or title-to-article-structure mapping for Chinese content production.

Do not use this skill for plain copyediting, finished article proofreading, brand slogan creation, or generic SEO metadata when the user does not need a GEO title system.

## Inputs

- Core keyword, question set, brand, competitors, target article type, region, and project date.
- Whether year or month anchors are allowed.
- Brand knowledge, competitor knowledge, industry dimensions, evidence sources, and compliance banned terms.
- Target domestic AI platforms, especially DeepSeek, Kimi, Doubao, Yuanbao, and Tongyi Qianwen.
- Optional real-data inputs: public URLs, local customer documents, exported platform answers, CMS fields, and evidence snapshots produced by `scripts/collect_yao_geo_title_evidence.py`.

## GEO Title Logic

1. Parse the main entity, user intent, scenario limit, and decision goal.
2. Select title structures from list, comparison, decision, recommendation, how-to, brand validation, FAQ, and topic-hub types.
3. Build a systematic analysis layer before writing titles: authoritative references, analysis dimensions, entity-intent matrix, evidence freshness, platform interpretation assumptions, and coverage gaps.
4. Run real-data readiness checks: public URL reachability, evidence source freshness, unavailable private data, and platform sampling gaps.
5. Generate varied title candidates that cover decision words, scenario hooks, evaluation dimensions, question wording, and risk-avoidance wording.
6. Apply brand isolation. Neutral list, comparison, horizontal review, recommendation, and procurement titles must not contain the target brand or competitor names unless the user explicitly asks for branded comparison.
7. Apply compliance filtering. Do not use unsupported absolute claims or unsupported recency claims such as "best", "latest", "first", "only", "authoritative", "industry standard", "guaranteed inclusion", or equivalent Chinese terms.
8. Score titles on intent match, entity clarity, differentiation, citation potential, compliance, and freshness.
9. Map each title to an article structure, evidence blocks, FAQ prompts, platform sampling plan, and publication checks.

Reference framework: [Systematic Reporting Framework](references/systematic-reporting-framework.md).

## Domestic Platform Adaptation

- Yuanbao and Doubao: prefer natural Chinese questions and concrete user scenarios.
- Tongyi Qianwen and Kimi: prefer clear dimensions, evidence/source orientation, and long-form structure.
- DeepSeek: prefer logical decision titles with explicit judgment chains.
- Domestic platforms often treat the title, summary, and first paragraph as the primary understanding entry, so titles should expose the main entity, intent, scene, comparison dimension, and supported time anchor.

## Time Anchor Rules

- Year and month anchors require support from the project date or evidence freshness.
- Do not create false recency. If evidence is not fresh enough, move the date into the evidence table instead of the title.
- Avoid batch-level title templates that only swap keywords.

## Four-Format Output

Always produce the report quartet:

- Markdown: complete reviewable source.
- HTML: white background, fixed table layout, explicit print styles, no viewport overflow.
- Word DOCX: fixed A4 page size, fixed table widths, no right overflow, and no nine-column title candidate tables.
- PDF: rendered from the HTML print layout, with page margins, repeatable table headers, and breakable long text.

## Renderer Contract

The renderer expects a completed report JSON, not a raw keyword brief. Build the report JSON from the user's brief before running `scripts/render_yao_geo_title_optimizer.py`.

Required report fields:

- `output_stem`, `report_title`, `generated_at`, `project`
- `title_candidates`, `compliance_checks`, `structure_map`, `self_review`
- `data_source_audit`, `platform_sampling_plan`, `reference_frameworks`, `analysis_dimensions`, `entity_intent_matrix`, `coverage_gaps`, `publication_checklist`

Required project fields:

- `name`, `module`, `priority`, `project_date`, `region`, `audience`
- `target_platforms`, `article_types`, `allow_year_anchor`, `allow_month_anchor`

Required title fields:

- `id`, `title`, `type`, `intent`, `scenario`, `platform_fit`, `why_it_works`, `rewrite_advice`, `scores`
- `scores.intent_match`, `scores.entity_clarity`, `scores.differentiation`, `scores.citation_potential`, `scores.compliance`, `scores.freshness`

Recommended depth fields:

- `title_pattern_library`
- `evidence_sources`
- `evidence_snapshot_path`
- `platform_adaptation`
- `scenario_selection`

### Real Data Collection

The skill can work with real data when the operator supplies public URLs, local files, or platform exports. For public URLs, run:

```bash
python3 scripts/collect_yao_geo_title_evidence.py --input examples/<case>/report_input.json --output examples/<case>/evidence_snapshot.json
```

This produces a lightweight evidence snapshot with status code, final URL, sampled byte count, SHA-256 sample hash, page title, meta description, H1, and fetch timestamp. It does not bypass authentication, paywalls, robots controls, or platform anti-bot rules.

Domestic AI platform answers are not automatically collected by this script. For DeepSeek, Kimi, Doubao, Yuanbao, and Tongyi Qianwen, use API access or manual exports and record the query, answer, timestamp, account/region, and citation behavior in the report input.

### Word Layout Standard

Word is the strictest artifact. Follow these rules:

- Use A4 portrait with explicit page margins.
- Keep every table grid width below the usable page width.
- Render title candidates as per-title cards or narrow key-value tables instead of wide nine-column tables.
- Insert break opportunities into URLs, long English product names, and long mixed strings.
- Run a DOCX structural check before completion: parse `word/document.xml`, compare `w:tblGrid/w:gridCol` totals against page width minus margins, and fail on any overflow.

### PDF/HTML Layout Standard

- Use `table-layout: fixed`, `overflow-wrap: anywhere`, and `word-break: break-word`.
- HTML reports must include a sticky navigation menu that follows the page while scrolling and links to the major report sections.
- Keep print CSS explicit with A4 margins and smaller table typography.
- Avoid page-width tables with unbreakable URL or product-name cells.
- For wide analytical tables, allow wrapping and avoid row-level page-break rules that create large blank areas.

## Quality Gate

Before returning files, perform self-review and repair:

- Confirm all four report files exist.
- Confirm the DOCX is a valid zip package.
- Confirm the PDF starts with a valid PDF header, can be parsed, and has at least one page.
- Confirm all DOCX tables fit within the usable page width.
- Confirm the report includes depth sections for references, analysis dimensions, entity-intent matrix, coverage gaps, and publication checklist.
- Confirm the report includes data source audit and platform sampling plan.
- Confirm HTML includes sticky navigation and section anchors.
- Confirm neutral titles follow brand isolation.
- Confirm banned or unsupported authority terms are absent.
- Confirm output language is Simplified Chinese when the user asks for domestic AI platform examples.
