# Decisions, evidence and design intent not captured elsewhere

Everything below was agreed during the build but only existed in conversation. It is the
reasoning behind the current design and the evidence behind what is still to do.

---

## 1. The two datasets that drove most decisions

### HubSpot KB search analytics (top 25 terms)

The column that mattered was **average result clicks** — i.e. did the searcher find
anything. Roughly **a third of searches ended with no click at all**.

Worked: invoice 1.15 · api 1.06 · poster gallery 1.0 · receipt 1.0 · withdraw 0.81 ·
website 0.80 · payment 0.79

Failed: **"incomplete submission" 11 searches / 0 clicks** · save 0.09 · template 0.13 ·
deadline 0.17 (24 searches) · submission 0.29 · registration 0.32 · incomplete 0.35 ·
feedback 0.36 · copyright 0.44

**Cause:** not one article title contained the words "deadline", "incomplete",
"copyright" or "save", even though 13 articles discussed deadlines and 17 mentioned
incomplete submissions. This is why titles were rewritten to contain searched words and
why `SYNONYMS` exists in `assets/search.js`. Feed new failing terms into both.

**Still outstanding from this:** copyright appears in only two articles in passing — a
genuine content gap, not a naming one. And **"api" is the single most-searched term**
(34 searches, best click-through) with only one article behind it; worth expanding.

### HubSpot pageviews (top 10 articles)

1. Accessing your reviews **4,739** · 2. Creating an account 2,948 · 3. Making a
submission 1,541 · 4. Setting up your conference program account 1,042 · 5. Editing an
abstract 941 · 6. Not receiving emails 842 · 7. Open and close submissions 735 ·
8. Completing a review 668 · 9. Your personal dashboard 577 · 10. Viewing sessions 565

**Nine of the top ten are participant-facing.** This drives the "Most popular" list.

**But the conclusion we reached is the important part**, and it is easy to get wrong:
this does *not* mean participants use the KB more than organisers. Admin traffic is
spread thinly across ~120 articles while participant traffic concentrates in about ten,
and only the top ten was visible. More importantly, **most participants never see the
homepage at all** — they arrive by deep link from an email or the app. So:

- **The homepage is an organiser surface** and should stay organiser-first.
- **The participant experience is the individual article**, landed on cold with no
  context. That is where participant design effort should go — orientation at the top of
  the page, and sideways links to what they might need next.

**To settle it properly, pull from HubSpot:** entry pages (which pages start sessions),
traffic sources (direct vs referral from app.oxfordabstracts.com), and total views by
category rather than the top ten.

---

## 2. Content gaps the search data implies (separate from the ticket gaps)

The ticket analysis lists gaps by ticket volume. These come from search behaviour and
from thin sections, and only partly overlap:

- **Submitter troubleshooting** — the happy path is covered, nothing covers what goes
  wrong: why a submission shows as incomplete, what happens at the deadline and whether
  you can still edit, withdrawing your own submission, whether work is saved if you close
  the tab, copyright in a submitted abstract.
- **Reviewers** — five articles carry the busiest traffic in the whole KB. Nothing on:
  what to do if you can't see your assigned reviews (this was also one of the two FAQ
  answers that could not be placed, and appeared twice in the old FAQ — support clearly
  fields it often), reviewing on a phone or tablet, whether you can change a submitted
  review, what reviewers can and cannot see.
- **Email deliverability** — DKIM and domains are documented; "my submitters say they got
  nothing, what do I check" is not. 842 people read the not-receiving-emails article.
- **The API** — most-searched term, one article.

## 3. Loose ends that are not on the checklist

- **`corpus/_review-unmapped-faq.md`** holds two FAQ answers from the old KB that could
  not be auto-placed. Both concern reviewers not seeing their reviews. Place them.
- **One card description is broken**: "Changing the owner of a submission" renders as
  "…instructions below # This article is for Admins ONLY." The first-sentence extractor
  ran across a heading boundary. Fix in `build.py` (`enrich_body`) by stopping at headings.
- **The header logo is remote** — it loads from Oxford Abstracts' Storyblok CDN. That is
  their own live infrastructure so it is safe, unlike the old HubSpot images, but it is
  the one external dependency left in the page.

---

## 4. Design intent for the things not yet built

### Ticket deflection on the HubSpot support form

Run the typed question against `/api/search` before the ticket sends, and show the likely
answer. Three rules, all deliberate:

1. **Never show a confidence percentage.** "We're 90% sure" is false precision; the one
   time it is confidently wrong, trust is gone. Use *"This might be what you're after —"*
   then the answer, then **That's solved it** / **Send my ticket anyway**.
2. **Never block the send.** The reader is already frustrated enough to open a support
   form; making them fight past a robot is exactly the high-effort moment that damages
   loyalty. One click past it, always visible.
3. **Only interrupt when the answer is strong.** This needs a **confidence signal added to
   the endpoint** — it currently returns `found: true/false`, which is not enough to
   decide whether to interrupt someone.

Also: when a ticket is sent anyway, attach the suggested articles so support can see what
was already tried.

