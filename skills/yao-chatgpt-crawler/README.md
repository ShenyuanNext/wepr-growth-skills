# Yao ChatGPT Crawler

`yao-chatgpt-crawler` turns repeated ChatGPT web AI-search crawls into GEO probability evidence.

It is designed for jobs like:

- 1-20 keywords/questions, each crawled repeatedly in a fresh ChatGPT conversation.
- Keep every raw answer and visible ChatGPT citation/source-flyout link or markdown URL.
- Diagnose one target entity with a declared entity type, then compare it with same-type competitors extracted from ChatGPT answers.
- Aggregate visibility, average mention count, average rank, Top 1 / Top 3 / Top 5 probability, sentiment tendency, source/channel mix, title intent patterns, repeated citations, and target-vs-competitor gaps.
- Generate a canonical JSON dataset, structured Markdown, structured Excel workbook, and a Kami-styled HTML report.

It is not a generic website crawler and does not use the ChatGPT API.

## Requirements

- Node.js 18+
- Python 3.10+
- OpenCLI CLI 1.8.4+
- OpenCLI Browser Bridge connected to a Chrome or Edge profile
- ChatGPT web session that can send messages; visible ChatGPT sources are required for source analysis
- Bundled crawler at `scripts/chatgpt_browser_crawl.mjs`, or pass `--crawler-script` to use a compatible replacement
- Optional: `OPENAI_API_KEY` for AI semantic review during analysis. Without it, the analyzer automatically falls back to local semantic rules.

Start with the user setup guide:

- `references/user-setup-and-usage.md`

Preflight for fresh crawling:

```bash
node scripts/preflight.mjs --profile <opencli-profile>
```

Preflight for report generation from an existing JSON:

```bash
node scripts/preflight.mjs --analysis-only
```

## Stage 1: Batch Crawl

Create `questions.txt` with one question per line, then run:

```bash
node scripts/chatgpt_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "光引GEO" \
  --target-aliases "光引" \
  --entity-type company \
  --delay-preset 1-3m \
  --out-dir runs/chatgpt-geo
```

Outputs:

- `runs/chatgpt-geo/chatgpt-crawl.json`
- `runs/chatgpt-geo/raw/*.json`
- `runs/chatgpt-geo/logs/*.log`

Use `--dry-run` to verify the plan without opening ChatGPT. Fresh runs use a random `30s-1m` interval between samples by default. Use `--delay-preset 1-3m` for a balanced run, or `--delay-preset 3-10m` / `--safe-random-delay` for a more conservative run. Slower random intervals reduce request frequency but do not guarantee account safety or bypass platform risk controls.

The batch crawler requests ChatGPT Web Search by default. Pass `--no-search` for answer-only sampling, `--model instant|thinking|pro` to switch the current ChatGPT web mode, or `--deep-research` for long-running Deep Research samples when the account supports it. If OpenCLI reports that the Web Search tool option cannot be found, the crawler retries without the explicit toggle and still extracts any visible ChatGPT citation pills, source-flyout links, markdown links, or bare URLs that the account displays.

## Public Real Example

This package includes a sanitized real ChatGPT Web Search test for the model product target `豆包`:

- `examples/doubao-model-products-real/questions.txt`
- `examples/doubao-model-products-real/brands-model-products.txt`
- `examples/doubao-model-products-real/chatgpt-crawl.json`
- `examples/doubao-model-products-real/report/summary.json`
- `examples/doubao-model-products-real/report/structured-data.md`
- `examples/doubao-model-products-real/report/report.html`

The example used five Chinese LLM-market questions, three repeats per question, and a reviewed model-product alias table. The public copy removes local profile names, ChatGPT conversation URLs, raw command excerpts, and absolute filesystem paths while keeping answer text, extracted citations, source metadata, semantic labels, and aggregate metrics.

## Stage 2: Analyze And Render

Standard input fields:

```text
1. 关键词：GEO服务商推荐、靠谱的GEO优化公司有哪些
2. 轮询次数：每个关键词查询 5 次
3. 目标实体：光引GEO
4. 实体类型：公司
5. OpenCLI profile：edge-chatgpt
6. 单次查询间隔：默认 30s-1m，可选 1-3m 或 3-10m
```

Optional `brands.txt` can provide reviewed aliases and competitors:

```text
光引GEO|光引
源易信息
PallasAI|Pallas AI
```

Run:

```bash
python3 scripts/analyze_chatgpt_results.py \
  runs/chatgpt-geo/chatgpt-crawl.json \
  --target-entity "光引GEO" \
  --target-aliases "光引" \
  --entity-type company \
  --brands-file brands.txt \
  --semantic-review auto \
  --out-dir runs/chatgpt-geo/report
```

