#!/usr/bin/env python3
"""Validate Qiaomu SEO machine-readable audit reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = (
    "schema_version",
    "generated_at",
    "scope",
    "coverage",
    "findings",
    "action_plan",
    "missing_evidence",
)
REQUIRED_SCOPE = ("mode", "targets", "market", "device", "evidence_modes")
REQUIRED_COVERAGE = (
    "discovered",
    "selected",
    "fetched",
    "rendered",
    "data_backed",
    "failed",
    "exclusions",
    "limitations",
)
REQUIRED_FINDING = (
    "id",
    "category",
    "issue",
    "status",
    "evidence_level",
    "evidence_refs",
    "impact",
    "confidence",
    "recommended_fix",
    "effort",
    "dependencies",
    "verification",
)
REQUIRED_ACTION = ("id", "finding_ids", "action", "impact", "effort", "owner", "verification")
MODES = {"advisory", "page", "template_sample", "site_inventory", "incident", "migration", "ai_search_extension"}
EVIDENCE_MODES = {"live", "code", "data", "advisory"}
STATUSES = {"pass", "warning", "fail", "not_checked"}
EVIDENCE_LEVELS = {"observed", "inferred", "missing evidence"}
IMPACTS = {"critical", "high", "medium", "low", "none"}
CONFIDENCE = {"high", "medium", "low"}
EFFORT = {"xs", "s", "m", "l", "xl", "unknown"}
CATEGORIES = {
    "discovery", "crawl", "render", "indexing", "canonical", "technical", "performance",
    "on_page", "content", "architecture", "structured_data", "international", "local",
    "commerce", "image_search", "video_search", "ai_search", "measurement", "experiment",
    "policy", "security",
}
EVIDENCE_KINDS = {
    "url", "file", "http", "rendered_dom", "search_console", "webmaster_tools", "analytics",
    "server_log", "crawl", "serp", "web_vitals_field", "lab_test", "official_doc", "other",
}
ENGINES = {"google", "bing", "openai", "perplexity", "other"}
MUTABLE_CATEGORIES = {"structured_data", "commerce", "image_search", "video_search", "ai_search", "policy"}


def require_fields(payload: dict[str, Any], fields: tuple[str, ...], prefix: str, failures: list[str]) -> None:
    for field in fields:
        if field not in payload:
            failures.append(f"{prefix} missing field: {field}")


def require_enum(value: Any, allowed: set[str], label: str, failures: list[str]) -> None:
    if value not in allowed:
        failures.append(f"{label} must be one of {sorted(allowed)}")


def require_list(value: Any, label: str, failures: list[str]) -> list[Any]:
    if not isinstance(value, list):
        failures.append(f"{label} must be an array")
        return []
    return value


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    require_fields(payload, REQUIRED_TOP_LEVEL, "audit", failures)
    if payload.get("schema_version") != "1.0":
        failures.append("schema_version must be 1.0")

    scope = payload.get("scope")
    if not isinstance(scope, dict):
        failures.append("scope must be an object")
        scope = {}
    require_fields(scope, REQUIRED_SCOPE, "scope", failures)
    require_enum(scope.get("mode"), MODES, "scope.mode", failures)
    targets = require_list(scope.get("targets"), "scope.targets", failures)
    if scope.get("mode") != "advisory" and not targets:
        failures.append("scope.targets must not be empty outside advisory mode")
    evidence_modes = require_list(scope.get("evidence_modes"), "scope.evidence_modes", failures)
    for mode in evidence_modes:
        require_enum(mode, EVIDENCE_MODES, "scope.evidence_modes item", failures)

    coverage = payload.get("coverage")
    if not isinstance(coverage, dict):
        failures.append("coverage must be an object")
        coverage = {}
    require_fields(coverage, REQUIRED_COVERAGE, "coverage", failures)
    for field in ("discovered", "selected", "fetched", "rendered", "data_backed"):
        value = coverage.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            failures.append(f"coverage.{field} must be a non-negative integer")
    for field in ("failed", "exclusions", "limitations"):
        require_list(coverage.get(field), f"coverage.{field}", failures)
    if scope.get("mode") == "template_sample" and not coverage.get("limitations"):
        warnings.append("template_sample should state coverage limitations")

    findings = require_list(payload.get("findings"), "findings", failures)
    finding_ids: set[str] = set()
    for index, raw in enumerate(findings):
        prefix = f"findings[{index}]"
        if not isinstance(raw, dict):
            failures.append(f"{prefix} must be an object")
            continue
        require_fields(raw, REQUIRED_FINDING, prefix, failures)
        finding_id = raw.get("id")
        if not isinstance(finding_id, str) or not finding_id.strip():
            failures.append(f"{prefix}.id must be a non-empty string")
        elif finding_id in finding_ids:
            failures.append(f"duplicate finding id: {finding_id}")
        else:
            finding_ids.add(finding_id)
        require_enum(raw.get("category"), CATEGORIES, f"{prefix}.category", failures)
        require_enum(raw.get("status"), STATUSES, f"{prefix}.status", failures)
        require_enum(raw.get("evidence_level"), EVIDENCE_LEVELS, f"{prefix}.evidence_level", failures)
        require_enum(raw.get("impact"), IMPACTS, f"{prefix}.impact", failures)
        require_enum(raw.get("confidence"), CONFIDENCE, f"{prefix}.confidence", failures)
        require_enum(raw.get("effort"), EFFORT, f"{prefix}.effort", failures)
        refs = require_list(raw.get("evidence_refs"), f"{prefix}.evidence_refs", failures)
        require_list(raw.get("dependencies"), f"{prefix}.dependencies", failures)
        evidence_level = raw.get("evidence_level")
        if evidence_level in {"observed", "inferred"} and not refs:
            failures.append(f"{prefix} {evidence_level} finding requires evidence_refs")
        if evidence_level == "missing evidence" and raw.get("status") not in {"warning", "not_checked"}:
            failures.append(f"{prefix} missing evidence cannot be a confirmed pass or fail")
        for ref_index, ref in enumerate(refs):
            if not isinstance(ref, dict) or not str(ref.get("kind", "")).strip() or not str(ref.get("ref", "")).strip():
                failures.append(f"{prefix}.evidence_refs[{ref_index}] requires kind and ref")
            elif ref.get("kind") not in EVIDENCE_KINDS:
                failures.append(f"{prefix}.evidence_refs[{ref_index}].kind must be one of {sorted(EVIDENCE_KINDS)}")
        engine_scope = raw.get("engine_scope")
        if engine_scope is not None:
            for engine in require_list(engine_scope, f"{prefix}.engine_scope", failures):
                require_enum(engine, ENGINES, f"{prefix}.engine_scope item", failures)

    actions = require_list(payload.get("action_plan"), "action_plan", failures)
    action_ids: set[str] = set()
    for index, raw in enumerate(actions):
        prefix = f"action_plan[{index}]"
        if not isinstance(raw, dict):
            failures.append(f"{prefix} must be an object")
            continue
        require_fields(raw, REQUIRED_ACTION, prefix, failures)
        action_id = raw.get("id")
        if not isinstance(action_id, str) or not action_id.strip():
            failures.append(f"{prefix}.id must be a non-empty string")
        elif action_id in action_ids:
            failures.append(f"duplicate action id: {action_id}")
        else:
            action_ids.add(action_id)
        refs = require_list(raw.get("finding_ids"), f"{prefix}.finding_ids", failures)
        if not refs:
            failures.append(f"{prefix}.finding_ids must not be empty")
        for finding_id in refs:
            if finding_id not in finding_ids:
                failures.append(f"{prefix} references unknown finding id: {finding_id}")
        require_enum(raw.get("impact"), IMPACTS, f"{prefix}.impact", failures)
        require_enum(raw.get("effort"), EFFORT, f"{prefix}.effort", failures)

    require_list(payload.get("missing_evidence"), "missing_evidence", failures)
    mutable_findings = [raw for raw in findings if isinstance(raw, dict) and raw.get("category") in MUTABLE_CATEGORIES]
    source_review = payload.get("source_review")
    if mutable_findings and not isinstance(source_review, dict):
        warnings.append("mutable platform findings should include source_review")
    elif isinstance(source_review, dict):
        for field in ("reviewed_at", "source_ids", "overdue_sources"):
            if field not in source_review:
                failures.append(f"source_review missing field: {field}")
        require_list(source_review.get("source_ids"), "source_review.source_ids", failures)
        require_list(source_review.get("overdue_sources"), "source_review.overdue_sources", failures)
    return {"ok": not failures, "failures": failures, "warnings": warnings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Qiaomu SEO audit JSON report.")
    parser.add_argument("audit_file", help="Path to the audit JSON file.")
    args = parser.parse_args()
    path = Path(args.audit_file)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "failures": [str(exc)], "warnings": []}, ensure_ascii=False, indent=2))
        raise SystemExit(2) from exc
    if not isinstance(payload, dict):
        result = {"ok": False, "failures": ["audit root must be an object"], "warnings": []}
    else:
        result = validate(payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
