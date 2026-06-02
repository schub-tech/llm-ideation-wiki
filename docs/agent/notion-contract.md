# Notion Contract

Notion-operational mechanics: how to read, write, and map pages via the helper script. Content and structure rules live in [wiki-contract.md](./wiki-contract.md).

## Canonical store

- Notion is canonical for user-facing `wiki/` and source `raw/` content only.
- The repo is the harness (`AGENTS.md`, `hot.md`, `wiki/index.md`, `wiki/log.md`, scripts, skills, templates). Layout: see [wiki-contract.md](./wiki-contract.md).
- `.cache/notion/` holds generated working copies — never edit as durable state. If cache or hashes disagree with Notion, Notion wins unless the last edit was accidental.

## Page conventions

- Title Case human titles, never slug-style (`bagel-shop-munich` is wrong).
- Every content page has an emoji icon; add it to `notion.config.json` when you map the page.
- Don't repeat the page title as the first body heading — Notion renders the title already.
- Scaffold pages open with one short sentence saying what belongs there.
- Path-like keys (`raw/shared/`, `wiki/<idea-slug>/`) live only in `notion.config.json` and scripts.
- Templates mirror into Notion for browsing; local `templates/` stays the source of truth.

## Root tree

The Notion root mirrors the content tree:

- `🧠 LLM Wiki`
  - `🧾 Raw` → `🔗 Shared`, `<Idea Title>`
  - `📚 Wiki` → `🎯 Founder` (after `/founder-profile`), `<Idea Title>`
  - `🧰 Templates` → `🧩 Idea Page`, `🎙️ Buyer Interview Protocol`

## CLI (`scripts/notion_wiki.py`)

- `get <path>` — print a mapped page's Markdown.
- `create <path> --parent <parent-path> --title <title> --emoji <emoji>` — create and map a page.
- `update <path> <file>` — replace a mapped page from Markdown.
- `toggle-details <path>` — convert plain `Details` H4 blocks to toggleable ones.
- `seed` — ensure standard containers exist with expected titles/icons.
- `pull-cache` — refresh `.cache/notion/` for grep and lint.
- `hash` — compute content hashes for mapped pages.
- `ls` — list mapped paths and page IDs.
- Use raw `ntn` only when the helper doesn't expose the operation.
