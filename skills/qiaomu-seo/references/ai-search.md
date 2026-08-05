# AI Search Extension

Last reviewed: 2026-08-03. Recheck volatile provider sources in `data/seo-source-registry.json`.

## Google AI features

Google states that AI Overviews and AI Mode use the same foundational SEO practices as Search. A supporting page must be indexed and eligible to appear with a snippet; there are no additional technical requirements, special AI schema types, or required AI text files.

Use normal foundations:

- crawl and index eligibility
- important text available in rendered content
- crawlable internal links
- useful, reliable, people-first content
- structured data matching visible content
- page experience, Merchant Center, and Business Profile where relevant

Google's newer generative-AI optimization guide documents a dedicated Search Console Generative AI performance report. Its broader AI-features documentation also describes AI-feature traffic as contributing to overall Search Console Web reporting. Treat these as different reporting views that may have rollout or property-availability conditions; verify the current property and documentation before claiming only one view exists.

Google's 2026 guidance also says:

- `llms.txt` neither helps nor harms Google Search visibility or ranking
- no special Schema.org type is required for generative Search
- there is no ideal AI-specific page length or mandatory “chunking” pattern
- pages do not need to be rewritten for AI or every fan-out query
- scaled pages created mainly to manipulate AI/search responses can violate spam policy

Official sources:

- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

## Other AI search systems

ChatGPT Search, Perplexity, Copilot, Gemini surfaces, and other systems may differ by provider, product, model, geography, login state, and date. Verify current official crawler/search documentation and observed source behavior per provider. Use [Engine Matrix](engine-matrix.md).

For OpenAI, keep these controls separate:

- `OAI-SearchBot`: automatic Search discovery/surfacing
- `GPTBot`: content that may be used for foundation-model training
- `ChatGPT-User`: user-triggered visits that are not automatic Search crawling and may not follow robots rules identically

For Perplexity, current documentation distinguishes `PerplexityBot` for search from other provider behavior. Verify published IP ranges when bot identity matters.

Do not assume:

- one robots directive controls every provider
- a training crawler is the same as a search/citation crawler
- one citation test predicts future answers
- a mention means recommendation
- structured data or `llms.txt` guarantees retrieval or citation

## Evidence ladder

Track separate stages:

1. `eligible`: content is accessible under the provider's documented conditions
2. `retrieved`: the system appears to use or surface the source
3. `cited`: the source receives an explicit citation/link
4. `mentioned`: the entity or brand is named
5. `recommended`: the entity is included in a preferred shortlist
6. `converted`: measurable downstream user action occurs

Never collapse these stages into “AI visibility improved.”

## Observation protocol

For a useful AI-search check, record:

- query set and selection rationale
- provider and product surface
- date/time, market/language, device, and login state when relevant
- answer, citations, cited URL, mention framing, and recommendation state
- repeated observations or independent reviewers when claims matter
- referral/conversion evidence when available

Treat manual prompt checks as sampled observations, not a stable ranking report.

## Optional agent-readable files

An `llms.txt`, markdown knowledge bundle, or simplified pricing/specification file may improve documentation or agent operability in some contexts. Before proposing one:

- identify the consumer and documented behavior
- avoid duplicating or exposing private content
- keep it consistent with visible canonical pages
- define how freshness will be maintained
- label ranking/citation impact as `missing evidence` unless measured

Do not add a file solely because an SEO checklist claims it is required.
