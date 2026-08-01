---
feature: delegate-registration
observed: true
app_version: unknown (module URL is delegate-registration-v3)
explored: 2026-08-01
plan: professional conference
---

# Delegate registration — article gap list

Proposed articles and edits, each with evidence. A human decides what gets
written; nothing here goes into `corpus/` or `corpus-internal/` unchecked.

## The framing

The module URL is **`delegate-registration-v3`**. It has been rebuilt, and the
section's articles largely describe an earlier version: 16 of 18 illustrated
articles carry pre-2025 screenshots, the two largest at 29/30 and 22/23. Several
articles name buttons that no longer exist.

But the bigger problem is not staleness. It is that **two structural facts about
this module are absent from all 19 articles**:

1. **Buyer and ticket holder are different people, everywhere.** Confirmation
   emails, the transactions tab, the attendee panel and the invoice all key on one
   or the other, inconsistently.
2. **"Invoice" names two unrelated features** — the documents, and a payment
   method.

Most of the individual confusions below are consequences of those two.

---

## Priority 1 — rewrite "Downloading invoices and receipts"

**Edit:** `corpus/07-delegate-registration/downloading-invoices-and-receipts.md`
(228 words — the shortest article in the section, against **193 tickets a year,
the largest single theme in the 4,898-ticket analysis**)

**Scope:** answer all four routes, not two, and split the word "invoice".

**Evidence:**

- The article documents only the two **attendee** routes. Observed, there are two
  **admin** routes as well: **Registrations table → click the row → "Order
  downloads"** (Receipt / Invoice) and **→ "Email"** (Receipt / Invoice), the
  latter sending it straight to the attendee.
- `[inferred]` most of the 193 are organisers asking *"how do I get my attendee
  their invoice"*, which the current article never answers. **Check a sample of
  the raw tickets before acting** — this inference is the load-bearing one on this
  whole list.
- Exact labels are **"Download receipt"**, **"Receipt - 2"**, **"Invoice - 1"** —
  the article's "Download Receipt" is close but the numbering is undocumented.

**Also worth its own section or article:** invoice *content* is configurable at
**Payment providers → "Configure invoice and receipts"** — title, which event and
customer details appear, a **"show on invoice"** toggle on individual form
questions, and **"Generate preview"**, which renders an invoice without needing an
order. None of it is documented, and it answers "can we put our logo / VAT number
/ PO number on it".

## Priority 2 — new article: paying by invoice / bank transfer

**Title:** Letting attendees pay by invoice or bank transfer
**Scope:** what delayed payments are, the fee collection card prerequisite, and
custom questions on the invoice.

**Evidence:**

- **Nothing in the corpus covers this.** Observed at **Finance → Payment providers
  → Configure invoice and receipts → Delayed payments**, verbatim: *"Offline
  payments allows people to complete their purchase by requesting an invoice and
  then transferring the amount to you, e.g. via bank transfer."*
- Prerequisite, verbatim: *"To activate offline payment you must first add a fee
  collection card. This is so we can collect Oxford Abstracts fees on offline
  invoices."*
- **"Custom questions for delayed payments"** — *"These questions and responses
  will appear on the invoice. E.g. tax number, or company address."* This is the
  answer to the classic "our finance department needs a PO number on the invoice",
  and it exists nowhere in the docs.
- **"Payment links"** is named in the same panel and appears in no article at all.

University and hospital delegates routinely cannot pay by card. This is a
commercially significant gap, not just a documentation one.

## Priority 3 — new article: who gets what email, and who owns an order

**Title:** Buyers, ticket holders and who receives what
**Scope:** the buyer/holder distinction and its consequences.

**Evidence:**

- Confirmation banner, verbatim: **"ORDER CONFIRMED AND EMAIL SENT TO
  \<buyer\>"** — the ticket holder receives nothing at that point.
- Confirmation screen shows *"Test Attendee One | test.attendee.one@example.com"*
  / *"Bought by \<buyer\>"*.
- Attendees tab is keyed on the holder; Transactions on **ORDER OWNER**, the
  buyer; the attendee panel says **"Order created by"**; the invoice offers
  **"Buyer email"** as a customer detail.
- Related existing articles that each cover a fragment:
  `completing-registration-when-someone-bought-your-ticket` (135 words),
  `registering-on-the-behalf-of-someone-else` (160 words),
  `changing-the-email-address-on-a-registration` (237 words). Three short articles
  circling one concept none of them names.

## Priority 4 — correct the ticket-creation article

**Edit:** `creating-your-delegate-registration-tickets-for-your-event.md`
(1,346 words, 29 of 30 screenshots pre-2025)

