<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-effect-monitor
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Monitoring Method

| 组别 | 目的 | 示例模式 |
|---|---|---|
| 推荐 | 判断品牌是否进入候选和推荐 | `推荐几个适合{场景}的{品类}` |
| 比较 | 观察排序、优劣描述和竞品 | `{品牌}和{竞品}哪个更适合{场景}` |
| 替代 | 判断竞品替代关系 | `{竞品}有哪些替代方案` |
| 价格 | 判断定价、套餐和成本表述准确性 | `{品牌}价格贵吗` |
| 风险 | 识别负面、风险和误解 | `{品牌}有什么缺点或风险` |
| 品牌验证 | 检查事实一致性 | `{品牌}是正规的吗 / 背景是什么` |
| 场景问法 | 覆盖真实业务长尾 | `{行业}{岗位}怎么选择{品类}` |

采样频率：P0 品牌事实纠偏每日或隔日复采；P1 推荐与引用质量每周采样；P2 长尾场景双周或月度采样；内容发布、页面修复、外部信源发布后设置 `T-14 ~ T0` 基线窗口和 `T+7 / T+14 / T+30` 观察窗口。

样本字段：`sample_id`、`sample_mode`、`evidence_level`、`platform`、`sampled_at`、`device`、`account_state`、`region`、`network_enabled`、`prompt_id`、`answer_text`、`answer_screenshot`、`raw_export_path`、`collector`、`permission_basis`、`brand_mentioned`、`brand_candidate`、`brand_recommended`、`brand_rank`、`competitor_mentions`、`negative_terms`、`fact_errors`、`citations`、`citation_supports_claim`、`confidence`。

真实数据门槛：没有 `answer_text`、采样环境、采集时间、Prompt 版本和至少一种可审计证据（截图、导出文件、接口日志或人工复核记录）时，报告只能标为 `synthetic`、`inferred` 或 `pending_review`，不得标为 `live_platform_sample`。

## 公司测试场景发现

针对指定公司做示例或客户项目时，先从公开资料提炼 `产品线`、`主要客户场景`、`AI/新功能`、`价格或套餐边界`、`集成生态`、`中文资料可得性`、`常见竞品/替代品`，再映射到七组 Prompt。每个测试场景至少记录：

- `scenario_id`
- `source_fact`
- `target_prompt_group`
- `domestic_platform_risk`
- `expected_correct_answer`
- `likely_wrong_answer`
- `source_url`

这种场景发现步骤必须先于合成采样或真实采样，避免生成与公司业务无关的通用监测 Prompt。
