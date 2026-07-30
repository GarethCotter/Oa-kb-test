"""Everything worth checking after a build. Run from the repo root:

    python scripts/checks.py

Exits non-zero if any check fails, so it can gate a commit. Each check exists because
the thing it catches actually happened - the note on each says what.
"""
import collections, csv, glob, json, os, re, sys
from urllib.parse import urljoin

FAIL = []


PROSE = re.compile(r'<div class="prose">(.*?)</div>\s*(?:<section class="support"|<div class="feedback")',
                   re.S)


def prose_of(path):
    """Just the article body. Checks must not count the chrome: the footer logo, the
    lightbox's deliberately empty alt, or a phrase quoted in a section-page card."""
    m = PROSE.search(open(path, encoding='utf-8').read())
    return m.group(1) if m else ''


def article_pages():
    return [p for p in glob.glob('*/*.html') if os.path.basename(p) != 'index.html']


def report(name, ok, detail=''):
    print('%-34s %s %s' % (name, 'ok  ' if ok else 'FAIL', detail))
    if not ok:
        FAIL.append(name)


# 1. Internal links, resolved the way a browser would under cleanUrls. Section-page
#    links must be root-absolute; a plain file-exists test misses that.
def served(p):
    rel = '/' + os.path.relpath(p, '.').replace(os.sep, '/')
    if rel.endswith('/index.html'):
        return rel[:-len('/index.html')] or '/'
    return rel[:-5] if rel.endswith('.html') else rel


def target(u):
    u = u.split('?')[0].split('#')[0]
    if u in ('/', ''):
        return 'index.html'
    p = u.lstrip('/')
    for c in (p, p + '.html', os.path.join(p, 'index.html')):
        if os.path.exists(c):
            return c
    return None


def check_links():
    bad = []
    for d, _, fs in os.walk('.'):
        if '.git' in d:
            continue
        for f in fs:
            if not f.endswith('.html'):
                continue
            fp = os.path.join(d, f)
            base = served(fp)
            for h in re.findall(r'(?:href|src)="([^"]+)"', open(fp, encoding='utf-8').read()):
                if h.startswith(('http', '#', 'mailto:', 'data:')):
                    continue
                if target(urljoin(base, h)) is None:
                    bad.append((base, h))
    report('would 404 in production', not bad, bad[:3])


# 2. No article may link to the knowledge base this site replaces - those die when
#    HubSpot is cancelled, and check 1 cannot see them because it skips http.
#    source_url in the frontmatter is exempt: it is provenance.
def check_old_kb():
    pat = re.compile(r'(?:https?:)?//help\.oxfordabstracts\.com/knowledge/')
    fm = re.compile(r'^---\n.*?\n---\n', re.S)
    bad = []
    for p in glob.glob('corpus/*/*.md') + glob.glob('corpus/*.md'):
        if os.path.basename(p) == 'README.md':
            continue
        body = fm.sub('', open(p, encoding='utf-8').read(), count=1)
        if pat.search(body):
            bad.append(p)
    for p in glob.glob('*/*.html') + ['index.html', '404.html']:
        if os.path.exists(p) and pat.search(open(p, encoding='utf-8').read()):
            bad.append(p)
    report('old-KB links', not bad, bad[:3])


