# GEO Output Contract

Return the default artifact in Markdown unless the user asks for another format.

## 1. 改造后的完整文章

```markdown
# 优化后的文章标题

## 核心要点摘要
- ...
- ...
- ...

## 正文

### ...

## 结论

## FAQ
**Q1: ...**
A: ...

---
**内容更新时间**：YYYY-MM-DD 或 [建议补充更新时间]
**证据边界**：说明哪些内容来自原文、哪些为外部核验、哪些仍需补充。
```

Only include a table of contents when the article is long enough that it helps scanning.

## 2. GEO优化度评分

Use this table shape:

| 维度 | 权重 | 改造前 | 改造后 | 主要依据 |
| --- | ---: | ---: | ---: | --- |
| 权威原文引语 | 16 | X | X | ... |
| 统计数据完整性 | 14 | X | X | ... |
| 可引用性/可信来源 | 13 | X | X | ... |
| 结构规范性 | 12 | X | X | ... |
| 表达流畅度 | 10 | X | X | ... |
| 语义密度 | 8 | X | X | ... |
| 权威信号 | 8 | X | X | ... |
| 专业术语 | 6 | X | X | ... |
| 鲁棒性/多源支撑 | 5 | X | X | ... |
| 跨域连接 | 4 | X | X | ... |
| 易懂表达 | 3 | X | X | ... |
| 风险项 | penalty | 说明 | 说明 | ... |

The positive weights total 99. Normalize the final summary to `/100` after applying any risk penalty, and briefly state the normalization if the user needs numeric rigor.

Then summarize:

- 综合评分：改造前 `XX/100` -> 改造后 `XX/100`
- 提升幅度：`+XX`
- 高权重项改造结论：1-3 sentences.

## 3. 改造执行说明

Group changes by purpose:

- `结构层面`: headings, summary, FAQ, tables, steps, paragraph reordering.
- `证据层面`: source labels, quote suggestions, data口径, traceable facts.
- `表达层面`: transitions, paragraph balance, term definitions, readability.
- `语义层面`: entity expansion, question coverage, adjacent domains.

Use concrete counts only when you can count them reliably. Otherwise use specific locations and examples.

## 4. 需要用户补充或确认的内容

List every unsupported but useful addition:

```markdown
1. 第X节：[建议补充来源] ...
2. 第X节：[建议补充数据口径] ...
3. 第X节：[建议确认术语] ...
```

If there are no supplement items, state that all material was grounded in the supplied article or verified sources.

## 5. 改造风险提示

Mention only real risks, such as:

- 原文数据缺少来源，已保守保留或标注。
- 某些术语解释基于行业通识，需要用户确认行业口径。
- 深度改写改变了段落顺序，核心观点已保留但叙事节奏变化明显。
- 外部来源因时效性可能需要后续复核。
