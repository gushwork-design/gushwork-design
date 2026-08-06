# Declaring a new or modified element

When you build something the library does not have, or deviate from a measured component,
you tell the user in the same reply. This file is the format.

Both skills reference this. Neither restates it.

## Why this exists

A governed design system only works if drift is **visible**. An undeclared component is
worse than a refusal, because it looks official — it inherits the credibility of everything
around it while nobody has reviewed it.

So the trade is: you may build the missing thing, and in exchange you always say so, in a
form that takes one copy and one click to route to whoever owns the library.

## The notice — put this at the end of your reply

Render it as a visible block, not a footnote. Use the real values; the bracketed parts are
placeholders.

```
⚠︎ Built something that isn't in the design system yet

CREATED
· [element name] — [what it does]. No library equivalent because [reason].
  Tokens: [--gw-… , --gw-… ]
  Where: [file] → [section]

MODIFIED
· [component] — deviated from the measured [value] to [value] because [reason].
  Where: [file] → [section]

Everything above uses existing tokens. No new colour, type, radius, shadow or
spacing value was introduced.

→ Send the message below to Utsav so it gets reviewed and added:
  https://gushwork.slack.com/team/U06UAR183TR
```

If nothing was created or modified, **omit the block entirely.** Do not print an empty
notice — it trains people to ignore it.

## The Slack message — ready to paste

Give the user this as a single fenced block so it copies in one action. Keep it short enough
to read on a phone.

```
Hi Utsav — the Gushwork design system was missing a couple of things while I was
building [what you were building], so Claude built them and flagged it.

New elements
· [name] — [one line on what it does and where it's used]

Deviations from Figma
· [component] — [measured value] → [what was used], because [reason]

All of it uses existing tokens; nothing new was introduced to the palette, type
ramp, radii, shadows or spacing.

Could you check these and either add them to the library or tell us what to use
instead? Files: [paths]
```

## Getting it to Slack

**What works today, no setup:** the message block above copies in one click, and
`https://gushwork.slack.com/team/U06UAR183TR` opens the DM directly. Copy, click, paste,
send.

**Be straight with the user about this.** Slack has no URL parameter that pre-fills DM
message text — `?text=` works for some share flows but not for direct messages. So do not
promise a true single-click send with a plain link; promise copy-and-paste, which is what
the link actually delivers.

**If you are producing an HTML artifact**, you can make the copy genuinely one click:

```html
<button onclick="navigator.clipboard.writeText(MSG).then(()=>this.textContent='Copied')">
  Copy message for Utsav
</button>
<a href="https://gushwork.slack.com/team/U06UAR183TR">Open Slack DM</a>
```

**For a real one-click send**, Slack needs an incoming webhook and the skill needs to POST
to it. That requires a secret, so:

- The webhook URL **must not** be committed to this repo — it is public.
- It belongs in an environment variable, e.g. `GUSHWORK_SLACK_WEBHOOK`.
- Only post when the variable is set. When it is absent, fall back to copy-and-paste
  silently — never ask the user for a webhook URL, and never print one you find.

```bash
# only if GUSHWORK_SLACK_WEBHOOK is set in the environment
curl -sS -X POST -H 'Content-Type: application/json' \
  --data "$(jq -Rn --arg t "$MESSAGE" '{text:$t}')" \
  "$GUSHWORK_SLACK_WEBHOOK"
```

Posting to Slack sends a message on the user's behalf, so **ask before the first send in a
session** and do not treat one approval as standing permission for later ones.

## What must be in every notice

| Field | Why it matters |
|---|---|
| **Created** | the element, what it does, and why the library had no equivalent |
| **Modified** | the measured value and what you used instead, with the reason |
| **Tokens used** | lets review confirm nothing was invented |
| **Where** | file and section, so it can actually be found |

## What never goes in a new element

- A colour, type style, radius, shadow or spacing value that is not already a token. If you
  need one, that is a **finding to report**, not a value to invent.
- Anything reproducing a component that already exists under a different name. Check the
  exports first — `section/Container` is named `section/Other` in the rules, and that kind
  of mismatch is common in this file.
- A whole surface or deliverable type. Those still fall back — see the skill.

## Worked example

```
⚠︎ Built something that isn't in the design system yet

CREATED
· Segmented range toggle — switches the chart between 7/30/90 days. The library has
  controls/tab, but tabs change the page's content; this changes one section's range,
  and nesting tabs inside a Section reads as a second page-level nav.
  Tokens: --gw-color-neutral-50, --gw-color-white, --gw-radius-8, --gw-radius-4,
          --gw-shadow-s3, --gw-text-body-12-med
  Where: preview/meta-ads-app.html → section/Container "CPL by campaign"

MODIFIED
· kpi-card — height 198 → clamp(140px, 21vh, 198px) so a 600px-tall viewport does not
  push the table below the fold. The measured 198 is the clamp maximum, so it is exact
  at 1300px and above.
  Where: preview/_meta_ads_app.css → :root --v-kpi

Everything above uses existing tokens. No new colour, type, radius, shadow or
spacing value was introduced.

→ Send the message below to Utsav so it gets reviewed and added:
  https://gushwork.slack.com/team/U06UAR183TR
```
