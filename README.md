# LLM Ideation Wiki

> Built by [**Schub**](https://www.schub.tech/).

A Notion-based workspace for turning rough business ideas into structured, evidence-bound decisions. You bring ideas, notes, interviews, and research; your AI agent keeps the wiki organized and pushes each idea toward a clear verdict.

## Get Started

1. **Fork this repo** to make your own copy, or clone it directly if you just want to try it.
2. **Clone it to your computer:**

```bash
git clone <your-repo-url>
cd llm-ideation-wiki
```

3. **Create or choose a Notion page** that should become the root of your wiki.
4. **Open this folder with your AI agent.**
5. **Ask the agent:**

> Use the onboarding skill to set up this wiki.

The agent will ask you for one thing:

- the Notion page link that should be the root

During setup, it will also check whether the Notion CLI is installed and whether you are logged in. If needed, it can install the CLI, run `ntn login`, and open the browser for you to approve access.

After that, it will create the empty Notion structure.

Then continue with:

```text
Use the founder-profile skill.
```

This captures your ambition, risk tolerance, and investment limits. After that, start your first idea:

```text
Use the new-idea skill.
```

## How It Works

- `Raw` in Notion holds inputs: founder notes, interviews, articles, data, and other source material.
- `Wiki` in Notion holds the current synthesis for each idea.
- `Templates` in Notion gives you copyable starting points.
- This repo holds the harness: agent instructions, skills, scripts, templates, and local state.

Notion is the place to read and edit user-facing content. Local Markdown files are for the agent.

## Skills

- `/onboarding` — connects a Notion root page and creates the empty structure.
- `/founder-profile` — captures the founder ambition and constraints every idea should be judged against.
- `/new-idea` — creates a raw note, idea workspace, and overview for one idea.
- `/research` — finds the most important open questions for an idea.
- `/research-deep` — researches a specific question and writes the result as raw material.
- `/grill-me` — interviews you to stress-test an idea.
- `/wiki-lint` — checks for weak claims, missing evidence, stale assumptions, and unclear verdicts.

Skills live in `.agents/skills/` and `.claude/skills/`.

## Useful Agent Commands

These are mainly for the agent, but they are helpful to know:

```bash
ntn doctor
ntn login
scripts/notion_wiki.py seed --refresh-existing
scripts/notion_wiki.py ls
scripts/notion_wiki.py pull-cache
scripts/notion_wiki.py hash
```

Highly inspired by Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

---

Made with ♥ in Munich by [**Schub**](https://www.schub.tech/). Forks, issues, and pull requests welcome.
