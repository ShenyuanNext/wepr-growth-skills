<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-comparison-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 品牌对比报告版式

- Markdown：内容母版，语义化标题、中文字段和标准 Markdown 表格。
- HTML：遵循 Kami 长文档风格，暖米纸底、ivory 内容面、油墨蓝强调、最大宽度受控、响应式表格、边框对齐、长文本可换行。
- PDF：从已校验 HTML 渲染，A4 页面、Kami 暖米纸底、合理页边距，避免表格跨页错位。
- Word：使用 `.docx`，保持与 Markdown/HTML 同一章节结构，标题、正文和表格边框必须可读；必须显式设置 A4、左右页边距、表格总宽、列宽、单元格内边距和暖灰边框。
- 四格式必须从单一内容结构生成；只能改变布局，不能删减章节、表格、FAQ、来源或自检记录。
- HTML/PDF/Word 中超过 4 列的长表必须拆成多张窄表。
- DOCX 表格不得依赖 Word 自动伸缩。生成后检查每张表的 `tblGrid` 宽度总和必须小于等于正文可用宽度；如果有一张表超过可用宽度，必须缩短字段、拆表或重设列宽后重新生成。
- HTML 可视化报告必须包含固定目录栏：使用 `<nav aria-label="报告目录">`，目录在页面下拉时跟随，移动端允许横向滚动，打印时隐藏。
- 每个主要章节使用稳定 `id`，并设置 `scroll-margin-top`，避免固定目录遮挡标题。
- 固定目录不得覆盖正文，不得使用深色背景、浮层卡片或会遮挡表格的样式；使用 warm sand 或 ivory 底、细边框、清晰焦点态即可。
- HTML 目录链接应覆盖所有核心章节，至少包括执行摘要、比较口径、决策维度、核心对比、风险治理、平台适配、FAQ、来源和自检。
- 字体按 Kami 规则：中文标题优先 serif，正文和 UI 元素使用 sans；行距控制在 1.55 以内；避免冷蓝灰、硬阴影和 rgba 半透明 tag。

```css
:root { --parchment:#f5f4ed; --ivory:#faf9f5; --brand:#1B365D; --near-black:#141413; --border:#e8e6dc; }
body { background: var(--parchment); color: var(--near-black); line-height: 1.55; }
.report { background: var(--ivory); border: 0.5pt solid var(--border); }
.sticky-menu { position: sticky; top: 0; z-index: 20; background: var(--ivory); border-bottom: 1px solid var(--border); overflow-x: auto; }
section { scroll-margin-top: 76px; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; }
th, td { border-bottom: 0.5pt solid #e5e3d8; padding: 8px 10px; vertical-align: top; overflow-wrap: anywhere; }
@media print { .sticky-menu { display: none; } }
```
