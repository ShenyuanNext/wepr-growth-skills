# GEO Article Transformation Method

This method converts an existing article into a GEO and AI-search-friendly article while preserving the original meaning.

## Depth Modes

- `light`: optimize evidence readiness and structure only; keep the original style close.
- `standard`: default mode; improve all weighted dimensions with conservative additions.
- `deep`: restructure more aggressively and add verified external evidence when the user asks for research-backed enrichment.

For long articles over roughly 5,000 Chinese characters or 3,000 English words, work section by section, then produce one consolidated score and change report.

## Phase 1: Source-Bound Analysis

Create a brief inventory before rewriting:

- Core claims and conclusions.
- Existing evidence: data, quotes, cases, source links, methodology, and examples.
- Information density: key facts, named entities, dates, definitions, and concrete claims.
- Structure: title hierarchy, summaries, paragraph logic, tables, steps, conclusion, and FAQ readiness.
- Reusable citation material: passages that can become quote blocks, data bullets, tables, or FAQ answers.

## Phase 2: GEO Gap Diagnosis

Score the article against this 99-point weighted base model, then normalize the summary score to 100 after applying any risk-control penalty:

| Layer | Dimension | Weight |
| --- | --- | ---: |
| Evidence citation layer | Authoritative direct quotes | 16 |
| Evidence citation layer | Statistical data completeness | 14 |
| Evidence citation layer | Citability and traceable sources | 13 |
| Structure understanding layer | Heading hierarchy, summary, steps, tables, FAQ | 12 |
| Expression layer | Fluency, transitions, paragraph balance | 10 |
| Semantic matching layer | Entity coverage, question coverage, semantic density | 8 |
| Trust layer | Author, organization, method, experience, limitations | 8 |
| Professional expression layer | Accurate and consistent terminology | 6 |
| Robustness layer | Multi-source support, boundaries, counter-cases, update date | 5 |
| Cross-domain layer | Links to adjacent domains and transferable scenarios | 4 |
| Readability layer | Plain expression, short paragraphs, term explanations | 3 |
| Risk control | No keyword stuffing, no over-optimization, no fabrication | penalty |

Prioritize the first five dimensions, which carry 65 points, but do not sacrifice source fidelity or readability to chase a score.

## Phase 3: Transformation Rules

### Evidence And Citability

- Convert vague claims into source-ready statements only when the original article already supports them.
- Preserve original links, report names, expert names, samples, time ranges, and data口径.
- If a claim needs a source but none is available, write `[建议补充来源：...]`.
- If a statistic needs sample size, time range, geography, or method, write `[建议补充数据口径：...]`.
- If an expert view is only paraphrased, write `[建议补充原文引语：...]`.
- Do not invent named studies, fake percentages, sample sizes, report dates, quotes, or institutions.

### Structure

- Add a clear H1, 3-5 bullet core summary, and a logical H2/H3 hierarchy.
- Use numbered steps for processes and tables only when comparison is the main job.
- Add a conclusion that restates the article's real answer, not a new claim.
- Add FAQ only from questions the original article can answer; unsupported answers belong in `建议补充`.

### Expression And Semantics

- Split overlong paragraphs and merge fragments that repeat the same point.
- Use transition sentences only when they clarify logic.
- Expand important entities and concepts enough for retrieval, but avoid keyword stuffing.
- Define important terms on first use, then keep naming consistent.

### Authority And Robustness

- Add author, institution, method, scenario, limitation, and update-date signals only when they are known or clearly marked as suggestions.
- Add boundary notes for claims that depend on industry, market, article type, audience, or date.
- Connect to adjacent domains such as SEO, content marketing, knowledge management, and RAG only when the original topic supports the connection.

## Verification Checklist

Before returning the artifact, verify:

- All original core claims are preserved.
- No unsupported data, quote, source, case, or ranking guarantee was stated as fact.
- Every key fact is labeled or traceable.
- The first five weighted dimensions were meaningfully improved.
- The final article remains readable and natural.
- All `建议补充` items are listed in the change notes.
