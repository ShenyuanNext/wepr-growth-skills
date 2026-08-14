# WEPR Growth Skills Usage Guide

## 1. What this collection does

This repository is a set of composable execution workflows, not a library of marketing slogans. Each skill owns a decision domain and is designed to move from objective and evidence to actions, owners, validation, and risk boundaries.

| Skill | Primary job |
| --- | --- |
| `$wepr-client-discovery` | Turn interviews, questionnaires, and decisions into a handoff-ready client brief |
| `$wepr-business-workbench` | Clarify commercial problems, diagnose models and trade-offs, and build testable client strategy |
| `$wepr-market-signal-research` | Distill needs, pains, objections, and audience language from public feedback and platform signals |
| `$diagnose-pr-crisis` | Respond to controversies, media inquiries, and reputation damage |
| `$pr-strategy-workbench` | Build client PR plans, communication decisions, narrative analysis, launch-risk plans, and public copy |
| `$audit-digital-growth` | Diagnose traffic, conversion, attribution, CRM, and retention |
| `$plan-paid-media` | Plan and review measurable search and social media buying |
| `$wepr-advertising-workbench` | Plan, audit, and optimize cross-platform advertising with creative, attribution, experiments, and guarded changes |
| `$plan-organic-growth` | Build SEO, GEO, community, launch, and content systems |
| `$wepr-seo` | Handle quick/full HTML audits, site strategy, technical SEO, keywords, migrations, international, commerce, and AI search |
| `$operate-georank-workbench` | Safely operate a deployed GEOrank instance and its API |
| `$plan-xiaohongshu-growth` | Plan, write, rewrite, and diagnose Xiaohongshu content |
| `$xiaohongshu-suite` | Route an unclear Xiaohongshu problem to the earliest blocked stage |
| `$xiaohongshu-profile` | Audit profile positioning, bio, proof, and pinned posts |
| `$xiaohongshu-topic-planner` | Build topic pools, series, calendars, and evidence plans |
| `$xiaohongshu-title` | Generate, diagnose, select, and rewrite titles and cover lines |
| `$xiaohongshu-comment-reply` | Classify comments, draft replies, handle objections, and flag risk |
| `$xiaohongshu-conversion-path` | Design content-to-profile-to-action and delivery paths |
| `$distill-creator-playbook` | Distill public creator content into an original testable playbook |
| `$plan-editorial-illustrations` | Translate articles into coherent illustration systems |
| `$analyze-brand-strategy` | Diagnose evidence-aware positioning, differentiation, competition, and expansion |
| `$create-marketing-content` | Turn business evidence into credible platform-native content |
| `$wepr-marketing` | Build client marketing plans, communication strategy, early acquisition, and conversion copy |
| `$wepr-editorial-quality` | Diagnose mechanical writing and evidence risk, then minimally revise while preserving author voice |
| `$wepr-human-writing` | Revise proposals, communication drafts, and copy into natural Chinese without changing business meaning |
| `$launch-content-account` | Launch WeChat, Douyin, WeChat Channels, X, and Xiaohongshu accounts |

## 2. Installation

```bash
git clone https://github.com/ShenyuanNext/wepr-growth-skills.git
cp -R wepr-growth-skills/skills/* ~/.codex/skills/
```

For a shared Agent Skills directory:

```bash
cp -R wepr-growth-skills/skills/* ~/.agents/skills/
```

Restart or refresh the agent. A compatible client should at minimum discover each folder's `SKILL.md`.

## 3. Minimum useful input

Provide the business, target user, current stage, desired decision or outcome, available evidence, time range, resources, and desired format. The skill should ask only when a missing choice materially changes the result; otherwise it should state assumptions and proceed.

```text
Use $skill-name.
Business:
Target user:
Current problem:
Required decision or deliverable:
Available evidence:
Constraints:
```

## 4. Skill examples

### Client discovery

```text
Use $wepr-client-discovery to turn these client meeting notes into confirmed facts, preferences, decisions, assumptions, and open questions; then produce a requirements brief, an asynchronous questionnaire, owners, and deadlines.
```

Provide the raw conversation, project purpose, participants, expected deliverable, and known constraints. The skill asks only questions that can change direction, scope, price, or acceptance; public facts remain the delivery team's research responsibility.

### Market-signal research

```text
Use $wepr-market-signal-research to study how target users describe this problem across public communities, reviews, Q&A, and launch platforms; preserve links and dates, deduplicate the sample, and report needs, pains, objections, alternatives, language patterns, and opportunity hypotheses.
```

