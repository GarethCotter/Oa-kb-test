# What 2,740 support tickets say about the knowledge base

*Analysis of every support-form ticket from 1 January 2025 to 29 July 2026. All names,
email addresses and phone numbers were stripped before analysis and none appear in any
output.*

---

## Headline

**Volume is flat to rising.** Roughly 140 tickets a month through 2025, ~165/month
across 2026 so far. The old KB is not deflecting a growing product.

Every ticket is, by definition, a moment where self-service failed. The useful question
isn't "how many could the KB answer?" — it's **which recurring questions keep arriving,
and why didn't the KB stop them?**

Three answers, in order of size:

1. **Content that exists but wasn't found.** The largest group. An article covers it, but
   the person didn't get there.
2. **Content that doesn't exist.** Real gaps — 281 tickets across 14 themes.
3. **Things the KB can never fix.** Invoicing, licences, refunds needing a human. Around
   a fifth of all tickets. Worth excluding from any deflection target so the target stays honest.

---

## The recurring themes

Multi-tagged, so a ticket can appear in more than one row. 55% of tickets matched at
least one theme; the untagged remainder are mostly one-off, event-specific queries.

### Covered by an existing article — a findability problem

| Tickets | Theme | Article that should have answered it |
|---:|---|---|
| 193 | Invoices & receipts | Downloading invoices and receipts |
| 121 | Deadline changes / extensions | Opening and closing submissions (deadlines) |
| 112 | Login & password problems | Creating an account and logging in |
| 102 | Editing or withdrawing a submission | Editing an abstract or submission |
| 100 | Assigning reviewers | Assigning and unassigning a submission to a reviewer |
| 77 | Abstract books / custom exports | Abstract books |
| 73 | New event setup | Creating and paying for a new event |
| 61 | Certificates | Creating a certificate *(add-on)* |
| 59 | Integrations & API | Application programming interface (API) |
| 46 | Poster gallery / poster upload | Professional Conference — the poster gallery |
| 45 | Verification email problems | If your verification email hasn't arrived |
| 37 | Programme / session building | Creating a session |
| 37 | Exhibitors & sponsors | Professional Conference — exhibitor space |
| 30 | Authors & affiliations question | The authors and affiliations question |
| 33 | Decisions / acceptance notifications | Notifying submitters of their outcomes |
| 29 | Editing registrations / attendee details | How admins can amend existing orders |
| 25 | Editing or scheduling emails | Editing the template emails |
| 24 | Zoom / streaming | Setting up your Zoom integration |
| 22 | Discount / coupon codes | Creating coupon codes |
| 21 | Incomplete submission | The submissions table (including incomplete submissions) |

**This is the single biggest finding: over 1,200 tickets are about things already
documented.** The new KB attacks this directly — better titles, typo-tolerant search,
the AI answer layer, guided section pages — so it's the clearest place to measure whether
the rebuild works.

Two worth singling out:

- **Invoices & receipts (193)** — the biggest documented theme by far, and it spans both
  event invoices (organisers paying you) and attendee receipts. Worth checking the existing
  article covers both, because the ticket text suggests people asking about quite different things.
- **Deadlines (121)** — vindicates the retitle. This was searched 24 times with 4 clicks and
  the word appeared in no article title; it's now in one.

### No article exists — genuine content gaps

**281 tickets. These are in `oa-kb-ticket-gaps.csv` for you to look up the replies.**

| Tickets | Gap | What to do |
|---:|---|---|
| 85 | File / figure / PDF upload failures | **Write an article.** Biggest single gap. Submitters and organisers both hit it; causes look varied (file size, type, browser). |
| 34 | Backups / archiving / data retention | **Write an article.** "How long do you keep our data / how do I get a backup" is asked constantly and there's only a partial answer. |
| 32 | Refunds & cancellations | Article exists for admin refunds — but these are mostly *attendees* asking. Needs a participant-facing version. |
| 26 | Reviewers cannot see assigned reviews | **Write an article.** Predicted this from the old FAQ; the tickets confirm it. |
| 26 | Emails not delivered / bounced / spam | **Write an article.** DKIM is documented; "my submitters got nothing, what do I check" isn't. |
| 23 | Email address change / merging accounts | **Internal note at minimum** — may need support to action, but the rules should be written down. |
| 19 | Presentation upload by presenters | Participant-facing gap. |
| 17 | Downloading submissions as individual files | Partially covered by exports, but people can't find it and hit failures. |
| 11 | Visa / letters of invitation | Recurring, and probably a flat "we don't do this, here's what to do instead". |
| 8 | SSO / institutional login | Small but high-effort tickets. |
| 5 | Wrong or duplicate account used | Good internal-note candidate. |
| 3 | Ticket limits / restricting purchases | Feature question — internal note. |
| 3 | Unwanted / repeated emails | Internal note. |
| 2 | Manually registering an attendee | Quick note. |

### Not a KB problem

| Tickets | Theme |
|---:|---|
| 138 | Pricing, licences, upgrades & renewals |
| 22 | Trial extensions |
| 4 | Enquiries not in English |

Commercial conversations that need a human. Around 160 tickets — worth routing rather than
documenting. **Worth noting: 4 tickets arrived in Spanish or French.** Tiny, but the AI
answer layer can respond in the user's language at no extra cost, which the old KB couldn't.

### One symptom-level cluster

**219 tickets mention an error message** (404, 500, "network failure", "something went wrong").
This isn't a topic — it's how people describe wildly different underlying problems: a failed
invoice view, a broken submission form, an email-change error. Two implications: a generic
"error" article won't help much, and **error messages that named the actual problem would
deflect more tickets than any article**. That's a product fix, not a docs fix.

---

## What I'd do with this

1. **Write the top five gap articles** — upload failures, backups/retention, reviewers can't
   see reviews, email deliverability troubleshooting, attendee-facing refunds. That's ~200
   tickets a year of coverage.
2. **Pull the support replies for the gap CSV** (281 tickets). Those replies are the raw
   material — most become internal-corpus notes immediately, and the recurring ones become articles.
3. **Treat the 1,200 findability tickets as the benchmark.** Re-run this analysis six months
   after launch: if the rebuild works, those themes should shrink while the gap themes stay flat.
4. **Feed the ticket vocabulary into the search synonym map** — this is real user language, and
   better than my guesses.

---

## Caveats

- Themes are keyword-matched, so counts are indicative, not exact. A ticket mentioning
  "invoice" in passing is counted under invoices.
- Multi-tagging means the column doesn't sum to 2,740.
- 45% of tickets matched no theme — mostly one-off, event-specific queries. I sampled these
  and pulled out the recurring ones, but there will be more signal in there if we want it.
- I only see the customer's question, not your reply, so "no article exists" means *the KB
  doesn't cover it*, not that the answer is unknown. Your replies are the missing half.
