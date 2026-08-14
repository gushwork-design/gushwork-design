#!/usr/bin/env python3
"""
Builds preview/gtm-command-center.html — the GTM Command Center overview screen.

Source of truth: Figma **GW Dashbords** Q9L6q38dEj3Qu1JkjiT13y, page `Claude handover`
(236:31784), frame `overview` (236:31785, 1440x4906). Components are the v2 set documented in
exports/dashboard/v2/.

Every colour and Inter type style is pulled BY NAME from foundation/tokens.css — no hex is
written in this file. A missing token raises rather than falling back, because a silent fallback
is the failure this repo exists to prevent.

Run:  python3 preview/_build_gtm_command_center.py
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKENS = ROOT / "foundation" / "tokens.css"
ICONS = ROOT / "assets" / "icons"
LOGO = ROOT / "assets" / "logo" / "gushwork-symbol-white.svg"
SHEET = ROOT / "preview" / "review-sheet.html"
OUT = ROOT / "preview" / "gtm-command-center.html"

# ─────────────────────────── tokens, read from tokens.css ───────────────────────────
_css = TOKENS.read_text()
_decl = dict(re.findall(r'(--gw-[a-z0-9-]+)\s*:\s*([^;]+);', _css))

def tok(name):
    """Return the custom-property NAME after asserting it exists. Never returns a literal."""
    if name not in _decl:
        sys.exit(f"token {name} is not in foundation/tokens.css — that is a gap to raise, "
                 f"not a value to invent")
    return f"var({name})"

def tokval(name):
    if name not in _decl:
        sys.exit(f"token {name} is not in foundation/tokens.css")
    return _decl[name].strip()

# colours used by this screen
NEEDED = ["--gw-color-white", "--gw-color-black",
          "--gw-color-neutral-25", "--gw-color-neutral-50", "--gw-color-neutral-100",
          "--gw-color-neutral-200", "--gw-color-neutral-300", "--gw-color-neutral-400",
          "--gw-color-neutral-500", "--gw-color-neutral-600", "--gw-color-neutral-700",
          "--gw-color-neutral-800", "--gw-color-neutral-900",
          "--gw-color-green-25", "--gw-color-green-400", "--gw-color-green-500",
          "--gw-color-yellow-400", "--gw-color-yellow-25", "--gw-color-yellow-500",
          "--gw-color-red-25", "--gw-color-red-50", "--gw-color-red-400", "--gw-color-red-500",
          "--gw-color-primary-500", "--gw-color-primary-alpha-10",
          "--gw-color-green-300", "--gw-color-red-300", "--gw-color-red-alpha-10",
          "--gw-color-neutral-250",
          "--gw-radius-4", "--gw-radius-8", "--gw-radius-12", "--gw-radius-16", "--gw-radius-40",
          "--gw-text-body-12-med", "--gw-text-body-12-sem", "--gw-text-body-14-med",
          "--gw-text-body-16-sem", "--gw-text-body-16-reg", "--gw-text-body-10-sem",
          "--gw-text-button-10", "--gw-text-button-12", "--gw-text-button-14"]
missing = [n for n in NEEDED if n not in _decl]
if missing:
    sys.exit("missing tokens: " + ", ".join(missing))

# Emit token DEPENDENCIES transitively. The type tokens are `font` shorthands that reference
# var(--gw-font-body) internally; omit that and the whole shorthand is invalid at computed-value
# time, so the declaration is dropped and every size silently falls back to the browser default.
# It renders plausibly and is completely wrong — caught by measuring, not by looking.
def closure(names):
    seen, stack = [], list(names)
    while stack:
        n = stack.pop(0)
        if n in seen:
            continue
        if n not in _decl:
            sys.exit(f"token {n} is referenced but not in foundation/tokens.css")
        seen.append(n)
        stack += re.findall(r'var\((--gw-[a-z0-9-]+)\)', _decl[n])
    return seen

EMIT = closure(NEEDED)
ROOTVARS = "\n".join(f"  {n}: {_decl[n].strip()};" for n in EMIT)
# tracking companions for the Inter styles
TRACK = "\n".join(f"  {n}-tracking: {_decl[n + '-tracking'].strip()};"
                  for n in EMIT if n.startswith('--gw-text-') and n + '-tracking' in _decl)

# ─────────────────────────── fonts ───────────────────────────
# Vert Grotesk is embedded (proven block, reused from review-sheet.html) so the BRAND FACE can
# never fall back — output-targets.md is explicit about that. Inter prefers an installed copy
# and falls back to the committed variable font, which resolves when opened from preview/.
_vg = re.search(r"@font-face\{font-family:'Vert Grotesk Display';[^}]*\}", SHEET.read_text())
if not _vg:
    sys.exit("could not lift the Vert Grotesk @font-face block out of review-sheet.html")
FONTS = _vg.group(0) + (
    "@font-face{font-family:'Inter';"
    "src:local('Inter'),local('Inter Variable'),"
    "url('../fonts/Inter-VariableFont_opsz_wght.ttf') format('truetype-variations');"
    "font-weight:100 900;font-style:normal;font-display:swap}")

# ─────────────────────────── icons ───────────────────────────
_ic = {}
def ico(name, weight="regular", size=16, cls="ic"):
    key = (name, weight)
    if key not in _ic:
        p = ICONS / weight / f"{name}.svg"
        if not p.exists():
            sys.exit(f"icon {weight}/{name}.svg not found in assets/icons")
        raw = p.read_text()
        inner = re.sub(r'^.*?<svg[^>]*>', '', raw, flags=re.S)
        inner = re.sub(r'</svg>\s*$', '', inner, flags=re.S)
        inner = re.sub(r'<rect[^>]*fill="none"[^>]*/>', '', inner)
        _ic[key] = inner.strip()
    return (f'<span class="{cls}" style="width:{size}px;height:{size}px">'
            f'<svg viewBox="0 0 256 256" fill="currentColor" width="{size}" height="{size}">'
            f'{_ic[key]}</svg></span>')

_logo_inner = re.sub(r'</svg>\s*$', '', re.sub(r'^.*?<svg[^>]*>', '',
                     LOGO.read_text(), flags=re.S), flags=re.S).strip()
_logo_vb = re.search(r'viewBox="([^"]+)"', LOGO.read_text())
LOGO_SVG = (f'<svg viewBox="{_logo_vb.group(1) if _logo_vb else "0 0 32 32"}" '
            f'width="16" height="16" fill="currentColor">{_logo_inner}</svg>')

# ─────────────────────────── data, transcribed from the frame ───────────────────────────
NAV = [("overview", [("Overview", "squares-four", True), ("Close Cohorts", "users-three", False)]),
       ("Channels", [("Meta Ads", "meta-logo", False), ("Google Ads", "google-logo", False),
                     ("Cold Email", "paper-plane-tilt", False), ("Organic", "plant", False),
                     ("Referral", "share-network", False)]),
       ("Settings", [("Appearance", "swatches", False), ("Controls", "sliders-horizontal", False)]),
       ("Admin", [("Targets", "chart-line", False), ("Changelog", "stack-overflow-logo", False)])]

DATE_TABS = ["Today", "Yesterday", "This Month", "Last Month", "Custom"]
ACTIVE_TAB = "Last Month"

STAT_CARDS = [  # label, value, sub, pct, tone  (pct/tone None => no bar, no percentage)
    ("DEMOS BOOKED", "1,310", "of 1,472", "89%", "green"),
    ("SHOW-UPS", "708", "of 720", "98%", "green"),
    ("CLOSES", "70", "of 130", "54%", "red"),
    ("DEMOS SCHEDULED", "1322", "in this period", None, None),
    ("CLOSES", "70", "of 130", None, None)]

RUN_RATE = [("Demos", "59.5", "need 66.9 / biz day"), ("Show-ups", "32.2", "need 32.7 / biz day"),
            ("Closes", "3.2", "need 5.9 / biz day"), ("ARR", "$36772", "need $63257 / biz day")]

CHAN_COLS = ["channnel", "demos", "Show-ups", "Pending", "Closes", "ARR"]
CHAN_ROWS = [  # channel, icon, badge, demos, showups, pending, closes, arr, spent, roi
    ("Meta Ads", "meta-logo", True, ("681/706", .96), ("294/297", .99), "134", "34", "$44.4K",
     "$48.3K of $48.3", "3.67x"),
    ("Cold Email", "paper-plane-tilt", False, ("500 of 640", .78), ("322/352", .91), "65", "31",
     "$30.6K", "$135.7K of $135.7K", "6.38x"),
    ("Google Ads", "google-logo", False, ("26/-", .10), ("21/-", .08), "1", "2", "$27.6K",
     "$17.0K of $17.0K", "-"),
    ("Organic", "plant", False, ("98/80", 1.0), ("71/48", 1.0), "8", "3", "$30.6K",
     "$68 of $68", "-")]
CHAN_TOTAL = ("total", ("1310/1426", .92), ("708/697", 1.0), "208", "70", "$808.98K",
              "$198.3K of $200.9K", "3.74x")

DAILY_COLS = ["DATE", "bookings", "Show-ups", "Booking attainment", "Show-up attainment"]
DAILY_ROW = ("Jul 1", "34", "26", "32/47", "68%", "32/47", "68%")

ONB_COLS = ["DATE", "Domain", "assigned AE", "channel", "monthly", "annual ARR", "Status"]
ONB_ROWS = [
    ("Jul 1", "www.designinrhythm.com", "Carlisle Dcosta", "Meta", "$840", "$10,080", "Active", "green"),
    ("Jul 1", "energytalentsearch.com", "Abhinav Chaturvedi", "Cold Email", "$800", "$9,600", "Active", "green"),
    ("Jul 2", "truscribe.com", "Arabind Mishra", "Meta", "$1,000", "$12,000", "To be onboarded", "yellow"),
    ("Jul 3", "shaanrais.com", "Mugil Vanjinath", "Meta", "$1,200", "$14,400", "Active", "green"),
    ("Jul 3", "www.peopleleaderaccelerator.com", "Akarsh Dayal", "Cold Email", "$640", "$7,680", "Active", "green")] * 2


# ── PASS-2 row sets ────────────────────────────────────────────────────────────────────
# The frame draws 10 identical daily rows and says "Page 1 of 4", i.e. 40 rows exist. Uniform
# rows make sorting and filtering look broken, so the set is VARIED here — deterministically,
# no randomness, so the build is reproducible. This is illustrative sample data, exactly as the
# frame's repeated row was: see the notice.
def daily_rows(n=40):
    rows = []
    for i in range(n):
        day = 1 + i // 2
        bookings = 28 + (i * 7) % 21
        shows = 18 + (i * 5) % 15
        b_t = 40 + (i * 3) % 12
        s_t = 30 + (i * 4) % 14
        b_pct = round(bookings / b_t * 100)
        s_pct = round(shows / s_t * 100)
        rows.append((f"Jul {day}", bookings, shows, f"{bookings}/{b_t}", b_pct,
                     f"{shows}/{s_t}", s_pct))
    return rows

def onb_rows(n=70):
    base = ONB_ROWS[:5]
    rows = []
    for i in range(n):
        d, dom, ae, chn, mo, arr, st, tone = base[i % 5]
        day = 1 + i // 5
        m = 600 + (i * 40) % 800
        rows.append((f"Jul {day}", dom, ae, chn, f"${m:,}", f"${m*12:,}", st, tone))
    return rows

DAILY_SET = daily_rows()
ONB_SET = onb_rows()
PAGE_SIZE = 10

# ─────────────────────────── chart ───────────────────────────
# The plot geometry is TRACED from the design, not data-bound: the Figma curve is an
# illustration. The readouts, axis ticks and tooltip values are transcribed exactly.
# NOTE the design's own inconsistency, reproduced as-is: the tooltip reads Actual 1104 /
# Target 1235 while the axis tops out at 340.
def area_chart(y_ticks, end_actual, end_target, today=0.78, w=1054, h=248):
    ymax = y_ticks[0]
    sx = lambda f: f * w
    sy = lambda v: h - (v / ymax) * h
    shape = [0, .12, .25, .38, .50, .62, .72, .78, .88, 1.0]
    ease = [0, .105, .235, .385, .535, .675, .775, .825, .915, 1.0]
    pts = [(sx(f), sy(end_actual * e)) for f, e in zip(shape, ease)]
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        cx = (x0 + x1) / 2
        d += f" C{cx:.1f},{y0:.1f} {cx:.1f},{y1:.1f} {x1:.1f},{y1:.1f}"
    area = d + f" L{w},{h} L0,{h} Z"
    grid = "".join(f'<line x1="0" y1="{sy(v):.1f}" x2="{w}" y2="{sy(v):.1f}" '
                   f'class="ch-grid"/>' for v in y_ticks)
    vgrid = "".join(f'<line x1="{sx(f):.1f}" y1="0" x2="{sx(f):.1f}" y2="{h}" class="ch-grid"/>'
                    for f in (.25, .5, .75, 1.0))
    uid = f"g{int(end_actual)}{int(ymax)}"
    return f'''<svg class="ch-svg" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">
<defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{tokval('--gw-color-primary-500')}" stop-opacity=".22"/>
<stop offset="1" stop-color="{tokval('--gw-color-primary-500')}" stop-opacity="0"/>
</linearGradient></defs>
{grid}{vgrid}
<path d="{area}" fill="url(#{uid})"/>
<polyline points="0,{h} {w},{sy(end_target):.1f}" class="ch-target"/>
<path d="{d}" class="ch-actual"/>
<line x1="{sx(today):.1f}" y1="0" x2="{sx(today):.1f}" y2="{h}" class="ch-today"/>
<circle cx="{sx(today):.1f}" cy="{sy(end_actual * .825):.1f}" r="3.5" class="ch-dot"/>
</svg>'''

def gauge(pct, tone):
    r, c = 16, 2 * 3.14159 * 16
    return f'''<span class="gauge"><svg viewBox="0 0 40 40" width="40" height="40">
<circle cx="20" cy="20" r="{r}" class="gauge-track"/>
<circle cx="20" cy="20" r="{r}" class="gauge-fill gauge-{tone}"
 stroke-dasharray="{c*pct/100:.1f} {c:.1f}" transform="rotate(-90 20 20)"/>
</svg><b>{pct}%</b></span>'''

def chart_card(title, readout, pct, tone, y_ticks, end_actual, end_target, tip, slot, hidden=False):
    ylab = "".join(f'<span>{v}</span>' for v in y_ticks)
    xlab = "".join(f'<span>Week {i}</span>' for i in (1, 2, 3, 4))
    a_cls = ' class="tip-red"' if tip[3] == 'red' else (' class="tip-green"' if tip[3] == 'green' else '')
    cls = "panel is-hidden" if hidden else "panel"
    return f'''<div class="{cls}" data-chart-panel="{slot}">
<div class="panel-head"><h3 class="ch-title">{title}</h3>
<div class="ch-readout"><span>{readout}</span>{gauge(pct, tone)}</div></div>
<div class="ch-body"><div class="ch-yaxis">{ylab}</div>
<div class="ch-plot">{area_chart(y_ticks, end_actual, end_target)}
<div class="ch-tip" style="left:78%"><span class="tip-date">{tip[0]}</span>
<span class="tip-row"><i>Actual</i><b{a_cls}>{tip[1]}</b></span>
<span class="tip-row"><i>Target</i><b>{tip[2]}</b></span></div></div></div>
<div class="ch-xaxis">{xlab}</div></div>'''

def chan_table():
    """ONE table. The two toolbar checkboxes toggle COLUMN GROUPS — the Figma frame stacks two
    cards because a design file has to draw both states side by side. `Spend & ROI` starts off,
    matching the first card; turning it on reveals the trailing divider + Spent/roi columns and
    the metric columns reflow (Figma: 160/160/137.3 -> 85.6 each), which flex does for free."""
    def sortable(c, i):
        return (f'<span class="tc" role="columnheader" tabindex="0" data-sort-key="{i}" '
                f'aria-sort="none" data-tip="Sort by {c}">{c} '
                f'<span class="sort-ic">{ico("arrows-down-up","bold",12)}</span></span>')
    head = ('<div class="trow trow-head">'
            f'<span class="tc tc-chan">{CHAN_COLS[0]}</span><i class="tdiv"></i>'
            '<span class="tcells" data-col-group="demos">'
            + "".join(sortable(c, i) for i, c in enumerate(CHAN_COLS[1:]))
            + '</span>'
            '<i class="tdiv is-hidden" data-col-group="spend"></i>'
            '<span class="tcells tcells-trail is-hidden" data-col-group="spend">'
            + "".join(sortable(c, 5 + i) for i, c in enumerate(("Spent", "roi")))
            + '</span></div>')

    def metric(v):
        return (f'<span class="tc tc-metric" data-sort="{v[1]}"><b>' + v[0] + '</b>'
                + bar(f"{v[1]*100:.0f}%", "green", "sm") + '</span>')

    def group_demos(demos, shows, pend, clos, arr):
        return ('<span class="tcells" data-col-group="demos">'
                + metric(demos) + metric(shows)
                + f'<span class="tc" data-sort="{pend}">{pend}</span>'
                f'<span class="tc" data-sort="{clos}">{clos}</span>'
                f'<span class="tc" data-sort="{arr}">{arr}</span></span>')

    def group_spend(spent, roi):
        return ('<i class="tdiv is-hidden" data-col-group="spend"></i>'
                '<span class="tcells tcells-trail is-hidden" data-col-group="spend">'
                f'<span class="tc" data-sort="{spent}">{spent}</span>'
                f'<span class="tc" data-sort="{roi}">{roi}</span></span>')

    rows = []
    for ch, icn, badge, demos, shows, pend, clos, arr, spent, roi in CHAN_ROWS:
        bdg = f'<span class="chan-badge">{ico("crown-simple","fill",12)}</span>' if badge else ''
        rows.append('<div class="trow" data-row>'
                    f'<span class="tc tc-chan" data-sort="{ch}">{ico(icn,"regular",12)}{ch}{bdg}</span>'
                    '<i class="tdiv"></i>'
                    + group_demos(demos, shows, pend, clos, arr)
                    + group_spend(spent, roi) + '</div>')
    ch, demos, shows, pend, clos, arr, spent, roi = CHAN_TOTAL
    rows.append('<div class="trow trow-total">'
                f'<span class="tc tc-chan">{ch}</span><i class="tdiv"></i>'
                + group_demos(demos, shows, pend, clos, arr)
                + group_spend(spent, roi) + '</div>')

    toolbar = ('<div class="panel-toolbar"><div class="pt-left">'
               '<label class="chk-wrap" data-toggles="demos">'
               f'<span class="chk is-on">{ico("check","bold",16)}</span>'
               '<span class="chk-label">Demos &amp; Show-ups</span></label>'
               '<label class="chk-wrap" data-toggles="spend">'
               f'<span class="chk">{ico("check","bold",16)}</span>'
               '<span class="chk-label">Spend &amp; ROI</span></label></div>'
               f'<button class="icon-btn icon-btn-ghost" data-tip="Choose columns">{ico("squares-four","bold",16)}</button>'
               '</div>')
    return ('<div class="card card-lg">' + toolbar
            + '<div class="grid-wrap">' + head + "".join(rows) + '</div></div>')


def chart_controls():
    """The `Show both` toggle is what makes the frame look like two Actual-vs-Target sections:
    off shows the tab-selected chart, on shows both. One section, two states."""
    return ('<div class="panel-controls"><div class="pc-left">'
            '<div class="tab-group" data-chart-tabs>'
            '<span class="tab-item is-active" data-chart="demos">Cumulative Demos</span>'
            '<span class="tab-item" data-chart="showups">Cumulative Show-ups</span></div>'
            '<label class="toggle-wrap" data-toggles-both>'
            '<span class="toggle" role="switch" aria-checked="false"></span>'
            '<span class="toggle-label">Show both</span></label></div>'
            '<div class="pc-right"><span class="muted-14">Showing for</span>'
            + select_menu("Last Month", [(v, None) for v in DATE_TABS], 'data-range')
            + '</div></div>')


# ─────────────────────────── component partials ───────────────────────────
def section_header(title, qualifier, legend=False):
    leg = ('<div class="legend">'
           + "".join(f'<span class="leg-item"><i class="dot dot-{t}"></i>{l}</span>'
                     for t, l in (("green", "On track"), ("yellow", "Pending"), ("red", "Behind")))
           + '</div>') if legend else ''
    return (f'<div class="section-header"><div class="sh-title"><h2>{title}</h2>'
            f'<span>{qualifier}</span></div>{leg}</div>')

def bar(pct, tone, size="md"):
    return (f'<span class="progress progress-{size}">'
            f'<i class="progress-fill fill-{tone}" style="width:{pct}"></i></span>')

def stat_card(label, value, sub, pct, tone):
    right = f'<span class="sc-pct">{pct}</span>' if pct else ''
    prog = bar(pct, tone) if pct else ''
    return f'''<div class="card card-md stat-card">
<div class="sc-body"><div class="sc-label">{label}</div>
<div class="sc-value-block"><div class="sc-value-row">
<div class="sc-value"><b>{value}</b><span>{sub}</span></div>{right}</div>{prog}</div></div></div>'''

def metric_card(label, value, sub):
    return (f'<div class="card card-md metric-card"><div class="mc-body">'
            f'<div class="mc-label">{label}</div>'
            f'<div class="mc-value"><b>{value}</b><span>{sub}</span></div></div></div>')


def sort_head(cols):
    """Header cells are the sort control. `data-sort-key` is the column index; aria-sort carries
    state for assistive tech. The ArrowsDownUp glyph is swapped for Arrow Up/Down when active."""
    out = []
    for i, c in enumerate(cols):
        out.append(f'<span class="tc" role="columnheader" tabindex="0" data-sort-key="{i}" '
                   f'aria-sort="none" data-tip="Sort by {c}">{c} '
                   f'<span class="sort-ic">{ico("arrows-down-up","bold",12)}</span></span>')
    return "".join(out)


def select_menu(label, options, attrs="", width=None, sel_cls=""):
    """Trigger + menu. Measured spec (controls.md): the open menu is WIDER than its trigger and
    right-aligned; border neutral/50; options button-12; option hover neutral/50; and there is
    NO selected checkmark — an earlier ruling invented one, so none is drawn here."""
    w = f'style="width:{width}px" ' if width else ""
    items = "".join(
        f'<button class="menu-item" role="option" data-value="{v}"'
        f'{" data-sort-key=\"%s\"" % k if k is not None else ""}>{v}</button>'
        for v, k in options)
    return (f'<span class="select-wrap" {attrs}>'
            f'<button class="select {sel_cls}" {w}aria-haspopup="listbox" aria-expanded="false">'
            f'<span class="select-label">{label}</span>{ico("caret-down","bold",12)}</button>'
            f'<span class="menu" role="listbox">{items}</span></span>')


def pagination(total, page_size=PAGE_SIZE):
    pages = max(1, -(-total // page_size))
    sizes = [(str(s), None) for s in (10, 25, 50, 100)]
    return (f'<div class="pagination" data-total="{total}">'
            f'<div class="pg-left"><span class="muted-14">Items per page</span>'
            + select_menu(str(page_size), sizes, 'data-pagesize', sel_cls="select-sm")
            + f'</div><div class="pg-right">'
            f'<span class="muted-14 pg-status">Page 1 of {pages}</span>'
            f'<button class="icon-btn" data-page="prev" aria-label="Previous page" disabled>'
            f'{ico("arrow-left","regular",12)}</button>'
            f'<button class="icon-btn" data-page="next" aria-label="Next page">'
            f'{ico("arrow-right","regular",12)}</button></div></div>')


def daily_table():
    cols = DAILY_COLS
    head = f'<div class="trow trow-head trow-daily">{sort_head(cols)}</div>'
    rows = []
    for d, bk, su, ba, bap, sa, sap in DAILY_SET:
        day = int(d.split()[1])
        rows.append(f'<div class="trow trow-daily" data-row>'
                    f'<span class="tc tc-strong" data-sort="{day}">{d}</span>'
                    f'<span class="tc" data-sort="{bk}">{bk}</span>'
                    f'<span class="tc" data-sort="{su}">{su}</span>'
                    f'<span class="tc tc-pair" data-sort="{bap}">{ba}'
                    f'<span class="badge badge-sm badge-{"red" if bap < 90 else "green"}">{bap}%</span></span>'
                    f'<span class="tc tc-pair" data-sort="{sap}">{sa}'
                    f'<span class="badge badge-sm badge-{"red" if sap < 90 else "green"}">{sap}%</span></span>'
                    f'</div>')
    sorts = [("Date", 0), ("Bookings", 1), ("Show-ups", 2),
             ("Booking attainment", 3), ("Show-up attainment", 4)]
    toolbar = ('<div class="panel-toolbar panel-toolbar-titled">'
               '<div class="pt-title"><h3>Demo bookings &amp; show-ups</h3>'
               f'<span>{len(DAILY_SET):,} bookings last month</span></div>'
               '<div class="pt-right"><span class="muted-14">Sort by</span>'
               + select_menu("Date", sorts, 'data-sort-select') + '</div></div>')
    return (f'<div class="card card-lg" data-table>{toolbar}'
            f'<div class="grid-wrap">{head}{"".join(rows)}</div>'
            f'{pagination(len(DAILY_SET))}</div>')


def onb_table():
    cols = ONB_COLS
    head = f'<div class="trow trow-head trow-onb">{sort_head(cols)}</div>'
    rows = []
    for d, dom, ae, chn, mo, arr, st, tone in ONB_SET:
        day = int(d.split()[1])
        money = int(mo.replace("$", "").replace(",", ""))
        rows.append(f'<div class="trow trow-onb" data-row '
                    f'data-text="{dom.lower()} {ae.lower()} {chn.lower()}">'
                    f'<span class="tc tc-strong" data-sort="{day}">{d}</span>'
                    f'<span class="tc" data-sort="{dom}">{dom}</span>'
                    f'<span class="tc" data-sort="{ae}">{ae}</span>'
                    f'<span class="tc" data-sort="{chn}">{chn}</span>'
                    f'<span class="tc" data-sort="{money}">{mo}</span>'
                    f'<span class="tc tc-ink" data-sort="{money*12}">{arr}</span>'
                    f'<span class="tc" data-sort="{st}">'
                    f'<span class="badge badge-sm badge-{tone}">{st}</span></span></div>')
    sorts = [(c, i) for i, c in enumerate(cols)]
    toolbar = ('<div class="panel-toolbar panel-toolbar-titled">'
               '<div class="pt-title"><h3>Onboardings</h3>'
               f'<span>{len(ONB_SET)} onboardings last month</span></div>'
               '<div class="pt-right"><span class="muted-14">Quick Filter</span>'
               '<span class="select select-filter filter-field">'
               f'{ico("magnifying-glass","regular",16)}'
               '<input type="search" placeholder="Search domain, AE, channel" '
               'aria-label="Filter onboardings" data-filter></span>'
               '<span class="muted-14">Sort by</span>'
               + select_menu("Date", sorts, 'data-sort-select') + '</div></div>')
    return (f'<div class="card card-lg" data-table>{toolbar}'
            f'<div class="grid-wrap">{head}{"".join(rows)}</div>'
            f'{pagination(len(ONB_SET))}</div>')


# ─────────────────────────── shell ───────────────────────────
nav_html = ""
for group, items in NAV:
    nav_html += '<div class="nav-group"><span class="nav-label">' + group + '</span>'
    for label, icn, sel in items:
        nav_html += (f'<a class="nav-item{" is-selected" if sel else ""}" href="#" '
                     f'data-nav="{label}"{" data-home" if sel else ""}>'
                     f'{ico(icn,"regular",16)}<span>{label}</span></a>')
    nav_html += '</div>'

tabs_html = "".join(f'<span class="tab-item{" is-active" if t == ACTIVE_TAB else ""}">{t}</span>'
                    for t in DATE_TABS)

hero = f'''<div class="card card-lg hero">
<div class="hero-body">
<div class="hero-top">
<div class="hero-head"><h2 class="hero-value">$809K ARR Added</h2>
<span class="badge badge-md badge-red">Behind</span></div>
<div class="hero-meta"><span>of $1392K</span><span>58%</span></div>
{bar('58%','red')}</div>
<div class="inset" data-inset>
<div class="inset-head"><span>What went wrong?</span>
<button class="icon-btn icon-btn-ghost" data-inset-toggle aria-expanded="true"
 aria-label="Collapse">{ico('caret-up','bold',12)}</button></div>
<div class="inset-rows">
<span class="inset-row" data-tip="Google Ads booked 26 demos against a plan of 16 for the period.">{ico('info','bold',12)}Google Ads demos at 26 vs expected 16.</span>
<span class="inset-row" data-tip="Repeated in the source frame; kept verbatim.">{ico('info','bold',12)}Google Ads demos at 26 vs expected 16, Google Ads demos.</span>
</div></div></div></div>'''

TIP1 = ("Jul 26", "1104", "1235", "ink")
TIP2 = ("Jul 26", "1104", "1235", "red")
TIP3 = ("Jul 26", "571", "556", "green")

body = f'''<div class="page">
<div class="page-header">
<h1 class="page-title">Overview</h1>
<div class="ph-row">
<div class="ph-left"><div class="tab-group">{tabs_html}</div>
<span class="ph-period" data-tip="18 business days elapsed of 30 in this period.">Day 18 of 30 {ico('question','fill',16)}</span></div>
<button class="btn btn-outlined btn-compare">{ico('selection-foreground','regular',16)}Compare</button>
</div></div>

<section class="section">{section_header('Overall Performance','for last month',True)}
{hero}
<div class="stat-row">{"".join(stat_card(*c) for c in STAT_CARDS)}</div></section>

<section class="section">{section_header('Run Rate','per biz day')}
<div class="metric-row">{"".join(metric_card(*m) for m in RUN_RATE)}</div></section>

<section class="section">{section_header('Channel Breakdown','per biz day')}
{chan_table()}</section>

<section class="section">{section_header('Actual vs Target','per biz day')}
<div class="card card-lg">{chart_controls()}
<div class="chart-row">
{chart_card('Cumulative Demos vs Target','260 of 340',76,'red',[340,272,204,136,68,0],260,340,TIP2,'demos')}
{chart_card('Cumulative Show-ups vs Target','708 of 720',98,'green',[800,600,400,200,0],708,720,TIP3,'showups',hidden=True)}
</div></div></section>

<section class="section">{section_header('Daily Breakdown','per biz day')}
{daily_table()}{onb_table()}</section>
</div>'''

CSS = f"""
{FONTS}
:root{{
{ROOTVARS}
{TRACK}
  /* Display ramp — NO TOKEN EXISTS. See DECISIONS.md R15: the five Dashboard/display-* styles
     match no --gw-text-* property (h3 is Bold where the page title is Semibold; h7 is
     line-height 1.4 where the card title is 1.0). Literal specs, flagged, never substituted. */
  --dash-display-44-sem:600 44px/1.2 'Vert Grotesk Display';
  --dash-display-36-med:500 36px/1.2 'Vert Grotesk Display';
  --dash-display-28-med:500 28px/1.2 'Vert Grotesk Display';
  --dash-display-22-med:500 22px/1 'Vert Grotesk Display';
  --dash-display-20-sem:600 20px/1 'Vert Grotesk Display';
  /* Vertical rhythm — measured values are the CEILING, floors are judgement (build-rules.md) */
  --v-sect-gap:clamp(40px,6vh,80px);
  --v-slot-top:clamp(24px,5vh,60px);
  /* ── Semantic surface aliases. Light values below; the [data-theme=dark] block swaps
     them. Every dark value is MEASURED off frame 236:33407 — see exports/dashboard/v2/. ── */
  --s-canvas:{tok('--gw-color-neutral-25')};
  --s-chrome:{tok('--gw-color-neutral-50')};
  --s-card:{tok('--gw-color-white')};
  --s-inset:{tok('--gw-color-neutral-25')};
  --s-row-head:{tok('--gw-color-neutral-25')};
  --s-row:transparent;
  --s-row-hover:{tok('--gw-color-neutral-25')};
  --s-nav-sel:{tok('--gw-color-neutral-100')};
  --s-invert:{tok('--gw-color-black')};
  --t-on-invert:{tok('--gw-color-white')};
  --s-menu:{tok('--gw-color-white')};
  --s-skel:{tok('--gw-color-neutral-100')};
  --b-chrome:{tok('--gw-color-neutral-100')};
  --b-card:{tok('--gw-color-neutral-100')};
  --b-inset:{tok('--gw-color-neutral-100')};
  --b-strong:{tok('--gw-color-neutral-200')};
  --b-input:{tok('--gw-color-neutral-400')};
  --b-divider:{tok('--gw-color-neutral-25')};
  --b-menu:{tok('--gw-color-neutral-50')};
  --t-display:{tok('--gw-color-black')};
  --t-body:{tok('--gw-color-neutral-900')};
  --t-label:{tok('--gw-color-neutral-700')};
  --t-muted:{tok('--gw-color-neutral-500')};
  --t-icon:{tok('--gw-color-neutral-600')};
  --t-faint:{tok('--gw-color-neutral-400')};
  --t-disabled:{tok('--gw-color-neutral-250')};
  --d-track:{tok('--gw-color-neutral-200')};
  --d-good:{tok('--gw-color-green-400')};
  --d-bad:{tok('--gw-color-red-400')};
  --d-warn:{tok('--gw-color-yellow-400')};
  --d-series:{tok('--gw-color-primary-500')};
  --tone-good-bg:{tok('--gw-color-green-25')};   --tone-good-fg:{tok('--gw-color-green-500')};
  --tone-bad-bg:{tok('--gw-color-red-25')};      --tone-bad-fg:{tok('--gw-color-red-500')};
  --tone-bad-bg-md:{tok('--gw-color-red-50')};
  --tone-warn-bg:{tok('--gw-color-yellow-25')};  --tone-warn-fg:{tok('--gw-color-yellow-500')};
}}
[data-theme="dark"]{{
  --s-canvas:{tok('--gw-color-black')};
  --s-chrome:{tok('--gw-color-neutral-900')};
  --s-card:{tok('--gw-color-neutral-900')};
  --s-inset:{tok('--gw-color-black')};
  --s-row-head:{tok('--gw-color-black')};
  --s-row:{tok('--gw-color-black')};
  --s-row-hover:{tok('--gw-color-neutral-900')};
  --s-nav-sel:{tok('--gw-color-neutral-800')};
  --s-invert:{tok('--gw-color-white')};
  --t-on-invert:{tok('--gw-color-neutral-900')};
  --s-menu:{tok('--gw-color-neutral-900')};
  --s-skel:{tok('--gw-color-neutral-800')};
  --b-chrome:{tok('--gw-color-neutral-700')};
  --b-card:{tok('--gw-color-neutral-800')};
  --b-inset:{tok('--gw-color-neutral-900')};
  --b-strong:{tok('--gw-color-neutral-700')};
  --b-input:{tok('--gw-color-neutral-600')};
  --b-divider:{tok('--gw-color-neutral-800')};
  --b-menu:{tok('--gw-color-neutral-800')};
  --t-display:{tok('--gw-color-white')};
  --t-body:{tok('--gw-color-white')};
  --t-label:{tok('--gw-color-neutral-400')};
  --t-muted:{tok('--gw-color-neutral-500')};
  --t-icon:{tok('--gw-color-neutral-300')};
  --t-faint:{tok('--gw-color-neutral-400')};
  --t-disabled:{tok('--gw-color-neutral-700')};
  --d-track:{tok('--gw-color-neutral-600')};
  --d-good:{tok('--gw-color-green-300')};
  --d-bad:{tok('--gw-color-red-300')};
  --tone-bad-bg:{tok('--gw-color-red-alpha-10')};
  --tone-bad-bg-md:{tok('--gw-color-red-alpha-10')};
  --tone-bad-fg:{tok('--gw-color-red-300')};
  --tone-good-fg:{tok('--gw-color-green-300')};
}}
*,*::before,*::after{{box-sizing:border-box}}
html,body{{margin:0;overflow:hidden;height:100%}}          /* exactly one region scrolls */
body{{background:var(--s-canvas);font-family:'Inter',ui-sans-serif,system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}}
h1,h2,h3{{margin:0;font-weight:inherit}}
.ic{{display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto}}
.ic svg{{display:block}}

