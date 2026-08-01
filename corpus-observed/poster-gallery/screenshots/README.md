---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Screenshots — capture status

The 31 July 2026 run produced no images: the browser extension available in that
session could return screenshots to the transcript but not save files. **Solved
1 August 2026** with `scripts/capture-poster-gallery.py` — Playwright driving the
installed Chrome at a fixed 1440×900 viewport, element-anchored crops, WebP
output into this folder.

```bash
py scripts/capture-poster-gallery.py            # public shots (no sign-in)
py scripts/capture-poster-gallery.py --login    # one-time sign-in, saves session
py scripts/capture-poster-gallery.py --admin    # admin shots (needs the session)
```

Because the shots are anchored to element selectors rather than pixel
coordinates, re-running the script after a UI change photographs the new state
of the same controls — captures are reproducible and refreshable.

## Status

| Shot | State | How |
|---|---|---|
| `gallery-grid-populated.webp` | **captured 2026-08-01** | public |
| `gallery-list-view.webp` | **captured 2026-08-01** | public |
| `gallery-empty-clear-filters.webp` | **captured 2026-08-01** | public (search `zzzz`; list view says "No posters found", grid view says "Sorry, we couldn't find any posters") |
| `gallery-poster-detail.webp` | **captured 2026-08-01** | public. Shows the PDF viewer spinner — that is the app's real current behaviour (see `errors.md`), so the image is honest; recapture when the viewer is fixed |
| `decisions-table-in-poster-gallery-column` | awaiting `--login` | admin |
| `question-picker-poster-group-after` | awaiting `--login` | admin |
| `poster-upload-question-defaults` | awaiting `--login` | admin |
| `program-menu-poster-gallery-enabled` | awaiting `--login` | admin |
| `program-access-settings` | awaiting `--login` | admin |
| `question-picker-poster-group-before` | next exploration run | needs the poster questions temporarily deleted — destructive, do deliberately |
| `poster-upload-invalid-file-type-error` | next exploration run | needs a scripted wrong upload on the submission form (admin) |
| `poster-upload-file-too-large-error` | next exploration run | as above |

## Notes for whoever captures next

- The one-time sign-in: `--login` opens a visible window; sign in yourself
  (the script never touches credentials), press Enter, and the session is
  saved to `%USERPROFILE%\.oa-capture-state.json` — outside the repo on
  purpose, since it holds live cookies. Never commit it.
- Name by state, not sequence number, per the exploration brief.
- Keep the 1440×900 viewport so images stay comparable between runs.
- The timezone dialog intercepts first load of a fresh profile; the script
  dismisses it.
