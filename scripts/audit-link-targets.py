"""Find links that resolve perfectly but point at the wrong article.

    py scripts/audit-link-targets.py
    py scripts/audit-link-targets.py --all      # include the weaker signals

scripts/checks.py already proves every internal link RESOLVES - "would 404 in
production", "in-page links resolve", "path+fragment links resolve" and
"no page links to itself" between them cover broken. A link can pass all four and
still be wrong: it returns 200 and lands the reader somewhere that does not answer
the thing they clicked on.

That failure is invisible to a crawler, because nothing about the HTTP response is
wrong. The only evidence is the mismatch between what the link SAYS and what the
destination is ABOUT.

So this compares the two. For each editorial link it scores the anchor text against
the destination's title and headings, then against every other article's title and
headings, and reports the cases where somewhere else is the obviously better home.

The case that prompted it, live on the site today: two links reading
"Event Administrator" in different-types-of-users-in-the-system, both pointing at
the event dashboard article. Neither is broken. Both are wrong - the words are the
name of a user type, and there is a section about user types one page away.

Nothing here is a verdict. It is a shortlist for a human to look at, and the
false-positive rate on the weaker signals is high enough that they are behind --all.
"""

import os
import re
import sys
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Words that carry no signal about what a page is about. "click", "here" and "page"
# are in here because they are the anchor text of the links this cannot judge.
STOP = set("""a an and are as at be but by can do does for from had has have how i if in
into is it its like made make may more must new not of on once one only or other our out
over own same see should so some such than that the their them then there these they this
those to too under until up use used using very via want was way we were what when where
which while who why will with within would you your yours click here page pages article
articles guide guides section sections link links read learn find out about above below
""".split())

# Anchor text that cannot be judged at all - it names nothing. Reported separately,
# because "click here" is a writing problem rather than a wrong-target problem.
UNINFORMATIVE = {'here', 'this', 'click here', 'read more', 'more', 'this article',
                 'this page', 'see here', 'link', 'follow this link', 'find out more',
                 'learn more', 'contact form', 'this link'}


def strip_tags(s):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def stem(w):
    """Crude, deliberately. The first version had none, and "Recording a decision"
    scored 33% against "Recording decisions" - decision/decisions and accepting/accept
    are the same word to a reader and were different words to the matcher, so correct
    links were reported as wrong. Anything cleverer needs a dependency for no gain at
    this vocabulary size."""
    for suf in ('ingly', 'edly', 'ing', 'ies', 'ed', 'es', 's'):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[:-len(suf)] + ('y' if suf == 'ies' else '')
    return w


def tokens(s):
    return {stem(w) for w in re.findall(r"[a-z][a-z'-]{2,}", s.lower()) if w not in STOP}


def pages():
    for sec in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, sec)
        if re.match(r'^\d\d-', sec) and os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.endswith('.html') and f != 'index.html':
                    yield sec, f[:-5], os.path.join(d, f)


PROSE = re.compile(r'<div class="prose">(.*?)(?:<section class="support"|<div class="feedback")', re.S)


def profile(path):
    """What a page is ABOUT: its title plus every heading in it. Headings matter as
    much as the title - a link saying "Event Administrator" should find the page
    with that heading, even though no article is titled that."""
    html = open(path, encoding='utf-8').read()
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    title = strip_tags(h1.group(1)) if h1 else ''
    m = PROSE.search(html)
    prose = m.group(1) if m else ''
    heads = [strip_tags(h).replace('#', '').strip()
             for h in re.findall(r'<h[234][^>]*>(.*?)</h[234]>', prose, re.S)]
    return {'title': title, 'heads': heads,
            'tok': tokens(title + ' ' + ' '.join(heads)), 'title_tok': tokens(title)}


def score(anchor_tok, page_tok):
    """How much of what the link SAYS is present in what the page is ABOUT."""
    if not anchor_tok:
        return 0.0
    return len(anchor_tok & page_tok) / len(anchor_tok)


