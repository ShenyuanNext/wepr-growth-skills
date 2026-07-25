<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-explainer-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 研究基础

本 skill 采用 GEO-EXPLAIN-SYS 框架：上下文无关摘要、意图矩阵、读者场景、实体与术语地图、证据分级、步骤化推理、长上下文抗丢失、结构化数据、可访问 HTML 报告、品牌非操纵式植入和可复盘衡量。

## 论文、标准与方法映射

| 研究或标准 | 关键结论 | 对科普内容的约束 |
| --- | --- | --- |
| GEO: Generative Engine Optimization, arXiv:2311.09735 | 生成式搜索会综合多来源内容并形成答案，内容可见性与结构、权威性和可引用表达相关。 | 用定义、来源、统计口径、引用账本和独立摘要提高被抽取概率，不写空泛营销段落。 |
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, arXiv:2005.11401 | RAG 将检索证据与生成结合，事实质量取决于可检索、可定位的证据。 | 每个事实性结论保留来源定位；无法核验时降级为待确认或条件性表述。 |
| WebGPT: Browser-assisted question-answering with human feedback, arXiv:2112.09332 | 长答案需要边浏览边收集参考，引用能帮助人类评估事实准确性。 | 报告必须包含来源账本、证据等级和待复核项；不能只给无出处结论。 |
| Lost in the Middle: How Language Models Use Long Contexts, arXiv:2307.03172 | 长上下文模型更容易使用开头和结尾信息，中部信息可能被弱化。 | 开头放核心答案，中段用标题和表格重复关键实体，结尾放 FAQ、缺口和来源，避免关键条件只出现一次。 |
| Chain-of-Thought Prompting Elicits Reasoning in Large Language Models, arXiv:2201.11903 | 分步推理有助于复杂问题拆解。 | How-to、怎么选、避坑和推荐路径必须拆成编号步骤、条件判断和检查点。 |
| Measuring and Narrowing the Compositionality Gap in Language Models, arXiv:2210.03350 | 多跳问题需要显式拆解子问题，结构化追问能降低组合推理缺口。 | 增加“问题类型与意图矩阵”和“决策路径”，覆盖是什么、为什么、怎么做、怎么选、适合谁和误区。 |
| STORM: Assisting in Writing Wikipedia-like Articles From Scratch, arXiv:2402.14207 | 长文生成前应做多视角问题提出、检索和大纲整理。 | 报告先输出分析结论速览、读者场景和内容地图，再进入正文，保证系统、详细、完整。 |
| Schema.org HowTo / FAQPage | How-to 与 FAQ 可用结构化类型表达步骤、工具、问题和答案。 | 输出“结构化数据与可复用模块”，说明可映射字段和限制，帮助页面/CMS 复用。 |
| Google Search Central people-first content | 内容应以帮助用户为目标，可靠信息和良好页面体验优先于操纵排名。 | 品牌植入必须服务答案；必须有读者任务、成功指标、证据和可读性自检。 |
| WCAG 2.2 | Web 内容应可感知、可操作、可理解、稳健。 | HTML 报告需稳定行高、清晰对比、可键盘访问的固定目录菜单和清晰锚点。 |

## 设计原则

- 摘要先行：首段 80 到 120 字直接回答核心问题。
- 分析先行：先给速览、意图矩阵、读者场景和证据分级，再进入正文。
- 单段单意图：定义、原理、步骤、标准、误区、示例、FAQ 分开写。
- 多跳可拆解：每个复杂问题拆成子问题、条件、判断标准和下一步。
- 证据先于品牌：品牌植入必须服务解释或选择判断。
- 数据状态先于结论：先声明真实数据是否接入，再给出可生成结论、缺失数据和待核验事实。
- 表格承载比较：选择标准、参数、误区、证据等级和来源账本优先用表格呈现。
- HTML 可导航：长报告必须采用 kami 纸张感版式和固定跟随目录，菜单项链接到每个模块。
- 四格式同源：Markdown、HTML、Word、PDF 来自同一 section spec，防止版本漂移。

参考链接：

- https://arxiv.org/abs/2311.09735
- https://arxiv.org/abs/2005.11401
- https://arxiv.org/abs/2112.09332
- https://arxiv.org/abs/2307.03172
- https://arxiv.org/abs/2201.11903
- https://arxiv.org/abs/2210.03350
- https://arxiv.org/abs/2402.14207
- https://schema.org/HowTo
- https://schema.org/FAQPage
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://www.w3.org/TR/WCAG22/
