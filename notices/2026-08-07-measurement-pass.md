# Web measurement pass — corrections and findings

Measured 7 Aug 2026. All 12 folds, `web/ component-library` (23 sets), `badge`, `Button`,
`cta-image`, and the `list-item` set.

Files: `foundation/tokens.css` · `exports/web/folds.md` · `exports/web/component-library.md` ·
`exports/dashboard/dashboard-build.md` · `preview/review-sheet.html`

**No new design element was created.** This pass measured what already exists and corrected the
repo where it disagreed with Figma. Everything below is a *change to a documented value* or a
*finding in the source* — which is why it needs your eye rather than mine.

---

## Modified — values this repo had wrong

### `tokens.css` — every letter-spacing token, px → em

The single biggest one. Figma reports `letterSpacing` as a **percent of font size**, not px.
`tokens.css` read it as px, making all 18 tracking values **5–6× too wide** on every piece of
text the system has ever generated.

| Style | Figma | Actually renders | File had |
|---|---|---|---|
| `body-18-med` | −0.2 | **−0.036px** at 18px | −0.2px |
| `body-16-med` | −0.2 | **−0.032px** at 16px | −0.2px |
| `body-18-sem` | −0.6 | **−0.108px** at 18px | −0.6px |

Three independent confirmations, exact. Now emitted in `em`, with the evidence in the file so the
wrong reading is not re-derived.

### `dashboard-build.md` — nav row and group label weights

Said **Inter Bold 14** and **Inter Bold 10**. The `list-item` set (`2102:13507`) says **Medium
500** and **Semi Bold 600**. The table had been written from a design-context read of the
*instance inside the shell*, which reports `Inter:Bold` for both.

`section-elements.md` already had this right and warned about the conflict. Two exports
disagreed; the wrong one was read and a rail shipped bold. **This is the second time this
specific defect has occurred.** The file now says which one wins.

Same file wrongly claimed `list-item`'s hover and selected fills were unmeasured. They are —
`neutral/25` and `neutral/50`.

### `folds.md` — `fold/ CTA` was described backwards

Recorded as a centred block with avatars. It is a **440-tall blue panel** with a white `h3`, two
buttons, and `cta-image` filling 600 on the right. The 600 is the image block; the `radius/40`
56×40 shapes are `ClientAvatar`s nested *inside* it. Written from aggregate token counts rather
than the component's structure.

### `folds.md` — `Show Card` toggles

The shared-toggles rule says `Show Card 3`–`6`. They exist only on **`Cards Grid (small)`**, as
`Show Card 4` and `Show Card 5` — two booleans, default `false`, so it renders three cards and
tops out at five. `fold/ Cards Grid` has none; its axes are `Card Style`, `Card Image` and
`Card Layout`, where **`Grid` is Desktop-only and `Single`/`Stacked` are Phone-only**.

---

## Worth a decision

**1. Confirm the letter-spacing fix.** It changes the rendering of every text style in the
system. The evidence is three exact matches at three sizes, but it is a system-wide change and
should be your call, not mine. If you disagree, everything else here is unaffected.

**2. The `image` typos are still open, and they are variant keys.** `image/startegy-and-pages`
(the **default** variant) and `image/product-&-serivce-cards`. The structure blob carries an
unresolved `[decide before handoff]` asking whether to fix them in Figma or keep them
permanently. Renaming breaks anything keyed to them; not renaming means the misspelling is
permanent. **This has been open since before this pass and blocks nothing until someone builds an
image-heavy page — then it blocks immediately.**

**3. `Button Style=White` binds raw `white` and raw `black`.** Its label renders at `#000000`
where every other button label is `neutral/black` `#0d0d0d`. Two untokenised values in the
most-used component in the system, and a palette change would not reach them.

---

## Findings — source inconsistencies, not changed here

Recorded as measured; none corrected in the exports, per the rule that the component wins.

| Finding | Detail |
|---|---|
| **No `Radius` variable in `Button`** | All 220 variants use raw 8px and 12px corners. A radius change in the variables reaches nothing. |
| **`Large` + `Icon Only` is 58 × 58** | Every other `Icon Only` squares off against its row height (36, 44). Large is 2px larger, consistently across all six styles. |
| **`_Helper/Purple` `#8427DE` ships inside `badge`** | A scaffolding variable bound in the component both surfaces share. |
| **Dark badge alphas are inconsistent** | `Green` reuses `alpha/10` — the same as its Light fill — where `Red` and `Yellow` step to `alpha/20` and `Blue` jumps to `alpha/40`. |
| **`Comparison Table` binds three raw hexes** | `#f7f8f9` is `neutral/25`, `#f2f8ff` is `primary/25`, plus a bare `bg-white`. |
| **`body-16-reg` reports two different trackings** | `−0.6` on `Comparison Table`, `−0.2` on both Cards Grids. One name, two values. |
| **`Testimonial` quote is Vert Grotesk Semibold 44** | No such token — `h3` is 44 **Bold** and the display ramp has no 44 Semibold. |
| **`Special/*` buttons cannot obey their own rule** | Both exist only at `Large` + `Trailing`, with no `Disabled`. The rule asks for Medium in all folds. |
| **`Text/ black`** | 36 built variants, documented nowhere. |
| **`badge`** | Rule names five colours and calls the default "Grey". Six exist; the value is `Neutral`; **`Blue` is undocumented**. |
| **`ai-agents`** | Rule names nine agents against 20 variants — the undocumented tenth is almost certainly `other`. |
| **`tooltip`** | Rule calls the property "Arrow position"; it is `Position`. |
| **`input-fields`** | The four documented dropdown names match **none** of the actual values, and "Success" is the value `Verified`. |

## Tokens

**No new colour, type, radius, shadow or spacing value was introduced.** Four bound variables
have no token in `tokens.css`:

| Variable | Value | Used by |
|---|---|---|
| `Colors/Secondary/500-main` | `#111827` | `fold/ CTA`, `Comparison Table` — a whole Secondary collection |
| `Colors/Neutral/white` | `#ffffff` | `fold/ CTA`, `eyebrow`, `Button` |
| Vert Grotesk Semibold 44 | — | `fold/ Testimonial` quote |
| `Colors/Green/Alpha/20` | — | absent where Red and Yellow have one |

## Assets

**Six AI-engine glyphs inside `cta-image` `Image=AI Search Engines` are not harvested** — gemini,
copilot and four others. They are remote Figma URLs that expire in about seven days. That variant
cannot be built until they are in `assets/`.

## Still unmeasured

Phone variants of all 12 folds · Hero's other four layouts · 21 of 23 `component-library` sets ·
the page shell (`page-build`, `navbar`, `footer`, `announcement-banner`, 13 fold-elements) ·
four of six `cta-image` `Image` values.

`footer/footer-elements/list-item` (`1672:35328`) is a **broken component set in Figma** and
cannot be read until it is fixed.
