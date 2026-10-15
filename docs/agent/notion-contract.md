# Notion Contract

Notion-operational mechanics: how to read, write, and map pages via the helper script. Content and structure rules live in [wiki-contract.md](./wiki-contract.md).

## Canonical store

- Notion is canonical for user-facing `wiki/` and source `raw/` content only.
- The repo is the harness (`AGENTS.md`, `hot.md`, `wiki/index.md`, `wiki/log.md`, scripts, skills, templates). Layout: see [wiki-contract.md](./wiki-contract.md).
- `.cache/notion/` holds generated working copies — never edit as durable state. If the cache disagrees with Notion, Notion wins unless the last edit was accidental.
- `.cache/notion-versions.json` records each page's last-edited time as of your last read or write. `update` checks it to avoid overwriting edits you have not seen.

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

Container paths end in `/` (`wiki/<idea-slug>/`), but every command also accepts them without it.

- `find <words>` — list mapped pages whose path, title, or summary contains every word, with Notion links. Use it instead of reading `notion.config.json`.
- `get <path>` — print a page's Markdown, cache it, and record its version. Also takes the Notion ID or URL of an unmapped page.
- `update <path> <file> [--force]` — replace a page from Markdown. It refuses when Notion changed since your last `get`; read again and merge rather than reach for `--force`. Notion rounds edit times to the minute, so an edit in the same minute as your `get` can slip through. The record is shared by every session in this checkout: two parallel agent sessions editing the same page can still overwrite each other, so give each page one writer at a time.
- `create <path> --parent <parent-path> --title <title> --emoji <emoji> [--summary <hook>] [--file <file>]` — create and map a page, optionally with content. A rerun is safe: it reuses the mapped page, or adopts a same-titled child of the parent instead of creating a twin.
- `describe <path> <summary>` — set the one-line hook that `index` and `find` show.
- `index` — regenerate `wiki/index.md` from the mapping.
- `query <database> [--filter <json>] [--sort "<property> desc"] [--limit N] [--json]` — list database rows as tab-separated values. Takes a mapped path or a database or data source ID or URL.
- `add-row <database> --title <title> [--set Name=value ...] [--file <file>] [--new]` — add a row, or update the row that already has this title. Comma-separate multi-select, people, and relation values.
- `toggle-details <path>` — convert plain `Details` H4 blocks to toggleable ones.
- `seed` — ensure standard containers exist with expected titles/icons.
- `pull-cache` — re-read every mapped page into `.cache/notion/` for broad grep and lint. It costs one call per page, so it is not part of the ritual.
- `ls` — list mapped paths and page IDs.
- Every call times out after 120 seconds (`NOTION_WIKI_TIMEOUT` overrides) and backs off on rate limits (HTTP 429).
- Use raw `ntn` only when the helper doesn't expose the operation. From a script or agent shell, close stdin (`< /dev/null`): `ntn api` otherwise waits for a request body that never comes.
