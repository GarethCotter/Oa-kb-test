# Old HubSpot KB: pages with no redirect

*Crawled `help.oxfordabstracts.com/knowledge` on 7 August 2026, following every internal
link. 358 URLs reached; 226 distinct pages once `?hsLang=en` and trailing slashes are
collapsed; 220 returning 200.*

**200 of those 220 are covered** by `redirects.csv` or a `source_url` in the corpus.
Twenty are not, and they are all the same kind of page.

This is the crawl the redirect check cannot do. `check-redirects.py` verifies that
everything *in* the map resolves; it structurally cannot see a page that exists on the
old site and was never put in the map. That is exactly how `/knowledge` itself was missed
until 4 August, when it turned out to be the target of the site-wide "Visit knowledge
base" link on the home page, /about, /pricing and several blog posts.

---

## 1. Eighteen category landing pages, all live, none redirected

Every one is a hub page the old KB links to from its own navigation, so anything that
ever linked to a *section* rather than an article lands here. They 404 the day HubSpot is
switched off.

Proposed targets — the mapping is obvious for most, but check the last four before
committing:

| Old page | Proposed target |
|---|---|
| `/knowledge/getting-started-and-creating-an-account` | `/01-getting-started` |
| `/knowledge/getting-started-with-your-event` | `/01-getting-started` |
| `/knowledge/introduction-to-the-oxford-abstracts-tools` | `/01-getting-started` |
| `/knowledge/the-submission-stage` | `/02-submissions` |
| `/knowledge/the-reviewing-stage` | `/03-reviewing` |
| `/knowledge/the-decision-stage` | `/04-decisions` |
| `/knowledge/emails` | `/05-emails` |
| `/knowledge/creating-exports-reports-and-abstract-books` | `/06-programme-exports-reports` |
| `/knowledge/delegate-registration` | `/07-delegate-registration` |
| `/knowledge/the-conference-platform` | `/08-conference-platform` |
| `/knowledge/integrations` | `/10-integrations-api` |
| `/knowledge/account-administrator-functions` | `/11-account-administration` |
| `/knowledge/attending-an-event` | `/14-for-attendees-exhibitors` |
| `/knowledge/symposia` | add-ons section — confirm the slug |
| `/knowledge/multi-stage` | add-ons section — confirm the slug |
| `/knowledge/guidance-for-reviewers` | the participant-facing reviewing section — confirm |
| `/knowledge/faq` | the FAQ silo was dissolved into topics on purpose. Send it to `/` so the reader can search, rather than to any one article. |
| `/knowledge/support` | confirm whether this is a KB page or the contact route |

## 2. Two functional pages

- `/knowledge/kb-search-results` — the old search results page. Anything that deep-linked
  a search lands here. `/` is the sensible target; the new search is on the home page.
- `/knowledge/kb-tickets/new` — the old support ticket form. This is the page the
  deflection card is meant to replace, so where it points is a product decision, not a
  redirect decision. Worth settling before HubSpot is cancelled either way.

## 3. Six pages already dead on HubSpot — and one explains a bug in our corpus

These returned 404 **on the old site** while crawling. They are linked from live old-KB
pages, so HubSpot has had rotted internal links for some time. Nothing to redirect — they
are already gone — but two are worth knowing about:

- `/knowledge/cross-referencing-presenters-and-delegates` — **this closes an open
  question.** `07-delegate-registration/managing-orders-and-edit-the-attendee-table.md`
  answers "How can I check if a presenter has registered?" with a link labelled *Cross
  referencing presenters and delegates*, pointing at our section index. The article it
  names existed on HubSpot once and is now 404 there too. So the answer was never carried
  across, and the link text is a fossil. That question needs a real answer written.
- `/knowledge/creating-exports-reports-and-abstract-books` is **live** and is a category
  page, which explains the other ghost link of the same name in `06`.

The remaining four: `/knowledge/editing-or-changing-the-status-of-a-registration`,
`/knowledge/registering-for-an-event-as-a-delegate`,
`/knowledge/setting-up-payments-for-delegate-registration`,
`/knowledge/the-registration-form`, `/knowledge/view-sent-email-log`.

---

## Done, 7 August

**Eighteen of the twenty are now redirected**, in both `redirects.csv` and `vercel.json`
(which now holds 220 entries). Coverage of the live old site goes from 200/220 to 218/220.

Two are held back deliberately, because they need a decision rather than a guess:

- `/knowledge/support` — unclear from the crawl whether this is a KB page or the contact
  route. Look at it before choosing a target.
- `/knowledge/kb-tickets/new` — the old support ticket form. Where this points is a
  product decision, not a redirect decision: the deflection card is meant to replace this
  page, so the answer depends on whether it should reach the new support form, the KB
  home, or stay pointing at whatever replaces it in the app.

**Re-run this crawl before HubSpot is cancelled, not after.** It is the only check that
looks at the old site rather than at our own map, and it costs a few minutes:
`scratchpad/crawl_old_kb.py` in the session notes, or rewrite it — it is forty lines of
BFS plus a set difference.
