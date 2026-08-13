# Hosted install page — new elements and deviations

Built 13 Aug 2026. Files: `preview/install.html`, `scripts/publish-sheets.sh`,
`scripts/publish-index.html`, `INSTALL.md`

**Why it exists.** The plugin was only installable by someone who could read the repo README
or the org-only Claude Code onboarding link. People joining on personal Claude accounts had
neither. This is a public, copy-and-run page: `https://gushwork-design.vercel.app/preview/install.html`

## Created

### `.step` — a numbered instruction row
A 28px `--gw-radius-full` counter in `--gw-color-primary-500` beside a title and body.
Nothing in `folds.md` or `fold-elements.md` covers ordered instructions — `fold/Timeline` is
the closest and is week-based, dark-themed, and marketing-shaped, so it fits neither the
content nor the surface. Lives in `preview/install.html`.

### `.code` — a copyable command block
Dark `--gw-color-neutral-900` block with a copy control pinned top-right. The library has no
code or terminal element at all; this page is meaningless without one, since every step is a
command someone has to run exactly.

The copy control uses the three-tier ladder `foundation/new-component-notice.md` already
prescribes for artifacts — `navigator.clipboard`, then a hidden `textarea` +
`execCommand`, then select-and-name-the-shortcut. **Verified all three paths in-browser**: a
real click reaches tier 1 (`TIER1_OK`), a synthetic click with no user activation degrades to
tier 3 with the platform-correct shortcut. It never fails silently.

Button styling is `--gw-color-neutral-alpha-10-white` → `-20-white` on hover, not a `Button`
instance. The web `Button` set has no on-dark icon-plus-label variant at this size, and
`Special/ Glowing` exists only at `Size=Large, Icon Placement=Trailing` — the gap already
recorded in the skill.

## Modified

Nothing. `scripts/publish-index.html` gained a fourth card using its own existing `.card`
pattern and a new Phosphor `download-simple` symbol; no component was changed.

## Worth a decision

**1. This page does not use `page-build`.** The skill says start from Page Build and never
hand-build page chrome. I followed `scripts/publish-index.html` instead — 720px column, no
navbar, no footer — because this is a hosted utility page in the sheets family, not a
marketing page. Forcing a navbar and full footer onto a six-step install doc would have made
it look like a landing page and buried the commands. **If the ruling is that anything served
on a public URL is a marketing surface, this should be rebuilt on `page-build` with
`Type=Brand` and the steps inside `fold/ other`.** That is the one call here I would not make
alone.

**2. Commands are set in Inter, not a monospace face.** `publish-index.html` established
"two families only — the browser's default `<code>` face would be a third", and I kept it.
It is the right call for consistency and the wrong one for a page whose entire purpose is
reading commands character-by-character, where `l`/`1` and `O`/`0` matter. Worth deciding
whether a mono face becomes a third sanctioned family for code contexts only, or whether the
two-family rule holds and this stays as-is.

## Tokens

50 custom properties used, all already defined in `foundation/tokens.css`. Verified
mechanically — every `var(--gw-*)` in the file was diffed against the token definitions and
the missing set was empty. No raw hex outside the shared favicon data-URI, which is copied
verbatim from `scripts/_favicon.txt`.

Colour `primary-25/100/500`, `neutral-50/100/200/900`, `neutral-alpha-10/20/80-white`,
`yellow-25/200/700`, `white`, `black`. Type `h5`, `h7`, `body-16-reg/sem`,
`body-14-reg/med/sem`, `body-12-reg/med/sem` with tracking pairs. Radius `8/10/12/full`.
Shadow `s2`. Spacing `2/4/8/12/16/24/32/40/56/80`. Plus `--gw-motion-fast`,
`--gw-focus-ring`, `--gw-focus-offset`, `--gw-font-body`, `--gw-font-display`.

**One value is not from a token and is declared as a choice:** the 720px column width, taken
from `publish-index.html` so the two hosted pages agree. It is not `--gw-content-width`
(1240), which is the marketing column and wrong for this surface.
