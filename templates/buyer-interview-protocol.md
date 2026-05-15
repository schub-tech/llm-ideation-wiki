# Buyer Interview Protocol Template

Scaffold for a Notion child page under `wiki/<idea-slug>/` — the operational checklist for running a buyer-discovery campaign on an idea.

Use this when an idea's `Next moves` calls for buyer interviews to validate problem framing or willingness to pay. The protocol covers: how many people to reach out to, where to find named champions, how to track outreach, what to ask, and what to check when conversion stalls.

## Scaffold

Create a Notion child page titled `Buyer Interview Protocol` under `wiki/<idea-slug>/`, give it an emoji icon, then paste the body below. Do not add a duplicate heading with the page title.

````markdown
Operational checklist for the relevant `Next moves` item.

## TODOs

- [ ] **Schedule [N] SME interviews by [date]** — via [hot-lead source].
- [ ] **Schedule [N] enterprise interviews by [date]** — via the tracker below.

## Volume math

Realistic LinkedIn cold-outreach conversion for student/research framing to senior buyers:

| Stage | Range |
|---|---|
| Connect accepted | 30-50% |
| Reply to follow-up | 30-50% of accepts |
| Books a 30-min call | 30-60% of repliers |
| **End-to-end** | **~5-15%** |

Working backward at 10%: **need ~10x the target interview count in connect-sends**. Add 30-50% buffer for stalls and passed rows.

## Source-mining recipe

Find named champions in roughly this order; yield drops sharply after the first three:

1. **Vendor case-study library.** Each case study often quotes 1-3 buyer-side champions by name and exact title.
2. **Industry awards announcements.** Cross-reference with case studies; the awarded project's owner may differ from the case-study quote.
3. **Conference speaker lists.** Filter to end-user enterprises; skip consulting partners, implementation partners, and vendor staff.
4. **LinkedIn skill-filter search.** Search inside LinkedIn by current company plus relevant skill or tool.
5. **Vendor community programs.** These skew toward partners/consultants, so use them for partner interviews more than buyer interviews.

For each named champion, note the **exact public hook**: quote, talk, award, or project. Generic outreach reads as scraped.

## Outreach tracker

Stage: `none` -> `sent` -> `connected` -> `replied` -> `scheduled` -> `done` / `passed`.

| Name | Role | Company | Lang | Stage | Notes |
|---|---|---|---|---|---|
| [Example Name](https://linkedin.com/in/...) | [Exact title] | [Company] | DE/EN | none | [hook reference] |

**Connect-request template (EN)** — replace `[hook]` per person; do not send without it.

```text
Hi [Name], [hook]. I'm a master's student at [University] researching [topic] for my thesis. Would love to connect and later hear about your experience with [tool/practice] in practice if you're open to it.
```

**Connect-request template (DE)** — replace `[hook]` per person; do not send without it.

```text
Hallo [Name], [Anker]. Ich schreibe an der [Universitaet] meine Masterarbeit ueber [Thema]. Wuerde mich gerne vernetzen und spaeter von Ihren Erfahrungen mit [Tool/Praxis] in der Praxis hoeren, falls Sie offen dafuer sind.
```

**After-accept ask** — send only after they accept the connection. Do not bundle it into the connect note.

## Interview

Ask in this order. Keep questions specific to this idea's hypothesis.

1. **Open question:** "[The single most-load-bearing question for the idea.]"
2. **Last incident:** when did [the relevant failure mode] last happen, what did it cost, who fixed it?
3. **Rank the pains:** let them rank the candidate pains; listen for pains you did not anticipate.
4. **Urgency score for the top pain:**
   - 1 = nice-to-have
   - 3 = budgeted this year
   - 5 = active deadline or actively shopping

If interviewing a buyer-side manager, end with: "Could you connect me with one or two of the people actually doing/building [the work]? I'd like to compare the operator perspective on the same questions."

## Capture per call

```text
### Call N — Name, Company
- Date:
- Segment: SME / enterprise
- [Idea-specific quantitative anchor]:
- Last incident:
- Pain ranking:
  1.
  2.
  3.
  4.
- Urgency for #1 (1-5):
- [Idea-specific yes/no]:
- CTA: intro / follow-up / none
- Notes / verbatim quotes:
```

## Calls

[Per-call notes accumulate here.]

## Decision

- **Hell yeah:** >=50% rank the same pain #1.
- **Hell no:** <20% can name a real recent incident, or >=50% are migrating off / actively replacing.

## Diagnostic playbook

If the funnel sits at 0% accepts after a meaningful sample, diagnose before sending more.

1. **Hook-audience mismatch.** Re-segment by actual public hook.
2. **Typos and placeholders.** Re-read the literal text you sent.
3. **No per-person specific hook.** Add a reference to a quote, project, or talk topic.
4. **Profile credibility.** Make the research topic and university affiliation visible.
5. **Channel/time.** Send with a note, preferably Tue-Thu during working hours.
6. **Throttling.** Do not batch aggressively enough to trigger platform filtering.

## Related

- [Main idea page]
````
