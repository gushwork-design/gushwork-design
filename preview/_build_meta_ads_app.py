#!/usr/bin/env python3
"""Build the nine-page Meta Ads app from measured Gushwork dashboard components.

Every section is a real Section. The shell is dashboard-build with one deliberate
extension: it is fluid rather than the measured fixed 1440. That is called out in
the page footer so the deviation is never mistaken for a Figma value.
"""
import json, os, re

REPO = '/Users/utsavsingh/Downloads/gushwork-design'
OUT = os.path.join(REPO, 'preview/meta-ads-app.html')
VAL = ('/private/tmp/claude-501/-Users-utsavsingh-Downloads-Gushwork-Design-System--2-/'
       'c5f5aac2-8749-438f-8280-441413e4e08c/scratchpad/validation/meta-ads-app.html')

ICONS = [('gauge','regular','gauge'),('pulse','regular','pulse'),('image','regular','image'),
 ('tree','regular','tree-structure'),('rotate','regular','arrows-clockwise'),
 ('handshake','regular','handshake'),('seal','regular','seal-check'),('users','regular','users'),
 ('chart','regular','chart-line'),('caret','fill','caret-down'),('refresh','bold','arrow-clockwise'),
 ('dots','regular','dots-three-outline-vertical'),('dots3','regular','dots-three'),
 ('money','regular','money'),('target','regular','target'),('up','bold','arrow-up-right'),
 ('down','bold','arrow-down-right'),('sort','bold','arrows-down-up'),('funnel','regular','funnel'),
 ('calendar','regular','calendar-blank'),('sparkle','regular','sparkle')]

def sprite():
    out=[]
    for sid,w,n in ICONS:
        s=open(f'{REPO}/assets/icons/{w}/{n}.svg').read()
        paths=''.join(f'<path d="{d}" fill="currentColor"/>'
                      for d in re.findall(r'<path[^>]*d="([^"]+)"',s))
        out.append(f'<symbol id="i-{sid}" viewBox="0 0 256 256">{paths}</symbol>')
    return '\n  '.join(out)

# ── measured Section builders ──────────────────────────────────────────────
def kpi(t,v,cap,kind,arrow,pct,icon='money'):
    return (f'<div class="kpi"><div class="kpi__hd"><span class="kpi__t">{t}</span>'
            f'<svg><use href="#i-{icon}"/></svg></div><div class="kpi__body">'
            f'<div class="kpi__vrow"><span class="kpi__v">{v}</span>'
            f'<span class="kpib kpib--{kind}">{pct}<svg><use href="#i-{arrow}"/></svg></span></div>'
            f'<span class="kpi__cap">{cap}</span></div></div>')

def ana(l,v,c='vs last month'):
    return (f'<div class="ana"><span class="ana__l">{l}</span><div class="ana__stack">'
            f'<span class="ana__v">{v}</span><span class="ana__c">{c}</span></div></div>')

def card_layout(kpis,anas):
    """KPI cards = len(kpis). 1 and 2 sit left of the analytics grid; 3 stacks above it."""
    if len(kpis)==3:
        return ('<section class="cl"><div class="cl__krow">'+''.join(kpis)+'</div>'
                '<div class="cl__arow">'+''.join(anas)+'</div></section>')
    n=len(kpis)
    return (f'<section class="cl cl--side" data-k="{n}"><div class="cl__kside">'+''.join(kpis)+'</div>'
            '<div class="cl__agrid">'+''.join(anas)+'</div></section>')

def progress(label,count,pct):
    return (f'<section class="pb"><div class="pb__hd">'
            f'<span class="pb__ico"><svg><use href="#i-target"/></svg></span>'
            f'<span class="pb__l">{label}</span><span class="pb__c">{count}</span></div>'
            f'<div class="pb__track"><div class="pb__fill" style="width:{pct}%">{pct}%</div></div></section>')

