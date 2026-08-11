# AI policy — draft for review

*Drafted 11 August 2026. **Not published, and not to be published without legal review.**
A public AI policy is a contractual commitment; several statements below need confirming
against Anthropic's current terms and Oxford Abstracts' own privacy policy before anyone
outside the company sees it.*

The reader this is written for is a university procurement officer or data protection
officer deciding whether Oxford Abstracts is safe to buy. They are not reassured by
warmth. They are reassured by specifics, and they read for weasel words. Every vague
sentence in a document like this creates a follow-up email, so the aim is to answer the
questions before they are asked.

---

## The draft

### Where we use AI, and where we do not

Oxford Abstracts uses AI in one place: **the help centre's answer layer.** When somebody
types a question into our help centre — or into the help widget inside the app, or the
support form — we send that question to an AI model, which writes a plain-English answer
from our own published help articles.

That is the only use of AI in Oxford Abstracts. **It is not used anywhere in the
conference software itself.** It does not read, score, summarise, sort or make any
decision about:

- abstracts or any other submission
- reviews, grades or reviewer comments
- decisions on submissions
- delegate or registration data
- programmes, sessions or any event content
- emails you send through the system

No submission is ever assessed by AI. No decision about a submission is ever influenced
by AI. If that changes, this page changes first.

### What is actually sent to the AI provider

Two things, and nothing else:

1. **The question the person typed.**
2. **The text of our own help articles** — the same public pages anyone can read on our
   help centre.

The model has no connection to your event. It cannot query your data, and your data is
not in the material it reads. This is not a policy promise; it is how the system is
built — the answer layer reads a fixed file of help content and has no access to the
conference database at all.

### Who provides the model

**Anthropic**, using Claude Haiku. Anthropic acts as a sub-processor for this feature and
is named as such in our data processing documentation.

### Is our data used to train AI models?

**No.** Questions sent through this feature are not used to train models. Anthropic's
commercial API terms state that inputs and outputs submitted through the API are not used
to train its models. `[LINK TO ANTHROPIC'S CURRENT TERMS — do not paraphrase, cite]`

`[REVIEW: confirm the exact current wording and retention period Anthropic applies to API
inputs, and whether a signed DPA is in place. Do not publish this section until that is
verified — this is the single sentence a DPO will hold us to.]`

### What we keep, and for how long

We log the questions people ask so we can see which parts of our documentation are not
working and fix them. That log records the question text, which articles were used to
answer it, and whether the person said it helped.

**Before storage, email addresses and telephone numbers are automatically removed from
the question text.**

We ask people not to include personal data or confidential event details in a help
question, because a help question is not the right place for them and we do not need them
to answer it. Automatic removal catches email addresses and phone numbers; it cannot
catch a name typed into a sentence.

`[REVIEW: state the retention period. There is currently no defined one, and "we keep it
indefinitely" is not an answer that survives procurement. Decide a period, and confirm the
interaction log is covered by the existing privacy policy — this is an open action already
on the engineering handover.]`

### What happens if you would rather not use it

The help centre works without the AI layer. If the answer feature is unavailable, or if
you would rather not use it, the help centre falls back to ordinary keyword search across
the same articles. Nothing is lost except the plain-English summary.

`[DECISION NEEDED: do we offer an opt-out at the event or account level — a switch that
turns the answer layer off for an organisation's users? Some institutions will ask. It is
straightforward to build and much harder to add later under time pressure.]`

### Accuracy, and what we do not let it do

The model answers **only** from our help articles. It is instructed not to guess: where
our documentation does not cover something, it returns no answer rather than inventing
one, and the reader gets ordinary search results instead.

Answers cite the articles they came from, so anyone can check the source. If an answer is
wrong, the fault is our documentation, and we would rather you told us — every answer has
a "this didn't help" option that reaches the team who maintain the content.

### Questions

`[Contact route — the support address, or a named privacy contact if procurement
requires one.]`

---

## Notes on the draft, for whoever reviews it

**What makes this document persuasive is the second section**, and it is worth protecting.
"The AI cannot see your event data" is an unusually strong claim, and it is true
architecturally rather than by promise — the answer layer imports a fixed file of help
content and has no database access. Most vendors cannot say that. It should be the first
thing on the page and it should never be softened into "we limit access to".

**Do not publish the training paragraph until it is verified.** It is the sentence a data
protection officer will quote back during a dispute. Cite Anthropic's terms with a link
rather than paraphrasing them, so the statement stays true when their wording changes.

**The retention gap is real and known.** The engineering handover already carries an open
action to confirm the interaction log is covered by the privacy policy, and notes that
while emails and phone numbers are stripped by pattern matching, nothing stops somebody
typing a name or an event ID into a question. The policy above says this plainly rather
than implying the log is anonymous. Claiming more than the software does would be worse
than saying nothing.

**Three things to decide before publication:**

1. A retention period for the question log.
2. Whether an opt-out exists, and at what level.
3. Whether the widget and the support form are named separately here — they call the same
   endpoint, but a procurement officer reading about "the help centre" may not realise the
   in-app widget is the same feature under a different name.

**Keep it on one page and keep it dated.** A short policy that is obviously current beats
a thorough one nobody trusts to still be true. Put "last reviewed" on it, and add a line
committing to updating it before any new use of AI ships — that commitment is worth more
to a cautious buyer than any amount of description.
