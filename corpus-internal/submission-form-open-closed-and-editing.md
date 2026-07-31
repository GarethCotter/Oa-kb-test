---
title: "\"New submissions are closed\" or a greyed-out Edit button — the form's separate switches"
internal: true
last_reviewed: 2026-07-31
---

New submissions are currently closed, cannot submit, edit button greyed out, edits
disabled for this submission, submitters cannot amend, reopen the form, let people
edit after the deadline, submission link not working, ineligible to submit.

Distilled from around 12 support tickets in the year to July 2026.

**The form is not one switch, it is several**, all on the event dashboard, and they
are the cause of nearly every "my submitters cannot do X" report:

- **New** — accepts new submissions. If this is off but the editing switches are on,
  submitters see *"Sorry, new submissions are currently closed for this event"*.
- **Edit complete** — lets submitters change a finished submission.
- **Edit incomplete** — lets them go back and finish an unfinished one.

A greyed-out or disabled **Edit** button, or *"Edits disabled for this submission"*,
is the relevant editing switch being off. Opening a form for editing opens it for
**everyone**, so export the submissions table first as a backup; for a single person,
it is usually easier for an admin to make the change in the submissions table instead.

**To let people revise without accepting new work**, turn the editing switches on and
leave **New** off, then send them the same submission link. They must sign in with the
address they originally used.

**"Your email address has not been permitted to submit"** means the stage is set to
*only allow specified email addresses* with none added — which blocks everybody.
Either switch it to allow anyone, or add the permitted addresses.

**The submission link is per stage**, of the form `.../stages/<id>/submitter`, and is
copied from Submissions → Form & setup. An old or mistyped link gives a
form-not-found error.

**A deadline written as "to 1 April" runs until 23:59 on 1 April.** The exact
auto-closure time and its timezone are shown by clicking the time on the dashboard.

**Always test as a non-admin.** Admin accounts see more and behave differently, so a
form that works for you can be shut to everyone else.