| Currently says | Should say |
|---|---|
| Path **Registration → Tickets → Create Tickets** | **Registration → Tickets → Conference tickets** |
| "Create Ticket", a **blue** button mid-screen | **"Create ticket"**, navy; moves to **top left** once a ticket exists |
| Currency via the blue **"Finance"** word **above** the price | link **"Change currency here."** **below** the price box |
| **"Add tax"** below the price box | **gone** — tax is a rules system at **Finance → Tax** |
| "Create Group" **top right** | **top left** |

**Add, all undocumented and all answering real tickets:**

- **"Maximum number of tickets per order"** — 3 tickets ask about restricting
  purchases; no article mentions it
- **"Hide ticket (visible to admins only)"** — the actual mechanism behind the
  article's "hidden tickets" section
- **Ticket groups control which questions and add-ons an attendee sees**, verbatim
  helper text: *"Use ticket groups to control which add-ons and questions are
  shown to attendees based on their ticket."*

## Priority 5 — correct the coupon article

**Edit:** `creating-coupon-codes-for-delegate-registration.md` (22 tickets)

- The field is **"Coupon code"**, not "Coupon Name"
- **Discounts are not percentage-only.** A **"Discount type"** dropdown offers
  **"Percentage (%)"** and **"Amount ($)"**. The product's own empty state says
  *"Choose amount or percentage price reductions"*; the article says percentage.
  This is the article's central concept and it is wrong.
- Undocumented **"Deactivate coupon"** toggle
- Controls are **"Available with selected tickets"** and **"Add addons"**, not
  "Add Tickets"/"Add Addons"

## Priority 6 — new article or section: the registration form is a grid

**Scope:** that the form is questions × ticket groups, and the ten question types.

**Evidence:** observed at **Registration → Form** — a matrix with a toggle per
cell. Name and Email are locked and required. Types are Dropdown, Checkbox, Radio,
File Upload, Phone number, Email, Address, Short text, Long text, Text block
(read only) — **a completely different set from the submission form builder**.
`creating-your-delegate-registration-form` (807 words, 22/23 stale) predates this.

Also note the **"show on invoice"** per-question option referenced from the
invoice panel. `[untested]` — needs confirming inside question setup.

## Priority 7 — the publishing prerequisites

**Edit:** `previewing-and-publish-your-event-registration.md`

- Publishing is a **toggle** — **"Visible to the public"** — beside **"Allow
  attendee to edit responses"**, not a button
- **"Set up your payment provider in order to publish paid tickets"** — a hard
  gate, stated only on the payment providers page
- **Authorize.net requires the event currency to be USD** (stated in red)
- **Invoice payments require a fee collection card**
- The **"Tips before you publish"** checklist, which ticks off completed steps
- **And a warning that Preview completes real orders** — see below

---

## Not article gaps — product issues to route

1. **"Preview" creates real registrations.** Walking the preview flow to
   completion produces a persisted order, an attendee record and a real
   confirmation email, on an unpublished event, with no warning. The most
   consequential finding of the run.
2. **A £0 order shows as "Paid"** with **"Payment method: Offline"** on an event
   where offline payments are explicitly not configured.
3. **One timestamp, two timezones on one screen** — 15:49 BST in the table, 14:49
   in the detail panel, unlabelled.
4. **"Amount ($)"** on a GBP event.
5. **Inconsistent copy inside one module** — "Change currency here." versus
   "Change currency in the finance tab".
6. **Grammar on money screens** — "1 rows", "Add a tax rules", "Offline payments
   is not currently configured."
7. **`/delegate-registration-v3/registrations`** returns a bare "Page not found."
   with no way back — and it is the path both the refund and amendment articles
   send people to.

## Must be settled before writing

**Do the "Edit Order" and "Edit & Refund Order" buttons exist on a real paid
order?** Both the amendment article (29 tickets) and the refund article (32
tickets) hinge on them, and neither appears on this event. I could not distinguish
"removed in v3" from "only shown for paid orders with a connected provider".

A five-minute check on any event that has taken a payment settles it, and it
decides whether those two articles need a light edit or a rewrite. **61 tickets a
year depend on the answer.** Do not act on this list's assumptions here.

## Suggested internal notes

One fact per note, keywords in the first 160 characters, title *is* the answer:

- **"How do I send an attendee their invoice or receipt?"** — Registrations table,
  click the row, Email → Invoice or Receipt.
- **"Can attendees pay by bank transfer or invoice?"** — yes, via delayed
  payments; needs a fee collection card first.
- **"How do I put a PO number or VAT number on the invoice?"** — custom questions
  for delayed payments.
- **"Can a coupon be a fixed amount rather than a percentage?"** — yes, Discount
  type → Amount.
- **"Why can't I publish my paid tickets?"** — a payment provider must be
  connected first.
- **"Can I limit how many tickets one person buys?"** — yes, "Maximum number of
  tickets per order" on the ticket.
