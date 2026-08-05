---
name: wepr-geoflow-cli
description: 通过命令行、API v1 或已登录的管理后台操作现有 GEOFlow 2.1 及以上版本。适用于管理目录、素材、任务、作业、文章、企业知识库、增长中心线索、分发、数据分析、URL 导入、主题编辑、前端能力同步、系统更新、配置、令牌和用户，以及执行前检查。不用于代码开发、数据库结构调整、直接修改数据库、前端设计或调用未经确认的接口。
---

# WEPR GEOFlow Operations

Operate a running GEOFlow instance. Prefer supported `bin/geoflow`, then API v1 for exposed content operations, then authenticated admin web for management workflows absent from API v1.

## Boundary

- Owns operational CLI/API/admin work, CSRF/session handling, idempotency, readback verification, high-risk confirmation, and secret/personal-data redaction.
- Excludes product-code edits, migrations, direct SQL, frontend design, route invention, auth bypass, and secret exposure.
- Use `wepr-geoflow-design` for homepage/design payload planning.

## Checks

1. Confirm `artisan` or `bin/geoflow`.
2. Run `scripts/geoflow_preflight.sh "<workspace>" [config] [checks]` before first mutation.
3. Inspect CLI help, `routes/api.php`, or `php artisan route:list` before choosing a surface.
4. API fallback uses bearer auth, JSON, `Accept: application/json`, and `X-Idempotency-Key`.
5. Admin web reads the target page first, keeps CSRF/cookies, posts the owning route, then verifies readback.
6. Require explicit target/action for destructive, secret-revealing, package-download, theme-publish, bulk sync, lead export, or update-center operations.

## References

[operation-boundary.md](references/operation-boundary.md), [command-map.md](references/command-map.md), [laravel-api-v1-docker.md](references/laravel-api-v1-docker.md), [geoflow-current-capability-map.md](references/geoflow-current-capability-map.md), [trigger_cases.json](evals/trigger_cases.json), [upgrade report](reports/geoflow-skill-upgrade-2026-07-05.md).
