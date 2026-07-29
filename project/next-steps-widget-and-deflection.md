# From prototype to production: logging, the widget, the form checker

*Written 29 July 2026, alongside the two live prototypes. Three questions answered:
how to record interaction data, how to ship the in-app widget, how to ship the
support-form checker.*

---

## 1. Recording interaction data

**Principle: every surface emits the same small event, and the store must be
readable by a person, not just a machine.** The current state — search logs in the
Vercel log stream — is already flagged in the checklist as the blocker for the
weekly gap digest.

### The event

One row per interaction, identical schema from all three surfaces:

| field | example |
|---|---|
| `ts` | 2026-07-29T14:02:11Z |
| `surface` | `kb-search` \| `widget` \| `ticket-form` |
| `screen` | `Emails` (widget only — the page context) |
| `question` | the reader's words, verbatim |
| `answered` | true / false |
| `sources` | the article paths shown |
| `action` | `solved` \| `sent_anyway` \| `not_interrupted` \| `opened_article` \| `followup` \| `none` |

**Never store who asked.** No names, emails or event IDs in the log — and strip
anything email-shaped from the question text before writing it. Same reasoning as
the corpus-internal rule: this data will be read widely and casually.

### Where to put it

Recommended start: **one `/api/log` function forwarding rows to a Google Sheet**
(via an Apps Script web-app URL). Zero infrastructure, instantly filterable and
pivotable by a human, and at this volume (~165 tickets/month plus searches) a
sheet lasts years. `api/feedback.js` already exists and just logs to the console —
it becomes the first client of `/api/log`. If volume ever outgrows a sheet, swap
the storage inside `/api/log` for Vercel KV or Postgres; the clients never change
because the schema doesn't.

### What the data answers

- **Gaps** — cluster the `answered: false` questions; five phrasings of one
  missing article arrive as one item with a count. This is the weekly digest's
  first list, and it tells you *what to write next*.
- **Broken articles** — an article `sources`-shown twenty times whose tickets
  still say `sent_anyway` is definitively not doing its job. No other signal
  reveals this: search logs say what was asked, only outcomes say what *worked*.
- **Benchmarks from day one** — deflection rate (`solved` ÷ deflections shown),
  failed-search rate, escalation rate. The checklist's "no benchmarks are being
  tracked" rough edge closes as a side effect.

---

## 2. Shipping the in-app widget

The prototype is the spec: one Help surface, per-screen suggestions, page
context, in-panel article reading, ticket escalation. What remains is plumbing.

1. **A real endpoint: `/api/assist`.** Accepts `{question, history[], screen}`,
   returns `{answer, confidence, sources, followups}`. Three prototype tricks
   move server-side: the confidence heuristic (currently client-side answer-length
   / has-sources / no-hedging), multi-turn history (currently a 90-char prefix
   squeezed into the 500-char cap), and the screen context. Keeps the 200-null
   failure contract. Reuses the same cached routing table as `/api/search`, so
   cost stays sub-penny per question.
2. **Access control.** CORS restricted to `app.oxfordabstracts.com`; rate-limit
   per session (the corpus is public, the Claude bill is not). The widget renders
   only for logged-in admins — the app already knows who's logged in.
3. **Delivery: one script tag.** The widget ships as `assets/widget.js` from the
   KB deployment; the app adds `<script src=… defer>` and a mount point — most
   naturally behind the **Support** button already in the app header. Widget
   updates then deploy with the KB, no app release needed.
4. **Route→screen map.** A small dictionary from app URLs (`admin/events/{id}/…`)
   to the section names the routing table knows. One OA developer knows these
   routes; ~an hour of their time.
5. **Logging from day one** (§1) — the unanswered-question log is the entire
   content-improvement loop, and it replaces command.ai's answer queue: a human
   reads the log, writes a note into `corpus-internal/`, commits.
6. **Pilot order:** internal staff → two or three friendly customers → everyone.
   Watch the gap log for two weeks between steps.
7. **Before cancelling Amplitude/command.ai:** confirm what else it does (tours,
   nudges, checklists) — this replaces the chat and resource centre only. The 45
   usable command.ai answers are already in `corpus-internal/`.
8. **Voice input** is in the prototype via the Web Speech API — free, no backend,
   button hidden where unsupported, transcript lands in the box for review and is
   never auto-sent. If real-world accuracy across accents disappoints, the swap is
   Whisper (or Deepgram) behind a small `/api/transcribe` function — roughly
   $0.001 per spoken question, single-digit dollars a month at any plausible
   volume; the button and UX stay identical, only where the text comes from
   changes. The real costs are a second vendor key in Vercel and a privacy line
   saying audio is transcribed, not stored.

What this costs to run: pennies per question on Haiku, plus the uptime obligation —
which the silent-fallback contract is specifically designed to soften.

## 3. Shipping the form checker on the live contact-support page

The prototype already speaks the real form's language (portal 9108826, form
`69bc8c33`, the exact field names). The path to live:

1. **Endpoint work first** — same `/api/assist` as above (CORS additionally
   allowing `https://oxfordabstracts.com`, confidence server-side). Do it once,
   both features use it.
2. **A ~100-line snippet in the marketing site** (whoever maintains
   oxfordabstracts.com adds it to the contact-support page):
   - prefetch on blur of the description field, exactly as prototyped;
   - a capture-phase listener on the submit click → `preventDefault` → show the
     interstitial → **Send my ticket** re-dispatches the original click, flagged
     to pass through. The HubSpot form, its reCAPTCHA and its file upload are
     never re-implemented — the reader always submits through HubSpot's own
     machinery.
3. **Attach what was tried.** Add a hidden ticket property in HubSpot
   (e.g. `kb_suggested`) and a hidden form field; the snippet fills it with the
   suggested article titles + whether deflection was shown. Needs HubSpot admin
   access, not code.
4. **Skip-list.** Never interrupt pricing / licence / trial / refund-money
   queries — the ~160 commercial tickets a year that no KB can deflect. A keyword
   guard in the endpoint; also excluded from any deflection target so the number
   stays honest.
5. **Staging pass.** Clone the form in HubSpot (test form ID) on an unlisted
   page; walk the timeout, outage and skip-list cases; confirm a test ticket
   arrives carrying `kb_suggested`.
6. **Kill switch.** The snippet reads a one-line config from the KB origin
   (`{"deflection": true}`); flipping it off requires no marketing-site deploy.
7. **Measure against the known baseline** — ~165 tickets/month — with §1's events.

Sequencing note: the endpoint (step 1 here, steps 1–2 in §2) is shared. Build it
once and both prototypes graduate together.
