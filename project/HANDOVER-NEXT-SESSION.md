# Handover — next session

*Written 1 August 2026 at the end of a long session. Everything below is committed
and pushed to `origin/poster-gallery-exploration`. Working tree clean.*

Read `CLAUDE.md` first — it is the house rules and it is accurate. This file only
covers what changed today and what is still open.

---

## State

- **Branch:** `poster-gallery-exploration` (pushed). The name stopped describing the
  contents around commit five; renaming now would mean deleting the remote branch,
  so probably leave it.
- **Not merged to `main`.** Six of the commits change live article content. A PR
  and a spot-check of two or three rendered pages would be sensible before merging.
- `python build.py` then `python scripts/checks.py` after any change. All ten
  checks pass right now.

## What happened today

**Two feature explorations**, both following `project/feature-exploration-brief.md`:

- `corpus-observed/poster-gallery/` — the gallery is not a thing you switch on;
  four conditions must all hold. Preview creates real registrations. Several
  article claims refuted.
- `corpus-observed/delegate-registration/` — buyer and ticket holder are different
  people everywhere and no article says so; "invoice" names two unrelated features.

**Five articles written or corrected**, live in `corpus/`: two new (paying by
invoice/bank transfer; buyers vs ticket holders), three corrected (coupons, ticket
creation, downloading invoices).

**A corpus-wide sweep**: 20 promises of videos that do not exist removed; 21 links
that pointed at HubSpot analytics wrappers rewritten; audience tags now on 182 of
182 articles; the customer portal article retired; 100 internal links removed or
unlinked.

**Four scripts added**, all re-runnable:

| Script | Does |
|---|---|
| `scripts/check-redirects.py <host>` | verifies all 200 redirects against a live host |
| `scripts/audit-screenshot-ages.py --write` | dates every image, writes the review workbook |
| `scripts/audit-internal-links.py --write` | audits editorial links, writes the review workbook |
| `scripts/capture-poster-gallery.py --admin` | Playwright screenshot capture |

## Open, in the order I would do them

### 1. Two five-minute questions only Gareth can answer

- **Does "Edit Order" / "Edit & Refund Order" exist on a real paid order?** Open any
  event that has taken a payment, click an attendee. Neither button appears on the
  demo event, but that may be because the test order is £0 with no payment provider.
  **61 tickets a year** ride on this, and it blocks fixing two articles. Detail in
  `corpus-observed/delegate-registration/findings-run-1.md`.
- **Where should Oxford Abstracts' own billing live?** Roughly a quarter of
  "invoice" tickets are organisers chasing *their* bill — payment extensions,
  overdue notices, package invoices. Not a registration topic, currently invisible
  because it shares a word. Structural call.

### 2. Screenshots

`py scripts/capture-poster-gallery.py --admin` opens a window, Gareth signs in, five
admin captures run themselves. Four public ones are already done. **The session
cannot be saved and replayed** — the app uses OAuth/PKCE with the token in memory;
three attempts failed. Budget one sign-in per admin run.

`project/screenshot-review-2021-2023.xlsx` holds the wider backlog: 134 articles
carrying 833 images from 2021–23.

### 3. The internal link review

`project/internal-link-review.xlsx` — 439 links with the sentence each sits in.
The mechanical ones are done. What remains (83 repeats, 161 general) is a reading
task, not a scripted one: **unwrapping a repeat leaves a dead cross-reference, which
is worse than the repeat**. Tried it, reverted it. Judge each on its sentence.

### 4. Content from the dossiers

`corpus-observed/delegate-registration/article-gaps.md` is the queue. Top unwritten
item is **changing what appears on an invoice after issue** — the largest delegate
theme in the ticket sample, and blocked on knowing what is changeable post-issue.

### 5. Smaller, well-defined

- Three `help.oxfordabstracts.com/tickets-view` links to the support portal are
  legitimate today but die at the hosting move → add to `hosting/HANDOVER.md`.
- Four links in `different-types-of-users-in-the-system` point the words "Event
  Administrator" at the dashboard article.
- 5 unresolved `plan:` values (`project/plan-gating-review.csv`).
- Skip-to-content link, WCAG 2.4.1 Level A, about six lines.

## Monday 3 August: the Loom project

`project/loom-transcript-mining-brief.md`. Mining ~500 of Geoff's Loom transcripts
as a new knowledge seam. **Read the brief before starting** — the two things that
are easy to get wrong are that view counts are useless (every video is a 1:1
response, so frequency must come from clustering topics) and that raw transcripts
must live outside the repo permanently, like `oa-support-replies/`.

Phase 1 is fifteen minutes: find how Loom serves transcripts, pull three samples,
and **read them**. If they are "click here, then this bit", the project becomes
topic mining only. That assumption is untested and everything rests on it.

## Things learned today that will save the next session time

- **Take a baseline before bulk edits.** Hashing all built pages before a change,
  and diffing after, caught an attempt to strip "dead" jump-link anchors that was
  actually destroying list content across 74 pages. There are **zero** dead in-page
  links reaching readers; `build.py` resolves them. That job does not exist.
- **A check that cannot fail is worth nothing.** Every check added today was
  negative-controlled: inject the fault, confirm FAIL, remove it, confirm pass.
- **The same fault wears disguises.** Old-KB links appeared as `/knowledge/`, then
  base64 inside an analytics wrapper, then behind a `t.ly` shortener. `checks.py`
  now catches all three shapes.
- **Fix the derivation, not the output.** 32 articles with a shouty "This
  information is for Admins ONLY!" line and no audience tag were one missing word
  in `build.py`, not 32 hand-edits. `corpus/` was left untouched.
- **Repetition in step-by-step guides is a feature.** Two "duplicated" sections
  turned out to be assign/unassign procedures sharing an opening. Read before
  deduplicating.
- Python is `py`, not `python`. Scripts must have **no shebang** — `py` honours
  `#!/usr/bin/env python3` and hits the Windows Store stub.
- Pushing needs a real PowerShell terminal.
