---
feature: delegate-registration
observed: true
app_version: unknown (module URL is delegate-registration-v3)
explored: 2026-08-01
plan: professional conference
---

# Registration — findings, run 1 (partial)

Covered this run: ticket creation, the publish/preview page, the attendee purchase
path end to end, the order confirmation screen, and the registrations table.

**Not yet covered:** the registration form builder, add-ons, coupons, groups,
Finance (billing / payment providers / tax), the ticket details page, admin
amendments to existing orders, refunds, and analytics.

---

## The headline: "Preview" creates real registrations

**Observed.** From **Registration → Publish → Preview**, the attendee flow opens at
`/register/event/78206?preview=true`. Walking that flow to "Complete order"
produced a **real, persisted registration**:

- order number **#AD47C**, confirmation at
  `/register/event/78206/confirmation/<uuid>` — note the `preview=true` parameter
  is **gone** from the confirmation URL
- the attendee appears in **Registration → Registrations table** as a live row,
  counter reading **"Paid 1"**
- a **real confirmation email was sent**, to the buyer's real address

Registration was **not** published at the time — "Visible to the public" was off.

So an organiser who clicks Preview to check their setup, and walks it through to
the end, creates genuine attendee records and sends genuine email. Nothing on the
screen warns of this, and the word "Preview" implies the opposite.

`[inferred]` — this is probably why some events show test registrations the
organiser cannot account for. Not confirmed against ticket data.

## A £0 ticket is recorded as "Paid"

**Observed.** The free ticket order shows a green **"Paid"** pill in the PAYMENT
column of the registrations table, and the counter above it is labelled **"Paid"**.
No money moved and no payment provider is configured on this event.

Defensible internally, but an organiser reconciling numbers will read "Paid" as
"money received".

## The confirmation email goes to the buyer, not the ticket holder

**Observed.** Banner text, verbatim:

> ORDER CONFIRMED AND EMAIL SENT TO GARETH@OXFORDABSTRACTS.COM

The ticket holder was `test.attendee.one@example.com`; the buyer was the signed-in
admin. The confirmation went to the **buyer only**. The confirmation screen shows
this relationship clearly —

> Test Attendee One | test.attendee.one@example.com
> Bought by gareth@oxfordabstracts.com

— but the person who now holds a ticket has had no email at this point.
`[untested]` whether the ticket holder is emailed separately or at all.

This is directly relevant to **"Completing registration when someone bought your
ticket"** (135 words) and to the 29 tickets about editing registrations.

---

## Verification list — reconciled so far

