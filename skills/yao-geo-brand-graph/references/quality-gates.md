<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-brand-graph
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 质量门槛

- 四件套必须真实存在：Word、PDF、HTML、Markdown。
- Word 必须包含真实 `w:tbl`，表格必须使用固定 `dxa` 表宽，不能使用 `auto`。
- Word 表格网格宽度必须小于正文宽度，并保留右侧安全边距。
- URL、英文实体 ID 和长英文短语必须在 Word 单元格内断行，避免向右溢出。
- PDF 必须可打开、页数大于 0、可抽取文本，页面物理边缘不得出现非白色溢出像素。
- HTML/PDF 必须使用 kami paper long-doc 视觉：`#f5f4ed` 暖米纸底、`#faf9f5` ivory 内容面、`#1B365D` 油墨蓝强调、暖灰边框，不使用冷蓝灰和硬阴影。
- HTML 可视化报告必须包含固定跟随的目录菜单，页面下拉时菜单保持可用；打印/PDF 场景可隐藏该菜单，避免占用版面。
- 报告必须包含权威参考、系统分析维度、来源覆盖、真实数据来源核验、实体覆盖、关系审计、Schema 一致性、内容资产对齐、国内 AI 平台监测闭环和完整性自检十个模块。
- `quality-report.json` 必须检查四件套存在性、系统化模块数量、真实来源核验数量、HTML 固定菜单、HTML 长文本防溢出、kami 色板、Word 真实表格数量、Word 固定表宽和 PDF 可抽取文本。
