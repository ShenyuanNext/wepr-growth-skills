<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-effect-monitor
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Data Acquisition And Evidence Modes

GEO Signal Monitor 可以分析真实数据，但不能默认声称已经拿到真实平台数据。每份报告必须先判定 `sample_mode`、`evidence_level` 和权限边界。

## 数据接入模式

| 模式 | 名称 | 可用条件 | 输出标记 | 典型用途 |
|---|---|---|---|---|
| M0 | 合成回放 | 用于 skill 测试、演示、方法样例 | `synthetic_replay` | 示例报告、流程验证 |
| M1 | 用户提供真实样本 | 用户提供答案文本、截图、导出文件或采样表 | `user_provided_sample` | 客户月报、历史复盘 |
| M2 | 人工授权采样 | 人工在平台内提问并记录环境，不绕过限制 | `manual_authorized_sample` | 小规模高质量抽样 |
| M3 | 授权 API / 连接器 | 有正式 API、密钥、额度、频率和日志 | `authorized_api_sample` | 稳定采样、看板入库 |
| M4 | 浏览器辅助合规采样 | 人工登录、授权、频率可控、可停止 | `browser_assisted_sample` | 半自动复核、截图证据 |
| M5 | 业务数据导入 | CRM、转化、CMS、发布记录由用户授权提供 | `business_data_import` | 归因窗口和效果复盘 |

## 证据等级

| 等级 | 条件 | 可写入报告的措辞 |
|---|---|---|
| E0 | 无原始答案、无截图、无环境字段 | 仅为推断或合成演示 |
| E1 | 有答案文本，但缺少截图或采样环境 | 可作为线索，需复核 |
| E2 | 有答案文本、Prompt、平台、时间、地区、联网状态 | 可作为单次真实样本 |
| E3 | E2 + 截图、导出文件、引用链接或接口日志 | 可作为可审计真实样本 |
| E4 | E3 + 多轮复采、对照 Prompt、复核人和去重记录 | 可作为月报统计样本 |

## 真实数据门槛

- 报告必须显式写出 `sample_mode`，不能把合成回放写成真实采样。
- 国内 AI 平台采样不得绕过登录、验证码、限流、付费限制或平台条款。
- 使用浏览器辅助采样时，必须记录操作者、账号状态、地区、设备、联网状态和采样频率。
- 使用 API 或连接器时，必须记录权限来源、额度、频率、失败重试和日志保留方式。
- 使用 CRM 或转化数据时，必须脱敏，并记录字段口径、时间窗口和数据拥有方授权。
- 没有对照 Prompt、基线窗口和外部事件记录时，只能报告相关性，不能报告强因果归因。

## 入库字段

| 字段 | 说明 |
|---|---|
| `sample_mode` | `synthetic_replay`、`user_provided_sample`、`manual_authorized_sample`、`authorized_api_sample`、`browser_assisted_sample`、`business_data_import` |
| `evidence_level` | `E0` 到 `E4` |
| `permission_basis` | 用户授权、公开网页、平台 API、人工采样、内部系统导出 |
| `collector` | 采集人、脚本、连接器或系统名 |
| `raw_answer_path` | 原始答案文本或导出文件路径 |
| `screenshot_path` | 截图或录屏路径 |
| `api_log_id` | API 或连接器日志 ID |
| `reviewer` | 复核人 |
| `review_status` | `pending`、`passed`、`rejected`、`needs_resample` |

## 报告判断

| 数据状态 | 报告结论 |
|---|---|
| 只有 M0 | 可展示方法，不可代表真实平台表现 |
| M1/M2 且 E2+ | 可做项目样本分析，但需说明采样范围 |
| M3/M4 且 E3+ | 可进入月报统计和看板趋势 |
| M5 单独存在 | 可做业务归因辅助，不能替代 AI 答案采样 |
| 任一模式缺少权限或证据 | 降级为待复核，不进入正式指标 |
