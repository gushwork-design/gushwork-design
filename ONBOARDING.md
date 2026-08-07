# Using the Gushwork Design System — start to finish

This makes Claude produce on-brand Gushwork screens by default: the right component for the
right surface, real tokens instead of guessed hexes, and a visible flag rather than a quietly
invented component.

Eight steps. The first four take about two minutes; the rest is how you work.

---

## Before you start

You need **Claude Code** — the CLI, desktop app, or the VS Code / JetBrains extension. If
`claude --version` prints a number, you're set. If not, install it first; nothing below works
without it.

---

## Step 1 — Install the plugin

**Check whether you need to.** If the repo you're working in has a `.claude/settings.json` that
mentions `gushwork`, it installs itself when you open the repo. Skip to Step 2.

Otherwise, two commands. Add the marketplace once, then install from it — `claude plugin install`
takes a plugin **name**, not a git URL:

```bash
claude plugin marketplace add utsav-gushwork/gushwork-design
```

```bash
claude plugin install gushwork-design@gushwork
```

## Step 2 — Restart, then check it loaded

**Restart Claude Code.** It will not load new skills otherwise — this is the single most common
reason someone thinks the install failed.

```bash
claude plugin list
```

You want to see `gushwork-design@gushwork`, a version number, and `enabled`. Two skills come
with it:

| Skill | Covers |
|---|---|
| `gushwork-dashboard` | logged-in product — dashboards, KPI cards, tables, side nav, settings screens |
| `gushwork-web` | public site — landing pages, heroes, folds, pricing, testimonials, navbar, footer |

## Step 3 — Open the repo you're building in

Not a scratch folder. Claude reads the repo's `package.json` and emits **React components in your
project's conventions** if it finds a Next app — rather than a standalone HTML file you'd have to
translate by hand.

No repo, or you just want to look at something? That's fine — you'll get a single static HTML
file, which is faster and the right output for a review.

## Step 4 — Just describe what you want

**You never name the skills.** They fire on the work:

> "Build a dashboard for the sales team to see show-ups over the week"

> "Add a KPI row to the leads screen"

> "Build a pricing page for Gushwork"

**How to tell it worked:** the reply opens with *"Using the Gushwork dashboard skill."* (or web).
If that line is missing, the skill did not fire — see troubleshooting below. Don't just carry on;
you'll get generic output wearing Gushwork's name.

## Step 5 — Answer the questions it asks

For a dashboard it will ask what the KPIs are, what should be seen first, and whether you're
**monitoring / diagnosing / acting**. It waits for you.

This is deliberate, not friction. A dashboard is a set of decisions about what matters, and
guessing produces a screen that looks right and answers nothing. Three answers beat three
rebuilds. If you genuinely don't know yet, say so — you'll get something reasonable, flagged as
assumed.

## Step 6 — Check the output against four things

You don't need to know the system to catch the failures that matter.

**1. Is the button the right one for the surface?** Buttons, Avatars and Logos exist
**separately per surface** — both button sets are literally named `Button` with completely
disjoint `Style` values. **A blue filled button on a dashboard means the wrong component got
picked.** That's the single most common way output goes off-system.

**2. Did it hand-roll something?** Components should come from `components/dashboard/` or the
documented Sections. A kpi-card that merely *looks* right is the exact failure this repo exists
to prevent — it inherits the credibility of everything around it while nobody reviewed it.

**3. Are there invented colours or sizes?** Every value comes from `foundation/tokens.css`. A
raw hex in the output is a bug. A value with no token is a **finding to report**, never a number
to make up.

**4. Is there a `Sample data` badge?** If you gave no real data, the numbers are illustrative and
the header says so. **Don't screenshot it into a deck until it's real** — a plausible figure in a
real-looking dashboard is indistinguishable from a measurement, and that's the mistake that
outlives the build.

## Step 7 — If it built something new, send the Slack block