| # | Claim | Status |
|---|---|---|
| 1 | Path is **Registration → Tickets → Create Tickets** | **Changed.** Nav is **Registration → Tickets**, which expands to **Conference tickets / Add-ons / Coupons / Ticket details page**. There is no "Create Tickets" nav item. |
| 2 | Ticket dashboard has **Tickets, Add-Ons and Coupons** at the top | **Confirmed**, wording corrected to **"Add-ons"**. Note they are now *both* top tabs and separate left-nav items. |
| 3 | "Create Ticket" is a **blue button in the middle of the screen** | **Changed.** Label is **"Create ticket"** (sentence case) and it is **navy**, not blue. Mid-page only in the empty state; once a ticket exists it moves to **top left** beside "Create group". |
| 4 | Ticket has a name and description | **Confirmed** — "Ticket name*" (placeholder "e.g. All access") and "Ticket description" (rich text, placeholder "Something about your ticket"). |
| 5 | Currency changed via the blue **"Finance"** word **above** the price box | **Changed.** It is a link reading **"Change currency here."** in a helper line **below** the price box: "This is a free ticket. Change currency here." |
| 6 | Price defaults to **0.00 (free)** | **Confirmed** — field shows `0`, helper text says "This is a free ticket." |
| 7 | **"Add tax"** sits below the price box | **Changed — not present.** No tax control in the ticket panel at all. Tax is now its own page under **Registration → Finance → Tax**. |
| 8 | **"Quantity Available"** box | **Confirmed**, label is "Quantity available" (placeholder "e.g. 500"). |
| 9 | Dates tickets are available | **Confirmed** — "Available from" / "Available to", `dd/mm/yyyy`. |
| 10 | Ticket group selector | **Confirmed** — "Ticket group", default **"Ungrouped"**. |
| 11 | Button at bottom is **"Create Ticket"** | **Confirmed** — "Create ticket". |
| 12 | Edit/delete via **three dots at the end of the row** | **Confirmed** (⋮ at row end). |
| 13 | **"Create Group"** mid-page with no tickets, **top right** with tickets | **Partly changed.** Mid-page in the empty state: confirmed. Once tickets exist it is **top left**, not top right. |
| 14 | Group creation is a **right-hand pop-up** | `[untested]` this run. |
| 15 | Hidden tickets let admins buy on behalf of a user | **Partly confirmed.** The control is a toggle **"Hide ticket (visible to admins only)"**. The attendee preview carries a **"Show hidden tickets"** control and an **"Admin mode"** toggle. Buying-on-behalf not yet walked. |
| 16 | Coupons via **Registration → Tickets → Coupon tab** | **Confirmed** the tab exists ("Coupons"); creation flow `[untested]`. |
| 17–19 | Coupon fields | `[untested]` this run. |
| 20 | Post-payment **Order Details Confirmation** shows a **"Download Receipt"** dropdown top right | **Confirmed**, wording corrected to **"Download receipt"**. Heading on the page is **"Order details"**. |
| 21 | Dropdown offers **receipt and invoice** | **Confirmed.** Exact options: **"Receipt - 2"** and **"Invoice - 1"** — each numbered. `[inferred]` these are document sequence numbers. |
| 22 | Attendee later signs in, finds the event box, clicks **"View Details"** | `[untested]` — needs an attendee account. The confirmation page does offer **"Return to dashboard"**. |

## Undocumented things found

- **"Maximum number of tickets per order"** field on every ticket (placeholder
  "e.g. 1"). **This answers three support tickets about restricting purchases**,
  and no article mentions it.
- **Ticket groups are functional, not cosmetic.** Helper text, verbatim: *"Use
  ticket groups to control which add-ons and questions are shown to attendees
  based on their ticket. Configurable anytime."* The empty state adds *"Groups
  will be used to assign forms."* The article describes groups only as a way to
  categorise in-person vs virtual.
- **A "Tips before you publish" checklist** on the Publish page, with a green tick
  against completed items: *Add tickets* ✓, *Setup payment provider*, *Add tax
  (optional)*, *Customise form (optional)*, *Preview event*.
- **Publishing is a toggle, not a button** — **"Visible to the public"**, beside a
  second toggle **"Allow attendee to edit responses"**, and a copyable **Link**.
- The registrations table has **Attendees** and **Transactions** tabs, columns
  NAME / PAYMENT / TYPE / ORDER REF. / REGISTERED / FORM / TICKETS / ADD-ONS /
  ROLES / COUPON / GROUP, plus search, date filter, Columns picker, and delete /
  email / settings / download actions.

## Error and empty states captured verbatim

The 19 articles in this section quote **none** of these.

| Trigger | Message |
|---|---|
| No tickets or groups yet | **"No tickets or groups added yet"** / "Create tickets for your event and add them to groups." / "Groups will be used to assign forms. e.g. In-person, remote, hybrid" |
| Empty cart, attendee side | **"Cart empty"**, with "Continue" greyed out |
| Clearing a required email on the attendee form | **"Email required"**, shown live in red under the field; "Complete order" greys out |
| Attendee needs help | "Not sure what you need? **Contact your event administrator**" |

## Cosmetic defects

- Registrations table reads **"1 rows"** (not pluralised) — same class of bug as
  the poster gallery's "Showing 1 results".
- Guessing `/delegate-registration-v3/registrations` gives a bare **"Page not
  found."** with no navigation back; the real path is `/attendees`.

## Housekeeping

Left on the event: ticket **"Test Ticket One - Free"** (quantity 50, max 2 per
order) and one registration, **Test Attendee One / order AD47C**. Both are
synthetic and both are deletable — the registrations table has a delete action.
Say the word and they go.

A real confirmation email was sent to Gareth's own address as a side effect of the
preview walk.
