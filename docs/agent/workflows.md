# Agent Workflows

Use this when answering wiki questions, ingesting sources, or maintaining the compiled layer.

## Fresh Setup

Use three separate skills:

1. `/onboarding` connects the Notion root and seeds empty `Raw`, `Wiki`, and `Templates` pages.
2. `/founder-profile` creates `wiki/founder`.
3. `/new-idea` creates one idea workspace and initial overview.

Do not create ideas during onboarding. Do not create ideas before the founder profile exists unless the user explicitly changes the project rules.

## Ingest A Raw Source

Read local `hot.md`, local `wiki/index.md`, the relevant Notion `wiki/<idea-slug>/overview` page, and related Notion raw pages first.

Work in two phases:

1. Analysis: identify material claims, entities, decisions, contradictions, affected pages, provenance state (`direct`, `inferred`, `ambiguous`, `user-claim`), and open questions before editing.
2. Write: distill into the relevant Notion `wiki/<idea-slug>/overview` page and supporting child pages. Merge with existing synthesis instead of appending duplicate summaries. Do not create per-source summary pages.

After meaningful edits:

1. Update local `wiki/index.md` if navigation changed.
2. Update local `hot.md`.
3. Append one short dated entry to local `wiki/log.md`.
4. Run `scripts/notion_wiki.py pull-cache` and `scripts/notion_wiki.py hash` to verify the Notion mapping still reads cleanly.

## Answer A Question

Read local `hot.md` and local `wiki/index.md` first, then the relevant Notion `wiki/<idea-slug>/overview` page and Notion raw sources. Use `scripts/notion_wiki.py pull-cache` when broad search is cheaper than targeted reads.

If the premise is shaky, name it before answering. Cite pages or raw sources relied on. Surface contradictions instead of smoothing them. If the wiki does not answer something, say so. If the answer is durable, update the existing Notion wiki page and refresh local index/log/hot as needed.

## Lint

Use deterministic checks that understand the Notion mapping:

```bash
python3 -m json.tool notion.config.json >/dev/null
python3 -m py_compile scripts/notion_wiki.py
scripts/check_agent_symlinks.py
scripts/notion_wiki.py pull-cache
scripts/notion_wiki.py hash
```

For semantic lint, use `/wiki-lint`: unsupported material claims, unmarked synthesis, ambiguity drift, user-only premises, stale claims, risk/verdict mismatch, and answered validations.

Fix the wiki directly unless findings are substantial enough to warrant a local lint note.

## Sync From Outside The Vault

Treat external material like ingest, but import only what is worth remembering. Avoid raw implementation detail unless it is the actual lesson.

## Scripts

- `scripts/notion_wiki.py get <path>` — print Markdown for a mapped Notion content page.
- `scripts/notion_wiki.py update <path> <file>` — replace a mapped Notion content page from Markdown.
- `scripts/notion_wiki.py seed` — ensure the standard Notion content containers exist and have expected titles/icons.
- `scripts/notion_wiki.py pull-cache` — refresh generated Markdown cache under `.cache/notion/`.
- `scripts/notion_wiki.py hash` — calculate Notion content hashes for mapped pages.
