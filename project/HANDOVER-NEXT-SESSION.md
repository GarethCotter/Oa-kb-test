# Handover — next session

*Written 3 August 2026. Everything below is committed and pushed to `main`.
Working tree clean. Replaces the 1 August handover, which described a branch that
has since been merged.*

Read `CLAUDE.md` first — it is the house rules and it is accurate. This file covers
where things stand and what is open.

---

## State

- **On `main`, and `main` is live.** `poster-gallery-exploration` was merged on
  3 August after a clean test-merge, a rebuild and a full check run. That branch is
  now history; do not branch from it again.
- `python build.py` then `python scripts/checks.py` after any change. Python is
  `py` on this machine, not `python`. **Twelve** checks pass right now.
- Vercel deploys from `main` automatically, about 30–60 seconds behind a push.

## Start here on the next session

**The Loom transcript project.** Read `project/loom-transcript-mining-brief.md`
before doing anything — it is complete and still accurate, and it names the two
things that are easy to get wrong.

Phase 1 is about fifteen minutes of Gareth's time and it is a **decision gate, not
a build**: sign in to Loom, open one video, watch the network traffic to see
whether the transcript arrives as JSON from an endpoint, and pull three transcripts
as samples. Then **read them**.

The whole project rests on one untested assumption: that screen-narration
transcripts are usable as prose. If they turn out to be *"click here, then this
bit, then pop that in there"*, the project pivots to topic mining only — still
worth doing, but a fraction of the effort and a different shape. Do not build a
500-video scraper before reading three transcripts.

Two things to check before writing any scraper at all: whether the paid workspace
offers a **bulk export**, and whether Atlassian (who bought Loom) now exposes an
**API**. Half an hour that could remove the need for Playwright entirely.

