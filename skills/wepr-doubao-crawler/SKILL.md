---
name: wepr-doubao-crawler
description: 当用户需要通过豆包网页端或 Android Appium 进行多轮 AI 搜索采样，并生成 JSON 数据及 Markdown、Excel、HTML 格式的 GEO 报告时使用。必须提供关键词或问题及采样次数；只有在进行品牌与竞品对比时，才需要目标实体和实体类型。不用于普通爬虫、豆包 API 对话、隐藏接口提取、SEO 写作、高频自动化或一次性问答。
---

# WEPR 豆包采样工具

## Inputs

Collect with keywords/questions, repeat count, backend (`web` or `mobile`), connection fields, and output dir. Add target entity + entity type for standard diagnosis. Without a target, generate exploratory output and label inferred candidates as heuristic.

## Workflow

1. Read `references/user-setup-and-usage.md`, `references/doubao-crawl-workflow.md`, and `references/report-contract.md`.
2. For Android/Appium, also read `references/mobile-appium-workflow.md` and run `python3 scripts/doubao_mobile_crawl.py preflight ...`.
3. Stage 1 web: run `scripts/doubao_batch_crawl.mjs`.
4. Stage 1 mobile: run `scripts/doubao_mobile_crawl.py batch`; use `--fresh-chat --require-fresh-chat` when samples must start in separate Doubao app conversations.
5. Stage 2: run `scripts/analyze_doubao_results.py` on the compatible crawl JSON.
6. Use `evals/` and `templates/` for packaging checks and collection briefs.
7. Return crawl JSON, `summary.json`, structured Markdown/Excel, HTML report, screenshots/XML for mobile, failed logs, and mobile search-material evidence when present.

## Honest Boundaries

- Do not bypass login, CAPTCHA, risk controls, hidden APIs, network traffic, or app storage.
- Android/Appium is low-frequency visible UI evidence capture.
- Probability and competitor metrics are repeated-sample estimates; review aliases before external use.
- Preserve raw answers, references, URLs, screenshots/XML, and logs.
