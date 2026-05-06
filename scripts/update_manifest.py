#!/usr/bin/env python3

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
WIKI = ROOT / "wiki"
MANIFEST = ROOT / ".manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_scalar(raw: str):
    raw = raw.strip()
    if not raw:
        return ""
    try:
        return ast.literal_eval(raw)
    except Exception:
        return raw.strip('"').strip("'")


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}

    lines = text.splitlines()
    data: dict[str, object] = {}
    i = 1
    while i < len(lines):
        line = lines[i]
        if line == "---":
            break
        if ":" not in line:
            i += 1
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value:
            data[key] = parse_scalar(value)
            i += 1
            continue

        items: list[str] = []
        j = i + 1
        while j < len(lines):
            candidate = lines[j]
            if candidate == "---":
                break
            stripped = candidate.strip()
            if stripped.startswith("- "):
                items.append(str(parse_scalar(stripped[2:])))
                j += 1
                continue
            if candidate and not candidate.startswith(" "):
                break
            j += 1
        data[key] = items
        i = j

    return data


def raw_files() -> list[Path]:
    return sorted(
        path for path in RAW.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    )


def wiki_pages() -> list[Path]:
    return sorted(path for path in WIKI.rglob("*.md") if path.name not in {"index.md", "log.md"})


def load_manifest() -> dict[str, object]:
    if not MANIFEST.exists():
        return {"version": 1, "sources": {}}
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def collect_page_refs() -> tuple[dict[str, list[str]], dict[str, str]]:
    refs: dict[str, list[str]] = {}
    source_dates: dict[str, str] = {}

    for page in wiki_pages():
        meta = frontmatter(page)
        rel_page = page.relative_to(ROOT).as_posix()
        updated = str(meta.get("updated", ""))
        sources = meta.get("source_files", [])
        if isinstance(sources, str):
            sources = [sources]
        if not isinstance(sources, list):
            continue

        for source in sources:
            source_path = str(source)
            refs.setdefault(source_path, []).append(rel_page)
            if updated:
                source_dates[source_path] = max(source_dates.get(source_path, ""), updated)

    for source_path in refs:
        refs[source_path] = sorted(set(refs[source_path]))

    return refs, source_dates


def build_manifest() -> dict[str, object]:
    old = load_manifest()
    old_sources = old.get("sources", {})
    if not isinstance(old_sources, dict):
        old_sources = {}

    page_refs, source_dates = collect_page_refs()
    today = date.today().isoformat()
    sources: dict[str, object] = {}

    for path in raw_files():
        rel = path.relative_to(ROOT).as_posix()
        old_entry = old_sources.get(rel, {})
        if not isinstance(old_entry, dict):
            old_entry = {}

        current_hash = sha256(path)
        old_hash = old_entry.get("content_hash")
        pages = page_refs.get(rel, old_entry.get("pages", []))
        if not isinstance(pages, list):
            pages = []

        if current_hash == old_hash:
            last_ingested = old_entry.get("last_ingested", "")
        else:
            last_ingested = source_dates.get(rel) or old_entry.get("last_ingested", "")

        sources[rel] = {
            "content_hash": current_hash,
            "last_ingested": last_ingested,
            "pages": sorted(str(page) for page in pages),
            "status": "ingested" if pages else "unlinked",
        }

    for rel, old_entry in sorted(old_sources.items()):
        if rel in sources:
            continue
        if isinstance(old_entry, dict):
            old_copy = dict(old_entry)
            old_copy["status"] = "missing"
            sources[rel] = old_copy

    return {
        "version": 1,
        "last_updated": today,
        "sources": sources,
    }


def print_delta(new_manifest: dict[str, object]) -> None:
    old = load_manifest().get("sources", {})
    if not isinstance(old, dict):
        old = {}
    new = new_manifest.get("sources", {})
    if not isinstance(new, dict):
        new = {}

    for rel, entry in sorted(new.items()):
        old_entry = old.get(rel, {})
        if not isinstance(entry, dict):
            continue
        if not isinstance(old_entry, dict):
            print(f"new: {rel}")
        elif entry.get("status") == "missing":
            print(f"missing: {rel}")
        elif entry.get("content_hash") != old_entry.get("content_hash"):
            print(f"modified: {rel}")
        elif entry.get("pages") != old_entry.get("pages"):
            print(f"pages-changed: {rel}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh .manifest.json from raw files and wiki source_files frontmatter.")
    parser.add_argument("--check", action="store_true", help="Print changes without writing .manifest.json.")
    args = parser.parse_args()

    manifest = build_manifest()
    if args.check:
        print_delta(manifest)
        return

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"updated {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
