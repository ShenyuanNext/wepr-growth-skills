<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-effect-monitor
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Quality Gates

- `SKILL.md`、`templates/brief-template.md`、`evals/trigger_cases.json`、`evals/expected_artifacts.json` 存在。
- registry 中存在同名条目，路径为 `skills/yao-geo-effect-monitor`。
- 示例四件套真实存在：Markdown、HTML、DOCX、PDF。
- 示例四件套结构一致，至少包含执行摘要、监测口径、指标、引用、纠偏、告警、自检。
- 公司专项测试示例必须包含公司测试场景发现、官方事实来源、国内五平台口径和合成/真实采样声明。
- 报告必须声明数据接入模式、证据等级、权限边界和是否拿到真实平台样本。
- 正式报告必须按 `references/report-completeness-model.md` 覆盖系统性、详细度和完整性检查。
- 报告必须包含权威参考与来源账本；没有来源的事实判断必须标注为推断或假设。
- 报告白底、表格有边框、长字段不断版、不溢出。
- HTML 报告必须有目录菜单，桌面端固定跟随滚动，移动端不遮挡正文。
- HTML 不得保留 Pandoc 默认 `body` 窄栏约束，例如 `max-width: 36em`；桌面正文可用宽度应足以容纳 4 列以上表格。
- HTML 样式必须使用 kami 约束的油墨蓝、暖灰层级、紧凑行距和稳定表格列宽；白底要求优先于 parchment 底。
- DeepSeek、豆包、千问、Kimi、元宝均有独立采样字段。
- 指标体系必须包含候选率、推荐率、描述准确率、引用召回率、引用准确率。
- 归因必须有基线窗口、观察窗口、处理 Prompt、对照 Prompt 和混杂因素记录。
- JSON 文件可被 `python3 -m json.tool` 解析。

- 自检后不得保留 `待文件校验`、`ready_for_file_checks`、`TODO`、`TBD` 或占位标记。
