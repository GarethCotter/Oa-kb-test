# Handover — next session

*Written 4 August 2026. Everything below is committed and pushed to `main`.
Working tree clean, 14 checks passing. Replaces the 3 August handover.*

Read `CLAUDE.md` first — it is the house rules and it is accurate. It now has a
section at the top about **who is asking**, because the help centre is edited by
talking to Claude rather than by hand.

---

## State

- **On `main`, and `main` is live.** Vercel deploys about a minute behind a push.
- **Publish with `py scripts/publish.py "what changed"`.** It rebuilds, runs every
  check, and only then commits and pushes. Nothing is pushed if a check fails.
  There is no `--force` and there should not be one. `--dry-run` stops before git.
- **Fourteen checks** in `scripts/checks.py`, all passing.
- Python is `py` on this machine, not `python`.

## Do these before the engineering handover

Ordered by what blocks what. The first two have lead times and nothing else
finishes without them.

### 1. Rate-limit `/api/search`

**Confirmed unprotected on 4 August**: five rapid POSTs returned five 200s, no 429.
It is unauthenticated, makes two paid model calls per request, and is about to sit
on a public hostname. `api/suggest.js` already has the pattern — honeypot, per-IP
window, 429. About an hour.

### 2. Get off the personal accounts

The Vercel project, the Anthropic key, the Google account behind the sheet and the
GitHub repo are all Gareth's personally. Each is a single point of failure attached
to one person. Not technical work, but it has a lead time.

### 3. Four smaller things, all verified open

- **Skip-to-content link missing on 199 of 202 pages.** WCAG 2.4.1 **Level A**.
  `/suggest` has one, the KB does not. ~6 lines in `build.py`.
- **Confirm the interaction log is covered by the privacy policy.** It stores
  customers' questions verbatim in a Google Sheet. `api/log.js` strips emails and
  phone numbers by regex; nothing stops someone typing a name or an event ID.
- **Clear the test rows from the sheet** so Kristy's first real week is not polluted.
- **Tell staff about `?oa-internal=1`.** The message is written; it works on the KB
  today, and needs repeating for the app and support form once those are deployed.

### 4. Half an hour signed in to the app

Closes seven things at once — the six items in
`Desktop\Claude\oa-loom-transcripts\VERIFICATION-QUEUE.md` plus the last unanswered
FAQ. Ordered there by risk; item 1 is the one where the live site may be wrong.

## What happened on 4 August

**The internal answer store was public and no longer is.** `assets/articles.json`
carried all 41 `corpus-internal/` notes in full and was served as a static file —
617KB, HTTP 200, no auth. `api/search.js` imports it from disk, so it never needed
to be reachable over HTTP. Now 307s to `/404`. `scripts/internal-review.py` renders
the notes as the router sees them; its output is gitignored, because **anything
committed here is served by Vercel** and that is exactly how this happened.

**21 of the 22 empty "Common questions" are answered.** Every one from content
already on its own page — the FAQ silo merge had carried the questions across and
dropped the paragraph that joined them to the answer. `check_faq_answered` is
pinned at **1**. The one left is *"How do I delete a registration?"*, deliberately
unanswered: the article lists what an admin can change and deletion is not among
them, so answering it would have been a guess.

**The performance dashboard is per-surface.** Knowledge base, widget and deflection
each get their own section, because blending them hid the differences worth acting
on. New **What people ask** tab groups questions by the article the router chose,
so thirteen wordings of one question count as one topic asked thirteen times.
`snapshotMonth()` keeps a monthly history. Paste `scripts/sheet-logger.gs`, Save,
**Run → setup** — no redeploy needed, `doPost` is untouched.

**An internal-team marker.** `?oa-internal=1` once per browser; `api/log.js` then
stores the surface as `kb-search-internal`. Marked, not dropped, so a flag left on
shows in the sheet rather than silently deleting a reader's data.

**Kristy edits the help centre by talking to Claude.** Claude desktop app → **Code**
tab → the repo folder on her machine. `scripts/update-article.js` was broken — it
read `site/assets/search-index.json`, a path from an older layout, so every run had
died on ENOENT before reaching Claude. Fixed. `kb-checks.yml` runs the build and
checks on every push and pull request.

