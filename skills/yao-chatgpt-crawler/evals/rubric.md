<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-chatgpt-crawler
Created by: 姚金刚
Date: 2026-06-25
X: https://x.com/yaojingang
-->

# yao-chatgpt-crawler Rubric

## Pass Conditions

- The agent asks for or confirms the standard inputs: question list, repeat count, target entity, entity type, OpenCLI profile, interval preset, and optional alias/competitor table.
- Fresh crawl runs call `scripts/preflight.mjs` before opening ChatGPT.
- Fresh crawl commands use a random interval preset. Default is `30s-1m`; longer runs should consider `1-3m` or `3-10m`.
- The crawler preserves answer text, visible ChatGPT citation/source links, markdown links, and bare URLs in the private run directory.
- The analyzer receives `--target-entity` and `--entity-type`, plus aliases or a brands file when available.
- Competitor rows are constrained to the same entity type as the target.
- Reports expose mention rate, average mentions, Top 1 / Top 3 / Top 5 probability, average rank, sentiment, sources, titles, semantic labels, and target-vs-competitor gaps.
- Public examples remove local browser profile names, ChatGPT conversation URLs, raw control output, and absolute local paths.

## Fail Conditions

- The agent treats ChatGPT Web Search as the ChatGPT API.
- The run uses generic scraping against arbitrary websites instead of the ChatGPT web answer surface.
- The report mixes people, companies, products, concepts, and noise terms into one competitor probability table without type gating.
- The agent claims the sampled probability is an official ranking, market share, or stable benchmark.
- The agent attempts to bypass login, CAPTCHA, throttling, account restrictions, or hidden platform controls.
- Public artifacts leak local profile names, private conversation IDs, cookies, raw terminal logs, or absolute personal filesystem paths.

## Review Notes

Use `--semantic-review required` for formal delivery when the semantic entity/competitor decision must be AI-reviewed. Use `--semantic-review auto` for exploratory runs; it falls back to local rules when no API key is available and records that status in the report.
