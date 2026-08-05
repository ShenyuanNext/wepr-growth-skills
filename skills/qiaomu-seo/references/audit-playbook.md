# SEO Audit Playbook

This is the cross-domain checklist. Load the specialist guide instead of expanding every audit: [Technical SEO](technical-seo.md), [Content Quality](content-quality.md), [Performance And Measurement](performance-measurement.md), [International And Commerce](international-commerce.md), [Vertical Search](vertical-search.md), [Engine Matrix](engine-matrix.md), or [AI Search](ai-search.md).

## 1. Scope before checks

Identify site type, target markets, important page groups, business conversions, recent migrations/releases, and available evidence. For a large site, sample by template and page type instead of pretending a few URLs represent everything.

Before reporting breadth, create the coverage ledger in [Execution And Sampling](execution-sampling.md). A URL observed in a sitemap, static fetch, rendered page, and Search Console export has four different evidence states.

## 2. Discovery and indexability

Check, when observable:

- important URLs are linked with crawlable `<a href>` links
- robots.txt does not accidentally block resources or important crawl paths
- index control uses supported robots meta or `X-Robots-Tag` directives
- sitemaps contain preferred canonical, indexable URLs and truthful `lastmod` values
- response codes, redirect destinations, loops, chains, soft-404 behavior
- canonical signals agree across redirects, HTML/HTTP canonical annotations, internal links, and sitemaps
- duplicate, faceted, parameter, pagination, and alternate-language URL behavior
- rendered content and metadata are available to crawlers when JavaScript is required

Do not recommend blocking a duplicate URL in robots.txt as a canonicalization method. Do not assume that a disallowed URL cannot be indexed.

## 3. Technical delivery

Check HTTPS, mixed content, mobile rendering, navigation, client/server rendering differences, lazy-loaded primary content, and performance evidence.

For JavaScript sites, compare the HTTP response and rendered DOM. Check meaningful error status codes, crawlable `<a href>` links, app-shell/soft-404 behavior, blocked resources, renderer failures, client-only metadata, and whether primary content depends on interactions Googlebot will not perform.

For Core Web Vitals, distinguish:

- field data from CrUX or Search Console
- lab diagnostics from PageSpeed Insights, Lighthouse, WebPageTest, or local profiling

Use lab data to diagnose; do not report it as real-user field performance.

For thresholds, Search Console limitations, incident segmentation, and test design, use [Performance And Measurement](performance-measurement.md).

## 4. Page meaning and presentation

Evaluate whether each important page has:

- a descriptive, concise title that reflects visible content
- a useful main heading and logical sections
- a snippet candidate that communicates value without stuffing
- descriptive internal links
- appropriate image alternatives based on image purpose
- visible content consistent with metadata and structured data
- a clear canonical and language/locale identity when relevant

Avoid rigid character counts and heading-number rules. Search engines can rewrite title links and snippets; optimize clarity, distinctness, and user expectation.

## 5. Structured data

- Choose only a Google-supported feature that matches visible page content.
- Include required properties and truthful recommended properties.
- Inspect rendered JSON-LD when frameworks or plugins inject it client-side.
- Validate with Rich Results Test and, after deployment, URL Inspection or Search Console enhancement reports.
- Never add review, rating, author, offer, event, FAQ, or organization claims that the visible page does not support.
- Distinguish Schema.org syntax, Google-supported feature eligibility, and observed rich-result appearance. Check feature lifecycle before recommending a type.

## 6. Content and intent

Ask whether the page solves the query better for the intended audience:

- original experience, research, examples, or analysis
- accurate sourcing and clear authorship when trust matters
- complete enough to finish the user's task without artificial word-count padding
- current where facts materially change
- matches informational, navigational, commercial, transactional, or local intent
- adds value beyond summarizing competitors

Check cannibalization only with query/page data or meaningful SERP overlap. Similar keywords alone do not prove cannibalization.

## 7. Architecture and international SEO

Check navigation depth as a usability and discovery issue, not a universal “three clicks” law. Find orphaned and weakly linked important pages. Align hub pages, supporting pages, breadcrumbs, and contextual internal links.

For international sites:

- use distinct, crawlable locale URLs
- keep canonicals in the same language when possible
- require reciprocal hreflang relationships and valid language/region codes
- keep hreflang, canonical, redirect, and sitemap signals consistent
- research keywords separately for each market

Use [International And Commerce](international-commerce.md) for hreflang sets, pagination, product variants, feeds, and inventory states.

## 8. Diagnose traffic or ranking drops

Segment before guessing:

1. confirm analytics and Search Console tracking continuity
2. identify affected dates, pages, queries, countries, devices, and search types
3. compare with releases, migrations, redirects, robots/noindex/canonical changes, outages, content edits, seasonality, and SERP changes
4. inspect index coverage and manual/security actions when access exists
5. distinguish lost demand, lost visibility, lost CTR, lost indexing, and lost conversion

Do not blame a named algorithm update without evidence connecting the timing and affected patterns.

Do not recommend bulk deletion or radical rewrites from a short-lived fluctuation. Preserve a control group and change log when multiple causes remain plausible.

## 9. Prioritization

Recommended order:

1. accidental deindexing, inaccessible pages, broken migrations, critical server/rendering failures
2. canonical/redirect duplication and major architecture blockers
3. intent mismatch, weak or misleading page value, important internal-link gaps
4. metadata, structured data eligibility, images, and snippet improvements
5. long-term content, authority, and measurement programs

Each fix needs an owner, dependency, rollback note when risky, and a verification method.
