---
name: wiki-lint
description: Run semantic wiki lint beyond structural link checks. Use when the user asks to audit, lint, health-check, find stale claims, find unsupported claims, check provenance, or identify contradictions in the wiki.
---

Run a semantic lint pass over the business-idea wiki. This complements the Notion helper checks in `docs/agent/workflows.md`; it does not replace them.

**Start with deterministic checks.**

1. Run the deterministic Notion helper checks from `docs/agent/workflows.md`.
2. Read `hot.md`, `wiki/index.md`, and the relevant Notion idea page before reading deep-dive pages.

**Semantic checks.** For each idea, inspect the overview and its related deep-dive notes for:

- **Unsupported material claims.** Any statistic, price, legal statement, named competitor claim, market-size claim, or dated event must have a raw-source line citation.
- **Unmarked synthesis.** Claims that are inferred from multiple sources, not directly stated by one source, should carry `^[inferred]`.
- **Ambiguity drift.** Contested or weak claims should carry `^[ambiguous]` and should not be written as settled.
- **User-only premises.** Founder assertions, anecdotes, and "everyone says yes" style evidence should carry `^[user-claim]` unless independently validated.
- **Risk/verdict mismatch.** If a risk could kill the idea, the verdict and Next moves must reflect it.
- **Answered validations.** If a `Still to validate` item is already answered in a deep-dive or raw note, update or remove it.
- **Stale claims.** Pages older than 90 days should be checked for date-sensitive claims before being treated as current.
- **Mapping mismatch.** Notion pages that should be script-addressable should either be added to `notion.config.json` or explicitly left as manually navigated child pages.

**Report format.** Lead with the highest-severity findings:

```markdown
## Semantic Lint

### P1
- [Page](path) — claim/risk. Why it matters. Suggested fix.

### P2
- ...

### Maintenance
- Mapping/index/log/hot-cache updates needed.
```

Use priorities this way:

- **P1:** Could change the verdict or invalidate a next move.
- **P2:** Material but not immediately verdict-changing.
- **P3:** Hygiene, clarity, or future retrieval quality.

If the user asked you to fix issues, edit the Notion wiki directly, then update local `wiki/index.md` when navigation changes, update `hot.md`, append one short entry to `wiki/log.md`, and run the Notion helper checks.
