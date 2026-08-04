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
    for d, dirs, fs in os.walk('.'):
        # Prune every dot-directory, not just .git. A git worktree under
        # .claude/worktrees/ holds a second copy of the whole site, and its pages
        # resolve against a base path that does not exist in production - so the
        # checker reported hundreds of 404s that were only ever the worktree.
        dirs[:] = [x for x in dirs if not x.startswith('.')]
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
    # Two shapes, both of which have actually occurred. The second is a HubSpot
    # analytics wrapper with the real old-KB URL base64'd inside the query string,
    # which the plain /knowledge/ pattern cannot see - 21 of them hid behind it.
    # Three shapes, all of which have occurred. The analytics wrapper hides the real
    # old-KB URL in a base64 query string; a URL shortener hides it completely -
    # three t.ly links resolved to the dying HubSpot KB and no pattern could have
    # seen that, so shorteners are flagged on principle and must be justified.
    pat = re.compile(r'(?:https?:)?//help\.oxfordabstracts\.com/knowledge/'
                     r'|help\.oxfordabstracts\.com/_hcms/'
                     r'|app\.hubspot\.com/'
                     r'|//(?:t\.ly|bit\.ly|tinyurl\.com|goo\.gl|ow\.ly)/')
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


# 6b. A link written as a full path PLUS a fragment sits in the blind spot between
#     checks 1 and 6, and one reached readers for months. Check 1 strips the fragment
#     and sees a page that exists; check 6 only looks at bare href="#x". So
#     /08-conference-platform/networking-for-attendees.html#NB - a link to a dead
#     anchor on the page you are already reading - passed both.
#     Scoped to built pages, because build.py drops the fragment from most of these
#     before a reader ever sees one; only the survivors are a real fault.
def check_path_fragments():
    ids_of = {}
    bad = []
    for p in glob.glob('*/*.html'):
        t = open(p, encoding='utf-8').read()
        base = served(p)
        for href in re.findall(r'href="([^"#]+#[^"]+)"', t):
            if href.startswith(('http', 'mailto:', 'data:')):
                continue
            # Resolved the way a browser would, because build.py rewrites links
            # within a section to relative form. Matching on a leading "/" alone
            # sees only the cross-section ones and calls the rest clean.
            path, frag = urljoin(base, href).split('#', 1)
            target = path.lstrip('/')
            for c in (target, target + '.html', os.path.join(target, 'index.html')):
                if os.path.exists(c):
                    target = c
                    break
            else:
                bad.append((p, href, 'no such page'))
                continue
            if target not in ids_of:
                ids_of[target] = set(re.findall(r'id="([^"]+)"',
                                                open(target, encoding='utf-8').read()))
            if frag not in ids_of[target]:
                bad.append((p, href, 'dead anchor'))
    report('path+fragment links resolve', not bad, bad[:3])


# 6c. No page may link to itself. The old KB kept its FAQs in a separate silo that
#     pointed at the topic articles; dissolving the silo into those same articles
#     turned 34 of those pointers into "see the page you are on". They read as a
#     way forward and are a dead end, which is worse than no link at all.
def check_self_links():
    bad = []
    for p in article_pages():
        here = served(p)
        for href in re.findall(r'href="([^"]+)"', prose_of(p)):
            if href.startswith(('http', '#', 'mailto:', 'data:')):
                continue
            # urljoin for the same reason as above: on an article page a self-link
            # comes out as the bare filename, so a string compare against the
            # root-absolute path never matches and the check quietly never fails.
            clean = urljoin(here, href).split('?')[0].split('#')[0]
            if clean.endswith('.html'):
                clean = clean[:-5]
            if clean == here:
                bad.append((here, href))
    report('no page links to itself', not bad, bad[:3])


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


# 7b. A "Common questions" heading with nothing under it. 22 of the 61 came over from
#     the dissolved HubSpot FAQ silo with the question intact and the answer lost, and
#     they are live: the reader sees their question and then the next heading. Worse
#     than not asking - it confirms the problem is known, then abandons them.
#     Pinned rather than zeroed, the way check 4 pins its legitimate matches, so the
#     debt is visible and can only fall. Listed in project/unanswered-faq-questions.md.
FAQ_BLOCK = re.compile(r'<div class="faq-block">(.*?)'
                       r'(?=<section class="support"|<div class="feedback"|</div>\s*</article>|\Z)', re.S)
# 4 August 2026: 21 of the original 22 were answered from content already on their
# own page. The one left needs somebody to check the software: the amendments
# article lists what an admin can change on an order and deleting one is not among
# them, so answering it from the page would have been a guess.
UNANSWERED_FAQ_PIN = 1


def check_faq_answered():
    bad = []
    for p in article_pages():
        m = FAQ_BLOCK.search(open(p, encoding='utf-8').read())
        if not m:
            continue
        parts = re.split(r'<h3\b[^>]*>(.*?)</h3>', m.group(1), flags=re.S)
        for i in range(1, len(parts), 2):
            body = parts[i + 1] if i + 1 < len(parts) else ''
            # Do not stop at a following <h2>: several entries are a question whose
            # answer sits under a standfirst h2, and truncating there reported six
            # perfectly good answers as missing. Strip headings, keep the rest.
            text = re.sub(r'<h\d\b[^>]*>.*?</h\d>', ' ', body, flags=re.S)
            text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', text)).strip()
            if len(text) < 15 and '<img' not in body:
                bad.append((p, re.sub(r'<[^>]+>', '', parts[i]).replace('#', '').strip()[:60]))
    n = len(bad)
    report('FAQ questions answered', n <= UNANSWERED_FAQ_PIN,
           '%d unanswered (pinned %d)%s' % (n, UNANSWERED_FAQ_PIN,
                                            '' if n <= UNANSWERED_FAQ_PIN else ' ' + str(bad[:3])))


# 7c. Nothing customer-specific may reach corpus-internal/. Those notes are answered
#     from for anyone who asks the right question, so a customer name or event ID in
#     one is disclosed to strangers, not merely committed. This has not happened yet -
#     the check exists because the Loom transcript project will feed generalised
#     knowledge from 1:1 customer videos into exactly this folder, and every one of
#     those names a customer and an event.
#
#     Emails and event IDs only. Personal names are not machine-detectable at
#     acceptable precision, so this is a floor, not a substitute for reading the note.
INTERNAL_PII_ALLOWED = {
    # A real event number used illustratively to explain where the ID sits in the
    # URL. It discloses nothing on its own, but it is a real event - genericising it
    # would cost nothing and is worth doing next time this note is touched.
    ('where-to-find-your-event-id.md', 'event-id', '528'),
}


def check_internal_privacy():
    email = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
    event = re.compile(r'/events?/(\d{2,})')
    found = []
    for p in glob.glob('corpus-internal/*.md'):
        fn = os.path.basename(p)
        if fn == 'README.md':
            continue
        t = open(p, encoding='utf-8').read()
        for e in set(email.findall(t)):
            # Our own support addresses are the point of some notes, not a leak.
            if e.lower().endswith(('oxfordabstracts.com', 'example.com')):
                continue
            found.append((fn, 'email', e))
        for i in set(event.findall(t)):
            found.append((fn, 'event-id', i))
    leaks = [f for f in found if f not in INTERNAL_PII_ALLOWED]
    report('no customer data in internal notes', not leaks, leaks[:3])


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
    check_path_fragments()
    check_self_links()
    check_structure()
    check_faq_answered()
    check_internal_privacy()
    check_corpus_shape()
    print()
    if FAIL:
        print('FAILED:', ', '.join(FAIL))
        sys.exit(1)
    print('all checks passed')
