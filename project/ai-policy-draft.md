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

Two things: the question you typed, and the text of our own help articles — the same
public pages anyone can read.

## Who provides the model, and training

**Anthropic**, using Claude Haiku, acting as a sub-processor for this feature.

**Your questions are not used to train AI models.**
`[LINK TO ANTHROPIC'S CURRENT API TERMS]`

## What we keep

We log the questions asked so we can see which of our documentation is not working and
improve it. Email addresses and telephone numbers are automatically removed before
storage. `[RETENTION PERIOD]`

Please do not include personal data or confidential event details in a help question —
we do not need them to answer it.

## If you would rather not use it

The help centre works without it. Turn the feature off, or if it is ever unavailable, and
search falls back to ordinary keyword results across the same articles.
`[CONFIRM: is there an account-level opt-out, or only the fallback?]`

## Changes

If we introduce AI anywhere else in Oxford Abstracts, we will update this page before
that feature ships.

`[CONTACT ROUTE]`

---

---

# Notes for review — not part of the policy

**Not to be published without legal review.** A public AI policy is a contractual
commitment.

**Protect the "what it cannot reach" section.** It is the strongest thing on the page and
it is true architecturally, not by promise — `api/search.js` imports a fixed file of help
content and has no database access. Most vendors can only say "we restrict access to". Do
not let it get softened into that.

**Four gaps to close before publication:**

1. **Anthropic's training terms** — cite by link, do not paraphrase, so the statement stays
   true when their wording changes. This is the sentence a data protection officer will
   quote back during a dispute.
2. **A retention period** for the question log. There is no defined one, and "indefinitely"
   does not survive procurement. Related open action on the engineering handover: confirm
   the interaction log is covered by the existing privacy policy.
3. **Whether an opt-out exists**, and at what level. Some institutions will ask. Easy now,
   hard to retrofit with a deal waiting.
4. **A contact route** — support address, or a named privacy contact if procurement wants one.

**One honest limitation, deliberately not claimed away.** Stripping emails and phone
numbers is pattern matching. It catches an address; it cannot catch a name typed into a
sentence. That is why the page asks people not to include personal data rather than
promising the log is anonymous.

**Keep it dated and keep it to a page.** A short policy that is obviously current beats a
thorough one nobody trusts to still be true.
