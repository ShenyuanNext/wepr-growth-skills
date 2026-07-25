---
name: yao-deepseek-crawler
description: "Use when a user provides DeepSeek web AI-search keywords, repeat count, target entity, and entity type, then needs repeated fresh-window crawls aggregated into JSON plus a Kami HTML GEO report. Not for generic website crawling, DeepSeek API chat, SEO writing, or one-off answer generation."
---

# Yao DeepSeek Crawler

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
