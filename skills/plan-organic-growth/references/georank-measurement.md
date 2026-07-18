# GEO diagnostic and measurement loop

Use this reference when a GEO project needs a repeatable baseline, prompt panel, diagnosis-to-action workflow, or a GEOrank-assisted operating model. Use `$operate-georank-workbench` only when a live GEOrank instance must be operated.

## 1. Define the decision before scoring

Record the brand, domain, market, audience, product category, commercial objective, comparison set, target languages, target AI surfaces, and review period. A score without this scope is not comparable over time.

## 2. Build an evidence ledger

Separate:

- first-party facts: product pages, pricing, policies, cases, experts, documentation, and support records;
- third-party evidence: editorial coverage, reviews, directories, standards, research, and partner references;
- technical signals: crawlability, canonicalization, structured data, metadata, page extraction quality, and internal linking;
- hypotheses: expected audience language, category associations, likely objections, and assumed citation sources.

Record URL, owner, publication date, last verification date, claim supported, and whether the source is independent.

## 3. Establish a fixed prompt panel

Create prompts across six jobs:

1. category discovery;
2. brand/entity understanding;
3. comparison and alternatives;
4. problem/solution questions;
5. buying-risk and objection questions;
6. recommendation and shortlist questions.

Keep a stable control panel for monthly comparison and a smaller exploratory panel for new demand. Store prompt, locale, model, date, answer, citations, rank/position when observable, and uncertainty. Do not merge results from different models or dates without labeling them.

## 4. Diagnose in layers

1. **Access:** robots, status codes, renderability, canonical and indexability.
2. **Extraction:** headings, concise answers, tables, definitions, facts, and semantic chunking.
3. **Entity:** consistent brand, product, people, location, category, and relationship signals.
4. **Evidence:** sources, citations, dates, authorship, methods, examples, and claim support.
5. **Coverage:** whether the site answers the prompt panel completely and without contradiction.
6. **External authority:** relevant independent references and corroboration.
7. **Conversion:** a clear next action after the answer is discovered.

## 5. Translate findings into 30/60/90 days

- **0–30 days:** repair access and extraction blockers; correct entity facts; create measurement baseline; fix unsupported claims.
- **31–60 days:** publish priority answer pages, comparisons, FAQs, cases, expert pages, and structured data; improve internal linking.
- **61–90 days:** earn independent references, refresh weak pages, test new prompt clusters, and consolidate duplicated or low-value content.

Every action needs an owner, dependency, effort, expected signal, validation date, and stop/continue rule.

## 6. Measurement model

Track multiple dimensions instead of one proprietary score:

- prompt coverage rate;
- accurate brand mention rate;
- recommendation/shortlist rate, separately labeled;
- citation share and source diversity;
- factual error or contradiction rate;
- crawl/index health;
- answer-page impressions and clicks where first-party data exists;
- assisted qualified leads and sales outcomes;
- content freshness and verification debt.

Report denominators, samples, dates, models, locales, and confidence. Treat model answers as observations, not stable rankings. Never promise that a platform will cite, recommend, or rank a brand.

## 7. GEOrank-assisted workflow

Use the workbench sequence as an operating scaffold:

`discover → diagnose → ask → plan → expand → structure → manage`

- Use diagnosis to produce a prioritized issue backlog, not a decorative score.
- Feed verified company and diagnostic context into solution conversations.
- Expand a validated business term into question, scenario, comparison, objection, and commercial-intent variants.
- Generate JSON-LD or `llms.txt` only after source facts and site architecture are confirmed.
- Export artifacts into the evidence ledger and review them before publication.

## 8. Quality gate

Reject a GEO plan when it lacks a fixed baseline, source ledger, denominators, prompt samples, owners, validation dates, or factual-risk controls. Reject keyword stuffing, fabricated citations, mass low-quality pages, hidden promotion, and guarantees of AI recommendations.
