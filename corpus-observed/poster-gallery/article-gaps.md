---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Poster gallery — article gap list

Proposed articles and edits, each with the evidence behind it. A human decides
what gets written; nothing here goes into `corpus/` or `corpus-internal/`
without being checked.

## The framing that matters

`project/context-from-conversation.md` records that **"poster gallery" is one of
the search terms that *works*** — 1.0 average result clicks, alongside invoice
and api, against a baseline where a third of searches end with no click.

So people **find** `professional-conference-the-poster-gallery.md`. And they open
292 tickets anyway, 59 of which ask how to set it up.

**This is not a findability problem. It is a content problem.** The article is
retrieved and does not answer the question. That changes the remedy: retitling
and synonyms will do nothing here; the article has to say different things.

The specific reason it doesn't answer them is now identifiable. The article
describes the steps in the order an expert would do them. It never states the
*dependency structure* — that one checkbox on one question is what brings the
entire feature into existence, and that four separate conditions must all hold
before a single poster appears. A reader who does the steps out of order sees an
interface with no poster features in it and no explanation.

---

## Priority 1 — rewrite the setup article around the four conditions

**Edit:** `corpus/08-conference-platform/professional-conference-the-poster-gallery.md`

**Scope:** Open with the four conditions a poster must satisfy to appear, as a
checklist, before any step-by-step. Then the steps, in the order the interface
forces. Add the two switches that can empty a working gallery.

**Evidence:**
- 59 of 147 question sentences in 292 poster gallery tickets are "how do I set
  it up" — three times the next theme.
- The confusion named in the ticket analysis is precisely "people do not connect
  the gallery to a question on the submission form".
- Observed: with a poster question and both submissions ticked but **Pending**,
  the gallery reads "Showing 0 results". Accepting one made exactly one appear.
  Ticking is not sufficient and nothing on screen says so.
- Observed: unticking "Poster gallery upload" removes the "In poster gallery"
  column from the decisions table **entirely** and empties the gallery.
- The article is already found by search (1.0 result clicks) and tickets
  continue — so the fix must be content, not title.

**Also fix, in the same pass — every one of these is wrong or renamed:**

| Currently says | Should say |
|---|---|
| "Poster Questions" heading, "Poster Upload" option | **"Poster questions"**, **"Poster upload"** |
| checkbox "Poster gallery upload" | **"Poster gallery upload (1 allowed per event)"** |
| checkbox "Include poster download button" | **"Allow poster downloads"** |
| button "CREATE SELECTED QUESTION" | **"CREATE QUESTION"** |
| "Form & Setup" | **"Form & setup"** — and note *Decisions* has one too |
| "no file size limit" | **10MB by default**, settable 0–500 |
| "posters can only be one page" | **not enforced** — see Priority 3 |

---

## Priority 2 — new article: "Why your poster gallery is empty"

**Title:** Why your poster gallery is empty
**Scope:** One page. Six numbered causes, each with the symptom, where to look,
and what to change. Written in the reader's voice, per the house convention for
troubleshooting titles.

The six causes, in the order they are likely:

1. The submissions are ticked but still **Pending** — they must be **Accepted**.
   And **"Accepted: Poster" is not the same as ticking "In poster gallery"** —
   it has no effect on the gallery at all.
2. No file upload question has **"Poster gallery upload (1 allowed per event)"**
   ticked — so the "In poster gallery" column does not exist at all.
3. Submitters didn't upload a file.
4. **DISPLAY → Program menu → "Poster gallery"** has been unticked.
5. **Program access settings → "Show submission contents"** has been unticked —
   its own help text says this "will disable access to all submission data
   including the poster gallery".
6. A filter is still applied in the gallery itself.

**Evidence:**
- Causes 1 and 2 both observed directly and reversibly on event 78206.
- The empty state reads **"Sorry, we couldn't find any posters"** with **"Clear
  filters"** as its only remedy — i.e. it advertises cause 6, the least likely,
  and says nothing about causes 1–5.
