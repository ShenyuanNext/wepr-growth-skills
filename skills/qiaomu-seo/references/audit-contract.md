# Machine-Readable Audit Contract

Use the JSON contract when findings must feed engineering, ticketing, dashboards, or repeated audits. Markdown remains the default human report.

Schema: `schemas/seo-audit.schema.json`  
Validator: `python3 scripts/validate_audit.py audit.json`

## Top-level sections

- `schema_version`
- `generated_at`
- `scope`: work mode, targets, market, device, evidence modes
- `coverage`: discovered/selected/fetched/rendered/data-backed counts, failures, limitations
- `findings`: evidence-bound issues and passes
- `action_plan`: ordered work tied to finding IDs
- `missing_evidence`
- optional `source_review`: review date, registry source IDs, and overdue sources for mutable platform claims

## Finding rules

- `impact` and `confidence` are separate.
- `observed` and `inferred` findings need evidence references.
- `missing evidence` findings use `not_checked` or `warning`, never a confirmed `pass` or `fail`.
- Every fix includes a verification method.
- Finding IDs are unique and action-plan items reference existing IDs.
- Name `engine_scope` when a finding applies only to Google, Bing, OpenAI, Perplexity, or another provider.
- Mutable structured-data, commerce, vertical-search, AI-search, or policy findings should include `source_review`.

Validation proves structural consistency, not SEO correctness. Human/source review remains required.
