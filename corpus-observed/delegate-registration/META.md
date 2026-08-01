---
feature: delegate-registration
observed: true
app_version: unknown
explored: 2026-08-01
plan: professional conference
---

# Assignment

- **Feature:** delegate registration — tickets, groups, add-ons, coupons, the
  registration form, the attendee-facing purchase path, and orders/attendee table
- **Plans to explore under:** Professional Conference (demo event 78206 is the only
  event available; other plans `[untested]`). Note the articles claim registration is
  on **all plans including free Basic**, which this run cannot verify.
- **Test account:** Gareth's admin account on demo **event 78206**
- **App version / date:** run started 1 August 2026; no version string visible
- **Existing articles covering this feature:** 19 in `corpus/07-delegate-registration/`,
  plus registration mentions in 01-getting-started and 10-integrations-api

## Why this feature

Registration is the biggest ticket cluster in the analysis after submissions:

| Tickets | Theme | Article |
|---:|---|---|
| 193 | Invoices & receipts | `downloading-invoices-and-receipts` (228 words, 4/4 screenshots stale) |
| 32 | Refunds & cancellations | admin article exists; tickets are mostly *attendees* asking |
| 29 | Editing registrations / attendee details | `how-admins-can-amend-existing-delegate-registration-orders` |
| 22 | Discount / coupon codes | `creating-coupon-codes-for-delegate-registration` |
| 8 | SSO / institutional login | none |
| 3 | Ticket limits / restricting purchases | none |
| 2 | Manually registering an attendee | none |

**Invoices and receipts is the single largest theme in the entire 4,898-ticket
analysis**, and it is answered by the shortest article in the section.

16 of the 18 illustrated articles in this section carry pre-2025 screenshots; the two
largest carry 29/30 and 22/23.

## Hard boundaries for this run

- **No purchase will be completed and no payment details will be entered.** Not by
  card, not by any saved method. The attendee path will be walked as far as the
  payment step and no further. Agreed with Gareth up front, and it is a standing rule
  regardless.
- **Registration will not be published** without asking first. Publishing may make
  tickets genuinely purchasable by the public on a live domain, and the event carries
  a real £2,490 pending balance. Preview only unless Gareth says otherwise.
- **No refund will be issued**, since that moves real money.
- Synthetic data only — "Test Attendee One", "test.attendee.one@example.com".
- Nothing written to `corpus/` or `corpus-internal/`; this dossier only.

## What is expected to limit the run

- The above boundaries mean the **post-payment half of the funnel is unreachable**:
  order confirmation, receipts, invoices, refunds and the transactions table all
  require a completed purchase. That is precisely where the 193-ticket theme lives.
  Those claims will be marked `[untested]` with a note on what would settle them —
  most likely a free (£0) ticket, which may pass through the same confirmation and
  receipt path without any money moving. **That is the one experiment worth trying**
  and it is listed below.
- No attendee account, so the attendee-side dashboard route to receipts is
  `[untested]` unless a £0 order can be completed.

---

# Verification list

Checkable claims from the articles, to be marked **confirmed**, **changed** or
**could not verify**.

## From `creating-your-delegate-registration-tickets-for-your-event.md`

| # | Claim | Status |
|---|---|---|
| 1 | Path is **Registration → Tickets → Create Tickets** | |
| 2 | The ticket dashboard has **Tickets, Add-Ons and Coupons** at the top | |
| 3 | "Create Ticket" is a **blue button in the middle of the screen** | |
| 4 | A ticket has a **name** and **description** | |
| 5 | Currency is changed by clicking the blue **"Finance"** word above the price box | |
| 6 | Ticket price defaults to **0.00 (free of charge)** | |
| 7 | **"Add tax"** sits below the price box | |
| 8 | There is a **"Quantity Available"** box | |
| 9 | You can select the **dates tickets are available for purchase** | |
| 10 | You can assign a ticket to a **group** | |
| 11 | Button at the bottom is **"Create Ticket"** | |
| 12 | Edit/delete via **three dots at the end of the row** | |
| 13 | **"Create Group"** appears mid-page with no tickets, top right with tickets | |
| 14 | Group creation opens a **pop-up on the right-hand side** | |
| 15 | Hidden tickets let admins buy on behalf of a user | |

## From `creating-coupon-codes-for-delegate-registration.md`

| # | Claim | Status |
|---|---|---|
| 16 | Coupons are reached via **Registration → Tickets → Coupon tab (top right)** | |
| 17 | **"Create Coupon"** button, opening a right-hand pop-up | |
| 18 | Fields: Coupon Name, **Discount amount (percentage)**, Quantity Available, date range | |
| 19 | Coupons can be limited to chosen tickets and add-ons via **"Add Tickets" / "Add Addons"** | |

## From `downloading-invoices-and-receipts.md`

| # | Claim | Status |
|---|---|---|
| 20 | After payment, the **Order Details Confirmation** screen shows a **"Download Receipt"** dropdown at top right | |
| 21 | The dropdown offers both **receipt and invoice** | |
| 22 | Later, an attendee signs in, finds the event box, clicks **"View Details"**, and uses the same dropdown | |

## Open questions to answer by observation

- **Q1** Can a **£0 ticket** be bought end to end without any payment step? If so it
  unlocks the confirmation screen, receipts and the attendee dashboard — the
  193-ticket theme — with no money moving.
- **Q2** What actually gates registration going live? Is "publish" a single switch,
  and is there any warning about what it exposes?
- **Q3** What does the attendee see before payment — which fields are mandatory, and
  what does the form look like with no tickets configured?
- **Q4** Are there ticket **limits/restrictions** (per person, per group)? Three
  tickets asked and no article exists.
- **Q5** How does an admin **register someone manually** / buy on behalf? Two tickets,
  no article, and "hidden tickets" is mentioned but barely explained.
- **Q6** What are the exact **error and empty states** across the section? None of the
  19 articles quotes a single one verbatim.

## Article defects already visible before opening the app

Recorded here because they are certain, not observations of the product.

**Reaches the reader:**

- `creating-your-delegate-registration-tickets-for-your-event.md` — the sentence
  "Plus You can learn how to purchase tickets on behalf of attendees." appears twice,
  once stranded on its own line above the standfirst.
- That article and the coupons article both open with "You can either watch the video
  below for a step-by-step walkthrough…" but **no video is embedded in either page**.
  `downloading-invoices-and-receipts.md` does the same ("please watch the below
  video"). Three articles promise a video that is not there — plausibly lost in the
  HubSpot migration, and worth checking across the whole corpus.

**Does *not* reach the reader — source cruft only:**

- The mangled `[Hidden Tickets — … a u](#hidden-tickets)ser.` link, and the
  `[here.](#instructions)` link in the invoices article, both point at anchors that
  do not exist. **Verified against the built HTML: `build.py` strips hand-written
  jump-link blocks**, so neither reaches the page and `scripts/checks.py` passes.
  Same behaviour as the poster gallery article's `#GO` anchors. Worth deleting from
  the markdown for whoever edits next, but it is tidying, not a live fault.
