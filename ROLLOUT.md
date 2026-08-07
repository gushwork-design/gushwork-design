# Rolling this out to the org

Three ways to get the plugin onto people's machines, from least to most automatic. Pick by how
many people and whether you can push config to laptops.

Everything below was verified against Claude Code **2.1.23**. Settings keys come from the
binary's own schema, not from guesswork.

| Approach | Who it fits | Effort for the teammate |
|---|---|---|
| **1. Two commands** | one or two people, ad hoc | runs two commands |
| **2. Commit `.claude/settings.json`** | a team working in known repos — **the default** | **nothing** |
| **3. Managed settings via MDM** | everyone in the org, including repos we don't control | **nothing** |

## 1. Two commands

```bash
claude plugin marketplace add utsav-gushwork/gushwork-design && claude plugin install gushwork-design@gushwork
```

Fine for a handful of people. It does not scale, and it is invisible — you cannot tell who ran
it, so you cannot tell who is on a stale version.

## 2. Commit `.claude/settings.json` to the product repos — start here

Claude Code installs marketplaces and plugins declared in settings **automatically in the
background** on startup. So this file, committed to a repo, means anyone who opens that repo
gets the design system with no commands and no instructions to follow.

**One command per repo.** Run this from the root of the repo you want it in:

```bash
curl -fsSL https://raw.githubusercontent.com/utsav-gushwork/gushwork-design/main/scripts/enable-in-repo.sh | bash
```

It merges into an existing `.claude/settings.json` rather than overwriting it, is safe to re-run,
and refuses to touch the file if it isn't valid JSON. Then commit the result.

Or write it by hand — `.claude/settings.json` in each product repo:

```json
{
  "extraKnownMarketplaces": {
    "gushwork": {
      "source": {
        "source": "github",
        "repo": "utsav-gushwork/gushwork-design"
      }
    }
  },
  "enabledPlugins": {
    "gushwork-design@gushwork": true
  }
}
```

That is the whole file. Commit it.

**Why this is the right default for a design system:** the plugin matters exactly where the
product code lives. Scoping it to those repos means a designer opening the marketing site gets
`gushwork-web`, and nobody carries it around in unrelated work.

- Pin a version with `"gushwork-design@gushwork": ["1.1.0"]` — the array form takes version
  constraints. Plain `true` tracks the marketplace's current version.
- `"source"` also accepts `{"source": "git", "url": "...git", "ref": "main"}` and
  `{"source": "url", "url": "https://.../marketplace.json"}` if you ever move off GitHub.
- A teammate who declines the prompt is recorded in `skippedPlugins` and won't be asked again —
  so if someone says it isn't loading, check that first.

## 3. Managed settings — org-wide, admin-deployed

This applies everywhere on the machine regardless of repo, and users cannot turn it off. Same
keys as above, in a file your MDM (Jamf, Kandji, Intune) drops on each laptop:

| OS | Path |
|---|---|
| **macOS** | `/Library/Application Support/ClaudeCode/managed-settings.json` |
| **Linux** | `/etc/claude-code/managed-settings.json` |
| **Windows** | `C:\Program Files\ClaudeCode\managed-settings.json` |

On Windows, `C:\ProgramData\ClaudeCode\managed-settings.json` still works but is **deprecated** —
Claude Code shows a warning and a future version will stop reading it. Use `Program Files`.

Writing to these paths needs admin rights, so this one is IT's to do, not yours.

### Two lockdown keys that only work here

Both are read **only** from managed settings — set them in user or project settings and they do
nothing.

```json
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "utsav-gushwork/gushwork-design" }
  ],
  "blockedMarketplaces": []
}
```

`strictKnownMarketplaces` is an allow-list: **only** these exact sources can be added as
marketplaces, and the check happens *before* download, so a blocked source never touches the
filesystem.

**Be careful with it.** Setting it to only Gushwork also blocks
`anthropics/claude-plugins-official` and every other plugin anyone uses. If you want the
allow-list, list both.

## Keeping everyone current

**Auto-update exists, and it is off by default for third-party marketplaces.** Official
Anthropic marketplaces auto-update; yours does not until the flag is set. Without it, a
teammate runs whatever version they installed, indefinitely, with no warning.

The flag lives per-machine in `~/.claude/plugins/known_marketplaces.json`:

```json
{
  "gushwork": {
    "source": { "source": "github", "repo": "utsav-gushwork/gushwork-design" },
    "autoUpdate": true
  }
}
```

**It is not settable from repo settings** — `extraKnownMarketplaces` entries only carry `source`
and `installLocation`. So either your MDM payload writes it, or people run this once:

```bash
curl -fsSL https://raw.githubusercontent.com/utsav-gushwork/gushwork-design/main/scripts/enable-autoupdate.sh | bash
```

That line is in [`ONBOARDING.md`](ONBOARDING.md) directly under the install, because it is the
difference between a system that stays current and one that quietly doesn't.

### What auto-update does and doesn't cover

Verified against the 2.1.23 startup path (`uB0`):

- **Does:** refresh the marketplace, update installed plugins, and report what changed. Covers
  `user` and `managed` scopes, plus project scope when you're in that project.
- **Doesn't:** take effect in the session that pulled it. The refresh is fire-and-forget at
  startup, so a new version lands during one run and loads on the **next**.
- **Doesn't:** run at all if the auto-updater is disabled globally.
- **Doesn't** apply to committed `.claude/settings.json`. That path installs what's **missing** —
  it never updates what's already there. Distribution and updating are separate problems.

Manual update, when someone hasn't:

```bash
claude plugin marketplace update gushwork && claude plugin update gushwork-design@gushwork
```

**A restart is required either way.** Claude Code says so on install and it means it — a
teammate who updates without restarting is still on the old skills.

## Checking what someone is actually running

```bash
claude plugin list
```

The version shown comes from `.claude-plugin/plugin.json`, **not** the marketplace entry. Both
carry a `version` field and nothing keeps them in sync, so bump both — see the propagation table
in [`README.md`](README.md).

## What to send people

If you took approach 2 or 3, there is nothing for them to install, so don't send install
instructions — send this:

> The Gushwork design system is now in `<repo>`. Just describe what you want — "build a dashboard
> for X", "add a KPI row" — and Claude uses the real components and tokens. It'll ask a couple of
> questions first; that's on purpose.
>
> Restart Claude Code once so it loads. Two things to know: if the reply doesn't open with "Using
> the Gushwork … skill" it didn't fire, and if a dashboard shows a `Sample data` badge the numbers
> are illustrative — don't put it in a deck yet.
>
> Detail if you want it: https://github.com/utsav-gushwork/gushwork-design/blob/main/ONBOARDING.md

[`ONBOARDING.md`](ONBOARDING.md) is the fuller version — three steps and the reference material
for when something looks wrong. It covers the four ways output goes off-system, which is what
actually determines whether the system holds.

## Announcing a release

```bash
bash scripts/release-notes.sh
```

Prints a short Slack message summarising what changed since the last release, built from the git
log. Review it, then post it. There is no push notification, so an unannounced release reaches
only the people with auto-update on.
