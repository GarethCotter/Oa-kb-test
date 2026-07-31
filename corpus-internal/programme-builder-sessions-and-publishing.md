---
title: "Programme builder — sessions, publishing, access and what cannot be customised"
internal: true
last_reviewed: 2026-07-31
---

Publish the programme, programme not visible, hide a session, parallel sessions,
tracks, session chairs, move a presentation to another session, embed the programme,
programme filters, no PDF of the programme, programme codes.

Distilled from around 30 support tickets in the year to July 2026.

**Publishing controls everything.** An unpublished programme is visible only to
admins, and an embedded programme will keep asking viewers to log in until it is
published — setting open access is not enough on its own. You can publish and
unpublish as often as you like. Access type (open, login required, invited only) is
set under Programme builder → Settings.

**Sessions:**

- Every session needs a date and time before it can be created; both can change later.
  Old dates left over from a copied event are cleared in Settings → Dates.
- To move a presentation, **unassign** it from its current session first, then assign
  it to the new one.
- To place many abstracts at once, copy the submission IDs from the submissions table
  and bulk assign them.
- Parallel sessions are built with **columns**, limiting each session to a column.
  There is no limit on how many run concurrently.
- A session takes only **one track**, though it can hold many submissions.
- **Chairs are entirely separate from authors and presenters.** They are entered
  manually in the programme builder and are never matched to a person of the same name.
  There is no chair report — export the sessions table and remove duplicate rows.
- To put a speaker in a session, add them as an ordinary submission and attach it.

**Things that cannot be changed, because the layout is shared by every event:**

- Individual sessions cannot be hidden; only the whole programme can be unpublished.
- The filters across the top of the public programme cannot be switched off. The topic
  and track filters do come from submission questions, so unticking the category label
  on that question removes it as a filter.
- The order and arrangement of items cannot be customised.
- There are no URL redirects for programme pages. Embed the programme URL in an iframe
  on your own site instead; only the whole programme can be embedded, not a section.

**There is no direct PDF of the programme.** Download the docx from the programme
builder and convert it, export the sessions table to Excel, or take the programme from
the public front end. Programme builder downloads are Word only and admin only.

**Programme codes** are assigned with the assign-codes tool or by hand in the
decisions table, and replace the submission ID in the programme. Bulk assignment needs
the Standard or Professional package — it is not on Abstract Management.