def sec_open(title,icon='chart'):
    return (f'<section class="sec"><div class="sec__hd"><span class="sec__ttl">'
            f'<span class="sec__ico"><svg><use href="#i-{icon}"/></svg></span>'
            f'<span class="sec__t">{title}</span></span>'
            f'<svg class="sec__caret sec__caret--up"><use href="#i-caret"/></svg></div>')

def sec_collapsed(title,icon='chart'):
    return (f'<section class="sec"><div class="sec__hd"><span class="sec__ttl">'
            f'<span class="sec__ico"><svg><use href="#i-{icon}"/></svg></span>'
            f'<span class="sec__t">{title}</span></span>'
            f'<svg class="sec__caret"><use href="#i-caret"/></svg></div></section>')

def graph_bar(rows,xticks):
    return ('<div class="sec__body"><div class="gr__row"><div class="gr__y">'
            + ''.join(f'<span>{n}</span>' for n,_,_ in rows)
            + '</div><div class="gr__area"><div class="gr__plot>'.replace('plot>','plot">')
            + ''.join(f'<div class="gbar" style="width:{w}%"><span>{v}</span></div>' for _,w,v in rows)
            + '</div><div class="gr__x">' + ''.join(f'<span>{x}</span>' for x in xticks)
            + '</div></div></div></div></section>')

def graph_line(pts,xticks,yticks):
    poly=' '.join(f'{x},{y}' for x,y in pts)
    return ('<div class="sec__body"><div class="gr__row">'
            '<div class="gr__y gr__y--line">'+''.join(f'<span>{y}</span>' for y in yticks)+'</div>'
            '<div class="gr__area"><div class="gline"><svg viewBox="0 0 600 200" preserveAspectRatio="none">'
            '<defs><linearGradient id="lf" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0%" stop-color="#e4efff"/><stop offset="55%" stop-color="#eff6ff"/>'
            '<stop offset="100%" stop-color="#f9fbff"/></linearGradient></defs>'
            f'<polygon points="{poly} 600,200 0,200" fill="url(#lf)"/>'
            f'<polyline points="{poly}" fill="none" stroke="var(--gw-color-primary-500)" stroke-width="2"/>'
            '</svg></div><div class="gr__x">'+''.join(f'<span>{x}</span>' for x in xticks)
            + '</div></div></div></div></section>')

def cells(items):
    out=[]
    for i,(l,v) in enumerate(items):
        out.append(f'<div class="cell"><span class="cell__l">{l}</span><span class="cell__v">{v}</span></div>')
        if i<len(items)-1: out.append('<span class="cell__sep"></span>')
    return '<div class="sec__body"><div class="cells">'+''.join(out)+'</div></div>'

def with_dropdown(label,items,sub=None):
    h=(f'<section class="sec"><div class="sec__hd">'
       f'<span class="secdd"><span class="secdd__l">{label}</span>'
       f'<svg class="sec__caret"><use href="#i-caret"/></svg></span>'
       f'<svg class="sec__caret sec__caret--up"><use href="#i-caret"/></svg></div>'+cells(items))
    if sub:
        h+='<div class="subgroup"><span class="subttl">'+sub[0]+'</span>'+cells(sub[1])+'</div>'
    return h+'</section>'

def table(title,cols,rows,sort='Spend',actions=('Export','Sync now')):
    head=''.join(f'<th style="width:{w}">{c}</th>' for c,w in cols)+'<th style="width:16px"></th>'
    body=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)
                 +'<td><svg style="width:16px;height:16px;color:var(--gw-color-neutral-600)">'
                  '<use href="#i-dots3"/></svg></td></tr>' for r in rows)
    return (sec_open(title)
      +'<div class="tblwrap"><div class="tbar"><span class="tbar__l">Sort by</span>'
      +f'<span class="dd" style="width:120px">{sort}<svg><use href="#i-caret"/></svg></span>'
      +'<button class="btn btn--ghost" aria-label="Toggle direction"><svg><use href="#i-sort"/></svg></button>'
      +'<span style="margin-left:auto;display:flex;gap:var(--gw-space-8)">'
      +f'<button class="btn btn--outline">{actions[0]}</button>'
      +f'<button class="btn btn--primary">{actions[1]}</button></span></div>'
      +f'<table class="dt"><tr>{head}</tr>{body}</table>'
      +'<div class="tbar"><span class="tbar__l">Showing per page</span>'
      +'<span class="dd" style="width:70px">10<svg><use href="#i-caret"/></svg></span>'
      +'<span class="pager"><button class="btn btn--ghost">&lsaquo;</button>'
      +'<span class="cur">1</span><span>2</span><button class="btn btn--ghost">&rsaquo;</button>'
      +'</span></div></div></section>')