def main():
    show_all = '--all' in sys.argv
    prof = {}
    for sec, slug, p in pages():
        prof[(sec, slug)] = profile(p)

    # Anchor text that is word-for-word a heading somewhere else. Precise rather than
    # fuzzy, and it exists because title-only matching cannot see the case that
    # prompted this script: "Event Administrator" is a heading in
    # different-types-of-users-in-the-system, but no article is TITLED that, so
    # scoring titles finds nothing better and the wrong link passes.
    heading_home = {}
    for key, pr in prof.items():
        for h in pr['heads']:
            k = re.sub(r'[^a-z0-9 ]', '', h.lower()).strip()
            if len(k) > 6:
                heading_home.setdefault(k, []).append(key)

    mismatches, exact_heading, orphaned_text, uninformative = [], [], [], []
    total = 0

    for sec, slug, p in pages():
        html = open(p, encoding='utf-8').read()
        m = PROSE.search(html)
        if not m:
            continue
        prose = re.sub(r'<a\b[^>]*class="anchor"[^>]*>.*?</a>', '', m.group(1), flags=re.S)

        for a in re.finditer(r'<a\b([^>]*)href="([^"]+)"([^>]*)>(.*?)</a>', prose, re.S):
            attrs, href, inner = a.group(1) + a.group(3), a.group(2), a.group(4)
            if 'aud-alt' in attrs or href.startswith(('http', 'mailto:', '#')):
                continue
            text = strip_tags(inner)
            if not text:
                continue
            tgt = href.split('#')[0].replace('.html', '')
            if tgt.startswith('../'):
                rest = tgt[3:]
                tsec, tslug = rest.split('/', 1) if '/' in rest else (sec, rest)
            elif tgt.startswith('/'):
                parts = tgt.lstrip('/').split('/')
                tsec, tslug = (parts[0], parts[1]) if len(parts) > 1 else (parts[0], 'index')
            else:
                tsec, tslug = sec, tgt
            if (tsec, tslug) not in prof:
                continue                      # section landing page, not an article
            total += 1

            if text.strip().lower().rstrip('.') in UNINFORMATIVE:
                uninformative.append((sec, slug, text, prof[(tsec, tslug)]['title']))
                continue

            atok = tokens(text)
            # One content word is not enough to accuse a link on. "Submitter" matched
            # a heading in an unrelated article and produced a confident, absurd
            # suggestion; two words is where the signal starts.
            if len(atok) < 2:
                continue
            here = score(atok, prof[(tsec, tslug)]['tok'])

            # Word-for-word a heading on some other page, and a poor match for the page
            # it actually points at. Both halves are needed: without the second, this
            # flagged "Account Administrator" pointing at the account administration
            # article, purely because another page happens to carry that heading too.
            # The link was fine; the rule was wrong.
            akey = re.sub(r'[^a-z0-9 ]', '', text.lower()).strip()
            if len(akey) > 6 and akey in heading_home and here < 0.5:
                homes = [k for k in heading_home[akey] if k != (tsec, tslug)]
                dest_heads = {re.sub(r'[^a-z0-9 ]', '', h.lower()).strip()
                              for h in prof[(tsec, tslug)]['heads']}
                if homes and akey not in dest_heads:
                    exact_heading.append({
                        'from': '%s/%s' % (sec, slug), 'anchor': text,
                        'to': '%s/%s' % (tsec, tslug),
                        'homes': ['%s/%s' % k for k in homes],
                    })

            # Generous to the destination, strict on the alternatives, on purpose.
            # The destination gets credit for its headings as well as its title (scored
            # above), so a link pointing at the right page for a reason buried
            # mid-article is not accused. Alternatives are judged on their TITLE only -
            # every article has a dozen headings, so scoring those makes almost
            # everything match something, and the first run of this suggested
            # "Collecting slides and posters" as the home for a link reading "Submitter".
            best, best_key = 0.0, None
            for key, pr in prof.items():
                if key == (tsec, tslug) or key == (sec, slug):
                    continue
                s = score(atok, pr['title_tok'])
                if s > best:
                    best, best_key = s, key

            # A clearly better home elsewhere is the strong signal.
            if best >= 0.75 and best >= here + 0.5:
                mismatches.append({
                    'from': '%s/%s' % (sec, slug), 'anchor': text,
                    'to': '%s/%s' % (tsec, tslug), 'to_title': prof[(tsec, tslug)]['title'],
                    'here': here, 'best': best,
                    'better': '%s/%s' % best_key, 'better_title': prof[best_key]['title'],
                })
            elif here == 0.0:
                orphaned_text.append((sec + '/' + slug, text, tsec + '/' + tslug,
                                      prof[(tsec, tslug)]['title']))

    print('editorial links checked: %d\n' % total)

    print('=' * 78)
    print('LIKELY WRONG TARGET - the words match a different article much better')
    print('=' * 78)
    if not mismatches:
        print('  none')
    for r in sorted(mismatches, key=lambda x: -(x['best'] - x['here'])):
        print('\n  "%s"' % r['anchor'])
        print('     in        %s' % r['from'])
        print('     points to %s   (%.0f%% match)' % (r['to'], r['here'] * 100))
        print('     but "%s" is a %.0f%% match  -> %s' % (r['better_title'], r['best'] * 100, r['better']))

    print('\n' + '=' * 78)
    print('THE LINKED WORDS ARE A HEADING SOMEWHERE ELSE')
    print('=' * 78)
    if not exact_heading:
        print('  none')
    for r in exact_heading:
        print('\n  "%s"' % r['anchor'])
        print('     in        %s' % r['from'])
        print('     points to %s' % r['to'])
        print('     but is word-for-word a heading in: %s' % ', '.join(r['homes']))

    print('\n' + '=' * 78)
    print('ANCHOR TEXT NAMES NOTHING - "%s" and friends' % 'click here')
    print('=' * 78)
    print('  %d links whose words say nothing about where they go' % len(uninformative))
    for f, s, t, dt in uninformative[:8 if not show_all else len(uninformative)]:
        print('     %-52s "%s" -> %s' % (f + '/' + s, t, dt))

    if show_all:
        print('\n' + '=' * 78)
        print('WEAK - none of the linked words appear on the destination at all')
        print('=' * 78)
        for f, t, to, dt in orphaned_text:
            print('     %-46s "%s"' % (f, t))
            print('     %-46s -> %s' % ('', dt))
    else:
        print('\n%d more links share no vocabulary with their destination. '
              'Run with --all to see them.' % len(orphaned_text))
    return 0


if __name__ == '__main__':
    sys.exit(main())
