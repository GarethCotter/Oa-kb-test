---
feature: delegate-registration
observed: true
app_version: unknown (module URL is delegate-registration-v3)
explored: 2026-08-01
plan: professional conference
---

# Delegate registration — by plan

**This file settles nothing.** Only one demo event was available (78206,
Professional Conference), so nothing about other packages was observed. It records
what Professional shows.

Every article in this section carries `plan: all plans (including free Basic)`.
**This run cannot verify that**, in either direction.

| Capability | Professional Conference | Abstract Management | Basic (free) |
|---|---|---|---|
| REGISTRATION section in the left nav | **Present** | `[untested]` | `[untested]` |
| Tickets, groups, add-ons, coupons | **Present** | `[untested]` | `[untested]` |
| Registration form (question × group grid) | **Present** | `[untested]` | `[untested]` |
| Payment providers (Stripe, PayPal, Authorize.net, Invoice payments) | **All four offered** | `[untested]` | `[untested]` |
| Delayed payments / offline payments | **Present** | `[untested]` | `[untested]` |
| Tax rules | **Present** | `[untested]` | `[untested]` |
| Registrations table, transactions | **Present** | `[untested]` | `[untested]` |
| Invoice/receipt documents | **Present** | `[untested]` | `[untested]` |

## The one plan-adjacent fact actually observed

A **2.5% fee applies to paid tickets** — shown on the dashboard Registration card,
not tied to package. And the payment providers page links to *"fees and collection
policy"*. `[untested]` whether that percentage varies by plan.

Note also that **paid tickets require a connected payment provider before they can
be published**, which is a functional gate rather than a plan gate, but will look
like one to an organiser on a plan that lacks something.

## How to close this out

Get one event on Basic and one on Abstract Management, then check in order:

1. Is there a **REGISTRATION** section in the nav at all?
2. If so, can tickets be created, and can a **paid** ticket be created?
3. Are all four payment providers offered, or a subset?
4. Are delayed payments and tax rules present?
5. If anything is missing, is it absent, greyed out, or does it show an upgrade
   prompt? **The wording of the block matters more than its existence** — it is
   what a blocked organiser will search for.

`project/plan-feature-matrix.md` is what has to agree with the answer, and the
`plan:` frontmatter on all 19 articles depends on it.
