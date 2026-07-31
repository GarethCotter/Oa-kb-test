---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Screenshots — empty, and why

**No screenshots were captured to disk on the 31 July 2026 run.**

The browser tooling available in that session returned screenshots into the
conversation transcript but exposed no writable file path; its `save_to_disk`
option returned no location. Every state the brief asks to be pictured is
therefore described in prose in `walkthrough.md`, `behaviour.md` and
`errors.md`, with all labels and messages quoted verbatim.

This is a genuine shortfall against the brief on two counts:

1. The brief asks for a screenshot of every distinct state.
2. Ten of the eleven images in
   `corpus/08-conference-platform/professional-conference-the-poster-gallery.md`
   date from 2021–2022, and this run was meant to supply replacements. It has
   not. Given the label changes recorded in `META.md` (claims 7, 9, 15, 23) and
   the fact that the "Poster questions" group changes contents depending on
   state, those images are near-certainly stale — but that is inference from the
   label drift, not an image-by-image comparison.

## States to capture on the next run

In rough priority order — the first four are the ones the articles most need:

1. **+ QUESTION picker, before any poster question exists** — showing "Poster
   questions → Poster upload" as the only entry.
   `question-picker-poster-group-before.png`
2. **+ QUESTION picker, after the upload question exists** — showing the four
   keyword/link options that were previously invisible.
   `question-picker-poster-group-after.png`
3. **The "File upload question" editor** with its pre-filled defaults and the
   "Question settings" block.
   `poster-upload-question-defaults.png`
4. **Decisions table** with the "In poster gallery" column visible.
   `decisions-table-in-poster-gallery-column.png`
5. **DISPLAY → Program menu panel** with "Poster gallery" ticked.
   `program-menu-poster-gallery-enabled.png`
6. **Gallery grid**, populated. `gallery-grid-populated.png`
7. **Poster detail panel** with download button, abstract, keywords.
   `gallery-poster-detail.png`
8. **Empty gallery** — "Sorry, we couldn't find any posters" / "Clear filters".
   `gallery-empty-clear-filters.png`
9. **Upload error, wrong type** — "Invalid file type…".
   `poster-upload-invalid-file-type-error.png`
10. **Upload error, too large** — "The file is too large…".
    `poster-upload-file-too-large-error.png`
11. **Program access settings** showing "Show submission contents".
    `program-access-settings.png`

Name by state, not by sequence number, per the brief.
