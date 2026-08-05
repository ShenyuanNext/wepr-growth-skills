---
name: wepr-deepseek-crawler
description: 当用户需要按关键词在 DeepSeek 网页端进行多轮独立窗口采样，并统计品牌、人物或产品的提及与引用情况时使用。输入包括关键词、采样次数、目标实体和实体类型；输出结构化 JSON 数据及可查看的 GEO HTML 报告。不用于普通网页抓取、DeepSeek API 对话、SEO 文案写作或一次性回答生成。
---

# WEPR DeepSeek 采样工具

## Inputs

Standard inputs: keywords/questions, repeat count, target entity, entity type (`人/person`, `公司/company`, `产品/product`), browser profile, and optional output directory. Competitors must match the target type. Reports default to Simplified Chinese with an English summary toggle.

## Workflow

1. Read `references/user-setup-and-usage.md` for install, prerequisites, and user-facing steps.
2. Read `references/deepseek-crawl-workflow.md` for crawler setup, preflight, delay, resume, and batch rules.
3. Read `references/report-contract.md` for JSON schema, metrics, target/competitor recognition, and report rules.
4. Run `node scripts/preflight.mjs --profile <profile>` before fresh crawling.
5. Stage 1: run `scripts/deepseek_batch_crawl.mjs` with questions, repeat, profile, target entity/type, `--safe-random-delay`, and output dir.
6. Stage 2: run `scripts/analyze_deepseek_results.py` on any crawl JSON with target entity/type, optional brands file, report output dir, and semantic review mode. Use `--semantic-review auto` by default; use `--semantic-review required` for formal delivery when AI review must pass.
7. Return the raw crawl JSON, structured Markdown, structured Excel workbook, HTML report, summary JSON, semantic-review cache when present, and failed logs. Reports include AI semantic labels for entity recognition, target-vs-best-3 radar, click-to-reveal bubbles, Chinese source names, clickable citations, title intent, compact treemap, and GEO actions.

## Honest Boundaries

- Do not use for generic website crawling, DeepSeek API chat, SEO copywriting, or one-off answer generation.
- Reuses local DeepSeek web automation; does not bypass login, CAPTCHA, bot checks, or hidden data.
- Probability metrics are repeated-sample estimates, not ground truth.
- Inferred competitors are heuristic unless `--semantic-review required` passes. AI semantic review is an audit enhancement and never replaces hard-rule gates or answer-body evidence.
- Review aliases, semantic labels, excluded candidates, and competitor tables before external use.
- Preserve raw answers, reference titles, URLs, and logs.
