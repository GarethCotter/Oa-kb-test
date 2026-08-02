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
  Abstract Management. Those lines are `[untested]`. See `by-plan.md`.
- No submitter account: the submitter-side experience was observed through admin
  **"Submit on behalf"**. What a real submitter sees when signing in, editing a
  submission, or replacing a poster after the deadline is `[untested]`.
- **No screenshots were saved to disk.** The screenshot tool in this session
  returns images to the transcript but exposes no writable path, and its
  `save_to_disk` option returned no location. `screenshots/` is therefore empty
  and every state is described in prose instead, with labels quoted verbatim.
  This is a real gap against the brief — the run cannot supply replacements for
  the 2021–2022 images. Next run should capture them deliberately.
- The Chrome extension disconnected near the end of the run, which is why
  claim 19 (bulk selection) is unverified.
- Test files were minimal PDFs generated for this run, not real posters. The
  inline-viewer failure in `errors.md` should be confirmed against a real
  customer poster before being written up as product behaviour.
- The event's own access settings were **not** changed. The five programme access
  types and the effect of unticking "Show submission contents" are `[untested]`.

## What was changed on event 78206

Left in place (Gareth agreed the demo event may be altered):

- Three questions added to the submission form: **Poster** (file upload, poster
  gallery upload), **Poster presentation link**, **Poster keywords**.
- Two submissions created on behalf of `test.submitter.one@example.com` and
  `test.submitter.two@example.com` — "Test Poster One" and "Test Poster Two",
  both Accepted and both ticked "In poster gallery".
- The programme was **published** (it was unpublished at the start of the run) in
  order to test anonymous access. **Worth reverting if the demo event is used to
  demonstrate an unpublished programme.**

Toggled and restored: "Poster gallery upload" was unticked and re-ticked to test
Q1. Verified restored — column back, both posters back, ticks intact.

---

# Verification list — reconciled

Status after the walk. **Confirmed** = observed to be true as written.
**Changed** = the claim is wrong or the wording has moved; what it is now is
given. **Could not verify** = not established this run.

## From `professional-conference-the-poster-gallery.md`

| # | Claim | Status |
|---|---|---|
| 1 | The feature is only available in the Professional Conference package | **Could not verify** — only a Professional event was available. Consistent with everything seen; not tested. |
| 2 | Posters can only be uploaded in PDF format | **Confirmed in effect** — but *not* via the "Allowed file extensions" field, which stays blank. Ticking "Poster gallery upload" forces `accept=".pdf"` and server-side rejection. |
| 3 | Posters can only be one page in length | **Changed — not enforced.** A 3-page PDF uploaded with no error or warning. Only page 1 is shown in the gallery. "1 page" is only the default description text. |
| 4 | There is no file size limit for poster upload | **Changed.** Default limit **10MB**; settable 0–500 in "Max file size (MB)". Verbatim error captured in `errors.md`. |
| 5 | Path is Event dashboard → Abstract Management → Submissions → Form & Setup → +QUESTION | **Confirmed**, with label corrections: **"Form & setup"** (lower-case s) and the button reads **"+ QUESTION"**. Note *Decisions* also has a "Form & setup". |
| 6 | There is a "Poster Upload" option underneath a "Poster Questions" heading | **Confirmed**, wording corrected to **"Poster upload"** under **"Poster questions"**. Major addition: it is the **only** option there until one exists. |
| 7 | A checkbox labelled "Poster gallery upload" exists at the bottom of the question | **Changed** — label is **"Poster gallery upload (1 allowed per event)"**. Pre-ticked when reached via Poster upload. |
| 8 | Ticking it automatically restricts uploads to PDFs only | **Confirmed in effect**, with the nuance in claim 2: the extensions field is never updated, so the interface contradicts the behaviour. |
| 9 | A checkbox labelled "Include poster download button" exists | **Changed** — label is **"Allow poster downloads"**. Ticked by default; only visible while "Poster gallery upload" is ticked. |
| 10 | A checkbox labelled "In program" is required for posters to show in the program | **Partly confirmed** — the checkbox exists and is ticked by default. Whether it is *required* for programme display is `[untested]`. |
| 11 | Button is labelled "Create Question" | **Confirmed** — accessible name "Create Question", rendered **"CREATE QUESTION"**. |
| 12 | Keyword questions enable searching by keyword in the gallery | **Changed.** Keywords drive a **"Keywords" filter dropdown**, not the search box. Searching a keyword returns 0 results. |
| 13 | Only one of the three poster keyword options can be added | **Confirmed**, and stronger: after adding one upload, one link and one keyword question, the whole **"Poster questions" group disappears** from the picker. |
| 14 | A presentation video question allows YouTube and Vimeo embedded in the gallery | **Confirmed.** The type is **"Poster presentation link"** (editor headed "Submitter link"), default description `Youtube and Vimeo links will appear as embedded videos`. A YouTube URL rendered as an embedded player. |
| 15 | Button is labelled "CREATE SELECTED QUESTION" | **Changed** — the button is **"CREATE QUESTION"** on all three poster question types. |
| 16 | Other questions appear beside the poster via tag checkboxes at the end of the question | **Confirmed**, wording corrected: a checkbox **"In poster gallery"** in each question's Settings, tooltip `Display responses to this question in the poster gallery`. Abstract was on and appeared; Presentation was off and did not. |
| 17 | Selection happens in the decisions table via an "In poster gallery" column | **Confirmed.** Column group **"Decision responses"**; shown by default; sits between "Decision last updated" and "Final category". |
| 18 | The submission must be accepted as well as ticked | **Confirmed by controlled test.** Two submissions ticked, one Accepted and one Pending → gallery showed only the Accepted one. |
| 19 | Bulk selection is possible from the decisions table | **Confirmed**, and the mechanism is more specific than the claim. Select rows → **"BULK DECIDE"** → panel section **"Additional decision options"** → **"ADD TO POSTER GALLERY"** with a paired **"REMOVE"**. Round trip tested both ways. |
| 20 | The gallery icon appears in the left-hand menu of the conference program | **Confirmed** — **"Poster gallery"** with an icon, in the persistent left sidebar. |
| 21 | Gallery offers: search, alphabetical sort, list/grid view, filter by session, filter by track, filter by keyword | **Partly changed.** Observed: search, sort (A-Z titles / Z-A titles / Program codes), list & grid, **"Topics"** filter, **"Keywords"** filter. **No session or track filter appeared** — no sessions/tracks were assigned, so `[untested]`. "Topics" is not in the article's list. |
| 22 | Clicking a poster allows download (if permitted) and viewing full abstract details | **Confirmed.** "Original poster (PDF)" plus program code, title, topic, authors + affiliations, abstract, presentation link, keywords, comments. |

