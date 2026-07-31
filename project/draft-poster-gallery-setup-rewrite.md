# DRAFT — rewrite of the poster gallery setup article

**Replaces the body of:**
`corpus/08-conference-platform/professional-conference-the-poster-gallery.md`

Drafted 31 July 2026 from the observed run in
`corpus-observed/poster-gallery/`. Sitting in `project/` so `build.py` cannot
pick it up (`CLAUDE.md` gotcha 9). A human promotes it.

## What changed and why

The old article describes the steps in the order an expert would do them. It
never states the **dependency structure**, which is what readers are actually
missing: one checkbox on one question brings the whole feature into existence,
and four conditions must all hold before a single poster appears.

`project/context-from-conversation.md` records that "poster gallery" is a search
term that **works** (1.0 average result clicks). People find this article and
still open 292 tickets a year, 59 of them asking how to set it up. So the
problem is what the article says, not whether it can be found — retitling and
synonyms will not help.

**Factual corrections folded in** (all observed 31 July 2026, evidence in
`corpus-observed/poster-gallery/META.md`):

| Old text | Corrected to |
|---|---|
| "Poster Questions" / "Poster Upload" | "Poster questions" / "Poster upload" |
| "Poster gallery upload" | "Poster gallery upload (1 allowed per event)" |
| "Include poster download button" | "Allow poster downloads" |
| "CREATE SELECTED QUESTION" | "CREATE QUESTION" |
| "Form & Setup" | "Form & setup" |
| "Posters ... can only be one page in length" | not enforced; only page 1 is displayed |
| "There is no file size limit" | 10MB by default, settable 0–500 |
| "checking this will automatically restrict any uploads to pdfs only" | true, but the "Allowed file extensions" box stays blank and appears to contradict it |
| keywords "enable searching by keyword" | keywords are a **filter**; the search box does not cover them |
| "Search using any term" | searches titles and author affiliations only |

**Structural changes:**

- New opening section stating the four conditions before any steps.
- New note that the other poster question types are invisible until the upload
  question exists — this is almost certainly why people think the feature is
  missing.
- New warning that "Accepted: Poster" is not the same as "In poster gallery".
- Bulk selection described properly ("BULK DECIDE" → "ADD TO POSTER GALLERY").
- Link out to the new "Why your poster gallery is empty" article.
- Delete the hand-written **"Skip to"** block. It survives in the markdown from
  the HubSpot import; `build.py` already drops it and generates the "On this
  page" box instead, so it is dead weight (`CLAUDE.md`: "No hand-written jump
  links").

**Before promoting, check:**

- **Plan gating is unverified.** The opening sentence claims Professional only.
  This run could not test it — no Basic or Abstract Management event was
  available. Keep the claim if `project/plan-feature-matrix.md` supports it, but
  it is not evidence from this run. See `corpus-observed/poster-gallery/by-plan.md`.
- **Screenshots.** Ten of the eleven current images date from 2021–2022 and the
  labels have demonstrably moved, so most are stale. None were captured this run
  (the tooling had no writable path). House rule is two or three per article at
  decision points — I would keep at most: the question-type picker, the
  "Question settings" block, and the decisions table column. The rest should go.
- The session and track filters are described from the old article, not
  observed — no sessions or tracks were assigned on the test event. Marked below.

---

```yaml
---
title: "Professional Conference - the poster gallery"
section: "08-conference-platform"
audience: organisers
plan: professional conference
source_url: https://help.oxfordabstracts.com/knowledge/setting-up-the-poster-gallery
last_reviewed: 2026-07-31
---
```

*`source_url` unchanged — it is provenance and must never be rewritten.*
*`last_reviewed` bumped, per the house convention on every edit.*

---

# Professional Conference - the poster gallery

## Display your accepted posters in a searchable gallery inside your conference programme. This feature is only available in the Professional Conference package.

