<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-comparison-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 研究基础：GEO-CITER-S 框架

本 skill 使用 `GEO-CITER-S`：Comparison scope、Information gain、Traceable evidence、Equitable comparison、Repair loop、Systematic completeness。

- Comparison scope：先锁定目标品牌、比较对象、用户场景和决策边界。
- Information gain：每个维度必须提供对决策有增量的信息。
- Traceable evidence：关键判断必须绑定来源 ID；来源不足时降级判断。
- Equitable comparison：保留竞品优势和目标品牌边界，不靠贬损竞品制造优势。
- Repair loop：生成后必须检查事实、引用、同口径、格式和排版，再迭代修复。
- Systematic completeness：报告必须覆盖业务、产品、数据、AI、集成、实施、成本、治理、可靠性、生态、本地化、迁移和 GEO 可提取性，避免只围绕少数优势点写软文。

## 权威标准与研究来源

- ISO/IEC 25010:2023：把 ICT 与软件产品质量拆为特性和子特性，适合作为 SaaS/CRM 选型维度的底层参考。
- NIST AI RMF 1.0：强调以治理、映射、测量、管理形成 AI 风险闭环，适合作为 AI 生成报告的事实、边界、风险和修复框架。
- W3C WCAG 2.2：提供可测试的 Web 内容可访问性原则，适合约束 HTML 报告目录、锚点、焦点、移动端可用性和打印兼容。
- GEO 论文：用于理解生成引擎可见性和内容结构化表达。
- RAG 与 Self-RAG：用于要求来源台账、证据绑定、引用准确性和自反式核验。
- Chain-of-Thought：用于把复杂选型拆成场景、约束、能力、证据、权衡和建议的因果链，但最终报告只输出可审计结论，不暴露无证据的推理断言。

参考论文：

- GEO: Generative Engine Optimization: https://arxiv.org/abs/2311.09735
- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks: https://arxiv.org/abs/2005.11401
- Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection: https://arxiv.org/abs/2310.11511
- Chain-of-Thought Prompting Elicits Reasoning in Large Language Models: https://arxiv.org/abs/2201.11903

参考标准：

- ISO/IEC 25010:2023 Product quality model: https://www.iso.org/standard/78176.html
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- Web Content Accessibility Guidelines (WCAG) 2.2: https://www.w3.org/TR/WCAG22/