The library has gaps. When a screen needs something that isn't in it — a date-range picker, an
empty state — Claude builds it, then hands you a **four-line block to paste into Slack**, linking
a full record in `notices/`.

**Please actually send it.** That block is the whole governance loop. Utsav replies with one of
four verdicts:

| Verdict | Means |
|---|---|
| **Add** | it earns a place in the library — draw it in Figma |
| **Replace** | something already covers this, here's what |
| **Promote** | the deviation was right; the *component* is what's wrong |
| **Revert** | no — use the measured value |

A decision that stays in Slack gets re-made next month, differently, by someone else. Thirty
seconds of pasting is what stops that.

## Step 8 — Stay current

A stale plugin fails silently: it keeps emitting last month's values with full confidence.

```bash
claude plugin marketplace update gushwork && claude plugin update gushwork-design
```

Then **restart**. Ask whoever set this up to turn on `autoUpdate` so you never think about it
again.

---

## A worked example

> **You:** build a dashboard for the sales team to see show-ups over the week
>
> **Claude:** Using the Gushwork dashboard skill. Before I build — what counts as a show-up, and
> against what denominator? Per rep or team total? And is this for monitoring the week,
> diagnosing a bad day, or chasing no-shows?
>
> **You:** booked meetings where they turned up, out of all booked. per rep. mostly chasing
> no-shows.
>
> **Claude:** Then show rate leads as one number, reps go in a table with a row action, and the
> day-of-week breakdown is a bar chart. No live data, so numbers are illustrative and the header
> carries a `Sample data` badge. Building the shell first.

Note what happened: **acting** rather than monitoring changed the layout — a table with row
actions instead of a wall of charts. That's why Step 5 exists.

---

## If it's not working

| Symptom | Cause | Fix |
|---|---|---|
| Reply doesn't say "Using the Gushwork … skill" | not loaded, or the request didn't read as Gushwork work | restart; say "use the Gushwork dashboard skill" explicitly |
| `claude plugin list` doesn't show it | install didn't complete, or you declined a prompt | re-run Step 1; a declined plugin is remembered and won't re-prompt |
| `marketplace add` fails | no GitHub access, or your org restricts marketplaces | ping Utsav — it may need adding to an allow-list |
| Output looks generic | the skill fired but you're in a repo it can't read | check you're in the product repo, not a scratch folder |
| Values differ from Figma | the plugin is stale, or Figma changed and wasn't measured in | run Step 8, then tell Utsav |

---

## Where to look things up

| Question | File |
|---|---|
| What's the hex / size / type style? | `foundation/tokens.css` |
| Which component do I use here? | `skills/gushwork-dashboard/SKILL.md`, `skills/gushwork-web/SKILL.md` |
| What exactly does it measure? | `exports/dashboard/`, `exports/web/` |
| Why does the shell scroll like that? | `exports/dashboard/build-rules.md` |
| Voice, casing, CTA copy | `foundation/voice.md` |
| React or static HTML? | `foundation/output-targets.md` |
| Where the two sources disagree | `RECONCILIATION.md` |

## Two things to know about the current state

**The dashboard surface is solid.** Every component is measured off Figma and the rules were
driven through a real nine-page build, so the defects are already found.

**The web surface is thinner.** Button, eyebrow, navbar, footer and `client/avatar` are measured;
roughly 22 components — folds, card types, inputs — are still transcribed from Figma annotations
rather than verified against what renders. Treat web output as a good first draft, not a spec.

## You do not need Figma

Everything measured is in `exports/`. Figma is only for **maintainers changing the system**. If
you're building a screen, you never open it — and you shouldn't, because reading a component
*instance* misreports type weight, which shipped a wrong nav rail twice before anyone understood
why.

## Who to ask

Utsav — https://gushwork.slack.com/team/U06UAR183TR

Anything the system genuinely doesn't cover — slides, flyers, a standalone tool — Claude will
tell you so and point you there rather than inventing something plausible. That's working as
intended, not a failure.
