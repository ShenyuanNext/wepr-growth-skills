#!/usr/bin/env python3
"""Read and validate bundled numbered tasks without external network access."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "numbered-prompts"
CODE = re.compile(r"[0-9]{3}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
TITLE = re.compile(r"^# ([0-9]{3})｜(.+)$", re.MULTILINE)
SECTIONS = (
    "## 用户要完成的事", "## 需要的输入", "## 执行步骤",
    "## 交付结果", "## 验收标准", "## 适用边界",
)


class CatalogError(Exception):
    pass


def validate_catalog(raw: bytes) -> list[dict[str, str]]:
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CatalogError("编号目录不是有效的 UTF-8 JSON") from error
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise CatalogError("编号目录格式版本不正确")
    items = document.get("items")
    if not isinstance(items, list) or len(items) > 1000:
        raise CatalogError("编号目录条目数量无效")
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            raise CatalogError("编号目录条目格式错误")
        code = item.get("id")
        if not isinstance(code, str) or CODE.fullmatch(code) is None or code in seen:
            raise CatalogError("编号目录包含无效或重复编号")
        seen.add(code)
        for key in ("title", "purpose"):
            value = item.get(key)
            if not isinstance(value, str) or not value.strip() or len(value) > 500:
                raise CatalogError(f"编号 {code} 缺少有效的{key}")
            if "\n" in value or "\r" in value:
                raise CatalogError(f"编号 {code} 的{key}格式错误")
        digest = item.get("sha256")
        if not isinstance(digest, str) or DIGEST.fullmatch(digest) is None:
            raise CatalogError(f"编号 {code} 缺少有效的内容校验值")
    if [item["id"] for item in items] != sorted(seen):
        raise CatalogError("编号目录没有按编号排序")
    return items


def catalog() -> list[dict[str, str]]:
    path = ROOT / "catalog.json"
    if not path.is_file():
        raise CatalogError("安装包中缺少编号目录")
    try:
        return validate_catalog(path.read_bytes())
    except OSError as error:
        raise CatalogError(f"无法读取本地编号目录：{error}") from error


def get_prompt(code: str) -> str:
    items = catalog()
    entry = next((item for item in items if item["id"] == code), None)
    if entry is None:
        raise CatalogError(f"安装包中没有编号 {code}")
    path = ROOT / code / "PROMPT.md"
    if not path.is_file():
        raise CatalogError(f"安装包中没有编号 {code} 的内容")
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise CatalogError(f"无法读取编号 {code}：{error}") from error
    if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
        raise CatalogError(f"编号 {code} 的目录与正文校验值不一致")
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CatalogError(f"编号 {code} 的正文不是 UTF-8") from error
    title = TITLE.search(content)
    if title is None or title.group(1) != code or any(section not in content for section in SECTIONS):
        raise CatalogError(f"编号 {code} 的正文结构不完整")
    return content


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    get = sub.add_parser("get")
    get.add_argument("code")
    args = parser.parse_args()
    try:
        if args.command == "list":
            items = catalog()
            if not items:
                print("本地安装包当前没有可用的编号任务。")
            for item in items:
                print(f"{item['id']}\t{item['title']}\t{item['purpose']}")
        else:
            if CODE.fullmatch(args.code) is None:
                raise CatalogError("编号必须是三位数字")
            print(get_prompt(args.code), end="")
    except CatalogError as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