- Cause 5 is quoted from the product's own help text and is otherwise
  undiscoverable; `[untested]` by direct experiment (I did not change the demo
  event's access settings).

This is the highest-value *new* article on the list: it targets the exact
failure the empty state misdirects people away from.

---

## Priority 3 — new article or prominent section: poster file rules

**Title:** What file can submitters upload as a poster?
**Scope:** PDF only and why; the 10MB default and how to change it; the one-page
rule being advisory; the exact error messages.

**Evidence:**
- **19 of 292** poster gallery tickets are file format and size — the second
  biggest theme.
- Observed: a **3-page PDF uploaded with no error, no warning**. The gallery
  shows page 1 only. The default question wording asks for "1 page" but nothing
  enforces it, and the gallery shows no page count or filename, so an organiser
  cannot audit it.
- Observed: the **"Allowed file extensions"** field stays blank, and its help
  text says "Leave blank to allow all files" — while ticking "Poster gallery
  upload" silently forces PDF-only. The interface contradicts the behaviour.
- Observed: default size limit is **10MB**, not "no limit" as the article says.

**The error messages belong in the article verbatim**, because `CLAUDE.md`'s own
rule is that a paraphrased error is useless for search matching, and these are
what a stuck submitter will paste into the search box:

> Invalid file type. Make sure the file is one of these ( pdf )

> The file is too large. Maximum upload size is 10.0MB. The file you tried to
> upload was 11.5MB.

---

## Priority 4 — new article: sharing the gallery and controlling who sees it

**Title:** Sharing your poster gallery (and who can see it)
**Scope:** The URL, the publish requirement, and the five access types.

**Evidence:**
- **9 of 292** tickets are "who can view it and for how long".
- Observed: the gallery URL is `…/event/<eventId>/poster-gallery` (list) and
  `…/poster-gallery/grid`. **The admin interface never gives it to you** —
  "Common program links", headed "Share or embed the links to your published
  program below", lists only the programme link, before and after publishing.
- Observed: unpublished + anonymous → **Oxford Abstracts sign-in page**;
  published + anonymous → gallery visible, no sign-in. The organiser cannot see
  this failure because they are signed in.
- Observed: five access types — Open access / All users - login required /
  Delegates and invited users / Only invited users / Access code. `[untested]`
  beyond Open access.

---

## Priority 5 — expand the attendee-side article

**Edit:** `corpus/14-for-attendees-exhibitors/exploring-the-poster-gallery.md`

**Scope:** Correct the search claim, correct the navigation description, add the
Keywords/Topics filters.

**Evidence:**
- Observed test matrix (full version in `behaviour.md`): the search box matches
  **title and author affiliation only**. `analysis` and `ana` both returned 0
  results despite "analysis" being a keyword on both posters and in one abstract;
  `Institute` and `Testville` (affiliation) returned 2; `Submitter` (author name)
  returned 0.
- **The article's worked example — "ana" returns "analysis" — does not work.**
  That is the kind of error that destroys a reader's trust in the whole page,
  because they will try it.
- Keywords are filterable, from a separate **"Keywords"** dropdown. Say so, and
  say the search box doesn't cover them.
- Navigation is a **persistent left sidebar**, not "the menu icon top left", and
  the item is **"Poster gallery"** — but the organiser can rename it, so the
  article should say "the poster gallery item, which your organiser may have
  renamed".
- Sort options are exactly **"A-Z titles"**, **"Z-A titles"**, **"Program codes"**.

---

## Priority 6 — audio/video posters

**Scope:** Cover **"Poster presentation link"** properly — that it is a separate
question type, that it only appears in the +QUESTION picker *after* a poster
upload question exists, and that YouTube and Vimeo URLs render as embedded
players in the gallery.

**Evidence:**
- **15 of 292** tickets are audio/video posters.
- Observed: the type exists, its editor is headed "Submitter link", its default
  description is `Youtube and Vimeo links will appear as embedded videos`, and a
  YouTube URL did render as an embedded player in the gallery detail panel.
- Observed: it is **invisible in the picker until a poster upload question
  exists** — a likely reason people ask whether the feature exists at all.

---

## Priority 7 — confirm plan gating

**Edit:** `project/plan-feature-matrix.md` and the `plan:` frontmatter on the two
poster articles.

**Evidence:**
- **10 of 292** tickets are cost and package.
- `CLAUDE.md`'s outstanding-work list already includes "confirming plan gating on
  17 articles"; this is one of them.
- This run **could not verify** the Professional-only claim — only a Professional
  event was available. See `by-plan.md` for the four checks that would settle it.

---

## Not article gaps — product issues to route elsewhere

These are not fixed by writing anything. Passing them to support/product is
likely worth more than documenting them.

1. **The inline poster viewer never renders the PDF.** Spinner forever, console
   error `UnknownErrorException: Failed to fetch`, reproduced in a clean browser
   with no extensions and no session. Thumbnails and downloads work.
   **Confirm on a real customer event before acting** — both test files were
   minimal hand-generated PDFs. If it reproduces there, it is the most visible
   fault in the feature.
2. **The empty-gallery message misdirects.** "Clear filters" is offered as the
   remedy when the cause is nearly always decision status or setup.
3. **"Your Conference Setup" intercepts every direct link** into the conference
   platform, and Skip does not persist across page loads. Delegates sent a
   poster link get an onboarding wizard.
4. **The "Allowed file extensions" field contradicts actual behaviour** on a
   poster gallery question.
5. **Submit-on-behalf reports "Sorry, something went wrong" when the submission
   succeeded** — only the confirmation email failed, and the address list in the
   message renders empty (`Found inactive addresses: .`). Organisers testing
   their own setup will create duplicates.
6. **Cosmetic:** `Showing 1 results`; `( pdf )` spacing; `…/poster-gallery/list`
   404s while `…/poster-gallery/grid` works.

---

## Suggested internal notes (`corpus-internal/`)

Per `CLAUDE.md`: one note per problem, keywords in the first 160 characters, the
title *is* the answer. Candidates, each answering a real ticket question in a
sentence or two:

- **"Why is the In poster gallery column missing from my decisions table?"** —
  because no submission form question has "Poster gallery upload (1 allowed per
  event)" ticked.
- **"Do posters have to be one page?"** — the platform does not enforce it; only
  page one is shown in the gallery.
- **"What is the maximum poster file size?"** — 10MB by default, settable 0–500MB
  per question.
- **"Can submitters upload a Word document or an image as a poster?"** — no, PDF
  only once "Poster gallery upload" is ticked.
- **"What is the poster gallery URL?"** — `…/event/<eventId>/poster-gallery`; the
  programme must be published for delegates to reach it without signing in.

Each of these is currently the kind of fact that would otherwise be appended to
an omnibus file — which `CLAUDE.md` records as measurably unfindable (4 of 14
test questions reached, versus 2 of 2 when split into their own notes).
