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

`.claude/settings.json` in each product repo:

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
and `installLocation`. So either your MDM payload writes it, or people set it once by hand.

Manual update, when someone hasn't:

```bash
claude plugin marketplace update gushwork && claude plugin update gushwork-design
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

The commands are the small part. Send them [`ONBOARDING.md`](ONBOARDING.md) — five minutes, and
it covers the four ways output goes off-system, which is what actually determines whether the
system holds.
