---
name: onboarding
description: Set up a new Notion-backed LLM Ideation Wiki from a fresh clone. Use when the user asks to get started, onboard, initialize the wiki, connect a Notion root page, or create the first idea.
---

Set up the repo as a Notion-backed idea wiki.

**Ask first.**

If the user has not already provided them, ask for:

1. The Notion page URL to use as the wiki root.
2. The first idea in a few sentences.

Do not proceed until you have both.

**Set up Notion.**

1. Read `README.md`, `AGENTS.md`, `docs/agent/notion-contract.md`, and `notion.config.json` if it exists.
2. Run `ntn doctor`. If the CLI is not authenticated, ask the user to run `ntn login`.
3. Extract the page ID from the Notion URL and store it as the compact ID in `notion.config.json`.
4. For a new wiki root, reset `pages` in `notion.config.json` before seeding so old demo page IDs are not reused.
5. Set `mode` to `notion-cli`, keep `version: 1`, and store `root_url`, `root_page_id`, `root_title`, and `root_emoji`.
6. Run `scripts/notion_wiki.py seed --refresh-existing` to create `Raw`, `Shared`, `Wiki`, and `Templates`.

**Create the first idea.**

1. Infer a short idea title from the user's description, then turn it into a slug for path keys, for example `bagel-shop-munich`.
2. Use Title Case human page titles in Notion, not slug-style titles.
3. Create `raw/<idea-slug>/` under `Raw` with an emoji.
4. Create `raw/<idea-slug>/founder-note` with the user's initial idea.
5. Create `wiki/<idea-slug>/` under `Wiki` as the idea workspace container.
6. Create `wiki/<idea-slug>/overview` from `templates/idea-page.md`.
7. Fill only what the initial idea supports. Mark founder claims as `^[user-claim]`, inferred synthesis as `^[inferred]`, and uncertain claims as `^[ambiguous]`.
8. Set an emoji on every Notion page.

Use `scripts/notion_wiki.py create <path> --parent <parent-path> --title <title> --emoji <emoji> --file <file>` for new mapped pages and `scripts/notion_wiki.py update <path> <file>` for durable writes.

**Finish.**

1. Run `scripts/notion_wiki.py pull-cache`.
2. Run `scripts/notion_wiki.py hash`.
3. Run `scripts/notion_wiki.py ls`.
4. Update local `wiki/index.md`.
5. Update local `hot.md`.
6. Append one short entry to local `wiki/log.md`.

**Rules.**

- Notion is canonical for `raw/` source material and user-facing `wiki/` content.
- The repo is the harness: `README.md`, `AGENTS.md`, `hot.md`, `wiki/index.md`, `wiki/log.md`, `docs/`, `templates/`, scripts, and skills.
- Do not put harness files into Notion.
- Do not invent evidence during onboarding; the first overview can mostly be gaps.
- If the root page title or icon cannot be read, default to `LLM Wiki` and `🧠`.
