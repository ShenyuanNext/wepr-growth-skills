<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-blueprint
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 四格式文件生成流程

```bash
python3 scripts/render_yao_geo_page_blueprint.py --input <report_input.json> --output-dir <output-dir>
```

默认生成 `.md`、`.html`、`.docx`、`.pdf` 和 `quality-review.json`。

## 交付后检查

- 四个报告文件必须真实存在且非空。
- `quality-review.json` 的 `passed` 必须为 `true`。
- HTML 不得包含本地绝对路径、渐变背景或深色页面底。
- HTML 必须包含白底、暖灰边框、油墨蓝强调、`border-collapse`、`overflow-wrap` 和 A4 打印规则。
- HTML 必须包含固定跟随目录：`class="toc-bar"`、`aria-label="报告目录"`、`position: sticky`、`top:0`，并检查移动端菜单不把文字挤出容器。
- Word 必须检查 `word/document.xml` 中是否包含固定表格布局、`tblGrid`、`tcMar` 和 `wordWrap`；当内容存在长 URL、英文产品名、Schema 字段或代码片段时，必须检查软换行。
- 示例报告如果新增研究依据、证据区或 Schema 规则，必须重新生成四格式，不能只改 Markdown。
