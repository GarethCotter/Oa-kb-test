---
title: "Authorize.net payments that are pending or held do not appear in the registrations table"
internal: true
last_reviewed: 2026-07-31
---

Authorize.net transaction not showing, payment pending in Authorize, charge held for
review, registration missing after payment, transaction in Authorize but not in Oxford
Abstracts, cannot find the registration to apply a payment to.

**Why it happens.** Authorize.net payments are handled differently from invoices and
payment links. Until Authorize confirms the payment, the registration is in the
database but does not appear in the registrations table, so there is nothing on screen
to match the transaction against. A charge held for review by Authorize does the same
thing.

**The workaround support uses:**

1. Create the registration for the person using the **offline invoice** option.
2. Once the money clears in your Authorize account, mark that registration as **Paid**.
3. The registrant gets an email and completes the form as normal.

If the transaction stays stuck rather than merely pending, that is one for support to
pass to the development team — it has happened, and it is not something the organiser
can resolve from the dashboard.
