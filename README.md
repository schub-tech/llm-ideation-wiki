# LLM Ideation Wiki

Obsidian-friendly research wiki for business ideas, maintained by an LLM. Built on Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Structure

- `raw/` — immutable source material (notes, brainstorms, attachments).
- `wiki/` — compiled markdown wiki the LLM maintains.
- `templates/` — scaffold for new idea pages.
- `skills/` — LLM skills you can invoke (see [Skills](#skills) below).
- `scripts/` — index and lint helpers.
- `AGENTS.md` — operating rules for the LLM.

## Use

Open the repo root as an Obsidian vault. Drop new sources into `raw/`, ask the LLM to ingest them into `wiki/`, ask the LLM questions starting from `wiki/index.md`. Run `python3 scripts/rebuild_index.py` after meaningful wiki edits.

## Skills

- `/grill-me` — interviews you about an idea one question at a time, walking through the overview's sections (Problem → Solution → Why this works → Market → Risks).
- `/research` — surfaces research gaps from an idea overview ("Still to validate" lines, "What we do not know," "Next moves") and proposes a plan tagged by strategy: ask the user, web research, or hybrid.
- `/research-deep` — runs targeted web research on specific questions and writes findings to `raw/notes/` for ingest.

## Scripts

- `rebuild_index.py` — regenerates `wiki/index.md` from page frontmatter.
- `find_orphans.py` — lists wiki pages with no inbound links.
- `check_wikilinks.py` — lists broken markdown links.

---

> Note: Claude Code is the recommended LLM tool for working with this repo.
