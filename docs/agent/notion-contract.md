# Notion Wiki Contract

Use this for all raw-source and user-facing wiki content work.

## Canonical Store

- Notion is canonical for user-facing wiki content and source material only.
- The repo is the harness: `AGENTS.md`, `README.md`, `hot.md`, `wiki/index.md`, `wiki/log.md`, scripts, skills, templates, and operating instructions.
- Local files under `.cache/notion/` are generated working copies only.
- Do not edit generated cache files as durable wiki state.

## Root Tree

The Notion root page should mirror the content tree with clean human page titles:

- `🧠 LLM Wiki`
- `🧾 Raw`
- `🔗 Shared` under `Raw`
- `<Idea Title>` under `Raw`
- `📚 Wiki`
- `<Idea Title>` under `Wiki`
- `🧰 Templates`
- `🧩 Idea Page` under `Templates`
- `🎙️ Buyer Interview Protocol` under `Templates`

Use path-like keys only inside `notion.config.json` and scripts, e.g. `raw/shared/` and `wiki/<idea-slug>/`.
Notion page titles should be Title Case human names, never slug-style names such as `bagel-shop-munich`.

Templates are mirrored into Notion for browsing/copying, but the local `templates/` files remain the harness source of truth.

Every Notion content page should have an emoji icon. Add the expected icon to `notion.config.json` whenever adding a mapped page.
Do not repeat the Notion page title as the first heading in the page body; Notion already displays the title.
Default scaffold pages should open with one short task-focused sentence that explains what belongs there.

## Idea Layout

- Put idea-specific source material under `raw/<idea-slug>/`.
- Put sources that apply to multiple ideas under `raw/shared/`.
- Use `wiki/<idea-slug>/` as the idea workspace container.
- Put the current LLM-maintained synthesis under `wiki/<idea-slug>/overview`.
- Put focused deep dives as additional child pages under `wiki/<idea-slug>/`.
- Keep raw pages immutable after ingest; update wiki pages instead.

## CLI Rules

- Read local harness context first: `hot.md`, `AGENTS.md`, and relevant files under `docs/agent/`.
- Use `scripts/notion_wiki.py get <path>` to read a known page.
- Use `scripts/notion_wiki.py create <path> --parent <parent-path> --title <title> --emoji <emoji>` to create and map a new page.
- Use `scripts/notion_wiki.py update <path> <file>` to replace a known page with Markdown.
- Use `scripts/notion_wiki.py toggle-details <path>` if an overview/template page has plain `Details` H4 blocks instead of toggleable ones.
- Use `scripts/notion_wiki.py pull-cache` to refresh generated local cache for grep and lint.
- Use `scripts/notion_wiki.py hash` to calculate Notion-page content hashes.
- Use raw `ntn` only when the helper script does not expose the needed operation.

## Evidence Rules

- Keep the same provenance markers as the Markdown wiki: `^[inferred]`, `^[ambiguous]`, and `^[user-claim]`.
- Prefer durable source IDs over Notion-only visual position references.
- For raw notes, include stable source URLs, dates, and short quoted excerpts for material claims.
- If a claim depends on a Notion raw note, cite the raw note page path and the nearest heading or quote ID.

## Maintenance

- After meaningful wiki-content edits, update local `hot.md` and append one concise entry to local `wiki/log.md`.
- Keep local `wiki/index.md` as the maintained navigation page for content pages.
- If generated cache or hashes disagree with Notion, Notion wins unless the latest edit was accidental.
