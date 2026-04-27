---
name: research-deep
description: Execute web research on specific questions and write findings to `raw/notes/` as new raw notes. Use after `/research` produces a confirmed plan, or when the user gives a direct research question (e.g. "research X" / "find me data on Y" / "look up Z").
---

Run targeted web research on one or more research questions and produce raw notes, then propose distilling them into the wiki via the AGENTS.md ingest workflow. Maintaining the wiki is the LLM's job, not the user's — don't leave the raw notes sitting unintegrated.

**Identify the question.** From a `/research` plan or a direct user prompt. If vague, narrow it before searching ("research the market" → "What 2024-2025 sources support or contradict the TAM figure cited in the overview's Market section?"). Read the existing `raw/notes/` directory first to avoid retreading ground — if a recent note already covers the question, say so and ask the user whether to skip, supplement, or refresh.

**Plan and execute searches.** Draft 2-4 targeted queries per question and run them. Read the most relevant sources end-to-end, not just snippets — snippets lose date and context. For multiple research questions in one session, consider launching one sub-agent per question so they run concurrently; each sub-agent owns its question end-to-end (queries, source reading, raw-note write) and returns when done. The parent agent then compiles the report-back.

**Write one raw note per research question** in `raw/notes/`, file-named by the convention `YYYY-MM-DD-<topic>-<type>.md` (e.g. `2026-04-24-market-pricing-research.md`). Each raw note should:

- State the originating question at the top (one sentence).
- Capture findings with **source URL, publication date, and direct quote** for every material claim.
- Mark uncertain or contested claims as `[uncertain]` with a one-line reason.
- Surface contradictions across sources explicitly instead of picking the most flattering one.
- Distinguish facts (what a source says) from synthesis (what the agent concludes from multiple sources).
- End with a `## Suggested wiki integration` section: which idea overview / deep-dive section would update, and a one-line draft of the diff.

**Report back.** After all notes are written (or all sub-agents have returned), list them with a one-line summary each, ordered by what would most move the verdict. Flag findings that confirm a load-bearing claim, findings that kill one, and questions where the search returned no useful evidence.

**Suggest the ingest pass.** Once the raw notes exist, propose running the AGENTS.md ingest workflow next — distilling the new findings into the relevant idea overview and deep-dive sections, merging with existing synthesis instead of appending duplicates, regenerating `wiki/index.md`, and appending to `wiki/log.md`. Offer to do it directly. Don't leave new evidence as raw-only.

Apply the AGENTS.md principles: don't fabricate facts — every claim in the raw note must cite a real source with a real URL, never an invented one; if a search returns nothing useful, say so explicitly rather than padding the raw note with adjacent content; lead with what would flip the verdict; be direct about confidence — `[uncertain]` is a feature, not a failure.
