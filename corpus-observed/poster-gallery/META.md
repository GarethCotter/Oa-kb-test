---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Assignment

- **Feature:** the poster gallery — setup on the submission form, selection in the
  decisions table, and the gallery as delegates see it
- **Plans to explore under:** Professional Conference (the only demo event available;
  everything about other plans is therefore `[untested]`)
- **Test account:** Gareth's admin account on demo **event 78206**, dashboard at
  `https://app.oxfordabstracts.com/admin/events/78206/app/dashboard`. Signed in via
  Chrome; the session lives in Gareth's browser, so use the `claude-in-chrome` tools.
  No live customer event touched.
- **App version / date:** run started 31 July 2026; no version string visible in the
  interface so far
- **Existing articles covering this feature:**
  - `corpus/08-conference-platform/professional-conference-the-poster-gallery.md`
  - `corpus/14-for-attendees-exhibitors/exploring-the-poster-gallery.md`
  - `corpus/02-submissions/collecting-slides-and-posters-from-presenters.md`
  - `corpus/02-submissions/question-setting-tags.md` (the tags the gallery depends on)

## Why this feature

292 of the 4,898 support tickets in the year to July 2026 mention the poster gallery.
"How do I set it up" is 59 of 147 question sentences in those tickets — three times the
next theme — and the specific confusion is consistent: people do not connect the
gallery to a question on the submission form.

## What limited the run

- Only a Professional event is available, so the by-plan section can record what
  Professional shows but cannot empirically confirm what is hidden on Basic or
  Abstract Management. Those lines are `[untested]`.
- No submitter account: the submitter-side experience is observed through admin
  "submit on behalf of" where possible, and marked `[untested]` where not.

---

# Verification list

Every checkable claim the current articles make. Each will be marked **confirmed**,
**changed** (with what it is now) or **could not verify** after the walk.

## From `professional-conference-the-poster-gallery.md`

| # | Claim | Status |
|---|---|---|
| 1 | The feature is only available in the Professional Conference package | |
| 2 | Posters can only be uploaded in PDF format | |
| 3 | Posters can only be one page in length | |
| 4 | There is no file size limit for poster upload | |
| 5 | Path is Event dashboard → Abstract Management → Submissions → Form & Setup → +QUESTION | |
| 6 | There is a "Poster Upload" option underneath a "Poster Questions" heading | |
| 7 | A checkbox labelled "Poster gallery upload" exists at the bottom of the question | |
| 8 | Ticking it automatically restricts uploads to PDFs only | |
| 9 | A checkbox labelled "Include poster download button" exists | |
| 10 | A checkbox labelled "In program" is required for posters to show in the program | |
| 11 | Button is labelled "Create Question" | |
| 12 | Keyword questions enable searching by keyword in the gallery | |
| 13 | Only one of the three poster keyword options can be added | |
| 14 | A presentation video question allows YouTube and Vimeo embedded in the gallery | |
| 15 | Button is labelled "CREATE SELECTED QUESTION" | |
| 16 | Other questions appear beside the poster via tag checkboxes at the end of the question | |
| 17 | Selection happens in the decisions table via an "In poster gallery" column | |
| 18 | The submission must be accepted as well as ticked | |
| 19 | Bulk selection is possible from the decisions table | |
| 20 | The gallery icon appears in the left-hand menu of the conference program | |
| 21 | Gallery offers: search, alphabetical sort, list/grid view, filter by session, filter by track, filter by keyword | |
| 22 | Clicking a poster allows download (if permitted) and viewing full abstract details | |

## From `exploring-the-poster-gallery.md` (attendee side)

| # | Claim | Status |
|---|---|---|
| 23 | Delegates reach it from the menu icon top left, then "Poster Gallery" | |
| 24 | Keyword search matches partial strings (e.g. "ana" returns "analysis") | |
| 25 | Sort options include alphabetical and by submission ID / program code | |

## Open questions the tickets raise, to answer by observation

- **Q1** What exactly makes a poster appear? Support replies say the "In poster gallery"
  column only exists once a poster upload question exists — is that so?
- **Q2** Is there a separate poster gallery URL that works before the programme is
  published? Support replies say yes.
- **Q3** Where is the Poster Gallery menu item switched on — programme builder?
- **Q4** What happens with a multi-page PDF, a non-PDF, and a very large file — verbatim
  error messages.
- **Q5** Do the article's screenshots still match the interface? Ten of the eleven date
  from 2021–2022.
