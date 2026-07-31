---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Poster gallery — happy path, step by step

Walked 31 July 2026 on demo event 78206 ("Gareth Demo"), Professional Conference
package, signed in as an admin. Every label below is quoted verbatim from the
interface. Rendered case is given where the CSS uppercases a button
(`CREATE QUESTION` renders uppercase; its accessible name is `Create Question`).

No screenshots were saved to disk this run — the screenshot tool available in
this session returns images to the transcript but no writable file path. States
are described precisely instead. See `META.md` → "What limited the run".

---

## Stage 1 — create the poster upload question

**1.** Event dashboard → left nav **ABSTRACT MANAGEMENT** → **Submissions** →
**Form & setup**.
Lands on `/admin/events/<id>/app/edit-submission-form`, headed "Submission form".

- Note the nav label is **"Form & setup"** — lower-case "s". Both *Submissions*
  and *Decisions* have a child called "Form & setup"; they are different pages.

**2.** Top of the page carries a dark status button (**"FORM CLOSED"** on this
event) and five links: "PREVIEW AND TEST FORM", "COPY SUBMISSION LINK",
"HEADER AND FOOTER", "COMBINED WORD LIMITS", "SUBMISSION FEES". The red button
top right reads **"+ QUESTION"**.

**3.** Click **+ QUESTION**. A question-type picker replaces the form, headed by
a **"BACK TO FORM"** button. Groups and options, in order, **before** any poster
question exists:

| Group | Options |
|---|---|
| Standard questions | Program permission |
| **Poster questions** | **Poster upload** |
| Read-only questions | Page break, Text block |
| Text questions | Simple text, Formatted text, Single column list |
| Checkbox questions | Checkbox, Multiple checkboxes, Radio button |
| Dropdown questions | Dropdown, Dropdown with subcategories, Dropdown with multiple responses |
| Multimedia questions | Upload file, Upload image, Submitter link |
| Other questions | Email link, Date picker |

"Poster upload" is the **only** entry under "Poster questions" at this point.

**4.** Click **Poster upload**. The editor that opens is headed
**"File upload question"** — not "Poster upload". It arrives pre-filled:

- **Question name**: `Poster`
- **Description**: `Please upload a 1 page pdf file to include in the poster gallery`
- Red-bordered note: `Allowed file extensions - comma separated list of accepted
  file extensions (doc, docx, etc.). Leave blank to allow all files.`
  → field **"Allowed file extensions"**, **empty**
- Red-bordered note: `Max file size in MB - add a number between 0 and 500.
  Leave blank for the default 10MB`
  → field **"Max file size (MB)"**, **empty**
- **Question type**: `Optional` (selected), `Required`, `Read only`, `Hide`
- **Question settings**:
  - ☑ **"Allow poster downloads"**
  - ☑ **"Poster gallery upload (1 allowed per event)"**
  - ☐ "Show to reviewer"
  - ☐ "In abstract book"
  - ☑ "In program"
- Buttons: **"PREVIEW QUESTION"** (top right), **"CREATE QUESTION"** (bottom)

**5.** Click **CREATE QUESTION**. The question appears immediately at the
**end** of the form list, tagged with pills `Program` and `Poster upload`, with
a tick (✓) rather than an asterisk because it is Optional. It persists across a
page reload with no explicit save step.

## Stage 2 — the other poster questions appear

**6.** Click **+ QUESTION** again. The "Poster questions" group has **changed
completely**:

| Group | Options |
|---|---|
| **Poster questions** | **Poster keyword - dropdown**, **Poster keywords - multi-dropdown**, **Poster keywords - user selected**, **Poster presentation link** |

"Poster upload" is gone (one allowed per event); the other four are now visible
for the first time.

**7.** **Poster presentation link** → editor headed **"Submitter link"**,
pre-filled: name `Poster presentation link`, description
`Youtube and Vimeo links will appear as embedded videos`. Settings: ☑ "In poster
gallery", ☐ "Show to reviewer", ☐ "In abstract book". → **CREATE QUESTION**.

