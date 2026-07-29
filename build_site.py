import os, re, json, shutil, html
import markdown

SRC = 'kb/corpus'
OUT = 'kb/site'
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

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
.helpful{margin-top:28px;text-align:center;color:var(--muted);font-size:17px}
.support{margin-top:30px;background:var(--navy);color:var(--cream);border-radius:var(--radius);padding:30px 34px;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap}
.support h2{font-family:'Gloock',serif;font-weight:400;font-size:25px;margin-bottom:6px;-webkit-text-stroke:.3px currentColor}
.support p{color:rgba(237,235,226,.78);font-size:17px;max-width:460px;margin:0}
.support .btn{flex:none}
.helpful button{margin:10px 6px 0;background:none;border:1.5px solid var(--line);border-radius:999px;padding:9px 22px;font-family:'Outfit',sans-serif;font-size:16px;cursor:pointer;color:var(--navy)}
.helpful button:hover{border-color:var(--navy)}
@media (max-width:820px){.steps{grid-template-columns:repeat(2,1fr)}.part-grid,.doors-grid,.sec-list{grid-template-columns:1fr}.nav-links .hide-sm{display:none}.prose{padding:24px 20px}}
"""

HEAD = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css"></head><body>
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
open(os.path.join(OUT, 'assets/style.css'), 'w').write(CSS)

md = markdown.Markdown(extensions=['extra', 'sane_lists'])
search_index = []
sec_articles = {}

# map old KB slug -> new site path, from redirects.csv
import csv as _csv
OLD2NEW = {}
for old, new in _csv.reader(open(os.path.join(SRC, 'redirects.csv'))):
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

def enrich_body(body_html, title):
    """Add heading ids + anchor links, contextual alt text, lazy click-to-enlarge
    images, an on-this-page list for long articles, and lift a short opening
    paragraph out as a standfirst. Returns (standfirst, toc_html, body_html)."""
    soup = BeautifulSoup(body_html, 'lxml')
    root = soup.body or soup

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
    for el in root.find_all(['h2', 'h3', 'img']):
        if el.name in ('h2', 'h3'):
            last_heading = el.get_text(' ', strip=True).rstrip('#').strip()
        else:
            el['loading'] = 'lazy'
            if not el.get('alt'):
                el['alt'] = 'Screenshot: %s' % last_heading
            el['class'] = (el.get('class') or []) + ['zoomable']
            el['tabindex'] = '0'

    inner = root.decode_contents() if root.name == 'body' else str(soup)
    return standfirst, toc, inner

for folder, num, name, aud, blurb in SECTIONS:
    src_dir = os.path.join(SRC, folder)
    if not os.path.isdir(src_dir):
        continue
    os.makedirs(os.path.join(OUT, folder), exist_ok=True)
    arts = []
    parsed = []
    meta_by_slug = {}
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
        standfirst, toc, body_html = enrich_body(body_html, title)
        parsed.append((slug, title, meta.get('plan', ''), standfirst, toc, body_html))
        meta_by_slug[slug] = meta

    for i, (slug, title, plan, standfirst, toc, body_html) in enumerate(parsed):
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
        lr = meta_by_slug.get(slug, {}).get('last_reviewed', '')
        if lr:
            try:
                import datetime as _dt
                lr_h = _dt.date.fromisoformat(lr).strftime('%-d %B %Y')
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
    struct_path = os.path.join('kb/structure', folder + '.json')
    by_slug_p = {sl: (t, st) for (sl, t, pl, st, tc, bh) in parsed}
    page = HEAD.format(title=html.escape(name) + ' | Oxford Abstracts Help',
                       desc=html.escape(blurb), root='../',
                       hdr_search=HDR_SEARCH.format(root='../'))
    page += f"""<div class="wrap crumbs"><a href="../index.html">Help centre</a> &nbsp;›&nbsp; {html.escape(name)}</div>
