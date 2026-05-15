# Log

- 2026-05-15 — Initialized Notion-backed wiki tree under root page `361bc1d4596980e3ae89f90eb61b0351`; added CLI harness, page mapping, cache/hash helpers, and Notion operating instructions.
- 2026-05-15 — Corrected Notion scope to content only: `raw/` and `wiki/` remain in Notion, while agent harness files stay local.
- 2026-05-15 — Updated Notion `wiki/index.md` wording so it no longer points agents at the legacy file-based index generator.
- 2026-05-15 — Added required emoji icons to all mapped Notion content pages and recorded expected icons in `notion.config.json`.
- 2026-05-15 — Moved `wiki/index.md` and `wiki/log.md` back to local-only harness scope; Notion now excludes maintenance/navigation pages.
- 2026-05-15 — Simplified Notion content structure to idea-first pages: `raw/<idea-slug>/`, `raw/shared/`, and `wiki/<idea-slug>/`.
- 2026-05-15 — Cleaned Notion page titles/body headings to human names (`raw`, `shared`, `wiki`) while keeping path keys in the harness config.
- 2026-05-15 — Removed duplicated title headings from Notion container page bodies; page titles now live only in Notion's title field.
- 2026-05-15 — Removed dual-mode/file-based wording from agent instructions and refreshed workflow/contract docs for Notion-only content storage.
- 2026-05-15 — Ported harness simplifications from `llm-knowledge-bases` commit `7b8f13c`: removed `purpose.md` from startup, made verdicts `active|killed`, and refreshed Notion-first skills/docs.
- 2026-05-15 — Added the missing buyer-interview protocol template from `llm-knowledge-bases`, adapted for Notion child pages.
- 2026-05-15 — Added Notion `templates` pages for browsing/copying local harness templates.
- 2026-05-15 — Reworded default Notion scaffold pages with short task-focused descriptions and taught the seed helper to refresh them.
