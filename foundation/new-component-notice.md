# Declaring a new or modified element

When you build something the library does not have, or deviate from a measured component,
you say so in the same reply — as **one message block the user copies straight into Slack.**

Both skills reference this. Neither restates it.

## Why this exists

A governed design system only works if drift is **visible**. An undeclared component is
worse than a refusal — it inherits the credibility of everything around it while nobody has
reviewed it.

So the trade is: you may build the missing thing, and in exchange you always declare it, in
a form short enough that someone actually reads it and sends it on.

## One block. Not two.

Do not write a summary for the user and a separate message for Slack. **The message to Utsav
is the only artefact.** The user's job is copy, click, paste, send — four actions, no editing,
no deciding what to include.

Everything long goes in a file and gets linked.

| | Where | Length |
|---|---|---|
| **The detail** | `notices/YYYY-MM-DD-<slug>.md`, committed | as long as it needs to be |
| **The message** | one fenced block in your reply | **four lines** |

## 1. Write the detail file

`notices/YYYY-MM-DD-<slug>.md` — one per piece of work, not one per element.

```markdown
# <what you were building> — new elements and deviations

Built <date>. Files: <paths>

## Created
### <element name>
What it does, why the library had no equivalent, tokens used, where it lives.

## Modified
### <component> — <measured value> → <what you used>
Why, and whether the measured value is still reachable (e.g. it is the clamp maximum).

## Worth a decision
The one or two items that are genuine judgement calls rather than obvious adaptations.

## Tokens
Every token used. Confirm no new colour, type, radius, shadow or spacing value was
introduced. List any value in use that has no token — that is a gap to report, not an
invention.
```

The **"Worth a decision"** section is the point. Most entries are routine adaptations; one or
two are you overriding a measured value because it produced a bad result. Saying which is
which turns a list into a review.

Commit and push the file **before** you give the message — the link must resolve. An
uncommitted path is a dead link.

## 2. Give exactly this, and nothing more

One short lead-in line, one fenced block, one link:

> Built 1 new element and 8 deviations — copy this to Utsav:
>
> ```
> Hi Utsav — built 1 new element + 8 deviations while making the Meta Ads dashboard.
> All token-safe, nothing new added to the palette or type ramp.
> Detail: https://github.com/utsav-gushwork/gushwork-design/blob/main/notices/2026-08-06-meta-ads.md
> Worth your eye: the card-layout KPI cap — I overrode a measured split.
> ```
>
> → https://gushwork.slack.com/team/U06UAR183TR

The four lines are always the same shape:

1. **What** — counts, and what you were building
2. **Token safety** — one clause, so the reviewer knows the palette is intact
3. **The link**
4. **The one thing worth their attention** — never a list

If nothing was created or modified, **say nothing.** Never print an empty notice; it trains
people to ignore the real ones.

## Getting it to Slack

**Works today, no setup:** the block copies in one action and
`https://gushwork.slack.com/team/U06UAR183TR` opens the DM.

**Be straight about the limit.** Slack has no URL parameter that pre-fills DM text —
`?text=` works for some share flows but not direct messages. Do not promise single-click
send with a plain link; promise copy-and-paste, which is what it delivers.

**In an HTML artifact**, make the copy genuinely one click:

```html
<button onclick="navigator.clipboard.writeText(MSG).then(()=>this.textContent='Copied ✓')">
  Copy message
</button>
<a href="https://gushwork.slack.com/team/U06UAR183TR">Open Slack DM</a>
```

**For a real one-click send**, Slack needs an incoming webhook:

- The URL **must not** be committed — this repo is public. Use `GUSHWORK_SLACK_WEBHOOK`.
- Only post when the variable is set; otherwise fall back to copy-and-paste silently. Never
  ask the user for a webhook URL.
- Posting sends a message on the user's behalf — **ask before the first send in a session**,
  and don't treat one approval as standing permission.

```bash
# only if GUSHWORK_SLACK_WEBHOOK is set
curl -sS -X POST -H 'Content-Type: application/json' \
  --data "$(jq -Rn --arg t "$MESSAGE" '{text:$t}')" "$GUSHWORK_SLACK_WEBHOOK"
```

## What never goes in a new element

- A colour, type style, radius, shadow or spacing value that is not already a token. Needing
  one is a **finding to report**, not a value to invent.
- A component that already exists under a different name. Check the exports first —
  `section/Container` is called `section/Other` in the rules, and that kind of mismatch is
  common in this file.
- A whole surface or deliverable type. Those still fall back — see the skill.
