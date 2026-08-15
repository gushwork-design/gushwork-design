#!/usr/bin/env python3
"""
Verifies preview/gtm-command-center.html against the measurements it was built from.

Run it after EVERY change to _build_gtm_command_center.py:

    python3 preview/_build_gtm_command_center.py && python3 preview/_verify_gtm_command_center.py

Every check here exists because something was once wrong. The build is measured from Figma, so a
regression is silent by nature — it still renders, it is just no longer the design. This is the
only thing standing between "it looks fine" and "it matches".

What it does NOT cover: anything that needs a live DOM — computed colours, hover contrast,
scroll behaviour, the date parser. Those were verified in-browser and are recorded in
dashboard-component-audit.md section 11; re-run them there if you touch that behaviour.
"""
import json, pathlib, re, sys

H = (pathlib.Path.home() / "Downloads/gushwork-design/preview/gtm-command-center.html").read_text()
fails = []
def chk(cond, label, detail=""):
    print(("  ok    " if cond else "  FAIL  ") + label + (f"   {detail}" if detail and not cond else ""))
    if not cond: fails.append(label)

print("── build-rules invariants ──")
# two scroll regions by design: the content slot and the sidebar nav list (both pre-existing,
# both with min-height:0). build-rules means one scroller for the PAGE, which .slot is.
# three scroll regions, all deliberate: the content slot, the sidebar nav list, and the date
# picker's month stack — the last one measured, since the frame draws its 4x69 thumb explicitly.
chk(H.count("overflow-y:auto") == 3 and ".slot{flex:1;min-width:0;overflow-y:auto" in H
    and ".sb-nav-top .nav-groups{overflow-y:auto" in H and ".dp-stack{" in H,
    "one page scroller (.slot) + sidebar nav + the measured month stack",
    f"found {H.count('overflow-y:auto')}")
chk(".page>*{flex:0 0 auto}" in H, "page children are flex:0 0 auto")
pgc = re.search(r"\.page\{[^}]+\}", H).group(0)
chk("width:100%" in pgc,
    "the content column FILLS the slot — pinned to 1200 it left 176px dead when the rail collapsed",
    pgc)
chk("padding:var(--v-slot-top) 40px 80px" in pgc, "40px side margins hold either way", pgc)
chk("zoom:var(--fit,1)" in H, "shell zooms by --fit")
chk(re.search(r"if\s*\(\s*!?\s*w\b|w\s*(===|==|<=)\s*0|Math\.min\(1,\s*w", H) is not None,
    "fit has a zero-viewport guard")

decl = set(re.findall(r"(--[a-z0-9-]+)\s*:", H))
used = set(re.findall(r"var\((--[a-z0-9-]+)", H))
# --fit is set from JS and every reference carries a fallback, so it is legitimately absent
used = {u for u in used if u != "--fit"}
chk(H.count("var(--fit)") == 0, "--fit is only ever read with a fallback")
missing = sorted(u for u in used if u not in decl)
chk(not missing, "every var() is declared", f"undeclared: {missing}")

print("\n── 1. circular indicator ──")
rings = re.findall(r'<span class="ring"', H)
chk(len(rings) == 5, "5 rings (1 page-header + 4 run-rate)", f"found {len(rings)}")
chk('stroke-width="2"' in H, "2px band — from arcData.innerRadius 0.8, not strokeWeight")
chk('r="9.0"' in H, "r=9 so the outer edge lands at the measured r=10")
ph = re.search(r'class="ph-period".*?</span>', H, re.S).group(0)
chk("var(--d-track)" in ph and "var(--d-series)" in ph, "page-header ring: neutral/200 + primary/500")
c = 2 * 3.14159265 * 9   # r=9 now, matching the 2px band
chk(f'stroke-dasharray="{c*60/100:.2f} {c:.2f}"' in ph, "page-header ring sweeps 60% (Day 18 of 30)")
chk("question" not in ph, "the ? icon is gone from the period pill")
mc = re.findall(r'class="mc-sub">.*?</span>', H, re.S)
chk(len(mc) == 4, "4 run-rate sub-rows", f"found {len(mc)}")
chk(all('var(--b-card)' in m and 'var(--d-good)' in m for m in mc),
    "run-rate rings: neutral/100 track + green/400 fill")

