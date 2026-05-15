#!/usr/bin/env python3

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "notion.config.json"
CACHE = ROOT / ".cache" / "notion"

LOCAL_CONTENT = {
    "templates/idea-page": ROOT / "templates" / "idea-page.md",
    "templates/buyer-interview-protocol": ROOT / "templates" / "buyer-interview-protocol.md",
}

SEED_TREE = [
    ("raw/", ""),
    ("raw/shared/", "raw/"),
    ("wiki/", ""),
    ("templates/", ""),
    ("templates/idea-page", "templates/"),
    ("templates/buyer-interview-protocol", "templates/"),
]

PAGE_ICONS = {
    "raw/": "🧾",
    "raw/shared/": "🔗",
    "wiki/": "📚",
    "templates/": "🧰",
    "templates/idea-page": "🧩",
    "templates/buyer-interview-protocol": "🎙️",
}

PAGE_TITLES = {
    "raw/": "Raw",
    "raw/shared/": "Shared",
    "wiki/": "Wiki",
    "templates/": "Templates",
    "templates/idea-page": "Idea Page",
    "templates/buyer-interview-protocol": "Buyer Interview Protocol",
}

ROOT_DESCRIPTION = "Start here: Raw holds source inputs, Wiki holds current syntheses, and Templates holds reusable scaffolds."

DEFAULT_DESCRIPTIONS = {
    "raw/": "Source material starts here. Use Shared for reusable inputs and idea pages for idea-specific notes.",
    "raw/shared/": "Reusable source notes live here: market facts, methods, vocabulary, and references that support multiple ideas.",
    "wiki/": "Current idea syntheses live here. Create one page per idea slug and keep claims tied back to raw evidence.",
    "templates/": "Copy these scaffolds when starting an idea page or interview workflow.",
    "templates/idea-page": "Copy this scaffold into an idea Overview page, replace placeholders with evidence-backed bullets, and leave gaps explicit.",
    "templates/buyer-interview-protocol": "Copy this as a wiki child page when buyer interviews are the next validation step.",
}