bg=lambda t:f'<span class="badge badge--g">{t}</span>'
bn=lambda t:f'<span class="badge badge--n">{t}</span>'
brd=lambda t:f'<span class="badge badge--r">{t}</span>'
by=lambda t:f'<span class="badge badge--y">{t}</span>'

PAGES={}
PAGES['command-center']=dict(title='Command center',tabs=['Today','This week','This month','Custom'],sel=2,
 filters=['All accounts','All campaigns'],body=
 card_layout([kpi('Blended CPL','$263.94','Above the $240 target · 6 campaigns live','neg','up','9%')],
  [ana('Spend','$8,446'),ana('Meta leads','32'),ana('Attr leads','28'),
   ana('Show-ups','11'),ana('Closed','4'),ana('CAC','$2,112')])
 +progress('Monthly budget pacing','$8,446/$12,000',70)
 +sec_open('Leads over time')+graph_line(
   [(0,150),(86,138),(172,120),(258,104),(343,96),(429,88),(514,70),(600,58)],
   ['Wk 1','Wk 2','Wk 3','Wk 4','Wk 5','Wk 6','Wk 7','Wk 8'],['40','30','20','10','0'])
 +table('Needs attention',
   [('Campaign','280px'),('Issue','240px'),('Spend','120px'),('CPL','120px'),('Status','130px')],
   [['FLI Retargeting Core Sched','CPL 76% over target','$845','$422.33',brd('Critical')],
    ['FLI AudienceTesting Sched','Paused mid-flight','$4,377','$291.78',by('Review')],
    ['FLI PlayCampaign Core ABO','No delivery for 3 days','—','—',brd('Critical')]],
   sort='Severity',actions=('Export','Resolve')))

PAGES['dashboard']=dict(title='Meta ads',tabs=['Today','Last week','This month','Last month','Custom'],sel=2,
 filters=['All campaigns','All ad sets','All status'],body=
 card_layout([kpi('Blended CPL','$263.94','Above the $240 target','neg','up','9%')],
  [ana('Spend','$8,446'),ana('Meta leads','32'),ana('Impressions','40,244'),
   ana('CTR','1.72%'),ana('CPM','$209.86'),ana('LP rate','87.9%')])
 +progress('Monthly budget pacing','$8,446/$12,000',70)
 +sec_open('CPL by campaign')+graph_bar(
   [('FLI TOF',40,'$180'),('FLI Prospecting',59,'$267'),('FLI AudienceTesting',59,'$268'),
    ('FLI AudienceTesting Sched',65,'$292'),('FLI Retargeting Core',94,'$422')],
   ['$0','$100','$200','$300','$400','$500'])
 +table('Campaigns',
   [('Campaign','280px'),('Spend','120px'),('Leads','110px'),('CPL','130px'),('CTR','110px'),('Status','120px')],
   [['FLI Retargeting Core Sched','$845','2','$422.33','2.40%',bg('Active')],
    ['FLI Prospecting','$1,604','6','$267.26','1.67%',bg('Active')],
    ['FLI TOF','$1,620','9','$179.95','1.90%',bg('Active')],
    ['FLI AudienceTesting Sched','$4,377','15','$291.78','1.63%',bn('Paused')],
    ['FLI AudienceTesting','$2,140','8','$267.50','1.58%',bg('Active')],
    ['FLI PlayCampaign Core ABO','—','—','—','—',bn('Paused')]])
 +with_dropdown('FLI Prospecting',
   [('Attr leads','7'),('Show-ups','4'),('Pending','1'),('$/attr lead','$229.08'),
    ('$/show-up','$400.90'),('Close rate','57%')]))

