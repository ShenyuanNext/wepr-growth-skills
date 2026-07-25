<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-audit
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 权威参考与证据分层

页面 GEO 诊断必须先建立证据层级，再输出结论。报告中的关键判断不得只来自印象、关键词密度或单页截图。

## 参考优先级

1. 一手页面证据：目标页面 HTML、渲染 DOM、HTTP 状态、robots、sitemap、canonical、schema、移动端截图、页面正文。
2. 官方资产：官网、官方文档、帮助中心、开发者文档、价格页、客户案例、新闻稿、投资者关系或备案公开信息。
3. 标准与平台指南：Google Search Central、Schema.org、W3C WCAG、Web Vitals、robots 与 sitemap 规范。
4. 学术与方法研究：GEO、RAG、SourceBench、正文抽取、结构化信息抽取、引用源质量评估。
5. 国内公开可见材料：搜索结果、百科页、资讯页、公众号、文档页、问答页和可公开访问的官方中文素材。
6. 第三方分析：行业文章、媒体测评、代理商内容和社区讨论，只能作为风险提示，不能替代官方事实。

## 证据标记

报告中的事实和建议必须标记为以下一种：

- 观察：来自页面、HTTP、HTML、schema、截图或可复测命令。
- 官方：来自品牌官方页面或官方帮助文档。
- 标准：来自平台指南、开放标准或稳定技术规范。
- 研究：来自论文或公开 benchmark。
- 推断：基于页面证据与方法论推导，需要后续日志、CMS 或用户提供的平台采样验证。
- 缺口：用户未提供或前台无法判断的信息。

## 证据台账字段

| 字段 | 填写要求 |
|---|---|
| 结论 | 一句话事实或诊断判断 |
| 来源层级 | 观察、官方、标准、研究、推断或缺口 |
| 页面或材料 | 用短链接文字说明来源，不放裸长 URL |
| 影响 | 对发现、抽取、引用准备、转化或合规的影响 |
| 可信度 | 高、中、低 |

## 权威参考清单

- Google Search Central：JavaScript SEO、结构化数据、robots meta、canonical、sitemap、移动优先索引。
- Schema.org：WebPage、Organization、Product、SoftwareApplication、FAQPage、BreadcrumbList、Article。
- W3C WCAG 2.2：标题结构、标签、焦点、移动与可访问性基础要求。
- Web Vitals：LCP、INP、CLS 与移动/桌面性能测量。
- GEO 研究：生成式引擎可见性、引用概率和内容呈现方式。
- RAG 研究：检索、抽取、生成链路中事实 grounding 的重要性。
- SourceBench：引用源的相关性、准确性、客观性、新鲜度、权威归属和清晰度。
- 正文抽取研究：导航、页脚、广告、空容器和客户端渲染对主内容抽取的干扰。

## 禁止事项

- 不用 schema 声明页面正文没有出现的事实。
- 不用第三方文章替代官方价格、功能、限制或服务边界。
- 不把“浏览器可见”直接等同于“初始 HTML 可读”。
- 不把“Google 可渲染”直接等同于“所有抓取器都能渲染”。
- 不在没有平台样本时判断 AI 平台召回、排名、答案出现率或引用份额。
