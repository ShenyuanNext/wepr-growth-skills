#!/usr/bin/env python3
"""Validate the wepr-seo package contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "manifest.json",
    "references/audit-playbook.md",
    "references/page-audit-checks.md",
    "references/technical-seo.md",
    "references/execution-sampling.md",
    "references/ai-search.md",
    "references/content-quality.md",
    "references/performance-measurement.md",
    "references/international-commerce.md",
    "references/vertical-search.md",
    "references/engine-matrix.md",
    "references/knowledge-freshness.md",
    "references/audit-contract.md",
    "references/evidence-policy.md",
    "references/keyword-content.md",
    "references/official-sources.md",
    "schemas/seo-audit.schema.json",
    "data/seo-source-registry.json",
    "assets/report-template.html",
    "LICENSE-JEFF.md",
    "scripts/check-site.py",
    "scripts/check-page.py",
    "scripts/fetch-page.py",
    "scripts/check-schema.py",
    "scripts/check-social.py",
    "scripts/check-pagespeed.py",
    "scripts/validate_knowledge.py",
)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    result: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"\'')
    return result


def validate(root: Path) -> dict[str, object]:
    root = root.resolve()
    failures: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            failures.append(f"missing required file: {relative}")

    nested = [
        str(path.relative_to(root))
        for path in root.rglob("SKILL.md")
        if path != root / "SKILL.md" and ".git" not in path.parts
    ]
    if nested:
        failures.append("nested discoverable SKILL.md files: " + ", ".join(sorted(nested)))

    skill_path = root / "SKILL.md"
    if skill_path.exists():
        text = skill_path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        if frontmatter.get("name") != "wepr-seo":
            failures.append("SKILL.md name must be wepr-seo")
        description = frontmatter.get("description", "").lower()
        for phrase in ("seo", "audit", "keyword", "exclude"):
            if phrase not in description:
                warnings.append(f"description may be missing routing phrase: {phrase}")
        for link in re.findall(r"\]\((references/[^)]+\.md)\)", text):
            if not (root / link).is_file():
                failures.append(f"SKILL.md links to missing reference: {link}")

    for relative in ("manifest.json", "schemas/seo-audit.schema.json", "data/seo-source-registry.json"):
        path = root / relative
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                failures.append(f"{relative}: invalid JSON: {exc}")
                continue
            if not isinstance(payload, dict):
                failures.append(f"{relative}: expected object")

    return {"ok": not failures, "root": str(root), "failures": failures, "warnings": warnings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the wepr-seo skill package.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    args = parser.parse_args()
    result = validate(Path(args.skill_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
