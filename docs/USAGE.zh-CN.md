# WEPR Growth Skills 中文使用手册

## 1. 这套技能解决什么问题

这不是营销术语库，而是一组可组合的执行工作流。每项技能负责一类清晰决策：先确认业务目标和证据，再输出动作、负责人、验证指标和风险边界。

当前包含十六项公开技能：

| 技能 | 一句话用途 |
| --- | --- |
| `$diagnose-pr-crisis` | 处理舆情、声明、媒体沟通和声誉恢复 |
| `$audit-digital-growth` | 找出流量、转化、归因、CRM和留存问题 |
| `$plan-paid-media` | 设计并诊断搜索、短视频和社交广告投放 |
| `$plan-organic-growth` | 规划SEO、GEO、Reddit、Product Hunt和内容增长 |
| `$plan-xiaohongshu-growth` | 写作、重构、诊断小红书搜索型内容 |
| `$xiaohongshu-suite` | 判断小红书任务应先处理主页、选题、标题、正文、评论还是转化 |
| `$xiaohongshu-profile` | 诊断主页第一眼、简介、定位、信任材料和置顶笔记 |
| `$xiaohongshu-topic-planner` | 建立选题池、系列内容与7/14/30天日历 |
| `$xiaohongshu-title` | 生成、诊断、筛选和优化小红书标题与封面短句 |
| `$xiaohongshu-comment-reply` | 分类并回复评论、处理质疑、设计置顶评论 |
| `$xiaohongshu-conversion-path` | 设计内容、主页、私信、咨询、体验、购买和复访路径 |
| `$distill-creator-playbook` | 从公开账号提炼原创、可测试的内容方法 |
| `$plan-editorial-illustrations` | 把文章转成统一的配图镜头和生成提示词 |
| `$analyze-brand-strategy` | 分析品牌价值、定位、渠道、竞争和出海路径 |
| `$create-marketing-content` | 把业务证据写成可信、可发布的多平台内容 |
| `$launch-content-account` | 规划公众号、抖音、视频号、X和小红书的内容账号冷启动 |

## 2. 安装

```bash
git clone https://github.com/ShenyuanNext/wepr-growth-skills.git
```

安装全部技能到 Codex：

```bash
cp -R wepr-growth-skills/skills/* ~/.codex/skills/
```

安装到通用 Agent 目录：

```bash
cp -R wepr-growth-skills/skills/* ~/.agents/skills/
```

重新启动或刷新 Agent。不同客户端对 Agent Skills 的支持程度可能不同；至少需要能读取技能目录中的 `SKILL.md`。

## 3. 高质量请求的最小输入

建议同时给出：业务、目标用户、当前阶段、目标结果、可用素材或数据、时间范围、预算或资源、输出格式。缺少的信息会影响结论时，技能会先询问；不影响主方向时，会明确假设后继续。

推荐写法：

```text
使用 $技能名。
业务：
目标用户：
当前问题：
希望完成的决策或交付物：
现有证据/素材：
限制条件：
```

## 4. 各技能怎么用

### 公关与危机

```text
使用 $diagnose-pr-crisis。根据事件时间线、现有证据和评论样本，区分已确认、争议和未知事实，输出0–2小时、2–24小时、24–72小时行动，并起草声明和媒体Q&A。
```

重要输入：事件时间线、证据、已公开表态、相关方、法律或运营进展。不要用它承诺删稿、控评或操纵舆论。

### 数字增长诊断

```text
使用 $audit-digital-growth。网站流量上涨但有效询盘下降，请建立指标树，检查埋点、渠道、落地页和CRM回传，给出竞争假设与验证实验。
```

重要输入：指标定义、时间范围、渠道数据、漏斗数据、销售结果和数据缺口。平台归因不等于增量。

### 付费媒体

```text
使用 $plan-paid-media。为客单价、毛利和销售周期已知的B2B服务设计首月投放测试，包含账户结构、素材变量、预算、CPL上限、CRM回传和停投规则。
```

重要输入：价格、毛利、LTV、有效线索标准、销售承接能力、平台准入和预算。正式执行前核验平台最新政策。

### 有机增长

```text
使用 $plan-organic-growth。为新SaaS设计90天SEO、GEO、Reddit和Product Hunt计划，先给需求证据与渠道角色，再排实验优先级。
```

重要输入：产品、用户、竞争替代、现有网站和内容、目标市场、可投入人力。禁止购买Karma、投票或垃圾外链。

### 小红书搜索与内容

```text
使用 $plan-xiaohongshu-growth。主题是“B2B品牌怎么做GEO”，面向市场负责人，写一篇可直接执行的图文笔记。给2个20字内标题、正文、主辅关键词、收藏清单和自然咨询钩子，不要分页说明。
```

可选模式：单篇、周更日历、账号诊断、全文重构。它会先确定一个主搜索意图，再让标题承诺与正文交付一致；不会虚构搜索量、排名或案例结果。