The guidance below is for event administrators/ organisers. If you are an end
user (eg. submitter, reviewer, delegate etc), please click [here](https://oxfordabstracts.com/resources/contact-support/).

## What makes a poster appear

The poster gallery is not a setting you switch on. It is a view of your
submissions, and a poster only appears in it when **all four** of these are
true:

1. A question on your submission form has **Poster gallery upload (1 allowed per
   event)** ticked. This one question is what creates the gallery.
2. The submitter has uploaded a file to that question.
3. The submission has **In poster gallery** ticked in the decisions table.
4. The submission has been **Accepted**.

Most setup problems are one of these four being missed, and the gallery cannot
tell you which. If your gallery is empty, work through
[Why your poster gallery is empty](/08-conference-platform/why-your-poster-gallery-is-empty.html).

Please note: condition 1 comes first for a reason. Until a question is marked as
the poster gallery upload, the **In poster gallery** column does not exist in
your decisions table, and the other poster question types do not appear on your
submission form. If those things seem to be missing, this is why.

## Stage 1: add a poster upload question

Go to **[Event dashboard](/01-getting-started/event-dashboard.html) → Abstract
Management → Submissions → Form & setup → + QUESTION**

Note that **Decisions** also has a **Form & setup** page. You want the one under
**Submissions**.

Click **Poster upload** underneath **Poster questions**.

The question opens with sensible defaults already filled in, including the
description "Please upload a 1 page pdf file to include in the poster gallery".
Edit these as you wish (see [Question types](/02-submissions/submission-question-types.html)
for further guidance).

In **Question settings** at the bottom, check that:

- **Poster gallery upload (1 allowed per event)** is ticked. This is what makes
  the question feed the gallery. It is ticked for you when you arrive via
  **Poster upload**.
- **Allow poster downloads** is ticked if you want delegates to be able to
  download the PDF. It is ticked by default.
- **In program** is ticked if you want the posters visible in the programme. It
  is ticked by default.

Click **CREATE QUESTION** at the bottom of the page when you are done.

You can only have one poster gallery upload question per event.

### What submitters can upload

Ticking **Poster gallery upload** restricts submitters to PDF files. Their upload
button will read **CHOOSE FILE (.PDF ONLY)** and anything else is refused with
"Invalid file type. Make sure the file is one of these ( pdf )".

Please note: the **Allowed file extensions** box on the question stays blank, and
its help text says "Leave blank to allow all files". That is misleading on a
poster gallery question — PDF-only is enforced regardless.

The default maximum file size is **10MB**. To change it, put a number between 0
and 500 in **Max file size (MB)** on the question. A submitter who exceeds it
sees "The file is too large. Maximum upload size is 10.0MB. The file you tried
to upload was 11.5MB."

Remember: the one-page guidance in the default question description is advice to
your submitters, not a rule the system enforces. A multi-page PDF will upload
without any warning, and the gallery will show only its first page. If one page
matters to you, say so clearly in the question description and check the
submissions yourself.

## Stage 2: add other poster questions (optional)

Click **+ QUESTION** again. **Poster questions** now offers four more options
that were not there before — they only appear once a poster upload question
exists.

### Keywords

Keywords let delegates filter the gallery. Only one of these three can be added:

1. **Poster keyword - dropdown** — submitters choose one keyword from a list you
   create
2. **Poster keywords - multi-dropdown** — submitters choose several from your
   list
3. **Poster keywords - user selected** — submitters type their own

Please note: keywords power the **Keywords** filter in the gallery. They are not
matched by the gallery's search box.

### Presentation videos

**Poster presentation link** lets a submitter add a video to accompany their
poster. YouTube and Vimeo links are embedded directly in the gallery.

Choose the question you want, complete the details and click **CREATE QUESTION**.

Once you have added one upload question, one keyword question and one
presentation link, the **Poster questions** group disappears from the list.
That is expected — you have added everything the gallery supports.

## Stage 3: choose what information appears with the poster

Any other answer from the submission form can be shown beside the poster.

Click on a question in the form and look at its **Settings**. Tick **In poster
gallery** for each question whose answers you want displayed.

For more information, see [Question tags](/02-submissions/question-setting-tags).

## Stage 4: select the posters

Once submissions are in and reviewing is complete, go to
**Event dashboard → Abstract Management → Decisions → Table**.

For each submission you want in the gallery:

- set **Decision** to **Accepted**, and
- tick the **In poster gallery** checkbox.

Both are needed. Ticking the box on a submission that is still **Pending** does
nothing.

Please note: **Accepted: Poster** is a decision type, not a gallery setting.
Choosing it does not add a submission to the poster gallery — you still need the
**In poster gallery** box ticked.

If the **In poster gallery** column is not visible, click **COLUMNS** and tick
it under **Decision responses**.

### Doing this in bulk

Tick the checkboxes beside the submissions you want, then click **BULK DECIDE**.
Under **Additional decision options** you will find **ADD TO POSTER GALLERY**,
and a **REMOVE** beside it to take posters back out again.

See the [decisions table](/04-decisions/the-decisions-table.html) for more on
working in bulk.

## Stage 5: the gallery in your conference programme

The gallery appears as **Poster gallery** in the left-hand menu of your
programme.

To turn that menu item on or off, or rename it, go to **Event dashboard →
Conference → Program → Builder → DISPLAY → Program menu**. It is switched on by
default.

The gallery has its own address:

`https://virtual.oxfordabstracts.com/event/<your event ID>/poster-gallery`

Please note: your programme must be **published** before delegates can open that
link. Until it is, anyone who is not signed in to your event will be sent to a
login page instead. You will not see this yourself, because you are already
signed in.

### What delegates can do

- **Search** — matches poster titles and author affiliations. It does not search
  abstracts or keywords.
- **Sort** — A-Z titles, Z-A titles, or program codes.
- **Switch between list and grid view.**
- **Filter by topic or keyword** using the **Topics** and **Keywords**
  dropdowns.
- **Filter by session or track**, where posters have been assigned to them. To
  add posters to sessions, see [Attaching content to sessions](/08-conference-platform/attaching-content-to-sessions);
  for tracks, see [Setting up your program - configuration](/08-conference-platform/setting-up-your-program-configuration).
- **Click a poster** to see the abstract, authors, any keywords, any presentation
  video, and to download the PDF if you allowed downloads.

## Controlling who can see the gallery

The gallery follows your programme's access settings. Go to **Event dashboard →
Conference → Program → Builder → DISPLAY**, or click **User access** on the
Conference card of your dashboard.

**Access type** offers open access, login required, delegates and invited users,
invited users only, or an access code.

Please note: unticking **Show submission contents** on that screen hides all
submission data from your programme, including the entire poster gallery.
