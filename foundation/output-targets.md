# What to actually emit

Both skills reference this. Neither restates it.

A design system that only produces screenshots is a mood board. Gushwork ships on **Vercel and
Railway, deployed from GitHub**, so the output has to be code that lands in one of those
repos — not a standalone file someone has to translate first.

## The default: React, in the repo you are already in

| | Choice | Why |
|---|---|---|
| **Framework** | **Next.js App Router**, React function components | What Vercel deploys with no configuration |
| **Language** | TypeScript if the repo has it, otherwise JS | Never introduce TS into a JS repo to satisfy this file |
| **Styling** | **Plain CSS + the `tokens.css` custom properties** | The tokens already *are* CSS custom properties |
| **Components** | `components/dashboard/` in this repo | Measured once, imported everywhere |
| **Fonts** | self-hosted from `fonts/`, via `next/font/local` | No network font fetch; both faces are committed |

### Not Tailwind — and this is a decision, not an oversight

`foundation/tokens.css` is the single source of truth for every colour, size, radius, shadow
and type style, generated from the Figma **variables**. A `tailwind.config` would be a second
copy of those same values, and the moment Figma changes, one of the two copies is wrong and
nothing tells you which.

If the target repo already uses Tailwind, **don't fight it** — map the utilities to the token
custom properties (`bg-[var(--gw-color-neutral-900)]`) rather than to raw hexes, and say in one
line that you did. What is banned is a parallel palette, not the utility syntax.

## Read the repo before choosing — it decides for you

Do this before writing a line. It takes one look and prevents the single most wasteful
outcome: a correct design delivered in a form the codebase cannot accept.

| What you find | Emit |
|---|---|
| `package.json` with `next` | React components in the repo's own conventions, its directory layout, its import style |
| `package.json` with React but not Next | Plain React components, no `next/*` imports, no `'use client'` |
| A repo in another stack (Vue, Django, Rails) | Its templates, using `tokens.css`. Say that the measured components are React and that you translated them |
| No repo — a mockup, a review, "show me what it'd look like" | **A single static HTML file.** Correct and much faster; nobody merges it |

**When you genuinely can't tell, ask.** It is one question and it saves a rebuild.

## Where the pieces live

```
foundation/tokens.css          import once, in the root layout
components/dashboard/          measured React components — the dashboard surface
fonts/                         both variable faces, committed, licensed
preview/*.html                 static reference builds, not importable
```

`components/dashboard/README.md` lists what exists. **Import from there before writing a
component** — a hand-rolled kpi-card that looks right is the exact failure this repo exists
to prevent.

## Deploying — the two that bite

**Fonts.** `Vert_Grotesk_Display_VF.ttf` and the two Inter variable faces are committed here
and licensed for our use. Load them with `next/font/local` pointed at the committed files.
Never load a Gushwork face from a CDN, and never let a build fall back to `system-ui` — the
display face is the brand and a fallback is silently off-brand. Verify by **measuring rendered
text width**, not with `document.fonts.check()`, which returns true for a face that is merely
*declared* and 404s.

**Railway holds the data; Vercel holds the screen.** Which means the shell renders before the
numbers arrive — always. So:

- **Every Section needs a loading state and an empty state.** Not optional in a deployed app.
- **The library has neither.** No skeleton, no spinner, no empty state. `Skeleton` and
  `Spinner` appear in `shared-components.md` only as *intended* components; nothing is drawn.
- So they are **build-then-declare**: compose from `section/Container` and tokens, comment
  them as pending review, and put them in the notice. See
  `foundation/new-component-notice.md`.

Never render a zero, a dash, or a plausible-looking number while data is in flight. A `0` that
means "not loaded yet" is read as "we got no leads", and that misreading is expensive.

## Publishing a dashboard as a hosted Artifact

A static file is often shared as an Artifact rather than deployed. Three things bite, all found
26 Aug 2026 and none visible until the page is actually in the frame.

**The wrapper is supplied.** The host wraps the file in its own `<!doctype html><head></head>
<body>`, so the file must contain none of those tags. Guard the check with a boundary — a bare
`<head` search also matches `<header class="topbar">`, and a comment containing a literal tag
name will trip it too.

**A viewport-relative height inside a content-sized frame resolves to ZERO.** The host sizes the
frame from the content height the page reports. A dashboard shell locks `html, body { overflow:
hidden }` and derives its height from `100vh`, which is circular there: reported height is 0, the
frame collapses, and the page renders **blank rather than broken** — easy to misread as a build
failure. Use `100dvh`, which resolves against the frame's own viewport, and keep a fixed canvas
only as a fallback applied by MEASUREMENT (`root.clientHeight < 200`). Do **not** pin a fixed
height unconditionally: in any frame shorter than it, the overflow sits outside the viewport with
`overflow: hidden` and is both clipped and unreachable.

**The host owns `data-theme`.** It stamps that attribute on the root element to carry the reader's
light/dark preference. Any dashboard using the same attribute for its own theme toggle collides
with it. Read the host's attribute as one input, write your own under a different name, and
declare both directions so the in-page control can still override — with the in-page selector
LAST, since the two have equal specificity.

## What stays out of scope

The design system covers **what a screen looks like**. It has no opinion on data fetching,
auth, state management, or API shape — those are the app's, and inventing a convention here
would be a rule nobody agreed to. Build the surface; leave the plumbing to the repo.
