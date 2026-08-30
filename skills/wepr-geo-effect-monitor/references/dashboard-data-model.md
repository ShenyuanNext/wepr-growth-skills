# Dashboard Data Model

| 模块 | 字段 |
|---|---|
| 总览 | 平台、周期、样本数、品牌出现率、候选率、推荐率、描述准确率、引用召回率、引用准确率、负面表述率 |
| 平台对比 | DeepSeek、豆包、千问、Kimi、元宝各自指标和趋势 |
| Prompt 组 | 推荐、比较、替代、价格、风险、品牌验证、场景问法 |
| 引用源 | source_type、domain、title、url、first_seen、last_seen、support_level |
| 纠偏任务 | issue_type、priority、owner、status、due_date、acceptance_metric |
| 归因观察 | intervention、baseline_window、observation_window、treated_prompts、control_prompts、confidence |

数据表：`monitor_prompts`、`answer_samples`、`citations`、`correction_tasks`。

API 草案：`POST /api/geo-monitor/prompts`、`POST /api/geo-monitor/samples`、`POST /api/geo-monitor/citations`、`GET /api/geo-monitor/monthly-report`、`POST /api/geo-monitor/correction-tasks`。
