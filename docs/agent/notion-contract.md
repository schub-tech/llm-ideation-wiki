# Notion Wiki Contract

Use this when the wiki is operating from a Notion root page instead of local Markdown files.

## Canonical Store

- Notion is canonical for user-facing wiki content and source material only.
- The repo is the harness: `AGENTS.md`, `README.md`, `purpose.md`, `hot.md`, `wiki/index.md`, `wiki/log.md`, scripts, skills, templates, and operating instructions.
- Local files under `.cache/notion/` are generated working copies only.
- Do not edit generated cache files as durable wiki state.

## Root Tree

The Notion root page should mirror the content tree with clean human page titles:

- `🧠 LLM-Wiki`
- `🧾 raw`
- `🔗 shared` under `raw`
- `<idea-slug>` under `raw`
- `📚 wiki`
- `<idea-slug>` under `wiki`

Use path-like keys only inside `notion.config.json` and scripts, e.g. `raw/shared/` and `wiki/<idea-slug>/`.

Every Notion content page should have an emoji icon. Add the expected icon to `notion.config.json` whenever adding a mapped page.
Do not repeat the Notion page title as the first heading in the page body; Notion already displays the title.

## Idea Layout

- Put idea-specific source material under `raw/<idea-slug>/`.
- Put sources that apply to multiple ideas under `raw/shared/`.
- Put LLM-maintained synthesis under `wiki/<idea-slug>/`.
- Keep raw pages immutable after ingest; update wiki pages instead.

## CLI Rules

- Read local harness context first: `purpose.md`, `hot.md`, `AGENTS.md`, and relevant files under `docs/agent/`.
- Use `scripts/notion_wiki.py get <path>` to read a known page.
- Use `scripts/notion_wiki.py update <path> <file>` to replace a known page with Markdown.
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