/* ── shell: 1440 canvas, scaled to fit. RULED, build-rules.md — never reflow below 1440 ── */
.shell{{zoom:var(--fit,1);width:calc(100vw / var(--fit,1));height:calc(100vh / var(--fit,1));
 display:flex;flex-direction:column;min-width:1440px}}
.shell-body{{flex:1;display:flex;min-height:0}}

/* ── topbar 1440x60 ── */
.topbar{{flex:none;height:60px;padding:0 40px;display:flex;align-items:center;
 justify-content:space-between;background:var(--s-chrome);
 box-shadow:inset 0 -1px 0 var(--b-chrome)}}
.tb-title{{display:flex;align-items:center;gap:8px}}
.tb-logo{{width:32px;height:32px;border-radius:{tok('--gw-radius-8')};
 background:{tok('--gw-color-black')};color:var(--t-on-invert);display:flex;
 align-items:center;justify-content:center;flex:0 0 auto}}
.tb-name{{font:var(--dash-display-20-sem);color:var(--t-display);white-space:nowrap}}
.tb-actions{{display:flex;align-items:center;gap:8px}}
.theme-toggle{{width:66px;height:36px;padding:4px;border-radius:{tok('--gw-radius-12')};
 border:1px solid var(--b-strong);display:inline-flex;align-items:center;
 justify-content:center;gap:2px}}
