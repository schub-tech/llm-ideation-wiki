# LLM Ideation Wiki

> Built by [**Schub**](https://www.schub.tech/).

Obsidian-friendly research wiki for business ideas, maintained by an LLM. Built on Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Quick Start

1. **Fork this repo** (recommended — gives you your own working copy to evolve) or clone it directly to try it out.
2. **Clone locally:** `git clone <your-fork-url>`
3. **Drop a starting point** into `raw/ideas/` as `YYYY-MM-DD-<idea-slug>.md` — a brainstorm, scratch note, or a few paragraphs explaining what you want to research.
4. **Open the repo with your AI agent** (Claude Code recommended — see note at the bottom). Ask it to scaffold an idea overview from your starting note using `templates/idea-page.md`. It will fill what your note supports and leave honest gaps everywhere else.
5. **Use the skills** (see [Skills](#skills) below) to grow the wiki:
   - `/research` to surface unvalidated gaps; `/research-deep` to fill them with web research that lands as new raw notes.
   - `/grill-me` to stress-test the idea section by section once the overview has substance.
6. **Add new material** (user interviews, external sources, articles) to `raw/notes/` as you collect it, and ask the LLM to ingest it.
7. **Ask questions** any time — the LLM reads `wiki/index.md` first and works down from there.

The wiki is meant to be living: each new piece of evidence either confirms a load-bearing claim, kills one, or sharpens the open questions. The `verdict` field on each idea (`exploring` → `pursuing` / `parked` / `killed`) tracks where it actually stands. Run `python3 scripts/rebuild_index.py` after meaningful wiki edits.

## Structure

- `raw/` — immutable source material (notes, brainstorms, attachments).
- `wiki/` — compiled markdown wiki the LLM maintains.
- `templates/` — scaffold for new idea pages.
- `skills/` — LLM skills you can invoke (see [Skills](#skills) below).
- `scripts/` — index and lint helpers.
- `AGENTS.md` — operating rules for the LLM.

## Skills

- `/grill-me` — interviews you about an idea one question at a time, walking through the overview's sections (Problem → Solution → Why this works → Market → Risks).
- `/research` — surfaces research gaps from an idea overview ("Still to validate" lines, "What we do not know," "Next moves") and proposes a plan tagged by strategy: ask the user, web research, or hybrid.
- `/research-deep` — runs targeted web research on specific questions and writes findings to `raw/notes/` for ingest.

## Scripts

- `rebuild_index.py` — regenerates `wiki/index.md` from page frontmatter.
- `find_orphans.py` — lists wiki pages with no inbound links.
- `check_wikilinks.py` — lists broken markdown links.

## Setup

- **Markdown viewer:** [Obsidian](https://obsidian.md/) is recommended as a lightweight viewer for browsing the wiki and following wikilinks.
- **LLM tool:** any agent that can read and edit local files works, but the Claude family is recommended for its conversational style.

---

Made with ♥ in Munich by [**Schub**](https://www.schub.tech/). Forks, issues, and pull requests welcome.
