---
name: research
description: Surface research gaps in the wiki and propose a plan to fill them. Reads an idea overview's "Still to validate" lines, "What we do not know" entries, and "Next moves," then proposes targeted research questions tagged by strategy (ask the user, do web research, or both). Use when the user wants to deepen an idea, fill gaps, or says "research this" / "what should I research next" / "what's missing".
---

Convert the wiki's existing open questions into a concrete research plan. Don't invent new questions — start from what the idea overview already flags as unvalidated, then group, prioritize, and propose a strategy for each.

**Read the wiki first.** Start with `wiki/index.md`, then the idea overview, then its deep-dive notes. Pull every "Still to validate" line, every "What we do not know" entry, and every numbered move under "Next moves." Skip questions the wiki already answers — those are noise.

**Cluster each gap by research strategy:**

- **Ask the user.** Things only the user knows — domain experience, network, prior conversations, direct buyer access, founder-fit detail.
- **Web research.** Things that should be in public sources — competitor pricing, regulatory deadlines, named partners, market sizing, dated triggers.
- **Hybrid.** Things that need a user hint to find the right web target ("is there a Texas DIR equivalent in your actual market?").

**Propose the plan as a numbered list.** For each item, name the question, the strategy, the wiki section it would feed, and rough effort (one search vs. deep dive). Lead with questions that would flip the verdict — fatal-flaw checks first, decoration last. If a question is decorative (would not change the verdict either way), say so and recommend dropping it.

**Confirm scope with the user before executing:**

- Which questions to pursue this round (don't over-batch).
- Time range for web research (e.g., "since 2024", "all time").
- Depth (one search → one note vs. multiple search rounds → comprehensive note).
- Whether to run web items in parallel via `/research-deep`.

**Hand off.** For web items, invoke `/research-deep` with the confirmed questions. For user-question items, surface them inline one at a time and capture the answers — short answers go directly into the relevant `Still to validate` line in the wiki overview; longer answers may warrant a new raw idea note in `raw/ideas/`.

Apply the AGENTS.md principles: tie every proposed question to a specific wiki claim it would confirm or kill ("this would test the 60%-selector-drift bank-case figure"); don't propose research the user could answer in two minutes; default to skepticism — if a "Still to validate" line is hedging vague concerns, sharpen the question before researching it; be direct about which questions are decoration vs. which would actually move the verdict.

The goal is to convert the wiki's open-question inventory into a small, ordered, actionable research plan — not a wishlist.
