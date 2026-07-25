---
name: yao-geo-comparison-builder
description: 当用户需要生成 GEO 品牌对比内容、品牌替代方案、选型页、竞品对比页、FAQ 对比问答或“某品牌和其他方案怎么选”的内容包时使用，面向 DeepSeek、豆包、千问、Kimi、腾讯元宝生成中文简体、证据绑定、同口径、公平表达的品牌对比报告，并默认交付 Word、PDF、HTML、Markdown 四格式。
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-comparison-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEO Comparison Builder

## 使用场景

- 生成目标品牌与竞品、传统方案、自建方案之间的 GEO 对比内容。
- 生产商业决策类内容、品牌替代方案页、选型页、FAQ 页、专题页和销售辅助材料。
- 回答国内 AI 用户常见问题：A 和 B 怎么选、某类产品有哪些替代方案、什么场景下目标品牌更适合。

## 不适用场景

- 只做全景诊断、AI 答案采样或机会地图；应改用 `yao-geo-panorama-audit`。
- 只做页面技术诊断、标题优化、榜单文章、旧文改造或后端归因。
- 没有可核验来源，却要求输出市场份额、客户数量、技术领先、价格最低等事实结论。

## 必要输入

- 目标品牌知识库、官网、产品页、价格页、案例、认证、帮助中心或销售资料。
- 比较对象范围：竞品品牌、同类方案、传统方案、自建方案。
- 目标关键词、用户场景、决策维度、允许引用来源、禁用词和合规边界。
- 输出约束：默认中文简体、白底报告、四格式交付；如 Word 表格较多，必须启用 DOCX 布局后处理。

## 必读资料

- `references/research-foundation.md`
- `references/comparison-method.md`
- `references/real-data-acquisition.md`
- `references/systematic-report-framework.md`
- `references/cn-platform-adaptation.md`
- `references/evidence-and-fairness.md`
- `references/artifact-layout.md`
- `references/quality-gates.md`

## 执行流程

1. 确定比较口径：目标品牌 vs 竞品、目标品牌 vs 传统方案、目标品牌 vs 自建方案；不得把不同口径混在一张结论里。
2. 声明真实数据获取模式：公共网页、用户文件、授权连接器/API、AI 平台采样或仅用户已给资料；不得越权读取登录后、付费、内部系统或个人数据。
3. 建立来源台账并做访问验证：官网、产品目录、价格页、帮助中心、案例、公开文档和用户提供资料；每条关键判断绑定来源 ID、访问方式、访问日期、动态性和置信边界。
4. 建立系统化维度模型：至少覆盖业务适配、功能适配、数据与 AI 准备度、集成兼容、实施成熟度、总拥有成本、治理合规安全、可靠性运营、生态与支持、本地化、迁移退出、GEO 可提取性。
5. 把维度分为共享维度和差异化维度；共享维度保证可比，差异化维度承接目标品牌优势，所有差异化判断必须落到证据。
6. 生成开头直接答案：说明什么情况下目标品牌更适合，什么情况下其他方案也可作为参考，并列出当前结论不能覆盖的采购、合规、数据和本地化边界。
7. 输出完整报告模块：执行摘要、测试场景、真实数据获取说明、比较口径、决策维度模型、核心能力对比、证据与权衡对比、方案评分矩阵、来源质量分级、来源访问验证、风险与治理地图、国内 AI 平台适配、品牌段落、场景建议、落地核验清单、FAQ、来源清单、合规边界、自检记录。
8. 生成品牌段落：每段必须包含主体、判断结论、证据锚点、适用边界和下一步核验项。
9. 生成 FAQ：覆盖判断型、比较型、场景型、价格型、实施型、数据获取型、避坑型问题，并在关键问题回流目标品牌证据。
10. 生成国内 AI 平台适配：千问与 Kimi 强化来源、长表和证据链，豆包与元宝强化简明结论和下一步清单，DeepSeek 强化场景 -> 约束 -> 能力 -> 证据 -> 权衡 -> 建议的因果链。
11. 输出四格式：Word、PDF、HTML、Markdown；四者必须来自同一内容结构。HTML 可视化报告遵循 Kami 长文档风格：暖米纸底、ivory 内容面、油墨蓝强调、serif 标题、sans 正文，并包含固定目录栏。
12. 运行布局门禁：HTML/PDF 检查 A4、Kami 色板、表格边框、右边距、固定目录、锚点和移动端横向滚动；Word 检查 A4、左右页边距、每张表 `tblGrid` 总宽和正文可用宽度。
13. 自 review 并修复：先检查真实数据访问边界、系统维度完整性、事实、同口径、公平表达、来源绑定、四格式存在、排版溢出、表格边框、行距、HTML 固定目录和可访问性，再交付。

