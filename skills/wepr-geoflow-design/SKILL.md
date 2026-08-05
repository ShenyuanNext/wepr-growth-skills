---
name: wepr-geoflow-design
description: 规划和预览 GEOFlow 默认站点及渠道站点的前端体验，覆盖 Laravel Blade 主题、首页模块与样式配置、线索表单、主题编辑器、目标主题包能力和跨渠道同步。适用于主题盘点、参考站映射、首页搭建、渠道能力审计和先预览后上线的设计迭代；不用于命令行运营、后端开发、线索表单增删改查、直接复制网页、未经支持的远程修改或直接上线。
---

# WEPR GEOFlow Design

Use this skill for current GEOFlow frontend experience work. It owns design/planning and preview artifacts, not live activation or backend changes.

## Boundary

- Owns Laravel Blade theme discovery, preview edit sessions, reference-site mapping, homepage `homepage-design.json`, `lead_form` modules with existing `lead_form_slug`, default-vs-channel frontend comparison, target-package capability gaps, and sync-preview planning.
- Excludes backend/routes/models/migrations, lead-form CRUD, CLI operations, direct production activation, raw HTML copying, and unsupported remote PHP edits.
- Use `wepr-geoflow-cli` for operational admin web actions such as creating lead forms, exporting leads, publishing theme-editor drafts, or running system updates.

## Required Checks

1. Confirm a GEOFlow Laravel workspace: `artisan`, `routes/web.php`, `resources/views/site`, `resources/views/theme`.
2. Run `scripts/discover_themes.py` and `scripts/discover_frontend_surfaces.py`.
3. Choose `target_surface`: `default_site`, `channel_site`, `cross_channel_sync`, or `template_mapping`.
4. Prefer reviewed `homepage-design.json` over Blade edits when HomepageModuleBuilder/import exists.
5. For `lead_form`, require an existing active slug and output canonical `lead_form_slug`; do not create the form here.
6. For channel sync, compare default-site supported modules with target-package `frontend-capabilities`; downgrade unsupported `lead_form` to CTA/link or require target upgrade.
7. Keep preview/import/sync/activation as separate confirmation steps.

## References

Read [geoflow-frontend-map.md](references/geoflow-frontend-map.md), [homepage-composition-guide.md](references/homepage-composition-guide.md), and [template-boundary.md](references/template-boundary.md) for default-site work.
For channel work also read [channel-frontend-contract.md](references/channel-frontend-contract.md), [distribution-target-site-map.md](references/distribution-target-site-map.md), and [backend-connection-workflow.md](references/backend-connection-workflow.md).
For package/edit flows read [laravel-theme-contract.md](references/laravel-theme-contract.md), [theme-package-contract.md](references/theme-package-contract.md), [theme-edit-workflow.md](references/theme-edit-workflow.md), and [design-optimization-playbook.md](references/design-optimization-playbook.md).
Review [trigger_cases.json](evals/trigger_cases.json) and [upgrade report](reports/geoflow-skill-upgrade-2026-07-05.md) when checking routing.