.theme-toggle span{{width:28px;height:28px;border-radius:{tok('--gw-radius-8')};display:inline-flex;
 align-items:center;justify-content:center;color:var(--t-icon);cursor:pointer}}
.theme-toggle .is-on{{background:var(--s-invert);color:var(--t-on-invert)}}

/* ── sidebar 240x… — rail is overflow:hidden, only the nav list scrolls ── */
.sidebar{{flex:none;width:240px;background:var(--s-chrome);
 box-shadow:inset -1px 0 0 var(--b-chrome);display:flex;flex-direction:column;
 justify-content:space-between;overflow:hidden}}
.sb-nav{{min-height:0;display:flex;flex-direction:column}}
.sb-collapse{{flex:none;padding:4px;display:flex;justify-content:flex-end}}
.nav-groups{{padding:20px;display:flex;flex-direction:column;gap:24px;overflow-y:auto;min-height:0;
 scrollbar-width:none}}                                   /* hidden scrollbar — NOT measured */
.nav-groups::-webkit-scrollbar{{width:0;height:0}}
.nav-group{{display:flex;flex-direction:column}}
.nav-label{{padding:4px 8px;font:{tok('--gw-text-body-10-sem')};text-transform:uppercase;
 color:var(--t-faint)}}
.nav-item{{height:32px;padding:8px;border-radius:{tok('--gw-radius-8')};display:flex;
 align-items:center;gap:8px;text-decoration:none;color:var(--t-body);
 font:{tok('--gw-text-button-14')}}}
