import os, re, json, shutil, html, collections
import markdown

# Repo layout: sources live alongside the generated site at the repo root.
#   corpus/           174 article markdown files  <- source of truth
#   corpus-internal/  notes the AI can use but that never become pages
#   structure/        one JSON per section: intro, "start here", groups, next stage
#   assets/img/       1,326 committed screenshots (NOT generated - never deleted)
#   api/, vercel.json, assets/search.js, assets/article.js  (hand-written, never deleted)
# Everything this script writes is listed in GENERATED below.
SRC = 'corpus'
OUT = '.'

# Only ever delete what we generate. Never rmtree the repo root.
GENERATED_DIRS = [s[0] for s in [
    ('01-getting-started',), ('02-submissions',), ('03-reviewing',), ('04-decisions',),
    ('05-emails',), ('06-programme-exports-reports',), ('07-delegate-registration',),
    ('08-conference-platform',), ('09-add-ons',), ('10-integrations-api',),
    ('11-account-administration',), ('12-for-submitters',),
    ('13-for-reviewers-committee',), ('14-for-attendees-exhibitors',)]]
for d in GENERATED_DIRS:
    shutil.rmtree(d, ignore_errors=True)
for f in ('index.html', '404.html', 'assets/style.css', 'assets/search-index.json',
          'assets/articles.json'):
    if os.path.exists(f):
        os.remove(f)
os.makedirs('assets', exist_ok=True)

SECTIONS = [
    ('01-getting-started', '1', 'Getting started', 'organisers', 'Your account, creating an event, adding your team'),
    ('02-submissions', '2', 'Submissions', 'organisers', 'Design your form and collect abstracts'),
    ('03-reviewing', '3', 'Reviewing', 'organisers', 'Recruit reviewers and assign their work'),
    ('04-decisions', '4', 'Decisions', 'organisers', 'Record outcomes and let submitters know'),
    ('05-emails', '5', 'Emails', 'organisers', 'Create, send and schedule your emails'),
    ('06-programme-exports-reports', '6', 'Programme & reports', 'organisers', 'Build sessions, abstract books and exports'),
    ('07-delegate-registration', '7', 'Registration', 'organisers', 'Tickets, payments, orders and invoices'),
    ('08-conference-platform', '8', 'Conference platform', 'organisers', 'Your event site, live and on demand'),
    ('09-add-ons', '', 'Symposia & Certificates', 'organisers', 'Optional extras you can buy alongside your plan'),
    ('10-integrations-api', '', 'Integrations & API', 'organisers', 'Connect Oxford Abstracts to other tools'),
    ('11-account-administration', '', 'Account administration', 'organisers', 'Your account, billing and archiving'),
    ('12-for-submitters', '', 'Submitting', 'participants', 'Make, edit or pay for your submission'),
    ('13-for-reviewers-committee', '', 'Reviewing', 'participants', 'Complete your reviews and make decisions'),
    ('14-for-attendees-exhibitors', '', 'Attending', 'participants', 'Join the event and find your way around'),
]
SEC_BY_FOLDER = {s[0]: s for s in SECTIONS}

FM = re.compile(r'^---\n(.*?)\n---\n', re.S)

def parse(path):
    raw = open(path, encoding='utf-8').read()
    m = FM.match(raw)
    meta, body = {}, raw
    if m:
        for line in m.group(1).split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip().strip('"')
        body = raw[m.end():]
    body = body.lstrip()
    body = re.sub(r'^#\s+.*\n', '', body, count=1).strip()
    return meta, body

