# What the Amplitude widget was asked, and whether we can answer it

*Analysed 11 August 2026 from an export of the Amplitude assistant's chat sessions.
710 sessions, 657 distinct opening questions.*

Grouping rewordings together ("how do I assign reviewers" and "how to assign abstracts
for review" are one question) leaves **47 questions asked more than once, covering 108
sessions — about 15% of all traffic**.

Each of those 47 went through the live `/api/search`, rather than being judged by
reading. Routing is probabilistic and phrasing moves it more than content does, so an
opinion about whether an article "covers" something is worth much less than asking the
router. Every result below is what the endpoint actually returned.

**Source data stays out of this repo.** The export carries user IDs and links to
individual chat sessions. Only the question wording is reproduced here, and one payment
message a user pasted in is described rather than quoted.

## The headline — and why one run is not a measurement

The 47 were run **twice**: once on 11 August, then again after a parser fix the same day.

| | First run | Second run |
|---|---|---|
| Strong confidence | 21 | 23 |
| Answered, low confidence | 10 | 5 |
| No answer | 16 | 19 |

Do not read the strong figure going 21 → 23 as improvement. **Nine of the 47 changed
state between the two runs — 19% churn** on identical questions against near-identical
content. That is the probabilistic routing CLAUDE.md warns about, measured: *"the same
question can answer on one run and not the next, and phrasing moves it more than content
does."*

So the only figures worth quoting are the ones that held across both runs:

- **20 of 47 answered strongly in both runs.** These are what the widget reliably deflects.
- **14 of 47 missed in both runs.** Of those, 4 are not questions, so **10 durable gaps**.
- The remaining 13 are unstable — sometimes answered, sometimes not.

**This has a direct consequence for the metrics.** A strong-answer rate taken from a
single run carries roughly ±19% noise, which is larger than any improvement a quarter of
content work would produce. Any KPI built on it must average several runs, or use a much
larger sample, or it will measure the dice rather than the corpus.

### What the parser fix did and did not do

The fix (commit `a9a979d`) was confirmed: three questions had been returning literal JSON
to the reader, and no longer do. Two of them now correctly report *no answer* and fall
back to keyword search, which is why "answered" went **down** while the site got better —
those three were counted as answered when what they served was machinery.

Everything else that moved is inside the churn and cannot be attributed to the fix. In
particular, "How do I reset my password?" went weak → strong **without** the `HEDGES` list
being touched, so that was the coin landing differently rather than anything being fixed.

---

## 1. Real gaps — missed in both runs, nothing to answer from

Ten durable gaps. Two items from the first pass have been removed from this list because
the second run answered them: **"I need the attendee to select only one ticket"** came
back strong (the *Maximum number of tickets per order* setting was found), and **"missing
recording links"** returned a weak answer. Both were single-run misses, not gaps —
exactly the trap this section is meant to avoid.

Ordered roughly by how cheap they look to fix:

- **"What is an email address in red with a circled C next to it?"** — somebody describing
  a UI indicator they cannot interpret. Nothing in the corpus explains any status icon.
  Probably the single best-value item here: whoever knows what that badge means can
  settle it in a sentence, and a reader who sees it has no other route.
- **"Restrict ticket registrations by role"** — nothing found in either run. Distinct
  from the per-order ticket cap, which the second run did answer.
- **"Steps to add an additional location"** — venues or rooms in the programme. Nothing
  found.
- **"Upload a program"** — importing an existing programme rather than building one.
- **"Inviting new program users"** and **"Event admins"** — user management for the
  conference platform. `corpus/01-getting-started` covers Users, but not from this angle.
- **"Who are the conference delegates?"** — reads like someone trying to understand the
  vocabulary. Worth noting the corpus uses "delegate", "attendee" and "registrant" in
  different places.
- **"Virtual booth"** — `corpus-internal/exhibitor-booths.md` exists but did not surface.
- **"Remove myself from event"** — an admin removing their own access.
- **"Missing recording links"** — session recordings.
- **"How do I get a link in a form or email to open in a new tab?"** — specific, and the
  sort of thing that has a one-line answer or a flat "not possible".

Four of the sixteen are not answerable questions and need no article: `tutorial`,
`person`, `wordpress` (one word, no context), and a pasted message from a supplier asking
for a billing address, which is not a product question at all.

## 2. Answered, but the model was not confident

Ten questions produced an answer the endpoint marked **weak**. Under the deflection
card's rules a weak answer is never shown, so today these behave exactly like misses even
though the content exists.

What is striking is that most of them cited **the right article**:

| Question | What it found |
|---|---|
| Disable video chat in networking (3x) | The chat feature · Networking for attendees |
| Where are the template emails stored | Editing the template emails · Creating custom emails |
| How can I edit the certificate email? | Creating a certificate · Editing the template emails |
| How can I find unassigned reviews? | The review tables · Assigning and unassigning a submission |
| I am assigning a reviewer but it won't save | Assigning and unassigning · If your reviewers can't see their assigned submissions |
| Can submitters amend submissions that already have reviewers assigned? | Editing an abstract or submission |
| Can I stop reviewers seeing their grades after decisions? | Controlling what the reviewer can see · Designing the review form |
| How do I reset my password? | Creating an account and logging in |
| Set up a new event | Creating and paying for a new event · Event details |
| Filtering specific recipients in email setup | Sending and scheduling emails · Creating custom emails |

This is not a content problem. The router reached the correct page and the answering call
could not commit. Two likely causes, both worth testing before writing anything:

- The article covers the topic but does not state the specific fact in a form the model
  can quote — the "answer is in the prose but not as an answer" problem.
- The question is short and keyword-shaped ("virtual booth", "past reviews", "refund"),
  which the answering prompt treats cautiously by design.

**"How do I reset my password?" coming back weak is the clearest signal.** That is about
as common and as answerable as a question gets. If it cannot reach strong confidence, the
confidence threshold or the article's phrasing is wrong — not the corpus.

## 3. What to do, in order

1. **Run the set three more times before writing anything.** With 19% churn, two runs
   cannot separate a real gap from an unlucky one. Five runs would put every question in
   one of three honest buckets: always answered, never answered, or unstable. The
   unstable bucket is its own finding — those are questions where the content exists but
   the router only sometimes reaches it, which is a phrasing and synonyms problem, not a
   writing one.
2. **Write the ten durable gaps**, cheapest first. Several are one-liners; the status-icon
   one needs somebody who knows the product.
3. **Check the vocabulary drift** — delegate / attendee / registrant, programme / program.
   Several misses read like the asker's word and ours not matching, which is exactly what
   `SYNONYMS` in `assets/search.js` exists for.
4. **Re-run this analysis after those changes.** The script is forty lines: group the
   export by meaning, post each cluster to `/api/search`, record answered and confidence.
   Pace it at 17 seconds a call or the rate limiter will 429 it, and a 429 is
   indistinguishable from "no answer" in the results.

## Two caveats on the data

**This is a different population from ticket-openers.** These are people who chose a chat
widget, and their questions skew short and keyword-ish. That is genuinely harder for a
router than a full sentence, so the miss rate here is probably a pessimistic estimate of
how the new widget performs on a support form, where people write in prose.

**The window is long.** Some questions refer to features that may have changed since. The
recording-links and virtual-booth items in particular are worth confirming against the
current product before writing anything.
