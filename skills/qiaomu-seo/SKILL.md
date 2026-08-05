---
name: qiaomu-seo
description: Audit, diagnose, research, plan, implement, experiment on, and verify website SEO across Google, Bing, and AI-search surfaces. Use for technical SEO, crawling, rendering and indexing, JavaScript SEO, robots.txt, sitemaps, canonicals, redirects, status codes, metadata, internal linking, structured data, Core Web Vitals, keyword and intent research, content quality or pruning, SEO experiment design, traffic drops, migrations, international SEO and hreflang, ecommerce and product SEO, image or video search, large-site and programmatic SEO, IndexNow, Search Console or Webmaster Tools analysis, and AI Overviews, AI Mode, ChatGPT Search, Copilot, or Perplexity visibility. Use with URLs, website code, rendered pages, server logs, crawl files, first-party exports, and keyword datasets. Exclude paid-search campaign management, app-store optimization, generic LLM prompt optimization, ranking or citation guarantees, link spam, and unsupported metrics or causal claims.
---

# Qiaomu SEO

Improve discoverability and qualified organic outcomes with current sources, explicit coverage, and reproducible evidence.

## Router Rules

- Use for organic website search work: audit, strategy, research, implementation, migration, monitoring, and experimentation.
- Route paid media and bidding to advertising workflows; route app-store listings to ASO; route pure conversion optimization elsewhere unless organic acquisition is also in scope.
- Treat Google, Bing, AI search, image, video, shopping, local, and news as distinct surfaces. Never generalize a feature, crawler, report, or policy across providers.
- Read only the task-relevant modules:
  - core audit and prioritization: [Audit Playbook](references/audit-playbook.md)
  - crawling, indexing, JavaScript, canonicals, migrations, large sites: [Technical SEO](references/technical-seo.md)
  - keywords, intent, page maps: [Keyword And Content](references/keyword-content.md)
  - content quality, pruning, programmatic pages: [Content Quality](references/content-quality.md)
  - performance, Search Console, incidents, experiments: [Performance And Measurement](references/performance-measurement.md)
  - international and ecommerce: [International And Commerce](references/international-commerce.md)
  - images and video: [Vertical Search](references/vertical-search.md)
  - Google, Bing, IndexNow, OpenAI, Perplexity: [Engine Matrix](references/engine-matrix.md)
  - generative search: [AI Search](references/ai-search.md)
  - mutable-claim review: [Knowledge Freshness](references/knowledge-freshness.md)
  - evidence semantics or JSON output: [Evidence Policy](references/evidence-policy.md) and [Audit Contract](references/audit-contract.md)

## Action Boundary

- `audit / diagnose / compare / advise`: inspect and report; do not edit code, content, webmaster settings, feeds, DNS, or production.
- `optimize / fix / implement`: change only files or systems the user placed in scope; capture before evidence and verify afterward.
- Never submit URLs, change index controls, publish, delete pages, disavow links, alter Merchant Center or Business Profile, buy data, or contact third parties without explicit authorization.

## Work Modes

- `advisory`: no target evidence; give a plan without site-specific claims.
- `page`: inspect one or a small named URL set deeply.
- `template sample`: inspect representative templates and disclose selection; never call it a full-site audit.
- `site inventory`: use crawl, sitemap, route, log, or first-party inventories to measure breadth.
- `incident`: diagnose a traffic/indexing loss using segmented timelines and competing hypotheses.
- `migration`: protect URL mappings, redirects, canonicals, hreflang, sitemaps, feeds, monitoring, and rollback.
- `experiment`: define hypothesis, treatment unit, comparison, guardrails, observation window, and decision rule.
- `specialty`: evaluate international, ecommerce, image, video, local, news, or AI-search requirements only when relevant.

## Compact Workflow

1. Define outcome, conversion, audience, market/language, search surface, engine/provider, target pages, time window, and authorized action.
2. Choose work mode and evidence modes: `live`, `code`, `rendered`, `data`, `logs`, or `advisory`.
3. Establish the target inventory and coverage ledger: discovered, selected, fetched, rendered, data-backed, failed, excluded, and not checked.
4. Classify required knowledge before using it:
   - `stable principle`: durable mechanism such as crawl → render → index.
   - `current platform rule`: provider documentation that must carry source and review date.
   - `observed market state`: dated SERP, crawler, feature, or competitor observation.
   - `hypothesis`: testable explanation, not a finding.