Raw transcripts live at `Desktop\Claude\oa-loom-transcripts\`, **outside the repo,
permanently** — every one is a 1:1 customer response and will name customers,
events and possibly payment data. Same rule as `oa-support-replies/`.

Playwright is already proven on this machine against an authenticated app session —
see `scripts/capture-poster-gallery.py` and
`corpus-observed/poster-gallery/screenshots/README.md`. That work also established
that a modern SPA may hold auth in memory and refuse to have its session saved and
replayed, so assume one long authenticated run rather than many short ones.

## What happened on 3 August

**The staff suggestions form is finished and connected.** Live at `/suggest`,
writing to the master sheet's **Staff suggestions** tab. Full detail in
`suggest/HANDOVER.md`. It survived a real failure during setup that is worth
knowing about: the Apps Script was pasted and saved, but the deployment still
served the previous version, and the form correctly refused rather than pretending
to save. `GET /api/log?check=ping` is the diagnostic — the new script answers
`{"ok":true,"wrote":["row"]}`, the old one answers `{"ok":true}`.

**Every self-referential link is gone.** There were 34; the merge fixed 24 and the
rest were judged individually. Two new standing checks stop them returning:
`no page links to itself` and `path+fragment links resolve`. The second closed a
blind spot between the two existing link checks that had let **13 dead HubSpot
anchors** reach readers.

**Answers are now structured.** `/api/search` returns `format: "steps" | "prose"`,
and procedural questions come back as numbered steps with a menu path per step.
All four surfaces render them — KB search, the widget, `deflect.js`, and the
support-deflection prototype. The prose still rides alongside, so every older
consumer and every failure path is unchanged.

**The help widget was rebuilt.** It opens on six topic doors ("Hello, how can we
help?") rather than dropping people into a chat, the answering surface is called
**Instant answers**, a chosen door opens onto an intro card explaining what the
chat is, and the panel can be resized by button or by dragging its top/left edges.
It also took on the admin-help prototype's visual language wholesale. Detail in
`widget/HANDOVER.md`.

**`prototype/admin-help.html` no longer carries its own copy of the widget** — it
loads the real `/widget/help-widget.js`. It had drifted a full redesign behind.
`prototype/support-deflection.html` still has its own inline flow by necessity, but
now renders steps too.

**Two registration articles corrected, and a dossier conclusion overturned** — see
"Settled" below.

## Open, in the order I would do them

### 1. Loom Phase 1

As above. It is the one item with a hard external dependency (Gareth's Loom
session) and the largest potential payoff.

### 2. The suggestion list for the KB ask bar

Gareth is gathering **real historic question data** — the recent interaction-log
rows are mostly test traffic and mean nothing. The plan, agreed 3 August:

- Suggestions appear as someone types in the KB search bar, matched on **words
  anywhere**, not on prefix. Prefix matching was rejected: the code's own note
  records that most people type two words ("incomplete submissions"), not "how do
  I…", so a prefix mechanic would be dead weight for most visitors.
- Every suggestion must be **verified to answer confidently** against the live API
  before shipping — the same rule the widget already enforces. A typed question
  answers probabilistically; a verified suggestion answers strongly every time.
  That guarantee is the actual prize, not the saved keystrokes.
- Log suggestion clicks **distinctly** from typed questions, or the gap log slowly
  goes blind: every clicked suggestion is a question we wrote, not one a reader
  volunteered.
- Useful existing seams: `project/ticket-gaps.csv` (from 2,740 tickets), the
  failing HubSpot search terms written up in `project/context-from-conversation.md`
  (search-shaped input, which is what has to match), the `SYNONYMS` map in
  `assets/search.js`, and ~20 already-verified questions parked in
  `widget/help-widget.js`.

### 3. The "payments" collision — a structural call for Gareth or Kristy

Three different pages answer to "payments", and the answer layer cannot reliably
tell them apart. Demonstrated live on 3 August:

- *"Where is my Oxford Abstracts invoice?"* → the new internal note (correct)
- *"Where do I pay Oxford Abstracts?"* → `creating-and-paying-for-a-new-event.md`,
  which describes a different route (**Payment pending** → **Pay for event**)
- *"Where is the event payments page?"* → **Registration → Tickets → Finance**,
  which is the *attendee* finance page. **Wrong answer.**

Unresolved: whether "Pay for event" is a second valid route to the same billing
area or stale content predating the credit-card icon. That needs someone who can
look at the app, not a guess.

### 4. Content from the dossiers

`corpus-observed/delegate-registration/article-gaps.md` is the queue.

- **Priority 1 — changing what appears on an invoice after issue.** Still the
  largest delegate theme in the ticket sample and still blocked on one untested
  question: what is changeable *after* an invoice is issued, and by whom.
- **Priorities 6 and 7 are unblocked and ready to write**: the registration form
  is a questions × ticket-groups grid, and the publishing prerequisites
  (the **Visible to the public** toggle, the payment-provider hard gate, the
  Authorize.net USD rule, and a warning that **Preview completes real orders**).

### 5. Smaller, well-defined (each verified still open on 3 August)

- **Skip-to-content link** — missing site-wide, WCAG 2.4.1 Level A, about six
  lines in `build.py`. `/suggest` has one; the KB does not.
- **2 "Event Administrator" links** in `different-types-of-users-in-the-system`
  point those words at the dashboard article.
- **17 rows** unresolved in `project/plan-gating-review.csv`.
- **A Dashboard question the KB answers weakly** — *"What does my package
  include?"*. (*"Where do I find my event ID?"* was the other and is now fixed by a
  new internal note.) Both had been shipped as suggested questions in the widget,
  which is how they were caught.

### 6. Watch, do not act yet

- **Deflection latency.** Steps answers take ~8s against a 2.5s interrupt cap, so
  they lean entirely on the prefetch; prose answers still return in 2–4s. Once the
  support form has real traffic, the `not_interrupted` share of `ticket-form` rows
  says whether the window is being missed. If it is, prefetch earlier — never raise
  `maxWaitMs`.
- **Step count varies slightly between runs** (4 vs 5 for the same question) even
  at temperature 0.2. Content is stable; temperature 0 is the next notch if it ever
  matters.

## Settled on 3 August — do not re-litigate

**"Edit or refund order" exists.** It is **one menu item, not two buttons**, behind
the **three dots at the top right of the attendee panel** (Registration →
Registrations → click the row). The amendment article called it "Edit Order" and
the refund article called it "Edit & Refund Order"; both were wrong and both are
corrected. It appears on a **€0.00 order**, so nothing is gated on payment.

The dossier had recorded the buttons as absent and could not distinguish "removed
in v3" from "only on paid orders". Neither — the exploration never opened the ⋮.
**61 tickets a year were waiting on that.** The lesson is recorded in the dossier:
*an option behind a kebab menu reads as absent; check the ⋮ before concluding a
control was removed.*

**Where the event ID lives.** The number after `/events/` in the URL while signed
in — `app.oxfordabstracts.com/admin/events/528/...` is event 528. Now an internal
note, and it answers.

## Housekeeping in the master sheet

Test rows from 3 August to delete: one in **Staff suggestions** ("ROUND-TRIP TEST
from Claude"), `CONNECTION TEST` rows in **Log**, and a handful of `asked` /
`sent_anyway` rows under surfaces `widget`, `kb-search` and `ticket-form`.

Optional, one line: set `NOTIFY` at the top of `scripts/sheet-logger.gs` to
Kristy's email and she gets a message per suggestion. Requires the same
paste-then-**redeploy** dance as before.

## Things learned that will save the next session time

- **A saved Apps Script is not a deployed one.** Deploy → Manage deployments →
  pencil → **New version** → Deploy. "New deployment" mints a *new URL* and leaves
  the old one serving old code, which looks exactly like nothing happening.
- **Verify a check can fail before trusting it.** The new self-link check passed
  its first run with a fault deliberately injected — `build.py` rewrites
  same-section links to relative form, so comparing against root-absolute paths
  could never match. It was a check that could not fail. Both new checks now
  resolve hrefs with `urljoin`, as `check_links` always did.
- **The preview pane does not composite frames**, so any transitioned property
  (width, height, background) reads frozen at its start value through
  `getBoundingClientRect` or `getComputedStyle`. This produced three separate
  false diagnoses in one session. Disable the transition before measuring.
- **PowerShell hides the response body on non-2xx** and mangles non-ASCII on
  output. `Sebastián` printed as mojibake while stored perfectly. Read error
  bodies and accented text from a browser tab instead.
- **Scrub an animation to the frame you care about rather than trusting the maths.**
  A dog's nose was buried below the ground line because a rotation had been
  computed to the muzzle's centre instead of its tip.
