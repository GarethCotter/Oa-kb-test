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

## CORRECTION — read `ticket-sample-findings.md` before using this list

The original version of this file claimed the 193-ticket invoice theme was mostly
organisers asking *"how do I get my attendee their invoice"*. **A read of 30
random invoice tickets on 1 August showed that was wrong**, and it was the
load-bearing assumption here. Four distinct themes exist and retrieval is one of
the smaller ones. Priorities below are revised accordingly.

## Priority 1 — new article: changing what appears on an invoice

**The biggest delegate-registration invoice theme, and wholly undocumented.**

**Scope:** what can be put on an invoice, how, and what can be changed after the
fact — attendee or company name, billing address, PO number, VAT number, invoice
note text.

**Evidence:**

- Roughly a quarter of a 30-ticket sample. Requests observed: correct a name on an
  issued invoice, add a company name, add a PO number, add a billing address,
  amend invoice note text. **Several organisers state they do not think they can
  do it themselves** and ask support to do it for them.
- The product surface exists and is undocumented: **Payment providers → "Configure
  invoice and receipts"** (invoice title, which event and customer details appear,
  **"Generate preview"**), the **"show on invoice"** toggle on individual form
  questions, and **"custom questions for delayed payments"** whose responses appear
  on the invoice — the panel explicitly suggests *tax number* and *company
  address*.
- One ticket independently confirms the buyer/holder split: an organiser can
  capture the buyer's address via the registration form **when the buyer is also
  the ticket holder**, but not when someone buys for another person.

**Open question this article must answer, and I could not:** what is changeable
**after** an invoice has been issued, and by whom? Organisers are escalating
because they believe it is not self-service. `[untested]`.

## Priority 1b — rewrite "Downloading invoices and receipts"

Still worth doing, but **smaller than I first claimed**.

**Edit:** `corpus/07-delegate-registration/downloading-invoices-and-receipts.md`
(228 words)

- It documents only the two **attendee** routes. Two **admin** routes exist and are
  undocumented: **Registrations table → click the row → "Order downloads"**, and
  **→ "Email"**, which sends it straight to the attendee.
- Exact labels: **"Download receipt"**, **"Receipt - 2"**, **"Invoice - 1"**.
- Note from the sample: several retrieval tickets are **fault reports** — "File not
  found" on a receipt link, an error page viewing receipt and invoice, an attendee
  locked out after changing their email. **An article would not have deflected
  those**; they belong on the product list.

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

## SETTLED — 3 August 2026

**The buttons exist. The run missed them, and the run's conclusion was wrong.**

Gareth checked a real order: open **Registration → Registrations**, click the
attendee's row, then **the three dots at the top right of the panel** — the menu
holds **"Edit or refund order"** and **"Delete attendee"**.

Three corrections follow:

1. **It is one menu item, not two buttons.** The amendment article called it
   "Edit Order" and the refund article called it "Edit & Refund Order"; both names
   are wrong and the single real one, **"Edit or refund order"**, covers both jobs.
   Both articles are now corrected.
2. **Nothing is gated on payment.** It appeared on an order whose total was
   €0.00 — status "Paid", a free ticket. The "only shown for paid orders with a
   connected provider" theory was wrong.
3. **The articles' navigation was right all along.** Both already said "click the
   three dots at the top right"; only the label was wrong. So this was a two-line
   fix, not the rewrite this file predicted.

**The lesson worth keeping:** an option behind a kebab menu reads as absent. The
run recorded "neither button appears" from a screen where both were one click
away. Where a dossier says a control is missing, check the ⋮ before concluding it
was removed.

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
