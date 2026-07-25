<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-knowledge-base-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Knowledge Base Architecture

This reference combines the formal AI brand knowledge-base structure from `ai-brand-kb-builder` with the evidence-led GEO reuse layer in this skill. It is also aligned with Schema.org entity typing, W3C PROV-O provenance thinking, W3C SKOS vocabulary/alias modeling, and Google Search Central structured-data module thinking.

## Output Stack

The report must read in this order:

| Layer | Purpose | Required Sections |
| --- | --- | --- |
| Decision layer | Let readers understand the brand without context | structured summary, test scenario, evidence boundary |
| Systematic KB layer | Provide a complete brand knowledge base that AI platforms can extract | basic profile, positioning, product/service matrix, metrics, cases, timeline, differentiation, query terms, expression rules |
| Data access layer | Make the real-data boundary explicit before claims are reused | acquisition mode, accessible sources, inaccessible sources, freshness cadence, strong-evidence eligibility |
| Entity layer | Make every reusable entity explicit and auditable | complete entity inventory |
| GEO reuse layer | Feed downstream GEO content, page, monitoring, and customer-service tasks | fact cards, FAQ, prohibited expressions, prompt input pack, domestic platform adaptation |
| Audit layer | Preserve verification and update controls | source index, pending-confirmation area, version/update mechanism |
| Completeness layer | Prove the analysis is systematic and complete | authoritative reference alignment, analysis completeness self-check, entity coverage statistics |

## Required Systematic KB Sections

| Section | Required Fields | Notes |
| --- | --- | --- |
| 结构化摘要 | brand, category, core products, proof points, verification date | 80-160 Chinese characters; must stand alone |
| 企业与品牌基本信息 | company, brand, website, industry, users, regions, verified date | Use key-value table |
| 品牌定位与核心主张 | one-sentence positioning, mission/value proposition, differentiation | Avoid advertising claims without evidence |
| 产品与服务矩阵 | product/service, category, scenario, capability, evidence source | Include all named public products or service groups found in sources |
| 核心数据与指标 | metric, value, date/scope, source, reuse scenario | Every number needs date or scope |
| 案例、客户与社会证明 | customer/case/aggregate proof, evidence, privacy boundary | If no named case is verified, say no public named case was verified |
| 品牌事件与时间线 | date, event, significance, source | Include launches, financial/customer-count milestones, major product releases |
| 竞品对比与差异化 | comparison dimension, brand position, common competitors, boundary | Do not invent rankings |
| 标准查询词与同义表达 | standard term, aliases, user queries, platform usage | Supports domestic AI query rewriting |
| 品牌使用与对外表达规范 | recommended wording, prohibited wording, replacement | Keeps downstream content consistent |
| 真实数据获取与限制 | acquisition mode, accessible sources, unavailable sources, freshness risk, next data-access actions | Required so users know whether the run used public web, user files, authenticated data, or manual brief only |
| 方法论参考与分析完整性自检 | reference alignment, coverage matrix, missing evidence, repair action | Must show how the report reached systematic/detail/complete standard |

## Complete Entity Inventory

The entity inventory is mandatory. Each row should contain:

| Field | Meaning |
| --- | --- |
| `entity_id` | Stable ID, such as `E-BRAND-001` |
| `entity_type` | brand, company, product, service, feature, agent, metric, price, region, channel, customer, case, competitor, source, pending-boundary |
| `canonical_name` | Preferred name for reuse |
| `aliases` | Chinese name, English name, abbreviation, old name, or query synonym |
| `relationship` | Parent, owner, part-of, related-to, competes-with, pending-for |
| `source` | Source ID or pending confirmation |
| `confidence` | A/B/C/D tier |
| `usage_note` | How the entity should be reused or restricted |

Entity coverage should include:

- brand and legal/company entities
- product and service families
- named features, tools, agents, dashboards, or technical concepts
- price/package facts
- metrics and milestone facts
- regions and domestic-market boundaries
- channels and ecosystems
- verified customers/cases or aggregate customer proof
- named competitors or comparison objects
- source documents and unresolved pending entities

## Fact Cards Versus Entity Inventory

- Entity inventory answers: "What entities exist and how are they related?"
- Fact cards answer: "What auditable claims can be reused?"
- Product/service matrix answers: "What does the brand offer?"
- Prompt input pack answers: "Which compressed facts should downstream skills ingest?"

Do not replace the entity inventory with fact cards. Both are required.
