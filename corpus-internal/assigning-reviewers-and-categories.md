---
title: "Auto-assign, reviewer categories and why assignment produces nothing"
internal: true
last_reviewed: 2026-07-31
---

Auto assign reviewers, reviewers have no submissions, categories not showing on the
reviewer form, reviewer upload template incompatible, assign by topic, bulk assign
reviewers, unassign incomplete reviews, delete a reviewer.

Distilled from around 20 support tickets in the year to July 2026.

**Categories come from the submission form, and only from a dropdown.** The category
question must be a **single-select dropdown** with the category tag ticked. A
multiple-select dropdown or a checkbox question will not produce assignable
categories — which is why the category field can be missing from the reviewer form
entirely. Only one category question is supported.

**The reviewer form has to carry that category question** before categories will
import against reviewers or appear in the download template.

**Auto-assign matches on category and nothing else.** You set a minimum number of
reviewers per submission, and categories must already be assigned to each reviewer in
the reviewers list. Assignment by any other question, or pairing particular reviewers,
has to be done by hand using the column filters in Reviews by submission. There is no
bulk upload of reviewer-to-submission assignments, and **no undo for a batch**.

**"Re-assign all incomplete reviews"** only touches submissions whose reviews were
never completed. Finished reviews are left alone.

**Things that quietly produce an empty reviewer dashboard:**

- Submissions have not actually been assigned yet — the review count stays at zero.
- The reviewer is listed under an address they have not registered.
- The reviewer was deleted from the list while still holding assignments. Removing a
  reviewer no longer unassigns their submissions, so unassign first, then delete.

**The reviewer upload spreadsheet must match the downloaded template exactly**,
including the parent category column. Extra columns or a stray comma give an
"incompatible" error — open the file in a plain text editor to find it.

**A multi-stage event with a category question in more than one stage** shows every
stage's options on the reviewer sign-up form. Keep the values identical across stages,
or hide the question in the stages you are not using.

**Bulk emails to reviewers fail** unless the reviewer's address is also on the event
users page.
