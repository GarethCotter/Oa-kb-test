---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Poster gallery — settings and what they actually do

All observations 31 July 2026, demo event 78206, Professional Conference,
admin account. Anything not directly observed is tagged `[inferred]` or
`[untested]`.

---

## The "Poster gallery upload (1 allowed per event)" checkbox

This is the master switch for the whole feature.

- Found on any **file upload question**, under "Question settings".
- **Pre-ticked** when the question is created via **Poster questions → Poster
  upload**. Not ticked when created via **Multimedia questions → Upload file**.
  The two routes open the same editor ("File upload question") with different
  defaults.
- Ticking it forces the submitter-side file input to `accept=".pdf"` and makes
  the server reject non-PDFs — **even when the "Allowed file extensions" field
  is left blank**, whose own help text says "Leave blank to allow all files".
  The blank field is never updated to show `pdf`.
- **Only one per event.** Once one exists, "Poster upload" disappears from the
  +QUESTION picker.

**Toggling it, observed in both directions:**

| Ticked | Unticked |
|---|---|
| Question settings show: "Allow poster downloads", "Poster gallery upload (1 allowed per event)", "Show to reviewer", "In abstract book", "In program" | "Allow poster downloads" **disappears**; **"In poster gallery"** appears instead |
| "In poster gallery" column present in decisions table | Column **gone entirely** — absent from the COLUMNS list, not merely hidden |
| Gallery shows the selected posters | Gallery shows "Showing 0 results" / "No posters found"; Topics and Keywords filters disappear |
| Question tagged with pills `Program` `Poster upload` | Pill reduces to `Program` |

Re-ticking restores everything, **including the per-submission "In poster
gallery" ticks**, which survive the round trip. Uploaded files are not deleted.

## "Allow poster downloads"

- Only visible while "Poster gallery upload" is ticked.
- **Ticked by default.**
- When on, the poster detail panel carries an **"Original poster (PDF)"** button.
- `[untested]` what the panel looks like with it off.

## "Allowed file extensions" and "Max file size (MB)"

- Both **blank by default** on a poster upload question.
- Help text, verbatim: `Allowed file extensions - comma separated list of
  accepted file extensions (doc, docx, etc.). Leave blank to allow all files.`
  and `Max file size in MB - add a number between 0 and 500. Leave blank for the
  default 10MB`.
- **The default size limit is therefore 10MB, not "no limit".** An 11.5MB upload
  was rejected — see `errors.md`.
- The app reports sizes in **decimal MB**: an 11,534,354-byte file was described
  as "11.5MB". `[inferred]` from that arithmetic — so the practical ceiling is
  about 10,000,000 bytes rather than 10 MiB. Not separately confirmed.
- `[untested]` whether typing `pdf` into "Allowed file extensions" on a poster
  gallery question changes anything, and whether values above 500 are rejected.

## The one-page rule is not enforced

- The default description asks for "a 1 page pdf file".
- **A three-page PDF uploaded with no error, no warning and no truncation.**
- The gallery renders **only page 1** as both the grid thumbnail and the detail
  view. Nothing in the gallery indicates further pages exist.
- The full multi-page file is what the "Original poster (PDF)" button downloads.
- Consequence: an organiser cannot tell from the gallery that a submitter
  uploaded a 20-page paper instead of a poster.

## Save behaviour

- **Creating** a question needs an explicit **"CREATE QUESTION"** click.
- **Editing** an existing question **autosaves** — a "Saving…" status appears and
  there is no Save/Update button, only "Preview question", "Back to form" and
  "Delete question".
- **Decisions table** checkboxes and Decision dropdowns save on click, no
  confirm step.
- **Program menu** checkboxes and names save on change; the panel has only a
  "CLOSE" button.
- Files upload to the server **the moment they are chosen**, before the
  submission is submitted.

## The gallery search box — what it actually matches

Tested against two posters whose titles were "Test Poster One"/"Test Poster
Two", abstracts containing "Abstract About Nothing" and "analysis", keywords
`nothing, analysis, testing, posters`, and authors "Test Submitter One/Two" at
"Institute of Nothing, Testville, United Kingdom".

