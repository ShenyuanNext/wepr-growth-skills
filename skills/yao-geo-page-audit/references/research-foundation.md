<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-audit
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 页面 GEO 诊断研究依据

## 底层模型

本 skill 将页面 GEO 表现拆成五段链路：

1. 发现入口：页面是否通过链接、sitemap、搜索结果、百科、资讯、公众号、文档页等入口被发现。
2. 检索候选：页面是否具备被搜索、AI 搜索或 RAG 系统作为候选素材的技术条件；不等同于实际平台召回数据。
3. 主内容抽取：系统是否能从 HTML 中抽出正文，而不是导航、广告、页脚或空容器。
4. 证据质量：被抽取片段是否相关、准确、清晰、客观、可追责、足够新。
5. 生成引用：生成式引擎是否能把页面片段用于回答、引用或推荐。

## 研究启发

- [GEO: Generative Engine Optimization](https://arxiv.org/abs/2311.09735) 强调生成式引擎可见性不等同于传统搜索排名；本 skill 只在有样本时分析真实答案表现。
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) 提醒页面诊断要关注候选素材、可抽取和可引用，而不只是页面文案。
- [SourceBench: Can AI Answers Reference Quality Web Sources?](https://arxiv.org/abs/2602.16942) 将引用源质量拆成相关性、事实准确性、客观性、新鲜度、权威/责任归属和清晰度。
- [Boilerplate Removal using a Neural Sequence Labeling Model](https://arxiv.org/abs/2004.14294) 提醒 HTML 中的正文、导航、页脚、广告和动态渲染内容会影响机器抽取结果。
- [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) 说明初始 HTML、渲染队列和可抓取链接会影响搜索系统看到的内容。
- [Google 结构化数据指南](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) 强调结构化数据必须代表页面主内容，且不能标记用户不可见内容。
- [Google 移动优先索引指南](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing) 要求移动端内容和元数据与桌面端保持等价。
- [Web Vitals](https://web.dev/articles/vitals) 把页面体验拆成 LCP、INP、CLS 等可复测指标。
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) 为标题、标签、焦点、移动可用性和可访问结构提供标准依据。

## 诊断影响

- 不把 schema 当作独立答案源；schema 必须和正文事实一致。
- 不把 SEO 关键词密度当作 GEO 可见性的核心指标；更重视事实原子性、段落独立性、来源可追责和证据一致性。
- 不把最终浏览器截图等同于机器可读页面；必须检查初始 HTML 和 JS 渲染依赖。
- 不把中文答案的素材来源只限定为官网营销页；公开素材还应覆盖中文知识库、百科、资讯、公众号、问答和文档页。
- 不把公开页面诊断写成平台召回报告；没有平台样本时，只输出素材准备度和修复建议。
