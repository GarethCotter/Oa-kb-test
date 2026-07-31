# Hosting the help centre — handover for the Oxford Abstracts engineer

For whoever moves this site onto Oxford Abstracts' own hosting and puts it on
**help.oxfordabstracts.com**. It is currently on a personal Vercel account at
`oa-kb-test.vercel.app`.

There is no build step and no runtime. The site is **static HTML committed to the
repo**, plus three serverless functions in `api/`. If your platform can serve a
folder and run a Node function, it will run this.

The whole job is reproducing five behaviours. Only two of them can bite.

---

## The one that matters: 200 redirects

`redirects.csv` maps every old HubSpot address to its new home. Two columns,
`old_url,new_path`. **This file is the source of truth, not `vercel.json`** — the
latter is only today's encoding of the same map.

Every source is on the hostname you are about to take over:

```
https://help.oxfordabstracts.com/knowledge/abstract-books
    -> /06-programme-exports-reports/abstract-books
```

**Read this bit before the cutover.** Those redirects are doing nothing today.
Nobody visits `oa-kb-test.vercel.app/knowledge/...` — there are no inbound links
to it. They become load-bearing the instant this site starts answering for
`help.oxfordabstracts.com`, when every Google result, bookmark, old email and
in-app link starts arriving at once.

That makes a botched redirect migration the single worst outcome of this move,
and a quiet one: a missing redirect returns a clean 404 and nothing alerts anyone.

They should be **permanent (308, or 301 if your platform prefers it)**.

### Verifying them

`scripts/check-redirects.py` is the acceptance test. Standard library only, no
dependencies:

```bash
py scripts/check-redirects.py help.oxfordabstracts.com
```

It requests all 200 old paths, follows redirects, and asserts each lands on HTTP
200 at the expected article. Exits non-zero if any fail. `.html` and trailing
slashes are ignored when comparing, so it tests where the reader arrives rather
than how the URL is spelled.

Baseline: **200/200 pass** against `oa-kb-test.vercel.app`, 31 July 2026.

Run it against a preview or staging host before you cut DNS over, and again
immediately after. If both pass, this move went fine.

---

## The one that is currently broken: the 404 page

`404.html` is built, correct, and reachable at `/404`. But unmatched paths on
Vercel currently return an **empty body**, and we deliberately did not fix it —
because the fix is Vercel-specific and would have been thrown away by this move.

The cause, so you don't rediscover it: Vercel serves the not-found page by
looking for a file literally named `404.html`. The `cleanUrls` setting strips
`.html` from every file, including that one, so it is published as `/404` and the
not-found handler no longer finds it. Fixing it on Vercel means replacing
`redirects` with a `routes` array containing a catch-all, and the two cannot
coexist — which would have put all 200 redirects in play to fix a cosmetic bug.

**On most other platforms this is one line of config, or automatic.** Whatever
you use, the requirement is:

> Any path that matches nothing serves the contents of `404.html`, with HTTP
> status 404.

Please do fix it as part of the move. The house design rule for this site is
"never a dead end", and right now a reader who follows a broken link gets a blank
white page — at the exact moment they most need the search box.

---

## The other three

**Clean URLs.** `/02-submissions/abstract-books` serves
`02-submissions/abstract-books.html`. Requests including `.html` should redirect
to the clean form.

Note the one consequence, because it has already caused a production bug: with
clean URLs there is no trailing slash on section pages, so relative links on them
resolve against the site root. Section-page links are therefore root-absolute in
the HTML. Don't "tidy" them.

**No trailing slash.** `vercel.json` sets `trailingSlash: false`. Match it, so
one canonical URL per page.

**Response headers.** Copy the `headers` block from `vercel.json` as-is. It
includes `Access-Control-Allow-Origin: *` on the static pages, which is **not
decorative** — the in-app help widget fetches article HTML cross-origin to render
guides inside its panel. Drop it and the widget shows empty articles.

`api/search.js` and `api/log.js` additionally send CORS headers for the
oxfordabstracts.com domains. Keep those origins accurate after the move.

---

## Environment and functions

`api/` holds three serverless functions — `search.js`, `feedback.js` and
`log.js`. Node, ESM: there is a local `package.json` with `"type": "module"`, so
they are not transpiled.

**`ANTHROPIC_API_KEY` must be set in the host's environment variables and must
never reach the browser.** It powers the two Claude calls behind search. Without
it, `/api/search` returns 200 with a null answer and the front end silently falls
back to keyword search — the site keeps working, the AI answers just stop. That
failure behaviour is deliberate; please keep it.

---

## What "done" looks like

1. `py scripts/check-redirects.py help.oxfordabstracts.com` → 200/200.
2. A made-up path returns the styled 404 page, with status 404.
3. `/02-submissions/abstract-books` loads; the `.html` form redirects to it.
4. Search returns AI answers (confirms the API key is set), and still returns
   keyword results if you unset it.
5. Section-page links all resolve — `scripts/checks.py` covers this
   structurally, but spot-check a couple live.

---

## Also worth knowing

- **Images are committed, not fetched** — 1,326 WebP files in `assets/img`. The
  old KB hot-linked them to HubSpot; those URLs die when HubSpot is cancelled.
  Please don't reintroduce remote image URLs.
- **The header logo is the last external dependency**, loaded from Storyblok
  (Oxford Abstracts' own CDN). Safe, but it is the one thing on the page you do
  not host.
- **Rebuild with `python build.py`** (needs `markdown`, `beautifulsoup4`,
  `lxml`). It regenerates the section folders and `index.html` from `corpus/`.
  It never touches `assets/img`, the hand-written JS, `api/` or `vercel.json`.
  You should not need to run it to host the site — everything is committed.
- **Two other handovers are waiting on you** and are unrelated to hosting:
  `deflection/HANDOVER.md` (support-form ticket deflection) and
  `widget/HANDOVER.md` (in-app help widget).