CSS = """
:root{--cream:#EDEBE2;--navy:#101C38;--red:#D0432C;--white:#fff;--muted:#4A5468;--line:rgba(16,28,56,.14);--radius:14px}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation:none!important;transition:none!important}}
body{font-family:'Outfit',sans-serif;font-size:18px;line-height:1.65;color:var(--navy);background:var(--cream)}
.display{font-family:'Gloock',serif;font-weight:400;-webkit-text-stroke:.4px currentColor;letter-spacing:.01em}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
.narrow{max-width:760px}
a{color:var(--navy)}
:focus-visible{outline:3px solid var(--red);outline-offset:3px;border-radius:4px}
header{border-bottom:1px solid var(--line);background:var(--cream);position:sticky;top:0;z-index:20}
/* Top row mirrors oxfordabstracts.com, to the values measured off its header on
   29 July 2026: 92px tall, container 1280px with 80px side padding, 156x37 logo,
   18px links whose hit-areas sit 12px apart, nav left of centre after the logo,
   Sign in and the demo pill right-aligned. The help centre's own search sits on a
   second row so it never competes with the site nav. */
.wrap-nav{max-width:1280px;margin:0 auto;padding:0 80px}
.nav{display:flex;align-items:center;height:92px}
.nav img{width:156px;height:37px;display:block}
.logo{flex-shrink:0}
.site-nav{display:flex;align-items:center;gap:12px;margin-left:52px}
.site-nav>a,.nav-item>button{color:var(--navy);text-decoration:none;font-weight:400;font-size:18px;
  font-family:'Outfit',sans-serif;background:none;border:none;cursor:pointer;padding:8px 12px;
  display:inline-flex;align-items:center;gap:6px;line-height:1.4}
.site-nav>a:hover,.nav-item>button:hover{color:var(--red)}
.caret{width:12px;height:12px;opacity:.75;flex-shrink:0}
.nav-item{position:relative}
/* Mega-menu panels replicated from oxfordabstracts.com: 640px white panel, 8px
   radius, 12px padding, two 308px columns; each item a 48px navy tile with a white
   icon, a semibold title and a muted description; #F5F8FF hover. */
.nav-drop{position:absolute;top:calc(100% - 2px);right:-160px;background:#fff;
  border-radius:8px;padding:12px;width:640px;display:none;z-index:30;
  box-shadow:0 10px 15px -3px rgba(0,0,0,.1),0 4px 6px -4px rgba(0,0,0,.1);
  grid-template-columns:308px 308px}
.nav-item:hover .nav-drop,.nav-item:focus-within .nav-drop{display:grid}
/* The leftmost menu anchors left, or its panel runs 79px off the viewport edge. */
.site-nav .nav-item:first-of-type .nav-drop{left:-12px;right:auto}
.nd-item{display:flex;align-items:flex-start;padding:12px;border-radius:8px;
  text-decoration:none;color:var(--navy);font-size:16px;line-height:1.25}
.nd-item:hover{background:#F5F8FF}
.nd-ico{flex:none;width:48px;height:48px;margin-right:12px;border-radius:8px;
  background:#0A1B3E;display:flex;align-items:center;justify-content:center}
.nd-ico svg{width:24px;height:24px;color:#fff}
.nd-item b{display:block;font-weight:600;margin-bottom:4px}
.nd-item small{display:block;font-size:14px;opacity:.6;line-height:1.35}
.nav-actions{display:flex;align-items:center;gap:12px;margin-left:auto;flex-shrink:0}
.signin{color:var(--navy);text-decoration:none;font-size:18px;padding:8px 12px}
.signin:hover{color:var(--red)}
/* Centred, which at these column widths also puts it over the article: the left rail
   plus its gap (260px) and the right rail plus its gap (236px) are near enough equal
   that page centre and article centre land within 5px. Left-aligned it matched the
   logo but nothing below it - not the rail, not the article - so it read as floating. */
.subnav{display:flex;align-items:center;justify-content:center;padding-bottom:16px}
.subnav .hdr-search{max-width:480px;width:100%}
.btn{display:inline-block;background:var(--red);color:#fff;border:none;cursor:pointer;font-family:'Outfit',sans-serif;font-weight:600;font-size:18px;padding:12px 24px;border-radius:999px;text-decoration:none}
.btn:hover{background:#b53a25}
.hero{padding:60px 0 38px;text-align:center}
.hero h1{font-size:clamp(32px,5vw,52px);margin-bottom:14px}
.lede{font-size:20px;color:var(--muted);max-width:560px;margin:0 auto 28px}
.searchbox{max-width:640px;margin:0 auto;position:relative}
.searchbox form{display:flex;align-items:center;gap:8px;background:var(--white);border:2px solid var(--navy);border-radius:999px;padding:8px 8px 8px 22px;box-shadow:0 6px 24px rgba(16,28,56,.10)}
.searchbox input{flex:1;border:none;background:none;font-family:'Outfit',sans-serif;font-size:19px;color:var(--navy);min-width:0}
.searchbox input::placeholder{color:#8a90a0}
.searchbox input:focus{outline:none}
.chips{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:18px}
.chip{background:none;border:1.5px solid var(--line);border-radius:999px;padding:8px 16px;font-family:'Outfit',sans-serif;font-size:15.5px;color:var(--muted);cursor:pointer}
.chip:hover{border-color:var(--navy);color:var(--navy)}
.results{display:none;max-width:640px;margin:22px auto 0;text-align:left;background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:24px 26px;box-shadow:0 10px 30px rgba(16,28,56,.10)}
.results.show{display:block}
.results h3{font-size:19px;margin-bottom:10px}
.results ul{margin:0;padding-left:20px}
.results li{margin-bottom:8px}
.doors-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:24px 0 8px}
.door{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:28px;text-decoration:none;display:block;transition:transform .15s ease,box-shadow .15s ease}
.door:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(16,28,56,.12)}
/* A single line-drawn icon per door, in the brand red, so the two choices are
   distinguishable at a glance before either is read. */
.door-ico{display:flex;align-items:center;justify-content:center;width:52px;height:52px;
  border-radius:14px;background:rgba(208,67,44,.09);color:var(--red);margin-bottom:16px}
.door-ico svg{width:29px;height:29px;display:block}
.door:hover .door-ico{background:var(--red);color:#fff}
.door h2{font-size:25px;margin-bottom:8px}
.door p{color:var(--muted);font-size:17px}
.door .go{display:inline-block;margin-top:14px;font-weight:600;color:var(--red)}
.section-head{text-align:center;margin-bottom:6px}
.section-head h2{font-size:clamp(26px,3.5vw,36px)}
.section-head p{color:var(--muted);max-width:560px;margin:10px auto 0}
.lifecycle{padding:54px 0 26px}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:32px}
.step{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:22px 20px;text-decoration:none;display:block;transition:transform .15s ease,box-shadow .15s ease}
.step:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(16,28,56,.12)}
.step .num{font-family:'Gloock',serif;font-size:30px;color:var(--red);line-height:1;margin-bottom:10px}
.step h3{font-size:19.5px;margin-bottom:6px}
.step p{font-size:15.5px;color:var(--muted);line-height:1.45}
/* The three non-lifecycle organiser sections - add-ons, integrations, account admin.
   They were plain text links and read as a footnote; people did not find Symposia.
   Now cards, but deliberately smaller and unnumbered, so they sit below the eight
   lifecycle steps rather than alongside them. */
/* The row needed a label. It cannot just say "Add-ons" - only the first of the three
   is one - so the heading names all three and the card drops the prefix. */
.quiet-head{margin:34px 0 12px;font-size:13px;font-weight:600;letter-spacing:.08em;
  text-transform:uppercase;color:var(--muted)}
.quiet-links{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.quiet-links a{display:flex;align-items:center;gap:11px;background:var(--white);
  border:1px solid var(--line);border-radius:12px;padding:15px 18px;text-decoration:none;
  color:var(--navy);font-size:16.5px;font-weight:500;line-height:1.3;
  transition:transform .15s ease,box-shadow .15s ease}
.quiet-links a:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(16,28,56,.10);border-color:var(--navy)}
.quiet-links svg{width:19px;height:19px;flex-shrink:0;color:var(--red)}
.quiet-links .ql-go{margin-left:auto;color:var(--red);font-weight:600;font-size:18px;line-height:1}
@media (max-width:820px){.quiet-links{grid-template-columns:1fr}}
.participants{padding:26px 0 6px}
.part-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}
.popular{padding:48px 0}
.pop-list{max-width:680px;margin:26px auto 0;background:var(--white);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
.pop-list a{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:17px 24px;text-decoration:none;font-size:17.5px;font-weight:500;border-bottom:1px solid var(--line)}
.pop-list a:last-child{border-bottom:none}
.pop-list a:hover{background:#faf9f4}
.pop-list .arrow{color:var(--red);font-weight:700;flex:none}
.human{background:var(--navy);color:var(--cream);padding:54px 0;text-align:center;margin-top:20px}
.human h2{font-size:clamp(26px,3.5vw,34px);margin-bottom:10px}
.human p{color:rgba(237,235,226,.75);max-width:520px;margin:0 auto 24px}
/* The site footer, to the values measured off oxfordabstracts.com: navy, cream
   #EAECE1 at 18px (the site's cream, marginally different from this page's), 1280px
   container at 80px padding, auto-filling 192px columns with a 24px gap, uppercase
   plain-weight h4 group headings, 12px between links, the address in muted green. */
.site-footer{background:#0A1B3E;color:#EAECE1;font-size:18px}
.site-footer .cols{max-width:1280px;margin:0 auto;padding:80px;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(192px,1fr));gap:24px}
.site-footer img{width:156px;height:38px;display:block}
.f-addr{color:#B7C097;line-height:26px;margin-top:18px}
.site-footer h4{font-size:18px;font-weight:400;text-transform:uppercase;margin:0 0 8px}
.site-footer ul{list-style:none;margin:0;padding:0}
.site-footer li{margin:0 0 12px}
.site-footer li a{display:block;color:#EAECE1;text-decoration:none;line-height:18px}
.site-footer li a:hover{text-decoration:underline;text-underline-offset:2px}
@media (max-width:1000px){.site-footer .cols{padding:48px 24px}}
.crumbs{padding:22px 0 0;font-size:16px;color:var(--muted)}
.crumbs a{color:var(--muted);text-decoration:none}
.crumbs a:hover{text-decoration:underline;text-underline-offset:4px}
.article{padding:14px 0 60px}
/* Article layout: a section-scoped rail beside the article on wide screens. The rail
   lists only this section's articles, grouped as the section page groups them - the
   old KB's whole-site tree buried the reader. Below 1100px the rail goes and the
   breadcrumbs carry orientation, as before. */
/* One breakpoint for both rails. A middle band with only the left rail pushed the
   article off-centre, so it no longer lined up with the centred header search - the
   article sat 138px right of it at 1200px. Either both rails or neither. */
.alayout{max-width:808px;margin:0 auto;padding:0 24px}
.acol{min-width:0}
.rail{display:none;position:sticky;top:104px;align-self:start;max-height:calc(100vh - 120px);
  overflow-y:auto;padding:24px 0 40px;font-size:15px}
.rail-over{display:block;font-weight:600;color:var(--navy);text-decoration:none;
  padding:6px 10px;border-radius:7px}
.rail-over:hover{color:var(--red)}
.rail-g{font-size:11.5px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;
  color:var(--muted);margin:16px 0 4px;padding:0 10px}
.rail a:not(.rail-over){display:block;padding:5px 10px;border-radius:7px;
  color:var(--muted);text-decoration:none;line-height:1.35}
.rail a:not(.rail-over):hover{color:var(--navy);background:rgba(16,28,56,.05)}
.rail a.on{color:var(--red);font-weight:600;background:rgba(208,67,44,.08)}
/* The down-arrow on jump links says "this jumps down the page, not to a new one".
   It is an inline SVG, not the U+2193 character: Outfit has no glyph for it and the
   Google Fonts subset renders it zero-width rather than falling back, so the arrows
   were in the markup on all 59 pages and invisible on every one of them. U+2192 in
   .aud-alt and .go is fine - it is only the down arrow that is missing.
   fill="currentColor" on the path keeps the muted/hover colours below working. */
.tj{display:inline-block;width:12px;height:12px;vertical-align:middle;color:var(--muted);margin-right:8px}
.toc a:hover .tj,.pagemap a:hover .tj{color:var(--red)}
/* On this page, as a right-hand rail once there is room for three columns; the
   inline box above the article serves every narrower width. */
.pagemap{display:none}
@media (min-width:1240px){
  /* Both rails 220px so the article column is truly centred in the layout - that
     makes the article's centre line up exactly with the centred header search
     above it, instead of sitting 12px to its right. */
  .alayout{max-width:1300px;padding:0 24px;display:grid;gap:40px;
    grid-template-columns:220px minmax(0,1fr) 220px}
  .rail{display:block}
  .pagemap{display:block;position:sticky;top:104px;align-self:start;
    max-height:calc(100vh - 120px);overflow-y:auto;padding:28px 0 40px;font-size:14.5px}
  .pagemap>span{display:block;font-weight:600;font-size:11.5px;letter-spacing:.07em;
    text-transform:uppercase;color:var(--muted);margin-bottom:8px}
  /* Hanging indent: the arrow sits left of the first line and wrapped lines align
     with the text, not under the arrow. */
  .pagemap a{display:block;padding:4px 0;color:var(--muted);text-decoration:none;
    line-height:1.4;padding-left:20px;text-indent:-20px}
  .pagemap a:hover{color:var(--red)}
  .acol .toc{display:none}
}
.article h1{font-size:clamp(30px,4.5vw,42px);margin:14px 0 10px}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:26px}
.badge{font-size:14px;font-weight:600;padding:4px 12px;border-radius:999px;background:rgba(16,28,56,.06);color:var(--muted)}
.badge.plan{background:rgba(208,67,44,.10);color:var(--red)}
/* Who the article is for. Lifted out of the prose so it reads before the body.
   Every --aud colour clears WCAG AA for white text on the pill. */
.audience{--aud:var(--navy);display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px;margin:-10px 0 24px;padding:12px 16px;border-radius:var(--radius);border:1px solid var(--line);border-left:5px solid var(--aud);background:var(--white)}
.aud-who{font-size:15px;font-weight:600;line-height:1.3;padding:5px 14px;border-radius:999px;background:var(--aud);color:#fff}
.aud-alt{font-size:15px;font-weight:500;color:var(--muted);text-underline-offset:3px}
.aud-alt::after{content:"\\2192";margin-left:.35em}
.aud-alt:hover{color:var(--aud)}
.aud-organisers{--aud:#101C38}
.aud-submitters{--aud:#1F6F5C}
.aud-reviewers{--aud:#5B3E8E}
.aud-attendees{--aud:#8A5A00}
.aud-everyone{--aud:#4A5568}
@media (max-width:520px){.audience{padding:12px 14px}}
.prose{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:34px 38px}
.prose h2{font-family:'Gloock',serif;font-weight:400;font-size:27px;margin:30px 0 12px;-webkit-text-stroke:.3px currentColor}
.prose h2:first-child{margin-top:0}
.prose h3{font-size:21px;margin:24px 0 10px}
.prose p{margin-bottom:16px}
.prose ul,.prose ol{margin:0 0 18px 22px}
.prose li{margin-bottom:8px}
.prose img{max-width:100%;height:auto;border-radius:8px;border:1px solid var(--line);margin:8px 0 20px}
/* Callouts. Sage for a tip, navy for a note. The brand red is the site's link and
   button colour throughout, so a red panel would read as something to click - and
   with 174 notes in the corpus a wall of red would stop meaning "important" by the
   third article. The tint carries the colour; the label text is a darkened version
   of it, because #B7C097 on its own tint is nowhere near AA. */
.callout{display:flex;gap:12px;margin:22px 0;padding:14px 18px 15px 16px;border-radius:var(--radius);border-left:4px solid var(--co);background:var(--co-bg)}
.callout .co-ico{flex:none;width:19px;height:19px;margin-top:3px;color:var(--co-ink)}
.callout .co-b{min-width:0}
.callout .co-label{display:block;font-weight:600;font-size:14.5px;letter-spacing:.02em;color:var(--co-ink);margin-bottom:2px}
.callout p{margin:0}
.callout p+p{margin-top:10px}
.callout p:last-child{margin-bottom:0}
.co-note{--co:#0A1B3E;--co-ink:#0A1B3E;--co-bg:rgba(10,27,62,.055)}
.co-tip{--co:#B7C097;--co-ink:#4E5A31;--co-bg:rgba(183,192,151,.22)}
@media (max-width:520px){.callout{padding:13px 14px 14px 13px;gap:10px}}
.prose a{color:var(--red);text-underline-offset:3px}
.prose strong{font-weight:600}
.prose iframe{max-width:100%;border-radius:8px;border:1px solid var(--line)}
.faq-block{margin-top:34px;padding-top:8px;border-top:2px solid var(--line)}
.sec-intro{max-width:640px;margin:14px auto 0;text-align:center;color:var(--muted);font-size:18.5px}
.start-card{display:block;max-width:680px;margin:30px auto 0;background:var(--navy);color:var(--cream);border-radius:var(--radius);padding:28px 32px;text-decoration:none;transition:transform .15s ease,box-shadow .15s ease}
.start-card:hover{transform:translateY(-3px);box-shadow:0 14px 30px rgba(16,28,56,.22)}
.start-card .tag{display:inline-block;font-size:13px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--red);background:var(--cream);border-radius:4px;padding:2px 9px;margin-bottom:12px}
.start-card h3{font-family:'Gloock',serif;font-weight:400;font-size:26px;margin-bottom:8px;-webkit-text-stroke:.3px currentColor}
.start-card p{color:rgba(237,235,226,.78);font-size:17px}
.group{max-width:820px;margin:44px auto 0}
.group h3{font-family:'Gloock',serif;font-weight:400;font-size:24px;-webkit-text-stroke:.3px currentColor}
.group .gblurb{color:var(--muted);margin:4px 0 16px;font-size:16.5px}
.gcards{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.gcard{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:17px 20px;text-decoration:none;transition:transform .15s ease,box-shadow .15s ease}
.gcard:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(16,28,56,.10)}
.gcard b{display:block;font-weight:600;font-size:17px;margin-bottom:4px}
.gcard span{color:var(--muted);font-size:15px;line-height:1.45}
.next-stage{display:block;max-width:680px;margin:48px auto 40px;text-align:center;background:var(--white);border:1.5px solid var(--navy);border-radius:999px;padding:16px 26px;text-decoration:none;font-weight:600;font-size:17.5px}
.next-stage:hover{background:var(--navy);color:var(--cream)}
@media (max-width:640px){.gcards{grid-template-columns:1fr}}
.sec-list{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:28px;padding-bottom:40px}
.sec-list a{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:18px 22px;text-decoration:none;font-weight:500;font-size:17.5px;transition:transform .15s ease,box-shadow .15s ease}
.sec-list a:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(16,28,56,.10)}
.search-badge{display:inline-flex;align-items:center;gap:8px;background:var(--white);border:1.5px solid rgba(208,67,44,.35);border-radius:999px;padding:7px 16px 7px 12px;margin-bottom:20px;font-size:14.5px;font-weight:600;color:var(--red);letter-spacing:.01em}
.search-badge .spark{width:16px;height:16px;flex:none;animation:sparkle 2.8s ease-in-out infinite}
.search-badge .sep{color:rgba(208,67,44,.4);font-weight:400}
.search-badge .plain{color:var(--muted);font-weight:500}
@keyframes sparkle{0%,100%{opacity:.55;transform:scale(.9) rotate(0deg)}50%{opacity:1;transform:scale(1.08) rotate(8deg)}}
@media (prefers-reduced-motion:reduce){.search-badge .spark{animation:none;opacity:1}}
@media (max-width:520px){.search-badge{font-size:13.5px;padding:6px 13px 6px 10px}.search-badge .sep,.search-badge .plain{display:none}}
.standfirst{font-size:20px;color:var(--muted);margin:0 0 22px;line-height:1.55}
.toc{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:16px 22px;margin-bottom:22px;font-size:16.5px}
/* Direct child only: a bare "span" selector also caught the .tj jump arrows inside
   each link and made them block, so every arrow sat on its own line. */
.toc>span{display:block;font-weight:600;font-size:14px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.toc a{display:block;padding:4px 0;text-decoration:none;color:var(--navy)}
.toc a:hover{color:var(--red)}
.prose h2 .anchor,.prose h3 .anchor{margin-left:8px;font-family:'Outfit',sans-serif;font-size:.75em;color:rgba(16,28,56,.22);text-decoration:none;-webkit-text-stroke:0}
.prose h2 .anchor:hover,.prose h3 .anchor:hover{color:var(--red)}
.prose h2,.prose h3{scroll-margin-top:90px}
.prose ol{counter-reset:step;list-style:none;margin-left:0}
.prose ol>li{counter-increment:step;position:relative;padding-left:44px;margin-bottom:14px}
.prose ol>li::before{content:counter(step);position:absolute;left:0;top:-1px;width:29px;height:29px;border-radius:50%;background:var(--red);color:#fff;font-weight:600;font-size:15px;display:flex;align-items:center;justify-content:center}
.prose ol ol>li::before{background:var(--navy)}
.prose img.zoomable{cursor:zoom-in}
.lightbox[hidden]{display:none}
.lightbox{position:fixed;inset:0;background:rgba(16,28,56,.88);display:flex;align-items:center;justify-content:center;z-index:60;cursor:zoom-out;padding:20px}
.lightbox img{max-width:96vw;max-height:92vh;border-radius:8px;background:#fff}
.prevnext{display:flex;gap:16px;margin-top:30px}
.prevnext a{flex:1;background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:16px 20px;text-decoration:none;font-weight:600;font-size:16.5px;transition:transform .15s ease,box-shadow .15s ease}
.prevnext a:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(16,28,56,.10)}
.prevnext a span{display:block;font-weight:500;font-size:13px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}
.pn-next{text-align:right}
.hdr-search{flex:1;max-width:330px;display:flex;background:var(--white);border:1.5px solid var(--line);border-radius:999px;padding:5px 6px 5px 16px}
.hdr-search input{flex:1;min-width:0;border:none;background:none;font-family:'Outfit',sans-serif;font-size:15.5px;color:var(--navy)}
.hdr-search input:focus{outline:none}
.hdr-search button{background:var(--red);color:#fff;border:none;border-radius:999px;padding:6px 14px;font-family:'Outfit',sans-serif;font-weight:600;font-size:14.5px;cursor:pointer}
.feedback{margin-top:30px;text-align:center;color:var(--muted);font-size:17px}
.feedback button{margin:8px 5px 0;background:none;border:1.5px solid var(--line);border-radius:999px;padding:9px 20px;font-family:'Outfit',sans-serif;font-size:15.5px;cursor:pointer;color:var(--navy)}
.feedback button:hover{border-color:var(--navy)}
.feedback .fb-thanks{margin-top:10px;color:var(--navy);font-weight:500}
.answer-block{margin:0 0 20px;padding-bottom:18px;border-bottom:1px solid var(--line);opacity:0;transform:translateY(6px);transition:opacity .45s ease,transform .45s ease}
.answer-block.revealed,.answer-block.is-loading{opacity:1;transform:none}
.answer-block p{font-size:18px;margin-bottom:10px}
.thinking{display:flex;align-items:center;gap:10px;color:var(--muted);font-size:17px;margin-bottom:14px}
.thinking-text{transition:opacity .18s ease}
/* The loading state is a little book leafing through its pages, and it settles into
   one of two endings rather than being swapped out for a result: a sage bookmark on
   the page when we found the answer, or a blank, unwritten page when we did not.
   The same line of text carries all three states, so the reader watches one object
   resolve instead of watching a spinner disappear. */
.book{position:relative;width:30px;height:22px;flex:none;perspective:60px;transition:transform .4s ease}
.book .cover{position:absolute;inset:0;border:1.5px solid var(--navy);border-radius:2px 4px 4px 2px;background:var(--white)}
.book .spine{position:absolute;left:50%;top:0;bottom:0;width:1.5px;background:var(--navy)}
.book .page{position:absolute;left:50%;top:3px;bottom:3px;width:11px;background:var(--cream);border:1px solid #b9b5a4;border-left:none;transform-origin:left center;animation:flip 2.2s infinite ease-in-out}
.book .page.p2{animation-delay:1.1s;background:#e2dfd2}
@keyframes flip{0%,10%{transform:rotateY(0)}45%,55%{transform:rotateY(-150deg)}90%,100%{transform:rotateY(0)}}
/* Sage, from the brand palette. The darker edges are doing real work: #B7C097 alone
   is too pale to hold its shape at 8px against the white answer card. */
.ribbon{position:absolute;top:-4px;left:68%;width:8px;height:0;box-sizing:border-box;background:#B7C097;border-left:1px solid #96A172;border-right:1px solid #96A172;clip-path:polygon(0 0,100% 0,100% 100%,50% calc(100% - 4px),0 100%);transition:height .35s cubic-bezier(.34,1.3,.64,1);z-index:3}
.blank{position:absolute;right:3px;top:6px;width:10px;height:10px;z-index:2;opacity:0;transition:opacity .5s .15s}
.blank i{display:block;height:1.5px;margin-bottom:2.5px;background:repeating-linear-gradient(90deg,#b9b5a4 0 3px,transparent 3px 5px)}
.thinking.found,.thinking.gap,.thinking.more{color:var(--navy)}
.thinking.found .page,.thinking.gap .page,.thinking.more .page{animation:none;transform:rotateY(0)}
.thinking.found .book{animation:settle .45s ease-out}
.thinking.found .ribbon{height:32px}
/* The gap message is a full sentence and wraps on a phone, so the book aligns to the
   first line rather than to the middle of a three-line paragraph. */
.thinking.gap,.thinking.more{align-items:flex-start}
.thinking.gap .book,.thinking.more .book{margin-top:3px}
.thinking.gap .book{transform:scale(1.15)}
.thinking.gap .blank{opacity:1}
@keyframes settle{0%{transform:scale(1)}40%{transform:scale(1.08)}100%{transform:scale(1)}}
.gap-card p{font-size:16.5px;color:var(--muted);line-height:1.6;margin-bottom:16px}
/* Used on an <a> (the ticket) and a <button> (ask your full question) - the button
   resets are harmless on the link and keep the two visually identical. */
.gap-btn{display:inline-block;background:var(--navy);color:var(--cream);font-weight:600;padding:11px 24px;border-radius:999px;text-decoration:none;border:none;cursor:pointer;font-family:'Outfit',sans-serif;font-size:16px}
.gap-btn:hover{background:#1d2b4f;color:var(--cream)}
/* Did the answer work? Two quiet pills, then either a one-line thank-you or the
   sorry-and-ticket card. The tick is the darkened sage from the Tip callout - the
   pale brand sage vanishes at 15px on white. */
.verdict{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.verdict button{display:inline-flex;align-items:center;gap:8px;background:none;border:1.5px solid rgba(16,28,56,.14);border-radius:999px;padding:9px 18px;font-family:'Outfit',sans-serif;font-size:15px;color:var(--navy);cursor:pointer}
.verdict button:hover{border-color:var(--navy)}
.verdict button svg,.verdict-thanks svg{width:15px;height:15px;flex:none}
/* Sage tick, muted cross. The no must be easy to find and never the inviting one -
   a red cross pulls the eye straight to the option we least want people to need. */
.verdict .v-yes svg,.verdict-thanks svg{color:#4E5A31}
.verdict .v-no svg{color:var(--muted)}
.verdict .v-no:hover{border-color:var(--muted)}
.verdict-thanks{display:flex;align-items:center;gap:8px;margin-top:18px;color:var(--navy);font-weight:500}
/* Only the content below the line fades in - the book itself must not flicker as
   the block goes from loading to answered. */
.ans-in{animation:ansIn .4s ease both}
@keyframes ansIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.skel{display:flex;flex-direction:column;gap:9px}
.skel span{height:13px;border-radius:7px;background:linear-gradient(90deg,rgba(16,28,56,.07) 25%,rgba(16,28,56,.14) 37%,rgba(16,28,56,.07) 63%);background-size:400% 100%;animation:shimmer 1.5s ease-in-out infinite}
@keyframes shimmer{0%{background-position:100% 0}100%{background-position:0 0}}
/* Reduced motion keeps every state legible and drops only the movement: the book
   still takes its bookmark or shows its blank page, just without animating there. */
@media (prefers-reduced-motion:reduce){.answer-block{transition:none;opacity:1;transform:none}.skel span{animation:none;background:rgba(16,28,56,.10)}.book .page,.thinking.found .book,.ans-in{animation:none}.book,.ribbon,.blank{transition:none}}
@media (max-width:640px){.hdr-search{max-width:none}.subnav{flex-wrap:wrap}.prevnext{flex-direction:column}}
/* Below the site-nav breakpoint the marketing links fold away and the help centre's
   own row carries the header, exactly as the main site drops to a burger. */
@media (max-width:1000px){.wrap-nav{padding:0 24px}}
@media (max-width:900px){.site-nav{display:none}.nav{height:76px}.nav-actions{gap:10px}}
/* The site's 18px / 12x24 demo pill plus Sign in plus the logo overflows a phone -
   419px of content in a 375px viewport. Shrink both, then drop the marketing pill,
   which is the least useful of the three to someone reading help docs. */
@media (max-width:700px){
  .nav-actions .btn{font-size:16px;padding:10px 16px}
  .signin{font-size:16px;padding:8px 6px}
}
@media (max-width:560px){.nav-actions .btn{display:none}}
.support{margin-top:30px;background:var(--navy);color:var(--cream);border-radius:var(--radius);padding:30px 34px;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap}
.support h2{font-family:'Gloock',serif;font-weight:400;font-size:25px;margin-bottom:6px;-webkit-text-stroke:.3px currentColor}
.support p{color:rgba(237,235,226,.78);font-size:17px;max-width:460px;margin:0}
.support .btn{flex:none}
@media (max-width:820px){.steps{grid-template-columns:repeat(2,1fr)}.part-grid,.doors-grid,.sec-list{grid-template-columns:1fr}.prose{padding:24px 20px}}
"""

