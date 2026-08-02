---
feature: delegate-registration
observed: true
app_version: unknown (module URL is delegate-registration-v3)
explored: 2026-08-01
plan: professional conference
---

# Delegate registration — where a first-timer gets stuck

The reader in `CLAUDE.md`: a conference organiser, often middle-aged, not
especially confident with software, arriving mid-task and mildly stressed. Ordered
by likely support volume.

Where **I** hesitated is recorded, since the brief's test is that if the exploring
agent had to hunt, the persona is lost.

---

## 1. "Preview" is not a preview

An organiser wants to check their setup before going live. They click **Preview**
— the safe-sounding button, on a page headed *"Make sure you are happy with the
set up of your form and ticket configuration."* They walk it through to see what
attendees experience.

They have just created a **real attendee, a real order and a real confirmation
email** on an unpublished event.

Nothing warns them. The `preview=true` parameter silently disappears at the
confirmation step. This is the worst kind of trap: correct instinct, safe-sounding
control, irreversible side effect.

Then they see a stranger's name in their attendee list — their own test — and
cannot account for it.

## 2. The invoice question has three different answers and one article

Say "invoice" to three organisers and you get three questions:

1. *"How does my attendee get their receipt?"* → the article answers this
2. *"How do I let a university pay us by bank transfer?"* → **Delayed payments**,
   undocumented
3. *"Finance need our PO and VAT number on the invoice"* → **Custom questions for
   delayed payments**, undocumented

193 tickets a year carry the word. The article addresses one of the three.

## 3. The organiser cannot find how to send an attendee their receipt

The article explains how the *attendee* gets it — from their confirmation screen,
or by signing in later. But the person asking is usually the organiser, whose
attendee has emailed *them*.

The answer exists and is two clicks away: **Registrations table → click the row →
"Email" → Receipt**. It is in no article. An organiser who reads the current page
comes away believing they must talk their attendee through signing in.

## 4. Two tabs, two names, one order

An organiser reconciles their attendee list against their payments. Attendees is
keyed on the **ticket holder**; Transactions on the **ORDER OWNER**, the buyer.
Where someone bought tickets for colleagues, the two lists do not match and
nothing on either screen explains why.

## 5. A free ticket says "Paid"

£0 ticket, no payment provider connected, no money moved anywhere. The attendee
row shows a green **"Paid"** pill and the counter above the table is labelled
**"Paid"**.

An organiser running a free event, or reconciling a mixed one, reads that as money
received. The transaction record compounds it: **"Payment method: Offline"** — on
an event where the product itself says offline payments are not configured.

## 6. The person holding the ticket never got an email

The confirmation goes to the **buyer**. Where someone booked for colleagues, those
colleagues have had nothing. The organiser hears "my delegates say they never got
anything", and there is a 135-word article about it that does not explain the
mechanism.

## 7. The tax setting has moved and the article points at where it was

An organiser follows the article to add tax: it says a **"Add tax"** link sits
below the price box on the ticket. There is no such link. Tax is now a **rules
system** at **Registration → Finance → Tax**.

They conclude tax is not supported, or that they are on the wrong screen.

## 8. Coupons look percentage-only

The article documents "Discount amount (percentage)". An organiser wanting to give
a flat £20 off concludes it cannot be done.

It can — **"Discount type"** offers **Amount** as well as **Percentage**. The
product's own empty state says so; the documentation does not.

## 9. Ticket groups look optional and cosmetic

The article presents groups as a way to categorise in-person versus virtual. So
organisers skip them.

Groups are how you control **which questions and which add-ons each attendee
sees**. Skipping them means every attendee sees every question. The organiser
discovers this when delegates complain about irrelevant questions, and by then
orders exist.

## 10. Paid tickets silently cannot be published

An organiser sets up paid tickets and cannot work out why registration will not go
live. The requirement is stated once, on a different page: *"Set up your payment
provider in order to publish paid tickets."*

**Two more hard prerequisites** are stated only on that page: Authorize.net
requires the **event currency to be USD**, and invoice payments require a **fee
collection card**. Each is exactly the sort of specific blocker that produces a
ticket.

## 11. The refund and amendment articles name a button that is not on screen

Both hinge on **"Edit Order"** / **"Edit & Refund Order"** at
**Registration → Registrations**. The nav item is **"Registrations table"**, and
clicking a row opens a panel with neither button.

**Caveat, and it matters:** this may be because the test order is £0 on an event
with no payment provider. Unverified — see `findings-run-1.md`. But if it holds on
real events, 61 tickets a year are hitting two articles whose central instruction
cannot be followed.

## 12. Small things that cost confidence

- The **same timestamp in two timezones on one screen** — table says 15:49 BST,
  the detail panel for that transaction says 14:49. Anyone checking against a bank
  statement meets an unexplained hour.
- **Two different phrasings for the same action** inside one module: the ticket
  panel says *"Change currency here."*, the add-on panel says *"Change currency in
  the finance tab"*.
- **"Amount ($)"** offered as a discount type on a **GBP** event.
- Grammar: *"1 rows"*, *"Add a tax rules"*, *"Offline payments is not currently
  configured."* Individually trivial; collectively they undermine trust on screens
  about money.
