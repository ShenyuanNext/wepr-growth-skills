#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-brand-graph
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import socket
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


USER_AGENT = "Mozilla/5.0 (compatible; YaoGeoBrandGraph/0.1; +https://x.com/yaojingang)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="report_input.json with evidence entries")
    parser.add_argument("--output", help="Optional source validation JSON output path")
    parser.add_argument("--update-input", action="store_true", help="Write source_validation back into report_input.json")
    parser.add_argument("--timeout", type=int, default=12, help="HTTP timeout seconds")
    parser.add_argument("--max-bytes", type=int, default=240_000, help="Maximum response bytes used for title extraction")
    return parser.parse_args()


def page_title(payload: bytes, content_type: str) -> str:
    if "html" not in content_type.lower():
        return ""
    head = payload.decode("utf-8", errors="ignore")
    match = re.search(r"<title[^>]*>(.*?)</title>", head, flags=re.I | re.S)
    if not match:
        return ""
    title = re.sub(r"\s+", " ", match.group(1)).strip()
    return html.unescape(title)[:180]


def fetch_evidence(item: dict[str, Any], timeout: int, max_bytes: int) -> dict[str, Any]:
    locator = str(item.get("locator", "")).strip()
    checked_at = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    base = {
        "source_id": item.get("id", ""),
        "evidence_title": item.get("title", ""),
        "url": locator,
        "checked_at": checked_at,
        "http_status": "",
        "reachable": False,
        "page_title": "",
        "content_type": "",
        "last_modified": "",
        "validation_status": "未核验",
        "real_data_judgement": "未采样",
        "action": "人工复核来源。",
    }
    if not locator.startswith(("http://", "https://")):
        base.update({
            "validation_status": "跳过",
            "real_data_judgement": "非 URL 来源，需人工或内部系统核验。",
            "action": "保留来源说明，补充可访问 URL 或内部文档定位符。",
        })
        return base
    request = urllib.request.Request(locator, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read(max_bytes)
            status = getattr(response, "status", 200)
            content_type = response.headers.get("content-type", "")
            base.update({
                "http_status": str(status),
                "reachable": 200 <= status < 400,
                "page_title": page_title(payload, content_type),
                "content_type": content_type.split(";")[0],
                "last_modified": response.headers.get("last-modified", ""),
            })
    except urllib.error.HTTPError as exc:
        base.update({
            "http_status": str(exc.code),
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "validation_status": "受限",
            "real_data_judgement": "URL 返回 HTTP 错误，不能仅凭自动采样确认页面内容。",
            "action": "改用浏览器人工访问、官方镜像、SEC 文件或已授权资料补证。",
        })
        return base
    except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
        base.update({
            "validation_status": "失败",
            "real_data_judgement": f"自动采样失败：{type(exc).__name__}",
            "action": "人工复核 URL，必要时替换为更稳定的官方来源。",
        })
        return base
    base.update({
        "validation_status": "已连通" if base["reachable"] else "受限",
        "real_data_judgement": "可作为真实来源核验样本；仍需用来源账本中的事实主张做人工语义核对。" if base["reachable"] else "URL 可响应但状态异常，需人工复核。",
        "action": "保留来源 ID，并在正式交付前核对页面正文与事实主张。" if base["reachable"] else "人工复核页面状态。",
    })
    return base


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    data = json.loads(input_path.read_text(encoding="utf-8"))
    results = [fetch_evidence(item, args.timeout, args.max_bytes) for item in data.get("evidence", [])]
    payload = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "source_count": len(results),
        "reachable_count": sum(1 for item in results if item.get("reachable")),
        "results": results,
    }
    if args.output:
        Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.update_input:
        data["source_validation"] = results
        input_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
