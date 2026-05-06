#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
SKIP = {"index.md", "log.md"}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")


def wiki_pages() -> list[Path]:
    pages: list[Path] = []
    for path in sorted(WIKI.rglob("*.md")):
        if path.name in SKIP:
            continue
        if not path.read_text(encoding="utf-8").startswith("---\n"):
            continue
        pages.append(path)
    return pages


def resolve_link(source: Path, target: str) -> Path | None:
    candidate = (source.parent / target).resolve()
    try:
        return candidate.relative_to(ROOT)
    except ValueError:
        return None


def main() -> None:
    pages = wiki_pages()
    inbound = {path.relative_to(ROOT): 0 for path in pages}

    for page in pages:
        text = page.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            rel = resolve_link(page, target)
            if rel in inbound:
                inbound[rel] += 1

    for path, count in sorted(inbound.items()):
        if count == 0:
            print(path.as_posix())


if __name__ == "__main__":
    main()
