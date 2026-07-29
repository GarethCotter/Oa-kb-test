# Oxford Abstracts KB — proposed structure (v2)

*Revised 28 July 2026 after product context: Symposia and Certificates are separately purchased add-ons (Certificates included in Professional), and the KB's primary audience is admins/organisers.*

## First principles

**1. Who arrives, and with what intent?**
The primary audience is **organisers/admins** — the paying customer, arriving with a task in mind, returning repeatedly across the life of an event. **Participants** (submitters, reviewers, committee, attendees, exhibitors) are secondary: they usually arrive once, via a link an organiser sent them, and need a short complete answer to "what do I do?". These two intents shouldn't share one flat list, so the top-level split is audience, with organisers first and given the depth.

**2. What order do organisers think in?**
An event has a natural lifecycle: set up → collect submissions → review → decide → communicate → build the programme → register delegates → run the conference → report. The organiser sections follow this order, so the nav doubles as a "what do I do next?" checklist.

**3. What you buy shapes what you see.**
Symposia and Certificates are add-ons most customers don't have. Content for products a customer hasn't bought shouldn't be woven through the core path — it creates noise for the majority and confusion ("why can't I find this screen?"). So add-on content lives in its own clearly-labelled section: self-contained, easy to route around for most users, easy to find for those who own it. This also keeps the door open to conditionally surfacing it later based on plan.

**4. What earns a page?**
One canonical page per task. The 20-page FAQ silo violates this — those answers belong with their topics, so each dissolves into the relevant canonical article and the FAQ category disappears. (FAQ silos duplicate, drift, and force users to check two places.)

## The proposed structure

**Organisers** *(follows the event lifecycle)*

| # | Section | Articles | Notes |
|---|---|---|---|
| 1 | Getting started | 21 | Accounts, dashboards, creating an event, users, packages, platform basics |
| 2 | Submissions | 29 | Form design, question types, multi-stage, collecting/managing |
| 3 | Reviewing | 14 | Review forms, recruiting, assigning, managing |
| 4 | Decisions | 9 | Acceptance types, recording outcomes |
| 5 | Emails | 12 | Creating, sending, scheduling, deliverability (DKIM, domains, sent log) |
| 6 | Programme, exports & reports | 14 | Sessions, program builder, publishing, abstract books, backups |
| 7 | Delegate registration | 20 | Tickets, payments, orders, invoices, refunds |
| 8 | Conference platform | 28 | Virtual/hybrid setup, professional features, announcements, Zoom, speakers |
| 9 | **Add-ons** | 17 | **Symposia** (16 articles, full lifecycle, self-contained) and **Certificates** (1) |
| 10 | Integrations & API | 5 | Cvent, Swapcard, idloom, EventsAir, API |
| 11 | Account administration | 5 | Account dashboard, customer portal, billing, deleting/archiving |

**Participants** *(short, self-contained, linkable)*

| # | Section | Articles | Notes |
|---|---|---|---|
| 12 | For submitters | 10 | Incl. symposia submitters — participants don't know or care what's an add-on |
| 13 | For reviewers & committee | 6 | |
| 14 | For attendees & exhibitors | 9 | Attending, using the platform, exhibitor booths |

14 sections instead of 46. All 199 articles are mapped (Proposed section column in the audit workbook).

## Corrections from v1

- **Symposia is no longer merged into the main track.** v1 assumed it was a variant of core functionality; as an add-on it stays together as a self-contained sub-lifecycle under Add-ons. Deduplication still applies *within* symposia content, but the 16 admin symposia articles survive as their own set.
- **The "duplicate" `Editing a symposium` turned out not to be one** — one is the admin version (→ Add-ons), one the submitter version (→ For submitters). Both stay.
- **Certificates** moves to Add-ons rather than Programme/exports. Its article should state plainly that it's a paid add-on, included with Professional.

## Judgement calls still open

- **"FAQ: Admins — X" pages** are mapped to section X, to be dissolved into articles there.
- **Legacy "2.0-2023-version" registration pages (5)**: assumed superseded — please confirm which registration version is current before deletion.
- **Professional-tier conference features** (9 articles) currently sit inside Conference platform. If the Professional tier works like an add-on commercially, they could move to Add-ons instead — needs your call on how customers perceive it.
- **Platform basics** (search bars, tables, picture dimensions, accessibility, network-failure error) sit in Getting started for now.

## Why this structure serves the LLM plan

- One canonical page per task → the update-LLM has exactly one file to edit per feature change.
- The audience and add-on splits give the search-LLM routing signals: who's asking, and what plan they're on.
- Build target: one folder per section, one markdown file per article with frontmatter (title, audience, section, add-on flag, related pages) — the same files the update-LLM edits and the static HTML site is generated from.

## Suggested next step

Confirm the sections (especially the Professional-features question), then I'll produce the merge plan: every FAQ dissolution and within-symposia consolidation, source pages → target page, so the corpus is clean before we design the HTML site and update pipeline.
