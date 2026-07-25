<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-explainer-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 四格式报告版式

## 共用规则

- 按 kami 风格使用纸张感浅底 `#f5f4ed`、象牙色内容面 `#faf9f5`、蓝黑强调色 `#1B365D` 和暖灰边框；不使用渐变、透明叠色、深色底或装饰性大色块。
- Markdown、HTML、Word、PDF 必须来自同一 section spec，标题集合必须一致。
- 表格边框对齐，行高稳定，单元格留白适中。
- 长中文句、URL、英文产品名、参数串必须自动换行。
- 报告模块需要足够系统：意图、读者、研究、证据、实体、定义、原理、步骤、标准、决策、误区、FAQ、术语、品牌、平台、结构化数据、衡量、缺口、合规、来源。

## HTML 与 PDF

- HTML 使用本地字体包：Inter 负责正文，TsangerJinKai 负责标题；字体文件需要随 HTML 包一起输出到 `fonts/`。
- HTML 使用 `background:#f5f4ed`、`border-collapse:collapse`、`overflow-wrap:anywhere`，正文容器和表格面使用 `#faf9f5`。
- 表格外层使用横向滚动容器，移动端不挤压正文。
- HTML 必须生成固定跟随目录菜单，使用 `position:sticky; top:0`，菜单项链接到每个模块的锚点。
- 目录菜单需要可键盘访问，提供 `aria-label`，hover/focus 状态不能遮挡正文。
- PDF 由 HTML 渲染，使用 A4 页面、`20mm/22mm` 级别稳定页边距；打印样式里表格不得设置超过正文宽度的最小宽度。

## Word

- A4：`11906 x 16838 dxa`。
- 左右页边距：`1134 dxa`。
- 可用正文宽度：`9638 dxa`。
- 表格必须固定布局，`tblW` 和 `gridCol` 宽度总和不得超过 `9638 dxa`。
- 单元格内长 ASCII token 需要插入软换行，避免向右侧溢出。
- Word 可使用浅纸张背景 `F5F4ED`，字体声明与 HTML 保持一致方向；每次生成后检查 `word/document.xml` 中表格宽度、长 token、文档背景和必备标题。