Provide the decision, market, language, user role, date range, competitors, and accessible sources. Platform engagement is not market size; insufficient samples should remain preliminary signals with a validation plan.

### Business strategy workbench

```text
Use $wepr-business-workbench to turn this vague client request into a testable problem statement, separate facts from assumptions, compare competing explanations, recommend one direction, and define falsification conditions and a minimum validation plan.
```

Provide the decision to unlock, current state, target user, evidence, horizon, budget, capacity, and acceptance standard. It owns commercial judgment and specialist handoff, not the full execution of marketing, PR, brand, or content work.

### Crisis and PR

```text
Use $diagnose-pr-crisis to separate confirmed, disputed, and unknown facts, then produce a 0–2h, 2–24h, and 24–72h response plan, holding statement, and media Q&A.
```

Provide a timeline, evidence, public statements, stakeholders, and legal or operational status. Do not use the skill to promise deletion or opinion manipulation.

### Digital growth audit

```text
Use $audit-digital-growth to diagnose why traffic increased while qualified leads declined. Build a metric tree, audit tracking and CRM feedback, and propose competing hypotheses with validation experiments.
```

Provide metric definitions, dates, channel and funnel data, sales outcomes, and known data gaps. Platform attribution is not incrementality.

### Paid media

```text
Use $plan-paid-media to design a first-month B2B acquisition test with account structure, creative variables, budget, sustainable CPL, CRM feedback, and stop rules.
```

Provide price, margin, LTV, valid-lead definition, sales capacity, eligibility, and budget. Recheck current platform policy before launch.

### Advertising strategy workbench

```text
Use $wepr-advertising-workbench to audit Google, Meta, and LinkedIn account exports against landing-page and CRM outcomes; separate account health, evidence coverage, and compliance risk; then produce budget, creative, attribution, and experiment recommendations without applying changes.
```

Provide the business objective, economics, valid-conversion definition, platforms and markets, account exports, date range, landing-page and CRM outcomes, tracking setup, budget boundaries, and any explicit write authorization. The default is read-only with draft outputs. Any live mutation requires explicit authorization, exact objects, before-and-after values, ceilings, rollback, and verification. Pair with `$plan-paid-media` and current official sources for China-platform-specific eligibility and delivery rules.

### Organic growth

```text
Use $plan-organic-growth to build a 90-day SEO, GEO, Reddit, and Product Hunt plan. Start with demand evidence and channel roles, then prioritize experiments.
```

Provide the product, user, alternatives, current site and content, market, and capacity. Purchased karma, votes, and spam links are out of scope.

### GEOrank workbench operations

```text
Use $operate-georank-workbench to connect to this GEOrank instance, verify the detected identity and permissions, and start a diagnosis for the specified site. Preflight every write and never expose credentials.
```

Provide the instance URL, account, target resource, intended operation, and explicit authorization for any write. Use `$plan-organic-growth` for general GEO strategy and client planning; use this skill only when a live GEOrank instance must be called. Remote instances require HTTPS, and administrator writes and deletions have separate confirmation gates.

### Xiaohongshu growth

```text
Use $plan-xiaohongshu-growth to turn “GEO for B2B brands” into an executable image-text post for marketing leaders. Provide two titles under 20 Chinese characters, final copy, primary and supporting keywords, a save-worthy checklist, and a natural consultation path.
```

Available modes are single post, calendar, diagnosis, and rewrite. The skill aligns one primary search intent with the title promise and body delivery; it must not invent volume, ranking, or case results.

### Xiaohongshu specialist workbench

Use `$xiaohongshu-suite` when the blocked stage is unclear. Use `$xiaohongshu-profile`, `$xiaohongshu-topic-planner`, `$xiaohongshu-title`, `$xiaohongshu-comment-reply`, or `$xiaohongshu-conversion-path` directly for a single-purpose request. Use `$plan-xiaohongshu-growth` for final copy, keywords, and publishing-ready posts.

### Creator distillation

```text
Use $distill-creator-playbook. Platform: Xiaohongshu. Mode: benchmark. Objective: topic and structure research. Analyze 30 public posts from each of these three accounts and produce an evidence-tagged original playbook.
```

Specify platform, target, own-account versus benchmark mode, objective, sample size, and accessible material. The output should separate observation from inference and include confounders and experiments—not copy a creator's wording or identity.

### Editorial illustrations

```text
Use $plan-editorial-illustrations to design six 16:9 visuals for this article using a clean background, loose black linework, and sparse red and blue accents. Start with placement, action, composition, and prompts, then perform text and consistency QA.
```

Provide the complete article, publishing surface, ratio, count, brand rules, and whether images should be generated. The default is a shot list; explicit generation requests should proceed when an image tool is available.

