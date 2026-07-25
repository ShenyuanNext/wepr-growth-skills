---
name: yao-geo-content-refiner
description: 当用户需要把已有 SEO 文章、公众号文章、官网文章、白皮书或产品页文案改造成 GEO 友好、AI 可引用、可核验、可扫描的内容时使用；输出原文 GEO 评分、改造版文章、改造前后差异、原子事实卡、FAQ、语义补强、真实数据获取与核验计划、证据缺口和 CMS 发布版 HTML 建议，并交付 Word、PDF、HTML、Markdown 四格式报告。
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-content-refiner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEO Content Refiner

## 使用场景

- 将已有文章、产品页、公众号稿、白皮书章节或 SEO 页面改造成 AI 更容易理解、抽取、引用和推荐的内容。
- 需要提升结构化、可信度、FAQ 覆盖、原子事实密度、语义信息密度和跨平台可引用性。
- 面向 DeepSeek、豆包、千问、Kimi、腾讯元宝和微信生态输出中文简体交付物。

## 必要输入

- 原始文章全文、目标品牌、目标问题或关键词、目标平台和目标读者。
- 品牌知识库、官网资料、产品资料、客户案例、报告、资质、已授权引用来源。
- 是否保留原文风格、是否允许新增 FAQ、是否允许新增表格、是否允许新增来源。
- 是否允许联网核验、是否有内部知识库/API/表格/CRM/BI 权限、哪些数据禁止访问或禁止写入报告。

## 不适用场景

- 从零写新文章、只做标题优化、全站 GEO 诊断、页面技术审计或后端归因方案。
- 没有原文和来源，却要求补充具体数据、价格、客户案例、资质或效果承诺。
- 未授权访问登录后台、付费数据库、私有 API、客户隐私数据或内部系统。

## 必读资料

- `references/content-refinement-method.md`
- `references/data-access-and-verification.md`
- `references/evidence-and-fact-rules.md`
- `references/platform-adaptation.md`
- `references/research-backed-framework.md`
- `references/artifact-layout.md`
- `references/quality-gates.md`

## 执行流程

1. 界定改造边界，确认可用来源和禁止扩写事实。
2. 先做分析完整性检查：输入边界、来源分层、主问题、追问、评分、事实、证据、结构、语义、平台、发布和自 Review。
3. 做真实数据获取与核验计划：区分公开网页、用户提供资料、授权连接器/API、内部系统和无法访问项，记录权限、时间、新鲜度和失败处理。
4. 按 8 个 GEO 维度做原文评分：语义密度、结构规范性、可引用性、权威信号、可读性、鲁棒性、新颖性、跨域贡献。
5. 提取原子事实卡：主体、属性、数值、时间、来源、适用边界、核验状态、可引用句。
6. 补结构：直接回答、摘要、H2/H3、表格、FAQ、有序步骤和来源列表。
7. 补证据、证据强度、语义实体、平台适配矩阵、发布追踪建议，删除注水、不可核验强断言和过度营销句。
8. 输出四格式报告，并按 `references/artifact-layout.md` 与 `references/quality-gates.md` 自检。

## 版式硬规则

- Word/PDF 不允许把宽表强行塞入页面。超过 4 列的表格必须在 Word/PDF 中转成纵向事实卡。
- Word 表格必须使用固定页面宽度和显式列宽，不依赖自动列宽。
- Word 表格总宽必须小于页面可用宽度；生成后必须检查 `tblGrid` 宽度。
- PDF 必须渲染成 PNG 检查右侧留白，不得贴边或裁切。
- HTML 可以保留宽表，但必须有横向滚动和长文本换行。
- HTML 必须带顶部 sticky 菜单栏，页面下拉时固定跟随，菜单锚点覆盖主要报告模块。

## 输出契约

- GEO 改造版文章。
- 分析完整性总览。
- 真实数据获取与核验计划。
- 原文 GEO 评分表。
- 改造前后差异报告。
- 原子事实卡。
- FAQ 与同义问法。
- 语义与实体地图。
- 平台适配矩阵。
- 理论依据与改造映射。
- 证据强度与缺口。
- 页面发布版 HTML 建议。
- 发布与追踪建议。
- Word、PDF、HTML、Markdown 四格式报告。
