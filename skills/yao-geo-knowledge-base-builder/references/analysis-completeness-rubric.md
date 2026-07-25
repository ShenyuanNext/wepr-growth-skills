<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-knowledge-base-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Analysis Completeness Rubric

Run this before writing the report and again before final delivery.

## Scoring

| Score | Meaning |
| --- | --- |
| 0 | Missing or only implied |
| 1 | Present but thin, generic, or not source-backed |
| 2 | Source-backed and reusable, but missing edge cases or aliases |
| 3 | Complete enough for downstream GEO reuse and audit |

## Required Dimensions

| Dimension | Pass Standard |
| --- | --- |
| Identity | Brand, company/legal entity if available, website, category, regions, target users |
| Entity Inventory | Complete entity list with type, canonical name, aliases, relationship, source, confidence, usage note |
| Offerings | Products, services, features, plans, packages, prices, and usage scenarios |
| Capabilities | Core capabilities, AI/technology capabilities, integrations/channels, limits |
| Metrics | Public numbers with date, source, scope, and reuse note |
| Evidence | Source IDs, publisher, source type, verification date, confidence tier |
| Data Access | Acquisition mode, accessible sources, unavailable sources, freshness cadence, strong-evidence eligibility |
| Provenance | Brand fact can trace back to source and extraction note |
| Vocabulary | Preferred terms, aliases, Chinese/English names, standard query terms |
| Cases | Named cases if verified; aggregate proof or explicit no-case boundary if not verified |
| Timeline | Milestones, launches, releases, metric dates, report version date |
| Competitive Context | Competitors or comparison objects with no unsupported ranking |
| Domestic AI Fit | Kimi, Qianwen, DeepSeek, Doubao, Yuanbao reuse notes |
| Risk Boundary | Pending claims, prohibited expressions, privacy/authorization checks |
| Output Quality | Four files exist, tables wrap, DOCX/PDF no right overflow, HTML has sticky menu |

## Repair Rule

If any dimension scores below `2`, either:

- add source-backed content to the report,
- move the claim to pending confirmation,
- or explicitly state that the dimension has no verified public evidence in this run.
