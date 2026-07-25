<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-knowledge-base-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Source Acquisition And Freshness

This skill can use real data only when the data is accessible, cited, and time-stamped. Every report must state the acquisition mode and boundary before strong facts are reused.

## Acquisition Modes

| Mode | Input | Can Enter Strong Evidence | Boundary |
| --- | --- | --- | --- |
| Public web evidence | Official pages, product pages, pricing pages, help centers, investor releases, public reports | Yes, if the URL is accessible and the claim is dated or scoped | Dynamic pages, geo-specific pages, paywalls, robots blocks, and content changes may limit coverage |
| User-provided files | PDFs, Word docs, white papers, sales decks, screenshots, exported sheets | Yes, if the file is provided by the user and the source/owner is clear | Internal claims should be marked as internal-source evidence, not public proof |
| Authenticated workspace | CRM, help desk, analytics, shared drives, or private docs explicitly connected by the user | Yes, but only inside the authorized scope | No access should be implied without explicit connector/tool permission |
| Manual brief only | User text without source files or URLs | Usually no; use C or D tier unless the user confirms authority | Must not present unchecked claims as verified facts |
| Unavailable source | Dead link, login wall, blocked page, missing file, or unsupported format | No | Move to pending confirmation with the exact reason |

## Freshness Rules

| Fact Type | Default Cadence | Reason |
| --- | --- | --- |
| Pricing, packaging, capacity limits, AI credits | Monthly | Commercial details change frequently |
| Product names, AI features, platform coverage | Monthly | Product pages and release notes are volatile |
| Customer counts, revenue, investor metrics | Quarterly or after earnings release | Financial metrics update on reporting cycles |
| Compliance, data residency, privacy, ICP, local support | Per engagement and before publication | High-risk claims require current authorized sources |
| Case studies and customer logos | Quarterly or before external use | Permission and usage rights can change |
| Brand positioning and evergreen company overview | Quarterly | Lower volatility but still needs source freshness |

## Mandatory Report Module

Every final report must include `真实数据获取与限制` with:

- acquisition mode used in this run,
- accessible real-data sources,
- inaccessible or not-yet-verified sources,
- freshness risk by fact type,
- what can enter strong evidence,
- what must stay in pending confirmation,
- next data-access actions.

## Strong-Evidence Rule

Only facts with a source ID, publisher, verification date, extraction note, and confidence tier can enter strong evidence. If any of those fields are missing, either repair the evidence record or move the claim to the pending-confirmation area.
