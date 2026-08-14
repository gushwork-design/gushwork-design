# Install the Gushwork Design System

Five minutes. Works on **any Claude account** — personal or work. You don't need to be in the
Gushwork org.

After this, Claude builds Gushwork screens using the real components and tokens instead of
guessing at them.

---

## First, two prerequisites

**1. Claude Code** — the terminal tool, not the claude.ai website. Pasting the commands below
into the claude.ai chat box does nothing.

```bash
claude --version
```

No output, or "command not found"? Install it first: https://docs.claude.com/en/docs/claude-code/setup

**2. GitHub access to this repo.** The marketplace is a git clone, so you need to be able to
reach the repo and have git authenticated on this machine:

```bash
git ls-remote https://github.com/utsav-gushwork/gushwork-design.git HEAD
```

A commit sha means you're set. An error means one of two things — **ask Utsav to add you as a
collaborator**, and make sure git can authenticate:

```bash
gh auth login && gh auth setup-git
```

> The repo is public at the time of writing, so this check passes for everyone. It becomes a
> real gate when the repo goes private — access will be granted per person.

---

## Then install the plugin

**The easy way — paste this into Claude Code** and approve the commands it runs:

```
Set up the Gushwork Design System plugin for me:

1. Run: claude plugin marketplace add utsav-gushwork/gushwork-design
2. Run: claude plugin install gushwork-design@gushwork
3. In ~/.claude/plugins/known_marketplaces.json, set "autoUpdate": true on the
   "gushwork" entry. Leave everything else in that file alone.
4. Verify with: claude plugin list

Then tell me to restart Claude Code, and give me three lines on how to use it.
```

**Or run it yourself**, in any terminal:

```bash
claude plugin marketplace add utsav-gushwork/gushwork-design && claude plugin install gushwork-design@gushwork
```

This repo is its own single-plugin marketplace — that's why it's two steps. `claude plugin install`
resolves a plugin *name from a marketplace*, not a git URL, so the marketplace has to be added
first. Installs at user scope by default, so it's live in **every** project you open, not just
the current folder.

---

## Now restart Claude Code

**This is the step people miss.** The plugin does not take effect in the session you installed it
from. Quit Claude Code and start it again.

Then confirm it's there:

```bash
claude plugin list
```

You should see `gushwork-design`.

## And check that it actually fires

Ask for something real:

> "Build a dashboard for the sales team to see show-ups over the week"

**The reply must open with "Using the Gushwork dashboard skill."** If that line is missing, it
didn't fire — restart again, or say "use the Gushwork dashboard skill" explicitly.

You never name the skills yourself. They trigger on the work.

It'll ask two or three questions before building — what the KPIs are, what matters most, whether
you're monitoring or acting. That's deliberate, not a stall.

---

## Don't skip the auto-update flag

Step 3 above sets `"autoUpdate": true`. It isn't required to make the plugin work, which is
exactly why it gets skipped — and then **stale versions fail silently.** They emit last month's
colours and spacing with full confidence. No error, no warning, just quietly wrong output.

If you skipped it, update by hand whenever things look off:

```bash
claude plugin marketplace update gushwork && claude plugin update gushwork-design@gushwork
```

Restart after. Either way, a new version takes effect on the **next** start, not the current one.

---

## If something isn't working

| Symptom | Fix |
|---|---|
| `claude: command not found` | Claude Code isn't installed — see the prerequisite above |
| Nothing happened when I pasted the commands | You pasted into claude.ai instead of Claude Code |
| `claude plugin list` doesn't show it | Run the install again — a declined plugin won't re-prompt on its own |
| No "Using the Gushwork … skill" line | You didn't restart; or ask for the skill by name |
| `marketplace add` fails | Most likely **you don't have repo access yet, or git isn't authenticated** — the repo is private. Run `git ls-remote https://github.com/utsav-gushwork/gushwork-design.git HEAD`: an error means ask Utsav to add you, then `gh auth login && gh auth setup-git`. Failing that, your work org may restrict marketplaces |
| Output looks generic | You're in a scratch folder, not a real product repo |
| Values don't match Figma | You're on a stale version — see auto-update above |

---

## Next

Read [`ONBOARDING.md`](ONBOARDING.md) — five minutes, and it covers the four ways output goes
off-system before you ship it.

Rolling this out to a team inside a shared repo? Don't send these commands around. Commit a
`.claude/settings.json` and it installs itself — see [`ROLLOUT.md`](ROLLOUT.md).
