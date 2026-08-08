# `dashboard-login-screen` — measured into the library

Measured 8 Aug 2026 off `2325:1202`, all three symbols read individually.

Files: `exports/dashboard/login-screen.md` (new) · `skills/gushwork-dashboard/SKILL.md` ·
`preview/review-sheet.html`

**Nothing was created.** The component already existed in Figma and was simply absent from the
repo. This documents it and records four inconsistencies found while doing so.

## Worth a decision

**1. The Google button is built three ways different across two variants of one component.**

| | `Type=Google` | `Type=Google + Email` |
|---|---|---|
| Height | 72 | 48 |
| Radius | `radius/16` | 12 |
| Trailing `ArrowRight` | yes | no |

Everything else about them matches. Nothing in the file says which is intended, and a build has
to pick one. **Your call.** The 48/12 version is closer to the measured `Button` `Large`
geometry, if that helps.

**2. `dashboardTitle` binds a raw `black`.** `#000000`, where every other title in the system is
`--gw-color-neutral-black` `#0d0d0d`. Same defect as `Button Style=White` in the web set — a
palette change would miss it. Two components now share this failure, which suggests a habit
rather than a one-off.

## Findings — recorded as measured, not corrected

| Finding | Detail |
|---|---|
| **`0.81px` border on the Google button** | Not a token and not a round number — a 1px border on a scaled instance. Build 1px. |
| **The logo tile's variable and value disagree** | Bound to `spacing/8` and `radius/8` while rendering 15 and 15, because the instance is scaled 2× — a 60px tile around a 30px symbol. Any `spacing/8` reading on a scaled instance is suspect. |
| **Two lattice treatments now exist** | This screen uses **dashed `neutral/800`** 40px squares; `cta-image` uses **solid `primary/400`** ones. Same idea, different treatment, no rule saying when to use which. |

## Tokens

**No new colour, type, radius, shadow or spacing value was introduced.** The screen uses
`neutral/black`, `neutral/25`, `neutral/400`, `neutral/50`, `neutral/500`, `neutral/600`,
`neutral/200`, `neutral/800`, `neutral/white`, `radius/20`, `radius/16`, `radius/8`,
`spacing/32`, `spacing/8`, and the type styles `h5`, `body-20-reg`, `body-16-med`,
`button-14-med`, `button-16-med` plus **Vert Grotesk Display Medium 60**, which has no token —
the display ramp tops out at `h1` 60 **Bold**, and this is Medium at the same size.
