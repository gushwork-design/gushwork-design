# Hosted install page — new elements and deviations

Built 13 Aug 2026. Files: `preview/install.html`, `scripts/publish-sheets.sh`,
`scripts/publish-index.html`, `INSTALL.md`

**Why it exists.** The plugin was only installable by someone who could read the repo README
or the org-only Claude Code onboarding link. Neither reaches people joining on personal
Claude accounts. This is a public, copy-and-run page:
`https://gushwork-design.vercel.app/preview/install.html`

**Two sections only — install, verify.** Earlier drafts carried a "what this is" section, a
changelog list, numbered step cards, a troubleshooting table, a prerequisite callout and a
separate auto-update section. All cut. The page is read once, by someone who wants a command,
and every section that is not a command competes with the ones that are. Version, date and
the changelog link now sit on one meta line under the header.

## Created

### `.code` — a copyable command block
Light block on `--gw-color-neutral-25` with a `--gw-color-neutral-100` border and a copy
control top-right. The library has no code or terminal element at all, and this page is
meaningless without one since every instruction is a command run exactly as written.

The copy control uses the three-tier ladder `foundation/new-component-notice.md` already
prescribes — `navigator.clipboard`, then a hidden `textarea` + `execCommand`, then
select-and-name-the-shortcut. **All three paths verified in-browser**: a real click reaches
tier 1 (`TIER1_OK`), a synthetic click with no user activation degrades to tier 3 with the
platform-correct shortcut, and the control self-resets after 2s. It never fails silently.

The control is not a `Button` instance — the web `Button` set has no icon-plus-label variant
at 28px, and `Special/ Glowing` exists only at `Size=Large, Icon Placement=Trailing`, the gap
already recorded in the skill.

It is pinned over the first line of the block, so the block reserves space for it:
`min-width: --gw-space-80` on the control fixes its footprint at 80 (+8 offset = 88) and the
block carries `padding-right: --gw-space-100`. Both are spacing tokens, not chosen numbers.
The fixed width matters — the first build let the control size to its label, so it grew when
the label changed to "Copied" and sat on top of the command. The tier-3 fallback label was
shortened to `⌘C` / `Ctrl+C` for the same reason.

### `.step` — a numbered instruction row
A 26px `--gw-radius-full` counter in `--gw-color-primary-500` beside a title and body.
Nothing in `folds.md` or `fold-elements.md` covers ordered instructions — `fold/Timeline` is
the closest and is week-based, dark-themed and marketing-shaped, so it fits neither the
content nor the surface.

### `.or` — an either/or divider
A centred `OR` on a `--gw-color-neutral-200` rule, separating two routes to the same outcome
inside one step. The library has no element for branching instructions; the alternative was
two numbered steps implying sequence, which would be wrong — you do one or the other, not
both.

## Modified

Nothing. `scripts/publish-index.html` gained a fourth card using its own existing `.card`
pattern and a new Phosphor `download-simple` symbol; no component was changed.

## Worth a decision

**1. This page does not use `page-build`.** The skill says start from Page Build and never
hand-build page chrome. I followed `scripts/publish-index.html` instead — 720px column, no
navbar, no footer — because this is a hosted utility page in the sheets family, not a
marketing page. **If the ruling is that anything on a public URL is a marketing surface, this
should be rebuilt on `page-build` with `Type=Brand` and the content inside `fold/ other`.**
That is the one call here I would not make alone.

**2. Commands are set in Inter, not a monospace face.** `publish-index.html` established
"two families only — the browser's default `<code>` face would be a third", and I kept it.
Right for consistency, arguably wrong for a page whose purpose is reading commands where
`l`/`1` and `O`/`0` matter. Worth deciding whether mono becomes a sanctioned third family for
code contexts only.

**3. The version and date in the meta line are hardcoded** and will drift on the next
release. `scripts/_releases.sh` already derives both for `CHANGELOG.md` and
`preview/changelog-sheet.html`; this page should be fed from the same source rather than
hand-maintained. Flagged rather than hidden.

**4. The page no longer states that Claude Code is a prerequisite.** A callout saying so —
and that pasting into claude.ai does nothing — was removed as clutter. That is the single
most likely way a reader on a personal account fails, and the page is now silent on it.
`INSTALL.md` still covers it. Worth confirming the trade is the one you want.

## Tokens

43 custom properties used, all already defined in `foundation/tokens.css`. Verified
mechanically — every `var(--gw-*)` in the file was diffed against the token definitions and
the missing set was empty. No raw hex anywhere outside the shared favicon data-URI, which is
copied verbatim from `scripts/_favicon.txt`.

**Light surface only.** No dark block remains; the page has no `neutral-900`, `neutral-850`
or `black` background. Colour is `primary-300/500`, `neutral-25/50/100/200/500/600/900`,
`white`, `black` (text only). Type `h5`, `h7`, `body-16-reg/sem`, `body-14-reg/med`,
`body-12-reg/med/sem` with tracking pairs. Radius `8/10/12/full`. Shadow `s2`. Spacing
`2/4/8/12/16/20/24/32/40/56/80`. Plus `--gw-motion-fast`, `--gw-focus-ring`,
`--gw-focus-offset`, `--gw-font-body`, `--gw-font-display`.

**One value is not from a token and is declared as a choice:** the 720px column width, taken
from `publish-index.html` so the two hosted pages agree. It is not `--gw-content-width`
(1240), which is the marketing column and wrong for this surface.
