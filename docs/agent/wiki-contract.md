# Wiki Contract

Use this when creating or editing wiki pages, source references, provenance markers, or idea structure.

## Layout

- `purpose.md` — durable intent: decision criteria, active portfolio, and current gating questions.
- `hot.md` — short recent-state cache. Keep it current after meaningful writes.
- `.manifest.json` — raw-source ledger with hashes, ingest status, and touched wiki pages.
- `raw/` — immutable source material.
  - `raw/notes/` — articles, reports, transcripts, research runs.
  - `raw/ideas/` — brainstorms and seed notes.
  - `raw/assets/` — images and attachments.
- `wiki/` — compiled layer the LLM maintains.
  - `wiki/ideas/<idea>/overview.md` — load-bearing idea page.
  - Supporting deep dives live alongside the overview as `type: "note"`.
  - `wiki/index.md` — auto-generated.
  - `wiki/log.md` — append-only dated change log.

## Page Frontmatter

Every wiki page except `wiki/index.md` and `wiki/log.md` starts with:

```yaml
---
title: "Page Title"
type: "idea|note|query|lint"
summary: "One-line summary."
status: "seed|active|stale"
verdict: "exploring|pursuing|parked|killed"  # idea pages only
tags: ["tag-one", "tag-two"]
source_files: ["raw/path/file.md"]
updated: "YYYY-MM-DD"
---
```

`type` controls index visibility: `idea`, `query`, and `lint` show up in `wiki/index.md`; `note` is reachable from the overview's Related section.

## Provenance Markers

Keep evidence and synthesis distinguishable next to the claim.

- Directly supported claims get a raw-source line citation and no marker.
- `^[inferred]` marks synthesis, implications, or claims combined across sources.
- `^[ambiguous]` marks contested, weak, unclear, or methodology-limited claims.
- `^[user-claim]` marks founder/user assertions that are not independently validated.

If a paragraph mixes sourced fact and interpretation, split it so the marker attaches to the specific inferred or ambiguous claim.

## Idea Pages

Use `templates/idea-page.md` for `overview.md`. Push detailed evidence into supporting notes instead of overloading the overview.

## Writing Rules

- Concise markdown; broad pages over many narrow pages.
- Cite raw sources with line anchors for material claims, e.g. `[label L27-L31](../../raw/notes/file.md#L27-L31)`.
- Cite the paragraph that makes the claim checkable, not every sentence.
- Preserve uncertainty explicitly; distinguish facts, synthesis, user claims, and open questions.
- Add a `## Related` section when a page has obvious neighbors.
