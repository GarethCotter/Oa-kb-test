---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Screenshots — capture status

The 31 July run produced no images: the browser extension could return
screenshots to the transcript but not save files. **Capture now works**, via
`scripts/capture-poster-gallery.py` — Playwright driving the installed Chrome at
a fixed 1440×900 viewport, element-anchored crops, WebP into this folder.

```bash
py scripts/capture-poster-gallery.py            # public shots - fully automatic
py scripts/capture-poster-gallery.py --admin    # admin shots - sign in when the window opens
```

Because shots are anchored to element selectors rather than pixel coordinates,
re-running after a UI change photographs the new state of the same controls.
Captures are reproducible and refreshable — which is the property the stale-image
backlog needs.

## Status

| Shot | State |
|---|---|
| `gallery-grid-populated.webp` | **captured 2026-08-01** |
| `gallery-list-view.webp` | **captured 2026-08-01** |
| `gallery-empty-clear-filters.webp` | **captured 2026-08-01** |
| `gallery-poster-detail.webp` | **captured 2026-08-01** — shows the PDF viewer spinner, which is the app's real behaviour (see `errors.md`); recapture when fixed |
| `decisions-table-in-poster-gallery-column` | scripted, needs `--admin` |
| `question-picker-poster-group-after` | scripted, needs `--admin` |
| `poster-upload-question-defaults` | scripted, needs `--admin` |
| `program-menu-poster-gallery-enabled` | scripted, needs `--admin` |
| `program-access-settings` | scripted, needs `--admin` |
| `question-picker-poster-group-before` | next exploration run — needs the poster questions temporarily deleted (destructive) |
| `poster-upload-invalid-file-type-error` | next exploration run — needs a scripted wrong upload |
| `poster-upload-file-too-large-error` | next exploration run — needs a scripted wrong upload |

## Admin shots need you at the keyboard

**The signed-in session cannot be saved and replayed.** Established 1 August 2026
after three failed attempts, recorded here so nobody burns another afternoon:

1. Playwright's `storage_state` export, taken straight after a real sign-in, held
   only `anon_user_id` and `_dd_s` — no auth token. Admin pages bounced to `/auth`.
2. A full persistent Chrome profile failed identically, in headless **and**
   headful runs. A fresh page on that profile showed `localStorage` completely
   empty, no auth cookie on `app.oxfordabstracts.com`, and a `code_verifier`
   cookie — an OAuth/PKCE flow whose access token lives in memory in the running
   page, and whose identity-provider session does not survive a browser restart
   in a clean automation profile.
3. So there is no artefact to save. `--admin` signs in and captures in the
   **same** browser session. Budget one sign-in per admin capture run.

**Also learned the hard way:** do not detect sign-in by watching the URL. The app
briefly shows an `/events` URL while bouncing through auth, and a URL-based
detector matched that transient, reported success, and ran five captures against
the sign-in page. Detection is now by probe — wait for the sign-in screen to stay
gone for six seconds, then load a real admin page and confirm it is not bounced.

## Running the admin capture

Open PowerShell in the repo and run:

```bash
py scripts/capture-poster-gallery.py --admin
```

A Chrome window opens on the sign-in page. Sign in; the five captures then run by
themselves in that window, which closes when done. Ten-minute window, and it
prints what it is doing.

Each shot is independent — one failure reports and the run carries on — and any
that fails still saves a `FAILED-<name>.webp` of whatever was on screen, so a bad
selector can be diagnosed without asking you to sign in again.

## Conventions for whoever captures next

- Name by state, not sequence number, per the exploration brief.
- Keep the 1440×900 viewport so images stay comparable between runs.
- The conference platform shows a timezone dialog on first load; the script
  dismisses it.
- Look at every capture. The empty-state shot was initially wrong because the
  wait fired on the "Clear filters" chip, which appears while the debounced
  search is still running with the old results on screen. It now waits for
  "Showing 0 results". A file appearing is not evidence it is the right file.