print("\n── 2. nav hover = neutral/25 ──")
nh = re.findall(r"--s-nav-hover:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(nh[:1] == ["--gw-color-neutral-25"], "light --s-nav-hover is neutral/25", str(nh))
chk(nh[1:] == ["--gw-color-neutral-700"], "dark --s-nav-hover is neutral/700 (your call)", str(nh))
ns = re.findall(r"--s-nav-sel:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(ns == ["--gw-color-neutral-100", "--gw-color-neutral-600"],
    "nav selected: light /100, dark /600 (your call)", str(ns))
chk(".nav-item:hover:not(.is-selected){background:var(--s-nav-hover)}" in H,
    "hover rule points at the new alias")

print("\n── 3. crown badge ──")
ICO = pathlib.Path.home() / "Downloads/gushwork-design/assets/icons"
reg = re.search(r'd="([^"]+)"', (ICO / "regular/crown-simple.svg").read_text()).group(1)
fil = re.search(r'd="([^"]+)"', (ICO / "fill/crown-simple.svg").read_text()).group(1)
cb = re.search(r'<span class="chan-badge">.*?</span></span>', H, re.S).group(0)
chk('width:12px;height:12px' in cb and 'width="12" height="12"' in cb, "crown drawn at 12px")
chk(reg in H, "crown uses the REGULAR path (measured Weight=Regular)")
chk(fil not in H, "the FILL path is gone")
cbc = re.search(r"\.chan-badge\{[^}]+\}", H).group(0)
chk("border-radius:var(--gw-radius-4)" in cbc, "badge r4", cbc)
chk("padding:4px" in cbc, "badge 4px padding", cbc)
chk("gap:2px" in cbc, "badge 2px gap", cbc)

print("\n── 4. graph tooltip on hover ──")
chk(".ch-tip{opacity:0;visibility:hidden" in H, "tooltip hidden by default")
chk(".ch-tip.is-on{opacity:1;visibility:visible}" in H, "shown via .is-on")
chk(H.count('data-pts="') == 2, "both charts carry point data", f"found {H.count('data-pts=')}")
pts = re.search(r'data-pts="([^"]+)"', H).group(1).split(",")
chk(len(pts) == 10, "10 traced points", f"found {len(pts)}")
p7 = pts[7].split("|")
chk(p7[1] == "Jul 26" and p7[2] == "1104" and p7[3] == "1235",
    "today point reproduces the measured tooltip verbatim", f"got {p7}")
chk(H.count('class="ch-cursor"') == 2, "crosshair on both plots")
chk("ch-today" not in H, "the invented solid vertical marker is gone (no such node in Figma)")
chk('class="ch-dot"' not in H, "the stretched in-SVG dot is gone")
chk("ch-mark" not in H,
    "the two static marker dots are gone — measured against the design's plot box, they floated "
    "above this chart's traced curve and marked nothing")
chk("stroke-dasharray:4 4" in H, "vertical/horizontal grid dash 4/4 as measured")
chk("stroke-dasharray:12 4" in H, "target line dash 12/4 as measured")
chk("ArrowRight" in H and "ArrowLeft" in H, "keyboard access to points")

print("\n── 5. search text no longer cut off ──")
ff = re.search(r'<span class="select select-filter filter-field">.*?</span>', H, re.S).group(0)
chk("<svg" not in ff, "no icons inside the filter field (measured: text only)")
chk("caret" not in ff, "no caret")
chk('placeholder="Search domain, AE, channel"' in ff, "full placeholder present")
chk(".filter-field{width:212px;border:0;box-shadow:inset 0 0 0 1px var(--b-strong)}" in H,
    "212 wide so the 186px placeholder fits (your call over Figma's own clip)")
fi = re.search(r"\.filter-field input\{[^}]+\}", H).group(0)
chk("text-overflow:ellipsis" in fi and "white-space:nowrap" in fi,
    "single-line ellipsis, reproducing Figma textTruncation:ENDING maxLines:1", fi)

print("\n── structure: sidebar vs 236:31801 ──")
sb = re.search(r"\.sidebar\{[^}]+\}", H).group(0)
chk("width:240px" in sb, "sidebar 240 wide", sb)
chk("justify-content:space-between" in sb, "space-between (Figma primaryAxisAlignItems=SPACE_BETWEEN)")
sc = re.search(r"\.sb-collapse\{[^}]+\}", H).group(0)
chk("height:28px" in sc and "padding:4px" in sc, "collapse row 28 tall, 4px pad", sc)
scb = re.search(r"\.sb-collapse \.icon-btn\{[^}]+\}", H).group(0)
chk("width:20px" in scb and "height:20px" in scb, "collapse button 20x20 (was 24)", scb)
ng = re.search(r"\.nav-groups\{[^}]+\}", H).group(0)
chk("padding:20px" in ng and "gap:24px" in ng, "nav groups pad 20 gap 24", ng)
nic = re.search(r"\.nav-item \.ic\{[^}]+\}", H).group(0)
chk("color:inherit" in nic, "nav icons inherit the row colour (all 11 bound to Neutral/900)", nic)
ni = re.search(r"\.nav-item\{[^}]+\}", H).group(0)
chk("color:var(--t-body)" in ni, "nav row colour is --t-body = neutral/900 light / white dark", ni)
nlc = re.search(r"\.nav-label\{[^}]+color:var\(--t-faint\)\}", H, re.S)
chk(nlc is not None, "group labels stay --t-faint = neutral/400 as measured")
chk("height:32px" in ni and "padding:8px" in ni and "gap:8px" in ni, "nav item 32 / pad 8 / gap 8", ni)
nl = re.search(r"\.nav-label\{[^}]+\}", H).group(0)
chk("padding:4px 8px" in nl, "nav label pad 4/8", nl)
sf = re.search(r"\.sb-footer\{[^}]+\}", H).group(0)
chk("padding:20px 20px 32px" in sf, "footer pad 20/20/32", sf)
uc = re.search(r"\.user-card\{[^}]+\}", H).group(0)
chk("justify-content:space-between" in uc and "gap:8px" in uc, "user card space-between gap 8", uc)

print("\n── fonts ──")
chk(H.count("@font-face") == 2, "both faces declared", str(H.count("@font-face")))
chk("../fonts/" not in H, "no relative font url (it 404d over http)")
chk(H.count("data:font/ttf;base64,") == 2, "both faces embedded")

print("\n── structure + avatar ──")
chk('class="uc-avatar">' in H and "uc-art" in H, "avatar uses the real character artwork")
chk('viewBox="0 0 38.1724 86.6301"' in H, "artwork viewBox matches the exported asset")
chk('width="25.4" height="57.8"' in H, "drawn at the measured 25.4x57.8")
av = re.search(r"\.uc-avatar\{[^}]+\}", H).group(0)
chk("background:var(--gw-color-white)" in av, "white fill (was a blue disc)", av)
chk("border:1px solid var(--b-card)" in av, "1px neutral/100 border (0.333 measured -> R5)")
chk(".uc-avatar::after" not in H, "the CSS pseudo-element stand-in is gone")

print("\n── loading screen ──")
chk("--dash-display-32-reg:400 32px/1.2 'Vert Grotesk Display'" in H,
    "32/120% Regular literal declared")
chk('class="loading-page"' in H, "loading page present")
chk(".loading-page{display:none;height:100%" in H, "hidden by default, full slot height")
chk("Loading &amp; fetching data" in H, "measured heading text")
lt = re.search(r"\.load-track\{[^}]+\}", H).group(0)
chk("width:400px" in lt and "height:12px" in lt, "track 400x12", lt)
chk("border-radius:var(--gw-radius-40)" in lt, "r40 as measured", lt)
lf = re.search(r"\.load-fill\{[^}]+\}", H).group(0)
chk("display:block" in lf, "fill is blockified (an inline span ignores width)", lf)
chk("background:var(--s-invert)" in lf, "fill is neutral/black", lf)
chk("width:58%" in lf, "starts at the drawn 58%", lf)
chk(">58%<" in H, "58% label")
chk(".load-box{width:442px" in H, "442px column")
chk("gap:24px" in re.search(r"\.load-box\{[^}]+\}", H).group(0), "24px gap")
chk("gap:12px" in re.search(r"\.load-row\{[^}]+\}", H).group(0), "12px row gap")

print("\n── no regressions ──")
chk(len(re.findall(r'data-chart-panel="', H)) == 2, "still two chart panels (one stateful pair)")
nh2 = len(re.findall(r'class="trow trow-head', H))
chk(nh2 == 3, "three table heads", str(nh2))
chk("3.74x" in H.lower(), "total row keeps real totals")
chk(H.count("--v-sect-gap") >= 2, "section gap declared in both themes")

print("\n── drift notice ──")
chk("gushwork-build:{" in H, "the build carries a stamp")
stamp = json.loads(re.search(r"gushwork-build:(\{.*?\})", H, re.S).group(1))
chk(stamp.get("pluginVersion") == json.load(open(
    pathlib.Path.home() / "Downloads/gushwork-design/.claude-plugin/plugin.json"))["version"],
    "the stamp's version matches plugin.json", str(stamp.get("pluginVersion")))
chk(len(stamp.get("components", [])) >= 20,
    "the stamp lists the components used", str(len(stamp.get("components", []))))
chk(stamp.get("registry", "").startswith("https://gushwork-design.vercel.app/"),
    "the registry is the PUBLIC deploy, so the check survives the repo going private",
    stamp.get("registry"))
chk(stamp.get("changelog", "").endswith("changelog-sheet.html"), "the stamp carries the changelog")
reg = json.load(open(pathlib.Path.home()
    / "Downloads/gushwork-design/exports/dashboard/component-registry.json"))
unknown = [c for c in stamp["components"] if c not in reg["components"]]
chk(not unknown, "every stamped component exists in the registry", str(unknown))
chk('DRIFT_JS = r"""' in (pathlib.Path.home()
    / "Downloads/gushwork-design/preview/_build_gtm_command_center.py").read_text(),
    "the JS block is a RAW python string — otherwise a JS \\n becomes a real newline "
    "and the whole script fails to parse")
chk("data-drift-update" in H, "the notice offers an action, not only Dismiss")
chk("window.prompt(" not in H, "no modal prompt — it blocks the page")
chk("localStorage.setItem(KEY, sig)" in H, "shown once per change-set, recorded at show time")
chk(".catch(function () {});" in H, "an unreachable registry stays silent")

print("\n── Figma comments ──")
sbn = re.search(r"\.sb-nav\{[^}]+\}", H).group(0)
chk("flex:1 1 auto" in sbn and "justify-content:space-between" in sbn,
    "nav column grows and splits, so Settings/Admin pin to the bottom", sbn)
chk('class="nav-groups nav-groups-end"' in H, "end group emitted")
chk(H.count('class="nav-label"') == 4, "still four nav groups")
sbf = re.search(r"\.sb-footer\{[^}]+\}", H).group(0)
chk("box-shadow:inset 0 1.5px 0 var(--b-chrome)" in sbf,
    "footer divider = measured 1.5px top stroke", sbf)
tt = re.search(r"\.theme-toggle>span\{[^}]+\}", H).group(0)
chk("border-radius:var(--gw-radius-4)" in tt, "toggle inactive cell r4 as measured", tt)
chk(".theme-toggle>.is-on{border-radius:var(--gw-radius-8)" in H, "active cell r8 as measured")
# DIRECT-child selectors. `.theme-toggle span` also matched the nested `.ic` span ico() emits,
# and a rule applied straight to that element beats colour inherited from the parent cell — so the
# ACTIVE glyph painted --t-toggle-off in BOTH themes and was invisible on its own pill.
chk(".theme-toggle>span{color:var(--t-toggle-off)}" in H,
    "OFF colour is scoped to direct children")
chk(".theme-toggle>.is-on{" in H, "ON colour is scoped to direct children")
chk(".theme-toggle span{" not in H,
    "no descendant selector left that would leak onto the inner .ic span")
tg = re.findall(r"--t-toggle-off:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(tg == ["--gw-color-neutral-900", "--gw-color-neutral-50"],
    "toggle OFF glyph: light /900, dark /50 (measured in 236:33407)", str(tg))
tn = re.findall(r"--t-toggle-on:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(tn == ["--gw-color-white", "--gw-color-black"],
    "toggle ON glyph: light white, dark BLACK — not the /900 --t-on-invert carries", str(tn))
chk("Sort by Roi" not in H and "Sort by ROI" in H, "roi title-cases to the acronym ROI")
chk(">Assigned AE<" in H and ">Annual ARR<" in H and ">Channel<" in H,
    "sort options are consistently cased")
chk(".toggle.is-on{background:var(--s-toggle-on)}" in H, "Show-both track is a theme alias")
tn = re.findall(r"--s-toggle-on:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(tn == ["--gw-color-neutral-900", "--gw-color-black"],
    "toggle track: measured /900 light, black dark so it clears the /900 card", str(tn))
# a hover fill must differ from the surface it lands ON, not just from the text
for alias, want in [("--s-menu-hover", ["--gw-color-neutral-50", "--gw-color-neutral-800"]),
                    ("--s-inset-hover", ["--gw-color-neutral-50", "--gw-color-neutral-900"]),
                    ("--s-compare-hover", ["--gw-color-neutral-35", "--gw-color-neutral-700"])]:
    got = re.findall(alias + r":var\((--gw-color-[a-z0-9-]+)\)", H)
    chk(got == want, f"{alias} steps off its own surface in both themes", str(got))
chk(".menu-item:hover,.menu-item.is-focus{background:var(--s-menu-hover)}" in H,
    "menu hover no longer collides with the menu surface")
chk(".filter-field:hover{background:var(--s-inset-hover)}" in H,
    "filter hover no longer collides with the field fill")
chk(".btn-compare:hover{background:var(--s-compare-hover)" in H,
    "Compare hover no longer collides with its own fill")
chk("vector-effect:non-scaling-stroke" in re.search(r"\.ch-target\{[^}]+\}", H).group(0),
    "target line stroke no longer scales down")
pt = re.search(r"\.pt-title\{[^}]+\}", H).group(0)
chk("flex-direction:row" in pt and "gap:12px" in pt, "card-header subtext sits to the right", pt)
chk("1,308 bookings last month" in H, "measured count literal")
chk("data-chan-range" in H, "Channel Breakdown carries the Showing-for select")
# every tone alias must be declared in BOTH themes — an omission silently keeps the light value
for tone in ("good", "bad", "warn"):
    for part in ("bg", "fg"):
        got = re.findall(r"--tone-%s-%s:var\((--gw-color-[a-z0-9-]+)\)" % (tone, part), H)
        chk(len(got) == 2, f"--tone-{tone}-{part} is declared in both themes", str(got))
dark_tints = re.findall(r"--tone-(?:good|bad|warn)-bg:var\((--gw-color-\w+-alpha-10)\)", H)
chk(len(dark_tints) == 3,
    "dark badge tints are the Alpha/10 steps, not the light /25 solids", str(dark_tints))
chk("function applyColGroup(" in H, "column groups toggle through one code path")
chk("if (!others.length)" in H,
    "unchecking the LAST column group hands the check to its pair — both off shows no data")
chk('l.setAttribute(\'role\', \'checkbox\')' in H, "column groups expose a checkbox role")
chk('data-tip="Choose columns"' not in H, "the invented column-chooser button is gone")
chk("(5, 10, 25, 50, 100)" in H or ">5<" in H, "page size 5 offered")
chk("--s-btn-hover:var(--gw-color-neutral-35)" in H, "Outline hover = measured neutral/35")
chk("--s-btn-primary-hover:var(--gw-color-neutral-850)" in H, "Primary hover = measured neutral/850")
chk(".btn:hover:not(.btn-primary){background:var(--s-btn-hover)}" in H,
    "outline/ghost hover rule, scoped away from primary")
# every hover fill must be a theme ALIAS. Baking a measured light value in as an absolute is what
# put white-on-near-white (1.23:1) and neutral/50-on-neutral/50 (1.00:1) into dark mode.
for rule, want in [(r"\.btn:hover:not\(\.btn-primary\)", "var(--s-btn-hover)"),
                   (r"\.btn-ghost:hover", "var(--s-btn-ghost-hover)"),
                   (r"\.btn-primary:hover", "var(--s-btn-primary-hover)"),
                   (r"\.icon-btn:hover:not\(\[disabled\]\)", "var(--s-btn-hover)"),
                   (r"\.dash-switch-item:hover", "var(--s-btn-hover)"),
                   (r"\.dp-preset:hover", "var(--s-btn-hover)")]:
    m = re.search(rule + r"\{[^}]*\}", H)
    chk(m is not None and want in m.group(0), f"hover fill is an alias: {rule}",
        m.group(0) if m else "rule missing")
ph = re.findall(r"--s-btn-primary-hover:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(ph == ["--gw-color-neutral-850", "--gw-color-neutral-850"],
    "primary hover stays DARK in both themes — the fill is absolute black", str(ph))
gh = re.findall(r"--s-btn-ghost-hover:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(gh == ["--gw-color-neutral-50", "--gw-color-neutral-800"],
    "ghost hover: measured /50 light, ruled /800 dark", str(gh))
tg2 = re.findall(r"--t-btn-ghost:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(tg2 == ["--gw-color-black", "--gw-color-neutral-50"],
    "Cancel label is an alias, not a hard-coded black", str(tg2))
chk(".dp-cancel{color:var(--t-btn-ghost)}" in H, "Cancel uses the alias")
chk(".btn-primary{background:var(--gw-color-black);color:var(--gw-color-white)" in H,
    "primary has a BASE rule (it only had a hover rule, so Apply rendered transparent)")
chk("color:var(--gw-color-white)" in re.search(r"\.btn-primary:hover\{[^}]+\}", H).group(0),
    "primary keeps white text through hover")
chk(".btn-outlined{box-shadow:inset 0 0 0 1px var(--b-strong)}" in H,
    "button outline is an inset shadow so the box hugs like Figma")
chk("is-preview" in H, "range hover preview on the calendar")
rw = re.search(r"\.dp-row\{[^}]+\}", H).group(0)
chk("grid-template-columns:repeat(7,1fr)" in rw,
    "day rows are 7 contiguous columns — space-between broke the band into strips", rw)
chk(".dp-day.is-start.has-end::before" in H and ".dp-day.is-end::before" in H,
    "half-column bands carry the run through both endpoints")
chk(".dp-day.is-edge::after" in H, "endpoint pill is an overlay, so the band shows underneath")
chk("<i>1</i>" in H and "<i>31</i>" in H, "day numbers wrapped so they stack above band and pill")
chk("var PRESETS = {" in H, "presets compute real ranges")
chk(H.count('class="dp-month"') == 12 or H.count("dp-month\" data-month") == 12,
    "twelve months rendered (Aug 2025 -> Jul 2026)", str(H.count("data-month=")))
for mn in ("AUG 2025", "JAN 2026", "MAY 2026", "JUL 2026"):
    chk(">" + mn + "<" in H, f"month block: {mn}")
st = re.search(r"\.dp-stack\{[^}]+\}", H).group(0)
chk("gap:20px" in st, "stack gap 20 as measured", st)
chk("overflow-y:auto" in st, "stack scrolls")
chk("scrollbar-color:var(--gw-color-neutral-300)" in st,
    "thumb is Neutral/300 — #bbbec4 exactly, the measured `Frame 2147260244` fill", st)
chk(".dp-stack::-webkit-scrollbar{width:4px}" in H, "thumb 4px wide as measured")
tipc = re.findall(r"--s-tip:var\((--gw-color-[a-z0-9-]+)\)", H)
tipt = re.findall(r"--t-tip:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(tipc == ["--gw-color-neutral-900", "--gw-color-white"],
    "tooltip bubble: /900 light, white dark (measured 282:727)", str(tipc))
chk(tipt == ["--gw-color-white", "--gw-color-neutral-900"],
    "tooltip text inverts with the bubble", str(tipt))
chk("background:var(--s-tip);color:var(--t-tip)" in H,
    "tooltip uses its own aliases, not --s-invert (which is black, not /900)")
chk("data-tip-place" in H and "'right'" in H, "tooltip supports a right placement")
chk("function railTips(" in H, "collapsed rail swaps nav labels into tooltips")
chk("data-uc-identity" in H and "data-signout" in H,
    "avatar and sign-out are tooltip targets on the rail")
uc = re.search(r"\.sidebar\.is-collapsed \.user-card\{[^}]+\}", H).group(0)
chk("flex-direction:column" in uc and "align-items:center" in uc,
    "collapsed user card stacks", uc)
chk("gap:8px" in uc, "avatar and sign-out are 8px apart", uc)
chk(".sidebar.is-collapsed .user-card>.icon-btn{display:none}" not in H,
    "sign-out is no longer hidden when collapsed")
chk(".sidebar.is-collapsed .uc-meta{display:none}" in H,
    "the name/role block still hides when collapsed — the tooltip carries it")
chk(".nav-item[data-tip],[data-uc-identity][data-tip],[data-signout][data-tip],\n.btn[data-tip]{cursor:pointer}" in H,
    "tooltip targets that are CONTROLS keep the pointer, not [data-tip]'s help cursor")
chk('.btn[data-tip][disabled]{cursor:default}' in H, "a disabled Sync Now drops the pointer")
chk('data-off="' in H and "data-day=" not in H,
    "day identity is an offset from Jul 1 2026, so it is unique across twelve months")
cal = re.search(r"\.dp-cal\{[^}]+\}", H).group(0)
chk("height:320px" in cal, "right pane is the measured 320, not stretched to the split's 360", cal)
chk("align-items:flex-start" in re.search(r"\.dp-split\{[^}]+\}", H).group(0),
    "split aligns top (measured c:MIN)")
for k in ("Last 7 days", "Last week (Sun - Sat)", "Quarter to date", "Last 12 months"):
    chk("'" + k + "':" in H, f"preset wired: {k}")
chk("var ANCHOR = new Date(2026, 6, 31)" in H, "anchor is the measured range end, Jul 31 2026")
chk("dpFrom.value = fmtDate(a)" in H,
    "fields carry TRUE dates even when the range starts before the rendered month")
chk('<input class="dp-field" data-dp-from' in H, "range start is typable")
chk('<input class="dp-field" data-dp-to' in H, "range end is typable")
chk("function parseDate(" in H, "typed dates are parsed")
# assert the four date shapes by their actual patterns — a bare count also catches the
# unrelated numeric-sort parser
for label, pat in [("Jul 15, 2026", r"\^\(\[A-Za-z\]\{3,\}\)\\s\+"),
                   ("15 Jul 2026", r"\^\(\\d\{1,2\}\)\\s\+\(\[A-Za-z\]"),
                   ("2026-07-15", r"\^\(\\d\{4\}\)-"),
                   ("7/15/2026", r"\^\(\\d\{1,2\}\)\\/")]:
    chk(re.search(pat, H) is not None, f"typed date shape accepted: {label}")
chk("aria-invalid" in H, "an unreadable date flags the field instead of guessing")
chk("var SPAN_MIN = offOf" in H, "typed dates are bounded by the rendered span")
chk("selFrom > selTo" in H, "a reversed range is swapped, not rejected")
chk("function refreshSyncTip(" in H, "Sync Now carries a last-synced tooltip")
chk("lastSync = Date.now();          /* only a COMPLETED sync resets it */" in H,
    "the last-synced clock only moves on a completed sync")
nday = len(re.findall(r'<button class="dp-day[^"]*" data-off="-?\d+">', H))
chk(nday == 365, "every day Aug 1 2025 -> Jul 31 2026 is a button (365)", str(nday))
chk("data-sync-label" in H, "Sync Now label is addressable")
chk(".btn .ic{color:inherit}" in H,
    "button glyphs follow their label — measured on both buttons in both frames")
tb = re.findall(r"--t-btn:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(tb == ["--gw-color-neutral-900", "--gw-color-neutral-50"],
    "Sync Now label: /900 light, /50 dark (NOT white)", str(tb))
sc = re.findall(r"--s-compare:var\((--gw-color-[a-z0-9-]+)\)", H)
bc = re.findall(r"--b-compare:var\((--gw-color-[a-z0-9-]+)\)", H)
tc = re.findall(r"--t-compare:var\((--gw-color-[a-z0-9-]+)\)", H)
chk(sc == ["--gw-color-white", "--gw-color-neutral-800"], "Compare fill: white / /800", str(sc))
chk(bc == ["--gw-color-neutral-400", "--gw-color-neutral-600"], "Compare stroke: /400 / /600", str(bc))
chk(tc == ["--gw-color-neutral-900", "--gw-color-white"], "Compare label: /900 / white", str(tc))
chk("'Syncing'" in H and "is-syncing" in H, "Syncing processing state wired")
chk("@keyframes spin" in H, "sync spinner defined")

print()
if fails:
    print(f"\u2718 {len(fails)} failed: " + "; ".join(fails)); sys.exit(1)
print("\u2714 all checks passed")
