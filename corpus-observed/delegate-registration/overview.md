---
feature: delegate-registration
observed: true
app_version: unknown (module URL is delegate-registration-v3)
explored: 2026-08-01
plan: professional conference
---

# Delegate registration — overview

## What it is

A ticketing and attendee-management module. Organisers define **tickets**,
optionally grouped, optionally with **add-ons** and **coupons**; attendees buy
through a two-step public flow; the resulting **orders**, **attendees** and
**transactions** are managed from a table, with **invoices and receipts** generated
per order.

## The mental model a user needs

### 1. Buyer and ticket holder are different people, everywhere

This is the single most load-bearing fact about the module, and no article states
it. One person can buy tickets for others, and the product keeps the two roles
separate throughout:

| Where | Keyed on |
|---|---|
| Order confirmation email | **buyer** |
| Attendees tab | **ticket holder** |
| Transactions tab (ORDER OWNER) | **buyer** |
| Attendee detail panel ("Order created by") | **buyer** |
| Invoice customer details ("Buyer email") | **buyer** |

So the same order appears under two different names depending which tab you are
on, and the person holding a ticket may never have received an email. Almost every
confusing thing in this module traces back to this distinction.

### 2. "Invoice" means two unrelated things

- **Invoice/receipt documents** — the PDFs generated per order, downloadable or
  emailable by either the attendee or an admin.
- **Invoice payments** — a *payment method* where the attendee requests an invoice
  and pays offline, e.g. by bank transfer. Configured under **Delayed payments**,
  and requires a fee collection card.

Two features, one word, and the documentation covers only the first.

### 3. Ticket groups are the control mechanism, not a label

A **ticket group** is not a display category. It determines **which registration
form questions and which add-ons an attendee sees**. The registration form is a
grid — questions down the side, ticket groups across the top, a toggle in each
cell.

Add-ons and coupons can *also* be scoped directly to individual tickets, so there
are two overlapping mechanisms. `[untested]` how they interact when they disagree.

### 4. Nothing is public until a toggle is flipped — but Preview is not safe

**"Visible to the public"** on the Publish page is what exposes registration.
Until then the link does not work for the public.

**But the Preview button walks the real purchase flow.** Completing it creates a
real order, a real attendee record and a real confirmation email, on an
unpublished event. See `findings-run-1.md`.

### 5. Paid tickets need a payment provider before they can be published

Stated on screen: *"Set up your payment provider in order to publish paid
tickets."* Free tickets do not need one. Four providers exist — Stripe, PayPal,
Authorize.net and Invoice payments — and two of them have hard prerequisites
(Authorize.net needs the event currency to be USD; invoice payments need a fee
collection card).

## Where each piece lives

| Piece | Path |
|---|---|
| Tickets, groups | **Registration → Tickets → Conference tickets** |
| Add-ons | **Registration → Tickets → Add-ons** |
| Coupons | **Registration → Tickets → Coupons** |
| Ticket details page | **Registration → Tickets → Ticket details page** |
| Registration form (question × group grid) | **Registration → Form** |
| Payment providers, invoice content, offline payments | **Registration → Finance → Payment providers** |
| Tax rules | **Registration → Finance → Tax** |
| Go live, preview, share link | **Registration → Publish** |
| Attendees, transactions, receipts, invoices | **Registration → Registrations table** |

The public flow is at `/register/event/<eventId>`, two steps: **Select tickets**,
then **Add-ons and attendee details**.

## What it is not

- It is **not** the same builder as submissions. The registration form has ten
  question types and a completely different set — no date picker, no number field.
- Groups are **not** cosmetic. See above.
- **Preview is not a sandbox.** See above.
