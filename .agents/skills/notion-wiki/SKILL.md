---
name: notion-wiki
description: Operate the LLM ideation wiki from a Notion root page through the Notion CLI. Use when wiki content lives in Notion and agents need to read, write, seed, cache, hash, or maintain pages via `ntn`.
---

Use Notion as the canonical store for raw material and user-facing wiki content. The local repo is the harness.

**Start here.**

1. Read `notion.config.json`.
2. Read `docs/agent/notion-contract.md`.
3. Read local `purpose.md`, `hot.md`, and `wiki/index.md`.

**Read pages.**

- Use `scripts/notion_wiki.py get <path>` for known pages.
- Use `scripts/notion_wiki.py pull-cache` before broad search or lint work.
- Treat `.cache/notion/` as generated scratch, not durable state.
- Do not read local `raw/` or user-facing `wiki/` pages as canonical when `notion.config.json` exists.
- Local `wiki/index.md` and `wiki/log.md` are harness files, not Notion content.

**Write pages.**

- Draft the full Markdown replacement in a temporary or reviewable local file.
- Run `scripts/notion_wiki.py update <path> <file>`.
- Re-read the page with `scripts/notion_wiki.py get <path>` after updating.
- Update `hot.md` and append one short `wiki/log.md` entry after meaningful wiki edits.

**Create new pages.**

- Create idea-specific source pages under `raw/<idea-slug>/`.
- Create cross-idea source pages under `raw/shared/`.
- Create idea synthesis pages under `wiki/<idea-slug>/`.
- Prefer extending `scripts/notion_wiki.py` or using raw `ntn api /v1/pages` for new content paths.
- If creating manually, create the Notion page via `ntn api /v1/pages` so the title property is set, then update Markdown content with `ntn pages update`.
- Set an emoji icon on every Notion content page.
- Do not repeat the page title as a body heading.
- Add the new page ID and emoji to `notion.config.json` immediately.

**Preserve the wiki contract.**

- Keep claims evidence-bound.
- Mark synthesis with `^[inferred]`.
- Mark weak or contested claims with `^[ambiguous]`.
- Mark founder/user assertions with `^[user-claim]`.
- Do not narrate page history inside durable pages; use `wiki/log.md` for change history.