<section class="wrap" style="padding-top:20px">
<div class="section-head"><h2 class="display">{html.escape(name)}</h2></div>"""

    if os.path.exists(struct_path):
        st = json.load(open(struct_path))
        listed = set()

        def card(slug):
            t, sf = by_slug_p.get(slug, (slug, ''))
            listed.add(slug)
            desc = html.escape((sf or '')[:150])
            return f'<a class="gcard" href="{slug}.html"><b>{html.escape(t)}</b><span>{desc}</span></a>'

        page += f'<p class="sec-intro">{html.escape(st["intro"])}</p>'
        sslug = st['start']['slug']
        stitle, ssf = by_slug_p.get(sslug, (sslug, ''))
        listed.add(sslug)
        page += f"""<a class="start-card" href="{sslug}.html"><span class="tag">Start here</span>
<h3>{html.escape(stitle)}</h3><p>{html.escape(st['start'].get('why', ssf or ''))}</p></a>"""
        for g in st['groups']:
            cards = ''.join(card(sl) for sl in g['slugs'] if sl in by_slug_p)
            page += f"""<div class="group"><h3>{html.escape(g['title'])}</h3>
<p class="gblurb">{html.escape(g.get('blurb', ''))}</p>
<div class="gcards">{cards}</div></div>"""
        leftover = [(t, sl) for (sl, t, pl, sf, tc, bh) in parsed if sl not in listed]
        if leftover:
            cards = ''.join(card(sl) for t, sl in leftover)
            page += f"""<div class="group"><h3>Also in this section</h3>
<p class="gblurb"></p><div class="gcards">{cards}</div></div>"""
        nx = st.get('next')
        if nx:
            page += f'<a class="next-stage" href="../{nx["folder"]}/index.html">{html.escape(nx["label"])} \u2192</a>'
        page += '</section>'
    else:
        links = ''.join('<a href="%s.html">%s</a>' % (sl, html.escape(t)) for t, sl in arts)
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
    ('12-for-submitters/accessing-your-review.html', 'Accessing your reviews'),
    ('01-getting-started/creating-an-account-with-oxford-abstracts.html', 'Creating an account and logging in'),
    ('12-for-submitters/making-a-submission.html', 'Making a submission'),
    ('12-for-submitters/editing-a-submission.html', 'Editing an abstract or submission'),
    ('01-getting-started/what-to-do-if-a-verification-email-hasnt-arrived-in-your-inbox.html',
     "If you're not receiving Oxford Abstracts emails"),
    ('13-for-reviewers-committee/completing-a-review.html', 'Completing a review'),
    ('02-submissions/open-and-close-submissions-_-call-for-abstracts.html',
     'Open and close submissions (organisers)'),
]
pop = ''.join('<a href="%s">%s <span class="arrow">→</span></a>' % (p, html.escape(t))
              for p, t in POPULAR if os.path.exists(os.path.join(OUT, p)))

index = HEAD.format(title='Help Centre | Oxford Abstracts',
                    desc='Guides and answers for organisers and participants using Oxford Abstracts.',
                    root='', hdr_search='')
index += f'''
<section class="hero wrap">
<h1 class="display">What do you need help&nbsp;with?</h1>
<p class="lede">Type your question the way you'd ask a colleague — we'll point you to the guide that answers it.</p>
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

shutil.copy(os.path.join(SRC, 'redirects.csv'), os.path.join(OUT, 'redirects.csv'))

# copy hand-written extras (search JS, API functions, deploy config, docs)
for root, dirs, files in os.walk('kb/extras'):
    rel = os.path.relpath(root, 'kb/extras')
    dst = os.path.join(OUT, rel) if rel != '.' else OUT
    os.makedirs(dst, exist_ok=True)
    for f in files:
        shutil.copy(os.path.join(root, f), os.path.join(dst, f))
print('sections:', len(sec_articles))
print('article pages:', sum(len(v) for v in sec_articles.values()))
print('total files:', sum(len(f) for _, _, f in os.walk(OUT)))
