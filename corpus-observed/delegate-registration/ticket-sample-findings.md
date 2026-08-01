---
feature: delegate-registration
observed: true
explored: 2026-08-01
plan: n/a — ticket analysis
---

# What the invoice tickets actually say

Read 1 August 2026 against `oa-support-replies/year-tickets.json` (4,898 tickets,
outside the repo, real names — **nothing customer-specific is reproduced here**).

## Method, and its limits

354 of 4,898 tickets mention "invoice" or "receipt". I first tried to classify
them by regex and got two mutually contradictory answers — one pass said 145
tickets were about Oxford Abstracts' own billing, another said 50, and 63% went
unclassified. **Those numbers were noise and are not reported.**

What follows is from **reading a random sample of 30** (seed fixed, so it is
reproducible). That is enough to establish which themes exist and roughly how
common they are. It is **not** a census, and the proportions below should be
treated as "roughly a quarter", not as percentages.

## The correction to my earlier inference

`article-gaps.md` originally claimed the 193-ticket invoice theme was mostly
organisers asking *"how do I get my attendee their invoice"*. **That was wrong,
and it was the load-bearing assumption on the gap list.** The sample shows four
distinct themes, and document-retrieval is not the largest.

## What the themes actually are

**1. Changing what is *on* an invoice, after it has been issued** — roughly a
quarter of the sample, and the largest delegate-registration theme.

Requests observed: correct an attendee's name on an issued invoice; add a company
name; add a PO number; add a billing address; amend an invoice note; correct a
conference year in the note text. Several say explicitly that they do not believe
they can do it themselves and are asking support to do it for them.

**This is not documented anywhere**, and the product surface for it — the invoice
configuration panel, "custom questions for delayed payments", and the "show on
invoice" per-question toggle — is exactly what run 1 found undocumented. The
match between the gap and the demand is very close.

**2. Oxford Abstracts' own billing to the organiser** — also roughly a quarter,
and **a different topic entirely** from delegate registration.

Payment extensions on the event package; "our invoice is overdue but we paid by
bank transfer"; requests for an invoice for the conference package with specific
bank details; account-expiry-while-arranging-payment; VAT and remittance details.

These have nothing to do with the registration module. `creating-and-paying-for-a-new-event`
is the nearest article. **This theme is invisible in the current section structure**
because it sits under the same word as delegate invoices.

**3. Paying *by* invoice rather than card** — present and real, smaller than the
above two.

Including one organiser asking whether an invoice can be generated **ad hoc**, for
individual delegates who ask, rather than offering the option to everyone. Another
reported that when the attendee chose payment by invoice, **no IBAN or bank
details were shown**, so they could not pay.

Confirms the `delayed payments` gap from run 1, and adds a specific question the
article should answer: can it be offered selectively?

**4. Retrieving the document, often because something is broken** — present,
smaller than expected.

Reports of "File not found" when following a receipt link, an error page when
viewing receipt and invoice, and an attendee unable to access an invoice after
changing their email address. These are **fault reports, not how-to questions** —
an article would not have deflected them.

## One ticket independently confirms a run-1 finding

An organiser reported that they can capture the buyer's address via the
registration form **when the buyer is also the ticket holder**, but that the
address does not carry through **when someone buys a ticket for another person**.

That is precisely the buyer-versus-ticket-holder split identified in
`overview.md`, arrived at independently from the app. A real customer hit it and
had to escalate. It is the strongest single piece of evidence on this list.

## What this changes

| Was going to say | Should say |
|---|---|
| The 193 are mostly "how does my attendee get their receipt" | They are at least four different questions; retrieval is one of the smaller ones |
| Priority 1 is rewriting the retrieval article to add the admin routes | Still worth doing, but **smaller** than editing invoice *content*, which is the biggest delegate theme and wholly undocumented |
| — | **A large share are not about registration at all** — they are about the organiser's own bill from Oxford Abstracts, and belong in a different section |
| Delayed payments is a gap | Confirmed, and it needs to answer "can I offer it to only some people?" and "why did no bank details appear?" |

## What would settle it properly

A hand-labelled pass over all 354, or at least a stratified sample of ~100, with
the four themes above as the labels. That converts "roughly a quarter" into real
figures and would rank the writing queue properly. Perhaps two hours.

The regex shortcut does not work here, for a reason worth remembering: the word
"invoice" appears in all four themes with almost identical surrounding language,
so keyword patterns cannot separate a customer asking for their event package
invoice from an attendee asking for their ticket receipt. **Only reading does.**
