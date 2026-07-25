---
name: yao-geo-article-friendly
description: Optimize an existing article or local article file into a GEO and AI-search-friendly rewrite with source-bound evidence, structure, semantic density, scoring, and change notes. Use for article rewriting and citation-readiness improvement; do not use for new articles, invented citations/data, compliance audits, ranking guarantees, or generic GEO strategy.
metadata:
  author: Yao Team
  maturity: scaffold
---

# Yao GEO Article Friendly

## Use

Use when the user provides pasted article text or a local path and wants a GEO/AI 搜索友好化改造 with evidence, structure, readability, and before/after scoring.

Accepted inputs: pasted text, `.md`, `.txt`, `.html`, `.htm`, `.docx`, and `.pdf` when local extraction is available. If the article cannot be read, return a blocker and ask for pasted text.

Do not use for topic-only drafting, legal/compliance judgments, ranking promises, competitor attacks, takedown work, or unsupported statistics, sources, quotes, cases, or claims.

## Required Reading

- `references/geo-article-transformation-method.md`: weighted method, evidence rules, and validation.
- `references/geo-output-contract.md`: final Markdown structure, scoring, and change-note templates.

## Workflow

1. Resolve input and preserve the original title, claims, facts, examples, and tone. Default to `standard` depth.
2. Inventory core claims, evidence, data, quotes, cases, structure, entities, terms, and reusable passages.
3. Score the original against the weighted GEO dimensions plus risk control; be conservative when sources, data口径, or quotes are missing.
4. Rewrite by priority: evidence, structure, fluency, semantic density, authority signals, terminology, robustness, cross-domain links, and readability.
5. Mark unsupported enhancements as `[建议补充...]`; state facts only when original-supported or verified.
6. Return the optimized article, score report, change notes, supplement list, and risk notes.
7. Verify original meaning, no fabrication, high-weight improvements, and natural readability.

## Evidence Discipline

Use `原文支持`, `外部已核验`, and `建议补充` labels when provenance matters.

If current laws, platform rules, market data, rankings, product facts, or recent research are needed, verify them with current primary or authoritative sources before insertion. When verification is not possible, keep the claim as `建议补充`.

## Output Contract

Default artifact: one structured Markdown response containing:

1. `改造后的完整文章`
2. `GEO优化度评分`
3. `改造执行说明`
4. `需要用户补充或确认的内容`
5. `改造风险提示`

If the user asks for a file, save the Markdown artifact and return the absolute path.

## Reference Map

- `references/geo-article-transformation-method.md`: method and scoring basis.
- `references/geo-output-contract.md`: output templates.
- `reports/`: prompt-quality, output-risk, artifact-design, and reference scan.