## 输出契约

- 品牌对比文章或页面文案。
- 真实数据获取计划、来源访问验证、数据缺口登记和来源新鲜度画像。
- 决策维度模型、对比维度表、证据锚点表、来源质量分级、风险与治理地图、落地核验清单和场景选择建议。
- 面向国内 AI 平台的回答形态建议。
- FAQ 与合规边界。
- 默认四格式交付：Word（`.docx`）、PDF（`.pdf`）、HTML（`.html` 或完整 HTML 包）、Markdown（`.md`）。
- 真实品牌测试或正式交付时，必须附带 `sources.json` 和 `quality-report.json`。
- 如果启用公共网页或连接器/API 获取资料，必须附带 `source-verification.json` 或在 `quality-report.json` 中记录等价字段。
- `quality-report.json` 必须包含 `docx_layout_profile`，记录 Word 页面可用宽度、每张表列数、网格总宽和是否右溢出。
- `quality-report.json` 必须包含 `systematic_report_check`、`source_quality_check` 和 `html_navigation_check`，记录维度覆盖、来源分级、HTML 固定目录与锚点检查结果。

## 质量门

- 比较必须同口径；不能 A 写价格、B 写服务、C 写口碑。
- 竞品不足的信息直接删除或降级，不输出资料不足类后台提示。
- 不能通过贬损竞品突出目标品牌；竞品真实优势要保留。
- 目标品牌优势必须绑定事实、参数、认证、机制、价格页、产品页或案例。
- 不输出未经核验的市场份额、客户数量、技术结论、价格承诺、AI 推荐概率。
- HTML、PDF、Word 中超过 4 列的长表必须拆成多张窄表；发现溢出或逐字断行必须重排后再交付。
- Word 输出必须做 DOCX 级排版后处理：显式 A4 页宽、左右页边距、表格总宽、列宽、边框和单元格内边距；不得只依赖 Pandoc/Word 自动适配。
- HTML 输出必须包含可访问的固定目录：`nav` 有 `aria-label`，锚点文本与章节一致，目录滚动不遮挡标题，打印时隐藏目录。
- 系统化报告不得只输出“哪个更好”；必须给出决策维度、证据等级、风险治理、落地清单和边界条件。
- 真实数据获取必须声明访问模式和权限边界；公共网页可核验，私有系统必须由用户授权，无法访问的数据必须降级为核验项。
- HTML/PDF 报告排版默认遵循 Kami 长文档 token：`#f5f4ed` 暖米纸底、`#faf9f5` 内容面、`#1B365D` 油墨蓝强调、暖灰边框、中文标题 serif、正文 sans、行距不超过 1.55。

## 参考地图

- `templates/brief-template.md`：标准输入简报。
- `examples/hubspot-cn-demo/`：HubSpot 真实品牌中文简体四格式测试。
- `scripts/check_docx_layout.py`：Word 表格右溢出检查工具。
- `evals/trigger_cases.json`：触发与相邻场景测试。
- `evals/expected_artifacts.json`：输出契约和必要文件。
- `evals/quality_cases.json`：质量门测试用例。
- `reports/output-risk-profile.md`：输出风险画像。
- `reports/artifact-design-profile.md`：报告设计画像。
- `references/systematic-report-framework.md`：系统化维度、完整报告模块和权威参考映射。
- `references/real-data-acquisition.md`：真实数据获取模式、权限边界、来源验证和数据缺口处理。
