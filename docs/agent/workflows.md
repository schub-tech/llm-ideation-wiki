# Agent Workflows

Step sequences for setup, ingest, answering, lint, and sync. Commands: see [notion-contract.md](./notion-contract.md). Output and maintenance rules: [AGENTS.md](../../AGENTS.md).

## Fresh setup

Three separate skills, in order:

1. `/onboarding` — connect the Notion root; seed empty `Raw`, `Wiki`, `Templates`.
2. `/founder-profile` — create `wiki/founder`.
3. `/new-idea` — create one idea workspace and initial overview.

Don't create ideas during onboarding, or before the founder profile exists, unless the user changes the project rules.

## Ingest a raw source

Read first: local `hot.md`, `wiki/index.md`, the relevant Notion `wiki/<idea-slug>/overview`, and related raw pages.

1. **Analyze** before editing: material claims, entities, decisions, contradictions, affected pages, provenance state, open questions.
2. **Write**: distill into the relevant `…/overview` and supporting child pages. Merge with existing synthesis; don't append duplicate summaries or create per-source summary pages.

Then run the maintenance ritual:

1. Update `wiki/index.md` if navigation changed.
2. Update `hot.md`.
3. Append one dated line to `wiki/log.md`.
4. Run `pull-cache` then `hash` to verify the mapping still reads cleanly.

## Answer a question

- Read `hot.md` and `wiki/index.md` first, then the relevant `…/overview` and raw sources. Use `pull-cache` when broad search beats targeted reads.
- Name a shaky premise before answering. Cite pages and sources relied on. Surface contradictions; don't smooth them. Say so if the wiki doesn't answer it.
- If the answer is durable, update the existing wiki page and refresh index/log/hot.

## Lint

Deterministic checks:

```bash
python3 -m json.tool notion.config.json >/dev/null
python3 -m py_compile scripts/notion_wiki.py
scripts/check_agent_symlinks.py
scripts/notion_wiki.py pull-cache
scripts/notion_wiki.py hash
```

Semantic lint via `/wiki-lint`: unsupported claims, unmarked synthesis, ambiguity drift, user-only premises, stale claims, risk/verdict mismatch, answered validations. Fix the wiki directly unless findings warrant a local lint note.

## Sync from outside the vault

Treat like ingest, but import only what's worth remembering. Skip raw implementation detail unless it's the actual lesson.
