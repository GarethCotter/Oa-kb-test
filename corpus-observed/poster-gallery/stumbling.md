---
feature: poster-gallery
observed: true
app_version: unknown
explored: 2026-07-31
plan: professional conference
---

# Poster gallery — where a first-timer gets stuck

The reader this matters for is the one in `CLAUDE.md`: a conference organiser,
often middle-aged, not especially confident with software, arriving mid-task and
mildly stressed. Ordered roughly by how much support volume each is likely to
account for.

Each entry records where **I** hesitated or was wrong, since the brief's test is
that if the exploring agent had to hunt for something, the persona is lost.

---

## 1. There is no "Poster gallery" anywhere in the admin navigation

**What happens.** An organiser told to "set up the poster gallery" opens the
left-hand menu and reads: Dashboard, Event setup, EMAILS, ABSTRACT MANAGEMENT,
SPEAKER MANAGEMENT, WEBSITE BUILDER, REGISTRATION, CONFERENCE, CERTIFICATES,
ADVANCED, SOAA, PREMIUM TRIALS. Expanding CONFERENCE gives Program (Builder,
Sessions, Bookings, Zoom) and Advanced tools (Homepage, Exhibitors, Networking,
Comment moderation).

**Nothing is called Poster gallery.** The feature is created by a *question on
the submission form*, two sections away, under ABSTRACT MANAGEMENT.

This is the single confusion the ticket analysis identifies — "people do not
connect the gallery to a question on the submission form" — and the navigation
actively causes it. I checked every branch of the CONFERENCE menu before going
back to the submission form.

## 2. The keyword and video questions are invisible until you've done step one

**What happens.** An organiser plans the form, opens **+ QUESTION**, and looks
for the poster options they were told about. Under "Poster questions" there is
exactly one: **Poster upload**. No keywords, no presentation link.

Only after creating the upload question do the other four appear. Nothing says
so. Someone comparing the picker against the current article — which describes
keyword options and a video question — will reasonably conclude their package
doesn't include them, or that the article is for a different product.

This is a strong candidate for the actual mechanism behind "how do I set it up"
tickets that mention keywords or videos.

## 3. "In poster gallery" doesn't exist yet, and the empty decisions table hides that

**What happens.** An organiser goes to **Decisions → Table** to find the
"In poster gallery" column before building the form. If there are no submissions
yet, the page shows only "No submissions" — **no columns at all**. If there are
submissions but no poster upload question, the column is genuinely absent, and
absent from the COLUMNS list too, so searching for it finds nothing.

Either way the organiser sees no evidence the feature exists, and no clue that
the cause is a missing question on a different page.

## 4. Ticking "In poster gallery" appears to do nothing

**What happens.** The organiser finds the column, ticks their posters, opens the
gallery, and sees **"Sorry, we couldn't find any posters"** with a **"Clear
filters"** button.

They have not made a mistake in the gallery. The submissions are still
**Pending** — they must also be **Accepted**. But the empty state's only
suggested remedy is clearing filters, which points at the wrong thing entirely.

This is the most expensive combination on the list: a correct action, a
plausible-looking result, and an error message that misdirects.

## 4a. "Accepted: Poster" looks exactly like the right answer, and isn't

**What happens.** The organiser opens the Decision dropdown and sees
**"Accepted: Poster"**. They are setting up a poster gallery. They choose it.

It does nothing for the gallery. Verified: a submission on *Accepted: Poster*
without the "In poster gallery" tick does **not** appear; one on plain
*Accepted* with the tick does.

This is worse than a missing feature, because the organiser has taken a
deliberate, confident action with a name that matches their goal, and got no
feedback that it was the wrong lever. Anyone who does this and then hits the
"Clear filters" empty state (item 4) has been misled twice in a row.

## 5. The "1 page pdf" instruction is advice, not a rule

**What happens.** The default question wording says "Please upload a 1 page pdf
file". The organiser reasonably assumes the platform enforces it and doesn't
police submissions.

A submitter uploads a 12-page paper. **It is accepted silently.** The gallery
thumbnail shows page 1, so it looks correct in the gallery too. The organiser
discovers the problem at the conference, or never.

Compounding it: the gallery **shows no filename and no page count** anywhere, so
there is no way to audit this short of downloading every poster.

## 6. The "Allowed file extensions" box says the opposite of what happens

**What happens.** The organiser reads, on the poster upload question:

> Allowed file extensions - comma separated list of accepted file extensions
> (doc, docx, etc.). Leave blank to allow all files.

…and the box is **blank**. So they believe all file types are allowed, and may
tell submitters so.

In fact ticking "Poster gallery upload" silently forces PDF-only, and submitters
get "Invalid file type. Make sure the file is one of these ( pdf )". The
organiser's own screen never shows `pdf` anywhere in that field.

I read this field, concluded all files were allowed, and was wrong — the
contradiction is not subtle in effect, only in presentation.

## 7. The gallery URL is never given to you

**What happens.** The organiser wants to email delegates a link straight to the
posters. They go to **Common links** — the obvious place, headed "Share or embed
the links to your published program below" — and find **one** link, to the
programme. There is no poster gallery link and no QR code for one, before or
after publishing.

The URL exists (`…/event/<id>/poster-gallery`) but you can only get it by
navigating there and copying the address bar. `…/poster-gallery/list` — a
reasonable guess for the list view — is a 404.

## 8. Sharing the link before publishing sends delegates to a login screen

**What happens.** The organiser opens the gallery themselves, copies the URL,
and sends it out before publishing the programme. It works perfectly for them
(they are signed in). Delegates get the **Oxford Abstracts sign-in page** with no
explanation.

The failure is invisible to the person who caused it. Publishing fixes it, but
nothing connects the two.

## 9. "Your Conference Setup" gets in the way of every link you send

**What happens.** Anyone following a link into the conference platform meets a
full-page **"Your Conference Setup"** wizard — timezone, badge — before seeing
anything. Skipping it does not persist; it reappeared on every fresh page load
in my session.

A delegate sent "here are the posters" gets an onboarding form instead. Some
will assume they're in the wrong place and close the tab.

## 10. Two different pages are both called "Form & setup"

**What happens.** Under ABSTRACT MANAGEMENT, both **Submissions** and
**Decisions** have a child called "Form & setup". The poster question is on the
Submissions one. An organiser working in the decisions area and told to "go to
Form & setup" has an even chance of landing in the wrong builder.

## 11. The error when nothing is wrong

**What happens.** Submitting a test poster on someone's behalf produces
**"Sorry, something went wrong. Please refresh the page or contact the Oxford
Abstracts support team."** — but the submission *was* created.

An organiser testing their own setup will believe it failed and try again,
creating duplicates, and may open a ticket about a submission process that is
working.

## 12. The poster viewer spins forever

**What happens.** The gallery grid looks right — thumbnails render. Click a
poster and the viewer panel shows a spinner that never resolves. The download
button still works.

Observed on every poster, in two different browsers, signed in and anonymous.
Flagged in `errors.md` as needing confirmation on a real customer event before
being written up as product behaviour — but if it reproduces there, it is the
most visible fault in the feature and no article mentions it.

## 13. Search doesn't find what's on the screen

**What happens.** A delegate looking at a poster tagged `analysis` types
"analysis" into "Search posters" and gets nothing. The keyword is visible on the
poster in front of them.

Keywords are filterable, but only from the separate **Keywords** dropdown. The
search box covers titles and author affiliations only. Nothing labels either
control to say so.
