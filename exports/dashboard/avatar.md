# Dashboard Avatar

## Which avatar?

| Surface | Component | Node | What it is |
|---|---|---|---|
| **Dashboard / product** | `Avatar` — this file | `1658:24023` | A generated character — coloured body + head with a face cutout. Represents **app users**. |
| Marketing web | `client/avatar` — see `exports/web/avatar.md` | `1619:722` | A grayscale squircle holding a **real photo** of a client or author. |

Never put the generated character on the website, and never put a client photo in
dashboard chrome. For client/author photos on the website, use Client Avatars.

Figma: group `avatar` (`1658:24113`), set `1658:24023`.

---

## Variant properties — 16 variants

| Property | Values |
|---|---|
| `Style` | `1`, `2`, `3` |
| `Color` | `Blue`, `Red`, `Yellow`, `Green`, `Orange` |
| `Admin` | `false`, `true` |

The declared matrix is `3 × 5 × 2` = 30 combinations, but **only 16 exist**: 15 standard
(`Style` × `Color`, `Admin=false`) plus **one** admin variant.

**Any `Admin=true` request other than `Style=1, Color=Blue` resolves to nothing.**

| Node | Variant |
|---|---|
| `1658:24024` / `24028` / `24032` | `Style=1/2/3, Color=Blue, Admin=false` |
| `1658:24036` / `24040` / `24044` | `Style=1/2/3, Color=Red, Admin=false` |
| `1658:24048` / `24052` / `24056` | `Style=1/2/3, Color=Yellow, Admin=false` |
| `1658:24060` / `24064` / `24068` | `Style=1/2/3, Color=Green, Admin=false` |
| `1658:24072` / `24076` / `24080` | `Style=1/2/3, Color=Orange, Admin=false` |
| `1658:24084` | `Style=1, Color=Blue, Admin=true` — **the only admin variant** |

## Appearance — from the component set (`1658:24024` standard, `1658:24084` admin)

**The frame is a landscape stadium, not a rounded square.** An earlier pass here described
`body rect 42×64 r4 + head rect 24×24 r4` — that is the artwork *inside* the frame, not the
component. The component itself is:

| Part | Value |
|---|---|
| frame | **64 × 48** · **`--gw-radius-80`** (clamps to a stadium on a 48-tall box) · `overflow: hidden` |
| border | **0.5px `--gw-color-neutral-100`** |
| fill | per `Color` — see the table below |

### The character, positioned inside that clip

| Part | Standard (`Style=1, Color=Blue`) |
|---|---|
| body | 42 × 64 · `--gw-radius-4` · `--gw-color-primary-300` · centred · **`top: 35.5`** |
| head | 24 × 24 · `--gw-radius-4` · `--gw-color-primary-300` · **`left: calc(50% + 9px)`** · `top: 9.5` |
| face | 14.114 × 10.713 · **rotated 24.01°** · `left: 30.5` · `top: 20.5` |

**The body starts at y=35.5 in a 48-tall box**, so only its top ~12px is visible — the clip
is what produces the head-and-shoulders read. **The head is offset 9px right of centre**,
not centred. Neither is guessable; both are load-bearing to the character's look.

Admin (`1658:24084`) replaces all three with a single 38.172 × 86.63 group at
`left: 15.5, top: 7.5`, on a `--gw-color-neutral-50` fill.

### Committed assets

The face and the admin character are drawn vectors and cannot be approximated:

| File | Use |
|---|---|
| `assets/avatar/face-vector-4.svg` | the `Vector 4` face, used by `Style=1` and `Style=2` |
| `assets/avatar/admin-character.svg` | the whole admin figure |

`Style=3` uses a different face (`Vector 6`) — **not yet harvested**.

### Fills per `Color` — two anomalies

| `Color` | Body | Background | Token reading |
|---|---|---|---|
| Blue | `#66A9FF` | `#E5F1FF` | body `primary-300`, bg **`primary-50`** |
| Red | `#FB7185` | `#FFF1F2` | body `red-300`, bg `red-25` |
| Yellow | `#FBBF24` | `#FFFBEB` | body `yellow-300`, bg `yellow-25` |
| Green | `#4ADE80` | `#F0FDF4` | body `green-300`, bg `green-25` |
| Orange | `#FB923C` | `#F1F2F3` | body `orange-300`, bg **`neutral-50`** |

