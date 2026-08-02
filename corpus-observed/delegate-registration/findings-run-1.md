---
feature: delegate-registration
observed: true
app_version: unknown (module URL is delegate-registration-v3)
explored: 2026-08-01
plan: professional conference
---

# Registration — findings, run 1 (partial)

Covered this run: ticket creation, the publish/preview page, the attendee purchase
path end to end, the order confirmation screen, the registrations table
(attendees and transactions), the attendee detail panel, the registration form
builder, add-ons, coupons, payment providers, invoice configuration, delayed
payments, and tax.

**Not yet covered:** ticket group creation, the ticket details page, billing,
admin amendments to existing orders, refunds, and analytics.

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
| 14 | Group creation is a **right-hand pop-up** | `[untested]`. Ticket, add-on and coupon panels are all right-hand slide-overs, so `[inferred]` groups are too. |
| 15 | Hidden tickets let admins buy on behalf of a user | **Partly confirmed.** The control is a toggle **"Hide ticket (visible to admins only)"**. The attendee preview carries a **"Show hidden tickets"** control and an **"Admin mode"** toggle. Buying-on-behalf not yet walked. |
| 16 | Coupons via **Registration → Tickets → Coupon tab** | **Confirmed.** Tab is "Coupons", and there is also a left-nav item. |
| 17 | **"Create Coupon"** button, right-hand pop-up | **Confirmed** — "Create coupon", right-hand panel. |
| 18 | Fields: Coupon Name, **Discount amount (percentage)**, Quantity Available, date range | **Changed.** The field is **"Coupon code"**, not name. Discount is **not percentage-only**: a **"Discount type"** dropdown offers **"Percentage (%)"** and **"Amount ($)"**. An undocumented **"Deactivate coupon"** toggle also exists. |
| 19 | Limited to tickets/add-ons via **"Add Tickets" / "Add Addons"** | **Partly changed.** Controls are **"Available with selected tickets"** and **"Add addons"**. |
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

## The 193-ticket theme: there are four routes to a receipt, and the article has two

`downloading-invoices-and-receipts.md` (228 words) documents only the two
**attendee** routes: the confirmation screen after payment, and the attendee's own
dashboard later. Observed in the app, there are two more, both **admin** routes,
and both undocumented:

**Registration → Registrations table → click the attendee row.** A right-hand
**"Attendee details"** panel opens showing Status, Order reference, *Order created
by*, Created date, a Ticket details block with **"Total paid"**, then two
dropdowns:

| Control | Options |
|---|---|
| **"Order downloads"** | **"Receipt - 2"**, **"Invoice - 1"** |
| **"Email"** | **"Receipt - 2"**, **"Invoice - 1"** |

So an admin can **download** a receipt or invoice for any attendee, **or email it
to them**, without the attendee doing anything.

Given the volume — 193 tickets, the single largest theme in the 4,898-ticket
analysis — the likeliest reading is that most of those are organisers asking *how
do I get my attendee their invoice*, and the article answers a different question:
how the attendee gets it themselves. `[inferred]` from the volume and the shape of
the gap, not from reading the tickets.

The panel also has an **Email** field with a swap/change icon beside it, which is
presumably the route for "Changing the email address on a registration" (237-word
article). `[untested]`.

## Transactions tab

**Registration → Registrations table → Transactions.**

- Summary cards: **Gross Total**, **Net Total**, **Refunds**, each £0.00
- Columns: PROCESSED AT / TRANSACTION ID / ORDER NO. / **ORDER OWNER** /
  TRANSACTION TYPE / **REFUND METHOD** / GROSS TOTAL / NET TOTAL / TAX TOTAL
- An **Export** dropdown

Two things worth documenting:

- **A £0 order still writes a transaction**, typed **"Payment"**, with a full
  transaction ID. Free tickets are not invisible to finance.
- **ORDER OWNER is the buyer**, while the Attendees tab is keyed on the **ticket
  holder**. The same order appears under two different names depending on which
  tab you are looking at. For anyone reconciling a list of attendees against a
  list of payments, that is a trap, and no article mentions it.

## The registration form is a grid, not a form

**Registration → Form.** This is not a linear question list like the submission
form builder. It is a **matrix: questions down the side, ticket groups across the
top**, with a toggle in every cell. A question is switched on or off *per ticket
group*.

That is the mechanism behind the ticket panel's helper text about groups
controlling "which add-ons and questions are shown to attendees". Two features
that read as unrelated in the documentation are the same feature.

- **Name** and **Email** are present by default, both marked **Required**, both
  carrying a **padlock** icon — they cannot be removed.
- The **"Visible to the public"** and **"Allow attendee to edit responses"**
  toggles appear here *as well as* on the Publish page. Same switches, two
  locations.
