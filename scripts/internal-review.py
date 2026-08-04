"""Render corpus-internal/ as a review page you can actually read.

    python scripts/internal-review.py       # writes internal-review.local.html

The internal notes are the one part of the answer store with no rendered surface:
they never become pages, so the only way to see them has been to open 42 markdown
files. This builds a single page showing the things CLAUDE.md says go wrong with
them.

**The output is gitignored on purpose. Never commit it.** Anything committed to
this repo is served by Vercel - that is exactly how assets/articles.json ended up
publicly downloadable with all 41 notes in it. A formatted, browsable index of the
internal corpus would be a worse version of the same mistake.
"""
import html as _html
import os
import re
import sys
from collections import Counter

SRC = 'corpus-internal'
OUT = 'internal-review.local.html'

# The router sees a note's title plus only this much of its body. A pricing note
# whose plan names sat below the line was never selected for "how much is the
# Professional Conference Package".
ROUTER_WINDOW = 160

# Above this, a note is doing too many jobs. not-currently-possible.md holds 25
# unrelated limitations and was reached for 4 of 14 test questions; the same facts
# split into their own notes, where the title is the answer, answered 2 of 2.
LONG = 4000

FM = re.compile(r'^---\n(.*?)\n---\n', re.S)
STOP = set('the a an and or of to in for on is are be can you your it this that with '
           'if when how what why not no do does they them their we our as at by from '
           'has have had will would there which who but so all any one two more most '
           'only also into out up down about after before than then some such each'.split())


def words(text):
    return [w for w in re.findall(r"[a-z][a-z'-]{2,}", text.lower()) if w not in STOP]


def load():
    notes = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith('.md') or fn == 'README.md':
            continue
        raw = open(os.path.join(SRC, fn), encoding='utf-8').read()
        m = FM.search(raw)
        meta, body = {}, raw
        if m:
            body = raw[m.end():]
            for line in m.group(1).splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"')
        plain = re.sub(r'\s+', ' ', re.sub(r'[#*`>\[\]()]', ' ', body)).strip()
        notes.append({
            'file': fn,
            'title': meta.get('title', fn[:-3]),
            'plan': meta.get('plan', ''),
            'body': plain,
            'head': plain[:ROUTER_WINDOW],
            'chars': len(plain),
        })
    return notes


def flags(n, notes):
    """Only the faults CLAUDE.md records as having actually happened."""
    out = []
    if n['chars'] > LONG:
        out.append(('omnibus', '%d chars - likely doing too many jobs; no %d characters '
                               'can represent it to the router' % (n['chars'], ROUTER_WINDOW)))
    # The rule is "keywords in the first 160 characters", so test for keyword
    # density, not for the title. Testing whether the title's own words appear in
    # the window flagged 14 of 41 notes - including several that open with a
    # deliberate run of search terms and are therefore doing exactly the right
    # thing. That flag was measuring the wrong rule, so it is gone.
    if len(set(words(n['head']))) < 8:
        out.append(('window thin', 'only %d distinct content words in the first %d '
                                   'characters - the router has little to match on'
                    % (len(set(words(n['head']))), ROUTER_WINDOW)))
    if n['chars'] < 200:
        out.append(('thin', 'only %d characters of body' % n['chars']))
    return out


# 0.30 was tried first and returned nothing at all: the highest real overlap in the
# corpus is 22%, so the threshold could never fire. A test that cannot fail is worse
# than no test. This is a prompt to go and look, not a verdict.
def overlaps(notes, floor=0.18):
    """Note pairs sharing a lot of vocabulary - candidates for merging or splitting."""
    sets = {n['file']: set(words(n['body'])) for n in notes}
    pairs = []
    files = [n['file'] for n in notes]
    for i, a in enumerate(files):
        for b in files[i + 1:]:
            sa, sb = sets[a], sets[b]
            if not sa or not sb:
                continue
            j = len(sa & sb) / len(sa | sb)
            if j >= floor:
                pairs.append((j, a, b))
    return sorted(pairs, reverse=True)


