#!/usr/bin/env python3

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "notion.config.json"
CACHE = ROOT / ".cache" / "notion"
# Last-edited time of each page as of our last read or write; `update` refuses when Notion moved past it.
VERSIONS = ROOT / ".cache" / "notion-versions.json"
INDEX = ROOT / "wiki" / "index.md"

NTN_TIMEOUT = float(os.environ.get("NOTION_WIKI_TIMEOUT", "120"))
NTN_ATTEMPTS = 5
# Notion refused the request, so repeating it is safe even for a create.
RATE_LIMITED = re.compile(r"\b429\b|rate.?limit", re.IGNORECASE)
# The request may have landed, so only idempotent calls repeat.
SERVER_ERROR = re.compile(r"\b(500|502|503|504)\b|timed out|connection (reset|closed)", re.IGNORECASE)
NOTION_ID = re.compile(r"[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}")

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


def run_ntn(args: list[str], *, input_text: str | None = None, idempotent: bool = True) -> str:
    """Run one ntn call with a timeout; back off and retry on 429, and on server errors when safe to repeat."""
    label = " ".join(args[:2])
    delay = 2.0
    timeouts = 0
    for attempt in range(1, NTN_ATTEMPTS + 1):
        try:
            result = subprocess.run(
                ["ntn", *args],
                cwd=ROOT,
                input=input_text,
                # `ntn api` reads a JSON body from any non-terminal stdin and waits for it to close.
                stdin=subprocess.DEVNULL if input_text is None else None,
                text=True,
                capture_output=True,
                check=False,
                timeout=NTN_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            timeouts += 1
            # One retry: a call that hangs twice will likely hang again.
            if idempotent and timeouts < 2:
                print(f"ntn {label} timed out after {NTN_TIMEOUT:.0f}s; retrying", file=sys.stderr)
                continue
            hint = "" if idempotent else "; the write may have landed, so check Notion before you retry"
            raise SystemExit(f"ntn {label} timed out after {NTN_TIMEOUT:.0f}s{hint}")
        if result.returncode == 0:
            return result.stdout
        detail = result.stderr.strip() or result.stdout.strip()
        retry = RATE_LIMITED.search(detail) or (idempotent and SERVER_ERROR.search(detail))
        if retry and attempt < NTN_ATTEMPTS:
            print(f"ntn {label}: {retry.group(0)}; retrying in {delay:.0f}s", file=sys.stderr)
            time.sleep(delay)
            delay = min(delay * 2, 60)
            continue
        raise SystemExit(f"ntn {' '.join(args)} failed: {detail}")
    raise SystemExit(f"ntn {label} failed after {NTN_ATTEMPTS} attempts")


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


def resolve_path(config: dict[str, Any], path: str) -> str:
    """Return the mapped key for path, accepting a container path without its trailing `/`."""
    pages = config.get("pages", {})
    for candidate in (path, f"{path}/", path.rstrip("/")):
        entry = pages.get(candidate)
        if isinstance(entry, dict) and entry.get("id"):
            return candidate
    raise SystemExit(f"unknown Notion page path: {path}; look it up with `find`")


def page_id(config: dict[str, Any], path: str) -> str:
    return str(config["pages"][resolve_path(config, path)]["id"])


def notion_id(value: str) -> str:
    """Accept a Notion ID or URL and return the compact ID."""
    matches = NOTION_ID.findall(value.lower())
    if not matches:
        raise SystemExit(f"not a Notion ID or URL: {value}")
    return compact_id(matches[-1])


def load_versions() -> dict[str, str]:
    if not VERSIONS.exists():
        return {}
    return json.loads(VERSIONS.read_text(encoding="utf-8"))


def record_version(page_id_value: str, edited: str) -> None:
    versions = load_versions()
    versions[compact_id(page_id_value)] = edited
    VERSIONS.parent.mkdir(parents=True, exist_ok=True)
    VERSIONS.write_text(json.dumps(versions, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def page_icon(path: str) -> str:
    return PAGE_ICONS.get(path, "📄")


def page_title(path: str) -> str:
    if path in PAGE_TITLES:
        return PAGE_TITLES[path]
    name = path.rstrip("/").split("/")[-1] or path
    return " ".join(part.capitalize() for part in re.split(r"[-_]+", name) if part)


def cache_path(path: str) -> Path:
    # `wiki/x` and `wiki/x/` can both be mapped, so a page is never stored where a folder must go.
    if path.endswith("/"):
        return CACHE / path / "_page.md"
    return CACHE / f"{path}.md"


def default_content(path: str) -> str:
    local = LOCAL_CONTENT.get(path)
    if local and local.exists():
        return template_content(path, local)
    return DEFAULT_DESCRIPTIONS.get(path, "Use this page for its mapped wiki content.") + "\n"


def template_content(path: str, source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    match = re.search(r"````markdown\n(.*?)\n````", text, flags=re.DOTALL)
    body = match.group(1).strip() if match else text.strip()
    # Comment-only lines are notes for the repo (such as fork markers); Notion would show them as text.
    body = re.sub(r"^[ \t]*<!--.*?-->[ \t]*\n", "", body, flags=re.MULTILINE)

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
        ],
        idempotent=False,
    )
    return json.loads(output)


def find_child_page(parent_id: str, title: str, skip: set[str]) -> str | None:
    for block in get_page_blocks(parent_id):
        block_id = compact_id(str(block["id"]))
        if block_id in skip:
            continue
        if block.get("type") == "child_page" and block.get("child_page", {}).get("title") == title:
            return block_id
    return None


def mapped_ids(config: dict[str, Any]) -> set[str]:
    return {compact_id(str(entry["id"])) for entry in config["pages"].values() if entry.get("id")}


def create_or_adopt_page(config: dict[str, Any], parent_id: str, title: str) -> tuple[str, bool]:
    """Return (page id, created). A same-titled child left by an interrupted earlier run is adopted, not duplicated.

    Only unmapped children are adopted: a page already mapped under another path keeps its own content.
    """
    existing = find_child_page(parent_id, title, mapped_ids(config))
    if existing:
        return existing, False
    return compact_id(str(create_empty_page(parent_id, title)["id"])), True


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


def fetch_page(page_id_value: str) -> tuple[str, str]:
    """Return (markdown, last-edited time) in one call, and record the time for the conflict guard."""
    output = run_ntn(["pages", "get", compact_id(page_id_value), "--json"])
    payload = json.loads(output)
    markdown = payload.get("markdown", {}).get("markdown", "")
    edited = str(payload.get("page", {}).get("last_edited_time", ""))
    if not isinstance(markdown, str):
        raise SystemExit("unexpected Notion markdown response")
    if edited:
        record_version(page_id_value, edited)
    return markdown, edited


def remote_edited_time(page_id_value: str) -> str:
    payload = json.loads(run_ntn(["api", f"/v1/pages/{compact_id(page_id_value)}"]))
    return str(payload.get("last_edited_time", ""))


def guard_unseen_edits(path: str, page_id_value: str) -> None:
    """Refuse a write that would overwrite Notion edits made since this checkout last read the page.

    Notion rounds edit times to the minute, so an edit in the same minute as the read can slip through.
    """
    seen = load_versions().get(compact_id(page_id_value))
    if not seen:
        raise SystemExit(f"{path}: run `get {path}` first, so this write cannot overwrite edits you have not seen (or pass --force)")
    current = remote_edited_time(page_id_value)
    if current != seen:
        raise SystemExit(
            f"{path}: changed in Notion since your last `get` (read at {seen}, now {current}); "
            "run `get` again, merge, then update (or pass --force)"
        )


def refresh_cache_entry(path: str, page_id_value: str) -> None:
    """Re-read one page after a write: refreshes its cache file and its recorded version."""
    markdown, _ = fetch_page(page_id_value)
    target = cache_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(markdown, encoding="utf-8")


def get_page_blocks(page_id_value: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    cursor = ""
    while True:
        args = ["api", f"/v1/blocks/{compact_id(page_id_value)}/children", "page_size==100"]
        if cursor:
            args.append(f"start_cursor=={cursor}")
        payload = json.loads(run_ntn(args))
        batch = payload.get("results", [])
        if not isinstance(batch, list):
            raise SystemExit("unexpected Notion blocks response")
        results.extend(batch)
        if not payload.get("has_more") or not payload.get("next_cursor"):
            return results
        cursor = str(payload["next_cursor"])


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
        ],
        idempotent=False,
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


def appendable_block(block: dict[str, Any], depth: int = 0) -> dict[str, Any]:
    """Copy a block for re-appending, with its children: a table without its rows is rejected."""
    block_type = str(block["type"])
    content = copy.deepcopy(block.get(block_type, {}))
    content.pop("children", None)
    # The append endpoint takes two levels of nesting; the toggle holding this block is the first.
    if block.get("has_children") and depth < 1:
        children = [appendable_block(child, depth + 1) for child in get_page_blocks(str(block["id"]))]
        if children:
            content["children"] = children
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


def ensure_page(config: dict[str, Any], path: str, parent_path: str) -> str:
    """Make sure a seed page exists; return "created", "adopted", or "existing"."""
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
        return "existing"

    parent_id = config["root_page_id"] if not parent_path else page_id(config, parent_path)
    title = page_title(path)
    new_id, created = create_or_adopt_page(config, parent_id, title)
    pages[path] = {
        "id": new_id,
        "title": title,
        "parent": parent_path,
        "emoji": page_icon(path),
    }
    save_config(config)
    set_page_icon(new_id, page_icon(path))
    if not created:
        return "adopted"
    update_page_markdown(new_id, default_content(path))
    return "created"


def ensure_root(config: dict[str, Any]) -> None:
    root_icon = str(config.get("root_emoji", "🧠"))
    set_page_icon(str(config["root_page_id"]), root_icon)
    set_page_title(str(config["root_page_id"]), str(config.get("root_title", "LLM Wiki")))


def cmd_seed(args: argparse.Namespace) -> None:
    config = load_config()
    report: list[str] = []

    ensure_root(config)
    if args.refresh_existing:
        refresh_description(str(config["root_page_id"]), ROOT_DESCRIPTION)

    for path, parent in SEED_TREE:
        state = ensure_page(config, path, parent)
        if state != "existing":
            report.append(f"{state}: {path}")
        elif args.refresh_existing:
            if path in LOCAL_CONTENT:
                update_page_markdown(page_id(config, path), default_content(path))
                if should_toggle_details(path):
                    toggle_details_sections(page_id(config, path))
            else:
                refresh_description(page_id(config, path), DEFAULT_DESCRIPTIONS[path])
            report.append(f"updated: {path}")

    config["last_seeded"] = date.today().isoformat()
    save_config(config)
    print("\n".join(report))


def mapped_path(config: dict[str, Any], path: str) -> str | None:
    try:
        return resolve_path(config, path)
    except SystemExit:
        return None


def page_target(config: dict[str, Any], value: str) -> tuple[str, str]:
    """Return (cache key, page id) for a mapped path, or for a Notion ID or URL of an unmapped page."""
    path = mapped_path(config, value)
    if path:
        return path, page_id(config, path)
    if not NOTION_ID.search(value.lower()):
        resolve_path(config, value)  # raises the unknown-path error
    target = notion_id(value)
    return f"_unmapped/{target}", target


def read_markdown_file(name: str) -> str:
    source = Path(name)
    if not source.is_file():
        raise SystemExit(f"not a file: {source}")
    return source.read_text(encoding="utf-8")


def write_page(path: str, target: str, markdown: str) -> None:
    update_page_markdown(target, markdown)
    if should_toggle_details(path):
        toggle_details_sections(target)
    refresh_cache_entry(path, target)


def cmd_get(args: argparse.Namespace) -> None:
    path, target = page_target(load_config(), args.path)
    markdown, _ = fetch_page(target)
    cache_file = cache_path(path)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(markdown, encoding="utf-8")
    sys.stdout.write(markdown)


def cmd_update(args: argparse.Namespace) -> None:
    path, target = page_target(load_config(), args.path)
    markdown = read_markdown_file(args.file)
    if not args.force:
        guard_unseen_edits(args.path, target)
    write_page(path, target, markdown)
    print(f"updated: {args.path}")


def promote_to_container(config: dict[str, Any], path: str) -> str:
    """Re-key a page mapped without its trailing `/` once it gets a child, so it reads as a container."""
    pages = config["pages"]
    container = f"{path}/"
    pages[container] = pages.pop(path)
    for entry in pages.values():
        if entry.get("parent") == path:
            entry["parent"] = container
    return container


def cmd_create(args: argparse.Namespace) -> None:
    config = load_config()
    pages = config["pages"]
    parent = resolve_path(config, args.parent) if args.parent else ""
    existing = mapped_path(config, args.path)
    if not existing and parent and not parent.endswith("/") and args.path.startswith(f"{parent}/"):
        parent = promote_to_container(config, parent)
    path = existing or args.path
    title = args.title or page_title(path)
    emoji = args.emoji or page_icon(path)
    markdown = read_markdown_file(args.file) if args.file else None

    if existing:
        target = page_id(config, path)
        if markdown is not None and not args.force:
            guard_unseen_edits(path, target)
        set_page_icon(target, emoji)
        set_page_title(target, title)
        pages[path].update({"title": title, "parent": parent, "emoji": emoji})
        action = "updated mapping"
    else:
        parent_id = config["root_page_id"] if not parent else page_id(config, parent)
        target, created = create_or_adopt_page(config, parent_id, title)
        pages[path] = {"id": target, "title": title, "parent": parent, "emoji": emoji}
        # Map the page before anything else can fail, so a rerun finds it instead of creating a twin.
        save_config(config)
        if not created and markdown is not None and not args.force:
            guard_unseen_edits(path, target)
        set_page_icon(target, emoji)
        action = "created" if created else "mapped existing page"

    if args.summary:
        pages[path]["summary"] = args.summary
    save_config(config)

    if markdown is not None:
        write_page(path, target, markdown)
    else:
        refresh_cache_entry(path, target)
    print(f"{action}: {path}")


def cmd_toggle_details(args: argparse.Namespace) -> None:
    config = load_config()
    path = resolve_path(config, args.path)
    moved = toggle_details_sections(page_id(config, path))
    refresh_cache_entry(path, page_id(config, path))
    print(f"toggled-details: {path} ({moved} nested blocks)")


def cmd_pull_cache(_args: argparse.Namespace) -> None:
    config = load_config()
    CACHE.mkdir(parents=True, exist_ok=True)
    for path in sorted(config["pages"]):
        refresh_cache_entry(path, page_id(config, path))
        print(f"cached: {path}")


def cmd_ls(_args: argparse.Namespace) -> None:
    config = load_config()
    for path, entry in sorted(config["pages"].items()):
        print(f"{entry.get('emoji', '')}\t{path}\t{entry.get('id', '')}")


def require_root(config: dict[str, Any]) -> None:
    if not config.get("root_page_id"):
        raise SystemExit("no Notion root configured; run /onboarding first")


def notion_url(page_id_value: str) -> str:
    return f"https://www.notion.so/{compact_id(page_id_value)}"


def cmd_find(args: argparse.Namespace) -> None:
    config = load_config()
    require_root(config)
    terms = [term.lower() for term in args.query]
    hits = []
    for path, entry in sorted(config["pages"].items()):
        haystack = f"{path} {entry.get('title', '')} {entry.get('summary', '')}".lower()
        if all(term in haystack for term in terms):
            hits.append((path, entry))
    if not hits:
        raise SystemExit(f"no mapped page matches: {' '.join(args.query)}")
    for path, entry in hits[: args.limit]:
        print(f"{entry.get('emoji', '')}\t{path}\t{entry.get('title', '')}\t{notion_url(str(entry.get('id', '')))}")
    if len(hits) > args.limit:
        print(f"… {len(hits) - args.limit} more; add words to narrow the search", file=sys.stderr)


def cmd_describe(args: argparse.Namespace) -> None:
    config = load_config()
    path = resolve_path(config, args.path)
    config["pages"][path]["summary"] = args.summary
    save_config(config)
    print(f"described: {path}")


def database_target(config: dict[str, Any], value: str) -> str:
    """Return the ID behind a mapped path, or the ID in a database or data source URL."""
    path = mapped_path(config, value)
    return page_id(config, path) if path else notion_id(value)


def data_source_id(target: str) -> str:
    """Resolve a database ID to its single data source; an ID that is not a database is taken as a data source."""
    try:
        payload = json.loads(run_ntn(["datasources", "resolve", target, "--json"]))
    except SystemExit:
        return target
    sources = payload.get("data_sources", [])
    if len(sources) != 1:
        names = ", ".join(f"{source.get('name')} ({compact_id(source.get('id', ''))})" for source in sources)
        raise SystemExit(f"database has {len(sources)} data sources; pass one of: {names}")
    return compact_id(str(sources[0]["id"]))


def property_text(prop: dict[str, Any]) -> str:
    kind = str(prop.get("type", ""))
    value = prop.get(kind)
    if value is None:
        return ""
    if kind in ("title", "rich_text"):
        return "".join(str(part.get("plain_text", "")) for part in value)
    if kind in ("select", "status"):
        return str(value.get("name", ""))
    if kind == "multi_select":
        return ", ".join(str(option.get("name", "")) for option in value)
    if kind in ("people", "created_by", "last_edited_by"):
        people = value if isinstance(value, list) else [value]
        return ", ".join(str(person.get("name") or person.get("id", "")) for person in people)
    if kind == "relation":
        return ", ".join(compact_id(str(item.get("id", ""))) for item in value)
    if kind == "date":
        end = value.get("end")
        return str(value.get("start", "")) + (f" to {end}" if end else "")
    if kind == "checkbox":
        return "yes" if value else "no"
    if kind == "formula":
        return str(value.get(value.get("type"), "") or "")
    if kind == "unique_id":
        prefix = value.get("prefix")
        return f"{prefix}-{value.get('number')}" if prefix else str(value.get("number", ""))
    if kind == "files":
        return ", ".join(str(item.get("name", "")) for item in value)
    return str(value)


def cmd_query(args: argparse.Namespace) -> None:
    target = database_target(load_config(), args.database)
    command = ["datasources", "query", target, "--json", "--limit", str(args.limit)]
    if args.filter:
        command += ["--filter", args.filter]
    for sort in args.sort or []:
        command += ["--sort", sort]
    payload = json.loads(run_ntn(command))
    rows = payload.get("results", [])
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return
    if not rows:
        print("no rows")
        return
    properties = rows[0].get("properties", {})
    names = sorted(properties, key=lambda name: (properties[name].get("type") != "title", name))
    print("\t".join(["url", *names]))
    for row in rows:
        values = [property_text(row.get("properties", {}).get(name, {})) for name in names]
        cells = [notion_url(str(row.get("id", ""))), *values]
        print("\t".join(re.sub(r"\s+", " ", cell).strip() for cell in cells))
    if payload.get("has_more"):
        print(f"… more rows; raise --limit above {args.limit} or narrow --filter", file=sys.stderr)


def property_value(name: str, kind: str, value: str) -> dict[str, Any]:
    """Build a Notion property payload from command-line text."""
    items = [item.strip() for item in value.split(",") if item.strip()]
    if kind in ("title", "rich_text"):
        return {kind: [{"text": {"content": value}}]}
    if kind == "number":
        try:
            return {kind: float(value) if value else None}
        except ValueError:
            raise SystemExit(f"{name}: not a number: {value!r}") from None
    if kind in ("select", "status"):
        return {kind: {"name": value} if value else None}
    if kind == "multi_select":
        return {kind: [{"name": item} for item in items]}
    if kind == "date":
        return {kind: {"start": value} if value else None}
    if kind == "checkbox":
        return {kind: value.strip().lower() in {"1", "true", "yes", "y", "x"}}
    if kind in ("url", "email", "phone_number"):
        return {kind: value or None}
    if kind in ("people", "relation"):
        return {kind: [{"id": notion_id(item)} for item in items]}
    raise SystemExit(f"{name}: a {kind} property cannot be set from the command line")


def cmd_add_row(args: argparse.Namespace) -> None:
    source = data_source_id(database_target(load_config(), args.database))
    schema = json.loads(run_ntn(["api", f"/v1/data_sources/{source}"])).get("properties", {})
    title_name = next((name for name, spec in schema.items() if spec.get("type") == "title"), None)
    if not title_name:
        raise SystemExit("data source has no title property")

    properties = {title_name: property_value(title_name, "title", args.title)}
    for assignment in args.set or []:
        name, sep, value = assignment.partition("=")
        if not sep or name not in schema:
            raise SystemExit(f"--set {assignment!r}: expected Name=value, where Name is one of: {', '.join(schema)}")
        properties[name] = property_value(name, str(schema[name].get("type")), value)

    matches: list[dict[str, Any]] = []
    if not args.new:
        title_filter = json.dumps({"property": title_name, "title": {"equals": args.title}}, ensure_ascii=False)
        found = run_ntn(["datasources", "query", source, "--json", "--limit", "5", "--filter", title_filter])
        matches = json.loads(found).get("results", [])
    if len(matches) > 1:
        raise SystemExit(f"{len(matches)} rows are titled {args.title!r}; pass --new to add another")

    markdown = read_markdown_file(args.file) if args.file else None
    if matches:
        row_id = compact_id(str(matches[0]["id"]))
        if markdown is not None and not args.force:
            guard_unseen_edits(notion_url(row_id), row_id)
        body = json.dumps({"properties": properties}, ensure_ascii=False)
        run_ntn(["api", f"/v1/pages/{row_id}", "-X", "PATCH", "-d", body])
        action = "updated"
    else:
        body = json.dumps({"parent": {"data_source_id": source}, "properties": properties}, ensure_ascii=False)
        row_id = compact_id(str(json.loads(run_ntn(["api", "/v1/pages", "-X", "POST", "-d", body], idempotent=False))["id"]))
        action = "created"

    if markdown is not None:
        update_page_markdown(row_id, markdown)
    fetch_page(row_id)
    print(f"{action}: {args.title}\t{notion_url(row_id)}")


def index_line(entry: dict[str, Any], indent: str = "", target: dict[str, Any] | None = None) -> str:
    link = notion_url(str((target or entry).get("id", "")))
    line = f"{indent}- {entry.get('emoji', '')} [{entry.get('title', '')}]({link})"
    if entry.get("summary"):
        line += f" — {entry['summary']}"
    return line


def render_index(config: dict[str, Any]) -> str:
    pages = config["pages"]
    idea_slugs = sorted(
        match.group(1) for path in pages if (match := re.fullmatch(r"wiki/([^/]+)/", path))
    )
    wiki_pages = sorted(path for path in pages if re.fullmatch(r"wiki/[^/]+", path))
    shared = sorted(path for path in pages if path.startswith("raw/shared/") and path != "raw/shared/")
    templates = sorted(path for path in pages if path.startswith("templates/") and path != "templates/")

    lines = [
        "# Index",
        "",
        "Generated by `scripts/notion_wiki.py index` from `notion.config.json`. Regenerate it; edits here are overwritten.",
        "",
    ]

    if wiki_pages:
        lines += ["## Wiki", ""]
        lines += [index_line(pages[path]) for path in wiki_pages]
        lines.append("")

    lines += ["## Ideas", ""]
    if not idea_slugs:
        lines.append("- None yet. Run `/onboarding`, then `/founder-profile`, then `/new-idea`.")
    for slug in idea_slugs:
        container = f"wiki/{slug}/"
        overview = pages.get(f"{container}overview")
        lines.append(index_line(pages[container], target=overview))
        for path in sorted(pages):
            if path.startswith(container) and path not in (container, f"{container}overview"):
                lines.append(index_line(pages[path], indent="  "))
    lines.append("")

    if shared:
        lines += ["## Shared sources", ""]
        lines += [index_line(pages[path]) for path in shared]
        lines.append("")

    if templates:
        lines += ["## Templates", ""]
        lines += [index_line(pages[path]) for path in templates]
        lines.append("")

    return "\n".join(lines)


def cmd_index(args: argparse.Namespace) -> None:
    content = render_index(load_config())
    if args.stdout:
        sys.stdout.write(content)
        return
    INDEX.write_text(content, encoding="utf-8")
    print(f"wrote: {INDEX.relative_to(ROOT)}")


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

    force_help = "Write even if the page changed in Notion since your last `get`."

    get = sub.add_parser("get", help="Print a page's Markdown and record its version for the update guard.")
    get.add_argument("path", help="Mapped path, or the Notion ID or URL of an unmapped page.")
    get.set_defaults(func=cmd_get)

    update = sub.add_parser("update", help="Replace a page with Markdown from a file; refuses if Notion changed since `get`.")
    update.add_argument("path", help="Mapped path, or the Notion ID or URL of an unmapped page.")
    update.add_argument("file")
    update.add_argument("--force", action="store_true", help=force_help)
    update.set_defaults(func=cmd_update)

    create = sub.add_parser("create", help="Create and map a page; a rerun reuses the page instead of duplicating it.")
    create.add_argument("path")
    create.add_argument("--parent", default="", help="Known parent path; omit for root child pages.")
    create.add_argument("--title", help="Human Notion page title.")
    create.add_argument("--emoji", help="Emoji icon for the Notion page.")
    create.add_argument("--file", help="Optional Markdown file to write after creating/registering.")
    create.add_argument("--summary", help="One-line hook shown in wiki/index.md and matched by find.")
    create.add_argument("--force", action="store_true", help=force_help)
    create.set_defaults(func=cmd_create)

    query = sub.add_parser("query", help="List database rows as tab-separated values: URL, then one column per property.")
    query.add_argument("database", help="Mapped path, or a database or data source ID or URL.")
    query.add_argument("--filter", help="Notion filter JSON, passed through unchanged.")
    query.add_argument("--sort", action="append", help="`<property> [asc|desc]`; repeat for several.")
    query.add_argument("--limit", type=int, default=100, help="Maximum rows to return.")
    query.add_argument("--json", action="store_true", help="Print the raw row objects instead.")
    query.set_defaults(func=cmd_query)

    add_row = sub.add_parser("add-row", help="Add a database row, or update the row with the same title.")
    add_row.add_argument("database", help="Mapped path, or a database or data source ID or URL.")
    add_row.add_argument("--title", required=True, help="Value of the title property; also the key for finding an existing row.")
    add_row.add_argument("--set", action="append", metavar="NAME=VALUE", help="Set a property; comma-separate multi-select, people, and relation values.")
    add_row.add_argument("--file", help="Optional Markdown file for the row's page body.")
    add_row.add_argument("--new", action="store_true", help="Always add a row, even if one with this title exists.")
    add_row.add_argument("--force", action="store_true", help=force_help)
    add_row.set_defaults(func=cmd_add_row)

    find = sub.add_parser("find", help="Search mapped page paths, titles, and summaries; print path, title, and Notion URL.")
    find.add_argument("query", nargs="+", help="Words that must all appear (case-insensitive).")
    find.add_argument("--limit", type=int, default=40, help="Maximum matches to print.")
    find.set_defaults(func=cmd_find)

    describe = sub.add_parser("describe", help="Set the one-line summary of a mapped page.")
    describe.add_argument("path")
    describe.add_argument("summary")
    describe.set_defaults(func=cmd_describe)

    index = sub.add_parser("index", help="Regenerate wiki/index.md from notion.config.json.")
    index.add_argument("--stdout", action="store_true", help="Print instead of writing the file.")
    index.set_defaults(func=cmd_index)

    toggle_details = sub.add_parser("toggle-details", help="Convert Details H4 blocks to toggle headings for a mapped page.")
    toggle_details.add_argument("path")
    toggle_details.set_defaults(func=cmd_toggle_details)

    pull = sub.add_parser("pull-cache", help="Re-read every mapped page into .cache/notion/ for broad local search.")
    pull.set_defaults(func=cmd_pull_cache)

    ls = sub.add_parser("ls", help="List known Notion wiki paths and page IDs.")
    ls.set_defaults(func=cmd_ls)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
