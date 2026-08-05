---
name: wepr-geoflow
description: 开发或运营 GEOFlow，覆盖 Laravel 后端、管理后台、API、命令行、默认站点、主题、线索及渠道站点。适用于代码修改、线上系统操作、前端与模板调整、渠道能力同步、旧 PHP 模板迁移，以及兼容 wepr-geoflow-cli、wepr-geoflow-design 和 wepr-geoflow-template 等入口。执行前必须确认真实路由；不处理无关任务，也不得绕过数据库流程、虚构接口、规避鉴权、泄露密钥、直接复制网页或未经批准执行上线及破坏性操作。
---

# GEOFlow

## Route

1. Run `scripts/discover_geoflow_workspace.py <workspace>` for source work or `scripts/geoflow_preflight.sh "<workspace>" [config] [checks]` before runtime mutations. Inspect current CLI help and routes when available.
2. Load one route:

- `development`: [development-workflow.md](references/development-workflow.md) and [system-capability-discovery.md](references/system-capability-discovery.md)
- `operations`: [operation-boundary.md](references/operation-boundary.md), [command-map.md](references/command-map.md), and [geoflow-current-capability-map.md](references/geoflow-current-capability-map.md)
- `public_frontend`: [frontend-resource-index.md](references/frontend-resource-index.md) and [geoflow-frontend-map.md](references/geoflow-frontend-map.md)
- `channel_frontend`: [frontend-resource-index.md](references/frontend-resource-index.md) and [channel-frontend-contract.md](references/channel-frontend-contract.md)
- `legacy_migration`: [legacy-template-migration.md](references/legacy-template-migration.md) and [legacy-skill-id-migration.md](references/legacy-skill-id-migration.md)

3. Mixed work follows: discover, implement, test or preview, approved finalize.

## Mode Boundaries

Each phase has one mode. `development` edits code and tests; `operations` uses supported runtime interfaces; `public_frontend` prepares themes or payloads; `channel_frontend` handles target-package contracts. Switch modes when crossing these boundaries. Keep authenticated form creation, sync, activation, and publication as confirmed operations phases.

## Guardrails

- Follow repository rules and focused tests.
- Run bundled helpers on macOS, Linux, or WSL with Python 3.10+ and Bash where required; runtime preflight also needs `curl`, and live channel reports need PHP CLI plus a working project `artisan`. If a dependency is unavailable, stay in read-only discovery, report the missing verification layer, and do not claim live success.
- Preserve authentication, CSRF, idempotency, permissions, readback, contracts, and secret redaction.
- Separate preview, import, sync, activation, publication, updates, rollback, and destructive actions. Require the exact target and explicit approval for high-risk steps.
- Report the selected mode, evidence, touched files/routes/resources, verification, final state, and remaining risks.
