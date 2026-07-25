<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-content-refiner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 内容改造报告版式

## 四格式规则

- Markdown：审阅母版，保留标准 Markdown 表格。
- HTML：白底、最大宽度受控，宽表使用横向滚动；`overflow-wrap:anywhere` 和 `word-break:break-word` 必须开启。
- HTML：必须输出顶部菜单栏，菜单栏使用 `position: sticky; top: 0`，页面下拉时固定跟随；菜单链接要覆盖所有主要模块。
- HTML：按 kami 的编辑排版原则处理细节：墨蓝强调、中文 serif 标题、sans 正文、暖灰边框、紧凑行距、无 `rgba()`、无硬阴影。
- Word：默认使用横向 A4、固定表宽、显式列宽；不使用自动列宽。
- PDF：A4 白底，可复制中文文本，表格或事实卡不得贴近页面右边界。

## 报告模块顺序

1. 元信息。
2. 报告摘要。
3. 分析完整性总览。
4. 真实数据获取与核验计划。
5. 原文 GEO 评分。
6. GEO 改造版文章。
7. 改造前后差异报告。
8. 原子事实卡。
9. FAQ 与同义问法。
10. 语义与实体地图。
11. 平台适配矩阵。
12. 理论依据与改造映射。
13. 证据强度与缺口。
14. 页面发布版 HTML 建议。
15. 发布与追踪建议。
16. 自 Review 结果。

## HTML 固定菜单规则

- 菜单栏放在标题区下方，白底、细边框、可横向滚动，不能遮挡正文。
- 每个菜单项链接到对应 `section id`，正文 `section` 设置 `scroll-margin-top`。
- 移动端不折叠菜单为复杂交互，直接允许横向滚动。
- 质量报告必须检查 sticky 菜单是否存在、菜单锚点数量是否完整、HTML 是否包含本地绝对路径。

## Word 防右溢出规则

- 页面使用横向 A4，左右边距 1.35 cm。
- 表格总宽使用安全值 `15260 dxa`，必须小于页面可用宽度。
- 4 列及以下使用固定宽度表格；短字段列压窄，说明列加宽。
- 超过 4 列的表格转成纵向事实卡：每条记录是一个两列表格，左列为字段名，右列为内容。
- 长 URL 在 Word/PDF 中插入可换行空格，避免单词级右溢出。
- 行高不固定，允许内容自然换行；禁止使用固定行高截断内容。

## PDF 防溢出规则

- PDF 生成后必须用 `pdftoppm` 渲染为 PNG。
- 检查每页右侧非白像素边界，右边留白应为正且稳定，不得贴到页面边缘。
- 宽表同样转成纵向事实卡，避免 6-8 列表格在 PDF 中过窄或裁切。

## 自检命令建议

```bash
pdftoppm -png -r 130 report.pdf tmp/page
```

Word 结构检查应读取 `word/document.xml` 中 `w:pgSz`、`w:pgMar` 和每张表的 `w:tblGrid/w:gridCol`，确保表格总宽小于可用宽度。
