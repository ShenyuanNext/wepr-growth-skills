<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-blueprint
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# GEO 页面蓝图研究依据

| 来源 | 关键发现 | 页面设计含义 |
| --- | --- | --- |
| [GEO: Generative Engine Optimization](https://arxiv.org/abs/2311.09735) | 生成式引擎会综合多个来源生成答案，GEO 方法在实验中提升内容可见性但效果有领域差异。 | 页面不能只追求关键词，应提供直接答案、证据、领域化事实和可引用结构。 |
| [Lost in the Middle](https://arxiv.org/abs/2307.03172) | 长上下文模型对信息位置敏感，关键信息放在中部时表现可能下降。 | 直接答案、关键事实、适用边界和来源摘要应靠前，并在结尾复述关键判断。 |
| [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) | RAG 强调外部知识检索、来源可追溯和具体事实生成。 | 页面应提供来源台账、事实字段、引用锚点和更新时间。 |
| [Structural Feature Engineering for GEO](https://arxiv.org/abs/2603.29979) | 该 2026 年 arXiv 预印本把内容结构拆为宏观结构、信息切块和微观强调。 | 页面蓝图应同时设计页面架构、模块切块和字段级强调。 |
| [Google 生成式 AI 搜索优化指南](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Google 将生成式搜索与核心搜索质量、RAG、query fan-out、可抓取页面、语义 HTML 和页面体验联系起来。 | 页面必须覆盖主问题和相关子问题，提供非同质化观点、清晰技术结构、可抓取正文和移动体验。 |
| [Google 结构化数据通用规则](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) | 结构化数据必须代表页面主体内容，不能标注隐藏、误导、过期或与页面无关的信息；丰富结果不保证展示。 | Schema 候选必须带事实来源、页面位置、必填/推荐字段和禁止项，不能把 Schema 当作可见性承诺。 |
| [Schema.org 类型文档](https://schema.org/) | Article、FAQPage、Product、Organization、BreadcrumbList、Review 等类型有各自属性边界。 | 每个 Schema 候选都要说明适用条件、字段来源、`@id` 关联方式和不适用原因。 |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) 与 [WAI 页面结构教程](https://www.w3.org/WAI/tutorials/page-structure/headings/) | 标题、标签、焦点、重复导航跳过和页面结构会影响用户与辅助技术导航。 | 报告需给出标题层级、固定菜单、键盘焦点、跳转锚点、移动端和公众号版的结构建议。 |
| [MDN CSS position](https://developer.mozilla.org/docs/Web/CSS/position) | `position: sticky` 需要设置非 `auto` 的偏移属性，并受最近滚动祖先影响。 | HTML 可视化报告的菜单栏使用 `position: sticky; top:0`，避免父容器设置破坏 sticky 的 overflow。 |
| [Google FAQPage 文档](https://developers.google.com/search/docs/appearance/structured-data/faqpage) | Google 文档在 2026-05-07 标注 FAQ rich results 不再出现在 Google Search；FAQPage 仍要求问答内容可见，且主要面向权威政府/健康类场景。 | FAQPage 只能作为正文可见问答的结构化语义候选，不承诺 Google 富结果；商业 CTA 与 FAQ 分离，Schema 不得写页面正文没有的内容。 |

## 派生规则

1. `首尾优先`：首屏放直接答案、关键事实和判断边界，结尾用 FAQ 或摘要回收关键问题。
2. `三层结构`：宏观层设计页面顺序，模块层设计信息切块，字段层设计可抽取事实。
3. `证据靠近结论`：重要结论附近必须有来源、案例或解释。
4. `Schema 从正文生成`：先写正文事实，再选择 Schema；不能为了 Schema 编事实，也不能把 FAQPage 作为 Google 富结果承诺。
5. `Query fan-out 覆盖`：从一个目标问题扩展定义、对比、风险、价格、替代方案、实施、案例和 FAQ 子问题，并把每类问题映射到页面模块。
6. `可访问结构`：标题层级、菜单锚点、焦点状态和移动端阅读顺序必须作为页面设计的一部分，而不是交给视觉稿自行决定。
7. `平台差异化`：DeepSeek 强化逻辑链，千问和 Kimi 强化来源和长文层级，豆包和元宝强化轻量问答和微信生态版本。
