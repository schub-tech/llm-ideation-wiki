# Idea Page Template

Scaffold for Notion `wiki/<idea-slug>/overview`. The shape is adapted from the schub day format — each section has a slide-ready lead paragraph followed by a toggleable `#### Details` block holding the supporting evidence and open questions. A reader scanning only the section leads should get the picture. When a section's evidence starts to overflow, spin it into a sibling deep-dive child page under the same idea workspace and link from `Related`.

## Scaffold

Copy the block below into Notion `wiki/<idea-slug>/overview`.

````markdown
---
title: "Idea Title"
type: "idea"
summary: "One-line summary for index generation."
status: "seed"
verdict: "active"
tags: []
source_files: []
updated: "YYYY-MM-DD"
---

# Idea Title

One-sentence reframing of the idea — what it actually is, in plain language.

## Problem

The customer pain in one paragraph, with the sharpest single statistic if there is one.

#### Details

Concrete numbers from the corpus with raw-source citations.

**Who feels it (ICP):**
The persona(s) with the pain *and* budget authority. Use `Not locked. Candidates: ...` rather than inventing a placeholder.

**Still to validate:**
What primary evidence would confirm or kill the framing.

## Solution

What you'd do, in as few words as possible. If unlocked, lead with "Not locked" and gesture at the interesting zone.

#### Details

Candidate wedges with viability or evidence notes, time-bound mandates.

**Still to validate:**
Which wedge has buyer pull; what economics or capability assumptions need testing.

## Traction

The numbers that matter — revenue, pilots, conversations, signed LOIs. In research mode this is usually empty: lead with the honest empty state (e.g. "None yet. Pre-validation. Currently N raw notes synthesized into M deep-dive pages plus this overview.") and let Details carry the why.

#### Details

Pilots, conversations, signed LOIs, revenue, retention, growth — or the why behind the empty state.

**Still to validate:**
What primary signal would move this off zero.

## Why this works

The insight + timing argument in one sentence. Fold the timing pressure (commoditization clock, dated triggers, regulatory deadlines) into the same section so the reader sees insight and "why now" together. Mark synthesis that combines multiple sources with `^[inferred]`.

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

Size of the prize and the vision if the bet plays out — TAM forecast, the slice you're targeting, and what the company looks like at scale.

#### Details

Top-line TAM forecasts with raw-source citations. Per-account revenue ladder if relevant (entry-point → retainer → managed services → outcome pricing). Push incumbent mapping and structural detail into a deep-dive note.

**Still to validate:**
Buyer behavior under switching events; consolidation timing; which slice actually pays.

## Team

What makes the founder(s) particularly well suited — domain expertise, technical capability, unfair advantages. In a personal vault before the founder fills it in, lead with one sentence framing what needs filling; the corpus typically already names the gaps any team will need to close.

#### Details

[Founder fit profile when filled in.] Concrete gaps the corpus has named — partner-tier credibility, regulated-industry security posture, delivery-network economics, etc. — with a path for each (earn it, hire for it, partner around it).

**Still to validate:**
Which gaps the founder already closes vs. which must be hired or partnered for.

## Risks

The three-to-five things most likely to kill the idea. For each, name the disconfirming signal and link to the supporting deep-dive page.

- **Risk 1.** One-sentence framing. → see [supporting-page.md](./supporting-page.md).
- **Risk 2.** ...

Use provenance markers where the evidence is not direct:

- `^[inferred]` for synthesis or implications.
- `^[ambiguous]` for contested, weak, or methodology-limited claims.
- `^[user-claim]` for founder/user assertions that still need outside validation.

## Next moves

The gating sentence — which move blocks everything else right now. In research mode this is usually a validation step; once validated, it becomes the build ask (capital, hires, partnerships, and what each unlocks).

**To validate:** numbered list of concrete research or customer-discovery actions. Order matters — name which moves gate the others.

1. ...

**To build (once validated):** capital, hires, partnerships, and what each unlocks. Skip until validation moves are landing.

## Related

- [Deep-dive 1](./deep-dive-1.md) — one-line description.
- [Deep-dive 2](./deep-dive-2.md) — ...
````