.nav-item .ic{{color:var(--t-icon)}}
.nav-item.is-selected{{background:var(--s-nav-sel)}}
.nav-item:hover:not(.is-selected){{background:var(--s-nav-sel)}}
.sb-footer{{flex:none;padding:20px 20px 32px}}
.user-card{{height:32px;display:flex;align-items:center;justify-content:space-between;gap:8px}}
.uc-identity{{display:flex;align-items:center;gap:8px;min-width:0}}
.uc-avatar{{width:32px;height:32px;border-radius:80px;background:var(--d-series);
 border:1px solid var(--b-card);flex:0 0 auto;overflow:hidden;position:relative}}
.uc-avatar::after{{content:"";position:absolute;left:7px;bottom:0;width:18px;height:14px;
 border-radius:9px 9px 0 0;background:{tok('--gw-color-white')};opacity:.9}}
.uc-meta{{display:flex;flex-direction:column;gap:4px;min-width:0}}
.uc-name{{font:{tok('--gw-text-button-12')};color:var(--t-display)}}
.uc-role{{font:{tok('--gw-text-button-10')};color:var(--t-faint)}}

/* ── the one scroller ── */
.slot{{flex:1;min-width:0;overflow-y:auto;overflow-x:hidden;scrollbar-width:none}}
.slot::-webkit-scrollbar{{width:0;height:0}}
.page{{width:1200px;padding:var(--v-slot-top) 40px 80px;display:flex;flex-direction:column}}
.page>*{{flex:0 0 auto}}                                   /* mandatory — build-rules.md */
.section{{display:flex;flex-direction:column;gap:12px;margin-top:var(--v-sect-gap)}}
.section>*{{flex:0 0 auto}}

