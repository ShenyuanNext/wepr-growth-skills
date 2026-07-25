# User Setup And Usage

This guide is for a user who has just installed `yao-chatgpt-crawler` and wants to run real ChatGPT web crawls.

## What This Skill Needs

Fresh crawling requires local browser automation. The skill does not install OpenCLI, log in to ChatGPT, solve CAPTCHA, or bypass account checks.

Required for fresh crawls:

- Node.js 18+.
- Python 3.10+.
- OpenCLI CLI 1.8.4+ available as `opencli`.
- OpenCLI Browser Bridge extension connected to a Chrome or Edge profile.
- A ChatGPT web session in that connected profile that can send messages.
- ChatGPT Web Search or visible ChatGPT source links when source analysis is required.
- The bundled ChatGPT browser crawler at `scripts/chatgpt_browser_crawl.mjs`. If using a compatible replacement, pass `--crawler-script <file>` or set `CHATGPT_CRAWLER_SCRIPT`.

Required for analysis-only usage:

- Node.js 18+.
- Python 3.10+.
- An existing `chatgpt-crawl.json` or compatible ChatGPT raw JSON.
- Optional `OPENAI_API_KEY` if you want AI semantic review for competitor entities. Without it, `--semantic-review auto` uses local-rule fallback.

## 1. Run Preflight

From the skill directory:

```bash
node scripts/preflight.mjs --profile <opencli-profile>
```

If the crawler script is not in the default local path:

```bash
node scripts/preflight.mjs \
  --profile <opencli-profile> \
  --crawler-script /absolute/path/to/chatgpt_browser_crawl.mjs
```

For report generation from an existing JSON only:

```bash
node scripts/preflight.mjs --analysis-only
```

Preflight must pass before a fresh crawl. A `ChatGPT login` warning means the page reports `Login=Yes` but `whoami` could not read a full session cookie; answer-only crawls may still work, while account-specific tools such as Web Search may fail.

## 2. Prepare Questions

Before running a standard report, prepare these inputs:

```text
1. 关键词：one or more ChatGPT questions, one per line
2. 轮询次数：how many times each keyword should be queried
3. 目标实体：the entity to diagnose, for example 光引GEO or 新东方
4. 实体类型：人, 公司, or 产品
5. OpenCLI profile：the connected Edge or Chrome Browser Bridge profile
6. 单次查询间隔：default random 30s-1m; optional 1-3m or 3-10m random interval
7. 可选别名/竞品表：reviewed target aliases and same-type competitors
```

Create a questions file with one keyword/question per line:

```text
出国留学公司推荐
出国留学机构
出国留学机构哪家好
出国留学公司哪家好
出国留学哪家靠谱
```

JSON input is also accepted:

```json
[
  {"id": "q01", "question": "出国留学公司推荐", "repeat": 5},
  {"id": "q02", "question": "出国留学机构", "repeat": 5}
]
```

## 3. Prepare Target Entity Aliases

The target entity and entity type are required for standard reports. Entity aliases make Top 1, Top 3, Top 5, mention rate, and average-rank metrics more reliable.

Target matching uses contains logic plus aliases. If the target entity is `新东方`, aliases or extracted names such as `新东方前途出国` and `前途出国` can be merged into the target row. Short Latin aliases such as `AI` or `GEO` only match standalone tokens, not longer names. Competitors are kept only when they match the same entity type.

Company example `brands.txt`:

```text
启德教育|启德留学|启德
新东方前途出国|新东方|前途出国
指南者留学|指南者
优越留学|优越教育
```

If no alias/competitor file is supplied, the analyzer infers same-type candidate entities and labels the result as inferred/lower-confidence. Use inferred competitors for exploration, not final reporting.

## 4. Dry Run

Check the plan before opening ChatGPT:

```bash
node scripts/chatgpt_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/my-chatgpt-run \
  --dry-run
```

