# Oxford Abstracts KB — what's left

*Updated 29 July 2026, after the move into Claude Code. The site is live at
oa-kb-test.vercel.app with working search, all images self-hosted, and the internal
corpus in place.*

> **Read `project/context-from-conversation.md` alongside this.** It holds the evidence
> and design decisions behind these items — the search analytics, the pageview
> conclusions, and the design intent for everything not yet built.

---

## Done in the Claude Code session (29 July)

- Sources brought into the repo; `build.py` now reproduces the deployed site on Windows
- **13 Registration articles were 404ing live** — they existed in the corpus and were
  linked from the section page, but their HTML had never been committed. Now live.
- **`%-d` in `strftime` broke every "Last reviewed" badge** — a glibc extension that
  raises on Windows, swallowed by a bare `except`, so all 174 pages showed `2026-07-28`
  instead of `28 July 2026`
- 5 articles had a duplicate H1 left over from the HubSpot import — removed
- **Audience tags**: the "who this is for" sentence is now a colour-coded tag under the
  title on 99 articles — navy organisers, teal submitters, plum reviewers, amber
  attendees, all WCAG AA. Its "click here" pointed at the old HubSpot KB on all 104
  occurrences, two at analytics URLs that expired in 2023; they now point at our own
  landing-page doors.
- **Alt text**: was the nearest heading, so 39 images shared 3 strings. Now 1,342
  distinct strings across 1,343 images. Derived from surrounding text, not from looking
  at the images — see the rough edges below.
- Favicon taken from oxfordabstracts.com; 404 page built (**but see below — Vercel is
  not serving it**)
- **Two project work-lists were sitting in the AI answer store.**
  `oa-kb-truncated-answers.md` and `_review-unmapped-faq.md` are to-do lists, not
  answers. The second was in the *public* store with the path
  `corpus/_review-unmapped-faq.html`, which nothing builds — so search could have cited
  a 404 for "a reviewer can't see their reviews", one of the top gap topics. Both moved
  to `project/`. `build.py` now refuses to build if a public corpus file sits outside a
  section folder.
- `title-renames.csv` turned out to be a review, not work — all 106 renames were already
  applied. Narrowed to the 32 worth checking in `renames-to-check.md`.

## Done since yesterday

- Site deployed and verified end to end — 174 articles, guided section pages, AI answers
- All 1,326 images moved off HubSpot, converted to WebP (65MB to 15MB)
- 2,740 support tickets analysed; 281 gap tickets exported for review
- 45 command.ai answers transcribed into the internal corpus
- Four production bugs found and fixed: broken import syntax, invisible answers,
  the lightbox overlay, and section links 404ing under cleanUrls

---

## 1. Content — the highest-value work left

- [ ] **Pull support replies for the 281 gap tickets** (`ticket-gaps.csv`).
      Most become internal-corpus notes; the recurring ones become articles.
- [ ] **Expand the ~48 truncated command.ai answers** (`truncated-command-ai-answers.md`),
      ordered by value so you can stop early.
- [ ] **Place the 2 unmapped FAQ chunks** (`unmapped-faq-chunks.md`) — both are about
      reviewers and submitters not being able to see reviews.
- [ ] **Search-derived gaps** (separate from the ticket gaps, and only partly overlapping):
      copyright in submitted abstracts · what happens at the deadline · withdrawing your
      own submission · does my work save automatically · expanding the API article
      (most-searched term, one page) · reviewer troubleshooting. Evidence in the context
      doc, §2.
- [ ] **Write the top five gap articles**, from the ticket data:
      file/figure/PDF upload failures (85 tickets), backups and data retention (34),
      attendee-facing refunds (32), reviewers who can't see assigned reviews (26),
      email deliverability troubleshooting (26).
- [ ] **Fix the "Send a test email" answer** in Amplitude — it's stored as raw HTML.
- [ ] **Delete the duplicate entries** in Amplitude (unassigning, adding submissions to
      the builder, publishing the homepage, setting up a reviewer).

## 2. Decisions only you can make

- [ ] **17 plan-gating questions** (`plan-gating-review.csv`) — 0 of 17 answered. Note the
      `plan` field only *labels*, it gates nothing; a wrong value costs a ticket either
      way. Three questions: is API/integration access really on free Basic; are exports
      and reports really Abstract Management and above; are the event website and
      conference homepage Professional only?
