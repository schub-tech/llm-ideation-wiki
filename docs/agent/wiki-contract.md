# Wiki Contract

Content and structure rules for wiki pages, sources, provenance, and idea layout. Notion mechanics (CLI, page conventions) live in [notion-contract.md](./notion-contract.md).

## Layout

- Local `hot.md` — short recent-state cache; keep current after meaningful writes.
- Local `wiki/index.md` — navigation for idea pages.
- Local `wiki/log.md` — append-only dated change log.
- Notion `raw/` — source material, immutable after ingest; update `wiki/` instead.
  - `raw/shared/` — applies to multiple ideas. `raw/<idea-slug>/` — idea-specific.
- Notion `wiki/` — the LLM-maintained, user-facing compiled layer.
  - `wiki/founder` — founder ambition, constraints, risk profile.
  - `wiki/<idea-slug>/` — idea workspace; `…/overview` — load-bearing synthesis; deep dives as sibling child pages.

## Provenance markers

Keep evidence and synthesis distinguishable next to the claim.

- No marker — directly supported; carries a raw-source citation.
- `^[inferred]` — synthesis, implications, or claims combined across sources.
- `^[ambiguous]` — contested, weak, unclear, or methodology-limited claims.
- `^[user-claim]` — founder/user assertions not independently validated.
- If a paragraph mixes sourced fact and interpretation, split it so the marker attaches to the specific claim.

## Idea pages

- Verdicts are binary: `active` or `killed`.
- Run `/founder-profile` before the first idea so pages have a founder decision frame.
- Use `templates/idea-page.md` as the `…/overview` scaffold; push detailed evidence into sibling deep-dive pages, not the overview.
- Each `Details` heading is a toggleable H4 so section leads stay scannable. `create`/`update` auto-convert `#### Details` on `*/overview` and `templates/idea-page` paths — don't write raw Notion toggle syntax.

## Writing

- Concise markdown; prefer broad pages over many narrow ones.
- Cite the paragraph, quote, or source section that makes a claim checkable — not every sentence. Use stable Notion paths, source URLs, quote IDs, or nearest-heading references.
- Preserve uncertainty: distinguish fact, synthesis, user claim, and open question.
- Add a `Related` section when a page has obvious neighbors.
- No YAML frontmatter in page bodies — metadata lives in `notion.config.json` and Notion properties; Notion renders a `---` block as visible text. (The upload script strips a leading block as a safety net.)
- Scannable and current-state rules: see [AGENTS.md](../../AGENTS.md), applied on every edit.
