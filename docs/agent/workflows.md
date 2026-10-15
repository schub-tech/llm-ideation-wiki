# Agent Workflows

Step sequences for setup, ingest, answering, lint, and sync. Commands: see [notion-contract.md](./notion-contract.md). Output and maintenance rules: [AGENTS.md](../../AGENTS.md).

## Fresh setup

Three separate skills, in order:

1. `/onboarding` — connect the Notion root; seed empty `Raw`, `Wiki`, `Templates`.
2. `/founder-profile` — create `wiki/founder`. Recommended before the first idea, not required.
3. `/new-idea` — create one idea workspace and initial overview. Without a founder profile, it asks for the founder's target and records it in the overview's Team section.

Don't create ideas during onboarding.

## Ingest a raw source

Read first: the relevant Notion `wiki/<idea-slug>/overview` and related raw pages.

1. **Analyze** before editing: material claims, entities, decisions, contradictions, affected pages, provenance state, open questions.
2. **Write**: distill into the relevant `…/overview` and supporting child pages. Merge with existing synthesis; don't append duplicate summaries or create per-source summary pages.

Then run the ritual (`AGENTS.md` § Mechanics).

## Answer a question

- Read the relevant `…/overview` and raw sources. Use `pull-cache` when broad search beats targeted reads.
- Name a shaky premise before answering. Cite pages and sources relied on. Surface contradictions; don't smooth them. Say so if the wiki doesn't answer it.
- If the answer is durable, update the existing wiki page and run the ritual.

## Lint

Deterministic checks:

```bash
python3 -m json.tool notion.config.json >/dev/null
python3 -m py_compile scripts/notion_wiki.py
scripts/check_agent_symlinks.py
scripts/check_state.py
scripts/notion_wiki.py pull-cache
```

Semantic lint via `/wiki-lint`: unsupported claims, unmarked synthesis, ambiguity drift, user-only premises, stale claims, risk/verdict mismatch, answered validations. Fix the wiki directly unless findings warrant a local lint note.

## Long runs

A long run is any job that spans many tool calls or sessions: a `/goal` run, a batch of research, a sourcing sweep.

1. Create `runs/<YYYY-MM-DD>-<slug>/` with three files:
   - `brief.md` — copied from [goal-brief](../../templates/goal-brief.md): objective, scope, and stop rule.
   - `progress.json` — machine-readable counters, rewritten after every batch.
   - `receipt.md` — written when the run stops: what was produced, where it lives, why it stopped.
2. Every brief names one stop rule with three parts. The run stops at whichever comes first:
   - **Target** — a ceiling, not a quota. Reaching it ends the run; falling short is fine.
   - **Budget** — the most time, calls, or money the run may spend.
   - **Quality floor** — the bar each item must clear. When new items stop clearing it, stop.
3. `hot.md` gets one pointer line per active run: its folder, status, and next step. Detail stays in the run folder.
4. When the run stops, write `receipt.md`, update the durable wiki pages, and replace the `hot.md` pointer with the outcome.

## Sync from outside the vault

Treat like ingest, but import only what's worth remembering. Skip raw implementation detail unless it's the actual lesson.