# 3. Redirect coverage. Every renamed article must still be reachable from its
#    original HubSpot URL. Depends on source_url, which is why check 2 leaves it alone.
def check_redirects():
    sources = {r.get('source') for r in json.load(open('vercel.json', encoding='utf-8')).get('redirects', [])}
    missing = []
    with open('project/title-renames.csv', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            if not row['proposed slug'].strip():
                continue
            md = os.path.join('corpus', row['section'], row['proposed slug'] + '.md')
            if not os.path.exists(md):
                missing.append(row['proposed slug'] + ' (no such article)')
                continue
            m = re.search(r'^source_url:\s*(\S+)', open(md, encoding='utf-8').read(), re.M)
            if m:
                path = m.group(1).strip('"').split('oxfordabstracts.com', 1)[-1]
                if path not in sources:
                    missing.append(row['proposed slug'])
    report('renamed articles redirected', not missing, missing[:3])


# 4. The audience sentence must be a tag, never left in the prose. A check for one
#    phrase once passed while most of the sentence was still on 87 pages, so every
#    fragment is tested and the legitimate occurrences are pinned.
def check_audience():
    # Only phrases unique to the boilerplate. "please click" and "an end user" were
    # tried as tripwires and had to go: they occur in ordinary instructions, and the
    # derived alt text repeats those instructions, so they false-positive by design.
    allowed = {}
    phrases = ['guidance below is for', 'delegate etc', 'end user (eg',
               'administrator of an event please see']
    counts = collections.Counter()
    tagged = 0
    for p in article_pages():
        if 'class="audience aud-' in open(p, encoding='utf-8').read():
            tagged += 1
        body = prose_of(p)
        for ph in phrases:
            counts[ph] += body.count(ph)
    over = {p: n for p, n in counts.items() if n > allowed.get(p, 0)}
    report('no audience sentence in prose', not over, over or '%d pages tagged' % tagged)


# 5. Alt text must be per-image. It used to be the nearest heading, so 39 images
#    shared 3 strings and a screen reader said the same phrase a dozen times.
def check_alt():
    total = distinct = empty = 0
    for p in article_pages():
        alts = re.findall(r'<img[^>]*\balt="([^"]*)"', prose_of(p))
        if not alts:
            continue
        total += len(alts)
        distinct += len(set(alts))
        empty += sum(1 for a in alts if not a.strip())
    ratio = distinct / total if total else 1
    report('alt text distinct', ratio > 0.99 and not empty,
           '%d/%d distinct, %d empty' % (distinct, total, empty))


# 6. No in-page link may point at an anchor that does not exist. The imported
#    articles carried 380 such links across 97 pages, all HubSpot-era.
def check_fragments():
    bad = 0
    for p in glob.glob('*/*.html'):
        t = open(p, encoding='utf-8').read()
        ids = set(re.findall(r'id="([^"]+)"', t))
        bad += len([x for x in re.findall(r'href="#([^"]+)"', t) if x not in ids])
    report('in-page links resolve', bad == 0, '%d broken' % bad)


# 7. Structural spot-checks that used to be done by eye.
def check_structure():
    doubles = [p for p in glob.glob('*/*.html') + ['index.html']
               if os.path.exists(p) and open(p, encoding='utf-8').read().count('<h1') > 1]
    report('one h1 per page', not doubles, doubles[:3])
    idx = open('index.html', encoding='utf-8').read()
    pop = re.search(r'Most popular(.*?)</section>', idx, re.S)
    n = len(re.findall(r'<a ', pop.group(1))) if pop else 0
    report('Most popular has 7', n == 7, n)
    cards = re.findall(r'<b>[^<]*</b><span>([^<]*)</span>', idx)
    thin = [c for c in cards if len(c.strip()) < 5]
    report('every section card described', not thin, thin[:3])


# 8. Nothing under corpus/ may sit outside a section folder - build.py enforces this
#    too, but check it here so a bad file is caught before a build is attempted.
def check_corpus_shape():
    stray = [p for p in glob.glob('corpus/*.md') if os.path.basename(p) != 'README.md']
    report('no stray files in corpus/', not stray, stray)


if __name__ == '__main__':
    if not os.path.exists('build.py'):
        sys.exit('run from the repo root')
    check_links()
    check_old_kb()
    check_redirects()
    check_audience()
    check_alt()
    check_fragments()
    check_structure()
    check_corpus_shape()
    print()
    if FAIL:
        print('FAILED:', ', '.join(FAIL))
        sys.exit(1)
    print('all checks passed')
