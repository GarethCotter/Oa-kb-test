# Loom transcript mining — project brief

*Agreed Saturday 1 August 2026. Starting Monday 3 August. Not started yet — this
file exists so Monday is not a cold start.*

---

## The idea

Sales and support answer customer enquiries by recording a Loom and narrating the
fix. That library is a large, untapped knowledge seam, and a particular kind of
seam: **people record a video precisely when writing it down was too hard.** So it
holds the knowledge that resists documentation by construction, not by neglect.

Loom has no obvious public API, so the working assumption is Playwright against
an authenticated session. We want the **transcripts and metadata only** — not the
video files.

## Scale

Starting with Geoff (the boss): **~500 videos, 2–3 minutes each.**

That is roughly 21 hours of narration, ~175,000 words — comparable in volume to
the entire existing 174-article corpus.

## Two things Gareth's clarification changed

**Every video is a 1:1 personal response to a specific customer.** Nothing is
generic or public. Consequences:

1. **View counts are useless as a signal.** An earlier version of this plan said
   "a Loom watched 200 times is an article that should exist". Wrong here — a
   video sent to one customer gets one or two views. Frequency has to come from
   **clustering topics across videos**, exactly as the 4,898 support tickets were
   clustered into 321 topics. Same method, proven.
2. **The privacy constraint is absolute, not a filter.** There is no safe subset
   to cherry-pick: every transcript is customer-specific by definition, and the
   screen was shared, so transcripts will name customers, events and possibly
   delegate or payment data. Geoff's in particular may carry commercially
   sensitive material — pricing, contract terms, complaints about named accounts.

## Where the data lives

**`Desktop\Claude\oa-loom-transcripts\`** — beside the repo, never inside it.

Follows the established pattern: `oa-support-replies/` sits outside the repo for
exactly this reason. `CLAUDE.md` is blunt that nothing customer-specific may enter
`corpus-internal/`, because anything there surfaces to any user who asks the right
question.

**Raw transcripts never cross into the repo.** Only generalised knowledge does,
written or reviewed by a human, after a scan for names, emails and event IDs.

## The plan, and where the real unknown sits

**Phase 1 — one session, ~15 minutes of Gareth's time.**
Sign in to Loom, open one video, watch the network traffic. The question:
**does Loom's frontend fetch the transcript as JSON from an endpoint?** If yes,
phases 2–3 are trivial and robust. If no, we scrape rendered DOM — workable but
fussier. Pull three transcripts as samples in the same session.

Note: modern SPAs often hold auth in memory and cannot have their session saved
and replayed — established the hard way on Oxford Abstracts admin (see
`corpus-observed/poster-gallery/screenshots/README.md`). Assume one long
authenticated run rather than many short ones.

**The decision gate is reading those three transcripts.**

- Steps reconstructable from transcript alone → goldmine; take all 500 and mine
  for content.
- Mostly *"click here, then this bit, then pop that in there"* → pivot to
  **topic mining only**: titles, dates, clustering. Still a real gap list, but a
  fraction of the effort and a different project.

Screen-narration transcripts are frequently unusable as prose because of deictic
language — "here", "this", "that" mean nothing without the picture. This is the
assumption the whole project rests on and it is currently untested.

**Phase 2 — full pull.** One background run; 500 videos at a few seconds each is
under an hour, ~1MB of text.

**Phase 3 — mine and cluster.** Reuse the ticket-mining method that produced 39
internal notes from 4,898 tickets.

## Access

- Geoff is the right first account because access is easy and he can **also grant
  workspace-admin access to everyone else's library** — one request instead of
  fifteen. Ask for both at once.
- **Do not collect anyone's login.** Shared credentials are a security problem,
  probably breach Loom's terms, and do not scale. Workspace admin, or people
  moving Looms into a shared folder.
- Before writing any scraper: check whether the paid workspace offers a **bulk
  export**, and whether Atlassian (who acquired Loom) now exposes an API. Half an
  hour that could remove the need for scraping entirely.

## Open questions for Monday

1. Do the videos have meaningful titles, or are they "Untitled Loom — 12 March"?
   If untitled, transcripts become the only signal and the topic-mining fallback
   weakens too.
2. Is there a bulk export or API on the paid plan?
3. Does Gareth have, or can he get, workspace admin rather than just Geoff's
   library?

## Why Geoff's library may not be the richest seam

A boss's Looms skew towards sales demos, prospect walkthroughs and escalations —
"here is how the product works" rather than "here is how to fix what you are stuck
on". That maps to onboarding content more than to ticket deflection. The frontline
support library is the likelier gold. Geoff is the pilot and the door-opener, not
necessarily the payload.
