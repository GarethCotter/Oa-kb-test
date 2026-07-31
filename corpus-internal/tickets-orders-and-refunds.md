---
title: "Tickets not showing, group bookings, refunds and what registration cannot do"
internal: true
last_reviewed: 2026-07-31
---

Tickets not visible, ticket not showing on the registration page, group booking,
buy tickets for colleagues, refund an attendee, partial refund, bulk import
registrations, check in delegates, reassign a ticket, guest checkout.

Distilled from around 25 support tickets in the year to July 2026.

**Tickets invisible to everyone but you** is nearly always the dates. A ticket is
automatically hidden from non-admins outside its start and end dates, so a start date
in the future — or a past year left on a copied ticket — hides it completely. To test,
switch on the **Admin mode** toggle at the top right of the registration page, or move
the visibility start date into the past. A ticket set "to 1 April" stays on sale until
23:59 that day.

**Group bookings:** selecting more than one ticket reveals name and email fields for
each person. There is a limit of **10 tickets per order**, and every ticket needs a
name and email at purchase — placeholders are fine, and an admin can reassign each
ticket afterwards with the reassign button. Everyone on one order shares a single
order reference, which cannot be split.

**Refunds** return the ticket price **excluding the Oxford Abstracts service fee and
excluding transaction fees**, so the organiser absorbs the service fee on anything
refunded. A partial refund is only possible where an order holds several tickets or
add-ons and one is removed. Payments run through the organiser's own provider, so
Stripe refunds may need doing in Stripe, and the transactions table links straight to
the matching payment there.

**Coupons** are covered in their own note, but two extra points: a coupon must be
applied to *every* ticket type it should cover, or registrants see "code not valid for
selected items"; and a coupon cannot be added once an order is paid — the only route
is refund and rebook.

**Things registration cannot do:**

- **No bulk import of registrants.** Entries are made by hand, or delegates complete
  their own details from their dashboard.
- **No check-in function** at the event.
- **No guest checkout.** Only the ticket details page is public; anyone clicking Get
  Tickets must register or log in first.
- **Tickets cannot be shown to some people and hidden from others.** They are fully
  visible, visible for a period, or admin-only. For a held-back allocation, an admin
  registers people directly.
- **Discount rules** (bulk, package-based percentages) do not exist. Coupons are the
  only mechanism.

**A very small test fee fails** at the payment provider with a 500 error — use at
least 0.50 in the chosen currency.