- Question types, from **"Add question" → "Select the question type you want to
  add:"**

  | Group | Types |
  |---|---|
  | **STANDARD** | Dropdown, Checkbox, Radio, File Upload |
  | **CONTACT DETAILS** | Phone number, Email, Address |
  | **TEXT** | Short text, Long text, Text block (read only) |

  Ten types, and **a completely different set from the submission form builder** —
  no date picker, no number field, no multi-response dropdown. An organiser who
  knows one builder will look for options that are not there.

## Add-ons

Empty state: **"No add-ons created yet"** / "Sell additional add-ons for your
event. E.g. galas, dinners, workshops or networking events." / **"Create add-on"**.

Panel fields: **Add-on name*** (e.g. Gala dinner), **Add-on description**,
**Price** (0, GBP, "This is a free add-on"), **Quantity available**,
**Quantity per person**, **Available from / Available to**, **Available with
selected tickets** (default "All tickets"), **Hide add-on** toggle, **Create
add-on**.

- Add-ons can be scoped **directly to chosen tickets**, independently of ticket
  groups. So there are two overlapping mechanisms for controlling what an attendee
  sees, and no article explains how they interact. `[untested]` what happens when
  they disagree.
- **Inconsistent helper text between two panels in the same module**: the ticket
  panel says *"Change currency here."*, the add-on panel says *"Change currency in
  the finance tab"*.

## Coupons — the article is wrong about the main thing

Empty state: **"No coupons created yet"** / "Add coupons to provide discounts to
your attendees. Choose amount or percentage price reductions." / **"Create
coupon"**.

| Field | Observed |
|---|---|
| **Coupon code*** | placeholder `E.G. SPEAKER50` — the article calls this "Coupon Name" |
| **Discount amount*** | e.g. 50, with a `%` suffix that follows the type |
| **Discount type*** | dropdown: **"Percentage (%)"** (default) and **"Amount ($)"** |
| **Quantity available** | e.g. 500 |
| **Available from / Available to** | date range |
| **Deactivate coupon** | toggle — undocumented |
| **Available with selected tickets** | default "All tickets" |
| **Add addons** | default "All addons" |

**Coupons can be a fixed amount, not only a percentage.** The article describes
only "Discount amount (percentage)". The empty state on screen even says "Choose
amount or percentage price reductions" — so the product says it and the
documentation does not.

Also: the option reads **"Amount ($)"** with a **dollar sign**, on an event whose
currency is **GBP** and whose price fields show GBP. A small localisation bug, but
a confusing one on a screen about money.

## Finance: payment providers

**Registration → Finance → Payment providers.** Tabs: **Billing / Payment
providers / Tax**.

> Select your payment provider
> Set up your payment provider in order to publish paid tickets. Read about
> Oxford Abstracts' **fees and collection policy**.

**Paid tickets cannot be published without a provider** — a gating rule stated
plainly on screen and in none of the articles.

| Provider | State | Notes |
|---|---|---|
| **Stripe** | NOT CONNECTED | "Enable payments to be collected by debit/credit card via Stripe." Button: **"Link to Stripe"** |
| **PayPal** | NOT CONNECTED | "Enable payments collected through PayPal." Button: **"Configure"** |
| **Authorize.net** | NOT CONNECTED | In red: **"Authorize.net payments require the event currency to be USD."** |
| **Invoice payments** | NOT CONNECTED | "Generate an invoice and allow attendees to pay offline. **Requires a fee collection card.**" Button **"Enable"**, greyed out |

Plus a highlighted panel: *"Add a fee payment method — To set up authorize.net or
invoice payments we require a payment card to collect our service fees through."*

The Authorize.net currency constraint is exactly the kind of hard, specific fact
that generates a ticket and is answerable in one line. Nothing documents it.

## The word "invoice" means two different things, and that may explain the 193

There are **two unrelated features** both called invoice:

1. **Invoice/receipt documents** — the PDFs an attendee or admin downloads after
   an order. Covered by `downloading-invoices-and-receipts` and
   `configuring-invoices-and-receipts-for-delegate-registration`.
2. **Invoice payments** — a *payment method* where the attendee asks for an
   invoice and pays offline by bank transfer. Covered by **nothing**.

`[inferred]` — the 193 tickets tagged "invoices & receipts" are very likely a
mixture of *"how does my attendee get their receipt"*, *"how do I let my
university pay by invoice"*, and *"how do I get our PO/VAT number onto the
invoice"*. Three different questions collapsed under one word, answered by
articles that only address the first. Worth checking against the raw tickets
before acting — but it would explain why the largest theme in the analysis sits
behind the shortest article.

## Invoice configuration — where the answers actually live

**Payment providers → "Configure invoice and receipts"** (top right) opens a
right-hand panel with two tabs, **Details** and **Delayed payments**.

> Configure the branding and content of your invoices and receipts. Registration
> form questions marked as 'show on invoice' will also appear.

**Details tab:**

