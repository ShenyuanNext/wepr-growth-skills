# Search Engine And Crawler Matrix

Last reviewed: 2026-08-03. Provider behavior is mutable; re-open overdue sources from `data/seo-source-registry.json`.

| Surface | Discovery/control | Evidence | Boundary |
|---|---|---|---|
| Google Search | Googlebot, links, sitemaps, Search Console | URL Inspection, Page Indexing, performance reports, logs | submission/eligibility does not guarantee indexing or serving |
| Bing Search/Copilot grounding | Bingbot, links, sitemaps, Bing Webmaster Tools, IndexNow | Site Explorer, sitemap/index reports, performance, logs | IndexNow `200/202` means received/accepted, not indexed |
| ChatGPT Search | `OAI-SearchBot`; public pages and provider systems | verified bot logs, `utm_source=chatgpt.com` referrals, dated answer observations | `GPTBot` is a separate potential-training control |
| ChatGPT user actions | `ChatGPT-User` | request logs and task reproduction | user-triggered fetches are not automatic Search crawling; robots rules may not apply identically |
| Perplexity Search | `PerplexityBot` and published IP ranges | verified logs, referrals, dated cited answers | search crawler is distinct from provider model-training behavior |
| Schema.org | vocabulary and syntax via Schema Markup Validator | extracted graph and syntax output | not a Google/Bing feature-eligibility guarantee |

## IndexNow

Use for timely change notifications to participating engines when implementation ownership and value justify it.

- Verify host ownership/key placement and submit only URLs belonging to that host.
- Automate additions, updates, and deletions rather than repeatedly submitting unchanged inventories.
- Respect response codes and rate limits; store no secret key in reports or public examples.
- Preserve URL, request date, endpoint, status, and later crawl/index evidence separately.
- Keep XML sitemaps and internal links; IndexNow is not a replacement for full discovery architecture.
- Do not claim Google supports or processes IndexNow unless current Google documentation explicitly says so.

## Bot verification

User-agent strings are spoofable. When crawler identity matters, use the provider's published IP ranges or documented reverse/forward DNS method and inspect server logs. Do not make allow/block recommendations from the user-agent string alone.

## Platform control matrix

Before changing robots rules, create a table with:

- provider and product purpose
- user agent
- automatic crawl vs user-triggered fetch
- desired business policy: search visibility, training use, agent interaction, ads validation
- current directive/WAF/CDN behavior
- verified official source and review date
- expected effect and what remains outside the control

This prevents a blanket `User-agent: *` decision from accidentally coupling search discovery, model training, and user-requested access.