Bodies are consistently the `-300` step. Backgrounds are not: **Blue uses `-50` where Red,
Yellow and Green use `-25`, and Orange abandons its own hue entirely for `neutral-50`.**
Both look unintended. Flagged, not normalised — the variants render what they render.

## Three avatar components, all stadiums

Worth stating plainly, because a circle is the natural assumption and it is wrong in all
three cases:

| Component | Size | Radius |
|---|---|---|
| `Avatar` (dashboard) | 64 × 48 | 80 |
| `client/avatar` (web) | 64 × 48 `large` | 100 |
| the avatar inside `user-card` | 42.667 × 32 | 53.333 |

Every one is a landscape pill at roughly 4:3. None is square, none is round.

## Rules

**Scope: dashboard / product only** — it represents app users.

**`Admin=true` is reserved for the owner or anyone with admin access.** Everyone else
gets a standard avatar, **assigned freely / shuffled** — the colour and style carry no
meaning, so distribute them for visual variety rather than encoding anything.

Because only `Style=1, Color=Blue` has an admin variant, an admin is always that
variant. Do not attempt to give an admin a different colour.

## Structure

```
Style=1, Color=Blue, Admin=false
COMPONENT (solid fill: #E5F1FF)
├── RECTANGLE "Rectangle 46735" (42×64, r:4, fill: #66A9FF)   ← body/torso
├── RECTANGLE "Rectangle 46736" (24×24, r:4, fill: #66A9FF)   ← head
└── VECTOR "Vector 4" (fill: #E5F1FF)                         ← face cutout

Style=1, Color=Blue, Admin=true
COMPONENT (solid fill: #F1F2F3)
└── GROUP → GROUP
    ├── RECTANGLE "Rectangle 46735" (38×59, r:4, fill: #262A2E)  ← dark body
    ├── VECTOR "Union" (fill: #262A2E)                            ← eared head shape
    └── VECTOR "Vector 4" (fill: #F1F2F3)                         ← face cutout
```

### Style differences

| Style | Body | Head | Face vector |
|---|---|---|---|
| `1` | 42×64 | 24×24 | `Vector 4` |
| `2` | 54×83 | 31×31 | `Vector 4` |
| `3` | 42×64 | 24×24 | `Vector 6` — a different expression |

`Style` 1 and 3 share proportions and differ only in expression. `Style 2` is the larger
proportion.

### Colour per variant

| Color | Body | Background | Token |
|---|---|---|---|
| `Blue` | `#66A9FF` | `#E5F1FF` | `--gw-color-primary-300` on `--gw-color-primary-50` |
| `Red` | `#FB7185` | `#FFF1F2` | `--gw-color-red-300` on `--gw-color-red-25` |
| `Yellow` | `#FBBF24` | `#FFFBEB` | `--gw-color-yellow-300` on `--gw-color-yellow-25` |
| `Green` | `#4ADE80` | `#F0FDF4` | `--gw-color-green-300` on `--gw-color-green-25` |
| `Orange` | `#FB923C` | `#F1F2F3` | `--gw-color-orange-300` on `--gw-color-neutral-50` |
| `Admin` | `#262A2E` | `#F1F2F3` | `--gw-color-neutral-900` on `--gw-color-neutral-50` |

**The Orange background is wrong in the source.** Every other colour pairs a `300` body
with its own `25` tint; Orange pairs `#FB923C` with the neutral gray `#F1F2F3` instead
of `--gw-color-orange-25` (`#FFF7ED`). This is an open finding against the Figma file —
do not "fix" it in generated output without a ruling, but be aware Orange looks
off-family.

## Where it appears

`user-card` (`2125:200`) instances it, and `dashboard-build` instances `user-card` in the
rail footer with `Admin=true`. See `section-elements.md`.