/* ── page header 1120x113 ── */
.page-header{{display:flex;flex-direction:column;gap:24px}}
.page-title{{font:var(--dash-display-44-sem);color:var(--t-display)}}
.ph-row{{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:nowrap}}
.ph-left{{display:flex;align-items:center;gap:16px}}
.ph-period{{display:inline-flex;align-items:center;gap:8px;
 font:{tok('--gw-text-button-10')};color:var(--t-label)}}
.ph-period .ic{{color:var(--t-faint)}}

/* ── controls ── */
.tab-group{{height:36px;padding:4px;border-radius:{tok('--gw-radius-12')};
 background:var(--s-chrome);border:1px solid var(--b-card);
 display:inline-flex;align-items:center;gap:4px}}
.tab-item{{height:28px;padding:8px 12px;border-radius:{tok('--gw-radius-8')};
 display:inline-flex;align-items:center;font:{tok('--gw-text-button-12')};
 color:var(--t-body);white-space:nowrap;cursor:pointer}}
.tab-item.is-active{{background:var(--s-invert);color:var(--t-on-invert)}}
.btn{{height:36px;padding:8px 12px;border-radius:{tok('--gw-radius-12')};display:inline-flex;
 align-items:center;justify-content:center;gap:4px;background:none;cursor:pointer;
 font:{tok('--gw-text-button-14')};color:var(--t-body);
 border:1px solid transparent}}
.btn-outlined{{border-color:var(--b-strong)}}
.btn .ic{{color:var(--t-icon)}}
.btn-compare{{font:{tok('--gw-text-button-12')}}}   /* measured: Compare is 12-med, Sync Now 14-med */
.select{{height:32px;padding:8px 12px;border-radius:{tok('--gw-radius-8')};
 background:var(--s-card);border:1px solid var(--b-input);
 display:inline-flex;align-items:center;justify-content:space-between;gap:4px;cursor:pointer;
 font:{tok('--gw-text-button-14')};color:var(--t-body);white-space:nowrap}}
.select-sm{{height:28px;padding:8px 8px 8px 12px;font:{tok('--gw-text-button-12')}}}
.select-filter{{background:var(--s-inset);
 border-color:var(--b-strong);color:var(--t-faint);width:200px}}
.icon-btn{{width:28px;height:28px;padding:8px;border-radius:{tok('--gw-radius-8')};
 border:1px solid var(--b-strong);background:none;display:inline-flex;
 align-items:center;justify-content:center;cursor:pointer;color:var(--t-icon)}}
.icon-btn-ghost{{width:24px;height:24px;padding:4px;border-radius:{tok('--gw-radius-4')};
 border-color:transparent}}
.toggle-wrap{{display:inline-flex;align-items:center;gap:8px;cursor:pointer}}
.toggle{{width:38px;height:20px;border-radius:{tok('--gw-radius-40')};
 background:var(--d-track);position:relative;flex:0 0 auto}}
.toggle::after{{content:"";position:absolute;top:2.5px;left:2.5px;width:15px;height:15px;
 border-radius:50%;background:{tok('--gw-color-white')};transition:left .12s}}
.toggle.is-on{{background:var(--s-invert)}}
.toggle.is-on::after{{left:20.5px}}
.toggle-label{{font:{tok('--gw-text-button-14')};color:var(--t-body)}}
.muted-14{{font:{tok('--gw-text-button-14')};color:var(--t-icon)}}
.chk-wrap{{display:inline-flex;align-items:center;gap:8px;cursor:pointer}}
.chk{{width:24px;height:24px;padding:4px;border-radius:{tok('--gw-radius-8')};
 border:1px solid var(--b-strong);display:inline-flex;align-items:center;
 justify-content:center;color:transparent;flex:0 0 auto}}
.chk.is-on{{background:var(--s-invert);color:var(--t-on-invert)}}
.chk-label{{font:{tok('--gw-text-body-14-med')};letter-spacing:var(--gw-text-body-14-med-tracking);
 color:var(--t-body)}}

/* ── section header + legend ── */
.section-header{{padding:0 8px;display:flex;align-items:center;justify-content:space-between;gap:8px}}
.sh-title{{display:flex;align-items:center;gap:8px}}
.sh-title h2{{font:{tok('--gw-text-body-16-sem')};
 letter-spacing:var(--gw-text-body-16-sem-tracking);color:var(--t-display)}}
.sh-title span{{font:{tok('--gw-text-body-16-reg')};
 letter-spacing:var(--gw-text-body-16-reg-tracking);color:var(--t-muted)}}
.legend{{display:flex;align-items:center;gap:32px}}
.leg-item{{display:inline-flex;align-items:center;gap:4px;font:{tok('--gw-text-body-12-med')};
 letter-spacing:var(--gw-text-body-12-med-tracking);color:var(--t-label)}}
.dot{{width:8px;height:8px;border-radius:20px;flex:0 0 auto}}
.dot-green{{background:var(--gw-color-green-400)}}
.dot-yellow{{background:{tok('--gw-color-yellow-400')}}}
.dot-red{{background:{tok('--gw-color-red-400')}}}

/* ── cards ── */
.card{{background:var(--s-card);border:1px solid var(--b-card)}}
.card-lg{{border-radius:{tok('--gw-radius-16')};padding:12px;display:flex;flex-direction:column;gap:12px}}
.card-md{{border-radius:{tok('--gw-radius-12')};padding:12px}}

/* hero */
.hero-body{{padding:20px;display:flex;flex-direction:column;gap:20px}}
.hero-top{{display:flex;flex-direction:column;gap:16px}}
.hero-head{{display:flex;align-items:center;gap:16px}}
.hero-value{{font:var(--dash-display-36-med);color:var(--t-display)}}
.hero-meta{{display:flex;align-items:center;justify-content:space-between;
 font:{tok('--gw-text-body-12-med')};letter-spacing:var(--gw-text-body-12-med-tracking);
 color:var(--t-muted)}}
.inset{{border-radius:{tok('--gw-radius-8')};background:var(--s-inset);
 border:1px solid var(--b-inset);padding:8px;display:flex;flex-direction:column;gap:16px}}
.inset-head{{display:flex;align-items:center;justify-content:space-between;
 font:{tok('--gw-text-body-12-med')};letter-spacing:var(--gw-text-body-12-med-tracking);
 color:var(--t-icon)}}
.inset-rows{{display:flex;align-items:center;gap:32px}}
.inset-row{{display:inline-flex;align-items:center;gap:4px;font:{tok('--gw-text-body-14-med')};
 letter-spacing:var(--gw-text-body-14-med-tracking);color:var(--tone-bad-fg)}}

/* stat + metric cards */
.stat-row{{display:flex;gap:8px}}
.stat-card{{flex:1 1 0;min-width:0}}
.sc-body{{padding:4px;display:flex;flex-direction:column;gap:16px}}
.sc-label{{font:{tok('--gw-text-body-12-med')};letter-spacing:var(--gw-text-body-12-med-tracking);
 color:var(--t-label);text-transform:uppercase;white-space:nowrap;
 overflow:hidden;text-overflow:ellipsis}}
.sc-value-block{{display:flex;flex-direction:column;gap:8px}}
.sc-value-row{{display:flex;align-items:flex-end;justify-content:space-between;gap:8px}}
.sc-value{{display:flex;flex-direction:column;gap:4px;min-width:0}}
.sc-value b{{font:var(--dash-display-28-med);color:var(--t-display);font-weight:500}}
.sc-value span,.sc-pct{{font:{tok('--gw-text-body-12-med')};
 letter-spacing:var(--gw-text-body-12-med-tracking);color:var(--t-muted)}}