PAGES['funnel-health']=dict(title='Funnel health',tabs=['This week','This month','Last month'],sel=1,
 filters=['All campaigns','All sources'],body=
 card_layout([kpi('Lead to show-up','39%','11 of 28 attributed leads','neg','down','6%',icon='funnel'),
              kpi('Show-up to close','36%','4 of 11 who showed','pos','up','4%',icon='funnel')],
  [ana('Meta leads','32'),ana('Attr leads','28'),ana('Booked','19'),
   ana('Show-ups','11'),ana('Pending','12'),ana('Closed','4')])
 +progress('Attributed of Meta leads','28/32 matched',88)
 +progress('Booked of attributed','19/28 booked',68)
 +progress('Showed of booked','11/19 attended',58)
 +sec_open('Stage conversion','funnel')+graph_bar(
   [('Lead → attributed',88,'88%'),('Attributed → booked',68,'68%'),
    ('Booked → showed',58,'58%'),('Showed → closed',36,'36%')],
   ['0%','25%','50%','75%','100%'])
 +with_dropdown('All campaigns',
   [('Avg days to book','2.4'),('Avg days to show','6.1'),('No-show rate','42%'),
    ('Reschedules','7'),('Pending > 7d','5'),('Stalled','3')],
   sub=('Drop-off by stage',
   [('At form','4'),('At booking','9'),('At show','8'),('At close','7'),('Recovered','2'),('Net','28')])))

PAGES['creatives']=dict(title='Creatives',tabs=['This month','Last month','All time'],sel=0,
 filters=['All campaigns','All formats','All status'],body=
 card_layout([kpi('Best CPL','$142.10','Static · Founder quote v3','pos','down','21%',icon='sparkle')],
  [ana('Live creatives','24'),ana('Fatigued','6'),ana('Avg CTR','1.72%'),
   ana('Avg freq','1.48'),ana('Thumb-stop','31%'),ana('Hook rate','18%')])
 +sec_open('CTR by creative')+graph_bar(
   [('Founder quote v3',86,'2.9%'),('Carousel — 3 steps',62,'2.1%'),('Static — pricing',48,'1.6%'),
    ('Video — 15s testimonial',41,'1.4%'),('Static — objection',29,'1.0%')],
   ['0%','1%','2%','3%','4%'])
 +table('Creative performance',
   [('Creative','280px'),('Format','130px'),('Spend','120px'),('CPL','120px'),('Freq','100px'),('Status','120px')],
   [['Founder quote v3','Static','$1,204','$142.10','1.21',bg('Scaling')],
    ['Carousel — 3 steps','Carousel','$986','$197.20','1.44',bg('Active')],
    ['Static — pricing','Static','$1,510','$251.66','1.62',by('Watch')],
    ['Video — 15s testimonial','Video','$2,140','$305.71','1.88',brd('Fatigued')],
    ['Static — objection','Static','$640','$320.00','2.10',brd('Fatigued')]],
   sort='CPL',actions=('Export','New creative')))