### Brand strategy analysis

```text
Use $analyze-brand-strategy to evaluate this brand's path into a younger market. Check research readiness first; separate company claims, customer perception, and behavioral evidence; map direct competitors, indirect alternatives, the current workaround, inaction, and the mental benchmark; compare three strategic options, recommend one, and provide sacrifices, falsification conditions, and a 90-day validation plan.
```

Provide the decision, market, audience, offer and price architecture, channels, substitutes, research, and operating evidence. When evidence is incomplete, the skill should return validate-first or insufficient-evidence instead of manufacturing certainty. Use cases to study mechanisms, not to copy conclusions.

### Marketing content creation

```text
Use $create-marketing-content to turn these project materials into a publishable article. Build a fact-and-opinion ledger first, then provide final copy, two headlines, and editorial QA notes.
```

Provide the reader, platform, content job, sources, publishable facts, voice, and length. Use `$plan-xiaohongshu-growth` for Xiaohongshu-specific search and account execution.

### Natural Chinese writing

```text
Use $wepr-human-writing to remove translated phrasing, generic filler, mechanical parallelism, and abrupt transitions from this proposal. Preserve every client name, fact, price, deliverable, commitment, and compliance statement; flag missing evidence instead of inventing it.
```

Provide the source text, reader, delivery context, editing boundary, protected facts and terms, and brand voice. Use it after strategy and structure are stable. Start with `$wepr-marketing`, `$create-marketing-content`, or `$pr-strategy-workbench` when the underlying message is still undecided.

### Editorial quality and minimal revision

```text
Use $wepr-editorial-quality to identify observable mechanical patterns, templated rhythm, generic claims, and evidence risks without guessing whether AI wrote the draft; then make the smallest useful revision while preserving the author's vocabulary, stance, and cadence.
```

Provide the full draft, reader, channel, content job, author or brand voice, editing boundary, and all protected facts, prices, commitments, and compliance language. Request diagnosis mode for findings only or minimal-revision mode for a complete edited draft. Use `$wepr-human-writing` afterward when a natural Chinese final pass is also required.

### Content-account launch

```text
Use $launch-content-account to launch a WeChat Channels account for international-brand leaders. The objective is professional trust and qualified inquiries. Design the account promise, profile, content pillars, first comparable sample, review metrics, and a 30-day plan.
```

Provide the business objective, platform, audience, account role, offer, publishable evidence, production capacity, horizon, and compliance constraints. The skill does not treat fixed cadence, three-second hooks, content ratios, or engagement thresholds as platform rules.

## 5. Combined workflows

### Client growth plan

1. Use `$analyze-brand-strategy` to define the best-fit customer, choice situation, category, competition reference, and provable difference.
2. Use `$audit-digital-growth` to define the problem and measurement system.
3. Use `$plan-paid-media` for controlled acquisition tests.
4. Use `$plan-organic-growth` for compounding search and community assets.
5. Combine owners and reviews in one 30/60/90-day roadmap.

### Xiaohongshu production system

1. Use `$distill-creator-playbook` to identify transferable patterns from public benchmarks.
2. Use `$xiaohongshu-suite` to locate the earliest blocked stage.
3. Use `$xiaohongshu-profile` and `$xiaohongshu-topic-planner` for profile acceptance and topic planning.
4. Use `$xiaohongshu-title` and `$plan-xiaohongshu-growth` for titles, intent, keywords, and final copy.
5. Use `$xiaohongshu-comment-reply` and `$xiaohongshu-conversion-path` for conversation and qualified actions.
6. Use `$plan-editorial-illustrations` for visuals and feed real publishing evidence into the next test cycle.

### Reputation recovery

1. Use `$diagnose-pr-crisis` to unify facts, response, and operations.
2. Use `$audit-digital-growth` to monitor search, site behavior, leads, and retention.
3. Use `$plan-organic-growth` to build verifiable fact pages, cases, and durable trust assets.

## 6. Acceptance criteria

A strong output contains a defined problem, separated facts and hypotheses, prioritized actions, owners, timing, resources, metrics, stop or scale rules, uncertainty, and risks. Reject outputs that consist only of platform tricks, slogans, or guaranteed outcomes.

## 7. Data and integrity

Use only data you are authorized to process. Public visibility does not authorize unlimited collection, re-identification, or redistribution. Do not fabricate coverage, reviews, orders, chats, cases, search data, or engagement. Do not use sockpuppets, ban evasion, hidden promotion, spam links, or keyword stuffing. Platform policies, product names, prices, and algorithms change; verify current official sources before execution.
