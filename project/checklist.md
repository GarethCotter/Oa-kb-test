# Oxford Abstracts KB — what's left

*Updated 29 July 2026. The site is live at oa-kb-test.vercel.app with working search,
all images self-hosted, and the internal corpus in place.*

---

## Done since yesterday

- Site deployed and verified end to end — 174 articles, guided section pages, AI answers
- All 1,326 images moved off HubSpot, converted to WebP (65MB to 15MB)
- 2,740 support tickets analysed; 281 gap tickets exported for review
- 45 command.ai answers transcribed into the internal corpus
- Four production bugs found and fixed: broken import syntax, invisible answers,
  the lightbox overlay, and section links 404ing under cleanUrls

---

## 1. Content — the highest-value work left

- [ ] **Pull support replies for the 281 gap tickets** (`oa-kb-ticket-gaps.csv`).
      Most become internal-corpus notes; the recurring ones become articles.
- [ ] **Expand the ~48 truncated command.ai answers** (`oa-kb-truncated-answers.md`),
      ordered by value so you can stop early.
- [ ] **Write the top five gap articles**, from the ticket data:
      file/figure/PDF upload failures (85 tickets), backups and data retention (34),
      attendee-facing refunds (32), reviewers who can't see assigned reviews (26),
      email deliverability troubleshooting (26).
- [ ] **Fix the "Send a test email" answer** in Amplitude — it's stored as raw HTML.
- [ ] **Delete the duplicate entries** in Amplitude (unassigning, adding submissions to
      the builder, publishing the homepage, setting up a reviewer).

## 2. Decisions only you can make

- [ ] **17 plan-gating questions** (`oa-kb-plan-review.csv`)
- [ ] **Skim the 122 renames** (`oa-kb-title-renames.csv`) — the non-style ones especially
- [ ] **Participant end-banner** — participant articles currently end with nothing.
      Add one pointing to their event administrator?
- [ ] **Landing page top tasks** — three quick links inside each of the two doors?
- [ ] **Who holds the approve button** on the update pipeline

## 3. Build list (me)

- [ ] **Ticket deflection on the HubSpot support form** — needs the form details from you.
      Best data source we'll have: every interaction is a labelled outcome.
- [ ] **Weekly gap-digest email** — Monday cron, clustered unanswered questions plus
      articles rated unhelpful. Needs search logs written somewhere queryable first.
- [ ] **404 page, favicon, social share tags, skip-to-content link, collapsible mobile ToC**
- [ ] **Alt text is placeholder-quality** — every image on a page currently shares the
      nearest heading as its alt. Fine for accessibility basics, poor for real description.
- [ ] **In-app chat widget** — same endpoint, bottom-right launcher, knows what page
      she's on. Best after the search proves itself.
- [ ] **8th-grade readability pass** — standing job for the update pipeline.
- [ ] **App-testing agent** — walks flows in a test event, records undocumented behaviour
      into the internal corpus, captures fresh screenshots.

## 4. Before going live on the real domain

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
- **Search logs live in the Vercel log stream**, not a queryable store. Fine for now,
  needs solving before the weekly digest.
- **The "Most popular" list** is the real top-seven, but the pageview data was top-ten
  only — more of that list would let me pick admin-weighted quick links.
