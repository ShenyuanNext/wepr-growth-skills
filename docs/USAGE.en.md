# WEPR Growth Skills Usage Guide

## 1. What this collection does

This repository is a set of composable execution workflows, not a library of marketing slogans. Each skill owns a decision domain and is designed to move from objective and evidence to actions, owners, validation, and risk boundaries.

| Skill | Primary job |
| --- | --- |
| `$diagnose-pr-crisis` | Respond to controversies, media inquiries, and reputation damage |
| `$audit-digital-growth` | Diagnose traffic, conversion, attribution, CRM, and retention |
| `$plan-paid-media` | Plan and review measurable search and social media buying |
| `$plan-organic-growth` | Build SEO, GEO, community, launch, and content systems |
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

### Organic growth

```text
Use $plan-organic-growth to build a 90-day SEO, GEO, Reddit, and Product Hunt plan. Start with demand evidence and channel roles, then prioritize experiments.
```

Provide the product, user, alternatives, current site and content, market, and capacity. Purchased karma, votes, and spam links are out of scope.

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
