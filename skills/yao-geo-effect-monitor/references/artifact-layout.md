<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-effect-monitor
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Artifact Layout

- Markdown 是内容源，HTML、Word、PDF 从同一份 Markdown 或结构化数据生成。
- HTML、Word、PDF 必须白底，正文黑灰色，避免深色背景和复杂装饰。
- 表格需要完整边框、固定列宽或可控换行；长 URL 和中文长词必须允许断行。
- PDF 优先使用 A4 landscape 或足够宽的页面，避免指标表被挤压。
- Word 需要保留标题层级、表格边框和段落间距。
- HTML 必须生成可跳转目录菜单；桌面端目录固定跟随滚动，移动端目录置顶 sticky，打印/PDF 时隐藏目录。
- 使用 Pandoc 生成 HTML 时必须禁用默认文档 CSS，或在自定义 CSS 中显式覆盖 `body { max-width: none !important; }`，避免默认 `max-width: 36em` 把正文和表格压成窄列。
- 报告 UI 使用 kami 的正式文档节奏：白底优先，油墨蓝 `#1B365D` 只用于目录链接、标题左线和少量强调；中性灰使用暖灰，正文行距控制在 `1.45 ~ 1.55`，避免 1.6 以上的松散网页节奏。
- 表格列宽必须在桌面端有足够阅读宽度；验证时检查 `h1` 高度、正文宽度、首列表格列宽和横向溢出，不能只看文件是否生成。

建议渲染链路：维护 `report_input.json` 和 `*.md`；用 `pandoc --metadata document-css=false --toc --toc-depth=2` 生成带目录的 HTML；用 `pandoc` 生成 DOCX；用浏览器打印或 WeasyPrint 从 HTML 生成 PDF；用 `file`、`pdftotext`、`pandoc -t plain` 检查四件套。
