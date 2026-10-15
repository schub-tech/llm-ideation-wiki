# Goal Brief

Copy this into `runs/<YYYY-MM-DD>-<slug>/brief.md` before a long run starts. Fill every field; write `unknown` rather than leave a placeholder. Rules: [workflows](../docs/agent/workflows.md) § Long runs.

````markdown
# <Run title>

**Objective:** One sentence: what the run produces and for which decision.

**Scope:** What is in. What is out. Which sources, pages, or databases the run may touch.

## Stop rule

The run stops at whichever comes first.

- **Target (ceiling):** <N items>. Reaching it ends the run. Falling short is fine.
- **Budget:** <hours, sessions, tool calls, or money>.
- **Quality floor:** <the bar every item must clear>. When new items stop clearing it, stop.

## Output

- **Where results go:** <Notion page or database, by mapped path or link>.
- **What one finished item looks like:** <fields, evidence, format>.

## Progress file

`progress.json` sits next to this brief. Rewrite it after every batch:

```json
{
  "status": "running",
  "target": 0,
  "done": 0,
  "rejected": 0,
  "budget": "",
  "spent": "",
  "last_batch": "",
  "next_step": "",
  "stop_reason": ""
}
```

`status` is `running` or `stopped`. On stop, set `stop_reason` to `target`, `budget`, `quality floor`, or a one-line explanation.

## Receipt

When the run stops, write `receipt.md` next to this brief:

- Stop reason and final counts against target and budget.
- Links to every page or row the run created or changed.
- What failed the quality floor, and why.
- Open questions and the next step, if any.
````
