---
name: research-deep
description: Execute web research on specific questions and write findings to Notion `raw/<idea-slug>/` or `raw/shared/` as new raw source pages. Use after `/find-gaps` produces a confirmed plan, or when the user gives a direct research question (e.g. "research X" / "find me data on Y" / "look up Z").
---

Run targeted web research on one or more research questions and produce raw notes, then propose distilling them into the wiki via `docs/agent/workflows.md`. Maintaining the wiki is the LLM's job, not the user's — don't leave the raw notes sitting unintegrated.

**Identify the question.** From a `/find-gaps` plan or a direct user prompt. If vague, narrow it before searching ("research the market" → "What 2024-2025 sources support or contradict the TAM figure cited in the overview's Market section?"). Read the relevant Notion `raw/<idea-slug>/` page and `raw/shared/` first to avoid retreading ground — if a recent note already covers the question, say so and ask the user whether to skip, supplement, or refresh.

**Plan and execute searches.** Draft 2-4 targeted queries per question and run them. Read the most relevant sources end-to-end, not just snippets — snippets lose date and context. For multiple research questions in one session, consider launching one sub-agent per question so they run concurrently; each sub-agent owns its question end-to-end (queries, source reading, raw-note write) and returns when done. The parent agent then compiles the report-back.

**Write one raw source page per research question** under the relevant Notion `raw/<idea-slug>/` page, or under `raw/shared/` if it applies across ideas. Title it with a date and topic, e.g. `2026-04-24 market pricing research`. Each raw page should:

- State the originating question at the top (one sentence).
- Capture findings with **source URL, publication date, and direct quote** for every material claim.
- Mark uncertain or contested claims as `[uncertain]` with a one-line reason.
- Surface contradictions across sources explicitly instead of picking the most flattering one.
- Distinguish facts (what a source says) from synthesis (what the agent concludes from multiple sources).
- End with a `## Suggested wiki integration` section: which idea overview / deep-dive section would update, and a one-line draft of the diff.

**Report back.** After all notes are written (or all sub-agents have returned), list them with a one-line summary each, ordered by what would most move the verdict. Flag findings that confirm a load-bearing claim, findings that kill one, and questions where the search returned no useful evidence.

**Suggest the ingest pass.** Once the raw pages exist, propose running the ingest workflow in `docs/agent/workflows.md` next — distilling the new findings into the relevant Notion idea page and child pages, merging with existing synthesis instead of appending duplicates, updating local `wiki/index.md` if navigation changed, updating `hot.md`, and appending to `wiki/log.md`. Offer to do it directly. Don't leave new evidence as raw-only.

Cite real URLs only — never fabricate one. If a search returns nothing useful, say so explicitly rather than padding the note with adjacent content.