- [ ] **Skim the 32 renames worth checking** (`renames-to-check.md`) — the other 142 are
      style-only, slug-only, or were never renamed
- [ ] **Participant end-banner** — participant articles currently end with nothing.
      Add one pointing to their event administrator?
- [ ] **Landing page top tasks** — three quick links inside each of the two doors?
- [ ] **Who holds the approve button** on the update pipeline

## 3. Build list (me)

- [ ] **Ticket deflection on the HubSpot support form** — needs the form details from you.
      Best data source we'll have: every interaction is a labelled outcome.
      Design rules in the context doc §4: never show a confidence percentage, never block
      the send, only interrupt when the answer is strong.
- [ ] **Add a confidence signal to `/api/search`** — it returns `found: true/false`, which
      is not enough to decide whether to interrupt someone. Blocks ticket deflection.
- [ ] **A "What's New" surface** the update pipeline can generate from its own PRs.
- [x] ~~Fix the card description that ran across a heading~~ — done 29 July. "Changing the
      owner of a submission" showed a stray `#`; 7 cards were affected, not 1.
- [ ] **Weekly gap-digest email** — Monday cron, clustered unanswered questions plus
      articles rated unhelpful. Needs search logs written somewhere queryable first.
- [x] ~~404 page~~, ~~favicon~~, ~~alt text~~ — done 29 July
- [ ] **Make Vercel actually serve the 404 page.** It is built, deployed and correct at
      `/404`, but unmatched paths return an empty 404 body. `cleanUrls: true` republishes
      `404.html` as `/404` (requesting `/404.html` 308-redirects), so the not-found
      handler no longer finds it under the name it looks for. The fix is converting
      `cleanUrls` + `redirects` into a `routes` array with a catch-all — `routes` cannot
      coexist with `redirects`, so all 199 are in play. Do it on a branch with a preview
      deployment, not on main.
- [ ] **Skip-to-content link** — WCAG 2.4.1 Level A. Without it a keyboard or screen
      reader user tabs through logo, search, nav and Sign in on every page. ~6 lines.
- [ ] **Collapsible mobile ToC**
- [ ] *Social share tags: dropped 29 July.* `<meta name="description">` already covers
      search engines; `og:` only changes the preview card when a link is pasted into
      Slack or email, and these articles are rarely shared.
- [ ] **In-app chat widget** — same endpoint, bottom-right launcher, knows what page
      she's on. Best after the search proves itself.
- [ ] **8th-grade readability pass** — standing job for the update pipeline.
- [ ] **App-testing agent** — walks flows in a test event, records undocumented behaviour
      into the internal corpus, captures fresh screenshots.

## 4. Before going live on the real domain

- [ ] **Pull entry pages, traffic sources and per-category totals from HubSpot** — settles
      whether the homepage audience really is organiser-dominated (context doc §1).
- [ ] **Confirm who controls DNS** for help.oxfordabstracts.com
- [ ] **Check the HubSpot contract renewal date**
- [ ] **Spot-check the 199 redirects** against the live deployment
- [ ] **Watch five real users** do three tasks each
- [ ] **Colour contrast check** on cream/navy/red against WCAG AA
- [ ] **Test on a real phone**, not a resized browser

---

## Known rough edges

- **Screenshots are old.** Many date from 2021–2023 and show a previous UI. The frame is
  new; some of the pictures aren't. The testing agent is the fix.
- **Alt text is derived, not described.** Every image now has its own specific string,
  built from the step it sits under. Nobody has looked at the images, so the alt says
  which step is pictured, not what is on screen. Same fix as above: the testing agent.
  A handful reflect weak source text — "Click on the icon, and then in the bar shown
  below" is an incomplete sentence in the article itself.
- **The header logo loads from Storyblok**, Oxford Abstracts' own CDN. Safe, but it is the
  last external dependency in the page.
- **No benchmarks are being tracked yet.** Deflection rate, failed-search rate, top
  zero-result queries and article-level "No" reasons all need somewhere to live.
- **`corpus-internal/` has not been fully reviewed.** Two of the files in and around it
  turned out to be work-lists rather than answers. The remaining 8 are worth a read on
  the same grounds: anything in there can be surfaced to any reader who asks the right
  question.
- **Search logs live in the Vercel log stream**, not a queryable store. Fine for now,
  needs solving before the weekly digest.
- **The "Most popular" list** is the real top-seven, but the pageview data was top-ten
  only — more of that list would let me pick admin-weighted quick links.
