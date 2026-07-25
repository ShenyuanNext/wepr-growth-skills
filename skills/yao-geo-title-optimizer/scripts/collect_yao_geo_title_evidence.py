#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-title-optimizer
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Collect lightweight public URL evidence snapshots for GEO Title Lab reports."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import ssl
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


USER_AGENT = "yao-geo-title-optimizer/0.1 (+https://x.com/yaojingang)"
MAX_BYTES = 600_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="report_input.json with evidence_sources")
    parser.add_argument("--output", required=True, help="snapshot JSON output path")
    parser.add_argument("--timeout", type=int, default=15)
    return parser.parse_args()


def load_urls(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    sources = data.get("evidence_sources", [])
    return [item for item in sources if item.get("url")]


def text_between(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.I | re.S)
    if not match:
        return ""
    value = re.sub(r"<[^>]+>", " ", match.group(1))
    value = re.sub(r"\s+", " ", value).strip()
    return html.unescape(value)


def extract_html_fields(raw: bytes, content_type: str) -> dict[str, str]:
    charset = "utf-8"
    match = re.search(r"charset=([\w.-]+)", content_type or "", flags=re.I)
    if match:
        charset = match.group(1)
    text = raw.decode(charset, errors="replace")
    title = text_between(r"<title[^>]*>(.*?)</title>", text)
    description = text_between(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', text)
    if not description:
        description = text_between(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', text)
    h1 = text_between(r"<h1[^>]*>(.*?)</h1>", text)
    canonical = text_between(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', text)
    return {
        "title": title,
        "meta_description": description,
        "h1": h1,
        "canonical": canonical,
    }


def fetch_url(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    context = ssl.create_default_context()
    fetched_at = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            raw = response.read(MAX_BYTES)
            content_type = response.headers.get("content-type", "")
            result: dict[str, Any] = {
                "url": url,
                "final_url": response.geturl(),
                "status": response.status,
                "ok": 200 <= response.status < 400,
                "content_type": content_type,
                "bytes_sampled": len(raw),
                "sha256_sample": hashlib.sha256(raw).hexdigest(),
                "fetched_at": fetched_at,
                "error": "",
            }
            if "html" in content_type:
                result.update(extract_html_fields(raw, content_type))
            return result
    except urllib.error.HTTPError as exc:
        return {"url": url, "status": exc.code, "ok": False, "fetched_at": fetched_at, "error": str(exc)}
    except Exception as exc:
        return {"url": url, "status": None, "ok": False, "fetched_at": fetched_at, "error": str(exc)}


def main() -> None:
    args = parse_args()
    sources = load_urls(Path(args.input))
    snapshots = []
    for item in sources:
        snapshot = fetch_url(item["url"], args.timeout)
        snapshot["source"] = item.get("source", "")
        snapshot["fact_claim"] = item.get("fact", "")
        snapshots.append(snapshot)
    output = {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "input": str(Path(args.input)),
        "source_count": len(sources),
        "ok_count": sum(1 for item in snapshots if item.get("ok")),
        "snapshots": snapshots,
    }
    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote evidence snapshot: {args.output}")
    print(f"OK sources: {output['ok_count']}/{output['source_count']}")


if __name__ == "__main__":
    main()
