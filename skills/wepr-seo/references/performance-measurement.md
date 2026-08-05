# Performance, Measurement, Incidents, And Experiments

## Core Web Vitals

Use field data for user-experience classification and lab data for diagnosis.

Current web.dev thresholds reviewed 2026-08-03:

| Metric | Good | Poor | Evaluation |
|---|---:|---:|---|
| LCP | ≤ 2.5 s | > 4.0 s | 75th percentile |
| INP | ≤ 200 ms | > 500 ms | 75th percentile |
| CLS | ≤ 0.1 | > 0.25 | 75th percentile |

Reopen the official source before using these thresholds in a long-lived standard. CrUX/Search Console field groups, page-level RUM, PageSpeed Insights, Lighthouse, and local profiles may cover different URLs, populations, time ranges, devices, and environments.

Do not say a Lighthouse score proves field Core Web Vitals, ranking improvement, or business impact. Diagnose the actual LCP element, interaction, layout shift, network, main-thread, cache, image, font, third-party, or server cause.

## Search Console data discipline

Record property type, search type, dimensions, filters, country, device, search appearance, time zone, date range, and whether data is final or fresh.

Known interpretation limits include:

- anonymized queries may be absent from tables while contributing to totals
- adding page/query dimensions can drop data
- Search Analytics returns top rows under internal limits, not a guaranteed exhaustive query inventory
- API pagination and daily row limits must be respected
- page and property aggregation can calculate metrics differently
- Web, image, video, news, Discover, and generative-AI views are not interchangeable
- average position is an aggregate diagnostic, not a fixed rank

Never subtract filtered query tables and present the remainder as a complete hidden-keyword set.

## Incident diagnosis

Start with symptom shape:

- clicks down, impressions stable: investigate CTR, result presentation, intent/SERP shifts, brand demand, and device/market mix
- impressions and clicks down, positions stable: investigate demand, seasonality, query mix, and tracking scope
- positions and impressions down: investigate affected templates/queries, content/competition, technical changes, policies, and updates
- indexed pages or crawl signals change: inspect robots, noindex, canonicals, redirects, rendering, outages, security, migrations, and sitemap/feed changes
- analytics down but Search Console stable: inspect analytics, consent, attribution, landing-page behavior, and conversion instrumentation

Compare like-for-like periods, include seasonality, segment before averaging, and preserve release/change timelines. Keep multiple hypotheses until evidence eliminates them.

## SEO experiment design

For changes that are reversible and repeated across comparable pages:

1. state one falsifiable hypothesis and expected mechanism
2. choose a treatment unit that limits cross-contamination, often page or template groups
3. define eligible population, exclusions, assignment, and baseline window before looking at outcomes
4. choose primary outcome, guardrails, minimum practical effect, observation window, and stopping rule
5. avoid changing templates, internal links, content, and tracking simultaneously unless the package is intentionally tested as one treatment
6. monitor implementation parity, crawl/reindex progress, seasonality, and external events
7. report positive, negative, null, and inconclusive outcomes; do not convert noise into a win

Time-series before/after comparisons without a credible control remain observational. For unique migrations or incidents where controlled tests are impossible, use change-point evidence and competing explanations with appropriately lower confidence.

Source anchors: web.dev Core Web Vitals, Google traffic-drop guidance, A/B testing guidance, and Search Console API documentation in `data/seo-source-registry.json`.