PAGES['ad-tree']=dict(title='Ad tree',tabs=['This month','Last month'],sel=0,
 filters=['All campaigns','All status'],body=
 card_layout([kpi('Active ads','38','Across 6 campaigns, 14 ad sets','pos','up','12%',icon='tree')],
  [ana('Campaigns','6'),ana('Ad sets','14'),ana('Ads','38'),
   ana('Paused','9'),ana('In review','2'),ana('Rejected','1')])
 +sec_open('FLI Prospecting — 3 ad sets, 11 ads','tree')
 +cells([('Spend','$1,604'),('Leads','6'),('CPL','$267.26'),('CTR','1.67%'),('Freq','1.63'),('Ads live','11')])
 +'<div class="subgroup"><span class="subttl">Ad sets</span>'
 +cells([('Creative testing','$742'),('Lookalike 1%','$531'),('Broad','$331'),
         ('Best CPL','$142.10'),('Worst CPL','$402.00'),('Spread','2.8×')])+'</div></section>'
 +sec_collapsed('FLI TOF — 4 ad sets, 12 ads','tree')
 +sec_collapsed('FLI Retargeting Core Sched — 2 ad sets, 6 ads','tree')
 +table('All ads',
   [('Ad','260px'),('Ad set','200px'),('Spend','110px'),('CPL','120px'),('Status','120px')],
   [['Founder quote v3','Creative testing','$412','$142.10',bg('Active')],
    ['Carousel — 3 steps','Lookalike 1%','$386','$197.20',bg('Active')],
    ['Static — pricing','Broad','$331','$251.66',bg('Active')],
    ['Video — 15s testimonial','Creative testing','$330','$305.71',bn('Paused')],
    ['Static — objection','Broad','$145','$320.00',brd('Rejected')]],
   sort='Spend',actions=('Export','Bulk edit')))

PAGES['creative-rotation']=dict(title='Creative rotation',tabs=['Last 7 days','Last 30 days','Quarter'],sel=1,
 filters=['All campaigns','All formats'],body=
 card_layout([kpi('Days since rotation','11','Target is every 14 days','pos','down','3%',icon='rotate'),
              kpi('Fatigued creatives','6','Frequency above 1.8','neg','up','2%',icon='rotate')],
  [ana('In rotation','24'),ana('Queued','8'),ana('Retired','17'),
   ana('Avg lifespan','19d'),ana('Avg freq','1.48'),ana('Refresh rate','63%')])
 +progress('Rotation cadence','11/14 days',79)
 +sec_open('Frequency by creative','rotate')+graph_bar(
   [('Static — objection',84,'2.10'),('Video — 15s testimonial',75,'1.88'),
    ('Static — pricing',65,'1.62'),('Carousel — 3 steps',58,'1.44'),('Founder quote v3',48,'1.21')],
   ['0','0.5','1.0','1.5','2.0','2.5'])
 +table('Rotation queue',
   [('Creative','280px'),('In rotation','140px'),('Freq','100px'),('CPL trend','140px'),('Action','140px')],
   [['Static — objection','23 days','2.10','↑ 31%',brd('Retire')],
    ['Video — 15s testimonial','19 days','1.88','↑ 18%',by('Refresh')],
    ['Static — pricing','14 days','1.62','↑ 6%',by('Watch')],
    ['Carousel — 3 steps','9 days','1.44','↓ 4%',bg('Keep')],
    ['Founder quote v3','4 days','1.21','↓ 21%',bg('Scale')]],
   sort='Frequency',actions=('Export','Rotate now')))

PAGES['show-up']=dict(title='Show up',tabs=['This week','This month','Last month'],sel=1,
 filters=['All campaigns','All owners','All status'],body=
 card_layout([kpi('Show-up rate','58%','11 of 19 booked calls','neg','down','7%',icon='handshake')],
  [ana('Booked','19'),ana('Showed','11'),ana('No-show','8'),
   ana('Rescheduled','7'),ana('Avg lead time','6.1d'),ana('Reminders sent','54')])
 +progress('Booked calls attended','11/19 attended',58)
 +sec_open('Show-up rate by day','calendar')+graph_line(
   [(0,90),(86,74),(172,96),(258,66),(343,80),(429,58),(514,72),(600,50)],
   ['Mon','Tue','Wed','Thu','Fri','Sat','Sun','Avg'],['80%','60%','40%','20%','0%'])
 +table('Scheduled calls',
   [('Lead','240px'),('Campaign','220px'),('Booked for','160px'),('Owner','140px'),('Status','130px')],
   [['Ryan Mitchell','FLI Prospecting','Tue 10:30','Priya',bg('Showed')],
    ['Dana Okafor','FLI TOF','Tue 14:00','Arjun',bg('Showed')],
    ['Sam Whitfield','FLI Retargeting Core','Wed 09:00','Priya',brd('No-show')],
    ['Lena Ortiz','FLI AudienceTesting','Wed 16:30','Marco',by('Rescheduled')],
    ['Tom Bergen','FLI Prospecting','Thu 11:00','Arjun',bn('Upcoming')]],
   sort='Booked for',actions=('Export','Send reminders')))