def run_ntn(args: list[str], *, input_text: str | None = None) -> str:
    result = subprocess.run(
        ["ntn", *args],
        cwd=ROOT,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise SystemExit(f"ntn {' '.join(args)} failed: {detail}")
    return result.stdout


def load_config() -> dict[str, Any]:
    if not CONFIG.exists():
        raise SystemExit(f"missing {CONFIG.relative_to(ROOT)}")
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    data.setdefault("pages", {})
    return data


def save_config(config: dict[str, Any]) -> None:
    CONFIG.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def compact_id(page_id: str) -> str:
    return page_id.replace("-", "")


def page_id(config: dict[str, Any], path: str) -> str:
    pages = config.get("pages", {})
    entry = pages.get(path)
    if not isinstance(entry, dict) or not entry.get("id"):
        raise SystemExit(f"unknown Notion page path: {path}")
    return str(entry["id"])


def page_icon(path: str) -> str:
    return PAGE_ICONS.get(path, "📄")


def page_title(path: str) -> str:
    if path in PAGE_TITLES:
        return PAGE_TITLES[path]
    name = path.rstrip("/").split("/")[-1] or path
    return " ".join(part.capitalize() for part in re.split(r"[-_]+", name) if part)


def cache_path(path: str) -> Path:
    if path.endswith("/"):
        return CACHE / path / "_page.md"
    return CACHE / path


def default_content(path: str) -> str:
    local = LOCAL_CONTENT.get(path)
    if local and local.exists():
        return template_content(path, local)
    return DEFAULT_DESCRIPTIONS.get(path, "Use this page for its mapped wiki content.") + "\n"


def template_content(path: str, source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    match = re.search(r"````markdown\n(.*?)\n````", text, flags=re.DOTALL)
    body = match.group(1).strip() if match else text.strip()

    if body.startswith("---\n"):
        _, _, remainder = body.partition("\n---\n")
        body = remainder.strip()

    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    body = "\n".join(lines).strip()

    if path == "templates/idea-page":
        return (
            f"{DEFAULT_DESCRIPTIONS[path]}\n\n"
            f"{body}\n"
        )

    if path == "templates/buyer-interview-protocol":
        return (
            f"{DEFAULT_DESCRIPTIONS[path]}\n\n"
            f"{body}\n"
        )

    return body + "\n"


def create_empty_page(parent_id: str, title: str) -> dict[str, Any]:
    output = run_ntn(
        [
            "api",
            "/v1/pages",
            f"parent[page_id]={compact_id(parent_id)}",
            f"properties[title][title][0][text][content]={title}",
        ]
    )
    return json.loads(output)


def set_page_icon(page_id_value: str, emoji: str) -> None:
    run_ntn(
        [
            "api",
            f"/v1/pages/{compact_id(page_id_value)}",
            "-X",
            "PATCH",
            f"icon[emoji]={emoji}",
        ]
    )


def set_page_title(page_id_value: str, title: str) -> None:
    run_ntn(
        [
            "api",
            f"/v1/pages/{compact_id(page_id_value)}",
            "-X",
            "PATCH",
            f"properties[title][title][0][text][content]={title}",
        ]
    )


def strip_yaml_frontmatter(markdown: str) -> str:
    lines = markdown.split("\n")
    if not lines or lines[0].strip() != "---":
        return markdown
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[i + 1 :]).lstrip("\n")
    return markdown


def update_page_markdown(page_id_value: str, markdown: str) -> None:
    run_ntn(["pages", "update", compact_id(page_id_value)], input_text=strip_yaml_frontmatter(markdown))


def get_page_markdown(page_id_value: str) -> str:
    output = run_ntn(["pages", "get", compact_id(page_id_value), "--json"])
    payload = json.loads(output)
    markdown = payload.get("markdown", {}).get("markdown", "")
    if not isinstance(markdown, str):
        raise SystemExit("unexpected Notion markdown response")
    return markdown


def get_page_blocks(page_id_value: str) -> list[dict[str, Any]]:
    output = run_ntn(["api", f"/v1/blocks/{compact_id(page_id_value)}/children"])
    payload = json.loads(output)
    results = payload.get("results", [])
    if not isinstance(results, list):
        raise SystemExit("unexpected Notion blocks response")
    return results


def set_paragraph_text(block_id: str, text: str) -> None:
    run_ntn(
        [
            "api",
            f"/v1/blocks/{compact_id(block_id)}",
            "-X",
            "PATCH",
            f"paragraph[rich_text][0][text][content]:={json.dumps(text)}",
        ]
    )


def set_heading_4_toggle(block: dict[str, Any]) -> None:
    block_id = str(block["id"])
    heading = copy.deepcopy(block.get("heading_4", {}))
    heading["is_toggleable"] = True
    run_ntn(
        [
            "api",
            f"/v1/blocks/{compact_id(block_id)}",
            "-X",
            "PATCH",
            f"heading_4:={json.dumps(heading, ensure_ascii=False)}",
        ]
    )


def append_block_children(block_id: str, children: list[dict[str, Any]]) -> None:
    if not children:
        return
    run_ntn(
        [
            "api",
            f"/v1/blocks/{compact_id(block_id)}/children",
            "-X",
            "PATCH",
            f"children:={json.dumps(children, ensure_ascii=False)}",
        ]
    )


def delete_block(block_id: str) -> None:
    run_ntn(["api", f"/v1/blocks/{compact_id(block_id)}", "-X", "DELETE"])


def block_plain_text(block: dict[str, Any]) -> str:
    block_type = block.get("type")
    content = block.get(str(block_type), {}) if block_type else {}
    rich_text = content.get("rich_text", []) if isinstance(content, dict) else []
    if not isinstance(rich_text, list):
        return ""
    return "".join(str(item.get("plain_text", "")) for item in rich_text if isinstance(item, dict))


def cleanup_legacy_seed_blocks(blocks: list[dict[str, Any]], first_paragraph_id: str) -> None:
    for block in blocks:
        block_id = str(block.get("id", ""))
        if not block_id or compact_id(block_id) == compact_id(first_paragraph_id):
            continue
        if block.get("type") == "paragraph" and not block_plain_text(block).strip():
            delete_block(block_id)
        elif block_plain_text(block).strip() == "Canonical content lives in child pages.":
            delete_block(block_id)


def appendable_block(block: dict[str, Any]) -> dict[str, Any]:
    block_type = str(block["type"])
    content = copy.deepcopy(block.get(block_type, {}))
    content.pop("children", None)
    return {"object": "block", "type": block_type, block_type: strip_nulls(content)}


def strip_nulls(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: strip_nulls(item) for key, item in value.items() if item is not None}
    if isinstance(value, list):
        return [strip_nulls(item) for item in value]
    return value


def should_toggle_details(path: str) -> bool:
    return path == "templates/idea-page" or "/overview" in path


def toggle_details_sections(page_id_value: str) -> int:
    blocks = get_page_blocks(page_id_value)
    moved = 0
    skip: set[str] = set()

    for index, block in enumerate(blocks):
        block_id = str(block.get("id", ""))
        if not block_id or block_id in skip:
            continue
        if block.get("type") != "heading_4" or block_plain_text(block).strip() != "Details":
            continue

        set_heading_4_toggle(block)
        if block.get("has_children"):
            continue

        nested: list[dict[str, Any]] = []
        delete_ids: list[str] = []
        for child in blocks[index + 1 :]:
            child_type = child.get("type")
            if child_type == "heading_2":
                break
            child_id = str(child.get("id", ""))
            if not child_id or child_id in skip:
                continue
            nested.append(appendable_block(child))
            delete_ids.append(child_id)

        append_block_children(block_id, nested)
        for child_id in delete_ids:
            delete_block(child_id)
            skip.add(child_id)
        moved += len(delete_ids)

    return moved


def refresh_description(page_id_value: str, description: str) -> bool:
    blocks = get_page_blocks(page_id_value)
    for block in blocks:
        if block.get("type") == "paragraph":
            block_id = str(block["id"])
            set_paragraph_text(block_id, description)
            cleanup_legacy_seed_blocks(blocks, block_id)
            return True
    return False


def ensure_page(config: dict[str, Any], path: str, parent_path: str) -> bool:
    pages = config["pages"]
    if path in pages and pages[path].get("id"):
        entry = pages[path]
        expected_icon = page_icon(path)
        expected_title = page_title(path)
        set_page_icon(str(entry["id"]), expected_icon)
        set_page_title(str(entry["id"]), expected_title)
        if entry.get("emoji") != expected_icon:
            entry["emoji"] = expected_icon
        if entry.get("title") != expected_title:
            entry["title"] = expected_title
        return False

    parent_id = config["root_page_id"] if not parent_path else page_id(config, parent_path)
    title = page_title(path)
    page = create_empty_page(parent_id, title)
    new_id = str(page["id"])
    set_page_icon(new_id, page_icon(path))
    update_page_markdown(new_id, default_content(path))
    pages[path] = {
        "id": compact_id(new_id),
        "title": title,
        "parent": parent_path,
        "emoji": page_icon(path),
    }
    return True


def ensure_root(config: dict[str, Any]) -> None:
    root_icon = str(config.get("root_emoji", "🧠"))
    set_page_icon(str(config["root_page_id"]), root_icon)
    set_page_title(str(config["root_page_id"]), str(config.get("root_title", "LLM Wiki")))


def cmd_seed(args: argparse.Namespace) -> None:
    config = load_config()
    created: list[str] = []
    updated_existing: list[str] = []

    ensure_root(config)
    if args.refresh_existing:
        refresh_description(str(config["root_page_id"]), ROOT_DESCRIPTION)

    for path, parent in SEED_TREE:
        was_created = ensure_page(config, path, parent)
        if was_created:
            created.append(path)
        elif args.refresh_existing:
            if path in LOCAL_CONTENT:
                update_page_markdown(page_id(config, path), default_content(path))
                if should_toggle_details(path):
                    toggle_details_sections(page_id(config, path))
            else:
                refresh_description(page_id(config, path), DEFAULT_DESCRIPTIONS[path])
            updated_existing.append(path)

    config["last_seeded"] = date.today().isoformat()
    save_config(config)

    for path in created:
        print(f"created: {path}")
    for path in updated_existing:
        print(f"updated: {path}")


def cmd_get(args: argparse.Namespace) -> None:
    config = load_config()
    sys.stdout.write(get_page_markdown(page_id(config, args.path)))


def cmd_update(args: argparse.Namespace) -> None:
    config = load_config()
    source = Path(args.file)
    if not source.is_file():
        raise SystemExit(f"not a file: {source}")
    update_page_markdown(page_id(config, args.path), source.read_text(encoding="utf-8"))
    if should_toggle_details(args.path):
        toggle_details_sections(page_id(config, args.path))
    print(f"updated: {args.path}")


def cmd_create(args: argparse.Namespace) -> None:
    config = load_config()
    pages = config["pages"]
    title = args.title or page_title(args.path)
    emoji = args.emoji or page_icon(args.path)

    if args.path in pages and pages[args.path].get("id"):
        existing_id = page_id(config, args.path)
        set_page_icon(existing_id, emoji)
        set_page_title(existing_id, title)
        pages[args.path].update({"title": title, "parent": args.parent, "emoji": emoji})
        action = "updated mapping"
    else:
        parent_id = config["root_page_id"] if not args.parent else page_id(config, args.parent)
        page = create_empty_page(parent_id, title)
        new_id = compact_id(str(page["id"]))
        set_page_icon(new_id, emoji)
        pages[args.path] = {
            "id": new_id,
            "title": title,
            "parent": args.parent,
            "emoji": emoji,
        }
        action = "created"

    if args.file:
        source = Path(args.file)
        if not source.is_file():
            raise SystemExit(f"not a file: {source}")
        update_page_markdown(page_id(config, args.path), source.read_text(encoding="utf-8"))
        if should_toggle_details(args.path):
            toggle_details_sections(page_id(config, args.path))

    save_config(config)
    print(f"{action}: {args.path}")


def cmd_toggle_details(args: argparse.Namespace) -> None:
    config = load_config()
    moved = toggle_details_sections(page_id(config, args.path))
    print(f"toggled-details: {args.path} ({moved} nested blocks)")


def cmd_pull_cache(_args: argparse.Namespace) -> None:
    config = load_config()
    CACHE.mkdir(parents=True, exist_ok=True)
    for path in sorted(config["pages"]):
        target = cache_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(get_page_markdown(page_id(config, path)), encoding="utf-8")
        print(f"cached: {path}")


def cmd_hash(_args: argparse.Namespace) -> None:
    config = load_config()
    hashes: dict[str, str] = {}
    for path in sorted(config["pages"]):
        markdown = get_page_markdown(page_id(config, path))
        hashes[path] = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
    print(json.dumps({"version": 1, "generated": date.today().isoformat(), "hashes": hashes}, indent=2))


def cmd_ls(_args: argparse.Namespace) -> None:
    config = load_config()
    for path, entry in sorted(config["pages"].items()):
        print(f"{entry.get('emoji', '')}\t{path}\t{entry.get('id', '')}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Operate the Notion-backed LLM wiki through the Notion CLI.")
    sub = parser.add_subparsers(required=True)

    seed = sub.add_parser("seed", help="Create missing standard Notion content pages.")
    seed.add_argument(
        "--refresh-existing",
        action="store_true",
        help="Refresh existing page descriptions and template pages.",
    )
    seed.set_defaults(func=cmd_seed)

    get = sub.add_parser("get", help="Print Markdown for a known Notion wiki path.")
    get.add_argument("path")
    get.set_defaults(func=cmd_get)

    update = sub.add_parser("update", help="Replace a known Notion wiki page with Markdown from a file.")
    update.add_argument("path")
    update.add_argument("file")
    update.set_defaults(func=cmd_update)

    create = sub.add_parser("create", help="Create or register a Notion wiki page path.")
    create.add_argument("path")
    create.add_argument("--parent", default="", help="Known parent path; omit for root child pages.")
    create.add_argument("--title", help="Human Notion page title.")
    create.add_argument("--emoji", help="Emoji icon for the Notion page.")
    create.add_argument("--file", help="Optional Markdown file to write after creating/registering.")
    create.set_defaults(func=cmd_create)

    toggle_details = sub.add_parser("toggle-details", help="Convert Details H4 blocks to toggle headings for a mapped page.")
    toggle_details.add_argument("path")
    toggle_details.set_defaults(func=cmd_toggle_details)

    pull = sub.add_parser("pull-cache", help="Refresh generated Markdown cache under .cache/notion/.")
    pull.set_defaults(func=cmd_pull_cache)

    hash_cmd = sub.add_parser("hash", help="Print SHA-256 hashes for all known Notion page Markdown.")
    hash_cmd.set_defaults(func=cmd_hash)

    ls = sub.add_parser("ls", help="List known Notion wiki paths and page IDs.")
    ls.set_defaults(func=cmd_ls)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
