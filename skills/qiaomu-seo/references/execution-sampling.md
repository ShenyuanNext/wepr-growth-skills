# SEO Execution And Sampling

## Coverage before conclusions

Record these counts or lists before describing audit breadth:

- `discovered`: URLs known from sitemaps, crawl, routes, exports, or user input
- `selected`: URLs intentionally sampled
- `fetched`: URLs with an HTTP/static response inspected
- `rendered`: URLs inspected after JavaScript execution
- `data_backed`: URLs or groups supported by Search Console, analytics, logs, or crawl exports
- `failed`: URLs/tools that could not be inspected and why
- `not_checked`: known surfaces outside scope

Never call a small sample a full-site audit. Use “representative template sample” and name the sample strategy.

## Sampling strategy

Sample by page type and risk, not random convenience:

1. homepage and primary navigation hubs
2. top conversion or organic landing pages
3. one or more URLs from each material template
4. recently changed or migrated URLs
5. low-performing and high-performing controls
6. indexable/non-indexable, canonical/duplicate, paginated/faceted, and locale variants when relevant
7. error, redirect, out-of-stock, archived, or empty states

If a crawl or route inventory exists, group findings by template and preserve representative URLs. Do not multiply one observed template bug into an exact site-wide count without inventory evidence.

## Collection layers

Use the lightest layer that can answer the question:

1. repository/config: routes, metadata generation, sitemap/robots logic, redirects, structured data source
2. HTTP/static response: status, headers, initial HTML, canonical and robots directives
3. rendered DOM: JavaScript-generated content, links, metadata, JSON-LD, lazy loading, client routing
4. first-party tools: Search Console, analytics, logs, CrUX, crawl exports
5. current SERP observation: intent, result types, title/snippet rendering, competitor page patterns

Static and rendered evidence are different artifacts. Save or cite which one supports a finding.

## Rerun manifest

Preserve:

- audit date and timezone
- target domain and canonical host
- market, language, device, login/cookie state
- URLs, templates, sitemap or crawl inputs
- tools, commands, versions, and render settings
- first-party export date ranges
- failures and rate limits
- output files and checksums when reproducibility matters

Do not store credentials, raw cookies, private query strings, or unnecessary personal data.

## Change verification

Separate four milestones:

1. `implemented`: source/config changed and tests pass
2. `deployed and observable`: live HTTP/rendered output reflects the change
3. `processed by search platform`: crawl, rendering, index, canonical, enhancement, or other platform evidence reflects the change
4. `outcome observed`: qualified performance or user/business data supports an effect after an appropriate window

Only the fourth milestone supports an outcome claim. Deployment or recrawl success is not ranking, traffic, or conversion success.
