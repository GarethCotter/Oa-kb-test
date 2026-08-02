---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Poster gallery — overview

## What it is

A page inside the published conference programme
(`virtual.oxfordabstracts.com`) that shows accepted submissions' uploaded poster
PDFs as a browsable grid or list, each opening into a detail panel with the
abstract, authors, an optional embedded video and optional PDF download.

## The mental model a user needs

The gallery is **not a thing you switch on**. It is a *view* over submissions,
and it only has content when four separate conditions are all true. This is the
single most important fact about the feature and it is why "how do I set it up"
is the top support theme.

A poster appears in the gallery when **all four** of these hold:

1. A **file upload question exists on the submission form with the "Poster
   gallery upload (1 allowed per event)" checkbox ticked.** This one question is
   what creates the gallery. Nothing else does.
2. The **submitter uploaded a file** to that question.
3. The submission's **"In poster gallery" checkbox is ticked** in the decisions
   table.
4. The submission's **decision is "Accepted"**. Ticking without accepting shows
   nothing. (Observed: verified by controlled test, 31 Jul 2026.)

   **"Accepted: Poster" is not condition 3.** It is a decision sub-type and has
   no effect on the gallery. A submission set to *Accepted: Poster* without the
   "In poster gallery" tick does **not** appear; one set to plain *Accepted*
   with the tick does. The two settings are independent despite the naming.

Two further switches can empty a correctly-configured gallery:

5. **DISPLAY → Program menu → "Poster gallery"** must stay ticked, or the menu
   item disappears from the programme. (On by default.)
6. **Program access settings → "Show submission contents"** must stay ticked.
   Its own help text says unticking it "will disable access to all submission
   data including the poster gallery". (On by default.)

## The dependency that surprises people

Condition 1 is load-bearing in a way the interface does not explain:

- Before a poster upload question exists, the **"In poster gallery" column does
  not exist in the decisions table at all** — not hidden, absent from the
  COLUMNS list entirely.
- Before a poster upload question exists, the **"Poster questions" group in the
  +QUESTION picker contains only "Poster upload"**. The keyword and presentation
  link question types are invisible.
- Untick "Poster gallery upload" on an existing question and both the decisions
  column and every poster vanish immediately; re-tick and they come back with
  previous selections intact. (Observed: tested both directions, 31 Jul 2026.)

So an organiser who starts from the decisions table, or who goes looking for
poster keyword questions first, sees an interface with no poster features in it
and no explanation of why.

## Where each piece lives

| Piece | Path |
|---|---|
| The upload question | **Event dashboard → ABSTRACT MANAGEMENT → Submissions → Form & setup → + QUESTION → Poster questions → Poster upload** |
| Keyword / video questions | same picker, but only *after* the upload question exists |
| Which questions show beside the poster | each question's **Settings → "In poster gallery"** |
| Selecting posters | **ABSTRACT MANAGEMENT → Decisions → Table → "In poster gallery"** column |
| Menu item on/off, and its name | **CONFERENCE → Program → Builder → DISPLAY → Program menu** |
| Who can see it | **CONFERENCE → Program → Builder → PUBLISHED / dashboard Conference card → User access** |
| The gallery itself | `https://virtual.oxfordabstracts.com/event/<eventId>/poster-gallery` |

## What the gallery is not

- It is **not** a separate purchasable thing you enable in a settings screen.
  There is no "Poster gallery" item anywhere in the admin left-hand navigation.
- It does **not** enforce the one-page-PDF rule its own default wording asks
  for. See `behaviour.md`.
- Its search box does **not** search abstracts or keywords. See `behaviour.md`.
