---
title: "Hot Cache"
updated: "2026-05-15"
---

# Hot Cache

Short recent-state cache for the next agent session. Read after `purpose.md` and before broad repo scans.

## Recent Activity

- Notion content storage was initialized from root page `361bc1d4596980e3ae89f90eb61b0351`.
- Standard content pages now exist in Notion and are mapped in `notion.config.json`.
- Harness pages stay local: `purpose.md`, `hot.md`, `README.md`, `wiki/index.md`, `wiki/log.md`, `docs/`, `templates/`, scripts, and skills are not canonical Notion content.
- Use `scripts/notion_wiki.py get <path>` for canonical reads and `scripts/notion_wiki.py update <path> <file>` for canonical writes.

## Active Threads

- Migration is at content-tree stage: Notion is canonical storage for `raw/<idea-slug>/`, `raw/shared/`, and `wiki/<idea-slug>/`; remaining old file-oriented scripts should be replaced with Notion-native helpers.

## Maintenance State

- No idea content has been added yet.
- `wiki/index.md` should stay empty of idea pages until the first Notion `wiki/<idea-slug>/` page is created.
- Generated cache belongs under `.cache/notion/` and is not durable state.