HEAD = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png"></head><body>
<header><div class="wrap-nav nav">
<a class="logo" href="https://oxfordabstracts.com/" aria-label="Oxford Abstracts"><img src="https://a.storyblok.com/f/262790/192x46/f2b614f59c/oa_dark.svg/m/384x0" alt="Oxford Abstracts"></a>
<nav class="site-nav" aria-label="Oxford Abstracts">
@@MENU_PRODUCTS@@
<a href="https://oxfordabstracts.com/pricing/">Pricing</a>
@@MENU_COMPANY@@
@@MENU_RESOURCES@@
</nav>
<div class="nav-actions">
<a class="signin" href="https://app.oxfordabstracts.com/">Sign in</a>
<a class="btn" href="https://oxfordabstracts.com/meeting/">Book a demo</a>
</div>
</div>
{subnav}</header><main>"""

# The help centre's own search sits on a second row so it never competes with the
# site nav. The row only exists where the search does - the home page has the hero
# search instead, so it gets no second row at all.
SUBNAV = """<div class="wrap-nav subnav">
<form class="hdr-search" role="search" action="{root}index.html" method="get">
<input type="search" name="q" placeholder="Ask a question&hellip;" aria-label="Ask a question">
<button type="submit">Ask</button></form></div>"""

CARET = ('<svg class="caret" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">'
         '<path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.17l3.71-3.94a.75.75 0 '
         '111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" '
         'clip-rule="evenodd"/></svg>')

# Callouts. 180 asides arrived from HubSpot as "NB:" or "Please note:" run into the
# prose, where they read as just another sentence - including the one telling you
# reviewer emails are not sent automatically. Two registers only: a note for the
# caveats and a tip for the advice. The brand red is deliberately not used; it is the
# site's link and button colour, and a red panel would read as something to click.
NOTE_ICON = ('<svg class="co-ico" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">'
             '<path fill-rule="evenodd" d="M18 10A8 8 0 112 10a8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 '
             '012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" '
             'clip-rule="evenodd"/></svg>')
TIP_ICON = ('<svg class="co-ico" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">'
            '<path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 '
            '1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 '
            '1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 '
            '110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 '
            '10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>')

# lead word -> (kind, visible label). Longest first, so "Please note" wins over "Note".
CALLOUT_LEADS = [
    ('please note', 'note', 'Note'),
    ('n.b.',        'note', 'Note'),
    ('nb',          'note', 'Note'),
    ('note',        'note', 'Note'),
    ('remember',    'tip',  'Tip'),
    ('tip',         'tip',  'Tip'),
]
CALLOUT_RE = re.compile(
    r'^\s*(' + '|'.join(re.escape(w) for w, _, _ in CALLOUT_LEADS) + r')\b\s*([:.,–-])?\s*',
    re.I)
CALLOUT_COUNTS = collections.Counter()

# The "On this page" jump arrow. An SVG rather than "&darr;" because Outfit has no
# U+2193 glyph and renders it zero-width instead of falling back, so the arrows were
# present in the markup and invisible on all 59 pages that carry a jump list.
JUMP_ARROW = ('<svg class="tj" width="12" height="12" viewBox="0 0 12 12" fill="none" '
              'aria-hidden="true"><path d="M5.01405 1.49072V9.14072L2.4507 6.36572C2.24286 '
              '6.14072 1.9311 6.14072 1.72326 6.36572C1.51542 6.59072 1.51542 6.92822 1.72326 '
              '7.15322L5.18724 10.9032C5.39508 11.1282 5.70684 11.1282 5.91468 10.9032L9.37866 '
              '7.15322C9.48258 7.04072 9.51722 6.89072 9.51722 6.74072C9.51722 6.59072 9.48258 '
              '6.44072 9.37866 6.32822C9.17082 6.10322 8.85907 6.10322 8.65123 6.32822L6.08788 '
              '9.10322V1.49072C6.08788 1.19072 5.8454 0.928223 5.56828 0.928223C5.3258 0.928223 '
              '5.01405 1.19072 5.01405 1.49072Z" fill="currentColor"/></svg>')

# The three header dropdowns, replicated item-for-item from oxfordabstracts.com's
# mega-menus (scraped 29 July 2026): a 48px navy tile with a white heroicon, a
# semibold title and a muted one-line description per item, in a 640px two-column
# white panel. One deliberate difference: the site's "Knowledge Base" item points at
# the old HubSpot KB; ours points home, because this IS the knowledge base.
NAV_MENUS = [
    ('Products', [
        ('https://oxfordabstracts.com/product/abstract-management-software/',
         'Abstract Management Software', 'Manage your submission, review and decision process',
         'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'),
        ('https://oxfordabstracts.com/product/academic-conference-software/',
         'Academic Conference Software', 'All-in-one system for your academic event',
         'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'),
    ]),
    ('Company', [
        ('https://oxfordabstracts.com/about/',
         'About Us', 'Find out more about Oxford Abstracts',
         'M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.3'),
        ('https://oxfordabstracts.com/careers/',
         'Careers', "View open jobs and see what it's like to work with us",
         'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'),
        ('https://oxfordabstracts.com/client-stories/',
         'Client Stories', 'Discover what our clients say about us',
         'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z'),
        ('https://oxfordabstracts.com/integrations-partners/',
         'Integrations & Partners', 'Explore integrations and partners for your event',
         'M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1'),
    ]),
    ('Resources', [
        ('https://oxfordabstracts.com/blog/',
         'Blog', 'See our latest industry articles and product updates',
         'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z'),
        ('{root}index.html',
         'Knowledge Base', 'Find answers and guides for your software questions',
         'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253'),
        ('https://oxfordabstracts.com/resources/videos/',
         'Video Tutorials', 'Watch our informative videos to learn more about Oxford Abstracts',
         'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z'),
        ('https://oxfordabstracts.com/resources/glossary/',
         'Glossary', 'A reference for common terms relating to academic conferences',
         'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253'),
        ('https://oxfordabstracts.com/changelog/',
         'Changelog', 'Latest updates',
         'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'),
        ('https://oxfordabstracts.com/resources/faq/',
         'FAQs', 'Look through our frequently asked questions',
         'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'),
        ('https://oxfordabstracts.com/resources/contact/',
         'Contact Us', 'Here to help with both sales queries and support issues',
         'M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z'),
    ]),
]


def _nav_menu_html():
    out = []
    for label, items in NAV_MENUS:
        rows = ''.join(
            '<a class="nd-item" href="%s"><span class="nd-ico">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="%s"/></svg>'
            '</span><span><b>%s</b><small>%s</small></span></a>'
            % (href, svg, html.escape(title), html.escape(desc))
            for href, title, desc, svg in items)
        out.append(
            '<div class="nav-item"><button type="button" aria-expanded="false">%s{caret}</button>'
            '<div class="nav-drop">%s</div></div>' % (label, rows))
    return out

NAV_PRODUCTS, NAV_COMPANY, NAV_RESOURCES = _nav_menu_html()
HEAD = (HEAD.replace('@@MENU_PRODUCTS@@', NAV_PRODUCTS)
            .replace('@@MENU_COMPANY@@', NAV_COMPANY)
            .replace('@@MENU_RESOURCES@@', NAV_RESOURCES))

# The site footer, replicated column-for-column from oxfordabstracts.com
# (scraped 29 July 2026): navy, cream 18px text, a 1280px container at 80px padding,
# auto-filling 192px columns, the cream logo above the registered address in the
# muted green, then five link groups. The logo is committed in assets/ rather than
# hotlinked, per the images rule.
FOOTER_HTML = """<footer class="site-footer"><div class="cols">
<div><a href="https://oxfordabstracts.com/" aria-label="Oxford Abstracts"><img src="/assets/oa-logo-cream.svg" alt="Oxford Abstracts" width="156" height="38"></a>
<div class="f-addr">Oxford Abstracts Limited<br>Silicon Croft, Saltacre<br>Kilchoan<br>Acharacle PH36 4LP<br>United Kingdom</div></div>
<div><h4>Getting started</h4><ul>
<li><a href="https://oxfordabstracts.com/pricing/">Pricing</a></li>
<li><a href="https://oxfordabstracts.com/meeting/">Book A Demo</a></li>
<li><a href="https://oxfordabstracts.com/resources/contact/">Contact Us</a></li></ul></div>
<div><h4>Product</h4><ul>
<li><a href="https://oxfordabstracts.com/product/abstract-management-software/">Abstract Management Software</a></li>
<li><a href="https://oxfordabstracts.com/product/academic-conference-software/">Academic Conference Software</a></li></ul></div>
<div><h4>Oxford Abstracts</h4><ul>
<li><a href="https://oxfordabstracts.com/about/">About Us</a></li>
<li><a href="https://oxfordabstracts.com/careers/">Careers</a></li>
<li><a href="https://oxfordabstracts.com/client-stories/">Client Stories</a></li></ul></div>
<div><h4>Resources</h4><ul>
<li><a href="https://oxfordabstracts.com/resources/faq/">FAQ</a></li>
<li><a href="https://oxfordabstracts.com/resources/glossary/">Glossary</a></li>
<li><a href="https://oxfordabstracts.com/terms-of-service/">Terms of Service</a></li>
<li><a href="https://oxfordabstracts.com/privacy-policy/">Privacy Policy</a></li>
<li><a href="https://oxfordabstracts.com/cookie-policy/">Cookie Policy</a></li>
<li><a href="https://oxfordabstracts.com/accessibility/">Accessibility</a></li>
<li><a href="https://oxfordabstracts.com/changelog/">Changelog</a></li></ul></div>
<div><h4>Popular posts</h4><ul>
<li><a href="https://oxfordabstracts.com/blog/top-ai-conferences-to-attend-in-2024/">Top AI Conferences In 2025</a></li>
<li><a href="https://oxfordabstracts.com/blog/top-sustainability-conferences-to-attend-in-2024/">Top Sustainability Conferences In 2025</a></li>
<li><a href="https://oxfordabstracts.com/blog/the-best-abstract-management-software-for-2024-a-comparison/">Best Abstract Management Software In 2025</a></li>
<li><a href="https://oxfordabstracts.com/blog/the-best-academic-conference-software-for-2024-a-comparison/">Best Academic Conference Software In 2025</a></li></ul></div>
</div></footer>"""

ARTICLE_FOOT = """</main>
""" + FOOTER_HTML + """
</body></html>"""

SUPPORT_URL = 'https://oxfordabstracts.com/resources/contact-support'

FOOT = ("""</main>
<section class="human"><div class="wrap">
<h2 class="display">Still stuck? Send us a ticket</h2>
<p>Tell us what you're trying to do and one of our support team experts will come back to you
promptly with the solution. No question is too small, and there's no charge for asking.</p>
<a class="btn" href="%s">Create ticket</a>
</div></section>
""" % SUPPORT_URL) + FOOTER_HTML + """
</body></html>"""

SUPPORT_BANNER = """<section class="support">
<div><h2>Didn't solve it? Ask our support team</h2>
<p>No question is too small, and there's no charge for asking. Raise a ticket and
someone who knows the software will pick it up.</p></div>
<a class="btn" href="%s">Create a support ticket</a>
</section>""" % SUPPORT_URL

os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
open(os.path.join(OUT, 'assets/style.css'), 'w', encoding='utf-8').write(CSS)

md = markdown.Markdown(extensions=['extra', 'sane_lists'])
search_index = []
sec_articles = {}

# map old KB slug -> new site path, from redirects.csv
import csv as _csv
OLD2NEW = {}
for old, new in _csv.reader(open('redirects.csv')):
    if old == 'old_url':
        continue
    if '/knowledge/' in old:
        OLD2NEW[old.split('/knowledge/')[-1].strip('/')] = new

def fix_links(body_html, folder):
    """Rewrite corpus-absolute links (/09-add-ons/foo) and any leftover HubSpot
    links into working relative paths within the generated site."""
    def rel(target_path):
        t = target_path.strip('/')
        if not t.endswith('.html'):
            t += '.html'
        if t.startswith(folder + '/'):
            return t[len(folder) + 1:]
        return '../' + t

    # /assets/... -> relative to this page's folder
    body_html = body_html.replace('src="/assets/', 'src="../assets/')
    body_html = body_html.replace('href="/assets/', 'href="../assets/')

    # /NN-section/slug  ->  relative
    body_html = re.sub(r'href="(/\d\d-[a-z0-9\-]+/[^"#?]+)"',
                       lambda m: 'href="%s"' % rel(m.group(1)), body_html)
    # section landing links: /NN-section/  -> index
    body_html = re.sub(r'href="/(\d\d-[a-z0-9\-]+)/?"',
                       lambda m: 'href="%s"' % rel(m.group(1) + '/index'), body_html)
    # leftover HubSpot links (incl. protocol-relative), with or without ?hsLang
    def hub(m):
        slug = m.group(1).strip('/')
        new = OLD2NEW.get(slug)
        return 'href="%s"' % (rel(new) if new else
                              'https://help.oxfordabstracts.com/knowledge/' + slug)
    body_html = re.sub(r'href="(?:https?:)?//help\.oxfordabstracts\.com/knowledge/([^"?#]+)(?:\?[^"]*)?"',
                       hub, body_html)
    return body_html


from bs4 import BeautifulSoup

def slugify(t):
    t = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    return t or 'section'

# Articles carry a sentence naming who they are for, in fourteen slightly different
# wordings inherited from HubSpot. We lift it out of the prose and show it as a
# colour-coded tag under the title instead, so the reader sees it before reading.
# The redirect in the source always pointed at the old HubSpot KB this site
# replaces - two of them at analytics URLs that expired in 2023 - so we send the
# reader to our own landing-page doors instead. Root-absolute: these links have to
# resolve from article pages and from 404.html, which can be served at any path.
# Key -> (tag label, "not you?" prompt, where that prompt goes).
AUDIENCES = {
    'organisers': ('For event organisers',        'Not an organiser?',      '/#participants'),
    'submitters': ('For people making a submission', 'Organising the event?', '/#organisers'),
    'reviewers':  ('For reviewers',               'Organising the event?',  '/#organisers'),
    'attendees':  ('For conference attendees',    'Organising the event?',  '/#organisers'),
    # Everyone: account, login, profile and connection problems apply to every role.
    # Without this, those articles carried no tag at all, which reads as "we forgot"
    # rather than "this one is for you whoever you are".
    'everyone':   ('For everyone',                'Browse by role',         '/'),
}
# The audience sentence came over from HubSpot in two families - "The guidance below
# is for X" and the shorter "This guide/article is for X" - behind an optional
# "NB:" / "Note:" / "Please note:", and sometimes as "this Knowledge Base article".
# "this information is for ..." is a third family, 32 articles strong. It was missing
# from the subject fragment, so those articles were never classified AND never
# stripped - they kept a shouty "This information is for Admins ONLY!" line in the
# prose and rendered with no audience tag at all.
# Classification and removal are built from the SAME subject fragment below: when they
# drifted apart, articles were classified by an unanchored search, tagged, and then
# had nothing stripped because the removal was anchored at the paragraph start.
# Comma included deliberately: one article writes "Please note, this information is
# for Admins Only!". This is safe here because AUD_LEAD only ever fires as part of a
# full audience sentence - it is NOT the callout label logic, where a trailing comma
# means the lead is part of the sentence's own grammar and must be left alone.
AUD_LEAD = r'(?:NB|Please\s+note|Note)\s*[:.,]?\s*'
AUD_SUBJ = r'(?:the\s+guidance\s+below|th(?:is|e)\s+(?:knowledge\s+base\s+)?(?:guide|article|information))'

def _aud(keyword):
    return AUD_SUBJ + r'\s+is\s+for\s+[^.!]*' + keyword

# Ordered: the first pattern that matches the paragraph text wins.
AUDIENCE_PATTERNS = [
    ('organisers', _aud(r'(?:admin|organiser)')),
    ('submitters', _aud(r'submit')),
    ('reviewers',  _aud(r'reviewer')),
    ('attendees',  _aud(r'(?:attendee|delegate)')),
]
# The sentence naming the audience, and the "if you are someone else, go here"
# sentence that usually follows it. Both are removed; anything else in the
# paragraph is left alone, because a few carry an extra note about plan limits.
# Only "If you are ..." is audience routing. "If you experience any issues ..."
# tells a reviewer to contact their event administrator - that is support routing
# and has to stay in the prose, so it is deliberately not matched here.
# Ends at a full stop, an exclamation mark, or the end of the paragraph - several of
# these sentences carry no terminator at all.
AUD_SENTENCE = re.compile(
    r'^\s*(?:' + AUD_LEAD + r')?' + AUD_SUBJ + r'\s+is\s+for\s*[^.!]*(?:[.!]|$)\s*', re.I)
# Runs to the end of the paragraph rather than to the first full stop: the usual
# wording is "If you are an end user (eg. submitter, reviewer, delegate etc),
# please click here." and a first-full-stop match stops dead inside "(eg." and
# strands the rest. The redirect is always the last sentence, so this is safe.
AUD_REDIRECT = re.compile(
    r'^\s*If you are .*$', re.I | re.S)
# Two articles put the redirect in a paragraph of its own, so it never reaches
# AUD_REDIRECT above. Matched narrowly and only on articles that already produced
# a tag: of the 16 standalone "If you are ..." lines in the corpus, the other 14
# are real content ("If you are on the Free Plan you cannot add any questions").
AUD_STANDALONE = re.compile(
    r'^\s*If you are the administrator of an event please see\b.*$', re.I | re.S)


def extract_audience(root, soup):
    """Strip every 'who this is for' paragraph from the prose and return the audience
    key of the first - or None when the article does not carry one. Five articles
    repeat the sentence further down the page, so this cannot stop at the first hit."""
    found = None
    for p in root.find_all('p'):
        text = p.get_text(' ', strip=True)
        key = next((k for k, pat in AUDIENCE_PATTERNS if re.search(pat, text, re.I)), None)
        if not key:
            continue
        if found is None:
            found = key

        # Rebuild the paragraph without the audience and redirect sentences. A few
        # carry a further note (plan limits, who to contact) that has to survive.
        rest = AUD_SENTENCE.sub('', text, count=1)
        rest = AUD_REDIRECT.sub('', rest, count=1).strip()
        if rest:
            p.clear()
            p.append(soup.new_string(rest))
        else:
            p.decompose()

    if found:
        for p in root.find_all('p'):
            if AUD_STANDALONE.match(p.get_text(' ', strip=True)):
                p.decompose()
    return found


# Alt text. Every screenshot used to inherit the nearest heading, so a page with 39
# images had 3 alt texts between them and a screen reader announced the same phrase
# a dozen times running. Each image sits directly under the step it illustrates
# (measured: all 1,343 have preceding text, 93% of it a paragraph), so the step is
# what the picture shows. We strip the imperative lead-in - "Click on the Create an
# Account button" -> "the Create an Account button" - so the alt names what is
# pictured instead of repeating the instruction word for word to someone who has
# just heard it. This is derived from surrounding text, not from looking at the
# images: it makes them distinct and specific, not truly described.
ALT_LEADIN = re.compile(
    r'^(?:next,?\s+|then\s+|now\s+|finally,?\s+|you (?:can|will|should|need to)\s+)*'
    r'(?:click(?:ing)?(?:\s+on)?(?:\s+the)?|select(?:ing)?|choose|go\s+to|navigate\s+to'
    r'|open(?:ing)?|press|tap|see|find|head\s+to)\s+', re.I)
ALT_MAX = 100          # the descriptive part
ALT_HEAD_MAX = 40      # the heading prefix used only to break a tie
ALT_HARD_MAX = 140     # the finished string, whatever it is made of
ALT_FILE_NOUN = re.compile(
    r'^(?:screen\s?shot|image|img|photo|picture|unnamed|untitled)\b', re.I)


def is_junk_alt(text):
    """True for alt text carried over from HubSpot that names the file rather than
    the picture - "Screenshot 2026-05-14 at 12.38.38", "image001.png", "unnamed".
    Such alt text is treated as absent so a described one is derived instead."""
    t = re.sub(r'\.(?:png|jpe?g|webp|gif|svg)$', '', text.strip(), flags=re.I)
    t = ALT_FILE_NOUN.sub('', t)
    t = re.sub(r'\b(?:at|on|am|pm|copy|final|v\d+)\b', ' ', t, flags=re.I)
    return len(re.sub(r'[^A-Za-z]', '', t)) < 3


def _preceding_text(img):
    """Text of the nearest element before the image that is not itself an image."""
    node = img
    while node is not None:
        prev = node.previous_sibling
        while prev is not None and not getattr(prev, 'name', None):
            prev = prev.previous_sibling
        if prev is not None:
            if prev.get_text(strip=True) and not prev.find('img'):
                # Inside a callout, only the note itself is context - not its "Note"
                # label, which would otherwise open the alt text of every screenshot
                # that happens to follow one.
                if prev.name == 'aside' and 'callout' in (prev.get('class') or []):
                    body = ' '.join(q.get_text(' ', strip=True) for q in prev.find_all('p'))
                    if body.strip():
                        return body.strip()
                return prev.get_text(' ', strip=True)
            node = prev
            continue
        node = node.parent
        if node is None or node.name in ('body', '[document]'):
            return ''
    return ''


def _trim(text, limit):
    text = ' '.join(text.split()).strip(' –—-:;,')
    if len(text) > limit:
        cut = text[:limit].rsplit(' ', 1)[0]
        text = cut.rstrip(' .,;:') + '…'
    return text.rstrip('.')


def derive_alt(img, heading, used):
    """Alt text naming what this screenshot shows, unique within the page."""
    context = _preceding_text(img)
    stripped = ALT_LEADIN.sub('', context, count=1).strip()
    # Falling back keeps a too-short remainder (e.g. "Next.") from becoming the alt.
    body = stripped if len(stripped) >= 12 else (context or heading)

    candidates = ['Screenshot: %s' % _trim(body, ALT_MAX)]
    if heading and heading.lower() not in body.lower():
        candidates.append('Screenshot: %s — %s'
                          % (_trim(heading, ALT_HEAD_MAX), _trim(body, ALT_MAX)))
    candidates = [_trim(c, ALT_HARD_MAX) for c in candidates]
    for alt in candidates:
        if alt not in used:
            used.add(alt)
            return alt
    # Still identical to an earlier image: say which one, rather than repeat blindly.
    # The counter is part of the length budget, not bolted on after it.
    base, n = candidates[-1], 2
    while True:
        suffix = ' (%d)' % n
        alt = _trim(base, ALT_HARD_MAX - len(suffix)) + suffix
        if alt not in used:
            break
        n += 1
    used.add(alt)
    return alt


def lead_sentence(body_html):
    """First real sentence of an article, used as its section-page card description
    when the article has no standfirst.

    Parsed rather than regex-stripped, and taken from one block at a time.

    Blanking tags with a regex flattened the whole article into a single string, so
    two things leaked in: the <a class="anchor">#</a> that enrich_body appends to
    every heading, and the text of the *next* block once the current one had no full
    stop - "…following the instructions below # This article is for Admins ONLY."

    Headings are deliberately still eligible. Most of these articles open with a
    descriptive '## Create a striking and visually engaging program.' which is the
    best one-line summary the article has; skipping headings dropped 150 good
    descriptions in favour of the menu path underneath them.
    """
    soup = BeautifulSoup(body_html, 'lxml')
    root = soup.body or soup
    for a in root.find_all('a', class_='anchor'):
        a.decompose()
    # A note is a caveat about the article, never a description of it. Left in, a
    # boxed "NB: emails are not sent automatically" became the card description for
    # the article on notifying reviewers.
    for c in root.find_all(class_='callout'):
        c.decompose()

    for el in root.find_all(['h2', 'h3', 'h4', 'p', 'li']):
        text = ' '.join(el.get_text(' ', strip=True).split())
        if len(text) < 20:
            continue
        # "Skip to written instructions" is navigation, not a description of anything.
        link_text = sum(len(a.get_text(' ', strip=True)) for a in el.find_all('a'))
        if link_text > 0.6 * len(text):
            continue
        m = re.match(r'(.{20,150}?[.!?])(\s|$)', text)
        return m.group(1) if m else text[:120]
    return ''


def _strip_callout_label(p, soup):
    """Remove a leading "NB:" from a callout paragraph, whether it is plain text or a
    bolded <strong>Please note:</strong>. Returns True if it removed one."""
    first = next((c for c in p.contents
                  if not (isinstance(c, str) and not c.strip())), None)
    if first is None:
        return False
    if isinstance(first, str):
        rest = CALLOUT_RE.sub('', str(first), count=1)
        if rest == str(first):
            return False
        first.replace_with(rest)
        return True
    # em/i as well as strong/b: several of these were written "*Please note if you
    # are a Multi-Stage event…*", italicising the whole sentence.
    if first.name in ('strong', 'b', 'em', 'i'):
        t = first.get_text(' ', strip=True)
        m = CALLOUT_RE.match(t)
        if not m:
            return False
        if m.end() == len(t):                # the bold run is the label and nothing else
            first.decompose()
            nxt = next((c for c in p.contents if isinstance(c, str)), None)
            if nxt is not None:
                nxt.replace_with(str(nxt).lstrip(' :–-'))
            return True
        # the label and the note are inside one bold run: "**Please note: IMPORTANT.**"
        inner = next((c for c in first.descendants if isinstance(c, str) and c.strip()), None)
        if inner is not None:
            rest = CALLOUT_RE.sub('', str(inner), count=1)
            if rest != str(inner):
                inner.replace_with(rest)
                return True
    return False


def _drop_leading_that(p):
    """"Please note, that you have thirty days" reads as a fragment once the label is
    gone, so the "that" goes with it."""
    node = next((c for c in p.descendants if isinstance(c, str) and c.strip()), None)
    if node is None:
        return
    s = str(node)
    m = re.match(r'^(\s*)that\s+', s, re.I)
    if m:
        node.replace_with(m.group(1) + s[m.end():])


def _capitalise_first(p):
    """After the label comes off, "this will add the user" needs its capital back.
    Words carrying an inner capital (iPhone, eTicket) are left alone."""
    node = next((c for c in p.descendants if isinstance(c, str) and c.strip()), None)
    if node is None:
        return
    s = str(node)
    i = len(s) - len(s.lstrip())
    ch = s[i:i + 1]
    if ch.islower() and not any(x.isupper() for x in s[i:].split(' ', 1)[0]):
        node.replace_with(s[:i] + ch.upper() + s[i + 1:])


def wrap_callouts(root, soup, counts):
    """Lift "NB:" and "Please note:" paragraphs out of the prose into a labelled box.

    The label is only stripped when it is a clean one - "NB:" or a bolded
    "**Please note:**". Where the lead runs into the sentence's own grammar
    ("Please note, that you have thirty days", "Remember to check the box") the text
    is left exactly as written, because cutting it produced fragments like "that you
    have thirty days to pay". Those paragraphs just gain the label above them.

    The icon goes in as a placeholder and is swapped for real SVG after the tree is
    serialised: both available parsers lowercase viewBox to viewbox, which silently
    breaks the icon's scaling.
    """
    for p in list(root.find_all('p')):
        # Testing for a top-level parent missed the "Common questions" block, which is
        # wrapped in a div.faq-block. What actually disqualifies a paragraph is being
        # inside something a box cannot sit in - a list item, a quote, a table cell.
        if p.find_parent(['li', 'blockquote', 'td', 'th', 'aside']):
            continue
        m = CALLOUT_RE.match(p.get_text(' ', strip=True))
        if not m:
            continue
        word = m.group(1).lower()
        kind, label = next((k, l) for w, k, l in CALLOUT_LEADS if w == word)
        # The label belongs in the header, not repeated in the sentence, so the lead
        # comes off whatever follows it - "NB:", "NB,", "NB -" or a bare "NB". The one
        # thing that cannot be cut is a lead doing duty as the sentence's verb:
        # "Remember to check the box" would be left as "to check the box".
        # Lowercase "to" only: "Remember to check the box" is the lead doing duty as
        # the verb, but "NB: To become familiar with the tables, see…" is already a
        # sentence and the capital says so.
        rest = CALLOUT_RE.sub('', p.get_text(' ', strip=True), count=1)
        if rest.startswith('to '):
            counts['lead is the verb, kept'] += 1
        elif _strip_callout_label(p, soup):
            _drop_leading_that(p)
            _capitalise_first(p)
            counts['stripped'] += 1
        else:
            counts['could not strip'] += 1

        # "NB:" alone on its own line with the note in the block underneath is the
        # commonest HubSpot shape - 7 of these. Stripping the label empties the
        # paragraph, so absorb the block below it, or there is nothing to box.
        if not p.get_text(strip=True):
            nxt = p.find_next_sibling()
            p.decompose()
            if nxt is None or nxt.name != 'p' or not nxt.get_text(strip=True):
                counts['bare label, nothing to box'] += 1
                continue
            p = nxt
            counts['label on its own line'] += 1
        counts[kind] += 1

        aside = soup.new_tag('aside')
        aside['class'] = ['callout', 'co-' + kind]
        holder = soup.new_tag('div')
        holder['class'] = ['co-b']
        lab = soup.new_tag('span')
        lab['class'] = ['co-label']
        lab.string = label
        p.insert_before(aside)
        # An empty element, not a text placeholder: a text one is picked up by
        # _preceding_text and ends up inside an image's alt attribute, where the
        # post-serialisation swap then injects raw SVG and breaks the markup.
        slot = soup.new_tag('i')
        slot['class'] = ['co-slot-' + kind]
        aside.append(slot)
        holder.append(lab)
        holder.append(p.extract())
        aside.append(holder)


def enrich_body(body_html, title):
    """Add heading ids + anchor links, contextual alt text, lazy click-to-enlarge
    images, an on-this-page list for long articles, lift a short opening paragraph
    out as a standfirst, and pull the 'who this is for' sentence out as a tag.
    Returns (standfirst, audience, toc_html, body_html)."""
    soup = BeautifulSoup(body_html, 'lxml')
    root = soup.body or soup
    audience = extract_audience(root, soup)

    # Legacy "Skip to:" navigation from HubSpot: paragraphs that are nothing but
    # in-page fragment links, and their "Skip to:" label lines. 380 of their targets
    # no longer exist, and the generated "On this page" box does the same job without
    # rotting - so every such paragraph goes, working or not.
    for p in root.find_all(['p', 'h2', 'h3', 'h4']):
        text = p.get_text(' ', strip=True)
        links = p.find_all('a')
        all_frag = bool(links) and all((a.get('href') or '').startswith('#') for a in links)
        link_text = sum(len(a.get_text(' ', strip=True)) for a in links)
        only_links = all_frag and len(text) - link_text <= max(12, len(links) * 3)
        says_skip = re.match(r'^skip to\b', text, re.I) and (all_frag or not links)
        if only_links or says_skip:
            p.decompose()

    # Callouts run BEFORE the standfirst lift on purpose. 40 articles open on an
    # "NB:", which the lift was taking as the article's summary - so the section-page
    # card for "Notifying reviewers" described the article as a warning that the
    # emails do not send themselves. Boxed first, those stop being eligible.
    wrap_callouts(root, soup, CALLOUT_COUNTS)

    # standfirst: lift the opening paragraph when it is short and text-only
    standfirst = ''
    first = None
    for child in root.children:
        if getattr(child, 'name', None):
            first = child
            break
    if first is not None and first.name == 'p' and not first.find('img'):
        txt = first.get_text(' ', strip=True)
        if 0 < len(txt) <= 300:
            standfirst = txt
            first.decompose()

    # headings: ids + visible anchors. h4 is included because a fair few imported
    # articles use it (or bold pseudo-headings above it) as their only structure -
    # those are exactly the ones that carried a hand-made "Skip to:" list.
    seen, by_level = {}, {'h2': [], 'h3': [], 'h4': []}
    for h in root.find_all(['h2', 'h3', 'h4']):
        text = h.get_text(' ', strip=True)
        if not text:
            continue
        base = slugify(text)
        n = seen.get(base, 0)
        seen[base] = n + 1
        hid = base if n == 0 else f'{base}-{n+1}'
        h['id'] = hid
        a = soup.new_tag('a', href='#' + hid)
        a['class'] = 'anchor'
        a['aria-label'] = 'Link to this section'
        a.string = '#'
        h.append(a)
        by_level[h.name].append((hid, text.rstrip('#').strip()))

    # The jump list uses the highest heading level with at least two entries, so an
    # h4-structured article gets the same box an h2-structured one does.
    entries = next((v for v in (by_level['h2'], by_level['h3'], by_level['h4'])
                    if len(v) >= 2), [])
    toc = ('', '')
    if sum(len(v) for v in by_level.values()) >= 4 and entries:
        # The same jump list is rendered twice: an inline box above the article on
        # narrow screens, and a plain right-hand rail on wide ones where it can stay
        # in reach all the way down. The down-arrow says "this jumps, not navigates".
        items = ''.join(
            f'<a href="#{hid}">{JUMP_ARROW}{html.escape(t)}</a>'
            for hid, t in entries[:14])
        toc = (f'<nav class="toc" aria-label="On this page"><span>On this page</span>{items}</nav>',
               f'<aside class="pagemap" aria-label="On this page"><span>On this page</span>{items}</aside>')

    # images: lazy, contextual alt where missing, click-to-enlarge
    last_heading = title
    used_alts = set()
    for el in root.find_all(['h2', 'h3', 'img']):
        if el.name in ('h2', 'h3'):
            last_heading = el.get_text(' ', strip=True).rstrip('#').strip()
        else:
            el['loading'] = 'lazy'
            existing = (el.get('alt') or '').strip()
            if existing and not is_junk_alt(existing):
                used_alts.add(existing)   # so a derived alt cannot collide with it
            else:
                el['alt'] = derive_alt(el, last_heading, used_alts)
            el['class'] = (el.get('class') or []) + ['zoomable']
            el['tabindex'] = '0'

    # Any in-page link whose target no longer exists becomes plain text. These are
    # HubSpot-era anchors (#TEX, #SQ...) whose targets did not survive conversion -
    # a link that scrolls nowhere reads as the page being broken.
    ids = {el.get('id') for el in root.find_all(attrs={'id': True})}
    for a in root.find_all('a', href=True):
        if (a['href'].startswith('#') and a['href'][1:] not in ids
                and 'anchor' not in (a.get('class') or [])):
            a.unwrap()

    inner = root.decode_contents() if root.name == 'body' else str(soup)
    inner = (inner.replace('<i class="co-slot-note"></i>', NOTE_ICON)
                  .replace('<i class="co-slot-tip"></i>', TIP_ICON))
    return standfirst, audience, toc, inner

for folder, num, name, aud, blurb in SECTIONS:
    src_dir = os.path.join(SRC, folder)
    if not os.path.isdir(src_dir):
        continue
    os.makedirs(os.path.join(OUT, folder), exist_ok=True)
    arts = []
    parsed = []
    meta_by_slug = {}
    first_sentence = {}
    for fn in sorted(os.listdir(src_dir)):
        if not fn.endswith('.md'):
            continue
        meta, body = parse(os.path.join(src_dir, fn))
        slug = fn[:-3]
        md.reset()
        body_html = md.convert(body)
        body_html = fix_links(body_html, folder)
        body_html = body_html.replace('<h2>Common questions</h2>',
                                      '<div class="faq-block"><h2>Common questions</h2>')
        if 'faq-block' in body_html:
            body_html += '</div>'
        title = meta.get('title', slug.replace('-', ' ').title())
        standfirst, audience, toc, body_html = enrich_body(body_html, title)
        # Most articles state their audience in the prose and it is lifted out above.
        # Where they do not, fall back to the frontmatter, so a deliberate value is
        # honoured rather than the article silently rendering with no tag at all.
        if not audience:
            fm_aud = (meta.get('audience') or '').strip().lower()
            if fm_aud in AUDIENCES:
                audience = fm_aud
        parsed.append((slug, title, meta.get('plan', ''), standfirst, audience, toc, body_html))
        meta_by_slug[slug] = meta
        first_sentence[slug] = lead_sentence(body_html)

    # The section rail: this section's articles, grouped as the section page groups
    # them, with the current article highlighted. Section-scoped on purpose - the old
    # KB's whole-site tree buried the reader; fourteen sections of links is not
    # orientation. Anything not yet placed in a group appears under "More guides",
    # so a new article is never invisible here.
    titles_by_slug = {sl: t for (sl, t, _pl, _sf, _au, _tc, _bh) in parsed}
    _sp = os.path.join('structure', folder + '.json')
    sec_struct = json.load(open(_sp, encoding='utf-8')) if os.path.exists(_sp) else None

    def rail_html(cur):
        """The rail shows only the group the current article belongs to - its
        immediate siblings, Miro-style - never the whole section. A first cut listed
        all of Submissions' 30 articles and read as a wall; the section page remains
        the one place with the full curated map, one click up."""
        if not sec_struct:
            return ''
        listed = set()
        group_title, group_slugs = None, []
        for g in sec_struct.get('groups', []):
            slugs = [sl for sl in g.get('slugs', []) if sl in titles_by_slug]
            listed.update(slugs)
            if cur in slugs:
                group_title, group_slugs = g.get('title', ''), slugs
        if group_title is None:
            extras = [sl for sl in titles_by_slug if sl not in listed]
            if cur not in extras:
                return ''
            group_title, group_slugs = 'More guides', extras
        links = ''.join('<a%s href="%s.html">%s</a>'
                        % (' class="on"' if sl == cur else '', sl,
                           html.escape(titles_by_slug[sl]))
                        for sl in group_slugs)
        return ('<aside class="rail" aria-label="Related articles">'
                '<a class="rail-over" href="index.html">&larr; %s overview</a>'
                '<div class="rail-g">%s</div>%s</aside>'
                % (html.escape(name), html.escape(group_title), links))

    for i, (slug, title, plan, standfirst, audience, toc, body_html) in enumerate(parsed):
        badges = ['<span class="badge">%s</span>' % html.escape(name)]
        label = None
        if plan.startswith('add-on: symposia'):
            label = 'Symposia add-on'
        elif plan.startswith('add-on: certificates'):
            label = 'Certificates add-on'
        elif plan.startswith('add-on: multi-stage'):
            label = 'Multi-stage add-on'
        elif plan.startswith('professional'):
            label = 'Professional Conference'
        elif plan.startswith('standard conference'):
            label = 'Conference plans'
        elif plan.startswith('abstract management'):
            label = 'Abstract Management and above'
        if label:
            badges.append('<span class="badge plan">%s</span>' % label)

        prev_a = next_a = ''
        if i > 0:
            pt, ps = parsed[i-1][1], parsed[i-1][0]
            prev_a = f'<a class="pn-prev" href="{ps}.html"><span>Previous</span>{html.escape(pt)}</a>'
        if i < len(parsed) - 1:
            nt, ns = parsed[i+1][1], parsed[i+1][0]
            next_a = f'<a class="pn-next" href="{ns}.html"><span>Next</span>{html.escape(nt)}</a>'
        else:
            ni = SECTIONS.index((folder, num, name, aud, blurb)) + 1
            if ni < len(SECTIONS) and SECTIONS[ni][3] == aud:
                nf, _, nn, _, _ = SECTIONS[ni]
                next_a = f'<a class="pn-next" href="../{nf}/index.html"><span>Next section</span>{html.escape(nn)}</a>'
        prevnext = f'<nav class="prevnext" aria-label="Article navigation">{prev_a}{next_a}</nav>' if (prev_a or next_a) else ''

        toc_inline, toc_rail = toc
        stand_html = f'<p class="standfirst">{html.escape(standfirst)}</p>' if standfirst else ''
        aud_html = ''
        if audience:
            a_label, a_prompt, a_href = AUDIENCES[audience]
            aud_html = (
                f'<p class="audience aud-{audience}">'
                f'<span class="aud-who">{html.escape(a_label)}</span>'
                f'<a class="aud-alt" href="{a_href}">{html.escape(a_prompt)}</a></p>')
        lr = meta_by_slug.get(slug, {}).get('last_reviewed', '')
        if lr:
            try:
                import datetime as _dt
                # Build the day by hand: '%-d' is a glibc extension and raises on Windows.
                _d = _dt.date.fromisoformat(lr)
                lr_h = '%d %s %d' % (_d.day, _d.strftime('%B'), _d.year)
            except Exception:
                lr_h = lr
            badges.append('<span class="badge reviewed">Last reviewed %s</span>' % lr_h)
        page = HEAD.format(title=html.escape(title) + ' | Oxford Abstracts Help',
                           desc=html.escape(standfirst or title), root='../',
                           subnav=SUBNAV.format(root='../'), caret=CARET)
        page += f"""<div class="alayout">
{rail_html(slug)}<div class="acol"><div class="crumbs">
<a href="../index.html">Help centre</a> &nbsp;›&nbsp; <a href="index.html">{html.escape(name)}</a></div>
<article class="article">
<h1 class="display">{html.escape(title)}</h1>
<div class="badges">{''.join(badges)}</div>
{aud_html}
{stand_html}
{toc_inline}
<div class="prose">{body_html}</div>
{SUPPORT_BANNER if aud == 'organisers' else ''}
<div class="feedback" data-path="{folder}/{slug}.html">
<p>Did this page solve it?</p>
<div class="fb-row"><button type="button" data-fb="yes">Yes</button><button type="button" data-fb="no">No</button></div>
<div class="fb-reasons" hidden>
<button type="button" data-reason="confusing">Confusing</button>
<button type="button" data-reason="out-of-date">Out of date</button>
<button type="button" data-reason="missing-details">Missing details</button>
<button type="button" data-reason="not-what-i-searched">Not what I searched for</button>
</div>
<p class="fb-thanks" hidden>Thanks — this helps us fix it.</p>
</div>
{prevnext}
</article></div>{toc_rail}</div>
<div class="lightbox" id="lightbox" hidden><img alt=""></div>
<script src="../assets/article.js"></script>"""
        page += ARTICLE_FOOT
        open(os.path.join(OUT, folder, slug + '.html'), 'w', encoding='utf-8').write(page)
        arts.append((title, slug))
        plain = re.sub(r'<[^>]+>', ' ', body_html)
        plain = ' '.join(plain.split())
        search_index.append({
            'title': title, 'path': '%s/%s.html' % (folder, slug),
            'section': name, 'audience': aud, 'plan': plan,
            'summary': (standfirst or plain)[:220],
        })
    sec_articles[folder] = arts

    # section index page
    struct_path = os.path.join('structure', folder + '.json')
    by_slug_p = {sl: (t, st) for (sl, t, pl, st, au, tc, bh) in parsed}
    page = HEAD.format(title=html.escape(name) + ' | Oxford Abstracts Help',
                       desc=html.escape(blurb), root='../',
                       subnav=SUBNAV.format(root='../'), caret=CARET)
    page += f"""<div class="wrap crumbs"><a href="/">Help centre</a> &nbsp;›&nbsp; {html.escape(name)}</div>
