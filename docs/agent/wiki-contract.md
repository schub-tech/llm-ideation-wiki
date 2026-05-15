# Wiki Contract

Use this when creating or editing wiki pages, source references, provenance markers, or idea structure.

## Layout

- Local `hot.md` — short recent-state cache. Keep it current after meaningful writes.
- Local `wiki/index.md` — navigation for idea pages.
- Local `wiki/log.md` — append-only dated change log.
- Notion `raw/` — immutable source material.
  - Notion `raw/shared/` — source material that applies to multiple ideas.
  - Notion `raw/<idea-slug>/` — idea-specific source material.
- Notion `wiki/` — user-facing compiled layer the LLM maintains.
  - Notion `wiki/founder` — founder ambition, constraints, and risk profile.
  - Notion `wiki/<idea-slug>/` — idea workspace container.
  - Notion `wiki/<idea-slug>/overview` — load-bearing idea synthesis.
  - Supporting deep dives live as sibling child pages under the same idea workspace.

## Page Metadata

Every Notion content page should have:

- A clean human title, not a path-like title.
- An emoji icon.
- A logical path entry in `notion.config.json` if the agent must address it by script.
- Idea verdicts are binary: `active` or `killed`.

Do not repeat the Notion page title as the first heading in the page body.

## Provenance Markers

Keep evidence and synthesis distinguishable next to the claim.

- Directly supported claims get a raw-source citation and no marker.
- `^[inferred]` marks synthesis, implications, or claims combined across sources.
- `^[ambiguous]` marks contested, weak, unclear, or methodology-limited claims.
- `^[user-claim]` marks founder/user assertions that are not independently validated.

If a paragraph mixes sourced fact and interpretation, split it so the marker attaches to the specific inferred or ambiguous claim.

## Idea Pages

Run `/founder-profile` before creating the first idea so idea pages have a founder-level decision frame.
Use `templates/idea-page.md` as the content scaffold for Notion `wiki/<idea-slug>/overview`. Push detailed evidence into supporting child pages instead of overloading the overview page.
In overview pages, each `Details` heading should be a toggleable H4 so the section lead stays scannable.

## Writing Rules

- Concise markdown; broad pages over many narrow pages.
- Cite raw sources with stable Notion page paths, source URLs, quote IDs, or nearest-heading references.
- Cite the paragraph, quote, or source section that makes the claim checkable, not every sentence.
- Preserve uncertainty explicitly; distinguish facts, synthesis, user claims, and open questions.
- Add a `Related` section when a page has obvious neighbors.

## Scannable And Current

Both rules are stated in [AGENTS.md](../../AGENTS.md) — lead with bullets/tables, and describe current state rather than narrating history. Apply them on every edit.
