<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-intent-miner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 国内平台适配

- Kimi 和千问：保留多轮追问链路，追问必须可回放。
- 豆包和元宝：增强日常生活化和业务场景问法。
- DeepSeek：增强复杂决策、约束条件和风险权衡问法。
- 常见句式包括“哪家好”“怎么选”“推荐”“靠谱吗”“多少钱”“和某某比怎么样”“适合谁”。
- 涉及竞品时使用中性表达，不输出无法证实的负面判断。

## 平台采样字段

- `platform`：DeepSeek、豆包、千问、Kimi、元宝。
- `prompt_style`：复杂决策、日常口语、资料整合、多轮追问、管理决策。
- `sample_prompt`：中文简体自然问法。
- `record_fields`：答案日期、平台版本、品牌是否提及、提及位置、引用来源、证据质量、风险提示、下一轮追问。
- `follow_up_policy`：Kimi/千问必须保留链路；豆包/元宝侧重口语转写；DeepSeek 增加约束和权衡。