<section class="wrap" style="padding-top:20px">
<div class="section-head"><h2 class="display">{html.escape(name)}</h2></div>"""

    if os.path.exists(struct_path):
        st = json.load(open(struct_path))
        listed = set()

        def card(slug):
            t, sf = by_slug_p.get(slug, (slug, ''))
            listed.add(slug)
            if not sf:
                sf = first_sentence.get(slug, '')
            desc = html.escape((sf or '')[:150])
            return (f'<a class="gcard" href="/{folder}/{slug}.html">'
                    f'<b>{html.escape(t)}</b><span>{desc}</span></a>')

        page += f'<p class="sec-intro">{html.escape(st["intro"])}</p>'
        sslug = st['start']['slug']
        stitle, ssf = by_slug_p.get(sslug, (sslug, ''))
        listed.add(sslug)
        page += f"""<a class="start-card" href="/{folder}/{sslug}.html"><span class="tag">Start here</span>
<h3>{html.escape(stitle)}</h3><p>{html.escape(st['start'].get('why', ssf or ''))}</p></a>"""
        for g in st['groups']:
            cards = ''.join(card(sl) for sl in g['slugs'] if sl in by_slug_p)
            page += f"""<div class="group"><h3>{html.escape(g['title'])}</h3>
<p class="gblurb">{html.escape(g.get('blurb', ''))}</p>
<div class="gcards">{cards}</div></div>"""
        leftover = [(t, sl) for (sl, t, pl, sf, au, tc, bh) in parsed if sl not in listed]
        if leftover:
            cards = ''.join(card(sl) for t, sl in leftover)
            page += f"""<div class="group"><h3>Also in this section</h3>
