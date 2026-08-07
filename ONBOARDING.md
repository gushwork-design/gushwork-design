# Gushwork Design System — start here

This makes Claude produce on-brand Gushwork screens by default: the right component for the
right surface, real tokens instead of guessed hexes, and a visible flag rather than a quietly
invented component.

Five minutes of reading saves you a rebuild.

## Install

Two commands. Add the marketplace once, then install from it — `claude plugin install` takes a
plugin **name**, not a git URL:

```bash
claude plugin marketplace add utsav-gushwork/gushwork-design
```

```bash
claude plugin install gushwork-design@gushwork
```

Two skills register. **You never name them** — they fire on the work.

If your repo already has a `.claude/settings.json` naming this plugin, skip both commands — it
installs itself in the background when you open the repo.

### Staying current

A stale plugin fails silently: it keeps emitting last month's values with full confidence. To
update:

```bash
claude plugin marketplace update gushwork && claude plugin update gushwork-design
```

Then **restart Claude Code** — it won't apply otherwise. Check what you're on with
`claude plugin list`. Ask whoever set this up to turn on `autoUpdate` so you never have to
think about it.

| You ask for | You get |
|---|---|
| "build a dashboard for showups this week" | `gushwork-dashboard` — dense, gray canvas, black actions |
| "a pricing page for Gushwork" | `gushwork-web` — spacious, white and blue |

## Two things to expect, so they don't feel like friction

**1. It asks you questions before it builds.** For a dashboard: what the KPIs are, what should
be seen first, whether you're monitoring / diagnosing / acting. This is deliberate. A dashboard
is a set of decisions about what matters, and guessing produces a screen that looks right and
answers nothing. Answering three questions beats rebuilding three times.

**2. It tells you when it invented something.** The library has gaps. When a screen needs
something that isn't in it — a date-range picker, an empty state — it builds it, then hands you
a **four-line block to paste into Slack**, linking a full record in `notices/`.

**Please actually send it.** That block is the whole governance loop. Reply with one of four
verdicts:

| Verdict | Means |
|---|---|
| **Add** | it earns a place in the library — draw it in Figma |
| **Replace** | something already covers this, here's what |
| **Promote** | the deviation was right; the *component* is what's wrong |
| **Revert** | no — use the measured value |

A decision that stays in Slack gets re-made next month, differently, by someone else.

## Run it inside your target repo

It reads `package.json` and emits React for a Next app rather than a standalone file you'd have
to translate. No repo — or you just want to look at something — and you get one static HTML
file, which is faster and correct for that.

Deploy is Vercel (screens) and Railway (services). Styling is plain CSS over the token custom
properties, **not Tailwind** — the tokens are already the source of truth and a Tailwind config
would be a second copy of the same values. Details in
[`foundation/output-targets.md`](foundation/output-targets.md).

## The four ways output goes off-system

Worth knowing even if you never read another file.

**1. Wrong-surface component.** Buttons, Avatars and Logos exist **separately per surface**.
Both button sets are literally named `Button` and both have a `Style` property with completely
disjoint values — web is `Blue` / `Black` / `Outlined/ black`, dashboard is `Primary` /
`Outline` / `Ghost`. This is intentional and permanent. **If you see a blue filled button on a
dashboard, the wrong component got picked.**

**2. A hand-rolled component.** Import from `components/dashboard/` or compose from the
documented Sections. A kpi-card that *looks* right is the exact failure this repo exists to
prevent — it inherits the credibility of everything around it while nobody reviewed it.

**3. An invented token.** Every colour, type style, radius, shadow and spacing value comes from
[`foundation/tokens.css`](foundation/tokens.css). A value with no token is a **finding to
report**, never a number to make up.

**4. A number nobody measured.** If you had no real data, the header carries a `Sample data`
badge and the numbers are illustrative. **Remove the badge only when real data lands** — and
until then, don't screenshot it into a deck. A plausible figure in a real-looking dashboard is
indistinguishable from a measurement.

## Where to look things up

| Question | File |
|---|---|
| What's the hex / size / type style? | `foundation/tokens.css` |
| Which component do I use here? | the relevant `skills/*/SKILL.md` |
| What exactly does it measure? | `exports/dashboard/`, `exports/web/` |
| Why does the shell scroll like that? | `exports/dashboard/build-rules.md` |
| Voice, casing, CTA copy | `foundation/voice.md` |
| Where the two sources disagree | `RECONCILIATION.md` |

## Current state — be straight about this

**The dashboard surface is solid.** Every component is measured off Figma and the rules were
driven through a real nine-page build, so the defects are already found.

**The web surface is thinner.** Button, eyebrow, navbar, footer and client/avatar are measured;
roughly 22 components — folds, card types, inputs — are still transcribed from annotations
rather than measured. Treat web output as a good first draft, not a spec.

## You do not need Figma

Everything measured is in `exports/`. Figma is only for **maintainers changing the system** —
adding a component or correcting a measurement. If you're building a screen, you never open it.

## Who to ask

Utsav — https://gushwork.slack.com/team/U06UAR183TR

Anything the system genuinely doesn't cover yet — slides, flyers, a standalone tool — the skill
will tell you so and point you there rather than inventing something plausible. That's working
as intended.
