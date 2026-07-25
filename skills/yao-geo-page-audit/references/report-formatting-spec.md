<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-audit
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 四格式报告排版规范

## 总体

- 采用 Kami 文档风格：暖纸面 `#f5f4ed`、象牙白内容面 `#faf9f5`、油墨蓝 `#1B365D` 强调、暖灰边框。
- 中文标题使用 serif 字体栈，正文使用 sans 字体栈；整体保持编辑型、克制、适合打印。
- Word、PDF、HTML、Markdown 必须来自同一份 Markdown 内容源。
- 报告首先保证 Word 和 PDF 不溢出，再追求 HTML 视觉丰富度。
- 正文行距控制在 1.5-1.55；表格和代码使用更紧凑的 1.4-1.45。
- 避免 `rgba()`、冷蓝灰和硬阴影；使用实色暖灰、边框和轻量 ring。

## HTML

- 默认生成带目录的独立 HTML：`pandoc --standalone --toc --toc-depth=2`。
- HTML 必须有固定跟随的目录菜单栏；页面下拉时目录保持可见，打印时隐藏。
- 使用 `box-sizing: border-box`。
- 页面主体设置最大宽度，移动端保留安全边距。
- 表格使用 `table-layout: fixed`、`max-width: 100%`、`overflow-wrap: anywhere`。
- `a`、`code`、`pre` 必须允许换行。
- 目录菜单不得遮挡正文；移动端目录可折行或纵向滚动。
- 不使用可见渐变、强阴影或大色块装饰；报告应像正式白皮书，而不是营销落地页。

## Word

- Word 表格最多 5 列；超过 5 列必须拆表或改成字段块。
- 可见长 URL 改成超链接文字；命令中的长 URL 拆成变量。
- 代码块单行建议控制在 76 字符以内。
- 表格必须可编辑，不能截图化。
- 生成 DOCX 后运行 `scripts/polish_docx.py`，统一 A4 页边距、中文字体、油墨蓝标题和暖灰表格。

## PDF

- 使用 A4 页面和固定页边距。
- `@page` 背景使用暖纸面，避免导出 PDF 外边缘突兀白边。
- 宽表和代码块不得裁切；交付前渲染 PNG 检查右边缘安全带。

## Markdown

- 保留关键表格、代码块、证据台账和优先级。
- Markdown 源文件同样不得出现 6 列及以上宽表。
- Markdown 必须包含“完整性自检”或“质量报告摘要”，保证四件套同源可复核。