### 小红书专项工作台

```text
使用 $xiaohongshu-suite。账号已经在更新，但主页、选题、标题、评论和咨询承接都有问题。请先判断最早的阻塞环节，再给处理顺序。
```

- 只改主页、简介、昵称或置顶：`$xiaohongshu-profile`。
- 只做选题池、系列和日历：`$xiaohongshu-topic-planner`。
- 只生成或优化标题：`$xiaohongshu-title`。
- 写完整正文、关键词和收藏清单：`$plan-xiaohongshu-growth`。
- 回复评论、处理质疑或写置顶评论：`$xiaohongshu-comment-reply`。
- 设计内容到咨询、体验或购买路径：`$xiaohongshu-conversion-path`。

这些技能共享同一条原则：先修复最早的断点，再增加后续动作；不靠夸张承诺、虚假身份或隐藏导流制造转化。

### 创作者内容蒸馏

```text
使用 $distill-creator-playbook。平台为小红书，模式为对标分析，目标是研究选题和结构。分析这3个账号最近各30篇公开内容，区分观察和推断，输出可测试的原创内容手册。
```

必须尽量明确平台、对象、自有或对标账号、分析目标、样本数量和可访问材料。输出不是“照抄爆款”，而是证据账本、稳定模式、可能干扰因素和测试计划。

### 编辑插画

```text
使用 $plan-editorial-illustrations。为这篇公众号文章规划6张16:9配图：白底、黑色松弛手绘、少量红蓝强调。先给插入位置、镜头动作、构图和提示词，再检查文字准确性与风格一致性。
```

重要输入：完整文章、载体、比例、数量、品牌规范、是否直接生成图片。默认先做镜头清单；明确要求生成且工具可用时直接生成。

### 品牌战略分析

```text
使用 $analyze-brand-strategy。分析这个品牌进入年轻消费市场的路径，区分企业主张、客户认知和行为证据，给出三个战略选项、取舍及90天验证计划。
```

重要输入：业务目标、市场、用户、产品价格、渠道、竞争替代、研究与经营数据。案例只能用于研究机制，不能直接复制结论。

### 营销内容创作

```text
使用 $create-marketing-content。把这些项目素材整理成一篇公众号文章，先建立事实与观点清单，再写正文、两个标题和编辑质检说明。
```

重要输入：目标读者、发布平台、内容任务、素材来源、可公开事实、语气和长度。小红书专项内容优先使用 `$plan-xiaohongshu-growth`。

### 内容账号冷启动

```text
使用 $launch-content-account。WEPR准备启动一个面向出海品牌负责人的视频号，目标是建立专业认知并获得合格咨询。请设计账号承诺、主页、内容支柱、首轮可比较样本、复盘指标和30天计划。
```

重要输入：业务目标、平台、目标受众、账号角色、产品或服务、可公开证据、内容产能、时间周期和合规限制。技能不会把固定频次、3秒钩子、内容比例或互动阈值当成平台规则。

## 5. 推荐组合工作流

### 客户增长方案

1. `$audit-digital-growth` 定义问题和指标；
2. `$plan-paid-media` 设计可控获客实验；
3. `$plan-organic-growth` 建设长期搜索与社区资产；
4. 用30/60/90天路线图统一负责人和复盘节奏。

### 小红书内容生产

1. `$distill-creator-playbook` 提炼公开对标的可迁移模式；
2. `$xiaohongshu-suite` 判断最早的阻塞环节；
3. `$xiaohongshu-profile` 与 `$xiaohongshu-topic-planner` 完成主页和选题系统；
4. `$xiaohongshu-title` 与 `$plan-xiaohongshu-growth` 完成标题、关键词和正文；
5. `$xiaohongshu-comment-reply` 与 `$xiaohongshu-conversion-path` 承接评论和咨询；
6. `$plan-editorial-illustrations` 生成统一配图，发布后用真实数据更新下一轮假设。

### 品牌事件后的恢复

1. `$diagnose-pr-crisis` 统一事实、声明和行动；
2. `$audit-digital-growth` 监测搜索、站内行为、线索和留存变化；
3. `$plan-organic-growth` 建设可验证的事实页、案例和长期信任资产。

## 6. 输出验收

检查结果是否包含：明确问题、事实与假设分离、动作优先级、负责人、时间、资源、指标、停止或扩量规则、不确定性和风险。若只有平台技巧、口号或保证结果，应视为不合格输出。

## 7. 数据与合规

只使用有权处理的数据。公开可见不等于可以无限采集、重新识别或再分发。避免伪造媒体、评价、订单、聊天、案例、搜索数据和互动；避免马甲号、封禁规避、隐藏推广、垃圾外链和关键词堆砌。平台规则、产品名称、价格和算法信息会变化，正式执行前应查阅当前官方资料。
