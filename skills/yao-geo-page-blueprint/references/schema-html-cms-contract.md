<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-blueprint
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# HTML、Schema 与 CMS 合同

- 页面主内容使用 `<main>`，页面核心内容使用 `<article>` 或清晰的 `<section>`。
- 首屏直接答案使用普通文本段落，不只放在图片或动画里。
- 事实卡优先用 `<dl>`、`<table>` 或带字段名的结构，不只用无语义卡片。
- 对比和榜单必须用 `<table>` 或等价结构；表格前说明比较口径。
- FAQ 使用明确问题和答案，不把问题藏在折叠组件脚本里。
- 证据区需要来源名称、URL 或文档名、核验日期、页面用途和对应模块。
- HTML 可视化报告的目录使用 `<nav class="toc-bar" aria-label="报告目录">`，模块区块使用稳定 `id`，正文区块设置 `scroll-margin-top` 防止 sticky 菜单遮挡标题。
- 多个 Schema 候选同时存在时，用稳定 `@id` 或页面锚点表达实体关系，避免孤立 JSON-LD 片段互相矛盾。

| Schema | 使用条件 | 禁止事项 |
| --- | --- | --- |
| Article | 文章、科普、专题页有作者、日期和正文 | 不给非文章页强行套 Article |
| FAQPage | 页面正文有真实可见 FAQ，且需要结构化表达问答语义 | 不用于广告型问答，不写隐藏问答，不承诺 Google 富结果展示 |
| Product | 产品页有产品名称、描述和类别 | 不编造价格、评分、库存、评价 |
| Organization | 页面有品牌/组织事实 | 不写未核验地址、资质、社媒 |
| BreadcrumbList | 页面存在可见面包屑 | 不伪造不存在的层级 |
| Review | 页面有真实评价和评价主体 | 不合成或虚构评分、作者、日期 |

## CMS 字段补充

系统、详细、完整的页面蓝图还应补充以下字段组：

- `query_fanout_items`：主问题、子问题、用户阶段、页面模块、答案形态。
- `entity_relationships`：实体名称、实体类型、关系、来源字段、页面锚点、Schema `@id`。
- `evidence_items`：来源名称、URL/文档名、核验日期、可信度、对应结论、页面位置。
- `acceptance_checks`：验收项、检查方法、负责人、频率、通过标准。
- `accessibility_requirements`：标题层级、键盘焦点、菜单行为、移动端布局、公众号版约束。
