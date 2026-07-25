<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-ranking-article-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 研究基础

本 skill 的底层假设是：GEO 榜单文章不是“软文排名”，而是面向生成式搜索、问答摘要和真人采购决策的证据化比较内容。执行时优先把参考文献和标准转成写作约束。

## 主要参考

| 参考 | 关键启发 | 转化为 skill 约束 |
|---|---|---|
| GEO: Generative Engine Optimization, arXiv 2311.09735 | 生成式引擎会综合多源信息，内容可见性依赖来源、权威表述、统计与引用等信号 | 榜单文章要提供清晰实体、来源归因、可引用结论和多源证据 |
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, arXiv 2005.11401 | 检索增强能提升知识密集生成的事实性、具体性和可更新性 | 关键事实必须来自可追溯来源，不能只靠模型记忆或品牌自述 |
| PRISMA 2020 statement | 系统综述强调透明报告、清单、筛选流程和完整性 | 榜单要说明筛选方法、纳入/排除理由、证据限制和核验日期 |
| Google Helpful, Reliable, People-First Content | 内容应提供完整描述、原创分析、清晰来源、专业性和良好页面体验 | 报告不能只改写来源，要加入选择建议、边界和额外判断 |
| Google E-E-A-T / Search Quality Rater Guidelines | 质量判断关注经验、专业性、权威性和可信度 | Sources、作者/组织背景、事实与观点分离、未核验降级表达 |
| W3C WCAG 2.2 | Web 内容应可感知、可操作、可理解、稳健 | HTML 报告要有可读行高、可访问目录、语义结构、对比度和非溢出表格 |
| MDN CSS position sticky | sticky 元素按普通流布局，再相对最近滚动祖先固定 | HTML 目录菜单使用 `position: sticky; top: 0; z-index`，避免遮挡正文 |
| Schema.org FAQPage/Product/AggregateRating | 结构化数据帮助描述页面、产品、评分和 FAQ | 仅在证据充分时建议结构化数据，不伪造评分、评价数或价格 |

## 参考优先级

1. 官方来源：官网、产品页、定价页、帮助中心、文档、年报、监管披露。
2. 标准与学术：W3C、PRISMA、arXiv/ACL/ACM 等与检索、生成、报告透明度相关的资料。
3. 行业研究：Gartner、Forrester、IDC、G2、Capterra、TrustRadius 等，注意时间和评价口径。
4. 媒体和访谈：只能作为背景或补充，不得替代关键事实。
5. 品牌 Brief：可作为待核验线索，不能单独支撑 TOP1、客户结果、奖项、认证或价格。

## 对榜单内容的理论要求

- **可回答性**：摘要、对比表和 FAQ 能直接回答 AI 平台常见问题。
- **可引用性**：每个核心结论有短句、明确主体和来源编号。
- **可比较性**：同一维度比较同类对象，避免把不同类别产品硬放一张榜。
- **可追溯性**：关键事实回到来源，不能出现无出处数字。
- **可复核性**：保留核验日期、价格区域、未公开项和限制说明。
- **非操纵性**：推荐梯度来自证据和场景，而不是营销目标。
