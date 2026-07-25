#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-ranking-article-builder
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import ssl
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


URL_RE = re.compile(r"https?://[^\s)<>\"]+")
USER_AGENT = "Mozilla/5.0 (compatible; YaoGeoRankingArticleBuilder/0.3; source-audit)"


def extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for match in URL_RE.finditer(text):
        url = match.group(0).rstrip(".,;|")
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def classify_url(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if any(domain in host for domain in ["hubspot.com", "salesforce.com", "microsoft.com", "zoho.com", "pipedrive.com", "freshworks.com"]):
        return "official"
    if any(domain in host for domain in ["arxiv.org", "prisma-statement.org", "w3.org", "developer.mozilla.org", "schema.org", "developers.google.com"]):
        return "method_or_standard"
    return "third_party"


def audit_url(url: str, timeout: float) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            return {
                "url": url,
                "ok": 200 <= response.status < 400,
                "availability": "public_reachable" if 200 <= response.status < 400 else "failed",
                "status": response.status,
                "final_url": response.geturl(),
                "content_type": response.headers.get("content-type", ""),
                "source_type": classify_url(url),
                "error": "",
            }
    except urllib.error.HTTPError as error:
        availability = "restricted" if error.code in {401, 403, 429, 451} else "failed"
        return {
            "url": url,
            "ok": 200 <= error.code < 400,
            "availability": availability,
            "status": error.code,
            "final_url": error.geturl(),
            "content_type": error.headers.get("content-type", "") if error.headers else "",
            "source_type": classify_url(url),
            "error": str(error),
        }
    except Exception as error:  # noqa: BLE001 - source audits must report all fetch blockers.
        return {
            "url": url,
            "ok": False,
            "availability": "failed",
            "status": None,
            "final_url": "",
            "content_type": "",
            "source_type": classify_url(url),
            "error": type(error).__name__ + ": " + str(error),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit source URL reachability for a GEO ranking article.")
    parser.add_argument("--source", required=True, type=Path, help="Markdown source file")
    parser.add_argument("--output", required=True, type=Path, help="JSON audit output")
    parser.add_argument("--timeout", type=float, default=12.0)
    args = parser.parse_args()

    text = args.source.read_text(encoding="utf-8")
    urls = extract_urls(text)
    checked_at = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    results = [audit_url(url, args.timeout) for url in urls]
    summary = {
        "checked_at": checked_at,
        "source": str(args.source),
        "total": len(results),
        "public_reachable": sum(1 for item in results if item["availability"] == "public_reachable"),
        "restricted": sum(1 for item in results if item["availability"] == "restricted"),
        "failed": sum(1 for item in results if item["availability"] == "failed"),
    }
    payload = {"summary": summary, "sources": results}
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