5. For current platform rules, consult `data/seo-source-registry.json`. Re-open volatile or overdue official sources; record conflicting documentation instead of silently choosing one.
6. Evaluate in dependency order: access → discovery → fetch/render → index eligibility → canonical/alternate signals → technical delivery → page meaning → usefulness/intent → architecture → specialty surfaces → measurement.
7. Record each finding as `observed`, `inferred`, or `missing evidence`; separate impact from confidence and cite the artifact that supports it.
8. Prioritize by qualified business impact, user/search impact, confidence, effort, dependencies, reversibility, and measurement lag. Avoid universal SEO scores.
9. If implementation is authorized, capture a before snapshot, make the smallest safe change, run repository and runtime checks, and preserve rollback information.
10. Separate `implemented`, `deployed and observable`, `processed by the search platform`, and `outcome observed`. Preserve rerun inputs and a dated monitoring plan.

## Non-Negotiable Evidence Rules

- Never invent search volume, difficulty, traffic, rankings, backlinks, conversion, competitor, crawl, or index metrics. Use `unknown` when evidence is absent.
- Never guarantee crawling, indexing, ranking, rich results, AI citations, traffic, or revenue.
- Do not turn title length, description length, H1 count, word count, keyword density, reading level, link count, or keyword position into universal ranking pass/fail rules.
- Keep controls distinct: robots.txt governs crawler access; robots meta/X-Robots-Tag governs supported index/presentation behavior; canonical is a preference signal; sitemap and IndexNow are discovery/change notifications. None guarantees indexing.
- Keep validators distinct: valid Schema.org syntax does not prove eligibility for a Google search feature; feature eligibility does not guarantee appearance.
- Keep performance evidence distinct: lab tools diagnose a controlled run; field Core Web Vitals describe real-user distributions. Do not substitute one for the other.
- Keep data scope visible: Search Console tables/APIs may omit anonymized queries or lower-volume rows; aggregates, filtered tables, page/query dimensions, and search types are not interchangeable.
- Static HTML and rendered DOM are separate artifacts. A crawler that renders JavaScript does not prove every engine, AI bot, or user-triggered agent does so identically.
- Do not attribute a traffic change to an algorithm update, migration, content change, or technical issue from timing alone.
- Reject cloaking, doorway pages, scaled low-value content, expired-domain abuse, fake reviews/mentions, link spam, hidden content, and destructive bulk pruning without page-level evidence.

## Current AI-Search Boundary

- For Google generative Search, foundational SEO remains the base; Google documents no special AI schema, required AI text file, ideal AI chunk size, or need to rewrite content for AI.
- As of 2026-08-03, Google's newer generative-AI guide documents a dedicated Search Console Generative AI performance report while AI-feature activity also contributes to Search performance. Verify property availability and current documentation before describing reporting.
- For OpenAI, distinguish `OAI-SearchBot` (Search), `GPTBot` (potential model training), and user-triggered `ChatGPT-User`; their controls are not interchangeable.
- Observe Perplexity, Microsoft, and other providers independently. One prompt, citation, crawler log, or referral is a sample—not a stable ranking report.

## Gate Ladder

- `Advisory`: scope, official sources, unknowns, and prioritized plan; no site-specific diagnosis.
- `Audit`: coverage ledger, cited artifacts, engine/surface scope, finding-level evidence, actions, rerun inputs, and limitations.
- `Implementation`: audit gates plus before evidence, changes, tests, runtime/rendered checks, rollback, and monitoring.
- `Migration / destructive change`: complete mapping or decision inventory, comparison/rollback boundary, staged launch, and post-launch platform evidence.
- `Experiment`: registered hypothesis, treatment unit, comparison, guardrails, minimum observation rule, and inconclusive outcome option.

## Output Contract

Unless the user requests another format, provide:

1. executive summary with the top three priorities
2. outcome, scope, search surface, engine/provider, work mode, and evidence mode
3. coverage ledger and source-freshness note
4. findings: category, issue, status, evidence level/reference, impact, confidence, fix, effort, dependency, and verification
5. quick wins, strategic work, experiments, and destructive actions separated
6. keyword/page map, content brief, URL mapping, or specialty checklist only when relevant
7. implementation record and four-stage outcome status when changes were made
8. rerun inputs, monitoring window, decision rule, and rollback boundary
9. missing evidence, conflicting sources, limitations, and next measurement step

For machine-readable audits, follow [Audit Contract](references/audit-contract.md) and validate with:

```bash
python3 scripts/validate_audit.py path/to/audit.json
```

Before relying on mutable SEO knowledge or publishing an upgrade, validate the source registry:

```bash
python3 scripts/validate_knowledge.py .
```

## WEPR Delivery Defaults

- Write concise Chinese unless the user requests another language.
- Explain user and business consequences before specialist terminology.
- Preserve URLs, dates, markets, devices, tools, versions, and evidence gaps for mutable claims.
