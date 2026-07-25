<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-chatgpt-crawler
Created by: 姚金刚
Date: 2026-06-25
X: https://x.com/yaojingang
-->

# ChatGPT AI Search Crawl Brief

## Run Basics

- Project / client:
- Target entity:
- Target entity aliases:
- Entity type: person / company / product
- Market / language:
- Report language:
- OpenCLI profile:
- ChatGPT account state:
- ChatGPT Web Search available: yes / no / unknown

## Questions

Put one question per line.

```text
国内目前最值得关注的大模型有哪些？
中国大模型排名前十的公司和产品分别是什么？
现在国产大模型里，哪些模型的推理和代码能力最强？
国产大模型主要可以分为哪些类型，各自适合什么场景？
如果企业要接入国产大模型，应该优先选择哪些模型？
```

## Sampling

- Repeat count per question:
- Single-query interval preset: 30s-1m / 1-3m / 3-10m
- Use `--safe-random-delay`: yes / no
- Resume interrupted run: yes / no
- Timeout per sample:
- Search mode: ChatGPT Web Search / answer-only / Deep Research
- Model mode, if fixed: instant / thinking / pro / leave current mode

Default fresh crawls use a random `30s-1m` interval. Use `1-3m` or `3-10m` when the run is long or the account should be used more conservatively. Slower intervals reduce request frequency; they do not bypass account limits or guarantee account safety.

## Alias And Competitor Table

Use one entity per line. Put aliases after `|`. Keep competitors in the same entity type as the target.

```text
豆包|Doubao|豆包大模型|豆包模型
通义千问|Qwen|千问|Qwen3|Qwen2.5
DeepSeek|DeepSeek-V3|DeepSeek-R1|深度求索
Kimi|Kimi K2|Kimi大模型|Moonshot Kimi
```

## Semantic Review

- Mode: auto / required / off
- Confidence threshold:
- `OPENAI_API_KEY` available: yes / no
- Manual review owner:
- Terms that should be treated as noise or generic concepts:

## Output

- Output directory:
- Report title:
- Keep raw evidence privately: yes / no
- Public example needs path/profile/session sanitization: yes / no
- Required files:
  - `chatgpt-crawl.json`
  - `report/summary.json`
  - `report/structured-data.md`
  - `report/structured-data.xlsx`
  - `report/report.html`
