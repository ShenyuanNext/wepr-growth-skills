---
name: operate-georank-workbench
description: Safely operate a self-hosted GEOrank instance through its HTTP API. Use for GEOrank登录、账户检查、网站诊断、诊断报告读取、方案对话、关键词拓展、用量查询，以及经明确授权的管理员配置与内容管理。Do not use for general GEO consulting or strategy when no running GEOrank instance is involved.
---

# Operate GEOrank Workbench

Operate a running GEOrank instance with explicit access checks, dry runs, secret redaction, and execution receipts.

> Adapted and renamed for the WEPR skill collection from the Apache-2.0 GEOrank operator skill. The workflow and bundled client have been modified and redistributed under the upstream license; see `LICENSE` and the repository third-party notices.

## Workflow

1. Confirm the instance base URL. Use `http://localhost:8000` only for a local instance; remote instances must use HTTPS.
2. Resolve authentication without asking the user to choose a role:
   - `python3 scripts/georank_client.py login --account <account>`
   - `python3 scripts/georank_client.py whoami`
   - Enable administrator actions only when `/api/auth/me` returns `role=admin`.
3. Read [references/user-capabilities.md](references/user-capabilities.md) for public and user-owned operations. Read [references/admin-capabilities.md](references/admin-capabilities.md) only for administrator work.
4. Execute reads directly with `call GET`. Treat every non-read call as a side effect.
5. For writes, run the request without `--execute`, show the redacted preflight, and execute only when the user clearly authorizes that exact change.
6. Before administrator writes, read [references/safety-policy.md](references/safety-policy.md) and apply the required confirmation phrase.
7. Return a receipt: access level, operation, target, dry-run/executed state, API status, resource ID, request ID, redacted summary, next step, and rollback guidance when relevant.

## Common operations

```bash
# Read current identity
python3 scripts/georank_client.py whoami

# Start a diagnosis: preflight first, then execute
python3 scripts/georank_client.py call POST /api/diagnostics/ --json-file /tmp/diagnosis.json
python3 scripts/georank_client.py call POST /api/diagnostics/ --json-file /tmp/diagnosis.json --execute

# Expand keywords
python3 scripts/georank_client.py call POST /api/keywords/expand --json-file /tmp/keywords.json
```

## Safety boundaries

- Never place passwords, tokens, API keys, cookies, or credentials in chat, command arguments, reports, fixtures, or commits.
- Login reads a hidden prompt or `GEORANK_PASSWORD`; calls read `GEORANK_TOKEN` or the protected session file.
- User/public writes require `--execute`; administrator writes require `--execute --confirm APPLY_ADMIN_CHANGE`.
- Deletes require the exact `DELETE:<api-path-with-query>` confirmation.
- Stop on ambiguous targets, insufficient permissions, missing rollback for high-impact changes, or an unknown write outcome after a network failure.
- Do not represent GEOrank diagnostics as guaranteed rankings or recommendations by any AI platform.

## Reference map

- [references/user-capabilities.md](references/user-capabilities.md): public and ordinary-user API operations.
- [references/admin-capabilities.md](references/admin-capabilities.md): administrator operation groups and gates.
- [references/safety-policy.md](references/safety-policy.md): authentication, secrets, side effects, polling, and rollback.
- `scripts/georank_client.py`: deterministic, standard-library API client.
- `tests/test_georank_client.py`: client safety and behavior tests.
