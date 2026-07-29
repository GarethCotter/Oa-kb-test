# Oxford Abstracts KB — merge & consolidation plan

*28 July 2026. Takes the corpus from 199 articles to ~174, with every change listed as source → target. Nothing is deleted until you approve this list.*

## Decisions folded in from your product context

- **Professional Conference features (9 articles) stay in Conference platform**, grouped as a clearly-labelled "Professional Conference" subsection. Professional is a plan tier, not a purchase bolted on later, so its features belong in the product area they extend — but every article gets a visible plan badge ("Professional plan") in its frontmatter so the tier boundary is unmissable and the search-LLM can answer "is this in my plan?".
- **Certificates stays in Add-ons**, with the article stating it's an optional paid add-on, included with Professional.
- **Plan metadata across the board**: each article's frontmatter records the minimum plan/add-on it applies to (free / paid abstract management / standard conference / professional / add-on). Cheap to add now, valuable for search routing later.

## A. Good news: the "legacy" pages aren't legacy

The five "2.0-2023-version" pages turn out to be the **current, live registration articles** — the version marker is only in the URL slug, left over from a HubSpot rename. Nothing to delete; they get clean slugs in the new KB (e.g. `/registration/dependency-questions`) with redirects from the old URLs.

## B. Removed outright (3)

Only the system pages: the search-results shell, the 404 page, and the "Didn't find the help you need?" prompt. These are site furniture, not articles — the new site rebuilds its own.

## C. FAQ dissolution (10 pages → 0)

Each question moves into the canonical article for its task, usually as content or a short "Common questions" block at the end. Per page:

**FAQ: Admins — submissions** (11 questions)
| Question | Target article |
|---|---|
| Difference between submitters, authors, presenters | Different types of users in the system |
| Handling user-reported issues | Admins: Guidance for dealing with submitter/reviewer/committee issues |
| Re-numbering abstracts for the programme | Assigning program codes in the decisions table |
| Submit on behalf of someone else | Making a submission on behalf of someone else |
| Images/tables in abstracts | Text editor types |
| Conditional questions | Dependency questions |
| Word-count alert issue | Word and character count |
| Submission marked incomplete | The Submissions Table |
| Changing deadlines | Open and close submissions / call for abstracts |
| Withdraw/delete as admin | Deleting / restoring or withdrawing a submission |
| Close submissions but allow editing | Open and close submissions / call for abstracts |

**FAQ: Admins — decisions** (5)
| Question | Target |
|---|---|
| Adding committee members | Manage users |
| Deciding as an administrator | Recording a decision |
| Adding a "rework" decision type | Design the decision form |
| Committee decisions by category | Assigning specific categories to committee members |
| Ensuring committee can decide | Opening and closing decision making |

**FAQ: Admins — emails** (9)
| Question | Target |
|---|---|
| Accept/reject notification emails | Notifying submitters of their outcomes |
| Emailing just presenters | Emailing presenters and authors directly |
| What info emails can include | Creating custom emails |
| Checking if an email sent | How To Use The Email Sent Log |
| Non-template emails | Creating custom emails |
| Pausing automatic emails | Amending template emails |
| Emailing a few people / one person | How to send emails from tables |
| Being notified of new submissions | Sending and scheduling emails |
| Sending from a chosen address | Sending emails from your chosen email address |

**FAQ: Admins — getting started** (6)
| Question | Target |
|---|---|
| Password reset | Creating an account with Oxford Abstracts and logging in |
| Granting admin rights | Manage users |
| Data retention period | How to permanently delete or archive your event |
| Being admin and reviewer at once | Different types of users in the system |
| Guidance to give users | Participant section landing pages |
| Deleting an account | How To Delete Your Oxford Abstracts Account |

**FAQ: Admins — reviews** (6)
| Question | Target |
|---|---|
| Unassigning reviews when removing a reviewer | Assigning and unassigning a submission to a reviewer |
| Seeing who's completed reviews | The review tables |
| Completing a review on behalf | Editing a review or completing a review on behalf of a reviewer |
| Reviewer accept/reject recommendations | Designing the review form |
| Bulk assigning | Assigning and unassigning a submission to a reviewer |
| Controlling reviewer data view | Controlling what the reviewer can see |

**FAQ: Admins — conference platform** (7)
| Question | Target |
|---|---|
| Public vs full-access programme | What is the difference between the public and full access program? |
| Full access without a ticket | Professional Conference — Controlling access |
| Downloading programme info | Downloading your program and session books |
| Deleting a session | Amending, deleting and copying a session |
| Booking clashes | Program bookings |
| Standard vs Professional programme | What are the differences between the free package and paid packages? |
| Exhibitors and sponsors | Professional Conference — Exhibitor space / Sponsors |

**FAQ: Admins — delegate registration** (5)
| Question | Target |
|---|---|
| Setting up payment / payment options (2 qs) | How to set up payment providers for delegate registration |
| Adding tickets to an existing order | How to add add-ons to an existing order |
| Checking a presenter has registered | How to manage orders and edit the attendee table |
| Deleting a registration | How admins can amend existing delegate registration orders |

**FAQ: Admins — multistage** (2) → *Setting up a multi-stage event* and *Managing a sequential multi-stage event*.

**FAQ: Admins — reports** (2) → *Other reports* (review export format) and *Abstract books* (field editing).

**Reviewer FAQ** (participant-facing) → dissolved into the For reviewers & committee guides.

## D. Thin-page merges (5 pages absorbed)

| Absorbed page | Into |
|---|---|
| Editing email signature (106w) | Creating custom emails |
| Acceptance types (111w) | Design the decision form |
| Allowing committee members to assign reviews (112w) | Assigning and unassigning a submission to a reviewer |
| How to embed the online programme to your event's website (83w) | Publishing your program |
| Event administrator dashboard (117w) | Event dashboard *(please sanity-check these are the same screen)* |

Kept despite being thin: the per-partner integration pages (Swapcard, EventsAir) — one page per partner is the right unit — and "How attendees can download event schedules" (participant-facing, complete as is).

## E. Within-symposia consolidation (17 → 7 in Add-ons)

The symposia set stays self-contained but its 16 fragments (median ~150 words) become 6 lifecycle articles:

| New article | Absorbs |
|---|---|
| Symposia overview & dashboard | Symposia overview · The Symposium Dashboard |
| Designing the symposia forms | Designing the symposium submission form · Designing the symposia review form |
| Collecting symposia | Open/close symposium submissions · Creating a symposium (as administrator) · How to Attach a Submission to a Symposium as an Admin |
| Symposia reviewing | Symposium — assigning reviews · Opening/closing symposia reviewing · Notifying reviewers (symposia) · Editing a symposia review / on behalf of a reviewer |
| Managing symposia | The symposium table · Editing a symposium · Delete / restore or withdraw symposia |
| Symposia decisions & emails | Symposia decisions (outcomes) · Symposia emails |

Plus **How To Create A Certificate** as the seventh Add-ons article.

## Resulting corpus

199 → **~174 articles**: −3 system, −10 FAQ pages dissolved, −10 symposia fragments consolidated, −5 thin merges. Every removed URL gets a redirect to its target (the crawl gives us the complete old-URL list, so the redirect map generates itself).

## Next step

On your approval of this list I'll execute it against the markdown corpus — producing the reorganised folder structure (one folder per section, frontmatter with title / section / audience / plan on every file) with FAQ content physically merged into targets. That corpus then becomes the source of truth for the HTML site build and the update pipeline.
