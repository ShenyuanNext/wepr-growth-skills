<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-intent-miner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 四格式输出与防溢出规范

- Word 使用横向 A4：`w:pgSz w:w="16838" w:h="11906" w:orient="landscape"`。
- 左右页边距建议不高于 `850 dxa`，页面可用宽度为 `15138 dxa`。
- 每张 Word 表必须写入 `w:tblW`、`w:tblLayout w:type="fixed"` 和 `w:tblGrid`。
- `w:tblW` 与 `w:tblGrid` 列宽总和不得超过页面可用宽度。
- 不得对 8-10 列宽表使用每列 `2200 dxa` 这类固定大宽度。
- PDF 默认 `@page { size: A4 landscape; }`，表格使用 `table-layout: fixed`、`overflow-wrap: anywhere`，并禁止表格行跨页拆分。
- HTML 默认使用 kami 长文档排版语言：页面底 `#f5f4ed`，内容容器 `#faf9f5`，油墨蓝 `#1B365D`，暖灰边框，serif 标题，中文正文 sans。
- 如用户明确要求纯白底，可切换白底变体；未说明时优先使用 kami 暖纸底。
- HTML 必须提供目录菜单，菜单使用 `position: sticky; top: 0;`，下拉时固定跟随；打印时可隐藏。
- HTML 目录锚点要覆盖正文模块和主要附录。
- Markdown、HTML、Word、PDF 的章节顺序和表格字段必须一致，不能只在某个格式中缺失问题库或监测库。
- Word 与 PDF 的宽表默认压缩字号、固定列宽、单元格自动换行，不得让长英文、URL、Prompt 造成右侧溢出。
- 避免 `rgba` 半透明背景和硬阴影，标签、菜单和表头使用实色 hex，防止 WeasyPrint 渲染双层矩形。
