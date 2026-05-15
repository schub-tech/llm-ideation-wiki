---
name: new-idea
description: Create a new idea workspace in the Notion-backed LLM Ideation Wiki. Use after onboarding and founder-profile, when the user wants to add the first idea, create another idea, or start working on a new business idea.
---

Create one new idea workspace in Notion.

**Preflight.**

1. Read `hot.md`, `wiki/index.md`, `notion.config.json`, `docs/agent/notion-contract.md`, and `templates/idea-page.md`.
2. If `notion.config.json` has no `root_page_id`, stop and tell the user to run `/onboarding` first.
3. If `wiki/` is missing from `notion.config.json`, run `scripts/notion_wiki.py seed --refresh-existing`.
4. If `wiki/founder` is missing from `notion.config.json`, stop and tell the user to run `/founder-profile` first.

**Ask first.**

If the user has not already provided it, ask for the idea in a few sentences.

Do not proceed until you have the idea.

**Create pages.**

1. Infer a short idea title from the user's description.
2. Turn the title into a slug for path keys, for example `bagel-shop-munich`.
3. Use Title Case human page titles in Notion, not slug-style titles.
4. Create `raw/<idea-slug>/` under `Raw` with an emoji.
5. Create `raw/<idea-slug>/founder-note` with the user's initial idea. Mark it as source material, not synthesis.
6. Create `wiki/<idea-slug>/` under `Wiki` as the idea workspace container.
7. Create `wiki/<idea-slug>/overview` from `templates/idea-page.md`.
8. Fill only what the initial idea and `wiki/founder` support. Mark founder claims as `^[user-claim]`, inferred synthesis as `^[inferred]`, and uncertain claims as `^[ambiguous]`.
9. Set an emoji on every Notion page.

Use `scripts/notion_wiki.py create <path> --parent <parent-path> --title <title> --emoji <emoji> --file <file>` for new mapped pages and `scripts/notion_wiki.py update <path> <file>` for durable writes.

**Finish.**

1. Run `scripts/notion_wiki.py pull-cache`.
2. Run `scripts/notion_wiki.py hash`.
3. Run `scripts/notion_wiki.py ls`.
4. Update local `wiki/index.md`.
5. Update local `hot.md`.
6. Append one short entry to local `wiki/log.md`.
7. Tell the user where the idea lives and suggest `/grill-me` or `/research` as the next step.

**Rules.**

- Create exactly one idea per run.
- Do not invent evidence. The first overview can mostly be gaps.
- Keep raw founder notes under `raw/<idea-slug>/`; keep synthesis under `wiki/<idea-slug>/overview`.
- Do not put harness files into Notion.
