---
name: qiaomu-seo
description: Complete evidence-led SEO workbench for quick page checks, full HTML audits, site-wide strategy, implementation, experiments, and verification across Google, Bing, and AI-search surfaces. Use for technical SEO, crawling, rendering, indexing, robots.txt, sitemaps, canonicals, redirects, metadata, internal links, structured data, PageSpeed and Core Web Vitals, social metadata, keyword and intent research, content planning or pruning, traffic drops, migrations, international and ecommerce SEO, image/video search, large-site sampling, Search Console analysis, IndexNow, AI Overviews, AI Mode, ChatGPT Search, Copilot, or Perplexity visibility. Use with URLs, code, rendered pages, logs, crawl files, first-party exports, and keyword datasets. Exclude paid-search management, ASO, ranking/citation guarantees, link spam, fabricated metrics, and unsupported causal claims.
---

# WEPR Complete SEO Workbench

Operate one unified SEO workflow from rapid single-page diagnosis through site strategy, implementation, and outcome verification. Use current sources, explicit coverage, reproducible evidence, and client-ready delivery.

## Select the mode

- **Quick page audit:** run the core scripts against one URL; review their JSON; deliver the highest-impact findings and an HTML report.
- **Full page audit:** run core scripts plus PageSpeed and social metadata; add semantic/content review; deliver the full HTML report and five prioritized fixes.
- **Advisory:** provide a plan when target evidence is unavailable; make no site-specific claims.
- **Template sample:** inspect representative URLs by page type and disclose sampling limits.
- **Site inventory:** use crawl, sitemap, route, log, or first-party inventories to measure breadth.
- **Incident:** diagnose traffic, ranking, crawl, or indexing loss using segmented timelines and competing hypotheses.
- **Migration:** protect mappings, redirects, canonicals, hreflang, sitemaps, feeds, monitoring, and rollback.
- **Implementation:** change only files or systems explicitly placed in scope; capture before evidence and verify after.
- **Experiment:** define hypothesis, unit, comparison, guardrails, observation window, and decision rule.
- **Specialty:** evaluate international, ecommerce, image, video, local, news, or AI-search requirements when relevant.

## Load only relevant references

- Audit scope and prioritization: `references/audit-playbook.md`
- Deterministic page-audit fields and report rules: `references/page-audit-checks.md`
- Crawl, render, index, canonical, migration, large sites: `references/technical-seo.md`
- Keywords, intent, page maps, briefs: `references/keyword-content.md`
- Content quality, pruning, programmatic SEO: `references/content-quality.md`
- Performance, Search Console, incidents, experiments: `references/performance-measurement.md`
- International SEO and ecommerce: `references/international-commerce.md`
- Image and video search: `references/vertical-search.md`
- Google, Bing, IndexNow, OpenAI, Perplexity: `references/engine-matrix.md`
- Generative search: `references/ai-search.md`
- Evidence and coverage: `references/evidence-policy.md`, `references/execution-sampling.md`
- Mutable rules: `references/knowledge-freshness.md`, `data/seo-source-registry.json`
- Machine-readable audits: `references/audit-contract.md`, `schemas/seo-audit.schema.json`

## Define scope before checks

Record objective, conversion, audience, market/language, engine and search surface, target pages, time window, authorized action, and available evidence. Select evidence modes from live HTTP, repository/code, rendered DOM, first-party data, logs, current SERP observation, or advisory.

Create a coverage ledger: discovered, selected, fetched, rendered, data-backed, failed, excluded, and not checked. Never call a small sample a full-site audit.

## Run a quick page audit

Use one URL and an explicit or inferred primary keyword:

```bash
python3 scripts/check-site.py https://example.com
python3 scripts/check-page.py https://example.com --keyword "primary keyword"
python3 scripts/fetch-page.py https://example.com --output /tmp/page.html
python3 scripts/check-schema.py --file /tmp/page.html
```

Inspect robots, sitemap, 404 behavior, host/canonical consistency, title, description, H1, slug, links, headings, images, content, and JSON-LD. Resolve every `llm_review_required` field with semantic judgment; do not repeat a script conclusion blindly.

Use the full report template at `assets/report-template.html`, but render only checked modules. Save to `reports/<hostname>-<slug>-audit.html`; never print raw HTML to the terminal.

## Run a full page audit

