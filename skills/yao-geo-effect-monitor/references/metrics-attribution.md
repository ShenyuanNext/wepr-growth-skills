<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-effect-monitor
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Metrics And Attribution

| 指标 | 定义 | 计算 |
|---|---|---|
| 品牌出现率 | 答案中出现品牌名或别名的样本占比 | `mentioned_samples / total_samples` |
| 候选率 | 品牌被列为可选方案但未必推荐的占比 | `candidate_samples / total_samples` |
| 推荐率 | 品牌被明确推荐、排名靠前或给出正向选择理由的占比 | `recommended_samples / total_samples` |
| 平均排序 | 品牌在列表或比较中的平均位置 | `mean(rank)` |
| 竞品出现率 | 竞品在同组 Prompt 中出现的占比 | `competitor_samples / total_samples` |
| 负面表述率 | 出现负面、风险或误导性表述的占比 | `negative_samples / total_samples` |
| 描述准确率 | 品牌事实、产品能力、价格、案例等准确的占比 | `accurate_claims / reviewed_claims` |
| 引用召回率 | 关键说法是否有引用支持 | `supported_claims / citation_required_claims` |
| 引用准确率 | 引用是否真正支持相邻说法 | `valid_citations / reviewed_citations` |
| 答案稳定性 | 同一 Prompt 多次采样的一致程度 | 按结论、排序、引用源和事实错误分别统计 |

| 归因置信度 | 条件 |
|---|---|
| 高 | 有足够基线、观察窗口、处理 Prompt、对照 Prompt、竞品对照、外部事件记录，且多个平台趋势一致 |
| 中 | 有基线和观察窗口，至少有一组对照，混杂因素可解释 |
| 低 | 只有前后变化，样本少或缺少对照，只能作为观察线索 |

月报中使用 `观察相关`、`可能相关`、`中等置信归因`、`高置信归因` 四档措辞。
