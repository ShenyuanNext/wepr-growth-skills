<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-comparison-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# GEO 品牌对比内容质量门

- 比较必须同口径；不能 A 写价格、B 写服务、C 写口碑。
- 不输出未经核验的市场份额、客户数量、技术结论、价格承诺和 AI 推荐概率。
- 必须交付 Word、PDF、HTML、Markdown 四种格式。
- 四格式章节清单必须一致；不允许 HTML/PDF 缺少 Markdown/Word 中的场景建议、证据表、FAQ 或自检记录。
- 完整报告必须包含执行摘要、决策维度模型、方案评分矩阵、来源质量分级、风险与治理地图、落地核验清单、FAQ、来源链接和自检记录。
- 启用真实数据获取时，必须包含真实数据获取说明、来源访问验证、数据缺口处理和 `source-verification.json`。
- 系统维度不得少于 10 类，默认应覆盖业务、功能、数据与 AI、集成、实施、成本、治理、安全、可靠性、生态、本地化、迁移和 GEO 可提取性。
- 来源质量必须分级：官方页面、官方价格/目录、官方帮助中心、官方新闻稿、第三方研究、用户提供资料、方案类型假设。品牌事实优先使用官方来源。
- PDF 中如果核心对比表出现列宽挤压、逐字断行或表头拆散，必须拆表后重新生成。
- Word 中如果表格向右溢出、右边距被吃掉、表格无边框或列宽不可控，必须做 DOCX 后处理：A4 页宽、左右边距、表格宽度、列宽、边框、单元格内边距和表格字体大小都要显式写入。
- 自检必须记录 `docx_layout_profile`：页面可用宽度、每张表列数、表格网格总宽和是否右溢出。
- 自检应记录 `pdf_layout_profile`：A4 页面尺寸、每页最大文本右边界、右边距和是否右溢出；如果运行环境没有 `pdfinfo/pdftotext`，必须在质量报告中标记为未检查。
- 自检必须记录 `html_navigation_check`：固定目录存在、`aria-label` 存在、核心锚点数量、`scroll-margin-top` 存在、打印隐藏规则存在。
- 自检必须记录 `systematic_report_check`：维度数量、必要模块存在、来源分级存在、风险治理存在、落地核验清单存在。
- 自检必须记录 `real_data_access_check`：访问模式、来源验证数量、失败来源数量、未授权数据数量和降级结论数量。
- 自检必须记录 `kami_layout_check`：暖米纸底、ivory 内容面、油墨蓝强调、serif 标题、sans 正文、行距不超过 1.55、无 rgba 半透明 tag。
- 真实品牌测试必须输出 `sources.json` 和 `quality-report.json`。