- **Invoice title*** — default "Conference invoice"
- **"Include the following event details on the invoice"** — Venue ✓, Email,
  Telephone, Start date, End date, Event logo (with an "Add here" link)
- **"Include the following customer details on the invoice"** — Order reference ✓,
  Registration date, **Buyer email**
- **"Question responses displayed"** — *"Attendee responses to questions can be
  included on invoices and receipts by toggling the 'show on invoice' option
  during question setup."* with a **"Go to form builder"** link
- **Header design** — a rich text editor
- Buttons: **"Save details"**, **"Generate preview"**

Two things worth pulling out:

- **A "show on invoice" toggle exists on registration form questions.** It was not
  visible in the question-type picker, so it must sit inside individual question
  setup. `[untested]`. This is the mechanism for getting arbitrary data onto an
  invoice.
- **"Generate preview"** lets an organiser see the invoice **without needing an
  order**. That is the single most useful thing for anyone setting this up, and no
  article mentions it.
- Note again the buyer/holder split: the customer detail available is **"Buyer
  email"**.

**Delayed payments tab:**

> Delayed payments include offline payments and payment links. Configure custom
> questions for both and payment details for offline payments.

- **"Offline payments is not currently configured."** *(sic — "is")*
- *"Offline payments allows people to complete their purchase by requesting an
  invoice and then transferring the amount to you, e.g. via bank transfer."*
- *"To activate offline payment you must first add a fee collection card. This is
  so we can collect Oxford Abstracts fees on offline invoices."*
- **"Custom questions for delayed payments"** — *"Ask questions to users paying
  with delayed payments. These questions and responses will appear on the invoice.
  E.g. tax number, or company address."*

**This answers a classic conference question — "our finance department needs a PO
number and VAT number on the invoice" — and it is documented nowhere.**
**"Payment links"** is also named here and appears in no article at all.

## Tax

**Registration → Finance → Tax.** Empty state: **"No tax rules added yet"** /
"Add a tax rules to apply to all or some tickets. Add multiple rules to handle
multiple scenarios." *(sic — "a tax rules")* / **"Create tax rule"**.

Confirms claim 7 from the other direction: tax is no longer an "Add tax" link on a
ticket but a **rules system**, supporting **multiple rules scoped to all or some
tickets**. That is more capable than the article describes, and the article
describes it in the wrong place.

## Refunds and amendments — the articles' central buttons are not there

Both articles hinge on a control that does not appear on this event.

| Article | Claimed path | Observed |
|---|---|---|
| `how-admins-can-amend-existing-delegate-registration-orders` (29 tickets) | **Registration → Registrations**, then **"Edit Order"** | Nav item is **"Registrations table"**. Clicking a row opens an **"Attendee details"** panel with **no "Edit Order" button**. |
| `refunding-an-attendee-through-delegate-registration` (32 tickets) | **Registration → Registrations**, then **"Edit & Refund Order"** | **No "Edit & Refund Order" button** anywhere. |

Searched the rendered page for `Edit Order`, `Edit order`, `Edit & Refund`,
`Amend` and `Cancel order`: **all absent**. The only match for "Refund" is the
**"Refunds £0.00"** summary card on the Transactions tab, which is a figure, not
an action.

The attendee panel offers only: **Order downloads**, **Email**, and an editable
**Email** field with a swap icon. The transaction panel offers only **Close**.

**I cannot tell which of two explanations is right, and this matters:**

1. The buttons were removed or renamed in `delegate-registration-v3`, in which
   case both articles are broken for everyone; or
2. They appear only on an order that has **money to refund** and a **connected
   payment provider** — neither of which this £0 order on an unconfigured event
   has.

Explanation 2 is at least as likely, and I have no way to separate them without a
paid order on an event with Stripe or PayPal connected. **Do not rewrite either
article on the strength of this** — settle it first. It is a five-minute check on
any real event that has taken a payment.

`[untested]` as a result: the whole refund flow, refund states ("Pending Refund"
is named in the article), and whether refunding cancels the attendee's place as
the article claims.

## Two smaller finds on the transaction panel

- **A £0 order is recorded as "Payment method: Offline"** — on an event where the
  Delayed payments tab states in an amber panel that *"Offline payments is not
  currently configured."* The product is labelling free orders with a payment
  method it also says is switched off.
- **The same timestamp is shown in two timezones on one screen.** The transactions
  table reads **"01 Aug 2026, 15:49 BST"**; the detail panel for that same
  transaction reads **"Created: 01 Aug 2026, 14:49"** — the UTC value, unlabelled.
  Anyone reconciling against a bank statement or a payment provider's dashboard
  will meet a one-hour discrepancy with no explanation on screen.

## Cosmetic defects

- Tax empty state reads **"Add a tax rules"**; delayed payments reads **"Offline
  payments is not currently configured."**
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