PAGES['closed-deals']=dict(title='Closed deals',tabs=['This month','Last quarter','Year'],sel=0,
 filters=['All campaigns','All owners'],body=
 card_layout([kpi('Revenue','$96,000','4 deals closed this month','pos','up','24%',icon='seal'),
              kpi('CAC','$2,112','Against $28,400 blended spend','pos','down','11%')],
  [ana('Deals','4'),ana('Avg deal','$24,000'),ana('Win rate','36%'),
   ana('Sales cycle','21d'),ana('Pipeline','$210K'),ana('LTV:CAC','4.2×')])
 +progress('Quarter revenue target','$96K/$150K',64)
 +sec_open('Revenue by campaign')+graph_bar(
   [('FLI Prospecting',82,'$42K'),('FLI TOF',56,'$28K'),
    ('FLI Retargeting Core',34,'$18K'),('FLI AudienceTesting',16,'$8K')],
   ['$0','$15K','$30K','$45K','$60K'])
 +table('Closed deals',
   [('Account','240px'),('Campaign','220px'),('Value','130px'),('Closed','140px'),('Owner','130px')],
   [['Fraxtional','FLI Prospecting','$34,000','2 Aug','Priya'],
    ['Source Equipment','FLI TOF','$28,000','28 Jul','Arjun'],
    ['Midwest Power Products','FLI Prospecting','$18,000','21 Jul','Priya'],
    ['Bureau','FLI Retargeting Core','$16,000','14 Jul','Marco']],
   sort='Value',actions=('Export','New deal')))

PAGES['audience']=dict(title='Audience',tabs=['This month','Last month','All time'],sel=0,
 filters=['All campaigns','All segments'],body=
 card_layout([kpi('Best segment CPL','$168.40','Ops leads, 50–200 headcount','pos','down','14%',icon='users')],
  [ana('Segments live','9'),ana('Reach','412K'),ana('Frequency','1.48'),
   ana('Overlap','12%'),ana('Saturation','38%'),ana('New reach','61%')])
 +sec_open('CPL by segment','users')+graph_bar(
   [('Ops leads 50–200',38,'$168'),('Founders < 50',52,'$232'),('Growth leads 200+',61,'$271'),
    ('Agencies',74,'$329'),('Broad interest',92,'$408')],
   ['$0','$100','$200','$300','$400','$500'])
 +with_dropdown('Ops leads, 50–200 headcount',
   [('Reach','86K'),('Impressions','12.4K'),('CTR','2.31%'),
    ('Leads','11'),('CPL','$168.40'),('Freq','1.22')],
   sub=('Overlap with other segments',
   [('Founders < 50','8%'),('Growth leads 200+','14%'),('Agencies','3%'),
    ('Broad interest','22%'),('Unique','61%'),('Saturation','31%')]))
 +table('Segments',
   [('Segment','280px'),('Reach','120px'),('Leads','110px'),('CPL','130px'),('Freq','110px'),('Status','120px')],
   [['Ops leads 50–200','86K','11','$168.40','1.22',bg('Scaling')],
    ['Founders < 50','104K','9','$232.10','1.38',bg('Active')],
    ['Growth leads 200+','61K','6','$271.00','1.51',bg('Active')],
    ['Agencies','48K','4','$329.40','1.74',by('Watch')],
    ['Broad interest','113K','2','$408.20','1.92',brd('Saturated')]],
   sort='CPL',actions=('Export','New segment')))

