# Technical SEO Decision Guide

Use this module for crawling, rendering, indexing, canonicalization, URL changes, and large-site behavior. Recheck provider-specific details in `data/seo-source-registry.json` when the claim is mutable.

## Pipeline diagnosis

Do not collapse these stages:

1. `known`: URL discovered through links, sitemap, feed, submission, or prior crawl
2. `allowed to fetch`: robots and infrastructure permit the named crawler
3. `fetched`: an HTTP response and resources were actually retrieved
4. `rendered`: required JavaScript completed sufficiently for the named renderer
5. `index eligible`: response, robots directives, content, and policies permit indexing
6. `canonical selected`: the platform clustered duplicates and selected a representative URL
7. `served`: the indexed result was selected for a query, market, device, and time

A failure at one stage does not prove all later stages, and a pass does not guarantee the next stage.

## Control semantics

| Mechanism | Primary job | Does not prove |
|---|---|---|
| `robots.txt` | crawler access by user agent | deindexing, canonicalization, ranking |
| robots meta / `X-Robots-Tag` | supported index and presentation directives after fetch | that a blocked crawler can read the directive |
| sitemap | preferred URL discovery and change hints | crawl, index, canonical selection |
| IndexNow | notify participating engines of URL changes | crawl, index, ranking, Google processing |
| canonical | express preferred representative among duplicates | forced selection or redirect |
| redirect | move users and crawlers to another URL | relevance equivalence when destination is unrelated |
| `404` / `410` | state that a resource is unavailable | immediate removal from every index |

Inspect combined signals. Redirect targets, canonical annotations, internal links, hreflang, sitemaps, feeds, and declared preferred hosts should not contradict each other.

## HTTP and URL behavior

- Verify status and headers at every hop; report loops, chains, protocol/host drift, and query loss.
- Prefer server-side permanent redirects for permanent moves. Do not redirect many unrelated URLs to the homepage.
- Treat soft 404s as content/status mismatches, not only literal `200` responses with the words “not found.”
- For removed content, choose among preservation, consolidation, relevant redirect, `404`, or `410` from user value and replacement equivalence—not a blanket SEO rule.
- Canonicalize duplicate or near-duplicate representations; do not use robots blocking as a canonicalization substitute.

## JavaScript

Collect both the initial response and rendered DOM when JavaScript affects primary content, links, metadata, structured data, canonicals, or status-like states.

Check:

- every meaningful screen has a stable URL
- navigation uses crawlable `<a href>` links rather than interaction-only discovery
- primary text and links do not require scroll, click, consent, or login unless intentionally restricted
- failed data fetching does not return an indexable empty app shell or soft 404
- canonical, robots, title, and structured data are stable after rendering
- lazy-loaded images/video have discoverable fallback URLs and metadata
- blocked scripts, APIs, CDNs, WAF rules, and timeouts do not prevent rendering

Server rendering or prerendering may simplify delivery, but implementation type is not itself a ranking claim. Verify output.

## Large sites and crawl efficiency

Crawl-budget work is mainly relevant to very large or frequently changing sites, or sites showing crawl-capacity problems. Before proposing it, inspect server logs, host errors, change frequency, duplication, faceted URLs, soft 404s, redirect chains, response time, cache behavior, sitemap freshness, and Search Console/Bing evidence.

Do not promise that blocking low-value URLs reallocates crawl to preferred URLs. Reduce useless URL generation, keep truthful `lastmod`, support caching/`304` where appropriate, and prioritize stable crawlable architecture.

## Migration gate

Before launch:

- inventory old URLs and classify their new equivalent, removal, or unchanged state
- test redirect mappings, status codes, canonical/hreflang, internal links, sitemaps, feeds, analytics, and robots directives
- preserve high-value pages, assets, structured data, and measurement continuity
- stage DNS/hosting capacity and keep rollback available

After launch:

- verify old and new hosts, redirects, logs, index reports, sitemaps, errors, and important templates
- keep redirects long enough for users and platforms to process the move
- separate expected recrawl fluctuation from mapping or availability failures

Source anchors: Google crawling/indexing, JavaScript SEO, canonicalization, redirects, site moves, crawl-budget, and Bing crawler documentation in `data/seo-source-registry.json`.
