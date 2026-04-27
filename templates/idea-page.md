# Idea Page Template

Scaffold for `wiki/ideas/<idea>/overview.md`. The shape is adapted from a YC seed pitch deck — each section has a slide-ready lead paragraph followed by a `#### Details` block holding the supporting evidence and open questions. A reader scanning only the section leads should get the picture.

## Rules

- **The lead carries the section.** A reader who only reads the paragraph under `## Section name` should still get the answer. If the lead hedges, rewrite it.
- **No `*To fill in.*` placeholders.** Either write the real content, name a concrete gap (e.g. `**Gaps to close (from the corpus):**`), or omit the sub-block.
- **Risks and Related skip the Details block.** Risks are already one-liner-with-link; Related is a short pointer list.
- **Why-now lives inside Why-this-works.** Don't split timing into its own section.
- **Use `#### Details` H4 headings, not HTML `<details>` toggles.** Obsidian renders the toggles unevenly; plain markdown is consistent.
- **`verdict`:** `exploring` (default) → `pursuing` (committed) → `parked` (deprioritized) or `killed` (decided against). Update on change and note in `wiki/log.md`.

## Pitch-deck-mode translations

- **Traction** is usually empty in research mode. Write the empty state honestly as the lead — "None yet. Pre-validation. Currently N raw notes synthesized into M deep-dive pages plus this overview." Use Details for the *why*.
- **Team** in a personal vault often has no completed answer. Lead with one sentence framing what the founder needs to fill in; use Details for the corpus-derived "Gaps to close."
- **Ask** becomes **Next moves.** Lead with the gating sentence; numbered list inside Details.

## Scaffold

Copy the block below into `wiki/ideas/<idea>/overview.md`.

````markdown
---
title: "Idea Title"
type: "idea"
summary: "One-line summary for index generation."
status: "seed"
verdict: "exploring"
tags: []
source_files: []
updated: "YYYY-MM-DD"
---

# Idea Title

One-sentence reframing of the idea. Verdict: `exploring|pursuing|parked|killed` — and the one sentence that says what would flip the verdict.

## Problem

The customer pain in one paragraph, with the sharpest single statistic if there is one.

#### Details

Concrete numbers from the corpus with raw-source citations.

**Who feels it (ICP):**
The persona(s) with the pain *and* budget authority. Use `Not locked. Candidates: ...` rather than inventing a placeholder.

**Still to validate:**
What primary evidence would confirm or kill the framing.

→ Optional pointer to a deep-dive page.

## Solution

What you'd do, in as few words as possible. If unlocked, lead with "Not locked" and gesture at the interesting zone.

#### Details

Candidate wedges with viability or evidence notes, time-bound mandates.

**Still to validate:**
Which wedge has buyer pull; what economics or capability assumptions need testing.

## Traction

The numbers that matter, or an honest empty-state if pre-validation.

#### Details

The why behind the empty state, or — once there are numbers — pilots, conversations, signed LOIs, revenue, retention, growth.

## Why this works

The insight + timing argument in one sentence. Fold the timing pressure (commoditization clock, dated triggers, regulatory deadlines) into the same section so the reader sees insight and "why now" together.

#### Details

The N supporting claims:

- **Claim 1.** Inline evidence and raw-source citation.
- **Claim 2.** ...
- **Timing pressure compresses the window.** Dated triggers and commoditization clock — what specific events open the buyer's budget *now* and what happens if you miss the window.

**Still to validate:**
What capability or assumption would invalidate the insight; how fast competing forces actually move.

## Business model

How money flows. Pricing shape, gross-margin source, expansion path. Call out the margin pool explicitly.

#### Details

Pricing reference points from the corpus — fixed-fee bands, retainer ranges, enterprise managed-services bands, hourly rates, outcome-pricing existence proofs.

**Still to validate:**
Margin viability at the proposed price; ladder mechanics; channel economics.

## Market

Size of the prize *and* the structural shape — both matter. Lead with the macro forecast (TAM), then the slice you're targeting, then how crowded that slice is.

#### Details

**Size of the prize:**

- **Category macro.** Top-line TAM forecasts with raw-source citations.
- **Per-account revenue ladder.** Entry-point → retainer → managed services → outcome pricing. Existence proofs at each rung.
- **Long-term consolidation dynamics.** Whether the category trends toward winner-take-most or fragments.

**Vision.**
The destination if the bet plays out — what the company looks like at scale and where the moat compounds. Conditional on the gate this idea is currently failing.

**Structural map:**

- **Top:** named incumbents at the high end.
- **Mid:** named incumbents at the middle.
- **Bottom:** offshore / freelance / commodity layer.
- **Moats and barriers:** partner-status gates, regulatory moats, certifications.

**Still to validate:**
Buyer behavior under switching events; stickiness of incumbent relationships; consolidation timing.

→ Optional pointer to a deep-dive page.

## Team

What makes the founder(s) particularly well suited — domain expertise, technical capability, unfair advantages. The fit profile is for the founder to fill in; the corpus typically already names the gaps any team will need to close.

#### Details

[Founder fit profile when filled in.]

**Gaps to close (from the corpus):**

- Concrete gaps the corpus has named — partner-tier credibility, regulated-industry security posture, delivery-network economics, trigger-incident operating credibility, etc. Each one has a path (earn it, hire for it, partner around it).

**Still to validate:**
Which gaps the founder already closes vs. which must be hired or partnered for.

## Risks to the thesis

The three-to-five things most likely to kill the idea. For each, name the disconfirming signal and link to the supporting deep-dive page.

- **Risk 1.** One-sentence framing. → see [supporting-page.md](./supporting-page.md).
- **Risk 2.** ...

## Next moves

The gating sentence — which moves block everything else.

#### Details

Numbered list of concrete research or customer-discovery actions. Order matters — name which moves gate the others.

1. ...

## Related

- [Deep-dive 1](./deep-dive-1.md) — one-line description.
- [Deep-dive 2](./deep-dive-2.md) — ...
````
