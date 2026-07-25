<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-intent-miner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 质量门

- 正文必须覆盖 `report-module-contract.md` 的核心模块；示例报告不少于 15 个正文模块。
- 正文必须包含 `真实数据接入状态与校准模式`，并说明当前是否已拿到真实数据。
- 附录必须包含真实数据源状态；未接入真实数据时必须列下一步采样或授权动作。
- 问题库不少于 18 条，且每条都有独立重写、检索重写、证据查询、资产映射、优先级和合规等级。
- 监测 Prompt 库必须覆盖 DeepSeek、豆包、千问、Kimi、元宝。
- 追问链路必须保留上下文依赖和独立重写。
- 评分矩阵必须包含十维评分或明确说明删减原因。
- HTML 必须使用 kami 版式变量或等效样式：`#f5f4ed` 暖纸底、`#faf9f5` 内容面、`#1B365D` 油墨蓝、目录菜单和 `position: sticky`。
- HTML/PDF CSS 不得使用 `rgba` 作为标签、菜单、卡片或表头背景。
- DOCX 可读，包含 `word/document.xml`。
- DOCX 每张表的 `w:tblW` 不超过页面可用宽度。
- DOCX 每张表的 `w:tblGrid` 列宽总和不超过页面可用宽度。
- DOCX 每张表都使用 `w:tblLayout w:type="fixed"`。
- PDF 为横向 A4。
- PDF 渲染 PNG 后右侧边缘不得出现非页面背景色内容贴边；kami 暖纸底下应以 `#f5f4ed` 为背景色判断，而不是纯白。
- 四格式报告文件必须真实存在，文件名、标题、章节和附录应保持一致。
