---
name: wepr-geo-suite
description: Route and orchestrate end-to-end WEPR GEO projects across research, AI-search intent mining, panorama audits, knowledge assets, page and content production, platform sampling, monitoring, attribution, execution roadmaps, GEOFlow operations, and client delivery. Use when a GEO request spans multiple workstreams, platforms, quarters, or deliverables, or when the correct specialist skill is unclear.
---

# WEPR GEO Suite

Turn a GEO objective into an evidence-led delivery chain. Route focused requests directly; orchestrate only the skills required for a multi-stage project.

## Start with scope

1. Record the brand, business goal, audience, market, platforms, period, budget, conversion action, available evidence, and required files.
2. Separate public evidence, user-provided evidence, platform samples, assumptions, and unavailable data.
3. Never represent synthetic prompts, inferred competitors, or generated examples as real platform data.
4. Define success with observable indicators. Do not promise ranking, citations, recommendations, leads, or revenue.

Read [references/routing-and-delivery.md](references/routing-and-delivery.md) for the skill map, stage gates, and standard project combinations.

## Route the work

- Baseline and opportunity map: `$yao-geo-panorama-audit`.
- Natural-language query expansion and prompt library: `$yao-geo-intent-miner`.
- Brand facts and reusable evidence: `$yao-geo-knowledge-base-builder`; use `$yao-geo-brand-graph` when entity relationships are central.
- Existing-page diagnosis: `$yao-geo-page-audit`; new page structure: `$yao-geo-page-blueprint`.
- Content: `$yao-geo-title-optimizer`, `$yao-geo-explainer-builder`, `$yao-geo-comparison-builder`, `$yao-geo-ranking-article-builder`, `$yao-geo-content-refiner`, or `$yao-geo-article-friendly` according to format.
- Platform evidence collection: `$yao-deepseek-crawler`, `$yao-doubao-crawler`, or `$yao-chatgpt-crawler`. Respect login, rate, CAPTCHA, privacy, and platform boundaries.
- Monitoring and attribution: `$yao-geo-effect-monitor` for answer/citation signals; `$yao-geo-tracking` for downstream conversion attribution.
- 30/60/90-day implementation: `$yao-geo-execution-roadmap`.
- GEOFlow product development and operations: `$geoflow`. Treat `$yao-geoflow-cli`, `$yao-geoflow-design`, and `$yao-geoflow-template` as compatibility routes.
- Broader WEPR channel strategy, GEO/SEO integration, and commercial growth planning: `$plan-organic-growth`; live GEOrank operations: `$operate-georank-workbench`.
- Browser-openable interactive proposal or report presentation: `$bento-slides`; use the PowerPoint skill when `.pptx` compatibility is required.

## Orchestrate multi-stage projects

Default sequence:

1. Establish evidence and measurement boundaries.
2. Build a baseline and intent universe.
3. Create the fact base and entity model.
4. Prioritize pages and content by business value, evidence readiness, and platform fit.
5. Produce or revise assets with source-bound claims.
6. Sample target platforms under a documented protocol.
7. Track answer quality, citations, conversions, and confounders.
8. Convert findings into a 30/60/90-day roadmap and quarterly review.

Skip stages only when the user already provides an equivalent, current artifact. Preserve handoff fields between skills: entity IDs, source IDs, prompt IDs, page IDs, platform, sample mode, date, confidence, owner, status, and acceptance criteria.

## Delivery contract

For a client-facing project, return:

- executive summary and decision boundaries;
- source ledger and data-access statement;
- intent and platform scope;
- prioritized workstreams, owners, timeline, and dependencies;
- deliverables and acceptance tests;
- measurement baseline, sampling protocol, and attribution limits;
- risks, approvals, and unresolved inputs;
- file links for every generated artifact.

Use one canonical content structure for Markdown, HTML, Word, PDF, slides, and spreadsheets. Verify formulas, links, citations, file validity, layout overflow, and consistency before delivery.

## Quality gates

- Keep brand facts traceable to sources and dates.
- Label fact, inference, estimate, synthetic example, and real sample distinctly.
- Use natural user questions, not mechanical suffix lists.
- Compare competitors on the same dimensions and preserve legitimate strengths.
- Treat platform metrics as repeated-sample estimates, not ground truth.
- Keep platform collection low-frequency, visible, authorized, and auditable.
- Require explicit approval before live publication, destructive operations, bulk synchronization, secret access, or production activation.
- Retain upstream license and attribution notices when redistributing adapted skills.
