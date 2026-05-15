---
name: onboarding
description: Set up a new Notion-backed LLM Ideation Wiki from a fresh clone. Use when the user asks to get started, onboard, initialize the wiki, or connect a Notion root page.
---

Set up the repo as a Notion-backed idea wiki. Do infrastructure only; do not create ideas.

**Ask first.**

If the user has not already provided it, ask for the Notion page URL to use as the wiki root.

Do not proceed until you have the root page URL.

**Set up Notion.**

1. Read `README.md`, `AGENTS.md`, `docs/agent/notion-contract.md`, and `notion.config.json` if it exists.
2. Check whether `ntn` exists with `command -v ntn` or `ntn --version`.
3. If `ntn` is missing, tell the user the Notion CLI is required. Ask before installing external software, then install with the official command `curl -fsSL https://ntn.dev | bash` when approved.
4. Run `ntn doctor`.
5. If the CLI is not authenticated, run `ntn login`. This should open the user's browser; ask the user to complete the browser approval and confirm the verification code.
6. If the environment is headless and `ntn login` prints a URL and poll command, show the URL/code to the user, then run the printed poll command after they approve in the browser.
7. Re-run `ntn doctor` after login.
8. Extract the page ID from the Notion URL and store it as the compact ID in `notion.config.json`.
9. For a new wiki root, reset `pages` in `notion.config.json` before seeding so old page IDs are not reused.
10. Set `mode` to `notion-cli`, keep `version: 1`, and store `root_url`, `root_page_id`, `root_title`, and `root_emoji`.
11. Run `scripts/notion_wiki.py seed --refresh-existing` to create `Raw`, `Shared`, `Wiki`, and `Templates`.

**Finish.**

1. Run `scripts/notion_wiki.py pull-cache`.
2. Run `scripts/notion_wiki.py hash`.
3. Run `scripts/notion_wiki.py ls`.
4. Update local `wiki/index.md` only if navigation changed.
5. Update local `hot.md`.
6. Append one short entry to local `wiki/log.md`.
7. Tell the user setup is complete and the next step is `/founder-profile`. After that, use `/new-idea` to create the first idea.

**Rules.**

- Notion is canonical for `raw/` source material and user-facing `wiki/` content.
- The repo is the harness: `README.md`, `AGENTS.md`, `hot.md`, `wiki/index.md`, `wiki/log.md`, `docs/`, `templates/`, scripts, and skills.
- Do not put harness files into Notion.
- Do not create idea pages during onboarding.
- If the root page title or icon cannot be read, default to `LLM Wiki` and `🧠`.
- The agent can start browser login, but the user must approve Notion access themselves.