Outputs:

- `runs/chatgpt-geo/report/summary.json`
- `runs/chatgpt-geo/report/structured-data.md`
- `runs/chatgpt-geo/report/structured-data.xlsx`
- `runs/chatgpt-geo/report/report.html`
- `runs/chatgpt-geo/report/semantic-review-cache.json` when AI semantic review produces reusable candidate classifications

The standard report requires `--target-entity` and `--entity-type` when those fields are not already stored in `chatgpt-crawl.json`. Entity type accepts `person/人`, `company/公司`, or `product/产品`. Target matching uses contains logic plus aliases, and competitors are limited to the same entity type as the target. The report compares mention rate, average mentions per valid answer, Top 1 / Top 3 / Top 5 probability, average rank, dominant sentiment, negative share, source mentions, title intent, clickable repeated citations, normalized target-vs-best-3 radar scoring, click-to-reveal bubble benchmarking, compact domain treemap, and GEO recommendations with priority charts and conservative trend projections. `structured-data.md` and `structured-data.xlsx` contain the same cleaned tables for overview fields, output file paths, semantic review status, question coverage, target metrics, same-type entity comparison, entity-recognition candidates, source/channel data, and title features.

Semantic review options:

- `--semantic-review auto`: default. Use AI review when `OPENAI_API_KEY` is available; otherwise fall back to local rules and record `semantic_review_status: fallback`.
- `--semantic-review required`: fail analysis if AI review is unavailable, incomplete, or invalid. Use this for formal delivery when semantic review must be enforced.
- `--semantic-review off`: skip AI review and use local rules only.
- `--semantic-confidence-threshold 0.72`: minimum confidence for AI-reviewed direct competitors.
- `--semantic-review-cache <path>`: cache path, defaulting to `<out-dir>/semantic-review-cache.json`.

Semantic review is an enhancement layer, not a replacement for hard evidence. Candidates must still pass noise filtering, type consistency, repeated answer-body evidence, surface/evidence score gates, and, when AI review is enforced, a direct-competitor semantic label. Reports and structured exports expose the semantic label, same-type flag, direct-competitor flag, competitor-matrix entry flag, confidence, source, recommended action, and exclusion reason.

If no brand list is supplied, the analyzer infers same-type candidate entities and marks the report as inferred/lower-confidence.

## Offline Verification

```bash
node --check scripts/chatgpt_browser_crawl.mjs
node --check scripts/chatgpt_batch_crawl.mjs
node --check scripts/test_chatgpt_batch_delay.mjs
node scripts/test_chatgpt_batch_delay.mjs
python3 -m py_compile scripts/analyze_chatgpt_results.py
python3 -m py_compile scripts/test_entity_recognition.py
python3 scripts/test_entity_recognition.py
python3 scripts/analyze_chatgpt_results.py fixtures/sample-chatgpt-crawl.json \
  --target-entity '光引GEO' \
  --entity-type company \
  --brands '光引GEO,源易信息,PallasAI' \
  --out-dir /tmp/yao-chatgpt-crawler-report
```

## Run Boundaries

- This skill does not solve ChatGPT login, CAPTCHA, rate limiting, account restrictions, or platform bypass.
- Probability metrics are repeated-sample estimates, not official ChatGPT rankings or market share.
- Competitor recognition should prefer a user-provided alias table when available. Automatic candidate inference is auditable but lower-confidence; formal reports should use `--semantic-review required` when AI semantic review is needed.
- AI semantic review is optional and cannot override hard rules, answer-body evidence requirements, or raw log auditability.

## Package Map

- `SKILL.md`: route trigger and workflow skeleton
- `references/user-setup-and-usage.md`: install prerequisites and end-user runbook
- `references/chatgpt-crawl-workflow.md`: local crawler setup and run rules
- `references/report-contract.md`: JSON contract and metric definitions
- `scripts/preflight.mjs`: dependency and login-state checker
- `scripts/chatgpt_browser_crawl.mjs`: single ChatGPT web sample collector
- `scripts/chatgpt_batch_crawl.mjs`: repeated crawl orchestrator
- `scripts/test_chatgpt_batch_delay.mjs`: delay preset and delay strategy regression checks
- `scripts/analyze_chatgpt_results.py`: aggregation and Kami-styled HTML rendering
- `scripts/test_entity_recognition.py`: local entity-recognition regression checks
- `fixtures/sample-chatgpt-crawl.json`: offline test fixture