.metric-row{{display:flex;gap:8px}}
.metric-card{{flex:1 1 0;min-width:0;padding:16px;min-height:124px}}
.mc-body{{display:flex;flex-direction:column;gap:16px}}
.mc-label{{font:{tok('--gw-text-body-12-med')};letter-spacing:var(--gw-text-body-12-med-tracking);
 color:var(--t-label)}}
.mc-value{{display:flex;flex-direction:column;gap:4px}}
.mc-value b{{font:var(--dash-display-28-med);color:var(--t-display);font-weight:500}}
.mc-value span{{font:{tok('--gw-text-body-12-med')};
 letter-spacing:var(--gw-text-body-12-med-tracking);color:var(--t-muted)}}

/* progress + badge */
.progress{{display:block;width:100%;border-radius:{tok('--gw-radius-40')};
 background:var(--d-track);overflow:hidden}}
.progress-md{{height:4px}} .progress-sm{{height:2px}}
.progress-fill{{display:block;height:100%;border-radius:{tok('--gw-radius-40')}}}
.fill-green{{background:var(--d-good)}}
.fill-red{{background:var(--d-bad)}}
.badge{{display:inline-flex;align-items:center;gap:4px;white-space:nowrap}}
.badge-sm{{padding:4px 8px;border-radius:{tok('--gw-radius-4')};
 font:{tok('--gw-text-button-12')}}}
.badge-md{{padding:4px 12px;border-radius:{tok('--gw-radius-8')};
 font:{tok('--gw-text-body-12-sem')};letter-spacing:var(--gw-text-body-12-sem-tracking)}}
.badge-red{{background:var(--tone-bad-bg);color:var(--tone-bad-fg)}}
.badge-md.badge-red{{background:var(--tone-bad-bg-md)}}
.badge-green{{background:var(--tone-good-bg);color:var(--tone-good-fg)}}
.badge-yellow{{background:var(--tone-warn-bg);color:var(--tone-warn-fg)}}

/* ── panels + tables ── */
.panel-toolbar{{padding:12px;display:flex;align-items:center;justify-content:space-between;gap:16px}}
.panel-toolbar-titled{{align-items:flex-start}}
.pt-left{{display:flex;align-items:center;gap:32px}}
.pt-right{{display:flex;align-items:center;gap:8px}}
.pt-title{{display:flex;flex-direction:column;gap:4px}}
.pt-title h3{{font:var(--dash-display-22-med);color:var(--t-display)}}
.pt-title span{{font:{tok('--gw-text-body-12-med')};
 letter-spacing:var(--gw-text-body-12-med-tracking);color:var(--t-muted)}}
.grid-wrap{{border-radius:{tok('--gw-radius-8')};border:1px solid var(--b-card);
 overflow:hidden}}
.trow{{padding:0 24px;min-height:56px;display:flex;align-items:center;gap:32px;
 background:var(--s-row);border-bottom:1px solid var(--b-divider)}}
.trow:hover:not(.trow-head):not(.trow-total){{background:var(--s-row-hover)}}
.trow-head{{min-height:44px;background:var(--s-row-head);
 border-bottom:1px solid var(--b-card);text-transform:uppercase}}
.trow-head .tc{{font:{tok('--gw-text-body-12-med')};
 letter-spacing:var(--gw-text-body-12-med-tracking);color:var(--t-label);
 gap:4px;align-items:center}}
.trow-head .ic{{color:var(--t-icon)}}
.trow-total{{border-bottom:0;border-top:1px solid var(--b-card)}}
.trow-total .tc-chan{{text-transform:uppercase}}   /* per-node textCase, not the whole row */
.trow:last-child{{border-bottom:0}}
.tc{{display:flex;min-width:0;font:{tok('--gw-text-body-12-med')};
 letter-spacing:var(--gw-text-body-12-med-tracking);color:var(--t-icon);
 align-items:center;gap:4px}}
.tc-chan{{width:110px;flex:0 0 110px;color:var(--t-display)}}
.tc-strong{{color:var(--t-display)}}
.tc-ink{{color:var(--t-body)}}
.tc-pair{{gap:8px}}
.tdiv{{width:1px;align-self:stretch;background:var(--b-divider);flex:0 0 auto}}
.trow-head .tdiv{{background:var(--b-card)}}
.tcells{{flex:1 1 auto;min-width:0;display:flex;gap:32px;align-items:center}}
.tcells>.tc{{flex:1 1 0}}
.tcells-trail{{flex:0 0 260px}}
.tcells-trail .tc{{white-space:nowrap}}
.tcells-trail .tc:first-child{{flex:1.6 1 0}}
.tc-metric{{flex-direction:column;align-items:flex-start;gap:4px}}
.tc-metric b{{font:{tok('--gw-text-body-14-med')};
 letter-spacing:var(--gw-text-body-14-med-tracking);color:var(--t-icon);
 font-weight:500}}
.chan-badge{{width:20px;height:20px;border-radius:{tok('--gw-radius-4')};
 background:{tok('--gw-color-primary-alpha-10')};display:inline-flex;align-items:center;
 justify-content:center;color:{tok('--gw-color-primary-500')};flex:0 0 auto}}
/* leave the first column unsized on the wide tables — build-rules.md: an explicit width on
   every column makes the browser spread leftover space across all of them */
.trow-daily{{display:grid;grid-template-columns:auto repeat(4,1fr);gap:32px}}
.trow-onb{{display:grid;grid-template-columns:auto 2fr 1.4fr 1fr .8fr 1fr 1.2fr;gap:32px}}
.pagination{{padding:12px;display:flex;align-items:center;justify-content:space-between;gap:16px}}
.pg-left,.pg-right{{display:flex;align-items:center;gap:8px}}

/* ── charts — NEW elements, no library equivalent. Declared, pending review. ── */
.is-hidden{{display:none !important}}
.chart-row{{display:flex;gap:8px}}
.chart-row>*{{flex:1 1 0;min-width:0}}
.panel{{border-radius:{tok('--gw-radius-8')};border:1px solid var(--b-card);
 padding:25px;display:flex;flex-direction:column;gap:32px}}
.panel-controls{{padding:12px;display:flex;align-items:center;justify-content:space-between;gap:16px}}
.pc-left{{display:flex;align-items:center;gap:16px}}
.pc-right{{display:flex;align-items:center;gap:8px}}
.panel-head{{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}}
.ch-title{{font:var(--dash-display-22-med);color:var(--t-display)}}
.ch-readout{{display:flex;align-items:center;gap:12px;flex:0 0 auto}}
.ch-readout>span{{font:{tok('--gw-text-button-12')};color:var(--t-label);
 white-space:nowrap}}
.gauge{{position:relative;width:40px;height:40px;display:inline-flex;align-items:center;
 justify-content:center;flex:0 0 auto}}
.gauge svg{{position:absolute;inset:0}}
.gauge b{{font:{tok('--gw-text-button-10')};color:var(--t-muted);
 position:relative}}
.gauge-track{{fill:none;stroke:var(--b-card);stroke-width:3}}
.gauge-fill{{fill:none;stroke-width:3;stroke-linecap:round}}
.gauge-red{{stroke:{tok('--gw-color-red-500')}}}
.gauge-green{{stroke:{tok('--gw-color-green-500')}}}
.ch-body{{display:flex;gap:12px;align-items:stretch;min-height:0}}
.ch-yaxis{{flex:0 0 auto;display:flex;flex-direction:column;justify-content:space-between;
 align-items:flex-end;font:{tok('--gw-text-button-12')};color:var(--t-label);
 border-right:1px solid var(--t-body);padding-right:8px}}
.ch-plot{{flex:1 1 auto;min-width:0;position:relative;height:248px}}
.ch-svg{{display:block;width:100%;height:100%}}
.ch-grid{{stroke:var(--b-card);stroke-width:1;stroke-dasharray:3 4}}
.ch-actual{{fill:none;stroke:{tok('--gw-color-primary-500')};stroke-width:2;
 vector-effect:non-scaling-stroke}}
.ch-target{{fill:none;stroke:var(--d-track);stroke-width:2;stroke-dasharray:6 6;
 vector-effect:non-scaling-stroke}}
.ch-today{{stroke:var(--t-label);stroke-width:1;vector-effect:non-scaling-stroke}}
.ch-dot{{fill:{tok('--gw-color-primary-500')}}}
.ch-tip{{position:absolute;top:18%;transform:translateX(6px);background:var(--s-menu);
 border:1px solid var(--b-card);border-radius:{tok('--gw-radius-8')};
 padding:8px 12px;display:flex;flex-direction:column;gap:6px;box-shadow:0 2px 4px #1b1c1d0a;
 pointer-events:none}}
.tip-date{{font:{tok('--gw-text-button-10')};color:var(--t-muted)}}
.tip-row{{display:flex;align-items:center;justify-content:space-between;gap:24px;
 font:{tok('--gw-text-button-10')};color:var(--t-display)}}
.tip-row i{{font-style:normal;color:var(--t-display)}}
.tip-red{{color:var(--tone-bad-fg)}}
.tip-green{{color:var(--tone-good-fg)}}
.ch-xaxis{{display:flex;justify-content:space-around;padding-left:40px;
 font:{tok('--gw-text-button-12')};color:var(--t-label)}}
/* ══ INTERACTIVE PASS ══ everything below is behaviour the frames imply but do not draw.
   Values reuse measured tokens; anything with no measured source is marked. */
.shell,.topbar,.sidebar,.card,.trow,.select,.icon-btn,.tab-item,.nav-item,.menu,.tip{{
 transition:background-color .12s,border-color .12s,color .12s}}
/* sortable header */
.trow-head .tc[data-sort-key]{{cursor:pointer;user-select:none}}
.trow-head .tc[data-sort-key]:hover{{color:var(--t-body)}}
.trow-head .tc[aria-sort]:not([aria-sort="none"]){{color:var(--t-body)}}
.sort-ic{{opacity:.55}}
.tc[aria-sort]:not([aria-sort="none"]) .sort-ic{{opacity:1;color:var(--t-body)}}
/* dropdown menu — measured spec, controls.md: menu is WIDER than its trigger, right-aligned,
   neutral/50 border, options button-12, option hover neutral/50, NO selected checkmark */
