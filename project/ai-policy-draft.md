# How Oxford Abstracts uses AI

*Last reviewed 11 August 2026*

## Where we use it

In one place: our help centre. When you ask a question in the help centre, the in-app
help widget, or our support form, we send that question to an AI model, which writes a
plain-English answer from our own published help articles.

## What it cannot reach

**AI is not used anywhere in the conference software itself.** It does not read, score,
summarise or make any decision about abstracts, reviews, grades, reviewer comments,
decisions, delegate data, programmes or the emails you send through the system.

No submission is ever assessed by AI, and no decision about a submission is ever
influenced by it. This is how the system is built rather than a promise about how we use
it: the answer feature reads a fixed file of help articles and has no connection to the
conference database at all.

## What we send

Two things: the text you typed, and our own help articles — the same public pages anyone
can read. Nothing from your event is sent.

Where you are asking through our support form, the text you typed is the subject and
description of the ticket you were about to send. That is usually longer than a search
box and may contain more detail, so please include only what is needed to describe the
problem.

## Who provides the model

**Anthropic**, using Claude Haiku, acting as a sub-processor for this feature. For
customers in the UK and EEA, the contracting entity is Anthropic Ireland Limited.

- **Your content is not used to train AI models.** This is the baseline position of
  Anthropic's Commercial Terms for API use, not a setting we have chosen — the opt-in
  training controls reported in the press apply to consumer Claude.ai accounts, not to
  API access of the kind we use.
- **Inputs and outputs are deleted within 30 days**, with narrow exceptions for legal
  obligations and usage-policy enforcement.
- **Zero Data Retention** is available from Anthropic by agreement for organisations with
  a contractual requirement for it. Talk to us if this applies to you.
- Anthropic publishes a [Data Processing Addendum](https://www.anthropic.com/legal/data-processing-addendum),
  and its SOC 2 and compliance documentation is at [trust.anthropic.com](https://trust.anthropic.com).

## What we keep

We log the questions asked so we can see which of our documentation is not working and
improve it. Email addresses and telephone numbers are automatically removed before
storage. `[RETENTION PERIOD]`

Please do not include personal data or confidential event details in a help question —
we do not need them to answer it.

## If you would rather not use it

You never have to. Every answer comes from our published help articles, and you can read
them directly: browse the help centre by section and open the article yourself, exactly
as you would any documentation site. The AI layer only saves you the step of finding it.

If the feature is unavailable, search falls back to ordinary keyword results across the
same articles, so nothing is lost but the plain-English summary.
`[CONFIRM: is there an account-level opt-out, or only manual browsing and the fallback?]`

## Changes

If we introduce AI anywhere else in Oxford Abstracts, we will update this page before
that feature ships.

Questions about any of this: [contact our support team](https://oxfordabstracts.com/resources/contact-support/).

---

---

# Notes for review — not part of the policy

**Not to be published without legal review.** A public AI policy is a contractual
commitment.

**Protect the "what it cannot reach" section.** It is the strongest thing on the page and
it is true architecturally, not by promise — `api/search.js` imports a fixed file of help
content and has no database access. Most vendors can only say "we restrict access to". Do
not let it get softened into that.

**The support-form paragraph is deliberate.** The deflection card sends the subject and
description of a ticket somebody was about to submit, which can carry far more personal
detail than a search box. Saying "the question you typed" and leaving it there would be
technically true and quietly misleading. Naming it costs nothing and is the difference
between a policy that survives scrutiny and one that does not.

**Two gaps left before publication:**

1. **A retention period** for our own question log. There is no defined one, and
   "indefinitely" does not survive procurement. Related open action on the engineering
   handover: confirm the interaction log is covered by the existing privacy policy.
2. **Whether an account-level opt-out exists.** Manual browsing and the keyword fallback
   are now described, which may be enough — but some institutions will ask for a switch.
   Easy to build now, hard to retrofit with a deal waiting.

**One honest limitation, deliberately not claimed away.** Stripping emails and phone
numbers is pattern matching. It catches an address; it cannot catch a name typed into a
sentence. That is why the page asks people not to include personal data rather than
promising the log is anonymous. This matters more for the support form than the search
box, for the reason above.

**A practical note for whoever administers the Anthropic account:** if someone uses the
thumbs up/down feedback button inside Anthropic's own Console or Workbench, that
conversation may be used for training. It is the one exception to the no-training
position. It does not apply to anything our software sends, or to the "did this help"
buttons in our help centre — those stay with us. Org admins can disable it under
Settings → Privacy.

**Keep it dated and keep it to a page.** A short policy that is obviously current beats a
thorough one nobody trusts to still be true.
