import os, re, json, shutil, html
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
    ('09-add-ons', '', 'Add-ons: Symposia & Certificates', 'organisers', 'Optional extras you can buy alongside your plan'),
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
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px 0}
.nav img{height:32px;display:block}
.nav-links{display:flex;align-items:center;gap:20px;font-size:16px}
.nav-links a{text-decoration:none;font-weight:500}
.nav-links a:hover{text-decoration:underline;text-underline-offset:4px}
.btn{display:inline-block;background:var(--red);color:#fff;border:none;cursor:pointer;font-family:'Outfit',sans-serif;font-weight:600;font-size:17px;padding:12px 22px;border-radius:999px;text-decoration:none}
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
.quiet-links{display:flex;flex-wrap:wrap;gap:12px 28px;justify-content:center;margin-top:26px;font-size:16.5px}
.quiet-links a{color:var(--muted);text-decoration:none;font-weight:500}
.quiet-links a:hover{color:var(--navy);text-decoration:underline;text-underline-offset:4px}
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
footer{padding:26px 0;text-align:center;font-size:15px;color:var(--muted)}
.crumbs{padding:22px 0 0;font-size:16px;color:var(--muted)}
.crumbs a{color:var(--muted);text-decoration:none}
.crumbs a:hover{text-decoration:underline;text-underline-offset:4px}
.article{padding:14px 0 60px}
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
@media (max-width:520px){.audience{padding:12px 14px}}
.prose{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:34px 38px}
.prose h2{font-family:'Gloock',serif;font-weight:400;font-size:27px;margin:30px 0 12px;-webkit-text-stroke:.3px currentColor}
.prose h2:first-child{margin-top:0}
.prose h3{font-size:21px;margin:24px 0 10px}
.prose p{margin-bottom:16px}
.prose ul,.prose ol{margin:0 0 18px 22px}
.prose li{margin-bottom:8px}
.prose img{max-width:100%;height:auto;border-radius:8px;border:1px solid var(--line);margin:8px 0 20px}
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
.toc span{display:block;font-weight:600;font-size:14px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
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
.dots{display:inline-flex;gap:4px}
.dots i{width:6px;height:6px;border-radius:50%;background:var(--red);opacity:.35;animation:blink 1.25s infinite ease-in-out}
.dots i:nth-child(2){animation-delay:.18s}
.dots i:nth-child(3){animation-delay:.36s}
@keyframes blink{0%,80%,100%{opacity:.25;transform:scale(.85)}40%{opacity:1;transform:scale(1)}}
.skel{display:flex;flex-direction:column;gap:9px}
.skel span{height:13px;border-radius:7px;background:linear-gradient(90deg,rgba(16,28,56,.07) 25%,rgba(16,28,56,.14) 37%,rgba(16,28,56,.07) 63%);background-size:400% 100%;animation:shimmer 1.5s ease-in-out infinite}
@keyframes shimmer{0%{background-position:100% 0}100%{background-position:0 0}}
@media (prefers-reduced-motion:reduce){.answer-block{transition:none;opacity:1;transform:none}.dots i,.skel span{animation:none}.skel span{background:rgba(16,28,56,.10)}}
@media (max-width:640px){.hdr-search{max-width:none;order:3;flex-basis:100%}.nav{flex-wrap:wrap}.prevnext{flex-direction:column}}
.support{margin-top:30px;background:var(--navy);color:var(--cream);border-radius:var(--radius);padding:30px 34px;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap}
.support h2{font-family:'Gloock',serif;font-weight:400;font-size:25px;margin-bottom:6px;-webkit-text-stroke:.3px currentColor}
.support p{color:rgba(237,235,226,.78);font-size:17px;max-width:460px;margin:0}
.support .btn{flex:none}
@media (max-width:820px){.steps{grid-template-columns:repeat(2,1fr)}.part-grid,.doors-grid,.sec-list{grid-template-columns:1fr}.nav-links .hide-sm{display:none}.prose{padding:24px 20px}}
"""

HEAD = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png"></head><body>
<header><div class="wrap nav">
<a href="{root}index.html" aria-label="Oxford Abstracts Help Centre"><img src="https://a.storyblok.com/f/262790/192x46/f2b614f59c/oa_dark.svg/m/384x0" alt="Oxford Abstracts"></a>
{hdr_search}<nav class="nav-links" aria-label="Main">
<a class="hide-sm" href="{root}index.html">Help centre home</a>
<a class="btn" href="https://app.oxfordabstracts.com/">Sign in</a>
</nav></div></header><main>"""

HDR_SEARCH = """<form class="hdr-search" role="search" action="{root}index.html" method="get">
<input type="search" name="q" placeholder="Search the guides" aria-label="Search the guides">
<button type="submit">Search</button></form>"""

ARTICLE_FOOT = """</main>
<footer><div class="wrap">Oxford Abstracts Help Centre &middot; <a href="https://oxfordabstracts.com/">oxfordabstracts.com</a></div></footer>
</body></html>"""

FOOT = """</main>
<section class="human"><div class="wrap">
<h2 class="display">Prefer to talk to a person?</h2>
<p>Our support team answers quickly, across every time zone — by email or on a free video call.</p>
<a class="btn" href="https://oxfordabstracts.com/resources/contact/">Contact support</a>
</div></section>
<footer><div class="wrap">Oxford Abstracts Help Centre &middot; <a href="https://oxfordabstracts.com/">oxfordabstracts.com</a></div></footer>
</body></html>"""

SUPPORT_URL = 'https://oxfordabstracts.com/resources/contact-support'

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
}
# Ordered: the first pattern that matches the paragraph text wins.
AUDIENCE_PATTERNS = [
    ('organisers', r'guidance below is for (?:event|account) administrators'),
    ('submitters', r'guidance below is for (?:users who are )?submit'),
    ('submitters', r'guidance below is for those wishing to submit'),
    ('reviewers',  r'guidance below is for reviewers'),
    ('attendees',  r'guidance below is for conference attendees'),
]
# The sentence naming the audience, and the "if you are someone else, go here"
# sentence that usually follows it. Both are removed; anything else in the
# paragraph is left alone, because a few carry an extra note about plan limits.
# Only "If you are ..." is audience routing. "If you experience any issues ..."
# tells a reviewer to contact their event administrator - that is support routing
# and has to stay in the prose, so it is deliberately not matched here.
AUD_SENTENCE = re.compile(
    r'^\s*(?:NB:\s*)?The guidance below is for [^.]*\.\s*', re.I)
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


def enrich_body(body_html, title):
    """Add heading ids + anchor links, contextual alt text, lazy click-to-enlarge
    images, an on-this-page list for long articles, lift a short opening paragraph
    out as a standfirst, and pull the 'who this is for' sentence out as a tag.
    Returns (standfirst, audience, toc_html, body_html)."""
    soup = BeautifulSoup(body_html, 'lxml')
    root = soup.body or soup
    audience = extract_audience(root, soup)

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

    # headings: ids + visible anchors; collect h2s for the jump list
    seen, h2s = {}, []
    for h in root.find_all(['h2', 'h3']):
        base = slugify(h.get_text(' ', strip=True))
        n = seen.get(base, 0)
        seen[base] = n + 1
        hid = base if n == 0 else f'{base}-{n+1}'
        h['id'] = hid
        a = soup.new_tag('a', href='#' + hid)
        a['class'] = 'anchor'
        a['aria-label'] = 'Link to this section'
        a.string = '#'
        h.append(a)
        if h.name == 'h2':
            h2s.append((hid, h.get_text(' ', strip=True).rstrip('#').strip()))

    toc = ''
    if len(root.find_all(['h2', 'h3'])) >= 4 and len(h2s) >= 2:
        items = ''.join(f'<a href="#{hid}">{html.escape(t)}</a>' for hid, t in h2s)
        toc = f'<nav class="toc" aria-label="On this page"><span>On this page</span>{items}</nav>'

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

    inner = root.decode_contents() if root.name == 'body' else str(soup)
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
        parsed.append((slug, title, meta.get('plan', ''), standfirst, audience, toc, body_html))
        meta_by_slug[slug] = meta
        first_sentence[slug] = lead_sentence(body_html)

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
                           hdr_search=HDR_SEARCH.format(root='../'))
        page += f"""<div class="wrap narrow crumbs">
<a href="../index.html">Help centre</a> &nbsp;›&nbsp; <a href="index.html">{html.escape(name)}</a></div>
<article class="wrap narrow article">
<h1 class="display">{html.escape(title)}</h1>
<div class="badges">{''.join(badges)}</div>
{aud_html}
{stand_html}
{toc}
<div class="prose">{body_html}</div>
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
{SUPPORT_BANNER if aud == 'organisers' else ''}
</article>
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
                       hdr_search=HDR_SEARCH.format(root='../'))
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
quiet = ''.join('<a href="%s/index.html">%s</a>' % (f, html.escape(nm))
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
                    root='', hdr_search='')
index += f'''
<section class="hero wrap">
<span class="search-badge">
<svg class="spark" viewBox="0 0 24 24" fill="none" aria-hidden="true">
<path d="M12 2.5l1.9 5.6 5.6 1.9-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.9L12 2.5z" fill="currentColor"/>
<path d="M19 15l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8L19 15z" fill="currentColor" opacity=".6"/>
</svg>
New search <span class="sep">&middot;</span> <span class="plain">answers your question, not just links</span>
</span>
<h1 class="display">What do you need help&nbsp;with?</h1>
<p class="lede">Ask a full question in your own words, the way you'd ask a colleague. You'll get a straight answer back, plus the guide it came from.</p>
<div class="searchbox">
<form id="searchForm" role="search" aria-label="Search the help centre">
<input id="searchInput" type="text" placeholder="e.g. How do I email my reviewers?" aria-label="Your question">
<button class="btn" type="submit">Search</button></form>
<div class="chips">
<button class="chip" type="button">Change the submission deadline</button>
<button class="chip" type="button">Why is my submission incomplete?</button>
<button class="chip" type="button">Editing the template emails</button>
</div></div>
<div class="results" id="results" aria-live="polite"><h3 id="resultsTitle">Guides that match</h3><ul id="resultsList"></ul></div>
</section>

<section class="wrap"><div class="doors-grid">
<a class="door" href="#organisers"><h2 class="display">I'm organising an event</h2>
<p>Setting up submissions, reviewing, decisions, emails, the programme, registration or your conference site.</p>
<span class="go">Show me organiser guides →</span></a>
<a class="door" href="#participants"><h2 class="display">I'm taking part in an event</h2>
<p>Submitting an abstract, reviewing, or attending a conference run on Oxford Abstracts.</p>
<span class="go">Show me participant guides →</span></a>
</div></section>

<section class="lifecycle wrap" id="organisers">
<div class="section-head"><h2 class="display">Your event, step by step</h2>
<p>Guides are arranged in the order you'll need them — start where you are.</p></div>
<div class="steps">{steps}</div>
<div class="quiet-links">{quiet}</div></section>

<section class="participants wrap" id="participants">
<div class="section-head"><h2 class="display">Taking part in an event?</h2>
<p>Short, simple guides for everything you've been asked to do.</p></div>
<div class="part-grid">{parts}</div></section>

<section class="popular wrap">
<div class="section-head"><h2 class="display">Most popular right now</h2></div>
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
                       hdr_search=HDR_SEARCH.format(root='/'))
notfound += '''<section class="wrap narrow hero">
<h1 class="display">We can't find that page</h1>
<p class="lede">The help centre was rebuilt recently, so a saved link or bookmark may
point somewhere that has moved. Search for what you need and you'll land in the right
place.</p>
<div class="searchbox">
<form role="search" action="/index.html" method="get" aria-label="Search the help centre">
<input type="text" name="q" placeholder="e.g. How do I email my reviewers?" aria-label="Your question">
<button class="btn" type="submit">Search</button></form>
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
print('total files:', sum(len(f) for _, _, f in os.walk(OUT)))
