<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-audit
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 输出排版防溢出策略

## Word 优先规则

- 报告源 Markdown 中不得出现 6 列及以上表格；超过 5 列时必须拆成 5 列以内表格，或改成“问题卡片 + 字段列表”。
- Word 可见文本中不得出现 42 字符以上的英文、URL 或代码连续 token；长 URL 必须改为超链接文字，命令中的长 URL 必须拆成变量和路径片段。
- 代码块单行建议控制在 76 字符以内；确实需要长命令时使用 shell 变量或分行。
- DOCX 表格必须固定在页面正文宽度内，不允许依赖 Word 自动扩宽。
- Word 报告优先可读性；宽表在 Word 中可以与 HTML/PDF 使用不同版式。
- Word 文件生成后必须运行 `scripts/polish_docx.py`，统一 Kami 字体、油墨蓝标题、暖灰表格和 A4 页边距。

## HTML/PDF 规则

- HTML 报告必须使用固定跟随目录菜单栏，默认由 `pandoc --toc --toc-depth=2` 生成，再由 `templates/report.css` 控制粘性定位。
- HTML/PDF 遵循 Kami 风格：暖纸面、油墨蓝强调、暖灰边框、无 `rgba()`、正文行距不超过 1.55。
- 表格使用 `table-layout: fixed`、`max-width: 100%`、`overflow-wrap: anywhere`。
- `a`、`code`、`pre` 必须允许换行，避免裸 URL、schema、命令右溢。
- PDF 使用 A4 页面和固定页边距；最终必须渲染 PNG 页面检查右边缘。
- PDF 打印时隐藏 HTML 目录菜单，避免目录占据过多首页篇幅。

## 自动质检门

- Markdown：检查 `|` 表格列数，任一表格超过 5 列即失败。
- DOCX：解析 `word/document.xml`，最大表格列数超过 5 即失败。
- DOCX：可见 URL 连续 token 超过 40 字符即失败。
- PDF：使用 `pdftoppm` 渲染页面，最右侧安全带不得出现文本或表格边框。
- HTML：检查 `#TOC` 目录存在，CSS 中存在 sticky/fixed 定位，并通过 Kami 基础样式检查。
- 四件套必须重新生成后再写入 `quality-report.json`。
