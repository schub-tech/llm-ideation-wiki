# LLM Ideation Wiki

> Built by [**Schub**](https://www.schub.tech/).

A workspace for taking business ideas from half-formed hunch to a defended verdict. You feed it brainstorms, interviews, and research; an LLM builds a structured case for each idea, surfaces what still needs validating, and stress-tests the thesis as new evidence comes in.

## Quick Start

1. **Fork this repo** (recommended — gives you your own working copy to evolve) or clone it directly to try it out.
2. **Clone locally:** `git clone <your-fork-url>`
3. **Add a starting point** under Notion `raw/<idea-slug>/` — a brainstorm, scratch note, or a few paragraphs explaining what you want to research.
4. **Open the repo with your AI agent.** Ask it to scaffold a Notion `wiki/<idea-slug>/` page from your starting note using `templates/idea-page.md`. It will fill what your note supports and leave honest gaps everywhere else.
5. **Use the skills** (see [Skills](#skills) below) to grow the wiki:
   - `/research` to surface unvalidated gaps; `/research-deep` to fill them with web research that lands as new raw notes.
   - `/grill-me` to stress-test the idea section by section once the overview has substance.
6. **Add new material** (user interviews, external sources, articles) to the relevant `raw/<idea-slug>/` page, or to `raw/shared/` if it applies across ideas, and ask the LLM to ingest it.
7. **Ask questions** any time — the LLM reads `wiki/index.md` first and works down from there.

The wiki is meant to be living: each new piece of evidence either confirms a load-bearing claim, kills one, or sharpens the open questions. The `verdict` field on each idea is binary — `active` or `killed`. An idea is alive until disconfirming evidence kills it; a killed idea can be flipped back to active if new evidence changes the picture.

## Structure

- Notion `raw/` — immutable source material (notes, brainstorms, attachments).
- Notion `wiki/` — user-facing compiled wiki the LLM maintains.
- `hot.md` — short recent-state cache for fast session startup.
- `wiki/index.md` — local navigation for idea pages.
- `wiki/log.md` — local append-only change log.
- `notion.config.json` — Notion root and logical path mapping.
- `templates/` — scaffolds for new idea pages and supporting process notes.
- `docs/agent/` — progressively disclosed schema, provenance, and workflow guidance for agents.
- `.agents/skills/` and `.claude/skills/` — LLM skills you can invoke (see [Skills](#skills) below).
- `scripts/` — index and lint helpers.
- `AGENTS.md` — lean always-loaded operating rules; deeper instructions live in `docs/agent/` and skills.

## Notion Content Store

Notion is the canonical content store for user-facing `wiki/<idea-slug>/` pages and `raw/<idea-slug>/` source material. Local Markdown files such as `hot.md`, `wiki/index.md`, `wiki/log.md`, `templates/`, and `docs/` are the agent harness; durable content reads and writes go through the Notion CLI.

```bash
ntn doctor
scripts/notion_wiki.py ls
scripts/notion_wiki.py get wiki/
scripts/notion_wiki.py pull-cache
scripts/notion_wiki.py hash
```

- `notion.config.json` stores the root page and path-to-page mapping.
- `scripts/notion_wiki.py seed` creates missing standard content pages without overwriting existing Notion content.
- `scripts/notion_wiki.py seed --refresh-existing` is reserved for future content templates; it does not overwrite existing pages today.
- `docs/agent/notion-contract.md` and the `notion-wiki` skill define the agent workflow.

## Skills

- `/grill-me` — interviews you about an idea one question at a time, walking through the overview's sections (Problem → Solution → Why this works → Market → Risks).
- `/research` — surfaces research gaps from an idea overview ("Still to validate" lines, "What we do not know," "Next moves") and proposes a plan tagged by strategy: ask the user, web research, or hybrid.
- `/research-deep` — runs targeted web research on specific questions and writes findings to the relevant raw source area for ingest.
- `/wiki-lint` — semantic lint workflow for unsupported claims, unmarked synthesis, stale validations, provenance drift, and risk/verdict mismatch.

Skills live in `.agents/skills/` and `.claude/skills/`. Claude Code picks up `.claude/skills/`; other agents can read the matching `SKILL.md` files from `.agents/skills/`.

## Scripts

- `notion_wiki.py get <path>` — print Markdown for a mapped Notion content page.
- `notion_wiki.py update <path> <file>` — replace a mapped Notion content page from Markdown.
- `notion_wiki.py seed` — ensure standard Notion content containers exist and have expected titles/icons.
- `notion_wiki.py pull-cache` — refresh generated Markdown cache under `.cache/notion/`.
- `notion_wiki.py hash` — calculate Notion content hashes for mapped pages.

## Notes

- **Viewer:** Notion is the user-facing content browser; generated local cache is only for agent search and verification.
- **LLM tool:** use an agent that can run the Notion CLI and edit the local harness files.
- Highly inspired by Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

---

Made with ♥ in Munich by [**Schub**](https://www.schub.tech/). Forks, issues, and pull requests welcome.
