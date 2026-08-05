#!/usr/bin/env python3
"""Validate Qiaomu SEO's official-source registry and stale-claim guard."""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REQUIRED_SOURCE_FIELDS = (
    "id",
    "authority",
    "topic",
    "url",
    "stability",
    "reviewed_at",
    "review_after_days",
)
STABILITIES = {"stable", "mutable", "volatile"}
LIFECYCLE_STATUSES = {"experimental", "limited", "supported", "unsupported", "deprecated", "removed"}


def parse_date(value: Any, label: str, failures: list[str]) -> date | None:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        failures.append(f"{label} must be an ISO date")
        return None


def validate_registry(payload: dict[str, Any], root: Path, as_of: date) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    if payload.get("schema_version") != "1.0":
        failures.append("registry schema_version must be 1.0")

    allowed_domains = payload.get("allowed_official_domains")
    if not isinstance(allowed_domains, list) or not allowed_domains:
        failures.append("allowed_official_domains must be a non-empty array")
        allowed_domains = []
    allowed = {str(item).lower() for item in allowed_domains}

    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        failures.append("sources must be a non-empty array")
        sources = []

    source_ids: set[str] = set()
    source_urls: set[str] = set()
    overdue: list[str] = []
    for index, source in enumerate(sources):
        prefix = f"sources[{index}]"
        if not isinstance(source, dict):
            failures.append(f"{prefix} must be an object")
            continue
        for field in REQUIRED_SOURCE_FIELDS:
            if field not in source:
                failures.append(f"{prefix} missing field: {field}")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id.strip():
            failures.append(f"{prefix}.id must be a non-empty string")
        elif source_id in source_ids:
            failures.append(f"duplicate source id: {source_id}")
        else:
            source_ids.add(source_id)

        url = source.get("url")
        if not isinstance(url, str):
            failures.append(f"{prefix}.url must be a string")
        else:
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                failures.append(f"{prefix}.url must be an absolute HTTPS URL")
            elif parsed.netloc.lower() not in allowed:
                failures.append(f"{prefix}.url domain is not in allowed_official_domains: {parsed.netloc}")
            if url in source_urls:
                failures.append(f"duplicate source URL: {url}")
            source_urls.add(url)

        if source.get("authority") != "official":
            failures.append(f"{prefix}.authority must be official")
        if source.get("stability") not in STABILITIES:
            failures.append(f"{prefix}.stability must be one of {sorted(STABILITIES)}")
        reviewed_at = parse_date(source.get("reviewed_at"), f"{prefix}.reviewed_at", failures)
        cadence = source.get("review_after_days")
        if not isinstance(cadence, int) or isinstance(cadence, bool) or cadence <= 0:
            failures.append(f"{prefix}.review_after_days must be a positive integer")
        elif reviewed_at and as_of > reviewed_at + timedelta(days=cadence):
            overdue.append(str(source_id))

    if overdue:
        warnings.append("overdue source reviews: " + ", ".join(sorted(overdue)))

    lifecycle = payload.get("feature_lifecycle", [])
    if not isinstance(lifecycle, list):
        failures.append("feature_lifecycle must be an array")
        lifecycle = []
    lifecycle_ids: set[str] = set()
    for index, item in enumerate(lifecycle):
        prefix = f"feature_lifecycle[{index}]"
        if not isinstance(item, dict):
            failures.append(f"{prefix} must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            failures.append(f"{prefix}.id must be a non-empty string")
        elif item_id in lifecycle_ids:
            failures.append(f"duplicate lifecycle id: {item_id}")
        else:
            lifecycle_ids.add(item_id)
        if item.get("status") not in LIFECYCLE_STATUSES:
            failures.append(f"{prefix}.status must be one of {sorted(LIFECYCLE_STATUSES)}")
        if item.get("source_id") not in source_ids:
            failures.append(f"{prefix} references unknown source_id: {item.get('source_id')}")
        parse_date(item.get("as_of"), f"{prefix}.as_of", failures)

    patterns = payload.get("deprecated_claim_patterns", [])
    if not isinstance(patterns, list):
        failures.append("deprecated_claim_patterns must be an array")
        patterns = []
    scan_files = [root / "SKILL.md"] + sorted((root / "references").glob("*.md"))
    for pattern in patterns:
        if not isinstance(pattern, str) or not pattern.strip():
            failures.append("deprecated_claim_patterns items must be non-empty strings")
            continue
        for path in scan_files:
            if path.is_file() and pattern.casefold() in path.read_text(encoding="utf-8").casefold():
                failures.append(f"deprecated claim found in {path.relative_to(root)}: {pattern}")

    return {
        "ok": not failures,
        "source_count": len(sources),
        "lifecycle_count": len(lifecycle),
        "overdue_sources": sorted(overdue),
        "failures": failures,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Qiaomu SEO knowledge freshness.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    parser.add_argument("--as-of", help="Evaluation date in YYYY-MM-DD; defaults to today.")
    parser.add_argument("--strict-stale", action="store_true", help="Fail when any source review is overdue.")
    args = parser.parse_args()
    root = Path(args.skill_dir).resolve()
    registry_path = root / "data" / "seo-source-registry.json"
    try:
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "failures": [str(exc)], "warnings": []}, ensure_ascii=False, indent=2))
        raise SystemExit(2) from exc
    if not isinstance(payload, dict):
        result = {"ok": False, "failures": ["registry root must be an object"], "warnings": []}
    else:
        failures: list[str] = []
        as_of = parse_date(args.as_of, "--as-of", failures) if args.as_of else date.today()
        if as_of is None:
            result = {"ok": False, "failures": failures, "warnings": []}
        else:
            result = validate_registry(payload, root, as_of)
            if args.strict_stale and result["overdue_sources"]:
                result["failures"].append("source review is overdue under --strict-stale")
                result["ok"] = False
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