Run the quick workflow, then:

```bash
python3 scripts/check-social.py --file /tmp/page.html
python3 scripts/check-pagespeed.py https://example.com --strategy mobile --timeout 180 --api-key "USER_PROVIDED_KEY"
```

Ask for a Google PageSpeed Insights API key before the performance step. Never store, echo, or commit it. If none is provided, do not claim a completed full audit; either stop or explicitly downgrade to a quick audit.

Add Open Graph, Twitter Card, Lighthouse categories, lab metrics, field-data availability, E-E-A-T content quality, duplicate-content signals, anchor quality, staging exposure, sitemap inventory, international signals, and client-ready priorities when observable. Keep lab diagnostics distinct from field Core Web Vitals.

Save to `reports/<hostname>-<slug>-full-audit.html` using `assets/report-template.html`.

## Run site strategy or diagnosis

Evaluate in dependency order:

1. access and discovery;
2. fetch and render;
3. index eligibility;
4. canonical and alternate signals;
5. technical delivery and performance;
6. page meaning, intent, and usefulness;
7. architecture and internal discovery;
8. international, commerce, vertical, or AI-search surfaces;
9. measurement, experiments, and verification.

For mutable platform rules, check `data/seo-source-registry.json` and reopen overdue or time-sensitive official sources. Preserve provider, date, market, device, and conflicting documentation.

## Apply evidence rules

Label every material conclusion:

- **observed:** directly present in a response, DOM, code, export, log, or official tool;
- **inferred:** supported by partial evidence with alternatives stated;
- **missing evidence:** required evidence is absent and the resolving input is named.

Separate impact from confidence. Never invent search volume, difficulty, traffic, rankings, backlinks, conversions, competitor metrics, crawl/index state, or AI visibility.

Do not turn character counts, H1 counts, word counts, keyword density, or keyword position into universal ranking pass/fail rules. Do not confuse robots access, index directives, canonical preference, sitemap discovery, IndexNow notification, structured-data validity, feature eligibility, or observed search appearance.

## Build keyword, content, and communication deliverables

Use current first-party and market evidence to cluster by intent and expected page type, not keyword similarity alone. For each approved opportunity provide audience/job, market, intent, cluster and evidence source, page type/URL role, distinctive value, questions, structure, internal links, truthful schema opportunity, conversion, factual reviewer, measurement, and review date.

For client proposals and SEO communication plans, include executive priorities, evidence limits, technical workstreams, keyword/page map, content and distribution plan, 30/60/90-day roadmap, owners, dependencies, budget logic, KPI definitions, verification, and risks. Route finished narrative copy to `$create-marketing-content` when specialist writing is useful.

## Implement safely

Audit and advisory requests do not authorize edits. For explicit implementation, capture a before snapshot, make the smallest safe change, run repository/runtime/rendered checks, and preserve rollback information.

Separate:

1. implemented;
2. deployed and observable;
3. processed by the search platform;
4. outcome observed.

Only the fourth stage supports an outcome claim. Never submit URLs, change index controls, publish, delete pages, disavow links, alter business/search accounts, buy data, or contact third parties without explicit authorization.

## Deliver results

Default output:

1. executive summary with top three priorities;
2. objective, scope, surface/provider, mode, and evidence;
3. coverage and source-freshness note;
4. findings with category, status, evidence/reference, impact, confidence, fix, effort, dependency, and verification;
5. quick wins, strategic work, experiments, and destructive actions separated;
6. relevant page map, brief, URL mapping, or specialty checklist;
7. implementation and four-stage status when changes were made;
8. rerun inputs, monitoring window, decision rule, and rollback boundary;
9. missing evidence, conflicting sources, limitations, and next measurement step.

Validate machine-readable audits with:

```bash
python3 scripts/validate_audit.py path/to/audit.json
```

Validate mutable knowledge with:

```bash
python3 scripts/validate_knowledge.py .
```

## Quality gate

Confirm that coverage supports breadth claims; every important finding has evidence; impact and confidence are separate; script outputs received semantic review; current platform rules are dated and provider-specific; fixes include owner, dependency, and verification; page and content recommendations match user intent; destructive actions have an inventory and rollback path; reports contain no secrets; and no crawl, index, ranking, rich-result, citation, traffic, or revenue outcome is guaranteed.
