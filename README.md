# WEPR Growth Skills

[中文](#中文说明) · [English](#english)

An open collection of practical Agent Skills for public relations, digital analytics, paid media, SEO/GEO, community marketing, and international growth.

一套面向公关、数字营销、广告投放、SEO/GEO、社区营销和品牌出海的可执行 Agent Skills。

---

## 中文说明

### 项目简介

`wepr-growth-skills` 将真实业务中的公关、数字营销、广告投放和出海增长方法，整理为可以被 Codex、Claude Code 及其他兼容 Agent 调用的独立技能。

这些技能强调：

- 先诊断问题，再选择渠道和服务；
- 先验证事实和数据，再给出判断；
- 输出动作、负责人、周期、指标和风险边界；
- 不用虚假互动、垃圾外链和平台规避换取短期数据；
- 不承诺无法控制的排名、爆款、推荐或销售结果。

### 技能目录

| 技能 | 中文名称 | 适用场景 | 主要输出 |
| --- | --- | --- | --- |
| `diagnose-pr-crisis` | 公关与危机诊断 | 舆情、声明、负面事件、媒体采访、海外危机 | 时间线、利益相关者、风险分级、回应策略、声明、Q&A、恢复计划 |
| `audit-digital-growth` | 数字营销增长诊断 | GA4/GTM、漏斗、转化、归因、CRM、留存 | 指标树、数据审计、漏斗、假设、实验、看板和90天路线图 |
| `plan-paid-media` | 全域广告投放规划 | 百度、360、Microsoft Ads、抖音、小红书、视频号 | 平台组合、账户结构、测试矩阵、预算、诊断、复盘和风险控制 |
| `plan-organic-growth` | 出海有机增长规划 | SEO、GEO、Reddit、Product Hunt、SaaS冷启动、内容增长 | 需求证据、渠道地图、SEO/GEO审计、社区与发布方案、实验和90天路线图 |

### 如何选择

- 发生负面事件、需要声明或媒体沟通：使用 `$diagnose-pr-crisis`。
- 有流量但不知道哪里出了问题：使用 `$audit-digital-growth`。
- 准备花媒体预算获客：使用 `$plan-paid-media`。
- 希望通过搜索、AI搜索、社区和内容长期获客：使用 `$plan-organic-growth`。
- 一个项目可以组合多个技能。例如先用增长诊断明确问题，再分别制定付费与有机增长计划。

### 安装

克隆仓库：

```bash
git clone https://github.com/ShenyuanNext/wepr-growth-skills.git
```

安装单个技能到 Codex：

```bash
cp -R wepr-growth-skills/skills/plan-organic-growth ~/.codex/skills/
```

安装到通用 Agent 技能目录：

```bash
cp -R wepr-growth-skills/skills/plan-organic-growth ~/.agents/skills/
```

也可以复制整个 `skills/` 下的四个目录。重新启动或刷新 Agent 后即可发现技能。

### 示例提示词

```text
使用 $diagnose-pr-crisis，分析这次产品安全争议，给出24小时回应计划和声明草案。
```

```text
使用 $audit-digital-growth，检查网站流量增长但询盘下降的原因，并设计验证实验。
```

```text
使用 $plan-paid-media，为B2B软件设计百度、Microsoft Ads和小红书的测试计划。
```

```text
使用 $plan-organic-growth，为一个新SaaS制定SEO、GEO、Reddit和Product Hunt的90天冷启动计划。
```

### 交付风格

技能默认使用执行者视角，输出：

1. 当前问题及证据；
2. 关键判断和不确定性；
3. 优先行动及负责人；
4. 时间表、预算或资源要求；
5. 验收指标与停止/扩量规则；
6. 合规、平台和商业风险。

### 安全与合规

本项目不支持：

- 伪造媒体报道、用户评价、订单、聊天记录或社会证明；
- 购买粉丝、Karma、Product Hunt投票或协同操纵互动；
- Reddit马甲号、封禁规避、自动垃圾回复；
- 垃圾外链、隐藏推广、关键词堆砌和批量低质页面；
- 盗版、侵权下载、未经授权使用个人数据；
- 保证排名、AI推荐、爆款、粉丝、询盘或收入。

所有平台功能、算法、准入、价格和案例数字，在正式执行前都应使用当前官方或第一方来源核实。

### 贡献

欢迎提交 Issue 和 Pull Request。建议包含：

- 具体业务场景；
- 当前技能的不足；
- 官方或第一方依据；
- 建议修改内容；
- 修改可能带来的风险；
- 可复现的测试提示词或样例输出。

---

## English

### Overview

`wepr-growth-skills` turns practical knowledge from PR, analytics, media buying, SEO/GEO, community work, and international growth into modular Agent Skills for Codex, Claude Code, and compatible agents.

The collection is designed to produce evidence-based execution plans—not generic marketing advice. Each skill emphasizes diagnosis, ownership, timelines, validation, and explicit risk boundaries.

### Included skills

| Skill | Purpose | Typical use cases | Core deliverables |
| --- | --- | --- | --- |
| `diagnose-pr-crisis` | PR and crisis response | Controversies, negative sentiment, statements, interviews, reputation recovery | Timeline, stakeholder map, risk grade, response plan, statement, Q&A, recovery roadmap |
| `audit-digital-growth` | Digital growth analytics | GA4/GTM, funnels, conversion, attribution, CRM, retention | Metric tree, tracking audit, funnel, hypotheses, experiments, dashboard, 90-day roadmap |
| `plan-paid-media` | Paid-media planning | Search ads, Douyin, Xiaohongshu, WeChat Channels, multi-platform acquisition | Channel roles, account structure, test matrix, budget, diagnostics, review system |
| `plan-organic-growth` | Organic international growth | SEO, GEO/AI search, Reddit, Product Hunt, SaaS launch, content systems | Demand evidence, channel map, SEO/GEO audit, community and launch plans, experiments, roadmap |

### Choosing a skill

- Use `$diagnose-pr-crisis` when the business needs a response, statement, media plan, or reputation recovery.
- Use `$audit-digital-growth` when performance is unclear or traffic, conversion, attribution, and retention disagree.
- Use `$plan-paid-media` when the team is preparing to spend media budget and needs a measurable acquisition system.
- Use `$plan-organic-growth` when growth should compound through search, AI search, community participation, launches, and content.
- Combine skills when appropriate. A growth audit can define the problem before separate paid and organic plans are built.

### Installation

Clone the repository:

```bash
git clone https://github.com/ShenyuanNext/wepr-growth-skills.git
```

Install one skill for Codex:

```bash
cp -R wepr-growth-skills/skills/plan-organic-growth ~/.codex/skills/
```

Install it in a shared Agent Skills directory:

```bash
cp -R wepr-growth-skills/skills/plan-organic-growth ~/.agents/skills/
```

You may copy all four folders under `skills/`. Restart or refresh the agent environment after installation.

### Example prompts

```text
Use $diagnose-pr-crisis to analyze this product-safety controversy and draft a 24-hour response plan.
```

```text
Use $audit-digital-growth to diagnose why website traffic grew while qualified leads declined.
```

```text
Use $plan-paid-media to design a measurable search and social advertising test for a B2B SaaS product.
```

```text
Use $plan-organic-growth to build a 90-day SEO, GEO, Reddit, and Product Hunt cold-start plan.
```

### Output philosophy

Skills aim to provide:

1. A clearly defined problem and supporting evidence;
2. Key judgments with uncertainty made explicit;
3. Prioritized actions and owners;
4. Timelines, resources, or budget requirements;
5. Success metrics and stop/scale rules;
6. Legal, platform, data, and commercial risks.

### Safety and integrity

This repository does not support fake media coverage, fake reviews, fabricated proof, purchased engagement, bought karma or votes, sockpuppets, ban evasion, spam backlinks, hidden sponsorships, piracy, unauthorized personal data, or guaranteed rankings and revenue.

Platform capabilities, policies, algorithms, prices, and examples must be re-verified against current official or first-party sources before client execution.

### Contributing

Issues and pull requests are welcome. Strong contributions include a concrete scenario, evidence or official source, a proposed change, the risk introduced by that change, and a reproducible prompt or example output.

## License

MIT
