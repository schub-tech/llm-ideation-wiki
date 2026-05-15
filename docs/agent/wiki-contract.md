# Wiki Contract

Use this when creating or editing wiki pages, source references, provenance markers, or idea structure.

## Layout

- Local `purpose.md` — durable intent: decision criteria, active portfolio, and current gating questions.
- Local `hot.md` — short recent-state cache. Keep it current after meaningful writes.
- Local `wiki/index.md` — navigation for idea pages.
- Local `wiki/log.md` — append-only dated change log.
- Notion `raw/` — immutable source material.
  - Notion `raw/shared/` — source material that applies to multiple ideas.
  - Notion `raw/<idea-slug>/` — idea-specific source material.
- Notion `wiki/` — user-facing compiled layer the LLM maintains.
  - Notion `wiki/<idea-slug>/` — load-bearing idea synthesis.
  - Supporting deep dives live as child pages under the relevant idea page.

## Page Metadata

Every Notion content page should have:

- A clean human title, not a path-like title.
- An emoji icon.
- A logical path entry in `notion.config.json` if the agent must address it by script.

Do not repeat the Notion page title as the first heading in the page body.

## Provenance Markers

Keep evidence and synthesis distinguishable next to the claim.

- Directly supported claims get a raw-source citation and no marker.
- `^[inferred]` marks synthesis, implications, or claims combined across sources.
- `^[ambiguous]` marks contested, weak, unclear, or methodology-limited claims.
- `^[user-claim]` marks founder/user assertions that are not independently validated.

If a paragraph mixes sourced fact and interpretation, split it so the marker attaches to the specific inferred or ambiguous claim.

## Idea Pages

Use `templates/idea-page.md` as the content scaffold for Notion `wiki/<idea-slug>/`. Push detailed evidence into supporting child pages instead of overloading the main idea page.

## Writing Rules

- Concise markdown; broad pages over many narrow pages.
- Cite raw sources with stable Notion page paths, source URLs, quote IDs, or nearest-heading references.
- Cite the paragraph, quote, or source section that makes the claim checkable, not every sentence.
- Preserve uncertainty explicitly; distinguish facts, synthesis, user claims, and open questions.
- Add a `Related` section when a page has obvious neighbors.

## Scannable, Not Wall Of Text

The reader should grasp a section's load-bearing claims in about 30 seconds of scanning. Bullets and tables first, prose only when genuinely sequential.

Anti-patterns to refuse:

- **Multi-claim paragraphs where the lede is buried.** Three sentences of context before the actual point. Open with the punchline, then evidence.
- **Bullets that are themselves dense paragraphs.** A single bullet containing 4+ distinct claims joined by semicolons. Split into multiple bullets, or use a sub-list.
- **Long details blocks written as prose.** If the content is a list of supporting facts, write it as a list.
- **Repeated context phrases across bullets.** Factor shared qualifiers into the section lede.
- **Throat-clearing intros.** Delete phrases like "It is worth noting that" and lead with the claim.

Default shapes:

- **Section:** one-sentence lede; then bullets, table, or sub-sections.
- **Bullet:** one claim, optional one-sentence elaboration, citation.
- **Table:** comparing at least three items on at least two dimensions, or at least two items on at least three dimensions.
- **Prose paragraph:** acceptable when the argument is genuinely sequential and bulletizing would lose the through-line.

## Current State, Not History

Wiki pages describe what is true now. They are not changelogs.

When you correct a page, replace the old framing. Do not narrate over it.

Reject these patterns:

- "The earlier version of this page treated X as Y."
- "The wiki previously softened this to Y."
- "**Update 2026-MM-DD:** ..."
- "This used to mean Y; now it means Z."

Acceptable time markers:

- A dated external-fact qualifier when the fact may move.
- Dated entries inside local `wiki/log.md`.

Why this rule: a reader scanning the wiki for current state should not have to parse what is true versus what used to be true.
