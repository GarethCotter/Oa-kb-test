# "Common questions" with no answer

*Found 3 August 2026, while tracing a Loom transcript back into the corpus.*

**22 of the 61 "Common questions" headings have nothing under them.** They are not
drafts sitting in a backlog — they are **live on the site**. A reader sees the
question they came for, followed immediately by the next heading.

Verified in the built HTML, e.g.
`03-reviewing/assigning-and-unassigning-a-submission-to-a-reviewer.html`:

```html
<h3 id="i-need-to-assign-a-large-number-of-submissions-to-several-reviewers...">
  I need to assign a large number of submissions to several reviewers. Is there a quick way of doing this?</h3>
<h3 id="allowing-committee-members-to-assign-reviews">Allowing committee members to assign reviews</h3>
```

They came over from the HubSpot FAQ silo when it was dissolved: the questions
survived the merge, the answers did not.

**A question with no answer is worse than no question.** It confirms the reader's
problem is a known one and then abandons them, on the page that was supposed to
help. It also feeds the answer layer a heading with no content behind it.

`scripts/checks.py` now pins this at 22 so the number can only fall.

---

## The 22

### 01 Getting started
- `manage-users.md` — How do I add committee members to the software?
- `manage-users.md` — How do I give someone admin rights to the event?

### 02 Submissions
- `making-a-submission-on-behalf-of-someone-else.md` — How do I submit an abstract on behalf on someone else?
- `opening-and-closing-submissions-deadlines.md` — I want to close submissions, but allow those who have already submitted to edit their submissions. How do I do that?
- `word-and-character-count.md` — Users have reported that the abstract field in the submission form is alerting them that they are over the word limit? How can I resolve this?

### 03 Reviewing
- `assigning-and-unassigning-a-submission-to-a-reviewer.md` — I need to assign a large number of submissions to several reviewers. Is there a quick way of doing this?
- `editing-a-review-or-completing-a-review-on-behalf-of-a-reviewer.md` — I need to complete a review on behalf of a reviewer. How do I do that?

### 04 Decisions
- `assigning-categories-to-committee-members.md` — I want committee members to be able to make decisions on specific categories. How do I do this?
- `design-the-decision-form.md` — I want to add another decision type - 'rework' - how do I do this?
- `notifying-submitters-of-their-outcomes.md` — How do I send emails to let submitters know if they have been rejected or accepted?

### 05 Emails
- `creating-custom-emails.md` — How can I create an email that's not on the list of templates?
- `emailing-presenters-and-authors-directly.md` — I want to send emails to just the presenters - how do I do this?
- `sending-emails-from-your-chosen-email-address.md` — I want the emails that are associated with the event to be from an email address of my choosing. Is this possible?
- `using-the-email-sent-log.md` — I'm not sure if I sent an email. How can I check?

### 06 Programme, exports and reports
- `abstract-books.md` — How do I edit the fields I want to appear in the abstract book?
- `downloading-your-program-and-session-books.md` — How do I download information from the Conference Program to Word?
- `public-vs-full-access-programme.md` — I am unsure what can be viewed in the public and private (full access) version of the program?

### 07 Delegate registration
- `how-admins-can-amend-existing-delegate-registration-orders.md` — How do I delete a registration?
- `setting-up-payment-providers-for-delegate-registration.md` — How do I set up payment for delegates?

### 08 Conference platform
- `amending-deleting-and-copying-a-session.md` — How do I delete a session?
- `controlling-access-to-the-programme.md` — I need to give full access to some people who have not bought a ticket to the conference. How do I do that?
- `session-bookings.md` — How can I see if there is a clash in bookings?

---

## How to clear them

Many are answerable **from the article they already sit on** — the question is a
restatement of a procedure documented higher up the same page. Those are a
cross-reference, not new research, and are the cheapest wins here.

Others need a fact nobody has confirmed. Do not guess: an unanswered question is
bad, a wrong answer is worse.

**Deleting a question is a legitimate outcome.** If it duplicates the article's own
standfirst, or nobody actually asks it, removing it beats leaving it hanging. The
pinned count falls either way.

## Why this list matters beyond the FAQ

It is the best target list the Loom transcript project could have. Support recorded
a video precisely where writing the answer down did not happen, and these are 22
places, in the customer's own words, where it demonstrably did not happen.

Of five sample transcripts read on 3 August, four landed on entries in this list —
including a complete answer to the reviewer-assignment question above. That match
rate is the metric worth tracking when the full library is pulled.
