# Routing and delivery

## Capability map

| Need | Primary skill | Required handoff |
| --- | --- | --- |
| GEO baseline | `yao-geo-panorama-audit` | platform scope, evidence ledger, gaps, priorities |
| Intent expansion | `yao-geo-intent-miner` | seed terms, audience, stage, evidence needs |
| Brand knowledge | `yao-geo-knowledge-base-builder` | source IDs, fact cards, prohibited claims |
| Entity graph | `yao-geo-brand-graph` | canonical entities, aliases, evidence-backed edges |
| Existing page audit | `yao-geo-page-audit` | URLs, page type, observed code/content evidence |
| Page blueprint | `yao-geo-page-blueprint` | target questions, facts, conversion goal, CMS constraints |
| Content production | matching `yao-geo-*` content skill | source pack, audience, format, compliance limits |
| AI answer sampling | platform crawler | prompt IDs, repeats, environment, raw evidence |
| Signal monitoring | `yao-geo-effect-monitor` | baseline, sample protocol, citation and fact metrics |
| Conversion attribution | `yao-geo-tracking` | landing paths, CRM fields, direct/indirect signals |
| Execution plan | `yao-geo-execution-roadmap` | diagnosis, capacity, budget, owners, acceptance criteria |
| GEOFlow work | `geoflow` | mode, workspace or instance, target, authorization |

## Stage gates

1. **Evidence gate:** key claims have a source, date, confidence level, and usage boundary.
2. **Intent gate:** questions are natural, deduplicated, stage-aware, and mapped to assets.
3. **Production gate:** every asset answers a defined question and cites only supported facts.
4. **Sampling gate:** real and synthetic samples are separated; raw answers and environment are retained.
5. **Measurement gate:** baseline, observation window, comparison prompts, and confounders are documented.
6. **Delivery gate:** files open correctly, formats agree, and owners plus acceptance tests are present.

## Standard combinations

### New quarterly GEO engagement

`panorama-audit → intent-miner → knowledge-base-builder → page-blueprint/content → effect-monitor → execution-roadmap`

### Content-only engagement

`intent-miner → knowledge-base-builder → selected content skill → effect-monitor`

### Platform visibility study

`intent-miner → selected crawler(s) → effect-monitor → execution-roadmap`

### GEOFlow implementation

`wepr-geo-suite scope → geoflow discovery/development or operations → verification → approved activation`

## WEPR commercial handoff

Keep scope and pricing outside unverifiable performance claims. Define the unit of work, platform count, prompt count, sampling repeats, asset count, review rounds, reporting cadence, exclusions, and optional work. Use `$wepr-pricing` when a formal WEPR estimate is requested.
