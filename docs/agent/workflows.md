# Agent Workflows

Use this when answering wiki questions, ingesting sources, or maintaining the compiled layer.

## Ingest A Raw Source

Read `purpose.md`, `hot.md`, `wiki/index.md`, the relevant overview, and related deep dives first.

Work in two phases:

1. Analysis: identify material claims, entities, decisions, contradictions, affected pages, provenance state (`direct`, `inferred`, `ambiguous`, `user-claim`), and open questions before editing.
2. Write: distill into the relevant overview and deep-dive notes. Merge with existing synthesis instead of appending duplicate summaries. Do not create per-source summary pages.

After meaningful edits:

1. Run `scripts/rebuild_index.py`.
2. Refresh `.manifest.json` with `scripts/update_manifest.py`.
3. Update `hot.md`.
4. Append one short dated entry to `wiki/log.md`.

## Answer A Question

Read `purpose.md`, `hot.md`, and `wiki/index.md` first, then the relevant overview and deep-dive notes. Grep only when cheaper passes are inconclusive.

If the premise is shaky, name it before answering. Cite pages or raw sources relied on. Surface contradictions instead of smoothing them. If the wiki does not answer something, say so. If the answer is durable, update the existing wiki page and refresh index/log/hot/manifest as needed.

## Lint

Run deterministic checks first:

```bash
scripts/wiki_status.py
scripts/check_wikilinks.py
scripts/find_orphans.py
```

For semantic lint, use `/wiki-lint`: unsupported material claims, unmarked synthesis, ambiguity drift, user-only premises, stale claims, risk/verdict mismatch, and answered validations.

Fix the wiki directly unless findings are substantial enough to warrant a `type: "lint"` page.

## Sync From Outside The Vault

Treat external material like ingest, but import only what is worth remembering. Avoid raw implementation detail unless it is the actual lesson.

## Scripts

- `scripts/rebuild_index.py` — regenerate `wiki/index.md`.
- `scripts/wiki_status.py` — compare `raw/` with `.manifest.json`.
- `scripts/update_manifest.py` — refresh raw-source hashes and wiki coverage.
- `scripts/check_wikilinks.py` — find broken markdown links.
- `scripts/find_orphans.py` — find wiki pages with no inbound links.