**8.** **Poster keywords - user selected** → editor headed **"Single column list
question"**, pre-filled: name `Poster keywords`, description `Enter keywords
that relate to your poster`, **"Number of inputs in list"** = `3`. Settings:
☑ **"In poster gallery (keywords always included)"**, ☑ "In program".
→ **CREATE QUESTION**.

**9.** Click **+ QUESTION** once more: the **entire "Poster questions" group has
disappeared** from the picker. One upload, one link and one keyword question is
the maximum.

## Stage 3 — choose what else shows beside the poster

**10.** Each existing question in the form list has a **Settings** list
containing a **"In poster gallery"** checkbox. Hovering it shows the tooltip
`Display responses to this question in the poster gallery`.

- Observed on this event: Abstract had it **on** and the abstract text appeared
  in the gallery detail panel; Presentation had it **off** and did not appear.

## Stage 4 — get a submission in

**11.** Dashboard → Submissions card → **"Submit on behalf"**
(`/stages/<stageId>/submissions/new?behalf=true`).

With the form closed, a modal appears first: **"Submissions closed"** /
`Submissions are currently closed for submitters. However, as an admin, you can
still create submissions.` / **OK**. Behind it a banner reads `Submissions are
currently closed so submitters will be unable to see this form. However
administrators can still create submissions`.

**12.** The poster question renders as:

> **Poster**
> Please upload a 1 page pdf file to include in the poster gallery
> [ ⬆ **CHOOSE FILE (.PDF ONLY)** ]

The underlying `<input type=file>` carries `accept=".pdf"`, **even though the
"Allowed file extensions" field was left blank**. Ticking "Poster gallery
upload" is what forces this.

**13.** Choosing a file uploads it **immediately**, before the form is
submitted. The control becomes:

> **DOWNLOAD UPLOADED FILE**
> [ ⬆ **REPLACE FILE (.PDF ONLY)** ]   **REMOVE**

No filename is shown anywhere on the form after upload.

**14.** Complete the remaining required questions and **Submit**.

## Stage 5 — select posters in the decisions table

**15.** **ABSTRACT MANAGEMENT → Decisions → Table**.

- With no submissions yet, this page shows only an empty state: **"No
  submissions"** / `Open your form from the dashboard using the toggles.` /
  **"Go to dashboard"**. No columns are rendered, so you cannot inspect the
  gallery column until at least one submission exists.

**16.** The **"In poster gallery"** column sits between "Decision last updated"
and "Final category". It is **shown by default**. In the **COLUMNS** dropdown it
lives under the group **"Decision responses"**.

- Searching `poster` in that dropdown's "Search columns" box also surfaces, under
  **"Submission responses"** and **unticked by default**: `Poster`,
  `Poster presentation link`, `Poster keywords`.

**17.** Tick **"In poster gallery"** on each row that should appear.

**18.** Set **Decision** to **"Accepted"** on those rows. The Decision cell
dropdown offers `Pending`, `Accepted` (with a submenu), `Rejected`, `Withdrawn`;
the bulk panel spells the submenu out as `ACCEPTED`, `ACCEPTED: ORAL`,
`ACCEPTED: POSTER`, `ACCEPTED: INVITED`.

- **Ticking without accepting shows nothing.** Verified: with both submissions
  ticked and both Pending, the gallery read "Showing 0 results". Accepting one
  made exactly that one appear.
- **"Accepted: Poster" is not a substitute for the tick.** Verified: submission
  2 set to *Accepted: Poster* with "In poster gallery" removed did **not**
  appear in the gallery, while submission 1 on plain *Accepted* with the tick
  did. Decision sub-type and gallery membership are independent.

**18a. Bulk selection.** Tick the row checkboxes (the header shows e.g.
"2 selected ×"), then **"BULK DECIDE"**. The panel is headed `Select submissions
and apply a decision to all of them` and lists the chosen submission ids. Under
**"Additional decision options"** it offers:

- **"ADD TO POSTER GALLERY"**  |  **REMOVE**
- **"ADD TO TITLES LISTING"**  |  **REMOVE**

Both directions tested: REMOVE emptied the gallery, ADD TO POSTER GALLERY
restored it. Confirmation is a toast reading `Bulk decision successfully made on
1 submission`; the panel header reads `1 submissions successfully accepted`
(not pluralised).

## Stage 6 — the gallery

**19.** The menu item is controlled at **CONFERENCE → Program → Builder →
DISPLAY → Program menu**. The panel explains: `This panel controls which pages
are accessible in the published program. Each menu item can be reordered by
clicking and dragging the sort icon, renamed through the text input, or disabled
by unchecking the checkbox.`

Default state of the ten items:

| Item | Default |
|---|---|
| Homepage | ☑ (locked, no checkbox) |
| Program | ☑ |
| Titles | ☑ |
| Participants | ☑ |
| Program codes | ☐ |
| Topics | ☐ |
| Presentation types | ☐ |
| Tracks | ☐ |
| **Poster gallery** | **☑** |
| Attendees | ☑ |

Each name is an editable text box, so a delegate may see this menu item under a
different name entirely.

**20.** The gallery lives at:

- list view — `https://virtual.oxfordabstracts.com/event/<eventId>/poster-gallery`
- grid view — `https://virtual.oxfordabstracts.com/event/<eventId>/poster-gallery/grid`
- one poster — `…/poster-gallery?current=<programCode>`

`…/poster-gallery/list` is **404 "Page not found."** — the list view is the bare
path.

**21.** Gallery toolbar, left to right: **"Search posters"** box, list-view and
grid-view toggle icons, sort dropdown (**"A-Z titles"** default, **"Z-A titles"**,
**"Program codes"**), **"Topics"** dropdown, **"Keywords"** dropdown, and a count
reading e.g. **"Showing 2 results"**.

- The Topics and Keywords dropdowns only render once there is at least one poster.

**22.** Grid card shows the PDF's **first page** as the thumbnail, the program
code, and the title. List view shows a small thumbnail, program code, title and
first author's name.

**23.** Clicking a poster opens a detail overlay:

- **"Close"** (top left), **"Original poster (PDF)"** download button (top right,
  present because "Allow poster downloads" was ticked)
- program code, title, `Topic: <n>`
- the poster viewer, with a **"Full screen"** button
- **Authors** — name, then `<Institution>, <City>, <Country>`
- **Abstract**
- **Poster presentation link** — YouTube/Vimeo URLs render as an embedded player
- **Poster keywords** — as pills
- **Comments** — "Add a comment…" / "Post comment"; anonymous visitors see
  **"Sign in to comment"**
- left/right chevrons step to the previous/next poster
