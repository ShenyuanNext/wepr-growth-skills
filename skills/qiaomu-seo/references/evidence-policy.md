# SEO Evidence Policy

## Evidence levels

| Label | Meaning | Allowed claim |
|---|---|---|
| `observed` | Directly seen in rendered DOM, HTTP response, repository, supplied export, or official tool output | State what was observed and how |
| `inferred` | Supported by partial evidence but not directly confirmed | State the inference and alternative explanations |
| `missing evidence` | Required data or access is absent | State what cannot be concluded and what would resolve it |

Never turn a heuristic, third-party estimate, `site:` query, one-page fetch, or generic checklist into a confirmed site-wide finding.

Coverage is evidence too. Record the target inventory, sampling method, checked/rendered/data-backed counts, failures, and exclusions before making site-wide claims.

## Source hierarchy

1. User-provided first-party data: Search Console, analytics, server logs, crawl exports, repository and deployment behavior.
2. Current official search-engine documentation and official testing tools.
3. Rendered public pages and HTTP behavior.
4. Reputable third-party tools and studies, labeled with provider, date, and methodology limitations.
5. Heuristics, clearly marked as heuristics.

## Mutable metrics

For rankings, search volume, difficulty, backlinks, traffic, Core Web Vitals, SERP features, or competitor performance, record:

- source
- market and language
- device when relevant
- observed/export date
- page/query scope
- whether the value is first-party, third-party estimate, or manual observation

If any required dimension is absent, use `unknown` rather than estimating a precise number.

## Audit finding schema

Every material finding should include:

- `category`
- `issue`
- `status`: pass, warning, fail, not_checked
- `evidence_level`: observed, inferred, missing evidence
- `evidence`
- `impact`: critical, high, medium, low
- `confidence`: high, medium, low
- `recommended_fix`
- `effort`
- `dependencies`
- `verification`

Severity answers “how much could this matter?” Confidence answers “how sure are we this finding is real?” Do not collapse them.

## Claim boundaries

- A successful Rich Results Test proves supported markup validity for that test, not future display.
- A URL in a sitemap proves declared discovery intent, not crawling or indexing.
- A `site:` query is a rough diagnostic, not a complete index report.
- A lab performance test is not field Core Web Vitals.
- A keyword tool reports estimates, not guaranteed demand or conversions.
- Correlation after an SEO change is not automatically causation; preserve change dates and competing explanations.
- A deployed fix proves implementation, not recrawl, reindexing, ranking, traffic, citation, or conversion impact.
- One AI answer or citation is a sampled observation, not a stable provider ranking.