<p class="gblurb"></p><div class="gcards">{cards}</div></div>"""
        nx = st.get('next')
        if nx:
            page += f'<a class="next-stage" href="/{nx["folder"]}/">{html.escape(nx["label"])} \u2192</a>'
        page += '</section>'
    else:
        links = ''.join('<a href="/%s/%s.html">%s</a>' % (folder, sl, html.escape(t)) for t, sl in arts)
        page += f"""<div class="section-head" style="margin-top:-8px"><p>{html.escape(blurb)}</p></div>
<div class="sec-list">{links}</div></section>"""

    page += FOOT
    open(os.path.join(OUT, folder, 'index.html'), 'w', encoding='utf-8').write(page)

json.dump(search_index, open(os.path.join(OUT, 'assets/search-index.json'), 'w'), indent=1)

# ---------------- landing page ----------------
def step_card(folder, num, name, blurb):
    return f'''<a class="step" href="{folder}/index.html"><div class="num">{num}</div>
<h3>{html.escape(name)}</h3><p>{html.escape(blurb)}</p></a>'''

steps = ''.join(step_card(f, n, nm, b) for f, n, nm, a, b in SECTIONS if n)
# One icon per non-lifecycle section, keyed on the folder so it cannot drift if the
# section names change.
QUIET_ICONS = {
    '09-add-ons':
        '<path d="M12 2.7 3 7.4v9.2l9 4.7 9-4.7V7.4Z"/><path d="M3 7.4l9 4.7 9-4.7M12 12.1v9.2"/>',
    '10-integrations-api':
        '<path d="M9.5 14.5 5.9 18a3.6 3.6 0 1 0 5.1 5.1l3.5-3.6M14.5 9.5 18 5.9a3.6 3.6 0 1 1 5.1 5.1l-3.6 3.5"/>'
        '<path d="M9.7 14.3l4.6-4.6"/>',
    '11-account-administration':
        '<circle cx="12" cy="8" r="3.6"/><path d="M4.8 21a7.2 7.2 0 0 1 14.4 0"/>',
}
quiet = ''.join(
    '<a href="%s/index.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '%s</svg>%s<span class="ql-go">&rarr;</span></a>'
    % (f, QUIET_ICONS.get(f, ''), html.escape(nm))
    for f, n, nm, a, b in SECTIONS if a == 'organisers' and not n)
parts = ''.join(f'''<a class="door" href="{f}/index.html"><h2 class="display" style="font-size:23px">{html.escape(nm)}</h2>
<p>{html.escape(b)}</p><span class="go">{html.escape(nm)} guides →</span></a>'''
                for f, n, nm, a, b in SECTIONS if a == 'participants')

POPULAR = [
    ('12-for-submitters/accessing-your-reviews.html', 'Accessing your reviews'),
    ('01-getting-started/creating-an-account-with-oxford-abstracts-and-logging-in.html',
     'Creating an account and logging in'),
    ('12-for-submitters/making-a-submission.html', 'Making a submission'),
    ('12-for-submitters/editing-an-abstract-or-submission.html', 'Editing an abstract or submission'),
    ('01-getting-started/if-your-verification-email-hasn-t-arrived.html',
     "If you're not receiving Oxford Abstracts emails"),
    ('13-for-reviewers-committee/completing-a-review.html', 'Completing a review'),
    ('02-submissions/opening-and-closing-submissions-deadlines.html',
     'Opening and closing submissions (organisers)'),
]
missing_pop = [p for p, t in POPULAR if not os.path.exists(os.path.join(OUT, p))]
if missing_pop:
    raise SystemExit('POPULAR points at missing pages: %s' % missing_pop)
pop = ''.join('<a href="%s">%s <span class="arrow">→</span></a>' % (p, html.escape(t))
              for p, t in POPULAR)

index = HEAD.format(title='Help Centre | Oxford Abstracts',
                    desc='Guides and answers for organisers and participants using Oxford Abstracts.',
                    root='', subnav='', caret=CARET)
index += f'''
<section class="hero wrap">
<span class="search-badge">
<svg class="spark" viewBox="0 0 24 24" fill="none" aria-hidden="true">
<path d="M12 2.5l1.9 5.6 5.6 1.9-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.9L12 2.5z" fill="currentColor"/>
<path d="M19 15l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8L19 15z" fill="currentColor" opacity=".6"/>
</svg>
New Advanced Search <span class="sep">&middot;</span> <span class="plain">answers your question, not just links</span>
</span>
<h1 class="display">Hello, how can we&nbsp;help?</h1>
<p class="lede">Ask a full question in your own words, the way you'd ask a colleague. You'll get a straight answer back, plus the guide it came from.</p>
<div class="searchbox">
<form id="searchForm" role="search" aria-label="Search the help centre">
<input id="searchInput" type="text" placeholder="e.g. How do I email my reviewers?" aria-label="Your question">
<button class="btn" type="submit">Ask</button></form>
<!-- Chosen from evidence, not taste. Each is the commonest real question on a topic
     the old KB handled badly, and each is checked against /api/search before it ships:
     an example that returns a weak answer is worse than no example at all.

       poster gallery - the top question in 292 support tickets mentioning it (59 of
                        147 question sentences ask how to set it up, three times the
                        next theme). People miss that a poster reaches the gallery
                        through a submission-form question.
       API            - the single most-searched term in the old KB (34 searches, best
                        click-through) against one thin article, and 59 tickets. Kept
                        general because the commonest real question is "can it connect
                        to X", where X is a different system every time.
       deadline       - 24 searches at 0.17 average clicks: the highest-volume failing
                        search in the old KB. It is also the only one of the three
                        that every organiser meets, the other two being a Professional
                        add-on and an integration topic.

     All phrased as questions on purpose: they used not to be, which argued against the
     line above them asking for a full question. Phrasing also steers who gets
     answered - "how do I change MY deadline" would be answered in submitter voice,
     so these stay in organiser voice, because this page is an organiser surface. -->
<div class="chips">
<button class="chip" type="button">How do we set up the poster gallery?</button>
<button class="chip" type="button">What can I do with the API?</button>
<button class="chip" type="button">How do I change the submission deadline?</button>
</div></div>
<div class="results" id="results" aria-live="polite"><h3 id="resultsTitle">Guides that match</h3><ul id="resultsList"></ul></div>
</section>

<section class="wrap"><div class="doors-grid">
<a class="door" href="#organisers"><span class="door-ico" aria-hidden="true">
<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
<rect x="3.5" y="6.5" width="25" height="21" rx="3"/><path d="M3.5 12.5h25"/><path d="M10 3.5v5M22 3.5v5"/>
<path d="M9 18h5.5M9 22.5h9.5"/><circle cx="22" cy="18" r="1.7" fill="currentColor" stroke="none"/>
</svg></span><h2 class="display">I'm organising an event</h2>
<p>Setting up submissions, reviewing, decisions, emails, the programme, registration or your conference site.</p>
<span class="go">Show me organiser guides →</span></a>
<a class="door" href="#participants"><span class="door-ico" aria-hidden="true">
<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
<circle cx="12.8" cy="12" r="4.4"/><path d="M5.5 26.5v-1.9a5.3 5.3 0 015.3-5.3h4a5.3 5.3 0 015.3 5.3v1.9"/>
<path d="M21.6 8.2a4 4 0 010 7.7M22.4 19.4h.7a5.3 5.3 0 015.3 5.3v1.8"/>
</svg></span><h2 class="display">I'm taking part in an event</h2>
<p>Submitting an abstract, reviewing, or attending a conference run on Oxford Abstracts.</p>
<span class="go">Show me participant guides →</span></a>
</div></section>

<section class="lifecycle wrap" id="organisers">
<div class="section-head"><h2 class="display">Your event, step by step</h2>
<p>Guides are arranged in the order you'll need them — start where you are.</p></div>
<div class="steps">{steps}</div>
<p class="quiet-head">Add-ons, integrations and your account</p>
<div class="quiet-links">{quiet}</div></section>

<section class="participants wrap" id="participants">
<div class="section-head"><h2 class="display">Taking part in an event?</h2>
<p>Short, simple guides for everything you've been asked to do.</p></div>
<div class="part-grid">{parts}</div></section>

<section class="popular wrap">
<div class="section-head"><h2 class="display">Most popular articles</h2></div>
<div class="pop-list">{pop}</div></section>

<script src="assets/search.js"></script>
'''
index += FOOT
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(index)


# 404. Vercel serves this file for any unmatched path, so every link and asset
# reference has to be root-absolute - a relative one would resolve against
# whatever URL the reader actually typed. For the same reason the search box here
# is a plain GET to the home page rather than the live widget: search.js fetches
# assets/search-index.json relatively and would 404 from a deep path.
notfound = HEAD.format(title='Page not found | Oxford Abstracts Help',
                       desc='We could not find that page.', root='/',
                       subnav=SUBNAV.format(root='/'), caret=CARET)
notfound += '''<section class="wrap narrow hero">
<h1 class="display">We can't find that page</h1>
<p class="lede">The help centre was rebuilt recently, so a saved link or bookmark may
point somewhere that has moved. Search for what you need and you'll land in the right
place.</p>
<div class="searchbox">
<form role="search" action="/index.html" method="get" aria-label="Search the help centre">
<input type="text" name="q" placeholder="e.g. How do I email my reviewers?" aria-label="Your question">
<button class="btn" type="submit">Ask</button></form>
</div>
</section>

<section class="wrap"><div class="doors-grid">
<a class="door" href="/index.html#organisers"><h2 class="display">I'm organising an event</h2>
<p>Setting up submissions, reviewing, decisions, emails, the programme, registration or
your conference site.</p>
<span class="go">Show me organiser guides &rarr;</span></a>
<a class="door" href="/index.html#participants"><h2 class="display">I'm taking part in an event</h2>
<p>Submitting an abstract, reviewing, or attending a conference run on Oxford Abstracts.</p>
<span class="go">Show me participant guides &rarr;</span></a>
</div></section>
'''
notfound += FOOT
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(notfound)



# regenerate the answer store the search API reads (public corpus + internal notes)
def _load_store(dirpath, internal):
    out = {}
    for root, _, files in os.walk(dirpath):
        for fn in sorted(files):
            if not fn.endswith('.md') or fn == 'README.md':
                continue
            meta, body = parse(os.path.join(root, fn))
            body = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', body).strip()
            if internal:
                p = 'internal/' + fn[:-3]
                out[p] = {'title': meta.get('title', fn[:-3]), 'path': p,
                          'section': 'Internal note', 'plan': '', 'internal': True,
                          'body': body[:6000]}
            else:
                folder = os.path.basename(root)
                # A public entry's path is rendered as a source link under the AI
                # answer, so it has to correspond to a page that actually gets built.
                # A stray file at the corpus root used to yield "corpus/x.html" and a
                # dead link. Fail loudly rather than ship one: put notes the AI may
                # answer from in corpus-internal/, and work-lists in project/.
                if folder not in SEC_BY_FOLDER:
                    raise SystemExit(
                        'answer store: %s is not inside a section folder, so its '
                        'source link "%s/%s.html" would 404. Move it to '
                        'corpus-internal/ (answerable, never cited) or project/.'
                        % (os.path.join(root, fn), folder, fn[:-3]))
                p = '%s/%s.html' % (folder, fn[:-3])
                out[p] = {'title': meta.get('title', fn[:-3]), 'path': p,
                          'section': meta.get('section', folder),
                          'plan': meta.get('plan', ''), 'body': body[:12000]}
    return out

store = _load_store(SRC, False)
store.update(_load_store('corpus-internal', True))
json.dump(store, open('assets/articles.json', 'w'), indent=0)
print('answer store:', len(store), 'entries (%d internal)'
      % sum(1 for v in store.values() if v.get('internal')))
print('sections:', len(sec_articles))
print('article pages:', sum(len(v) for v in sec_articles.values()))
def _site_files():
    # dot-directories are not the site: .git, and .claude/worktrees/ when a background
    # task is running, which otherwise inflated this count by a whole second copy
    for root, dirs, files in os.walk(OUT):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        yield len(files)


c = CALLOUT_COUNTS
print('callouts: %d note, %d tip (%d label stripped, %d kept whole)'
      % (c['note'], c['tip'], c['stripped'], c['kept whole']))
print('total files:', sum(_site_files()))