| Query | Where that string lives | Results |
|---|---|---|
| `Post` | title (prefix) | 2 |
| `oster` | title (mid-word) | 2 |
| `Poster One` | title | 1 |
| `Institute` | author affiliation — institution | 2 |
| `Testville` | author affiliation — city | 2 |
| `Submitter` | author surname | **0** |
| `Second` | abstract of poster 2 | **0** |
| `Abstract About` | both abstracts | **0** |
| `analysis` | keyword on both, and abstract of poster 2 | **0** |
| `ana` | substring of the keyword "analysis" | **0** |
| `testing` | keyword on poster 1 | **0** |

**Conclusion: the search box matches the poster title and the authors'
affiliation (institution and city) only.** It does substring matching within
those fields, including mid-word. It does **not** match abstracts, poster
keywords, or author names.

This directly contradicts the current article's example that searching "ana"
returns "analysis".

## Keyword filtering does work — via the dropdown

- The **"Keywords"** dropdown lists every keyword any poster submitted, as
  checkboxes (observed: `analysis`, `nothing`, `posters`, `testing`).
- Ticking `testing` (submitted on poster 1 only) correctly narrowed to
  "Showing 1 results" / Test Poster One.
- So keywords are a **filter**, not a **search term**. Both the article and, on
  this evidence, most users would expect the search box to cover them.

## Sort and view

- Sort dropdown: **"A-Z titles"** (default, ticked), **"Z-A titles"**,
  **"Program codes"**. Sort is reflected in the URL as `?sort=titles`.
- **Grid** and **list** toggle icons. Grid is `…/poster-gallery/grid`; list is
  the bare `…/poster-gallery`. `…/poster-gallery/list` returns 404.
- **"Topics"** and **"Keywords"** filter dropdowns.
- **No "session" or "track" filter appeared** on this event. No sessions or
  tracks were assigned to the two test posters, so `[untested]` whether those
  filters appear when they are.

## Who can see the gallery

Set at **CONFERENCE → Program → Builder → DISPLAY**, and at the dashboard
Conference card → **User access** (`/program-builder/access-code`), headed
**"Program access settings"**.

- **"Access type"** offers five options: **"Open access"** (the default on this
  event), **"All users - login required"**, **"Delegates and invited users"**,
  **"Only invited users"**, **"Access code"**.
- With Open access the panel states: `All areas of the program are publicly
  available.` and `Note: networking and comment features require login.`
- Three "Configure access" checkboxes, **all ticked by default**:
  - **"Show session download links"** — `Allow authorised users to download a PDF
    version of the session with attached submission information.`
  - **"Show submission contents"** — `Check box to enable access to all
    submission data.` / **`If this box is unchecked it will disable access to all
    submission data including the poster gallery.`**
  - **"Show submission Ids"** — `Toggle the visibility of submission program
    codes and Ids in the program.`
- `[untested]` the four non-open access types, and the effect of actually
  unticking "Show submission contents" — I did not change the event's access
  settings. The quoted help text is the product's own claim, not an observation.

## Published vs unpublished

Programme publish state is the **UNPUBLISHED / PUBLISHED** dropdown at the top
left of the programme builder.

| | Admin, signed in | Anonymous, not signed in |
|---|---|---|
| **UNPUBLISHED** | gallery loads and shows posters | redirected to the Oxford Abstracts **sign-in page** |
| **PUBLISHED** | gallery loads and shows posters | **gallery loads, posters visible, no sign-in required** |

So there *is* a gallery URL that works before the programme is published — but
only for someone who is already signed in with access to the event. Sharing it
with delegates before publishing sends them to a login screen.

**The admin interface never offers this URL.** "Common program links" (programme
builder → status dropdown → "Common links") is headed `Share or embed the links
to your published program below.` and lists exactly one link, the programme
(`…/event/<id>/program`) — both before and after publishing. There is no poster
gallery link and no QR code for it.
