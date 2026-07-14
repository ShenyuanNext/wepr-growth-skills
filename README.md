# WEPR Growth Skills

[中文](#中文说明) · [English](#english)

An open collection of practical Agent Skills for public relations, digital analytics, paid media, SEO/GEO, creator research, Xiaohongshu operations, editorial illustration, community marketing, and international growth.

一套面向公关、数字营销、广告投放、SEO/GEO、小红书运营、内容研究、编辑插画、社区营销和品牌出海的可执行 Agent Skills。

---

## 中文说明

### 项目简介

`wepr-growth-skills` 是 WEPR 建设并持续维护的开放式增长技能库。它把公关、品牌、数据分析、广告投放、SEO/GEO、社区增长、内容运营和视觉生产中的真实执行方法，整理为可以被 Codex、Claude Code 及其他兼容 Agent 调用的独立技能。

仓库不是提示词合集。每个技能都包含明确触发场景、执行流程、交付结构、条件性参考资料和风险边界，可单独调用，也可以组合成完整客户工作流。

这些技能强调：

- 先诊断问题，再选择渠道和服务；
- 先验证事实和数据，再给出判断；
- 输出动作、负责人、周期、指标和风险边界；
- 不用虚假互动、垃圾外链和平台规避换取短期数据；
- 不承诺无法控制的排名、爆款、推荐或销售结果。

### 能力架构

```text
业务与品牌判断
├── analyze-brand-strategy
├── audit-digital-growth
└── diagnose-pr-crisis

增长规划与获客
├── plan-paid-media
├── plan-organic-growth
└── plan-xiaohongshu-growth

内容生产与账号运营
├── launch-content-account
├── distill-creator-playbook
├── create-marketing-content
└── plan-editorial-illustrations
```

每项技能都遵循同一条主线：`目标 → 证据 → 判断 → 动作 → 负责人 → 指标 → 复盘 → 风险`。

### 技能目录

| 技能 | 中文名称 | 适用场景 | 主要输出 |
| --- | --- | --- | --- |
| `diagnose-pr-crisis` | 公关与危机诊断 | 舆情、声明、负面事件、媒体采访、海外危机 | 时间线、利益相关者、风险分级、回应策略、声明、Q&A、恢复计划 |
| `audit-digital-growth` | 数字营销增长诊断 | GA4/GTM、漏斗、转化、归因、CRM、留存 | 指标树、数据审计、漏斗、假设、实验、看板和90天路线图 |
| `plan-paid-media` | 全域广告投放规划 | 百度、360、Microsoft Ads、抖音、小红书、视频号 | 平台组合、账户结构、测试矩阵、预算、诊断、复盘和风险控制 |
| `plan-organic-growth` | 出海有机增长规划 | SEO、GEO、Reddit、Product Hunt、SaaS冷启动、内容增长 | 需求证据、渠道地图、SEO/GEO审计、社区与发布方案、实验和90天路线图 |
| `plan-xiaohongshu-growth` | 小红书搜索与内容增长 | 标题、关键词、图文笔记、周更计划、账号诊断 | 搜索意图、双标题、发布正文、内容日历、诊断与自然咨询路径 |
| `distill-creator-playbook` | 创作者内容蒸馏 | 博主拆解、对标账号、内容模式研究 | 样本账本、定位、选题、结构、证据强度和原创执行手册 |
| `plan-editorial-illustrations` | 编辑插画规划 | 文章配图、小红书配图、公众号插画、提示词与质检 | 配图地图、镜头清单、生成提示词、替代文本和视觉质检 |
| `analyze-brand-strategy` | 品牌战略分析 | 品牌定位、年轻化、渠道、竞争、品牌出海 | 证据账本、品牌诊断、战略选项、执行与验证路线图 |
| `create-marketing-content` | 营销内容创作 | 公众号、品牌内容、案例、观点、跨平台改写 | 素材账本、内容结构、成稿、标题和编辑质检 |
| `launch-content-account` | 内容账号冷启动 | 公众号、抖音、视频号、X、小红书起号与诊断 | 账号承诺、主页、内容支柱、样本实验、复盘和路线图 |

### 如何选择

- 发生负面事件、需要声明或媒体沟通：使用 `$diagnose-pr-crisis`。
- 有流量但不知道哪里出了问题：使用 `$audit-digital-growth`。
- 准备花媒体预算获客：使用 `$plan-paid-media`。
- 希望通过搜索、AI搜索、社区和内容长期获客：使用 `$plan-organic-growth`。
- 要写、改或诊断小红书内容：使用 `$plan-xiaohongshu-growth`。
- 要从公开账号提炼可复用方法：使用 `$distill-creator-playbook`。
- 要把文章转成统一的配图系统：使用 `$plan-editorial-illustrations`。
- 要诊断品牌价值、定位、竞争或出海路径：使用 `$analyze-brand-strategy`。
- 要把业务素材写成可信的多平台内容：使用 `$create-marketing-content`。
- 要从零启动或修复一个内容账号：使用 `$launch-content-account`。
- 一个项目可以组合多个技能。例如先用增长诊断明确问题，再分别制定付费与有机增长计划。

### 安装

克隆仓库：

```bash
git clone https://github.com/ShenyuanNext/wepr-growth-skills.git
```

安装全部技能到 Codex：

```bash
cp -R wepr-growth-skills/skills/* ~/.codex/skills/
```

安装单个技能到 Codex：

```bash
cp -R wepr-growth-skills/skills/plan-organic-growth ~/.codex/skills/
```

安装到通用 Agent 技能目录：

```bash
cp -R wepr-growth-skills/skills/plan-organic-growth ~/.agents/skills/
```

也可以复制整个 `skills/` 下的所有目录。重新启动或刷新 Agent 后即可发现技能。

完整使用方法、输入要求、输出结构和组合工作流见[中文使用手册](docs/USAGE.zh-CN.md)。

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

```text
使用 $plan-xiaohongshu-growth，把这个选题写成图文笔记：给2个20字内标题、正文、关键词和自然咨询钩子。
```

```text
使用 $distill-creator-playbook，拆解这3个公开账号最近30篇内容，标注证据强度并输出原创的30天执行手册。
```

```text
使用 $plan-editorial-illustrations，为这篇文章设计6张统一风格配图，先给镜头清单和生成提示词。
```

```text
使用 $analyze-brand-strategy，分析这个品牌的定位、渠道、竞争与年轻化路径，给出三个战略选项和验证计划。
```

```text
使用 $create-marketing-content，把这些项目资料写成一篇有证据、有判断、可发布的公众号文章。
```

```text
使用 $launch-content-account，为WEPR设计视频号从0到1冷启动方案，包括主页、内容支柱、首轮样本和复盘指标。
```

### 推荐组合工作流

#### 客户增长诊断与方案

1. `$audit-digital-growth` 定义业务问题、指标和数据缺口；
2. `$analyze-brand-strategy` 判断品牌价值、竞争位置和客户选择理由；
3. `$plan-paid-media` 设计可控的付费获客实验；
4. `$plan-organic-growth` 建立SEO、GEO、社区与长期内容资产；
5. 汇总为统一的30/60/90天路线图。

#### 小红书内容与获客

1. `$distill-creator-playbook` 分析公开对标样本；
2. `$plan-xiaohongshu-growth` 规划搜索意图、关键词、标题和正文；
3. `$plan-editorial-illustrations` 设计统一配图；
4. `$launch-content-account` 管理发布样本、复盘和账号迭代。

#### 品牌危机与恢复

1. `$diagnose-pr-crisis` 统一事实、声明、媒体和行动；
2. `$audit-digital-growth` 监测搜索、网站、线索和客户变化；
3. `$create-marketing-content` 生产事实页、FAQ、说明与恢复内容；
4. `$plan-organic-growth` 建设长期可信信源和品牌发现资产。

### 技能目录结构

```text
skills/<skill-name>/
├── SKILL.md              # 触发条件、核心流程、输出与风险边界
├── agents/openai.yaml    # Agent界面名称、简介和默认调用提示
└── references/           # 按具体任务读取的详细方法与检查表
```

详细输入模板、逐项调用方式、组合流程和验收标准见[中文使用手册](docs/USAGE.zh-CN.md)。参考来源与许可见[来源说明](docs/SOURCES.md)。

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

`wepr-growth-skills` is an open, continuously maintained collection built by WEPR. It turns practical work in PR, brand strategy, analytics, media buying, SEO/GEO, community growth, content operations, and visual production into modular Agent Skills for Codex, Claude Code, and compatible agents.

This is not a prompt collection. Each skill defines triggering contexts, an execution workflow, deliverables, conditionally loaded references, and risk boundaries. Skills can operate independently or combine into a client-ready workflow.

### Capability architecture

```text
Business and brand decisions
├── analyze-brand-strategy
├── audit-digital-growth
└── diagnose-pr-crisis

Growth planning and acquisition
├── plan-paid-media
├── plan-organic-growth
└── plan-xiaohongshu-growth

Content production and account operations
├── launch-content-account
├── distill-creator-playbook
├── create-marketing-content
└── plan-editorial-illustrations
```

Every skill follows the same operating line: `objective → evidence → judgment → action → owner → metric → review → risk`.

### Included skills

| Skill | Purpose | Typical use cases | Core deliverables |
| --- | --- | --- | --- |
| `diagnose-pr-crisis` | PR and crisis response | Controversies, negative sentiment, statements, interviews, reputation recovery | Timeline, stakeholder map, risk grade, response plan, statement, Q&A, recovery roadmap |
| `audit-digital-growth` | Digital growth analytics | GA4/GTM, funnels, conversion, attribution, CRM, retention | Metric tree, tracking audit, funnel, hypotheses, experiments, dashboard, 90-day roadmap |
| `plan-paid-media` | Paid-media planning | Search ads, Douyin, Xiaohongshu, WeChat Channels, multi-platform acquisition | Channel roles, account structure, test matrix, budget, diagnostics, review system |
| `plan-organic-growth` | Organic international growth | SEO, GEO/AI search, Reddit, Product Hunt, SaaS launch, content systems | Demand evidence, channel map, SEO/GEO audit, community and launch plans, experiments, roadmap |
| `plan-xiaohongshu-growth` | Xiaohongshu search and content | Titles, keywords, image-text posts, calendars, account diagnosis | Search intent, title options, publishing copy, calendar, diagnosis, consultation path |
| `distill-creator-playbook` | Creator-pattern distillation | Creator research, benchmark accounts, content-pattern analysis | Sample ledger, positioning, structures, evidence strength, original playbook |
| `plan-editorial-illustrations` | Editorial illustration planning | Article visuals, social illustrations, prompts, visual QA | Placement map, shot list, prompts, alt text, QA findings |
| `analyze-brand-strategy` | Brand strategy analysis | Positioning, youth strategy, channels, competition, international expansion | Evidence ledger, diagnosis, strategic options, activation roadmap |
| `create-marketing-content` | Marketing content creation | Articles, brand content, cases, thought leadership, adaptation | Source ledger, structure, final copy, headlines, editorial QA |
| `launch-content-account` | Content-account launch | WeChat, Douyin, WeChat Channels, X, and Xiaohongshu launches | Account promise, profile, pillars, experiments, reviews, roadmap |

### Choosing a skill

- Use `$diagnose-pr-crisis` when the business needs a response, statement, media plan, or reputation recovery.
- Use `$audit-digital-growth` when performance is unclear or traffic, conversion, attribution, and retention disagree.
- Use `$plan-paid-media` when the team is preparing to spend media budget and needs a measurable acquisition system.
- Use `$plan-organic-growth` when growth should compound through search, AI search, community participation, launches, and content.
- Use `$plan-xiaohongshu-growth` to plan, write, rewrite, or diagnose Xiaohongshu content.
- Use `$distill-creator-playbook` to turn public creator content into an evidence-tagged original playbook.
- Use `$plan-editorial-illustrations` to translate an article into a coherent illustration system.
- Use `$analyze-brand-strategy` to diagnose positioning, customer value, competition, or international expansion.
- Use `$create-marketing-content` to turn business evidence into credible platform-native content.
- Use `$launch-content-account` to launch or repair a content account through comparable experiments and business signals.
- Combine skills when appropriate. A growth audit can define the problem before separate paid and organic plans are built.

### Installation

Clone the repository:

```bash
git clone https://github.com/ShenyuanNext/wepr-growth-skills.git
```

Install all skills for Codex:

```bash
cp -R wepr-growth-skills/skills/* ~/.codex/skills/
```

Install one skill for Codex:

```bash
cp -R wepr-growth-skills/skills/plan-organic-growth ~/.codex/skills/
```

Install it in a shared Agent Skills directory:

```bash
cp -R wepr-growth-skills/skills/plan-organic-growth ~/.agents/skills/
```

You may copy every folder under `skills/`. Restart or refresh the agent environment after installation.

See the [English usage guide](docs/USAGE.en.md) for inputs, outputs, operating modes, and combined workflows.

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

```text
Use $plan-xiaohongshu-growth to turn this topic into a searchable image-text post with two titles, final copy, keywords, and a natural consultation path.
```

```text
Use $distill-creator-playbook to analyze 30 public posts from these accounts and build an evidence-tagged, original 30-day playbook.
```

```text
Use $plan-editorial-illustrations to design six coherent article illustrations, starting with a shot list and generation prompts.
```

```text
Use $analyze-brand-strategy to evaluate this brand's positioning, channels, competition, and youth strategy, then provide three strategic options and a validation plan.
```

```text
Use $create-marketing-content to turn these project materials into an evidence-based, publishable thought-leadership article.
```

```text
Use $launch-content-account to design a WeChat Channels launch for WEPR, including the profile, content pillars, initial sample, and review metrics.
```

### Recommended combined workflows

#### Client growth diagnosis and plan

1. Use `$audit-digital-growth` to define the business problem, metrics, and data gaps.
2. Use `$analyze-brand-strategy` to clarify customer value, competitive position, and reasons for choice.
3. Use `$plan-paid-media` for controlled acquisition tests.
4. Use `$plan-organic-growth` for SEO, GEO, community, and compounding content assets.
5. Consolidate owners and reviews into one 30/60/90-day roadmap.

#### Xiaohongshu content and acquisition

1. Use `$distill-creator-playbook` to study public benchmark samples.
2. Use `$plan-xiaohongshu-growth` for search intent, keywords, titles, and copy.
3. Use `$plan-editorial-illustrations` for a coherent visual system.
4. Use `$launch-content-account` to manage publishing samples, reviews, and account iteration.

#### Crisis response and recovery

1. Use `$diagnose-pr-crisis` to unify facts, response, media, and operations.
2. Use `$audit-digital-growth` to monitor search, site, lead, and customer changes.
3. Use `$create-marketing-content` to produce fact pages, FAQs, explanations, and recovery content.
4. Use `$plan-organic-growth` to build durable trusted sources and brand-discovery assets.

### Skill structure

```text
skills/<skill-name>/
├── SKILL.md              # Triggers, workflow, outputs, and boundaries
├── agents/openai.yaml    # UI metadata and default invocation
└── references/           # Detailed methods loaded only when relevant
```

See the [English usage guide](docs/USAGE.en.md) for input templates, individual modes, combined workflows, and acceptance criteria. See [sources and acknowledgements](docs/SOURCES.md) for provenance and licensing.

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