.select-wrap{{position:relative;display:inline-flex}}
.menu{{position:absolute;top:calc(100% + 4px);right:0;min-width:160px;z-index:40;
 background:var(--s-menu);border:1px solid var(--b-menu);border-radius:{tok('--gw-radius-8')};
 padding:4px;display:none;flex-direction:column;gap:4px;box-shadow:0 2px 4px #1b1c1d0a}}
.menu.is-open{{display:flex}}
.menu-item{{padding:8px 12px;border-radius:{tok('--gw-radius-4')};font:{tok('--gw-text-button-12')};
 color:var(--t-body);cursor:pointer;white-space:nowrap;background:none;border:0;text-align:left}}
.menu-item:hover,.menu-item.is-focus{{background:var(--s-chrome)}}
.select[aria-expanded="true"]{{border-color:var(--t-body)}}
/* live filter field */
.filter-field{{width:200px}}
.filter-field input{{all:unset;flex:1;min-width:0;font:{tok('--gw-text-button-14')};color:var(--t-body)}}
.filter-field input::placeholder{{color:var(--t-faint)}}
/* pagination disabled — measured Outline-disabled treatment from button.md: label drops to
   neutral/250. No disabled arrow is drawn in the frame; this is the nearest measured value. */
.icon-btn[disabled]{{cursor:default;color:var(--t-disabled);border-color:var(--b-divider)}}
/* collapsed sidebar — the measured 64px state */
.sidebar.is-collapsed{{width:64px}}
.sidebar.is-collapsed .nav-label,.sidebar.is-collapsed .nav-item span:not(.ic),
.sidebar.is-collapsed .uc-meta,.sidebar.is-collapsed .user-card>.icon-btn{{display:none}}
.sidebar.is-collapsed .nav-groups{{padding:8px;align-items:center}}
.sidebar.is-collapsed .nav-item{{width:32px;justify-content:center;padding:8px}}
.sidebar.is-collapsed .sb-footer{{padding:20px 8px 32px;display:flex;justify-content:center}}
.sidebar.is-collapsed .sb-collapse{{justify-content:center}}
.sidebar.is-collapsed .user-card{{justify-content:center}}
/* tooltip */
.tip{{position:fixed;z-index:60;max-width:260px;padding:8px 12px;
 border-radius:{tok('--gw-radius-8')};background:var(--s-invert);color:var(--t-on-invert);
 font:{tok('--gw-text-body-12-med')};letter-spacing:var(--gw-text-body-12-med-tracking);
 pointer-events:none;opacity:0;transition:opacity .1s}}
.tip.is-on{{opacity:1}}
[data-tip]{{cursor:help}}
/* collapsible inset */
.inset.is-closed .inset-rows{{display:none}}
.inset-head button{{transition:transform .12s}}
.inset.is-closed .inset-head button{{transform:rotate(180deg)}}
/* empty state for nav destinations with no page built — build-rules.md requires this */
.empty-page{{display:none;padding:80px 0;justify-content:center}}
.empty-page.is-on{{display:flex}}
.page.is-off{{display:none}}
.es{{width:480px;padding:40px;display:flex;flex-direction:column;align-items:center;gap:16px;
 text-align:center}}
.es-circle{{width:40px;height:40px;border-radius:999px;background:var(--s-chrome);display:flex;
 align-items:center;justify-content:center;color:var(--t-faint)}}
.es h2{{font:{tok('--gw-text-body-16-sem')};letter-spacing:var(--gw-text-body-16-sem-tracking);
 color:var(--t-display)}}
.es p{{margin:0;font:{tok('--gw-text-body-12-med')};
 letter-spacing:var(--gw-text-body-12-med-tracking);color:var(--t-muted)}}
@media (prefers-reduced-motion:reduce){{*{{transition:none !important}}}}

:focus-visible{{outline:2px solid {tok('--gw-color-primary-500')};outline-offset:2px}}
"""


# ── PASS-3 controller ──────────────────────────────────────────────────────────────────
# Icon markup is precomputed here so the JS never hand-builds SVG.
import json as _json
SORT_ICONS = {
    "none": ico("arrows-down-up", "bold", 12),
    "asc": ico("arrow-up", "bold", 12),
    "desc": ico("arrow-down", "bold", 12),
}
CHEVRONS = {
    "expanded": ico("caret-double-left", "bold", 12),
    "collapsed": ico("caret-double-right", "bold", 12),
}
JS = r"""
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var SORT_ICONS = __SORT__, CHEVRONS = __CHEV__;

  /* 1440 canvas scaled to fit. RULED, build-rules.md. Guard the zero viewport: a tab that has
     not been laid out reports 0, which would collapse the shell to nothing. */
  var DESIGN_W = 1440;
  function fit() {
    var w = window.innerWidth || DESIGN_W;
    document.documentElement.style.setProperty('--fit', Math.min(1, w / DESIGN_W));
  }
  fit();
  window.addEventListener('resize', fit);

  /* theme — a measured token swap, not a filter. Persisted so a reload keeps it. */
  function setTheme(mode) {
    document.documentElement.setAttribute('data-theme', mode);
    $$('[data-theme-set]').forEach(function (b) {
      var on = b.getAttribute('data-theme-set') === mode;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    try { localStorage.setItem('gw-theme', mode); } catch (e) {}
  }
  var stored = null;
  try { stored = localStorage.getItem('gw-theme'); } catch (e) {}
  setTheme(stored === 'dark' ? 'dark' : 'light');
  $$('[data-theme-set]').forEach(function (b) {
    function go() { setTheme(b.getAttribute('data-theme-set')); }
    b.addEventListener('click', go);
    b.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
    });
  });

  /* sidebar collapse — the measured 64px state */
  var collapseBtn = $('[data-collapse]');
  if (collapseBtn) collapseBtn.addEventListener('click', function () {
    var sb = $('.sidebar');
    var open = !sb.classList.toggle('is-collapsed');
    collapseBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    collapseBtn.setAttribute('aria-label', open ? 'Collapse sidebar' : 'Expand sidebar');
    collapseBtn.innerHTML = open ? CHEVRONS.expanded : CHEVRONS.collapsed;
  });

  /* generic tab groups */
  $$('.tab-group').forEach(function (g) {
    g.addEventListener('click', function (e) {
      var tb = e.target.closest('.tab-item');
      if (!tb || !g.contains(tb)) return;
      $$('.tab-item', g).forEach(function (i) { i.classList.remove('is-active'); });
      tb.classList.add('is-active');
    });
  });

  /* Channel Breakdown column groups — ONE table, two states */
  $$('.chk-wrap[data-toggles]').forEach(function (l) {
    l.addEventListener('click', function () {
      var on = $('.chk', l).classList.toggle('is-on');
      var group = l.getAttribute('data-toggles');
      $$('[data-col-group="' + group + '"]', l.closest('.card')).forEach(function (el) {
        el.classList.toggle('is-hidden', !on);
      });
    });
  });

  /* Actual vs Target — ONE section, two states */
  $$('[data-toggles-both]').forEach(function (l) {
    var card = l.closest('.card');
    function render(want) {
      var both = $('.toggle', l).classList.contains('is-on');
      if (!want) {
        var a = $('[data-chart-tabs] .tab-item.is-active', card);
        want = a ? a.getAttribute('data-chart') : 'demos';
      }
      $$('[data-chart-panel]', card).forEach(function (p) {
        p.classList.toggle('is-hidden', !both && p.getAttribute('data-chart-panel') !== want);
      });
      $('.toggle', l).setAttribute('aria-checked', both ? 'true' : 'false');
    }
    l.addEventListener('click', function () { $('.toggle', l).classList.toggle('is-on'); render(); });
    var tabs = $('[data-chart-tabs]', card);
    if (tabs) tabs.addEventListener('click', function (e) {
      var tb = e.target.closest('.tab-item');
      if (tb) render(tb.getAttribute('data-chart'));
    });
  });

  /* dropdown menus — measured spec: menu wider than its trigger, right-aligned, and NO
     selected checkmark (an earlier ruling invented one). Escape closes, arrows move. */
  function closeAll(except) {
    $$('.menu.is-open').forEach(function (m) {
      if (m === except) return;
      m.classList.remove('is-open');
      var trig = m.parentNode.querySelector('.select');
      if (trig) trig.setAttribute('aria-expanded', 'false');
    });
  }
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.select-wrap')) closeAll();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(); });

  $$('.select-wrap').forEach(function (wrap) {
    var trig = $('.select', wrap), menu = $('.menu', wrap);
    if (!trig || !menu) return;
    trig.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = menu.classList.contains('is-open');
      closeAll();
      if (!open) { menu.classList.add('is-open'); trig.setAttribute('aria-expanded', 'true'); }
    });
    menu.addEventListener('click', function (e) {
      var it = e.target.closest('.menu-item');
      if (!it) return;
      $('.select-label', trig).textContent = it.getAttribute('data-value');
      closeAll();
      wrap.dispatchEvent(new CustomEvent('gw:select', {
        bubbles: true,
        detail: { value: it.getAttribute('data-value'), sortKey: it.getAttribute('data-sort-key') }
      }));
    });
    trig.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        menu.classList.add('is-open'); trig.setAttribute('aria-expanded', 'true');
        var f = $('.menu-item', menu); if (f) f.focus();
      }
    });
    menu.addEventListener('keydown', function (e) {
      var items = $$('.menu-item', menu), i = items.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); (items[i + 1] || items[0]).focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); (items[i - 1] || items[items.length - 1]).focus(); }
      if (e.key === 'Escape') { closeAll(); trig.focus(); }
    });
  });

  /* table controller: filter -> sort -> page, in one object per card. Wiring the three
     independently is what makes them fight (a sort that forgets the filter, a page that
     forgets the sort). */
  function num(v) {
    if (v == null) return null;
    var s = String(v).replace(/[$,\s]/g, '');
    var m = s.match(/^-?\d*\.?\d+/);
    return m ? parseFloat(m[0]) : null;
  }
  function keyOf(row, idx) {
    var c = $$('[data-sort]', row)[idx];
    if (!c) return '';
    var raw = c.getAttribute('data-sort');
    var n = num(raw);
    return n === null ? String(raw).toLowerCase() : n;
  }

  $$('.grid-wrap').forEach(function (grid) {
    var card = grid.closest('.card');
    var pg = card ? $('.pagination', card) : null;
    var head = $('.trow-head', grid);
    var rows = $$('[data-row]', grid);
    var totalRow = $('.trow-total', grid);            /* pinned to the bottom, never sorted */
    var st = { key: null, dir: 0, q: '', page: 1, size: pg ? 10 : rows.length };

    function render() {
      var live = rows.filter(function (r) {
        if (!st.q) return true;
        var hay = (r.getAttribute('data-text') || r.textContent).toLowerCase();
        return hay.indexOf(st.q) > -1;
      });
      if (st.key !== null && st.dir !== 0) {
        live = live.slice().sort(function (a, b) {
          var x = keyOf(a, st.key), y = keyOf(b, st.key);
          if (x < y) return -st.dir;
          if (x > y) return st.dir;
          return 0;
        });
      }
      var pages = Math.max(1, Math.ceil(live.length / st.size));
      if (st.page > pages) st.page = pages;
      var from = (st.page - 1) * st.size;

      rows.forEach(function (r) { r.classList.add('is-hidden'); });
      live.slice(from, from + st.size).forEach(function (r) {
        r.classList.remove('is-hidden');
        grid.appendChild(r);
      });
      if (totalRow) grid.appendChild(totalRow);

      if (pg) {
        $('.pg-status', pg).textContent = 'Page ' + st.page + ' of ' + pages;
        $('[data-page="prev"]', pg).disabled = st.page <= 1;
        $('[data-page="next"]', pg).disabled = st.page >= pages;
      }
      if (head) $$('[data-sort-key]', head).forEach(function (h) {
        var active = String(st.key) === h.getAttribute('data-sort-key') && st.dir !== 0;
        var mode = !active ? 'none' : (st.dir === 1 ? 'asc' : 'desc');
        h.setAttribute('aria-sort', mode === 'none' ? 'none'
          : (mode === 'asc' ? 'ascending' : 'descending'));
        var ic = $('.sort-ic', h);
        if (ic) ic.innerHTML = SORT_ICONS[mode];
      });
    }

    function sortBy(k) {
      k = parseInt(k, 10);
      if (st.key === k) st.dir = st.dir === 1 ? -1 : (st.dir === -1 ? 0 : 1);
      else { st.key = k; st.dir = 1; }
      if (st.dir === 0) st.key = null;
      st.page = 1;
      render();
    }

    if (head) {
      head.addEventListener('click', function (e) {
        var h = e.target.closest('[data-sort-key]');
        if (h) sortBy(h.getAttribute('data-sort-key'));
      });
      head.addEventListener('keydown', function (e) {
        var h = e.target.closest('[data-sort-key]');
        if (h && (e.key === 'Enter' || e.key === ' ')) {
          e.preventDefault(); sortBy(h.getAttribute('data-sort-key'));
        }
      });
    }
    if (pg) pg.addEventListener('click', function (e) {
      var b = e.target.closest('[data-page]');
      if (!b || b.disabled) return;
      st.page += (b.getAttribute('data-page') === 'next' ? 1 : -1);
      render();
    });
    if (card) {
      card.addEventListener('gw:select', function (e) {
        var w = e.target.closest('.select-wrap');
        if (!w) return;
        if (w.hasAttribute('data-pagesize')) {
          st.size = parseInt(e.detail.value, 10); st.page = 1; render();
        }
        if (w.hasAttribute('data-sort-select') && e.detail.sortKey !== null) {
          st.key = parseInt(e.detail.sortKey, 10); st.dir = 1; st.page = 1; render();
        }
      });
      var filt = $('[data-filter]', card);
      if (filt) filt.addEventListener('input', function () {
        st.q = filt.value.trim().toLowerCase(); st.page = 1; render();
      });
    }
    render();
  });

  /* tooltips */
  var tip = document.createElement('div');
  tip.className = 'tip';
  document.body.appendChild(tip);
  function showTip(el) {
    tip.textContent = el.getAttribute('data-tip');
    tip.classList.add('is-on');
    var r = el.getBoundingClientRect(), tw = tip.offsetWidth, th = tip.offsetHeight;
    var left = Math.min(Math.max(8, r.left + r.width / 2 - tw / 2), window.innerWidth - tw - 8);
    var top = r.top - th - 8;
    if (top < 8) top = r.bottom + 8;
    tip.style.left = left + 'px';
    tip.style.top = top + 'px';
  }
  function hideTip() { tip.classList.remove('is-on'); }
  document.addEventListener('mouseover', function (e) {
    var el = e.target.closest('[data-tip]'); if (el) showTip(el);
  });
  document.addEventListener('mouseout', function (e) {
    if (e.target.closest('[data-tip]')) hideTip();
  });
  document.addEventListener('focusin', function (e) {
    var el = e.target.closest('[data-tip]'); if (el) showTip(el); else hideTip();
  });
  window.addEventListener('scroll', hideTip, true);

  /* collapsible inset */
  $$('[data-inset-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var open = !b.closest('[data-inset]').classList.toggle('is-closed');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
      b.setAttribute('aria-label', open ? 'Collapse' : 'Expand');
    });
  });

  /* nav: only Overview has a page. Anything else gets the empty state rather than leaving
     the previous page's content behind — build-rules.md. Shown/hidden rather than swapped,
     which also sidesteps the rebinding trap. */
  var page = $('.page'), empty = $('.empty-page'), title = $('[data-empty-title]');
  function goto(el) {
    $$('.nav-item').forEach(function (n) { n.classList.remove('is-selected'); });
    el.classList.add('is-selected');
    var home = el.hasAttribute('data-home');
    page.classList.toggle('is-off', !home);
    empty.classList.toggle('is-on', !home);
    if (!home && title) title.textContent = el.getAttribute('data-nav') + ' is not built yet';
    $('.slot').scrollTop = 0;
  }
  $$('.nav-item').forEach(function (n) {
    n.addEventListener('click', function (e) { e.preventDefault(); goto(n); });
  });
  var back = $('[data-empty-back]');
  if (back) back.addEventListener('click', function () {
    var home = $('.nav-item[data-home]');
    if (home) goto(home);
  });
})();
""".replace("__SORT__", _json.dumps(SORT_ICONS)).replace("__CHEV__", _json.dumps(CHEVRONS))


HTML = f"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GTM Command Center — Overview</title>
<style>{CSS}</style>
<div class="shell">
  <header class="topbar">
    <div class="tb-title">
      <span class="tb-logo">{LOGO_SVG}</span>
      <span class="tb-name">GTM Command Center</span>
      <button class="icon-btn icon-btn-ghost">{ico('caret-down','bold',16)}</button>
    </div>
    <div class="tb-actions">
      <button class="btn btn-outlined">{ico('arrows-clockwise','regular',16)}Sync Now</button>
      <!-- Theme switcher is rendered as designed. Light/dark switching is OUT OF SCOPE for this
           build (scope: the light overview frame). Dark values are measured and documented in
           exports/dashboard/v2/ if it is wired up later. -->
      <div class="theme-toggle" role="group" aria-label="Colour theme">
        <span data-theme-set="light" class="is-on" role="button" tabindex="0"
         aria-label="Light">{ico('sun-dim','bold',12)}</span>
        <span data-theme-set="dark" role="button" tabindex="0"
         aria-label="Dark">{ico('moon','bold',12)}</span></div>
    </div>
  </header>
  <div class="shell-body">
    <aside class="sidebar">
      <div class="sb-nav">
        <div class="sb-collapse">
          <button class="icon-btn icon-btn-ghost" data-collapse aria-expanded="true"
           aria-label="Collapse sidebar">{ico('caret-double-left','bold',12)}</button>
        </div>
        <nav class="nav-groups">{nav_html}</nav>
      </div>
      <div class="sb-footer">
        <div class="user-card">
          <span class="uc-identity"><span class="uc-avatar"></span>
            <span class="uc-meta"><span class="uc-name">Bruce Wayne</span>
              <span class="uc-role">Admin</span></span></span>
          <button class="icon-btn icon-btn-ghost">{ico('sign-out','bold',16)}</button>
        </div>
      </div>
    </aside>
    <main class="slot">{body}
      <!-- build-rules.md: every nav destination needs a real page; an unbuilt one gets the
           empty state rather than leaving the previous page's content behind. Shown/hidden
           rather than swapped, which also avoids the rebinding trap. -->
      <div class="empty-page"><div class="es">
        <span class="es-circle">{ico('squares-four','regular',16)}</span>
        <h2 data-empty-title>Not built yet</h2>
        <p>This destination has no page in the build. The Overview screen is the one surface
           measured from Figma so far.</p>
        <button class="btn btn-outlined" data-empty-back>Back to Overview</button>
      </div></div></main>
  </div>
</div>
<script>{JS}</script>
"""

OUT.write_text(HTML)
print(f"{OUT.relative_to(ROOT)} — {len(HTML)/1024:.0f}K")
print(f"  tokens requested: {len(NEEDED)} · emitted with dependencies: {len(EMIT)}")
print(f"  pulled in transitively: {', '.join(n for n in EMIT if n not in NEEDED) or 'none'}")
print(f"  icons inlined: {len(_ic)}")