**Why this matters more than it looks:** every interaction is a labelled outcome —
question, article suggested, whether it solved it. Search logs tell you what people
asked; this tells you what *worked*. An article suggested twenty times that deflects
nothing is definitively broken, and no other signal would reveal that.

### The in-app chat widget (replacing command.ai / Amplitude)

Same endpoint, bottom-right launcher, multi-turn by sending history back each turn.

- **The advantage over the standalone site: it knows what page the user is on.** Pass the
  current app screen as context so "why can't I do this?" gets a contextual answer.
- **No admin UI is needed.** Unanswerable questions get logged; a human writes a short
  note into `corpus-internal/` and commits. That replaces command.ai's answer queue
  entirely — the file system is the answer store.
- **Economics:** Amplitude-tier tooling runs hundreds to thousands per month; this runs on
  pennies of Haiku. The trade is that uptime and edge cases become yours.
- **Sequencing:** launch the KB, let the search endpoint prove itself for a few weeks,
  then wrap the widget around it. By then the gap log will already say what to write.
- Check what else command.ai is used for — if it also does product tours or nudges, this
  replaces the chat only.

### The app-testing agent ("secret corpus")

The original idea was an agent that uses the product and records what it learns.
**Point it at finding gaps, not at answering customers.** An agent misreading a screen
produces plausible, confidently wrong notes; if those feed live answers, a wrong menu
path becomes a support ticket and nobody knows which layer produced it.

As a gap-detector it is near pure upside: walk a feature, compare what was observed
against what the article says, and output a list — *this error state is undocumented,
this button was renamed, this article says three steps and there are now four*. A human
promotes the true findings into articles.

Two other benefits: **fresh screenshots** (the current ones date from 2021–2023 and some
show a previous UI), and **drift detection on a schedule** — run it monthly against key
flows to learn which articles have gone stale, which is currently unknowable.

Hard constraint: **a test event on a test account, never live data.** Real submissions
contain named academics' personal information. Notes need a date and app-version stamp,
because observations rot faster than prose.

### The weekly gap-digest email

Monday cron. Two lists: **questions the bot could not answer**, clustered so five
phrasings of the same thing arrive as one item with a count; and **articles rated
unhelpful**, grouped by the reason picked. Each cluster with a suggested next step —
write a note, or write an article.

Dependency: search logs must be written somewhere queryable, not just streamed to the
Vercel console. That same change makes a dashboard possible later.

**Why it is the highest-leverage thing left:** everything else makes existing content
findable; this is the only piece that tells you *what to write next based on evidence*.

---

## 5. From the help-centre benchmarking research

Full report is in the original chat; the actionable conclusions:

**Already done and validated by it:** search-first landing page, two audience doors,
lifecycle IA, guided section pages, answer-first standfirsts, plain-language answers with
cited sources, graceful degradation, visible-but-quiet human escalation, last-reviewed
dates, diagnostic feedback instead of a bare thumbs-up.

**Still outstanding, in priority order:**

1. **Ticket deflection** (see above) — the single highest-value pattern not yet built.
2. **In-app contextual help** — the strongest 2025–26 pattern; help where the user is
   stuck rather than on a separate site.
3. **A "What's New" surface** tied to product releases. The update pipeline could generate
   this from its own pull requests almost for free.
4. **8th-grade readability pass** — the evidence on less-confident users is unambiguous,
   and writing for them measurably helps everyone else too.
5. **Lightweight personalisation by plan/role** — badges that set expectations rather than
   hide content. Hiding content confuses people comparing plans or growing into them.

**Benchmarks worth tracking from day one:** self-service deflection rate (a
well-maintained KB reaches 25–40%; AI-assisted 40–60%), failed-search rate and top
zero-result queries, article-level "No" reasons, and the escalation rate from the answer
layer. If failed searches dominate, fix search and IA before writing more articles. If
articles are found but rated unhelpful, fix the writing. If deflection is high but
follow-up tickets rise, the answer layer is over-containing — loosen escalation.

**Exclude from any deflection target:** the ~160 tickets a year that are pricing, licence
and trial conversations. No KB can deflect those, and including them makes the target
dishonest.

---

## 6. Product observations for the wider team

Not KB work, but they came out of the ticket analysis and are worth passing on:

- **219 tickets mention an error message** (404, 500, "network failure", "something went
  wrong"). These are not one topic — they are how people describe completely different
  underlying faults. **Error messages that named the actual problem would deflect more
  tickets than any article could.** That is a product fix.
- **Ticket volume is rising**, not falling: ~140/month across 2025, ~165/month in 2026.
- **Four tickets arrived in Spanish or French.** Tiny, but the answer layer can reply in
  the reader's language at no extra cost — the old KB could not.

---

## 7. Plans and add-ons (for badges and gating)

Tiers: **Basic (free)** → **Abstract Management** → **Standard Conference** →
**Professional Conference** (most expensive; includes Certificates as a bonus).

Separately purchased add-ons: **Certificates**, **Symposia**, **Multi-stage**.

Symposia is not widely bought, which is why its content is grouped under Add-ons rather
than woven through the core path. Certificates is included with Professional but sold
separately otherwise — the article should say so.

17 articles still carry `plan: all plans (including free Basic)` as an unverified default;
see `project/plan-gating-review.csv`.