CSS = """
:root{--bg:#EDEBE2;--ink:#101C38;--red:#D0432C;--rule:#d8d5c8;--warn:#8a6d1f}
@media(prefers-color-scheme:dark){:root{--bg:#12141c;--ink:#e8e6dd;--rule:#2e3140}}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,sans-serif;
     margin:0;padding:2.5rem 1.25rem 6rem}
main{max-width:60rem;margin:0 auto}
h1{font-size:1.9rem;margin:0 0 .4rem}
.sub{opacity:.72;margin:0 0 2rem}
.bar{display:flex;gap:1.5rem;flex-wrap:wrap;padding:1rem 1.25rem;border:1px solid var(--rule);
     border-radius:.6rem;margin-bottom:2rem;background:rgba(255,255,255,.35)}
@media(prefers-color-scheme:dark){.bar{background:rgba(255,255,255,.04)}}
.bar b{display:block;font-size:1.5rem}
.bar span{opacity:.7;font-size:.82rem}
.note{border:1px solid var(--rule);border-radius:.6rem;padding:1.1rem 1.25rem;margin:0 0 1rem;
      background:rgba(255,255,255,.35)}
@media(prefers-color-scheme:dark){.note{background:rgba(255,255,255,.04)}}
.note h2{font-size:1.05rem;margin:0 0 .3rem}
.meta{font-size:.78rem;opacity:.65;margin-bottom:.7rem}
.window{font:13px/1.5 ui-monospace,monospace;padding:.6rem .7rem;border-radius:.4rem;
        background:rgba(16,28,56,.07);border-left:3px solid var(--red)}
@media(prefers-color-scheme:dark){.window{background:rgba(255,255,255,.06)}}
.window .rest{opacity:.4}
.flag{display:inline-block;font-size:.72rem;padding:.16rem .5rem;border-radius:.3rem;
      background:var(--warn);color:#fff;margin:.45rem .35rem 0 0}
table{border-collapse:collapse;width:100%;font-size:.86rem;margin-top:.5rem}
td,th{border-bottom:1px solid var(--rule);padding:.42rem .5rem;text-align:left}
h3{margin:2.5rem 0 .5rem;font-size:1.15rem}
.hint{opacity:.7;font-size:.86rem;margin:.2rem 0 1rem}
"""


def main():
    if not os.path.isdir(SRC):
        sys.exit('run from the repo root')
    notes = load()
    flagged = {n['file']: flags(n, notes) for n in notes}
    n_flagged = sum(1 for f in flagged.values() if f)
    pairs = overlaps(notes)

    e = _html.escape
    parts = [f'<!doctype html><meta charset="utf-8"><title>corpus-internal review</title>'
             f'<style>{CSS}</style><main>',
             '<h1>corpus-internal review</h1>',
             '<p class="sub">Local only &mdash; never commit this file. '
             'Everything committed here is served by Vercel.</p>',
             '<div class="bar">'
             f'<div><b>{len(notes)}</b><span>notes</span></div>'
             f'<div><b>{n_flagged}</b><span>with flags</span></div>'
             f'<div><b>{len(pairs)}</b><span>overlapping pairs</span></div>'
             f'<div><b>{sum(n["chars"] for n in notes) // 1000}k</b><span>characters</span></div>'
             '</div>']

    parts.append('<h3>Every note, as the router sees it</h3>')
    parts.append(f'<p class="hint">The red block is the first {ROUTER_WINDOW} characters &mdash; '
                 'all the router gets besides the title. If the words someone would '
                 'search for are not in there, the note will not be found.</p>')
    for n in sorted(notes, key=lambda x: (not flagged[x['file']], x['title'])):
        parts.append('<div class="note">')
        parts.append(f'<h2>{e(n["title"])}</h2>')
        parts.append(f'<div class="meta">{e(n["file"])} &middot; {n["chars"]} chars'
                     + (f' &middot; plan: {e(n["plan"])}' if n['plan'] else '') + '</div>')
        parts.append(f'<div class="window">{e(n["head"])}'
                     f'<span class="rest">{e(n["body"][ROUTER_WINDOW:ROUTER_WINDOW + 90])}&hellip;</span></div>')
        for name, why in flagged[n['file']]:
            parts.append(f'<span class="flag" title="{e(why)}">{e(name)}</span>')
        parts.append('</div>')

    if pairs:
        parts.append('<h3>Notes that overlap</h3>')
        parts.append('<p class="hint">Shared vocabulary. High overlap means two notes '
                     'compete for the same question &mdash; merge them, or sharpen each '
                     'title so it is obviously the answer to one thing.</p><table>'
                     '<tr><th>Shared</th><th>Note</th><th>Note</th></tr>')
        for j, a, b in pairs[:25]:
            parts.append(f'<tr><td>{j:.0%}</td><td>{e(a)}</td><td>{e(b)}</td></tr>')
        parts.append('</table>')

    parts.append('</main>')
    open(OUT, 'w', encoding='utf-8').write(''.join(parts))
    print(f'{len(notes)} notes, {n_flagged} flagged, {len(pairs)} overlapping pairs')
    print('wrote', OUT, '(gitignored - do not commit)')


if __name__ == '__main__':
    main()
