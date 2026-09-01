---
name: gushwork-lead-magnet
description: Builds Gushwork lead-magnet documents — the downloadable PDF asset behind an ad landing page. Checklists, prompt packs, audit worksheets, playbooks, teardowns, buyer guides. Use this whenever the deliverable is a multi-page PDF a prospect downloads in exchange for their details: "a lead magnet", "a downloadable guide", "a PDF checklist", "the gated asset for this campaign", "a worksheet for the ad". Not for the landing page itself — use gushwork-web for the lander, the hero and the form.
---

# Gushwork lead magnet

You are building a **downloadable document**, not a web page. It is the asset behind a paid
ad: someone clicked, gave an email, and now has a PDF open. It has to look considered on a
laptop screen, survive being printed, and end on a reason to book.

Announce at the start: **"Using the Gushwork lead-magnet skill — v1.42.0, updated 28 Aug 2026."**

That version and date are stamped into this file, so **a stale copy reports its own stale date**
rather than claiming to be current.

## Read these first

| For | Read |
|---|---|
| Every colour, radius, shadow | `foundation/tokens.css` |
| **Every standing ruling** | `DECISIONS.md` |
| Voice, casing, banned words, CTA copy | `foundation/voice.md` |
| Gushwork logo, Phosphor icons | `foundation/shared-components.md` |
| **Page shell, margins, render pipeline** | `exports/lead-magnet/document.md` |
| **The cover** — measured, Figma-exact | `exports/lead-magnet/cover.md` |
| **The closer** — measured, Figma-exact | `exports/lead-magnet/closer.md` |
| Running head, prompt rows, worksheets, score bands | `exports/lead-magnet/interior.md` |

## Start from the template. Never from a blank file.

`templates/lead-magnet/lead-magnet.html` is the base for **every** lead-magnet document. It is
a complete nine-page worked example — the "Can AI find your business?" prompt pack — and it
doubles as the component library. Copy it, keep the page types you need, delete the rest,
refill the copy.

```
cp -r templates/lead-magnet templates/<your-doc-slug>
cd templates/<your-doc-slug> && ./render.sh
```

Rendering needs Google Chrome and, on the first run, a network connection — Phosphor icons
come from the jsDelivr CDN and are then embedded as a font subset. Fonts are local.

## The three page types

| Type | Ground | What it is |
|---|---|---|
| **Cover** | `--gw-color-black` + blueprint grid | Logo, chip pair, headline, standfirst, hero image. Laid out at Figma coordinates in `pt` |
| **Interior** | `--gw-color-neutral-25`, white cards on top | Running head, heading, body, then components. This is where the content lives |
| **Closer** | `--gw-color-black` + blueprint grid | Headline, two paragraphs, one button. The only ask in the document |

Interiors invert the usual convention: the **page** is the neutral wash and the **cards are
white**. Anything you add must be a white surface or it vanishes into the ground.

## Guardrails

- **No footers.** The running head carries identity, section and page number. Adding a footer
  back costs ~30pt on every page and duplicates what the head already says.
- **No kicker above the heading.** Section identity lives in the running head, right-aligned:
  `Part 1 of 4 · Page 03 of 09`.
- **Page numbers are literal strings.** Add or remove a page and every head must be renumbered
  by hand. There is no generator.
- **The pages are fixed-height with `overflow:hidden`, so overflow is silent.** After any copy
  change, measure — see the check in `exports/lead-magnet/document.md`. Eyeballing has passed a
  clipped page more than once.
- **One ask, at the end.** A lead magnet earns the click by being useful first. Do not scatter
  CTAs through the interior pages.
- Numbers and outcomes lead, as everywhere else. No gradients, no emoji, no italics in display
  copy.

## When the design comes from Figma

The cover and closer are **owned by Figma frames**, not by this template. Re-fetch the node
before editing either — they are Letter-sized, so they are laid out at true Figma coordinates
in `pt` and every number in the export docs is measured, not eyeballed. Do not round them.

`CONTRIBUTING.md` applies in full: read the component set and not an instance, compare geometry
numerically, and sample the render for colour.
