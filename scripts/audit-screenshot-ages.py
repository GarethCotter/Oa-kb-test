"""Date every screenshot in the corpus from its filename, and report the articles
carrying old ones.

    py scripts/audit-screenshot-ages.py                  # summary to stdout
    py scripts/audit-screenshot-ages.py --before 2025    # default cutoff
    py scripts/audit-screenshot-ages.py --write          # also write project/screenshot-ages.md

What the date means, and what it does not
-----------------------------------------
The date comes from the *filename*, which is when the image was uploaded to the
old knowledge base -- not when the screenshot was taken. So it is an upper bound
on freshness: an image uploaded in 2022 cannot show a UI newer than 2022, but it
may well show an older one. Treat these dates as "no newer than".

Three filename families carry a date:

    screenshot-2022-04-11-at-12-21-45-png-e44c6407.webp   -> 2022-04-11
    undefined-oct-06-2021-08-35-58-07-am-86e145f5.webp    -> 2021-10-06
    image-png-apr-12-2021-05-33-47-61-pm-10b3e747.webp    -> 2021-04-12

Two families carry none, and both are Freshdesk-era -- the KB *before* HubSpot,
so they are almost certainly older than anything dated, not newer:

    s3-amazonaws-comcdn-freshdesk-comdatahelpdeskattachmentsprod-3a85ef46.webp
    oxfordabstracts-freshdesk-comsupportsolutionsarticles1234-5ab1.gif

Anything else undateable is reported separately rather than assumed to be fine.
"""

import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, 'corpus')

MONTHS = {m: i + 1 for i, m in enumerate(
    ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
     'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])}

RE_ISO = re.compile(r'^screenshot-(\d{4})-(\d{2})-(\d{2})-at-')
RE_MON = re.compile(r'^(?:undefined|image-png)-([a-z]{3})-(\d{1,2})-(\d{4})-')
RE_IMG_MD = re.compile(r'!\[[^\]]*\]\(([^)\s]+)')
RE_IMG_HTML = re.compile(r'<img[^>]+src="([^"]+)"')

FRESHDESK = ('s3-amazonaws-comcdn-freshdesk', 'oxfordabstracts-freshdesk-com')


def date_of(name):
    """-> (year, month, day) or None."""
    m = RE_ISO.match(name)
    if m:
        return tuple(int(g) for g in m.groups())
    m = RE_MON.match(name)
    if m:
        mon, day, year = m.groups()
        if mon in MONTHS:
            return (int(year), MONTHS[mon], int(day))
    return None


def articles():
    for section in sorted(os.listdir(CORPUS)):
        d = os.path.join(CORPUS, section)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith('.md'):
                yield section, fn[:-3], os.path.join(d, fn)


def main():
    args = sys.argv[1:]
    cutoff = 2025
    if '--before' in args:
        cutoff = int(args[args.index('--before') + 1])
    write = '--write' in args

    rows, no_images = [], []
    for section, slug, path in articles():
        text = open(path, encoding='utf-8').read()
        srcs = RE_IMG_MD.findall(text) + RE_IMG_HTML.findall(text)
        names = [os.path.basename(s.split('?')[0]) for s in srcs]
        if not names:
            no_images.append((section, slug))
            continue

        dated, old, undated_fd, undated_other = [], [], [], []
        for n in names:
            d = date_of(n)
            if d:
                dated.append(d)
                if d[0] < cutoff:
                    old.append((d, n))
            elif any(n.startswith(p) for p in FRESHDESK):
                undated_fd.append(n)
            else:
                undated_other.append(n)

        rows.append({
            'section': section, 'slug': slug, 'total': len(names),
            'dated': sorted(dated), 'old': sorted(old),
            'fd': undated_fd, 'other': undated_other,
        })

    flagged = [r for r in rows if r['old'] or r['fd'] or r['other']]
    flagged.sort(key=lambda r: (r['dated'][0] if r['dated'] else (0, 0, 0),
                                -len(r['old'])))

    total_imgs = sum(r['total'] for r in rows)
    total_old = sum(len(r['old']) for r in rows)
    total_fd = sum(len(r['fd']) for r in rows)
    total_other = sum(len(r['other']) for r in rows)

    print('articles with images      : %d of %d' % (len(rows), len(rows) + len(no_images)))
    print('image references          : %d' % total_imgs)
    print('dated before %d          : %d' % (cutoff, total_old))
    print('undated, Freshdesk-era    : %d  (older than anything dated)' % total_fd)
    print('undated, other            : %d' % total_other)
    print('articles needing attention: %d\n' % len(flagged))

    by_year = collections.Counter(d[0] for r in rows for d in r['dated'])
    print('images by year:')
    for y in sorted(by_year):
        print('  %d  %4d  %s' % (y, by_year[y], '#' * (by_year[y] // 12)))
    print()

    lines = []
    for r in flagged:
        oldest = min(r['dated']) if r['dated'] else None
        newest = max(r['dated']) if r['dated'] else None
        span = ('%04d-%02d' % oldest[:2]) if oldest else 'undated'
        if newest and newest[:2] != oldest[:2]:
            span += ' to %04d-%02d' % newest[:2]
        bits = ['%d/%d pre-%d' % (len(r['old']), r['total'], cutoff)] if r['old'] else []
        if r['fd']:
            bits.append('%d Freshdesk-era' % len(r['fd']))
        if r['other']:
            bits.append('%d undated' % len(r['other']))
        lines.append('| %s | %s | %s | %s |' % (r['slug'], r['section'], span, ', '.join(bits)))

    print('%-58s %-28s %s' % ('article', 'section', 'oldest image'))
    for r in flagged[:40]:
        oldest = min(r['dated']) if r['dated'] else None
        print('%-58s %-28s %s' % (
            r['slug'][:57], r['section'],
            ('%04d-%02d' % oldest[:2]) if oldest else 'undated (Freshdesk)'))
    if len(flagged) > 40:
        print('... and %d more (use --write for the full list)' % (len(flagged) - 40))

    if write:
        out = os.path.join(ROOT, 'project', 'screenshot-ages.md')
        with open(out, 'w', encoding='utf-8') as fh:
            fh.write('# Screenshot ages\n\n')
            fh.write('Generated by `scripts/audit-screenshot-ages.py`. '
                     'Dates come from filenames and mean *uploaded no later than* '
                     '- see the script header.\n\n')
            fh.write('%d image references across %d articles. %d dated before %d, '
                     '%d Freshdesk-era (undated, older still), %d otherwise undated. '
                     '**%d articles need attention.**\n\n'
                     % (total_imgs, len(rows), total_old, cutoff, total_fd,
                        total_other, len(flagged)))
            fh.write('| article | section | image dates | issue |\n')
            fh.write('|---|---|---|---|\n')
            fh.write('\n'.join(lines) + '\n')
        print('\nwrote %s' % os.path.relpath(out, ROOT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