## From `exploring-the-poster-gallery.md` (attendee side)

| # | Claim | Status |
|---|---|---|
| 23 | Delegates reach it from the menu icon top left, then "Poster Gallery" | **Changed.** It is a **persistent left sidebar** (collapsible via a hamburger top left), and the item is **"Poster gallery"**. The name is editable by the organiser, so it may read anything. |
| 24 | Keyword search matches partial strings (e.g. "ana" returns "analysis") | **Changed — refuted as written.** Search matches **title and author affiliation only**. Substring matching does work there ("oster" → "Poster"). Both "ana" and "analysis" returned 0 results despite "analysis" being a keyword on both posters and in one abstract. Full test matrix in `behaviour.md`. |
| 25 | Sort options include alphabetical and by submission ID / program code | **Confirmed** — **"A-Z titles"**, **"Z-A titles"**, **"Program codes"**. |

## Open questions — answered

**Q1 — Does the "In poster gallery" column only exist once a poster upload
question exists?**
**Yes, confirmed, both directions.** Unticking "Poster gallery upload" on the
question removed the column from the decisions table entirely — absent from the
COLUMNS list, not merely hidden — and emptied the gallery to "No posters found".
Re-ticking restored the column, the posters, and the previous per-submission
ticks. Support replies are correct. This also means the column cannot be found
by an organiser who has not yet built the question, which is the setup confusion
the tickets describe.

**Q2 — Is there a separate poster gallery URL that works before the programme is
published?**
**Partly.** The URL is
`https://virtual.oxfordabstracts.com/event/<eventId>/poster-gallery` (list) and
`…/poster-gallery/grid`. While the programme is **unpublished** it works for a
signed-in admin but sends an anonymous visitor to the Oxford Abstracts sign-in
page. Once **published** it works anonymously with no sign-in. So the support
answer "yes, there's a separate URL" is true but misleading if the organiser
intends to share it pre-publication.
**Also: the admin interface never offers this URL.** "Common program links"
lists only the programme link, before and after publishing.

**Q3 — Where is the Poster Gallery menu item switched on?**
**CONFERENCE → Program → Builder → DISPLAY → Program menu.** It is **ticked by
default**, sits ninth of ten items, and its name is an **editable text box** —
so a delegate may see it under a different label. Full default state in
`walkthrough.md` step 19.

**Q4 — Multi-page PDF, non-PDF, very large file — verbatim errors.**
Answered in `errors.md`. Headlines: non-PDF → `Invalid file type. Make sure the
file is one of these ( pdf )`; oversize → `The file is too large. Maximum upload
size is 10.0MB. The file you tried to upload was 11.5MB.`; **multi-page → no
error at all**.

**Q5 — Do the article's screenshots still match the interface?**
**No — expect substantial drift**, on the evidence of the label changes above
(claims 7, 9, 15, 23) and the whole "Poster questions" group changing contents
depending on state. I could not compare image-by-image because no screenshots
were captured this run; see "What limited the run".

## Findings not on the verification list

0. **"Accepted: Poster" does not put a submission in the poster gallery.** The
   decision dropdown offers `Pending`, `Accepted`, `Accepted: Oral`,
   **`Accepted: Poster`**, `Accepted: Invited`, `Rejected`, `Withdrawn`.
   Verified 31 Jul 2026: a submission set to **Accepted: Poster** with
   "In poster gallery" unticked **did not appear**, while one set to plain
   **Accepted** with the box ticked **did**. The decision sub-type and the
   gallery are entirely independent. This is the most inviting wrong turn in the
   whole feature — the option is named after the thing the organiser wants.
1. **The four other poster question types are hidden until a poster upload
   question exists.** Probably the mechanism behind a large share of "how do I
   set it up" tickets.
2. **"Show submission contents"** in Program access settings will, per its own
   help text, "disable access to all submission data including the poster
   gallery" — a third switch that can empty a correct gallery.
3. **Five programme access types** (Open access / All users - login required /
   Delegates and invited users / Only invited users / Access code) — the answer
   to the "who can view it" ticket theme.
4. **The inline poster viewer never loads the PDF** in this environment;
   reproduced in a clean browser. See `errors.md` for the caveats.
5. **"Your Conference Setup"** intercepts every direct link into the conference
   platform and Skip does not persist.
6. **Editing a question autosaves; creating one does not.**
7. **Files upload the instant they are chosen**, before the form is submitted,
   and the form then shows no filename.
