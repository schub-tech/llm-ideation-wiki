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

## Scannable, Not Wall of Text

The reader should grasp a section's load-bearing claims in ~30 seconds of scanning. Bullets and tables first, prose only when genuinely sequential.

Anti-patterns to refuse:

- **Multi-claim paragraphs where the lede is buried.** Three sentences of context before the actual point. → Open with the punchline, then evidence.
- **Bullets that are themselves dense paragraphs.** A single bullet containing 4+ distinct claims joined by semicolons. → Split into multiple bullets, or use a sub-list.
- **Long `#### Details` blocks written as prose.** If the content is a list of supporting facts, write it as a list. → Bulletize.
- **Repeated context phrases across bullets.** Same qualifier ("for the energy vertical", "per the slide deck", "as a 1-2 person shop") repeated five bullets in a row. → Factor into the section lede.
- **Throat-clearing intros.** "It is worth noting that…", "Importantly,…", "As mentioned above,…", "It should be emphasized that…" → Delete, lead with the claim.

Default shapes:

- **Section:** one-sentence lede; then bullets, table, or sub-sections.
- **Bullet:** one claim, optional one-sentence elaboration, citation.
- **Table:** comparing ≥3 items on ≥2 dimensions, or ≥2 items on ≥3 dimensions.
- **Prose paragraph:** acceptable when the argument is genuinely sequential and bulletizing would lose the through-line (Why this works, Vision, narrative analysis). Even then, lead with the punchline.

A page that already exists but has drifted into wall-of-text should be tightened on the next edit pass — not later. The fix is usually: identify the lede, promote it to the section opener, bulletize the rest, and delete throat-clearing connective tissue.

## Current State, Not History

Wiki pages describe what is true now. They are not changelogs.

When you correct a page, **replace** the old framing — do not narrate over it. The following anti-patterns are out, no exceptions:

- *"The earlier version of this page treated X as Y. That was wrong."* → Just write the current framing.
- *"The wiki previously softened this to 'plausible but dangerous'."* → State the current verdict directly.
- *"An earlier version of this page framed the question as binary."* → Open with the correct frame.
- *"**Update 2026-05-04:** UiPath has shipped X."* → Drop the "Update" prefix; write the fact in current tense.
- *"This used to mean Y; now it means Z."* → Write Z.

Acceptable time markers, narrowly scoped:

- The frontmatter `updated:` field.
- `as of YYYY-MM-DD` qualifying a specific external-fact claim that may move (e.g. "as of 2026-05-04, UiPath/skills ships ~19 skills") — dates a fact, not the wiki's stance on it.
- Dated entries inside `wiki/log.md` only. The log is append-only and is where revision narrative belongs.

Why this rule: a reader scanning the wiki for current state should not have to parse what's true vs. what *used to be* true. Meta-narrative wrappers carry no forward-looking value, bloat the page, and erode signal density.
