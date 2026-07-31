---
title: "Exports, custom reports and abstract books — child rows, columns and empty books"
internal: true
last_reviewed: 2026-07-31
---

Export author details, download the submission table, child rows, spreadsheet builder,
custom report, abstract book empty, book contains only titles, presenter email list,
export missing columns, registration export.

Distilled from around 25 support tickets in the year to July 2026.

**Child rows are the answer to most export questions.** Author names, affiliations,
emails, presenting status and registration status all live on the *child rows* of a
submission. Export the submissions table **with child rows** and each author appears
as their own row. A presenter list is that export filtered on the presenting column.
Without child rows you get the submitter only.

**Exports contain the columns you can see.** On the submissions and decisions tables,
use the **Columns** button to switch fields on before downloading, because the export
mirrors the current view. The **registration table behaves the opposite way** — the
column filter changes only the screen, and the download always contains every column,
so unwanted ones have to be deleted afterwards.

**The spreadsheet builder** lets you pick exactly which fields appear in a custom
Excel report, and is the right route when no standard report has the combination you
need. It cannot reach the registration table, and registration status is not among its
fields.

**An accepted-abstracts book downloads empty until decisions have actually been made.**
The "all abstracts" reports still contain data, so an empty accepted book is usually
a decisions problem rather than a book problem. If submissions are missing from a book
or custom report, look for an unanswered dependency question.

**A book containing nothing but titles** is the per-question **In abstract book**
checkbox, unticked. See the note on question checkboxes.

**Two book tools exist:** the custom book builder, which offers grouping and sorting
(by acceptance type, first author surname and so on), and the more advanced book
builder where you edit the template and use *Save as* to keep a named version. Oxford
Abstracts can also build bespoke books and reports on request — these then appear as
extra headings on the event's Reports and downloads page. Complex ones may carry a
development cost.

**Two export oddities worth knowing:** the registered-date column comes out as text
because it carries date, time and timezone together, so strip the time to sort
chronologically; and TRUE/FALSE in an export is simply the system's yes/no.