**`/knowledge` was not redirected.** It returns 200 on HubSpot today and 404ed here
— the site-wide "Visit knowledge base" link, on the home page, /about, /pricing and
several blog posts. `check-redirects.py` could never have caught it: it verifies
what is *in* the map. Found by crawling the marketing site for links *to* the old
KB. Now 201/201.

**Event details rewritten against the redesigned page.** Two of the old article's
facts were wrong — the country list is now editable text, not click-to-deselect,
and "More options" is now "Advanced" — and two whole sections were missing, Stages
and Deadlines. The old screenshots spanned 2021–2026 and were removed rather than
left contradicting the page. **Fresh screenshots are the one outstanding gap.**

**Heading anchors hide until hover.** 515 of them across 179 pages were rendering
permanently, and 102 `h4` anchors matched no rule at all and rendered as full-size
red text.

**A link-target audit.** `py scripts/audit-link-targets.py` finds links that
resolve perfectly but point at the wrong article — the failure a crawler cannot
see. Four candidates; the strongest is verified real: a link reading *"Creating
custom emails"* pointing at `editing-the-template-emails`.

## Design work that is NOT built

Explored with Gareth on 4 August, agreed in principle, nothing implemented. These
are product changes for the app team, not the help centre.

- **Event details page**: move the custom country list into a collapsed **Advanced**
  drawer with API and event code, showing each setting's current state on its row so
  nobody has to open it to check. Auto-expand if a setting is non-default.
- **Merge Stages into Deadlines**, with deadlines as the section and each stage a
  card inside it. Deadlines are per-stage and the current split means adding a stage
  silently changes a heading further down the page.
- **Combine each deadline with its form's open/closed switch**, which is how the
  dashboard already works. That combination is what makes "deadline passed, form
  still open" detectable — today it is invisible.
- **Gate "Add another stage"** behind the Multi-stage add-on as a visibly locked row
  that opens a panel with the benefit, the price and a link to the help centre.
  Three things need confirming first: what $650 buys (per event? per year?), whether
  it self-serves, and whether package tier gates it too.

## Settled — do not re-litigate

**The 404 page works.** The 3 August handover said it returned an empty body on
Vercel. Checked on 4 August across six shapes of missing path — bare slug, missing
article in a real section, near-miss on a real slug, unmapped `/knowledge/` address,
missing asset, deep nested path. All six: status 404, styled page, search box.
Document 1 was still telling engineers to fix it; that has been corrected. Re-check
after the migration, because it is easy to lose and nothing will tell you.

## Where things live

| What | Where |
|---|---|
| Engineer handover documents (4 Word files) | `Desktop\Claude\oa-handover-docs\` |
| Loom transcripts, findings, verification queue | `Desktop\Claude\oa-loom-transcripts\` — **outside the repo, permanently** |
| Unanswered FAQ work-list | `project/unanswered-faq-questions.md` |
| Hosting reference for engineers | `hosting/HANDOVER.md` |

The four documents are: the knowledge base, the help widget, support deflection,
and a short demo brief on why it is better. Plus a separate guide written for
Kristy rather than for engineers.

## Things learned that will save time

- **`py` reads shebang lines.** `#!/usr/bin/env python` sends it to the Microsoft
  Store stub and the script dies before running. `build.py`, `checks.py` and
  `publish.py` all have no shebang, deliberately.
- **The preview pane does not composite frames**, so any transitioned property reads
  frozen at its start value. Disable the transition before measuring. This produced
  a false "the fix does not work" during the anchor work.
- **`:focus` needs the document to have focus.** In an undisplayed pane it never
  matches, which reads as a broken rule rather than an untestable one.
- **Do not run `publish.py` to "test the guards".** It published on a tree that was
  not as clean as assumed. `--dry-run` exists now for that reason.
- **Never interpolate `${{ github.event… }}` into a `run:` block.** The first draft
  of a workflow did, which is the standard Actions script-injection hole.
- **A passing redirect check does not mean full coverage** — it only tests what is
  already in the map. Crawl the other direction too.
