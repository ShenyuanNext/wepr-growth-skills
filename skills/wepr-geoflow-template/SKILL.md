---
name: wepr-geoflow-template
description: 仅用于处理旧版 GEOFlow PHP 模板包、历史模板规范，以及采用根目录 index.php、article.php、category.php、archive.php 和 includes/*.php 的旧交付物。当前 Laravel Blade 主题、参考站复刻、首页模块、线索表单、主题编辑器、渠道前端和目标主题包映射应转交 wepr-geoflow-design。不用于新前端设计、后端开发、直接复制 HTML 或线上启用。
---

# WEPR GEOFlow Template Legacy Router

Compatibility entrypoint for old GEOFlow PHP template-package notes. Current frontend work belongs in `wepr-geoflow-design`.

## Boundary

- Owns legacy output review, old PHP contract explanation, and handoff notes to `wepr-geoflow-design`.
- Excludes new Laravel Blade themes, homepage builder, `lead_form`, theme editor, channel sync, target-package mapping, backend changes, and activation.
- Old `index.php`, `article.php`, `category.php`, `archive.php`, and `includes/*.php` are legacy assumptions, not current preconditions.

## Routing

1. Current GEOFlow frontend design or reference-site cloning: use `wepr-geoflow-design`.
2. Explicit “legacy template skill” or “旧 PHP 模板包”: continue here.
3. Read [template-boundary.md](references/template-boundary.md) and [theme-package-contract.md](references/theme-package-contract.md) before interpreting old files.

## References

[template-boundary.md](references/template-boundary.md), [theme-package-contract.md](references/theme-package-contract.md), [geoflow-frontend-map.md](references/geoflow-frontend-map.md), [trigger_cases.json](evals/trigger_cases.json), [upgrade report](reports/geoflow-skill-upgrade-2026-07-05.md).