NAV=[('Overview',[('Command Center','gauge','command-center'),('Dashboard','chart','dashboard')]),
     ('Insights',[('Funnel Health','pulse','funnel-health')]),
     ('Creatives',[('Creatives','image','creatives'),('Ad Tree','tree','ad-tree'),
                   ('Creative Rotation','rotate','creative-rotation')]),
     ('Outcomes',[('Show Up','handshake','show-up'),('Closed Deals','seal','closed-deals')]),
     ('Audience',[('Audience','users','audience')])]

nav_html=''.join('<div>'+f'<div class="li li--group">{g}</div>'+''.join(
    f'<a class="li" data-page="{pid}"><svg><use href="#i-{ic}"/></svg>{n}</a>'
    for n,ic,pid in items)+'</div>' for g,items in NAV)

def header(p):
    tabs=''.join(f'<span class="tab{" tab--sel" if i==p["sel"] else ""}">{t}</span>'
                 for i,t in enumerate(p['tabs']))
    fils=''.join(f'<span class="dd">{f}<svg><use href="#i-caret"/></svg></span>' for f in p['filters'])
    return (f'<div class="hdr"><h1>{p["title"]}</h1><div class="toolbar">'
            f'<span class="tabs">{tabs}</span>{fils}'
            f'<span class="refresh"><span>Updated 1h ago</span>'
            f'<button aria-label="Refresh"><svg><use href="#i-refresh"/></svg></button>'
            f'</span></div></div>')

payload=json.dumps({k:{'header':header(v),'body':v['body']} for k,v in PAGES.items()})

CSS = open(os.path.join(os.path.dirname(__file__),'app.css')).read()

HTML = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Meta Ads — Gushwork dashboard system</title>
<link rel="stylesheet" href="../foundation/tokens.css">
<style>{CSS}</style></head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  {sprite()}
</svg>

<div class="shell">
  <aside class="rail">
    <div class="rail__container">
      <div class="rail__title">
        <span class="logotile"><img src="../assets/logo/gushwork-symbol-white.svg" alt=""></span>
        <span class="rail__name">Meta Ads</span>
      </div>
      <div class="groups">{nav_html}</div>
    </div>
    <div class="ucwrap"><div class="usercard">
      <span class="uc__l">
        <span class="uc__av"><img src="../assets/avatar/admin-character.svg" alt=""></span>
        <span class="uc__n"><b>Utsav Singh</b><span>Admin</span></span>
      </span>
      <span class="uc__m"><svg><use href="#i-dots"/></svg></span>
    </div></div>
  </aside>

  <main class="main">
    <div id="hdr"></div>
    <div class="slot" id="slot"></div>
  </main>
</div>

<script>
const PAGES = {payload};
function show(id){{
  const p = PAGES[id]; if(!p) return;
  document.getElementById('hdr').innerHTML = p.header;
  document.getElementById('slot').innerHTML = p.body;
  document.querySelectorAll('.li[data-page]').forEach(a =>
    a.classList.toggle('li--sel', a.dataset.page === id));
  document.getElementById('slot').scrollTop = 0;
  if (location.hash.slice(1) !== id) history.replaceState(null,'','#'+id);
}}
document.querySelectorAll('.li[data-page]').forEach(a =>
  a.addEventListener('click', e => {{ e.preventDefault(); show(a.dataset.page); }}));
show(location.hash.slice(1) in PAGES ? location.hash.slice(1) : 'command-center');
</script>
</body></html>
'''

open(OUT,'w').write(HTML)
open(VAL,'w').write(HTML.replace('href="../foundation/tokens.css"','href="tokens.css"')
                        .replace('src="../assets/','src="assets/'))
print('pages:', len(PAGES), '| html', len(HTML), 'bytes ->', OUT)
