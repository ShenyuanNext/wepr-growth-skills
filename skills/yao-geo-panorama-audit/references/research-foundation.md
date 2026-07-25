<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-panorama-audit
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# GEO 全景诊断研究依据

本 skill 的底层方法不是把传统 SEO 指标换名为 GEO 指标，而是把官网事实源、断言级可引用性、公开信源交叉验证和站内/站外证据建设作为 GEO 诊断的第一层工作。

## 核心研究来源

| 来源 | 本 skill 采用的结论 | 落地规则 |
|---|---|---|
| GEO: Generative Engine Optimization, arXiv:2311.09735 | 生成式引擎会综合多源信息生成答案，内容创作者需要面向生成答案中的可见性做内容与证据优化。 | 先把官网和外部公开信源整理成可抽取、可引用、可交叉验证的事实资产，再评估机会优先级。 |
| Evaluating Verifiability in Generative Search Engines, arXiv:2304.09848 | 生成式搜索的可信度取决于引用召回与引用精度，流畅答案也可能包含无支持断言或错配引用。 | 每个关键断言必须检查“来源是否存在、来源是否支持该断言、是否有待确认或冲突来源”。 |
| Trustworthiness in Retrieval-Augmented Generation Systems: A Survey, arXiv:2409.10102 | RAG 可信度至少涉及事实性、鲁棒性、透明度等维度，检索增强也可能因为检索或利用不当产生错误。 | 评分中必须单独记录事实性、鲁棒性、来源透明度和外部知识利用问题。 |
| Leveraging Contextual Information for Effective Entity Salience Detection, ACL Findings NAACL 2024 | 实体显著性与位置、上下文、关系和文档结构有关，不能只按出现次数判断。 | 报告必须检查品牌实体在官网中的位置、关系、别名、上下文、页面主次和跨页面一致性。 |
| Characterizing Attribution and Fluency Tradeoffs for Retrieval-Augmented Large Language Models, arXiv:2302.05578 | 归因与流畅性存在权衡，多源检索可能提升归因但影响答案组织。 | 诊断不能只奖励长答案或流畅答案，必须同时看来源覆盖、断言支撑和可读性。 |
| Google Search Central: helpful, reliable, people-first content | 高质量内容应提供原创信息、完整说明、可信来源、专业性、明确受众、良好页面体验，并避免只为搜索引擎而写。 | 报告必须增加“系统性与完整性”检查：原创价值、完整说明、专业来源、用户目标、页面体验和 Who/How/Why。 |
| Google Search Central: structured data guidelines | 结构化数据必须与页面可见内容一致，保持准确、最新、相关，不得误导；JSON-LD 是推荐格式之一。 | Schema 建议必须落到页面可见内容，不得给页面没有的断言加标记；必须检查 Organization、Product/Service、FAQ、Breadcrumb、Article/CaseStudy 等适配。 |
| Schema.org: Organization/Product/FAQPage | 实体、产品和问答可以用标准类型和属性表达，`sameAs`、`legalName`、`url`、`description` 等有助于消歧。 | 站内方案必须包含实体结构化字段清单，明确哪些页面承载 Organization、Product/Service、FAQ、Breadcrumb 和案例结构。 |
| W3C WCAG consistent navigation 与 MDN `position: sticky` | 一致导航帮助用户预测信息位置；sticky 元素可在滚动时固定在视口阈值位置，但不能遮挡内容。 | HTML 报告必须有固定跟随的章节菜单，保持白底、可键盘访问、锚点清晰，并在打印时隐藏或降级。 |

## 方法假设

- GEO 全景诊断的第一目标是把品牌事实变成可抓取、可复述、可引用、可验证的公开证据，而不是反推平台内部排序模型。
- 品牌 GEO 基础至少包含七层：实体清晰、事实准确、结构可抽取、来源可追溯、场景可覆盖、外部有背书、后续可监测。
- 官网是第一事实源；公众号、媒体、百科、社区、文档站、视频号、行业报告和第三方页面用于补强生成式答案可能使用的证据池。
- “可引用内容”必须具体到断言级，不只是页面级；一个页面存在不代表页面里的关键事实可被正确引用。

## 必须输出的研究化口径

- 方法依据与评分口径：说明本次诊断如何衡量官网事实源、断言可引用性、来源透明度、结构规范性和跨域证据。
- 权威参考映射：说明本次诊断如何吸收 GEO 论文、可验证性研究、Google 内容质量、结构化数据、Schema.org 和可访问导航规范。
- 用户问题覆盖矩阵：覆盖推荐、比较、替代、教程、价格、风险、真实性、购买决策和场景解决，并标注官网覆盖状态。
- 来源台账：每个关键事实标注来源类型、核验状态、用途和待确认项。
- 方案拆分：把站内页面/内容/技术结构动作与站外媒体/百科/社区/案例/合作伙伴证据建设分开。
- 完整性评分：检查官网抓取覆盖、实体关系、产品与价格、证明材料、外部信源、技术结构、内容深度、风险边界和执行闭环。

## 系统性与完整性原则

- `系统`：报告必须从输入、抓取、事实、核验、评分、问题、方案、风险、验收形成闭环。
- `详细`：每个核心结论必须落到页面、断言、来源、责任人、优先级和验收口径。
- `完整`：至少覆盖 12 个诊断域：官网抓取、实体消歧、产品服务、价格商业、客户案例、内容资产、用户问题、技术结构、Schema、外部信源、竞品对标、风险假设。
- `克制`：完整不等于堆砌；没有来源的内容写成待确认，没有资源的动作不列 P0。

## 参考链接

- https://arxiv.org/abs/2311.09735
- https://arxiv.org/abs/2304.09848
- https://arxiv.org/abs/2409.10102
- https://aclanthology.org/2024.findings-naacl.28.pdf
- https://arxiv.org/abs/2302.05578
