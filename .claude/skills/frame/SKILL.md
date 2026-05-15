---
name: frame
description: Capture the founder's ambition, end-game, financial target, timeframe, investment willingness, and risk tolerance, then reality-check the answers against themselves. Writes to `wiki/founder` in Notion. Use at wiki start, or when the user asks to frame goals, set ambition, capture the founder profile, or reality-check what's possible.
---

Capture the founder profile that every later idea will be measured against. One Notion page, six questions, then a tension check.

**Read first.**

1. `hot.md`, `wiki/index.md`, `notion.config.json`.
2. If `wiki/founder` already exists in `notion.config.json`, fetch it with `scripts/notion_wiki.py get wiki/founder` and offer to update rather than overwrite.

**Ask one question at a time.** Wait for the answer before moving on — multi-question dumps let the user dodge the hard one. Reflect each answer back in one short line before asking the next, so the user can correct drift early.

Ask these six, in order:

1. **Team shape** — solo founder, small team (≤10), or large organization?
2. **End game** — fast exit (growth play), IPO (valuation play), or hold-and-run (profit/lifestyle play)?
3. **Financial success** — what's the number? Net to the founder, total enterprise value, or annual income — be specific about which.
4. **Timeframe** — by when does (3) need to be true?
5. **Investment willingness** — how much of your own time (hours/week, years) and your own money (€/$ ceiling) are you willing to commit before the idea has to pay for itself?
6. **Risk tolerance** — what probability of going to zero are you comfortable with? Frame as a number, not "I'm okay with risk."

If the user gives a vague answer (e.g. "a lot", "comfortable", "soon"), ask one clarifying follow-up to pin a number or category. Do not move on without one.

**Reality check — tensions in the answers only.**

After all six are captured, scan the answers against each other and surface any tensions in 3–6 bullets. Examples of the kind of tension worth flagging:

- Solo founder + IPO end game + short timeframe.
- High financial target + low capital willingness + low risk tolerance.
- Lifestyle/profit end game + fast-exit-sized number.
- Timeframe shorter than typical category cycle (e.g. 2 years to a regulated-market IPO).

Do not bring in market or idea-specific facts — this is a self-consistency check on the stated answers. If there are no tensions, say so in one line and move on. No manufactured objections, no padding.

If the user wants to revise an answer in light of the tensions, update before writing.

**Write to Notion.**

1. Create the page if missing:
   `scripts/notion_wiki.py create wiki/founder --parent wiki/ --title "Founder" --emoji 🎯 --file <markdown-file>`
2. If it already exists, update it:
   `scripts/notion_wiki.py update wiki/founder <markdown-file>`

Page body, in this order:

- One-line lede: who the founder is and what shape company they want.
- **Ambition** table or bullets: team shape, end game, financial target (with which metric), timeframe.
- **Willing to invest**: time and money ceilings.
- **Risk tolerance**: stated probability-of-zero comfort.
- **Tensions** (only if any were surfaced): one bullet per tension, plain and direct.
- **Last updated**: today's date.

Mark every stated answer as `^[user-claim]`. Mark tensions as `^[inferred]`. Do not invent numbers the user did not give — if they refused to pin one, write "not pinned" rather than guessing.

**Finish.**

1. `scripts/notion_wiki.py pull-cache`
2. `scripts/notion_wiki.py hash`
3. Update local `hot.md` with one line noting the founder profile is set.
4. Append one short entry to local `wiki/log.md`.
5. Tell the user the page is at `wiki/founder` in Notion and that future idea overviews will be checked against it as they take shape.

**Rules.**

- One page only: `wiki/founder`. Never per-idea.
- Current state, not history — overwrite on update; revision lives in `wiki/log.md`.
- Do not check the profile against any specific idea here. Idea-vs-profile fit is the job of later skills (`grill-me`, `wiki-lint`, idea overview synthesis) once an idea has enough surface area to test.