Expected output should show the planned sample count. Five questions repeated five times should produce 25 samples.
Dry-run only validates the plan and target fields; it does not require the crawler script, OpenCLI profile, or ChatGPT page to be available. Real crawling still requires all fresh-crawl prerequisites.

## 5. Run Fresh Crawl

For real ChatGPT web runs, use a random delay preset. The default is random `30s-1m`; use `1-3m` or `3-10m` when you want to lower request frequency.

```bash
node scripts/chatgpt_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --target-aliases "新东方前途出国,前途出国" \
  --entity-type company \
  --out-dir runs/my-chatgpt-run \
  --delay-preset 1-3m \
  --timeout 300
```

The crawler requests ChatGPT Web Search by default. Add `--no-search` when you want answer-only sampling, `--model instant|thinking|pro` when a specific web mode is needed, or `--deep-research --timeout <seconds>` for deliberate Deep Research runs. `--model` changes the current ChatGPT web mode in the connected session. If OpenCLI reports `Could not find the ChatGPT Web Search tool option`, the crawler retries without the explicit toggle and still captures visible citation pills, source-flyout links, markdown links, or bare URLs when the ChatGPT account displays them.

Delay presets:

- `--delay-preset 30s-1m`: default; random 30-60 seconds between fresh samples.
- `--delay-preset 1-3m`: balanced; useful for moderate runs.
- `--delay-preset 3-10m`: conservative; slower but reduces request frequency.
- `--safe-random-delay`: alias for `--delay-preset 3-10m`.

Five questions repeated five times means 25 samples and 24 waits. With the default interval, waiting time is roughly 12-24 minutes; with `1-3m`, roughly 24-72 minutes; with `3-10m`, roughly 72-240 minutes. Slower random intervals reduce request frequency but do not guarantee account safety or bypass platform risk controls.

Use a custom random interval when needed:

```bash
node scripts/chatgpt_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/my-chatgpt-run \
  --delay-min-minutes 5 \
  --delay-max-minutes 20
```

If your crawler script is outside the default path:

```bash
node scripts/chatgpt_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --crawler-script /absolute/path/to/chatgpt_browser_crawl.mjs \
  --delay-preset 3-10m \
  --out-dir runs/my-chatgpt-run
```

Outputs:

- `runs/my-chatgpt-run/chatgpt-crawl.json`
- `runs/my-chatgpt-run/raw/*.json`
- `runs/my-chatgpt-run/logs/*.log`

Each sample starts a fresh ChatGPT conversation by default. Keep the run single-threaded unless the replacement crawler explicitly supports concurrency.

## 6. Resume Interrupted Runs

If the run stops midway, rerun the same command with `--resume`:

```bash
node scripts/chatgpt_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/my-chatgpt-run \
  --resume
```

Resume only reuses raw JSON when it is valid, successful, has answer text, and matches the current question.

## 7. Generate The Report

```bash
python3 scripts/analyze_chatgpt_results.py \
  runs/my-chatgpt-run/chatgpt-crawl.json \
  --target-entity "新东方" \
  --target-aliases "新东方前途出国,前途出国" \
  --entity-type company \
  --brands-file brands.txt \
  --semantic-review auto \
  --title "ChatGPT 搜索概率分析报告" \
  --out-dir runs/my-chatgpt-run/report
```

Outputs:

- `runs/my-chatgpt-run/report/summary.json`
- `runs/my-chatgpt-run/report/structured-data.md`
- `runs/my-chatgpt-run/report/structured-data.xlsx`
- `runs/my-chatgpt-run/report/report.html`
- `runs/my-chatgpt-run/report/semantic-review-cache.json` when AI semantic review produces cacheable results

