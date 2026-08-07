# Gushwork Design System

Claude builds Gushwork screens using the real components and tokens, instead of guessing at
them. Three steps to start.

---

## 1. Install

```bash
claude plugin marketplace add utsav-gushwork/gushwork-design && claude plugin install gushwork-design@gushwork
```

*Skip this if your repo has a `.claude/settings.json` mentioning `gushwork` — it installs itself.*

## 2. Restart Claude Code

It won't load the skills otherwise. This is the one step people skip and then think the install
failed.

## 3. Ask for what you want

> "Build a dashboard for the sales team to see show-ups over the week"

You never name the skills — they fire on the work. **The reply opens with "Using the Gushwork
dashboard skill."** If that line is missing, it didn't fire.

It'll ask two or three questions first — what the KPIs are, what matters most, whether you're
monitoring or acting. That's on purpose: a dashboard is a set of decisions about what matters,
and guessing produces a screen that looks right and answers nothing.

**That's it.** Everything below is for when something looks off.

---

## Before you ship it, eyeball four things

| Look for | Why |
|---|---|
| **A blue filled button on a dashboard** | means the wrong component got picked — web and dashboard have separate button sets, both named `Button`. The most common way output goes off-system. |
| **A raw hex code** | every value comes from `foundation/tokens.css`. A hardcoded colour is a bug. |
| **A `Sample data` badge** | the numbers are illustrative. Don't put it in a deck until it's real. |
| **A four-line Slack block** | Claude had to build something the library lacks. **Paste it to Utsav** — see below. |

## If it built something new

The library has gaps. When a screen needs something missing — a date-range picker, an empty
state — Claude builds it and hands you a four-line block for Slack, linking a full record.

**Please send it.** That's the whole governance loop. Utsav replies **Add** (draw it in Figma),
**Replace** (something already covers this), **Promote** (the deviation was right — the component
is what's wrong), or **Revert**. A decision that stays in Slack gets re-made next month by
someone else.

## If something isn't working

| Symptom | Fix |
|---|---|
| No "Using the Gushwork … skill" line | restart; or say "use the Gushwork dashboard skill" explicitly |
| `claude plugin list` doesn't show it | re-run step 1 — a declined plugin won't re-prompt |
| `marketplace add` fails | ping Utsav; your org may restrict marketplaces |
| Output looks generic | you're in a scratch folder, not the product repo |
| Values differ from Figma | you're on a stale version — see below |

**Stale versions fail silently**, emitting last month's values confidently:

```bash
claude plugin marketplace update gushwork && claude plugin update gushwork-design
```

Restart after. Ask Utsav to turn on `autoUpdate` so you never think about it again.

## Where to look things up

| Question | File |
|---|---|
| What's the hex / size / type style? | `foundation/tokens.css` |
| Which component do I use here? | `skills/gushwork-dashboard/SKILL.md`, `skills/gushwork-web/SKILL.md` |
| What exactly does it measure? | `exports/dashboard/`, `exports/web/` |
| Why does the shell scroll like that? | `exports/dashboard/build-rules.md` |
| Voice, casing, CTA copy | `foundation/voice.md` |
| React or static HTML? | `foundation/output-targets.md` |

## Two things about the current state

**The dashboard surface is solid** — measured off Figma and driven through a real nine-page
build, so the defects are already found.

**The web surface is thinner** — Button, eyebrow, navbar, footer and `client/avatar` are
measured; roughly 22 components are still transcribed from annotations rather than verified
against what renders. Treat web output as a good first draft, not a spec.

**You don't need Figma.** Everything measured is in `exports/`. Figma is only for maintainers
changing the system — and reading a component *instance* misreports type weight, which shipped a
wrong nav rail twice before anyone worked out why.

## Who to ask

Utsav — https://gushwork.slack.com/team/U06UAR183TR

Anything the system genuinely doesn't cover — slides, flyers, a standalone tool — Claude will say
so and point you there rather than inventing something plausible. That's working as intended.
