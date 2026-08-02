---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Poster gallery — error and empty states

Every message below is quoted **verbatim**, including its own spacing and
grammar errors. File-upload failures are 19 of the 292 poster-gallery tickets in
the year to July 2026 and none of these messages appear anywhere in the current
articles.

---

## Upload: wrong file type

**Trigger** — attach anything that is not a PDF to a poster gallery upload
question. (Tested with a `.txt` file. The native file picker filters to PDFs via
`accept=".pdf"`, so a user normally hits this by drag-and-drop or by renaming a
file.)

**Modal:**

> **Sorry, something went wrong with the file upload**
>
> Invalid file type. Make sure the file is one of these ( pdf )
>
> **OK**

Note the spacing inside the brackets — `( pdf )` — which is how it renders.

**Fix** — upload a PDF. If the organiser wants other formats they must untick
"Poster gallery upload", which removes the question from the gallery entirely;
there is no way to have a gallery that accepts non-PDFs.

---

## Upload: file too large

**Trigger** — attach a PDF larger than the limit. Default limit is 10MB; it is
set per question in **"Max file size (MB)"**, blank meaning 10MB.

**Modal:**

> **Sorry, something went wrong with the file upload**
>
> The file is too large. Maximum upload size is 10.0MB. The file you tried to
> upload was 11.5MB.
>
> **OK**

The message substitutes both numbers, so the limit is always stated back to the
submitter. Sizes are reported in decimal MB — the 11.5MB file was 11,534,354
bytes.

**Fix** — compress the PDF, or raise "Max file size (MB)" on the question (0–500
accepted per the help text).

---

## Upload: multi-page PDF — *no error at all*

**Trigger** — attach a three-page PDF.

**Result: it uploads successfully.** No error, no warning, no truncation
message. The default question wording asks for "a 1 page pdf file" but nothing
enforces it. The gallery silently shows only page 1.

This is a **missing** error state rather than a bad one, and it is worth
documenting precisely because organisers assume the platform enforces the rule
they were told to state.

---

## Gallery is empty

**Trigger** — no submission satisfies all four conditions (poster upload
question ticked as gallery upload / file uploaded / "In poster gallery" ticked /
decision = Accepted).

**Empty state, no search term:**

> 🔍 Sorry, we couldn't find any posters   **Clear filters**

**Empty state, with a search term (e.g. `ana`):**

> 🔍 Sorry, we couldn't find any posters that match your search for "ana"
> **Clear filters**

**Empty state when the master switch is off:**

> Showing 0 results
> No posters found

**Why this message is a problem.** The first two offer **"Clear filters"** as the
only remedy, which points the reader at filtering when the real cause is almost
always a decision-status or setup problem. An organiser who has just ticked
twenty posters and sees "Clear filters" has been sent in exactly the wrong
direction.

---

## Programme not published, delegate not signed in

**Trigger** — send a delegate the gallery URL before publishing the programme.

**Result** — they land on the Oxford Abstracts sign-in page, headed with the
event name:

> **Gareth Demo**
> **Sign in to Oxford Abstracts**
> Email address / Password / … / Sign in

No message explains that the programme is unpublished. Publishing the programme
makes the same URL work anonymously.

---

## The "Your Conference Setup" wizard intercepts direct gallery links

**Trigger** — open any `virtual.oxfordabstracts.com/event/<id>/…` URL directly.

**Full-page interstitial, observed on every one of five separate page loads:**

> **Your Conference Setup**
>
> Welcome to Gareth Demo. We just need your help setting up a few last things
> and then you'll have access to the conference.
>
> 🕐 3 minutes  📅 Set timezone  🪪 Create your badge
>
> **Next**    **Skip**

Anonymous visitors get a shorter version — a **"Set your timezone"** step with
`Set your conference timezone preference`, an "Event timezone - UTC" dropdown
and **Save**.

**Skip does not stick.** It reappeared on each fresh page load in the same
session. Anyone following a poster gallery link meets this first.

---

## Inline poster viewer fails to load the PDF

**Trigger** — open any poster's detail panel.

**Result** — the viewer area shows a **loading spinner that never resolves**. The
"Full screen" button is present. The grid thumbnail renders correctly, so the
poster looks fine until you click it.

**Console error, verbatim:**

> `Error: UnknownErrorException: Failed to fetch`

**What I established:**

- Reproduced on **both** an extension-loaded signed-in Chrome and a clean
  browser with no extensions and no session, so it is not caused by an
  ad-blocker or by being signed in.
- A `fetch()` from `virtual.oxfordabstracts.com` to the poster's URL on
  `app.oxfordabstracts.com` throws `Failed to fetch`.
- The **thumbnail works**, because it is served from `/content-thumb/…` and
  loaded as an `<img>`, which is not subject to the same restriction.
- **Navigating directly to the poster URL downloads the file normally**, and the
  "Original poster (PDF)" button works. So the file is intact and served.

`[inferred]` — the cross-origin request for `/content/…` is missing the response
header the viewer needs; the failure is in the viewer, not the file. Not
confirmed against response headers.

**This needs confirming against a real customer event before it is written up as
product behaviour** — it may be specific to this demo event, to files uploaded
by an admin on someone's behalf, or to hand-generated PDFs. Both my test files
were minimal PDFs generated for this run.

---

## Confirmation email fails on "Submit on behalf"

**Trigger** — submit on behalf of an address that has bounced or been
suppressed (I used `test.submitter.one@example.com`).

**Modal:**

> **Sorry, something went wrong.**
>
> Please refresh the page or contact the Oxford Abstracts support team.
>
> You tried to send to recipient(s) that have been marked as inactive. Found
> inactive addresses: . Inactive recipients are ones that have generated a hard
> bounce, a spam complaint, or a manual suppression.
>
> **Ok**

Two things worth recording:

1. **The submission is still created.** Both submissions that produced this
   error appeared in the decisions table as Complete = Yes. Only the
   confirmation email failed. The wording ("Sorry, something went wrong. Please
   refresh the page") strongly implies the opposite, and an organiser will
   reasonably re-submit and create duplicates.
2. `Found inactive addresses: .` — the list of addresses renders **empty**, so
   the message never says which address was rejected.

Not a poster gallery bug, but it sits directly on the path an organiser takes to
put a test poster in the gallery, so they will hit it.

---

## Minor wording defects observed

| Where | Text | Note |
|---|---|---|
| Gallery toolbar | `Showing 1 results` | not pluralised |
| Upload type error | `( pdf )` | stray spaces inside brackets |
| Submit-on-behalf error | `Found inactive addresses: .` | empty list |
| `…/poster-gallery/list` | `404` / `Page not found.` / `Go to homepage` | plausible URL guess, but the list view is the bare path |
