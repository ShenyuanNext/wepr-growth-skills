# WEPR Growth Skills

[中文](#中文说明) · [English](#english)

WEPR's open, evidence-led Agent Skills system for business diagnosis, brand strategy, public relations, digital analytics, cross-platform advertising, complete SEO/GEO and authority-building delivery, natural Chinese writing, content and account operations, client proposals, presentations, and international growth.

WEPR 开放式、证据驱动的增长 Agent Skills 系统，覆盖商业诊断、品牌战略、公关传播、数字分析、跨平台广告投放、完整 SEO/GEO 与链接权威建设、自然中文写作、内容与账号运营、客户方案、演示文档和品牌出海。

---

## 中文说明

### 项目简介

`wepr-growth-skills` 是 WEPR 建设并持续维护的开放式增长执行系统。它把品牌、公关、数据、投放、SEO/GEO、内容、账号运营、报价和演示中的真实方法，整理为 Codex、Claude Code 及其他兼容 Agent 可调用的完整工作流。技能既能完成单项诊断和生产，也能组合成从研究、策略、报价、执行到复盘的客户交付链路。更多服务与案例见 [WEPR 官网](https://www.scwepr.com/)。

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
├── wepr-client-discovery（客户访谈、需求澄清、问卷与交接）
├── wepr-business-workbench（商业问题、目标、决策与客户策略）
├── wepr-market-signal-research（公开用户反馈、需求信号与传播洞察）
├── analyze-brand-strategy（证据化定位、差异化与品牌战略）
├── audit-digital-growth
├── pr-strategy-workbench（公关方案、传播决策与公共文案）
└── diagnose-pr-crisis

增长规划与获客
├── plan-paid-media
├── wepr-advertising-workbench（跨平台广告审计、创意、归因与优化）
├── plan-organic-growth
├── wepr-seo（完整 SEO：快速/深度审计、策略、实施与验证）
├── wepr-link-authority-workbench（链接、品牌提及、数字公关与权威建设）
├── operate-georank-workbench（GEOrank 安全操作与交付回执）
└── plan-xiaohongshu-growth

内容生产与账号运营
├── launch-content-account
├── distill-creator-playbook
├── create-marketing-content
├── wepr-marketing（客户营销方案、传播与文案）
├── wepr-editorial-quality（文稿质量审计、最小改写与作者声纹保护）
├── wepr-human-writing（自然中文写作与客户终稿润色）
├── wepr-presentation-workbench（PPTX 与 HTML 演示文档统一入口）
├── wepr-slides（单文件交互式演示文档）
├── plan-editorial-illustrations
└── Xiaohongshu Workbench
    ├── xiaohongshu-suite
    ├── xiaohongshu-profile
    ├── xiaohongshu-topic-planner
    ├── xiaohongshu-title
    ├── xiaohongshu-comment-reply
    └── xiaohongshu-conversion-path
```

每项技能都遵循同一条主线：`目标 → 证据 → 判断 → 动作 → 负责人 → 指标 → 复盘 → 风险`。

### 技能治理与调用原则

- **总入口负责路由：** 跨模块项目先使用总入口，明确单项任务则直接调用专项技能，避免重复加载。
- **专项技能保持单一职责：** 策略、生产、执行、监测和归因分别处理，不用一个大而全的入口替代专业判断。
- **底层执行器不与总入口竞争：** 例如 `$wepr-presentation-workbench` 负责演示需求判断与统一交付，`$wepr-slides` 只负责已明确的单文件交互式 HTML 路线。
- **旧能力并入完整版：** GEOFlow 的开发、运行操作、前端主题、渠道站点和旧模板迁移统一由 `$wepr-geoflow` 承接；已有文章的 GEO 改造统一由 `$wepr-geo-content-refiner` 承接。
- **定期清理重复入口：** 删除仅保留旧名称、与完整版高度重合或不再具备独立调用价值的技能；Git 历史保留恢复能力。
- **只保留交付所需信息：** 技能正文和示例不承担外部项目推广，不保留上游仓库名称、来源链接或许可证副本；仓库自身的授权信息仅由根目录文件统一管理。

### GEO 专业能力包

仓库现已新增 `$wepr-geo-suite` 作为 WEPR GEO 项目总入口，覆盖从策略诊断到执行监测的完整工作流：

- GEO 全景诊断、意图拓词、30/60/90 天执行路线图；
- 品牌知识库、事实卡、实体关系图谱与证据治理；
- 页面审计、页面蓝图、标题、科普、对比、榜单和文章改造；
- DeepSeek、豆包、ChatGPT 合规重复采样与可审计报告；
- AI 答案、引用源、品牌事实、转化归因和月度监测；
- GEO 工作台的开发、CLI/API/后台操作、企业知识库、人工发布工单、主题、渠道站点和旧模板迁移；
- 基于已核验系统能力形成客户实施方案、传播执行规划和内容生产简报。

推荐从 `$wepr-geo-suite` 开始。它会按目标、证据状态、平台、周期和交付物路由到所需专项技能，避免一次加载全部能力；涉及 GEO 工作台开发、运营或系统承接方案时使用 `$wepr-geoflow`。当前技能基线已适配 GEOFlow v2.3.0 与 CLI 0.2.0，具体实例仍以现场发现结果为准。

### 技能目录

| 技能 | 中文名称 | 适用场景 | 主要输出 |
| --- | --- | --- | --- |
| `wepr-client-discovery` | 客户需求澄清工作台 | 方案前访谈、启动会、异步问卷、多人决策、会议纪要和跨人员交接 | 需求简报、决策树、问题前沿、问卷、未决项和交接文档 |
| `wepr-business-workbench` | 商业策略工作台 | 商业问题澄清、模式诊断、对标、客户方案、传播与内容前置判断、长期决策 | 问题说明书、证据账本、商业诊断、策略简报、验证计划和决策记录 |
| `wepr-market-signal-research` | 市场信号研究工作台 | 公开评论、社区、问答、发布平台和竞品反馈中的需求、痛点、异议与语言研究 | 研究设计、证据账本、机会卡、传播洞察和验证计划 |
| `diagnose-pr-crisis` | 公关与危机诊断 | 舆情、声明、负面事件、媒体采访、海外危机 | 时间线、利益相关者、风险分级、回应策略、声明、Q&A、恢复计划 |
| `pr-strategy-workbench` | 公关策略工作台 | 客户公关方案、传播决策、媒体叙事、上线预案、公共文案和新闻稿 | 事实底稿、利益相关者、行动取舍、信息架构、30/60/90 路线图与成品内容 |
| `audit-digital-growth` | 数字营销增长诊断 | GA4/GTM、漏斗、转化、归因、CRM、留存 | 指标树、数据审计、漏斗、假设、实验、看板和 90 天路线图 |
| `plan-paid-media` | 全域广告投放规划 | 百度、360、Microsoft Ads、抖音、小红书、视频号 | 平台组合、账户结构、测试矩阵、预算、诊断、复盘和风险控制 |
| `wepr-advertising-workbench` | 广告策略工作台 | 跨平台媒体方案、账户审计、预算归因、创意文案、实验、监测和优化 | 证据账本、客户方案、审计报告、创意简报、实验与变更草案 |
| `plan-organic-growth` | 出海有机增长规划 | SEO、GEO、Reddit、Product Hunt、SaaS 冷启动、内容增长 | 需求证据、渠道地图、SEO/GEO 审计、社区与发布方案、实验和 90 天路线图 |
| `wepr-seo` | 完整 SEO 工作台 | 快速/深度页面审计、技术 SEO、关键词内容、国际化、电商、迁移、流量诊断、AI 搜索 | HTML 审计报告、覆盖台账、页面地图、优先级、实施验证与机器可读审计 |
| `wepr-link-authority-workbench` | 链接与权威建设工作台 | 外链和品牌提及审计、竞品差距、目录筛选、可链接资产、数字公关与合规触达 | 证据基线、机会分层、资产计划、个性化触达、30/60/90 天路线图与监测 |
| `operate-georank-workbench` | GEOrank工作台操作 | 登录、网站诊断、方案对话、拓词、用量检查和管理员操作 | 权限识别、写操作预检、API 执行回执、资源 ID、风险与回滚说明 |
| `plan-xiaohongshu-growth` | 小红书搜索与内容增长 | 标题、关键词、图文笔记、周更计划、账号诊断 | 搜索意图、双标题、发布正文、内容日历、诊断与自然咨询路径 |
| `xiaohongshu-suite` | 小红书工作流路由 | 不确定先改主页、选题、标题、正文、评论还是转化 | 阻塞环节、技能选择、处理顺序和输入交接 |
| `xiaohongshu-profile` | 小红书主页诊断 | 简介、昵称、定位、信任材料、置顶笔记 | 第一眼判断、定位句、简介版本、置顶结构和下一步测试 |
| `xiaohongshu-topic-planner` | 小红书选题系统 | 选题池、系列、7/14/30天计划、周更排期 | 内容支柱、意图、证据需求、日历、复用与学习目标 |
| `xiaohongshu-title` | 小红书标题工作台 | 标题生成、诊断、选择、封面短句 | 多角度标题、首推版本、关键词与承诺风险检查 |
| `xiaohongshu-comment-reply` | 小红书评论运营 | 回复评论、置顶评论、质疑与高风险评论 | 评论分类、自然回复、替代语气、升级处理建议 |
| `xiaohongshu-conversion-path` | 小红书转化路径 | 内容到主页、私信、咨询、体验、购买与复访 | 阶段路径、阻力、内容分工、筛选问题、指标与交付风险 |
| `distill-creator-playbook` | 创作者内容蒸馏 | 博主拆解、对标账号、内容模式研究 | 样本账本、定位、选题、结构、证据强度和原创执行手册 |
| `plan-editorial-illustrations` | 编辑插画规划 | 文章配图、小红书配图、公众号插画、提示词与质检 | 配图地图、镜头清单、生成提示词、替代文本和视觉质检 |
| `analyze-brand-strategy` | 证据化品牌定位与战略 | 品牌定位、差异化、再定位、年轻化、竞争与品牌出海 | 就绪门槛、五类竞争参照、D6优势诊断、定位方案、反证条件与验证路线图 |
| `create-marketing-content` | 营销内容创作 | 公众号、品牌内容、案例、观点、跨平台改写 | 素材账本、内容结构、成稿、标题和编辑质检 |
| `wepr-marketing` | 营销策略工作台 | 客户方案、传播策略、获客路径、发布计划、转化文案 | ICP、定位、渠道优先级、30/60/90 路线图、KPI 与成品文案 |
| `wepr-editorial-quality` | 文稿质量工作台 | 方案、传播、公关、广告和品牌内容的机械表达诊断、最小改写与声纹保护 | 问题证据表、完整改写稿、变更说明与事实风险提示 |
| `wepr-human-writing` | 自然中文写作 | 客户方案、传播稿、品牌文章、营销文案和终稿润色 | 素材缺口、自然中文成稿、机械表达诊断与事实风险提示 |
| `wepr-presentation-workbench` | 演示文档工作台 | 客户方案、传播提案、商业计划、报价、复盘、培训和发布会的 PPTX 或 HTML 制作 | 叙事结构、页面计划、可编辑成品、演讲备注与逐页质检 |
| `wepr-slides` | 交互式演示文档 | 客户方案、报价展示、策略汇报、季度复盘、浏览器演示 | 单文件 `.bento.html`、图表、Morph、状态页、动效和演讲备注 |
| `launch-content-account` | 内容账号冷启动 | 公众号、抖音、视频号、X、小红书起号与诊断 | 账号承诺、主页、内容支柱、样本实验、复盘和路线图 |

### 如何选择

- 客户需求模糊、关键问题未回答、需要访谈或向客户补材料：使用 `$wepr-client-discovery`。
- 商业问题还没说清，或需要先判断目标、模式、对标、取舍和验证路径：使用 `$wepr-business-workbench`。
- 要从公开用户反馈、社区讨论、评论和发布平台中寻找真实需求、痛点、异议和传播语言：使用 `$wepr-market-signal-research`。
- 发生负面事件、需要声明或媒体沟通：使用 `$diagnose-pr-crisis`。
- 要做客户公关方案、传播决策、媒体叙事分析、上线预案、公共文案审校或新闻稿：使用 `$pr-strategy-workbench`；正在发生的危机仍使用 `$diagnose-pr-crisis`。
- 有流量但不知道哪里出了问题：使用 `$audit-digital-growth`。
- 准备花媒体预算获客：使用 `$plan-paid-media`。
- 要做跨平台广告账户审计、归因对齐、广告创意与文案、实验、监测或有安全门禁的优化草案：使用 `$wepr-advertising-workbench`。涉及中国平台的具体准入、账户和投放规则时，同时使用 `$plan-paid-media`。
- 希望通过搜索、AI 搜索、社区和内容长期获客：使用 `$plan-organic-growth`。
- 所有 SEO任务统一使用 `$wepr-seo`：可自动选择快速页面审计、包含 PageSpeed 的深度审计、站点策略、关键词内容、迁移、国际化、电商或 AI 搜索模式。
- 要审计外链和品牌提及、筛选高质量目录与资源、规划可链接资产、数字公关或合规触达：使用 `$wepr-link-authority-workbench`。
- 已部署 GEOrank，需要执行诊断、拓词、方案对话或后台操作：使用 `$operate-georank-workbench`。一般 GEO 策略仍使用 `$plan-organic-growth`。
- 要写、改或诊断小红书内容：使用 `$plan-xiaohongshu-growth`。
- 不确定小红书任务应从哪里开始：使用 `$xiaohongshu-suite`；明确是主页、选题、标题、评论或转化时，直接使用对应的 `$xiaohongshu-*` 专项技能。
- 要从公开账号提炼可复用方法：使用 `$distill-creator-playbook`。
- 要把文章转成统一的配图系统：使用 `$plan-editorial-illustrations`。
- 要诊断品牌价值、定位、差异化、竞争或出海路径：使用 `$analyze-brand-strategy`。它会先检查研究资料是否足够，再区分直接竞品、间接替代、现状、不行动和心智标杆。
- 要把业务素材写成可信的多平台内容：使用 `$create-marketing-content`。
- 要形成客户营销方案、传播策略、早期获客计划或转化文案：使用 `$wepr-marketing`。
- 要检查文稿中的机械表达、空泛判断、模板化节奏和证据风险，或在保留作者个人语气的前提下做最小改写：使用 `$wepr-editorial-quality`。它不判断文本是否由 AI 创作。
- 要在不改变事实、数据和承诺的前提下，让方案、传播稿或营销文案更自然、更符合中文阅读习惯：使用 `$wepr-human-writing`。策略和内容结构尚未确定时，先使用对应的营销、公关或内容技能。
- 要制作、重构或审校可编辑 PPTX 或单文件 HTML 演示，并处理叙事、客户模板、图表、演讲备注和逐页质检：使用 `$wepr-presentation-workbench`。
- 要把方案、报价或报告制作成可直接在浏览器演示的单文件演示文档：使用 `$wepr-slides`。
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
使用 $wepr-client-discovery，把这次客户沟通整理成需求简报，列出已经确认的事实、必须由客户决定的问题、证据缺口、审批人和下一步。
```

```text
使用 $wepr-market-signal-research，研究目标用户在公开社区和评论区如何描述这个问题，建立可回查证据账本，并输出需求、痛点、异议、传播语言和验证计划。
```

```text
使用 $wepr-business-workbench，把这个模糊的客户需求整理成问题说明书，比较三种商业解释，只推荐一个当前方向，并给出反证条件和最小验证计划。
```

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
使用 $wepr-advertising-workbench，基于这份账户导出和CRM数据审计广告表现，分开账户健康、证据覆盖与合规风险，并输出预算、创意、归因和实验建议。
```

```text
使用 $plan-organic-growth，为一个新 SaaS制定 SEO、GEO、Reddit和Product Hunt 的90 天冷启动计划。
```

```text
使用 $wepr-link-authority-workbench，审计品牌现有链接与无链接提及，筛选高质量机会，并输出可链接资产、数字公关、个性化触达和季度监测计划。
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
使用 $wepr-human-writing，在不改变报价、服务范围和事实的前提下，把这份客户方案改成自然、可信、符合中国人阅读习惯的中文。
```

```text
使用 $wepr-presentation-workbench，把这份客户方案和报价表制作成可编辑 PPTX，先给页面计划，再完成图表、演讲备注和逐页视觉质检。
```

```text
使用 $wepr-editorial-quality，先指出这份传播稿中可核验的机械表达、空泛判断和证据风险，再在保留作者语气与全部事实的前提下完成最小改写。
```

```text
使用 $analyze-brand-strategy，分析这个品牌的定位、渠道与竞争。先检查研究就绪度，建立五类竞争参照和 D6优势诊断，再比较三套方向、只推荐一套，并给出反证条件和 90 天验证计划。
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
5. 汇总为统一的 30/60/90 天路线图。

#### 小红书内容与获客

1. `$distill-creator-playbook` 分析公开对标样本；
2. `$xiaohongshu-suite` 找到最早的阻塞环节；
3. `$xiaohongshu-profile` 和 `$xiaohongshu-topic-planner` 完成主页承接与选题系统；
4. `$xiaohongshu-title` 和 `$plan-xiaohongshu-growth` 完成标题、关键词与正文；
5. `$xiaohongshu-comment-reply` 和 `$xiaohongshu-conversion-path` 承接评论、咨询与转化；
6. `$plan-editorial-illustrations` 设计统一配图，`$launch-content-account` 管理发布样本和复盘。

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

详细输入模板、逐项调用方式、组合流程和验收标准见[中文使用手册](docs/USAGE.zh-CN.md)。

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

`wepr-growth-skills` is an open, continuously maintained collection built by WEPR. It turns practical work in PR, brand strategy, analytics, media buying, SEO/GEO, community growth, content operations, and visual production into modular Agent Skills for Codex, Claude Code, and compatible agents. Learn more about WEPR's services and work on the [official WEPR website](https://www.scwepr.com/).

This is not a prompt collection. Each skill defines triggering contexts, an execution workflow, deliverables, conditionally loaded references, and risk boundaries. Skills can operate independently or combine into a client-ready workflow.

### GEO capability pack

The repository provides `$wepr-geo-suite` as the WEPR orchestration entrypoint for complete GEO delivery. It covers panorama audits, intent mining, evidence-backed knowledge assets, page and content production, compliant platform sampling, answer and citation monitoring, attribution, execution roadmaps, and GEO workbench delivery. Use `$wepr-geoflow` for workbench development, operations, system-backed client plans, enterprise knowledge, manual-publication workflows, themes, and channel delivery. Its current baseline covers GEOFlow v2.3.0 and CLI 0.2.0; each target instance must still be discovered and verified.

### Capability architecture

```text
Business and brand decisions
├── wepr-client-discovery (client interviews, requirements, questionnaires, and handoffs)
├── wepr-business-workbench (business diagnosis, decisions, and client strategy)
├── wepr-market-signal-research (public feedback, demand signals, and communication insight)
├── analyze-brand-strategy (evidence-aware positioning and brand strategy)
├── audit-digital-growth
├── pr-strategy-workbench (PR plans, communication decisions, and public copy)
└── diagnose-pr-crisis

Growth planning and acquisition
├── plan-paid-media
├── wepr-advertising-workbench (cross-platform audit, creative, attribution, and optimization)
├── plan-organic-growth
├── wepr-seo (complete SEO: quick/full audits, strategy, implementation, verification)
├── wepr-link-authority-workbench (links, mentions, digital PR, and authority building)
├── operate-georank-workbench (safe GEOrank operations)
└── plan-xiaohongshu-growth

Content production and account operations
├── launch-content-account
├── distill-creator-playbook
├── create-marketing-content
├── wepr-marketing (client plans, communications, and copy)
├── wepr-editorial-quality (editorial diagnosis, minimal revision, and voice preservation)
├── wepr-human-writing (natural Chinese writing and final revision)
├── wepr-presentation-workbench (unified PPTX and HTML presentation delivery)
├── wepr-slides (single-file interactive presentations)
├── plan-editorial-illustrations
└── Xiaohongshu Workbench
    ├── xiaohongshu-suite
    ├── xiaohongshu-profile
    ├── xiaohongshu-topic-planner
    ├── xiaohongshu-title
    ├── xiaohongshu-comment-reply
    └── xiaohongshu-conversion-path
```

Every skill follows the same operating line: `objective → evidence → judgment → action → owner → metric → review → risk`.

### Skill governance and routing

- **Orchestrators route cross-module work:** use a suite for an unclear or multi-stage project and call a specialist directly for a defined task.
- **Specialists keep one responsibility:** strategy, production, execution, monitoring, and attribution remain distinct.
- **Execution routes do not compete with orchestrators:** `$wepr-presentation-workbench` owns presentation planning and format selection; `$wepr-slides` owns only the explicitly selected single-file interactive HTML route.
- **Legacy capabilities live in the complete workbench:** `$wepr-geoflow` covers development, operations, frontend themes, channel sites, and legacy migration; `$wepr-geo-content-refiner` owns GEO refinement of existing articles and pages.
- **Redundant entrypoints are removed regularly:** a skill is retired when it is only an old name, substantially duplicates a complete workbench, or no longer has an independent routing purpose. Git history remains the recovery path.
- **Only delivery-relevant information remains:** skills and examples do not promote external projects or retain upstream repository names, source links, or copied license files. Repository-level licensing is managed only at the root.

### Included skills

| Skill | Purpose | Typical use cases | Core deliverables |
| --- | --- | --- | --- |
| `wepr-client-discovery` | Client discovery workbench | Pre-proposal interviews, kickoffs, questionnaires, multi-owner decisions, meeting notes, handoffs | Requirements brief, decision tree, question frontier, questionnaire, open items, handoff |
| `wepr-business-workbench` | Business strategy workbench | Problem framing, business diagnosis, benchmarks, client strategy, communication and content briefs, long-term decisions | Problem statement, evidence ledger, diagnosis, strategy brief, validation plan, decision record |
| `wepr-market-signal-research` | Market-signal research workbench | Public reviews, communities, Q&A, launch platforms, competitor feedback, demand language | Research design, evidence ledger, opportunity cards, communication insight, validation plan |
| `diagnose-pr-crisis` | PR and crisis response | Controversies, negative sentiment, statements, interviews, reputation recovery | Timeline, stakeholder map, risk grade, response plan, statement, Q&A, recovery roadmap |
| `pr-strategy-workbench` | PR strategy workbench | Client PR plans, communication decisions, media narratives, launch-risk plans, public copy, press releases | Fact base, stakeholder map, action choice, message system, 30/60/90 roadmap, finished content |
| `audit-digital-growth` | Digital growth analytics | GA4/GTM, funnels, conversion, attribution, CRM, retention | Metric tree, tracking audit, funnel, hypotheses, experiments, dashboard, 90-day roadmap |
| `plan-paid-media` | Paid-media planning | Search ads, Douyin, Xiaohongshu, WeChat Channels, multi-platform acquisition | Channel roles, account structure, test matrix, budget, diagnostics, review system |
| `wepr-advertising-workbench` | Advertising strategy workbench | Cross-platform plans, account audits, budget and attribution, creative and copy, experiments, monitoring, optimization | Evidence ledger, client plan, audit, creative brief, experiment, guarded change draft |
| `plan-organic-growth` | Organic international growth | SEO, GEO/AI search, Reddit, Product Hunt, SaaS launch, content systems | Demand evidence, channel map, SEO/GEO audit, community and launch plans, experiments, roadmap |
| `wepr-seo` | Complete SEO workbench | Quick/full page audits, technical SEO, keyword/content systems, international, commerce, migrations, incidents, AI search | HTML audits, coverage ledger, page maps, priorities, implementation verification, machine-readable audits |
| `wepr-link-authority-workbench` | Link and authority workbench | Link and mention audits, competitor gaps, directory qualification, linkable assets, digital PR, compliant outreach | Evidence baseline, opportunity tiers, asset plan, personalized outreach, roadmap, monitoring |
| `operate-georank-workbench` | GEOrank operations | Login, diagnostics, solution chat, keyword expansion, usage, and authorized administration | Access detection, write preflight, API receipt, resource IDs, risk and rollback guidance |
| `plan-xiaohongshu-growth` | Xiaohongshu search and content | Titles, keywords, image-text posts, calendars, account diagnosis | Search intent, title options, publishing copy, calendar, diagnosis, consultation path |
| `xiaohongshu-suite` | Xiaohongshu workflow routing | Unclear whether to start with profile, topics, titles, copy, comments, or conversion | Blocked stage, skill selection, processing order, and input handoff |
| `xiaohongshu-profile` | Xiaohongshu profile audit | Bio, positioning, proof, pinned posts, profile acceptance | First-impression diagnosis, positioning, bio options, pinned-post plan |
| `xiaohongshu-topic-planner` | Xiaohongshu topic system | Topic pools, series, calendars, evidence planning | Pillars, intent, calendar, proof requirements, reuse, learning goals |
| `xiaohongshu-title` | Xiaohongshu title studio | Title generation, diagnosis, selection, cover lines | Distinct title angles, recommendation, keyword and promise-risk checks |
| `xiaohongshu-comment-reply` | Xiaohongshu comment operations | Replies, pinned comments, objections, high-risk comments | Classification, natural replies, alternatives, escalation advice |
| `xiaohongshu-conversion-path` | Xiaohongshu conversion path | Content to profile, inquiry, trial, purchase, and return | Stage map, friction, content jobs, qualification, metrics, delivery risks |
| `distill-creator-playbook` | Creator-pattern distillation | Creator research, benchmark accounts, content-pattern analysis | Sample ledger, positioning, structures, evidence strength, original playbook |
| `plan-editorial-illustrations` | Editorial illustration planning | Article visuals, social illustrations, prompts, visual QA | Placement map, shot list, prompts, alt text, QA findings |
| `analyze-brand-strategy` | Evidence-aware positioning and brand strategy | Positioning, differentiation, repositioning, competition, youth strategy, international expansion | Readiness gate, five-role competition set, D6 advantage test, options, falsification conditions, activation roadmap |
| `create-marketing-content` | Marketing content creation | Articles, brand content, cases, thought leadership, adaptation | Source ledger, structure, final copy, headlines, editorial QA |
| `wepr-marketing` | Founder marketing workbench | Client plans, communication strategy, early acquisition, launches, conversion copy | ICP, positioning, channel priorities, 30/60/90 roadmap, KPIs, finished copy |
| `wepr-editorial-quality` | Editorial quality workbench | Mechanical-pattern diagnosis, minimal revision, evidence checks, and author-voice preservation across client content | Evidence-tagged findings, full revision, change notes, fact-risk flags |
| `wepr-human-writing` | Natural Chinese writing | Client proposals, communication drafts, brand articles, marketing copy, final revision | Material gaps, natural Chinese copy, mechanical-writing diagnosis, fact-risk notes |
| `wepr-presentation-workbench` | Presentation workbench | PPTX or HTML proposals, plans, quotations, reviews, training, and launches | Narrative, slide plan, editable deck, speaker notes, rendered QA |
| `launch-content-account` | Content-account launch | WeChat, Douyin, WeChat Channels, X, and Xiaohongshu launches | Account promise, profile, pillars, experiments, reviews, roadmap |

### Choosing a skill

- Use `$wepr-client-discovery` when client requirements are vague, critical questions remain unanswered, or an interview, questionnaire, kickoff, or handoff is needed.
- Use `$wepr-business-workbench` when the commercial problem, objective, business model, benchmark, trade-off, or validation path must be clarified before channel execution.
- Use `$wepr-market-signal-research` to find evidence-backed needs, pains, objections, alternatives, and audience language in public feedback, communities, reviews, and launch platforms.
- Use `$diagnose-pr-crisis` when the business needs a response, statement, media plan, or reputation recovery.
- Use `$pr-strategy-workbench` for client PR plans, communication decisions, narrative analysis, pre-launch risk, public-copy review, or press releases; use `$diagnose-pr-crisis` for active incidents.
- Use `$audit-digital-growth` when performance is unclear or traffic, conversion, attribution, and retention disagree.
- Use `$plan-paid-media` when the team is preparing to spend media budget and needs a measurable acquisition system.
- Use `$wepr-advertising-workbench` for cross-platform account audits, attribution alignment, advertising creative and copy, experiments, monitoring, or safely gated optimization drafts. Pair it with `$plan-paid-media` when China-platform eligibility, account, or delivery rules are involved.
- Use `$plan-organic-growth` when growth should compound through search, AI search, community participation, launches, and content.
- Use `$wepr-seo` for every SEO task; it selects quick page audit, PageSpeed-enabled full audit, site strategy, keyword/content, migration, international, commerce, or AI-search mode.
- Use `$wepr-link-authority-workbench` to audit links and brand mentions, qualify directories and resources, plan linkable assets and digital PR, or prepare compliant personalized outreach.
- Use `$operate-georank-workbench` when a deployed GEOrank instance must be queried or changed. Use `$plan-organic-growth` for general GEO strategy.
- Use `$plan-xiaohongshu-growth` to plan, write, rewrite, or diagnose Xiaohongshu content.
- Use `$xiaohongshu-suite` when the blocked Xiaohongshu stage is unclear; use the matching `$xiaohongshu-*` specialist directly for profile, topics, titles, comments, or conversion.
- Use `$distill-creator-playbook` to turn public creator content into an evidence-tagged original playbook.
- Use `$plan-editorial-illustrations` to translate an article into a coherent illustration system.
- Use `$analyze-brand-strategy` to diagnose evidence-aware positioning, differentiation, competition, or international expansion. It checks readiness and covers direct competitors, indirect alternatives, the current workaround, inaction, and the mental benchmark.
- Use `$create-marketing-content` to turn business evidence into credible platform-native content.
- Use `$wepr-marketing` for client marketing plans, communication strategy, early acquisition, launch plans, or conversion copy.
- Use `$wepr-editorial-quality` to identify observable mechanical writing, generic claims, templated rhythm, or evidence risk, and to make the smallest useful revision while preserving the author's voice. It does not infer whether AI wrote the text.
- Use `$wepr-human-writing` to make Chinese proposals, communication drafts, and marketing copy sound natural without changing facts, data, scope, or promises. Use the relevant strategy or content skill first when the message and structure are not yet settled.
- Use `$wepr-presentation-workbench` to create, reconstruct, or audit editable PPTX or single-file HTML presentations with narrative planning, templates, charts, speaker notes, and rendered visual QA.
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
Use $wepr-client-discovery to turn this client conversation into a requirements brief with confirmed facts, client-owned decisions, evidence gaps, approvers, and next steps.
```

```text
Use $wepr-market-signal-research to study how target users describe this problem in public communities and reviews, build a traceable evidence ledger, and report needs, pains, objections, language, and validation steps.
```

```text
Use $wepr-business-workbench to turn this vague client request into a testable problem statement, compare three competing explanations, recommend one direction, and define falsification conditions and a minimum validation plan.
```

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
Use $wepr-advertising-workbench to audit these account exports and CRM outcomes, separate account health from evidence coverage and compliance risk, and produce budget, creative, attribution, and experiment recommendations.
```

```text
Use $plan-organic-growth to build a 90-day SEO, GEO, Reddit, and Product Hunt cold-start plan.
```

```text
Use $wepr-link-authority-workbench to audit current links and unlinked mentions, qualify opportunities, and produce a quarterly linkable-asset, digital-PR, personalized-outreach, and monitoring plan.
```

```text
Use $wepr-human-writing to revise this client proposal into natural Chinese without changing its facts, pricing, scope, or commitments.
```

```text
Use $wepr-presentation-workbench to turn this proposal and quotation sheet into an editable PPTX, starting with a slide plan and finishing with charts, speaker notes, and rendered slide-by-slide QA.
```

```text
Use $wepr-editorial-quality to identify observable mechanical patterns, generic claims, and evidence risks in this draft, then make the smallest useful revision while preserving its facts and the author's voice.
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
Use $analyze-brand-strategy to evaluate this brand's positioning, channels, and competition. Check research readiness, build the five-role competition set and D6 advantage test, compare three materially different directions, recommend one, and provide falsification conditions and a 90-day validation plan.
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
2. Use `$xiaohongshu-suite` to locate the earliest blocked stage.
3. Use `$xiaohongshu-profile` and `$xiaohongshu-topic-planner` for profile acceptance and the topic system.
4. Use `$xiaohongshu-title` and `$plan-xiaohongshu-growth` for titles, keywords, and final copy.
5. Use `$xiaohongshu-comment-reply` and `$xiaohongshu-conversion-path` for conversation and qualified next actions.
6. Use `$plan-editorial-illustrations` for visuals and `$launch-content-account` for publishing experiments and reviews.

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

See the [English usage guide](docs/USAGE.en.md) for input templates, individual modes, combined workflows, and acceptance criteria.

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
