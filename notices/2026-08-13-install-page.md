# Hosted install page — new elements and deviations

Built 13 Aug 2026. Files: `preview/install.html`, `scripts/publish-sheets.sh`,
`scripts/publish-index.html`, `INSTALL.md`

**Why it exists.** The plugin was only installable by someone who could read the repo README
or the org-only Claude Code onboarding link. Neither reaches people joining on personal
Claude accounts. This is a public, copy-and-run page:
`https://gushwork-design.vercel.app/preview/install.html`

Four sections only — what this is, install, verify, changelog. An earlier draft carried
numbered step cards, a troubleshooting table and a separate auto-update section; it was cut
back because the page is read once, under mild time pressure, by someone who wants a command.

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

### `.rel` — a changelog row
Version, description, date in one line. `fold-elements.md` has table rows, but they belong to
`fold/Comparison Table` and carry its 4-column structure; this is a three-part list row on a
utility page.

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

**3. The changelog rows and the version number are hardcoded.** They will drift on the next
release. Everything else on the page is version-independent, so the drift is contained — but
`scripts/` already generates `CHANGELOG.md` and `preview/changelog-sheet.html` from
`scripts/_releases.sh`, and this page should be fed from the same source rather than
hand-maintained. Left as-is for now, flagged rather than hidden.

## Tokens

43 custom properties used, all already defined in `foundation/tokens.css`. Verified
mechanically — every `var(--gw-*)` in the file was diffed against the token definitions and
the missing set was empty. No raw hex anywhere outside the shared favicon data-URI, which is
copied verbatim from `scripts/_favicon.txt`.

**Light surface only.** No dark block remains; the page has no `neutral-900`, `neutral-850`
or `black` background. Colour is `primary-25/100/300/500`, `neutral-25/50/100/200/400/600/
700/900`, `white`, `black` (text only). Type `h5`, `h7`, `body-16-reg`, `body-14-reg/med`,
`body-12-reg/med/sem` with tracking pairs. Radius `8/10/12`. Shadow `s2`. Spacing
`2/4/8/12/16/20/24/32/40/56/80`. Plus `--gw-motion-fast`, `--gw-focus-ring`,
`--gw-focus-offset`, `--gw-font-body`, `--gw-font-display`.

**One value is not from a token and is declared as a choice:** the 720px column width, taken
from `publish-index.html` so the two hosted pages agree. It is not `--gw-content-width`
(1240), which is the marketing column and wrong for this surface.
