---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Poster gallery — by plan

**This file is weak and should be treated as such.** Only one demo event was
available (78206, Professional Conference), so nothing about the other packages
was observed. Everything below marked `[untested]` is a gap for the next run,
not a finding.

The brief calls this section load-bearing because it settles plan gating
empirically. It does not settle it. It records what Professional shows.

| Capability | Professional Conference | Abstract Management | Basic (free) |
|---|---|---|---|
| "Poster questions" group in the +QUESTION picker | **Present** — "Poster upload" only, until one exists | `[untested]` | `[untested]` |
| "Poster gallery upload (1 allowed per event)" checkbox on file upload questions | **Present**, pre-ticked via the Poster upload route | `[untested]` | `[untested]` |
| "Poster keyword - dropdown" / "- multi-dropdown" / "- user selected" | **Present**, but only after an upload question exists | `[untested]` | `[untested]` |
| "Poster presentation link" | **Present**, but only after an upload question exists | `[untested]` | `[untested]` |
| "In poster gallery" checkbox in each question's Settings | **Present** on ordinary questions even with no poster question on the form | `[untested]` | `[untested]` |
| "In poster gallery" column in the decisions table | **Present**, but only while a poster gallery upload question exists | `[untested]` | `[untested]` |
| "Poster gallery" item under DISPLAY → Program menu | **Present and ticked by default** | `[untested]` | `[untested]` |
| The gallery itself at `/event/<id>/poster-gallery` | **Present** | `[untested]` | `[untested]` |
| Programme access types (Open access / login required / delegates / invited / access code) | **All five offered** | `[untested]` | `[untested]` |

## What can be said with confidence

- The gallery is part of the **conference programme** (`virtual.oxfordabstracts.com`),
  reached through **CONFERENCE → Program**. On this event the whole CONFERENCE
  section of the left-hand navigation is present.
  `[inferred]` — a package with no conference programme could not have a poster
  gallery, since the gallery is a page *of* the programme and its menu item is
  configured in the programme builder. That is an inference from architecture,
  not an observation of another plan.

## What the current article claims

`professional-conference-the-poster-gallery.md` claims the feature is available
**only in the Professional Conference package**. This run **could not verify**
that claim in either direction. It is consistent with everything observed, and
with the article's own title, but no other package was inspected.

## How to close this out on the next run

Get one event on each of Abstract Management and Basic and check, in order:

1. Is there a **CONFERENCE** section in the left-hand navigation at all?
2. Does **+ QUESTION** show a "Poster questions" group?
3. If a file upload question is created, does it offer "Poster gallery upload
   (1 allowed per event)"?
4. If not, is the option absent, greyed out, or does it show an upgrade prompt?
   The wording of the block matters more than its existence — it is what a
   confused organiser will search for.

`project/plan-feature-matrix.md` is the file that has to agree with the answer.