The analyzer keeps `summary.json` as a machine-readable metric summary. `structured-data.md` and `structured-data.xlsx` contain the same cleaned structured tables: output file list, overview fields, semantic review status, question coverage, target metrics, same-type entity comparison, question-by-entity metrics, entity recognition candidates, semantic labels and reasons, source/channel tables, frequent domains/sources/URLs/titles, and title-feature buckets. The HTML report defaults to Simplified Chinese and includes a top-right language toggle for English overview analysis. It starts with a numeric overview, directory, and metric explanations. It then includes core conclusions, target-vs-competitor comparison, sentiment analysis, average mention count, sample coverage, target entity recognition, mention probability, Top 1 / Top 3 / Top 5 probability, average rank, source channels, repeated domains, clickable repeated URLs/titles, title-feature and title-intent charts, and GEO optimization recommendations. Domain displays use readable Chinese names where available. High-frequency URL rows show one clickable compact label per row, keep the full URL as link target/hover title, and avoid visually duplicated URL lines. GEO recommendations include priority bars, a conservative core-metric trend projection, method/check tables, and concise action cards. Detail lists are capped at 10 rows by default.

Semantic review options:

- `--semantic-review auto`: default. AI review runs when `OPENAI_API_KEY` is available. If AI is unavailable or fails, the analyzer falls back to local rules and records `semantic_review_status: fallback`.
- `--semantic-review required`: recommended for formal delivery when semantic review must be enforced. The analyzer fails if AI review is unavailable, incomplete, or invalid.
- `--semantic-review off`: only local rules are used.
- `--semantic-confidence-threshold 0.72`: minimum confidence for AI-reviewed direct competitors.
- `--semantic-review-cache <path>`: optional cache path; default is `semantic-review-cache.json` in the report directory.

Semantic review does not replace raw evidence. A competitor must still pass the local hard gates: not noise, not a generic category or attribute phrase, same entity type as the target, enough confidence, and at least one answer-body evidence snippet rather than source-title-only evidence.

Accepted standard entity types are `person/人`, `company/公司`, and `product/产品`.

## 8. Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `opencli: command not found` | OpenCLI is not installed or not on `PATH`. | Install OpenCLI and verify `opencli --version`. |
| `No Browser Bridge profiles connected` | Browser extension is not connected. | Open the Chrome or Edge profile with OpenCLI Browser Bridge enabled, then run `opencli profile list`. |
| `Browser profile ... is not connected` | The selected profile is offline. | Use `opencli profile list`, then pass a connected profile with `--profile`. |
| `logged_in: false` | ChatGPT is not logged in. | Log in to ChatGPT in the connected browser, then run `opencli chatgpt whoami -f json`. |
| `Could not find the ChatGPT Web Search tool option` | The current account, model, locale, or session does not expose the explicit Web Search toggle to OpenCLI. | The crawler retries without the explicit toggle; inspect `raw.web_search_fallback` and `references.items` to see whether visible sources were still captured. |
| `Crawler script not found` | The bundled crawler is missing or a custom path is wrong. | Repair `scripts/chatgpt_browser_crawl.mjs`, pass `--crawler-script <file>`, or set `CHATGPT_CRAWLER_SCRIPT`. |
| `Semantic review is required, but OPENAI_API_KEY is not set` | `--semantic-review required` was used without an AI API key. | Set `OPENAI_API_KEY`, provide a valid semantic-review cache, or rerun with `--semantic-review auto/off` for exploratory analysis. |
| `references.count = 0` | ChatGPT answered without visible external URLs, Web Search was off, or citations/source controls were not exposed in the DOM or answer text. | Confirm search mode, rerun one sample, and inspect the raw answer/log. |
| Many samples fail after several successes | Browser bridge, account throttling, ChatGPT page instability, or platform risk controls. | Stop the run, wait before retrying, use `--delay-preset 3-10m` or wider custom random intervals, rerun with `--resume`, and inspect failed logs. |

## Evidence And Privacy

The run directory stores raw ChatGPT answers, source titles, URLs, and logs. Treat it as audit evidence. Do not publish or commit run outputs if the questions, answers, or sources contain private or client-sensitive information.
