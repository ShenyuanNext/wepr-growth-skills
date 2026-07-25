<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-effect-monitor
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Research Basis

| 研究方向 | 关键启发 | 落到本 skill 的要求 |
|---|---|---|
| GEO 黑盒可见性 | 生成式引擎会综合多个来源生成答案，内容创作者需要优化何时、如何被展示。 | 指标不能只看传统排名，要记录品牌出现、候选、推荐、排序、引用和答案表述。 |
| 生成式搜索可验证性 | 可信答案需要 citation recall 和 citation precision。 | 引用质量拆成引用召回率和引用准确率，不能只数引用链接。 |
| RAG 评价 | RAG 评估强调检索上下文、事实忠实度和回答质量多个维度。 | 除引用质量外，还要检查上下文相关性、答案事实性、证据覆盖和生成质量。 |
| 生成式相关反馈 | LLM 可生成查询、实体、事实、文档等反馈材料帮助扩展检索。 | Prompt 库用实体、事实、场景、替代、风险和追问扩展，每个事实必须可验证。 |
| Citation failure diagnosis | GEO 优化应先诊断文档为什么未被引用，再选择修复策略。 | 纠偏任务诊断未引用原因：无索引、弱实体、证据不足、页面不清、信源权威不足。 |
| Causal impact | 没有随机实验时，营销干预归因需要反事实、对照、时间窗口和协变量。 | 归因必须有基线、观察窗口、处理/对照 Prompt、竞品对照和混杂因素记录。 |
| AI 风险管理 | AI 风险管理强调治理、映射、测量和管理，生成式 AI 还需要处理幻觉、数据、滥用和透明度风险。 | 正式报告必须加入治理、合规、数据质量、采样权限、隐私和风险控制模块。 |

参考来源：

- GEO: Generative Engine Optimization, arXiv:2311.09735, https://arxiv.org/abs/2311.09735
- Evaluating Verifiability in Generative Search Engines, arXiv:2304.09848, https://arxiv.org/abs/2304.09848
- RAGAS: Automated Evaluation of Retrieval Augmented Generation, arXiv:2309.15217, https://arxiv.org/abs/2309.15217
- Generative Relevance Feedback with Large Language Models, arXiv:2304.13157, https://arxiv.org/abs/2304.13157
- AgenticGEO: A Self-Evolving Agentic System for Generative Engine Optimization, arXiv:2603.20213, https://arxiv.org/abs/2603.20213
- Diagnosing and Repairing Citation Failures in Generative Engine Optimization, arXiv:2603.09296, https://arxiv.org/abs/2603.09296
- Inferring causal impact using Bayesian structural time-series models, arXiv:1506.00356, https://arxiv.org/abs/1506.00356
- NIST Artificial Intelligence Risk Management Framework 1.0, NIST AI 100-1, https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- NIST AI Risk Management Framework: Generative AI Profile, NIST AI 600-1, https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

方法边界：海外生成式搜索结论不能直接等同于国内平台；GEO 结果受模型、联网状态、索引更新、账号历史和地区影响，必须记录上下文；单次答案截图不能作为稳定事实。
