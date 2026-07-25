---
name: yao-geo-effect-monitor
description: Use when designing a GEO Signal Monitor, AI answer monitoring system, citation tracking plan, brand-fact correction loop, GEO monthly report, alert rules, dashboard fields, or cautious attribution framework for DeepSeek, Doubao, Qianwen, Kimi, Tencent Yuanbao, and similar answer engines.
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-effect-monitor
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEO Effect Monitor

## When To Use

- 为 GEO 长期运营建立 AI 答案监测、引用源追踪、品牌表述纠偏和效果归因闭环。
- 面向客户月报、内容迭代、页面优化、外部信源建设或品牌事实纠偏输出后端监测方案。
- 覆盖国内平台：DeepSeek、豆包、千问、Kimi、元宝，并为每个平台建立独立采样口径。
- 默认交付 `Word`、`PDF`、`HTML`、`Markdown` 四格式报告，要求白底、表格边框、对齐、换行和页面溢出可控。

## Do Not Use

- 一次性 GEO 战略诊断，优先用 `yao-geo-panorama-audit`。
- 只做 CRM 字段、表单和转化追踪，不需要 AI 答案监测，优先用 `yao-geo-tracking`。
- 需要绕过平台限制、批量滥采、模拟真人登录或违反服务条款。
- 只需要内容生产或文章改写，不需要监测闭环。

## Required Inputs

最少输入：品牌名、目标平台、监测目标或报告周期。可选输入包括意图拓词 Prompt 库、竞品名、目标页面、内容清单、基线数据、发布日期、更新记录、CRM 或转化数据、外部信源清单、历史 AI 答案样本、设备、账号、地区、联网状态和合规限制。

## Required Reading

- `references/research-basis.md`
- `references/monitoring-method.md`
- `references/cn-platform-sampling.md`
- `references/data-acquisition.md`
- `references/metrics-attribution.md`
- `references/correction-loop.md`
- `references/dashboard-data-model.md`
- `references/report-completeness-model.md`
- `references/artifact-layout.md`
- `references/quality-gates.md`

## Workflow

1. 统一监测对象：品牌名、别名、产品名、竞品名、官网域名、公众号、文档站、媒体稿、社区和视频号。
2. 做权威参考扫描：先收集官网、官方文档、投资者/监管/标准资料、研究论文和可信第三方来源，建立来源账本，再进入分析。
3. 做公司测试场景发现：从公开事实提炼产品线、客户场景、AI/新功能、价格边界、集成生态、中文资料可得性和竞品/替代品，再映射到 Prompt 组。
4. 建立 Prompt 库：按 `推荐`、`比较`、`替代`、`价格`、`风险`、`品牌验证`、`场景问法` 七组组织，每组保留核心问法、长尾问法、对照问法和追问问法。
5. 建立五平台独立采样口径：DeepSeek 记录结论稳定性和证据链；豆包记录口语问答和图文输出；千问记录引用源和追问；Kimi 记录深度研究与长文引用；元宝记录微信生态来源和公众号内容表现。
6. 选择数据接入模式：按 `合成回放`、`人工真实样本`、`授权 API/连接器`、`浏览器辅助合规采样`、`CRM/转化数据导入` 分级，先确认权限、频率、证据和隐私边界。
7. 执行采样并记录环境：平台、时间、设备、账号状态、地区、联网状态、Prompt 版本、答案原文、引用链接、截图、导出文件、接口日志或其他可审计证据。
8. 做真实数据可用性判定：没有原始答案、截图/导出、采样环境和来源记录时，不得把结果标成真实采样；只能标成合成样例、推断或待复核。
9. 按六层模型分析：覆盖可见性、事实性、证据性、稳定性、竞争性和治理/归因，不允许只输出单维度指标。
10. 计算指标：品牌出现率、候选率、推荐率、排序、竞品出现率、负面表述率、描述准确率、事实错误率、引用召回率、引用准确率、引用类型覆盖、答案稳定性。
11. 做引用源追踪：区分官网、公众号、媒体、百科、社区、视频号、文档站、评测站、聚合页和竞品页面，并判断引用是否支持对应说法。
12. 做谨慎归因：设置基线窗口、观察窗口、处理 Prompt、对照 Prompt、竞品对照和外部事件记录；默认使用 `观察相关`，只有证据充分才提高归因置信度。
13. 生成纠偏闭环：把错误事实、缺失证据、弱页面、负面表达和引用缺口映射到知识库、内容改造、页面设计、外部发布或销售口径。
14. 输出系统、详细、完整的报告：必须包含来源账本、数据接入声明、分析边界、指标体系、平台差异、引用质量、风险治理、纠偏路线图、仪表盘/API 和附录。

## Output Contract

- `GEO 后端监测方案`
- `权威参考与来源账本`
- `五平台采样口径`
- `真实数据接入模式与证据等级`
- `公司测试场景发现表`
- `监测 Prompt 库`
- `指标体系与计算口径`
- `引用源追踪规则`
- `答案差异分析与谨慎归因`
- `纠偏任务表`
- `月报模板`
- `阈值告警规则`
- `复盘节奏`
- `仪表盘字段说明`
- `数据库表结构和 API 草案`
- `治理、合规、数据质量和置信度说明`
- `真实数据可用性判断：可用、部分可用、不可用、合成演示`
- `附录：Prompt 全表、指标字典、来源账本、采样记录字段`
- `风险、合规与置信度说明`
- 默认四件套：`Word`、`PDF`、`HTML`、`Markdown`

## Validation Checklist

- 四个示例或交付文件真实存在，并能被 `file`、文本抽取或浏览器打开校验。
- `HTML`、`Word`、`PDF`、`Markdown` 来源一致，章节和关键表格一致。
- 报告为白底，表格边框完整，列宽、换行、行距和页边距不溢出。
- 五个平台都有独立采样口径，不混用一个平台结论。
- 必须明确 `sample_mode` 和证据等级；没有可审计原始样本时，不得声称拿到真实平台数据。
- 不只看品牌出现率，也计算候选率、推荐率、描述准确率和引用质量。
- 引用质量同时检查召回和准确，不把引用链接数量等同于可信度。
- 归因必须有基线、观察窗口、对照 Prompt、竞品对照和混杂因素记录。
- 采样方式不违反平台服务条款；批量自动化必须写频率、权限和人工复核边界。
