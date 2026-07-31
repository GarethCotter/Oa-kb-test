---
title: "Which emails send automatically, and what merge fields can and cannot do"
internal: true
last_reviewed: 2026-07-31
---

Automatic emails, chase incomplete submissions, email selected submitters, merge field
not working, submission edit link, test email shows empty links, email authors and
submitters together, notify admins of new submissions, attach a file to an email,
resend the confirmation email.

Distilled from around 20 support tickets in the year to July 2026.

**Only the templates at the top of the emails page send automatically**, they fire on
submission, and they always go to **submitters only**. Everything else — chasing
incomplete submissions, telling people about decisions, reminding presenters — is a
manual send, either from the emails page or by selecting rows in a table.

**Tables are how you reach anyone who is not a submitter:** the decisions table for
authors and presenters, the envelope icon on the registrations table for delegates.
Filter the decisions table on decision and registration status to email, say, accepted
presenters who have not yet registered. You cannot email submitters and authors in one
send; do the two groups separately.

**Merge fields:**

- **A test email does not populate merge fields**, so links look empty. Send to a real
  or test submission to check one properly.
- There are **two link fields**: the submission link, and the **submission edit link**
  which drops the person straight into their own submission to amend it.
- **Form responses cannot be merged** into automatic templates — this is by design.
  Point people to their dashboard, or email manually from the submission table.
- **A question hidden in a stage will not merge** into that stage's emails. Set it to
  **read only** instead of hidden and the value still appears.
- There is **no merge field for the stage name** — make a template per stage and type
  it.
- **Reviewer comments cannot be merged** into notification emails; submitters read
  them on their dashboard.

**Notifying admins of each new submission:** add the notification addresses on Event
setup → Event details, then open the relevant template and tick the CC or BCC option
for conference notification emails at the bottom.

**Things that cannot be changed:**

- The **"submission created"** email fires at the moment of submission and cannot be
  re-sent. A manual email is the alternative, without the personalised detail.
- The **reviewer recruitment** confirmation and the **certificate** email have fixed
  wording shared across all events. Follow up with an "email selected" message from
  the reviewers list instead.
- A **deleted email template cannot be restored.**

**Attachments** on a template reach the recipient as a link to the file in Oxford
Abstracts, not as an attached file.

**Emails send from the event name with the notification address as reply-to** unless
you verify your own sender address — see the DKIM note.
