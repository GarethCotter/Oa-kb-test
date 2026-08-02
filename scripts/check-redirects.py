"""Verify every redirect in redirects.csv actually lands where it should.

    py scripts/check-redirects.py                     # checks oa-kb-test.vercel.app
    py scripts/check-redirects.py help.oxfordabstracts.com
    py scripts/check-redirects.py localhost:8000 --scheme http

Why this exists
---------------
`redirects.csv` is the platform-neutral map from the old HubSpot addresses to
the new ones. `vercel.json` is only today's encoding of it; if the site moves to
different hosting, that file is thrown away and the map has to be re-expressed
in whatever the new host uses.

That migration is the one change that can break years of inbound links silently
-- a wrong redirect returns a clean 404 and nothing alerts anyone. This script is
the acceptance test for it. Point it at any host, before or after a move.

Note the redirects are currently DORMANT: their source paths are on
help.oxfordabstracts.com, which still serves the old HubSpot KB. Nothing reaches
them on the test domain. They become load-bearing the moment the new site takes
over that hostname, so the run that matters is the one against the real domain
at changeover. Run it here first to establish the baseline.

What counts as a pass: requesting the old path, following redirects, ends at
HTTP 200 on the expected new path. `.html` and trailing slashes are ignored when
comparing, because `cleanUrls` strips them -- what matters is that the reader
arrives at the right article, not the exact spelling of the URL.
"""

import csv
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

DEFAULT_HOST = 'oa-kb-test.vercel.app'
TIMEOUT = 20
WORKERS = 12
UA = 'oa-kb-redirect-check/1.0'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, 'redirects.csv')


def normalise(path):
    """Compare what the reader lands on, not how the host spells it."""
    path = path.split('?')[0].split('#')[0]
    if path.endswith('.html'):
        path = path[:-len('.html')]
    if path.endswith('/index'):
        path = path[:-len('/index')]
    if len(path) > 1:
        path = path.rstrip('/')
    return path or '/'


def check(host, scheme, row):
    src = urlparse(row['old_url']).path
    # A destination may be an absolute URL - one row points off-site to the support
    # contact form, because the article it used to reach was retired. Compare paths.
    want = normalise(urlparse(row['new_path']).path if '://' in row['new_path']
                     else row['new_path'])
    url = '%s://%s%s' % (scheme, host, src)
    req = urllib.request.Request(url, headers={'User-Agent': UA}, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            got = normalise(urlparse(resp.geturl()).path)
            if resp.status != 200:
                return (src, 'status %s' % resp.status, want, got)
            if got != want:
                return (src, 'landed elsewhere', want, got)
            return None
    except urllib.error.HTTPError as e:
        return (src, 'HTTP %s' % e.code, want, normalise(urlparse(e.url).path) if e.url else '-')
    except Exception as e:                                   # network, DNS, TLS
        return (src, type(e).__name__ + ': ' + str(e)[:60], want, '-')


def main():
    args = [a for a in sys.argv[1:]]
    scheme = 'https'
    if '--scheme' in args:
        i = args.index('--scheme')
        scheme = args[i + 1]
        del args[i:i + 2]
    host = args[0] if args else DEFAULT_HOST

    with open(CSV_PATH, encoding='utf-8-sig') as fh:
        rows = [r for r in csv.DictReader(fh)
                if r.get('old_url', '').strip() and r.get('new_path', '').strip()]

    print('checking %d redirects against %s://%s\n' % (len(rows), scheme, host))

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(lambda r: check(host, scheme, r), rows))

    bad = [r for r in results if r]
    for src, why, want, got in bad:
        print('  FAIL %-58s %s' % (src, why))
        print('       expected %s' % want)
        print('       got      %s' % got)

    print('\n%d/%d ok, %d failed' % (len(rows) - len(bad), len(rows), len(bad)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
