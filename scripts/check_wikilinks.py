#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
SKIP = {"index.md", "log.md"}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+?\.md(?:#[^)]+)?)\)")


def wiki_pages() -> list[Path]:
    return sorted(path for path in WIKI.rglob("*.md") if path.name not in SKIP)


def split_anchor(target: str) -> tuple[str, str | None]:
    path, marker, anchor = target.partition("#")
    return path, anchor if marker else None


def resolve_link(source: Path, target: str) -> Path | None:
    path, _anchor = split_anchor(target)
    candidate = (source.parent / path).resolve()
    try:
        return candidate.relative_to(ROOT)
    except ValueError:
        return None


def line_anchor_is_valid(path: Path, anchor: str | None) -> bool:
    if not anchor:
        return True

    match = re.fullmatch(r"L(\d+)(?:-L?(\d+))?", anchor)
    if not match:
        return True

    start = int(match.group(1))
    end = int(match.group(2) or start)
    if start < 1 or end < start:
        return False

    line_count = len(path.read_text(encoding="utf-8").splitlines())
    return end <= line_count


def main() -> None:
    pages = wiki_pages()
    existing = {path.relative_to(ROOT) for path in pages}
    existing.add(Path("wiki/index.md"))
    existing.add(Path("wiki/log.md"))

    for page in pages:
        text = page.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for target in LINK_RE.findall(line):
                _path, anchor = split_anchor(target)
                rel = resolve_link(page, target)
                raw_source = (
                    rel is not None
                    and rel.parts
                    and rel.parts[0] == "raw"
                    and (ROOT / rel).is_file()
                )
                if rel is None or (rel not in existing and not raw_source):
                    print(f"{page.relative_to(ROOT)}:{line_no}: {target}")
                elif raw_source and not line_anchor_is_valid(ROOT / rel, anchor):
                    print(f"{page.relative_to(ROOT)}:{line_no}: {target}")


if __name__ == "__main__":
    main()
