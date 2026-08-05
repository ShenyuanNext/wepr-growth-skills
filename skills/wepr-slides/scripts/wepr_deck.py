#!/usr/bin/env python3
"""Safely inject or validate the JSON document block in a Bento deck."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


BLOCK = re.compile(
    r'(<script\b[^>]*\bid=["\']bento-doc["\'][^>]*>)(.*?)(</script>)',
    re.IGNORECASE | re.DOTALL,
)


def load_block(path: Path) -> tuple[str, re.Match[str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(BLOCK.finditer(text))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one #bento-doc block, found {len(matches)}")
    return text, matches[0]


def validate_doc(doc: object) -> dict:
    if not isinstance(doc, dict):
        raise ValueError("document root must be an object")
    if doc.get("format") != "bento/slides":
        raise ValueError('document format must be "bento/slides"')
    size = doc.get("size")
    theme = doc.get("theme")
    slides = doc.get("slides")
    if not isinstance(size, dict) or not size.get("width") or not size.get("height"):
        raise ValueError("size.width and size.height are required")
    if not isinstance(theme, dict) or not theme.get("fontFamily"):
        raise ValueError("theme.fontFamily is required")
    if not isinstance(slides, list) or not slides:
        raise ValueError("slides must be a non-empty array")
    ids = [slide.get("id") for slide in slides if isinstance(slide, dict)]
    if len(ids) != len(slides) or any(not value for value in ids):
        raise ValueError("every slide requires an id")
    if len(ids) != len(set(ids)):
        raise ValueError("slide ids must be unique")
    return doc


def parse_embedded(path: Path) -> dict:
    _, match = load_block(path)
    payload = match.group(2).strip()
    if not payload:
        raise ValueError("#bento-doc block is empty")
    return validate_doc(json.loads(payload))


def inject(deck_path: Path, json_path: Path) -> None:
    text, match = load_block(deck_path)
    doc = validate_doc(json.loads(json_path.read_text(encoding="utf-8")))
    payload = json.dumps(doc, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("<", "\\u003c")
    replacement = f"{match.group(1)}\n{payload}\n{match.group(3)}"
    deck_path.write_text(text[: match.start()] + replacement + text[match.end() :], encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    inject_parser = subparsers.add_parser("inject")
    inject_parser.add_argument("deck", type=Path)
    inject_parser.add_argument("document", type=Path)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("deck", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "inject":
            inject(args.deck, args.document)
            parse_embedded(args.deck)
            print(f"valid Bento deck: {args.deck}")
        else:
            doc = parse_embedded(args.deck)
            print(f"valid Bento deck: {args.deck} ({len(doc['slides'])} slides)")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
