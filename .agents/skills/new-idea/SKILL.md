---
name: new-idea
description: Create a new idea workspace in the Notion-backed LLM Ideation Wiki. Use after onboarding and founder-profile, when the user wants to add the first idea, create another idea, or start working on a new business idea.
---

Create one new idea workspace in Notion.

**Preflight.**

1. Read `docs/agent/notion-contract.md` and `templates/idea-page.md`.
2. Run `scripts/notion_wiki.py find wiki/`. If it reports no Notion root, stop and tell the user to run `/onboarding` first. If it finds no `wiki/` page, run `scripts/notion_wiki.py seed --refresh-existing`.
3. If `scripts/notion_wiki.py find wiki/founder` finds nothing, stop and tell the user to run `/founder-profile` first.

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

1. Set the idea's index hook with `scripts/notion_wiki.py describe wiki/<idea-slug>/ "<one line>"`, then run the ritual (`AGENTS.md` § Mechanics).
2. Tell the user where the idea lives and suggest `/grill-me` or `/find-gaps` as the next step.

**Rules.**

- Create exactly one idea per run.
- Do not invent evidence. The first overview can mostly be gaps.
