#!/usr/bin/env python3

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
INDEX = WIKI / "index.md"
SKIP = {"index.md", "log.md"}
TYPE_ORDER = ["idea", "query", "lint"]
TYPE_LABELS = {
    "idea": "Ideas",
    "query": "Queries",
    "lint": "Lint",
}


def parse_value(raw: str):
    raw = raw.strip()
    if not raw:
        return ""
    try:
        return ast.literal_eval(raw)
    except Exception:
        return raw.strip('"').strip("'")


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    lines = text.splitlines()
    data: dict[str, object] = {}
    for line in lines[1:]:
        if line == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = parse_value(value)
    return data


def collect_pages() -> dict[str, list[dict[str, object]]]:
    grouped = {key: [] for key in TYPE_ORDER}
    for path in sorted(WIKI.rglob("*.md")):
        if path.name in SKIP:
            continue
        meta = parse_frontmatter(path)
        page_type = str(meta.get("type", "")).strip()
        if page_type not in grouped:
            continue
        rel = path.relative_to(WIKI).as_posix()
        grouped[page_type].append(
            {
                "title": meta.get("title", path.stem),
                "summary": meta.get("summary", ""),
                "status": meta.get("status", ""),
                "verdict": meta.get("verdict", ""),
                "tags": meta.get("tags", []),
                "updated": meta.get("updated", ""),
                "path": rel,
            }
        )
    return grouped


def render_index(groups: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# Index",
        "",
        "Auto-generated from wiki page frontmatter by `scripts/rebuild_index.py`.",
        "",
    ]

    for page_type in TYPE_ORDER:
        pages = sorted(groups[page_type], key=lambda item: str(item["title"]).lower())
        if not pages:
            continue
        lines.append(f"## {TYPE_LABELS[page_type]}")
        lines.append("")
        for page in pages:
            tags = page["tags"] if isinstance(page["tags"], list) else []
            tag_text = f" | tags: {', '.join(tags)}" if tags else ""
            status_text = f" | status: {page['status']}" if page["status"] else ""
            verdict_text = f" | verdict: {page['verdict']}" if page["verdict"] else ""
            updated_text = f" | updated: {page['updated']}" if page["updated"] else ""
            lines.append(
                f"- [{page['title']}](./{page['path']}) - {page['summary']}{status_text}{verdict_text}{updated_text}{tag_text}"
            )
        lines.append("")

    lines.extend(
        [
            "## Workflow",
            "",
            "- Read this file first when answering a question against the wiki.",
            "- Prefer updating an existing idea page over creating a new page.",
            "- Regenerate this file after adding or editing durable wiki pages.",
            "",
            "## Special Files",
            "",
            "- [Log](./log.md) - chronological record of ingests, durable queries, and lint passes.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    groups = collect_pages()
    INDEX.write_text(render_index(groups), encoding="utf-8")


if __name__ == "__main__":
    main()
