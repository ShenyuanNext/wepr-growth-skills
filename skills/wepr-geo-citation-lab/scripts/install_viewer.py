#!/usr/bin/env python3
"""Verify the pinned research viewer and add a WEPR navigation page."""
import argparse
import hashlib
import html
import json
import shutil
import stat
import tempfile
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

VERSION = "0.1.0"
BASE = "https://github.com/yaojingang/geo-citation-lab/releases/download/v" + VERSION
ARCHIVE = "geo-citation-lab-viewer.zip"
MARKER = ".wepr-geo-citation-viewer.json"
MAX_BYTES = 15 * 1024 * 1024


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(url, destination):
    request = urllib.request.Request(url, headers={"User-Agent": "WEPR-Research-Viewer/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Download exceeds 15 MiB")
    destination.write_bytes(data)


def extract_verified(archive, checksum, target):
    tokens = checksum.read_text(encoding="utf-8").split()
    expected = tokens[0].lower() if tokens else ""
    if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
        raise ValueError("Malformed SHA-256 sidecar")
    if digest(archive) != expected:
        raise ValueError("Archive SHA-256 mismatch")
    with zipfile.ZipFile(archive) as package:
        entries = package.infolist()
        if sum(item.file_size for item in entries) > MAX_BYTES:
            raise ValueError("Expanded viewer exceeds 15 MiB")
        names = set()
        for item in entries:
            path = PurePosixPath(item.filename)
            if path.is_absolute() or ".." in path.parts or "\\" in item.filename:
                raise ValueError("Unsafe ZIP path")
            if stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError("ZIP symlinks are unsupported")
            if item.filename in names:
                raise ValueError("Duplicate ZIP path")
            names.add(item.filename)
        package.extractall(target)
    required = ["index.html", "LICENSE", "LICENSE-CODE", "LICENSE-CONTENT",
                "THIRD_PARTY_NOTICES.md", "geo-citation-lab-manifest.json",
                "geo-citation-lab-files.sha256"]
    if any(not (target / name).is_file() for name in required):
        raise ValueError("Viewer is missing entrypoint or required notices")
    manifest = json.loads((target / "geo-citation-lab-manifest.json").read_text())
    if manifest.get("distribution_version") != VERSION:
        raise ValueError("Unexpected viewer version")
    rows = (target / "geo-citation-lab-files.sha256").read_text().splitlines()
    if not rows:
        raise ValueError("Empty file checksum manifest")
    for row in rows:
        sha, name = row.split("  ", 1)
        candidate = target / name
        if not candidate.resolve().is_relative_to(target.resolve()):
            raise ValueError("Unsafe checksum path")
        if not candidate.is_file() or digest(candidate) != sha:
            raise ValueError("Viewer file checksum mismatch: " + name)
    return expected


def add_wepr_navigation(target):
    (target / "index.html").rename(target / "research-index.html")
    report_links = []
    for file in sorted(target.rglob("*.html")):
        relative = file.relative_to(target).as_posix()
        if relative.startswith("01-"):
            title = "跨平台引用选择与内容吸收报告"
        elif relative.startswith("02-"):
            title = "GEO 论文目录"
        elif relative.startswith("03-"):
            title = "中文 AI 信源与 Web/App 差异报告"
        else:
            continue
        report_links.append('<li><a href="' + urllib.parse.quote(relative)
                            + '">' + html.escape(title) + '</a></li>')
    page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WEPR GEO 引用研究工作台</title>
<style>body{max-width:960px;margin:64px auto;padding:0 24px;background:#f7f8fa;
color:#162033;font:18px/1.8 system-ui,sans-serif}h1{font-size:36px}a{color:#1658a3}
li{margin:16px 0}footer{margin-top:48px;font-size:14px;color:#536174}</style>
<main><p>WEPR · GEO RESEARCH</p><h1>GEO 引用研究工作台</h1>
<p>研究 AI 如何选择信源、使用页面证据，并将观察结果转为内容优化与采样实验。</p>
<ul>''' + "".join(report_links) + '''</ul>
<p><a href="https://www.scwepr.com/">WEPR 官网与服务</a></p>
<footer>WEPR 增加本导航页；研究报告保留原始内容、署名和许可，研究成果归原作者。
<a href="research-index.html">原始研究导航与来源</a> ·
<a href="LICENSE">许可范围</a> · <a href="THIRD_PARTY_NOTICES.md">第三方材料说明</a>
<p>历史研究样本不等于客户当前表现；引用、推荐和转化分别测量。</p></footer></main></html>'''
    (target / "index.html").write_text(page, encoding="utf-8")


def install(args):
    raw = args.dir.expanduser()
    if raw.is_symlink():
        raise ValueError("Installation target must not be a symlink")
    destination = raw.resolve()
    if destination in (Path("/"), Path.home(), Path.home() / ".codex", Path.home() / ".agents"):
        raise ValueError("Choose a dedicated installation directory")
    if destination.exists() and not (destination / MARKER).is_file():
        raise ValueError("Existing destination is not managed by this installer")
    if bool(args.archive) != bool(args.checksum):
        raise ValueError("Pass both --archive and --checksum")
    destination.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    with tempfile.TemporaryDirectory(prefix="wepr-citation-", dir=destination.parent) as work:
        work = Path(work)
        archive = args.archive or work / ARCHIVE
        checksum = args.checksum or work / (ARCHIVE + ".sha256")
        if not args.archive:
            fetch(BASE + "/" + ARCHIVE, archive)
            fetch(BASE + "/" + ARCHIVE + ".sha256", checksum)
        stage = work / "viewer"
        stage.mkdir()
        sha = extract_verified(archive, checksum, stage)
        add_wepr_navigation(stage)
        record = {"version": VERSION, "archive_sha256": sha,
                  "source": BASE, "changes": "WEPR navigation added; original index renamed",
                  "installed_at": datetime.now(timezone.utc).isoformat()}
        (stage / MARKER).write_text(json.dumps(record, ensure_ascii=False, indent=2))
        if destination.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup = destination.with_name(destination.name + ".backup-" + stamp)
            destination.rename(backup)
        try:
            shutil.move(str(stage), str(destination))
        except Exception:
            if backup is not None and not destination.exists():
                backup.rename(destination)
            raise
    return {"status": "installed", "version": VERSION, "archive_sha256": sha,
            "install_path": str(destination), "entrypoint": str(destination / "index.html"),
            "backup_path": str(backup) if backup else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--checksum", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(install(args), ensure_ascii=False, indent=2))
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, "Install failed: " + str(error) + "\n")


if __name__ == "__main__":
    main()
