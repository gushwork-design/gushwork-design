# Lead-magnet closer — measured

Source: **`GW Meta / Google Ads`**, frame `Letter - 4`, `node-id=1769-3965`,
file key `O6g05YAT980r85VaDQha4h`. Letter-sized, so again laid out at true Figma coordinates
in `pt`.

The last page carries the document's only ask.

| Element | Position · size | Spec |
|---|---|---|
| Ground | full bleed | `--gw-color-black`. **The frame is flat — the grid here is an override**, see `RECONCILIATION.md` |
| Logo | `40,40` · 126.29×24 | blue symbol + white wordmark |
| Headline | `40,184` · 459×106 | `Heading/h3` — Vert Grotesk Display Bold **44/1.2**, white, hard break |
| Body | `40,310` · 532×184 | `Body/body-16-reg` — Inter Regular **16/24**, `--gw-color-neutral-400`, two paragraphs with a **16pt** gap |
| Button | `40,534` · **246×44** | radius **10pt**, `--gw-color-primary-500`, label Inter Medium **18pt**, padding `0 21pt 0 22pt`, gap 13pt, icon `ph-bold ph-arrow-up-right` at 18pt |

The headline takes a **2pt** nudge for the same ascent-vs-half-leading reason as the cover.

## The button label is not 16pt

The frame binds `Body/body-16-med`, but it **renders at ~18pt** — measured, 13% wider than 16pt
produces. The variable list and the render disagree and, per `CONTRIBUTING.md`, the measurement
wins. Built at 18pt, which lands the button at exactly 246×44 with the icon ink on 252–261,
matching the frame.

## Known metric gap — do not "fix" it

The bundled Inter renders about **3.7% narrower** than Figma at the same size — an `opsz` axis
and font-version difference. Vert Grotesk matches at ratio 1.000, so it is Inter-specific. It is
invisible in ragged-right copy. Inflating sizes to compensate would break every other page.
