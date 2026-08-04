# "Common questions" with no answer

*Found 3 August 2026. **21 of the 22 answered on 4 August 2026.** One remains.*

22 of the 61 "Common questions" headings had nothing under them, and they were
live: a reader saw the question they came for, followed immediately by the next
heading. They came over from the HubSpot FAQ silo when it was dissolved — the
questions survived the merge, the answers did not.

`scripts/checks.py` pins the count, now at **1**, so it can only fall.

---

## What was done

Every one of the 21 was answered **from content already on its own page**. Not one
needed new research, which is the interesting part: the answers had been sitting a
few paragraphs above the question the whole time. The FAQ had been asking things
the article already covered, and the merge dropped the paragraph that connected
them.

Most are two or three sentences with the menu path in bold. A few were worth more:

- **Word and character count** — the real answer is that this is a *counting
  difference*, not an overrun, and the fix is to raise the limit after the deadline.
- **Design the decision form** — you cannot add a new **Decision** option, because
  that question is fixed. You add 'rework' as an **acceptance type** instead. The
  question as asked has a false premise, and the answer says so.
- **Amending, deleting and copying a session** — deleting is one click, but you
  cannot delete a session that still has abstracts attached. That caveat is now in
  the answer rather than three paragraphs above it.
- **Session bookings** — the clash detector matches on surname plus first initial,
  so Jane Smith and J. Smith clash but Albert Jones and Bert Jones do not.

One malformed heading was fixed on the way past: *"How do I download information
from the** **Conference Program** **to Word?"* had stray bold markers in the
source.

## The one still open

**`07-delegate-registration/how-admins-can-amend-existing-delegate-registration-orders.md`
— "How do I delete a registration?"**

Deliberately left. The article lists exactly what an admin can change on an order —
change tickets, add or remove tickets and add-ons, request payment, issue a refund
— and deleting the registration is not among them. "Remove all tickets" is not the
same thing as deleting the order, and nothing in `corpus/` or `corpus-internal/`
mentions deletion at all.

So there are three possibilities and the page cannot tell us which: deletion is
somewhere else in the interface, deletion is not possible, or it is possible but
undocumented. **Answering it from the page would have been a guess**, and the
"Edit or refund order" correction — where a control was recorded as absent because
nobody opened the kebab menu — is the standing reminder of what guessing costs
here.

It needs somebody signed in to the software for two minutes. It is on the
verification list in `oa-loom-transcripts/VERIFICATION-QUEUE.md` alongside the
other claims waiting on app access.

Three outcomes are all fine: write the answer, say plainly that it is not
possible, or delete the question. Whichever it is, drop the pin in
`scripts/checks.py` to 0 afterwards.
