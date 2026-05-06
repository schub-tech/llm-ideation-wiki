#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
MANIFEST = ROOT / ".manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def raw_files() -> set[str]:
    return {
        path.relative_to(ROOT).as_posix()
        for path in RAW.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    }


def main() -> None:
    if not MANIFEST.exists():
        print("No .manifest.json found. All raw sources are untracked.")
        for rel in sorted(raw_files()):
            print(f"new: {rel}")
        return

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sources = manifest.get("sources", {})
    if not isinstance(sources, dict):
        raise SystemExit(".manifest.json has no object-valued sources field")

    current = raw_files()
    tracked = set(sources)

    groups = {
        "new": [],
        "modified": [],
        "unchanged": [],
        "deleted": [],
        "unlinked": [],
    }

    for rel in sorted(current - tracked):
        groups["new"].append(rel)

    for rel in sorted(tracked - current):
        groups["deleted"].append(rel)

    for rel in sorted(current & tracked):
        entry = sources.get(rel, {})
        if not isinstance(entry, dict):
            groups["modified"].append(rel)
            continue
        actual_hash = sha256(ROOT / rel)
        if actual_hash != entry.get("content_hash"):
            groups["modified"].append(rel)
        else:
            groups["unchanged"].append(rel)
        if not entry.get("pages"):
            groups["unlinked"].append(rel)

    print("# Wiki Status")
    print("")
    print(f"- Raw sources: {len(current)}")
    print(f"- Tracked sources: {len(tracked)}")
    print(f"- New: {len(groups['new'])}")
    print(f"- Modified: {len(groups['modified'])}")
    print(f"- Deleted: {len(groups['deleted'])}")
    print(f"- Unlinked: {len(groups['unlinked'])}")
    print("")

    for name in ["new", "modified", "deleted", "unlinked"]:
        if not groups[name]:
            continue
        print(f"## {name.title()}")
        print("")
        for rel in groups[name]:
            print(f"- {rel}")
        print("")


if __name__ == "__main__":
    main()
