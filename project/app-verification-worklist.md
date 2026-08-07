# Claims to check in the app — emails, programme, registration

*Opened 7 August 2026 from a three-section audit of `corpus/05-emails/`,
`corpus/06-programme-exports-reports/` and `corpus/07-delegate-registration/`.*

**The rule this list exists to enforce: nothing here goes into an article until it has
been confirmed in the app.** On 7 August three separate articles were found asserting
that a submission deadline does not close the submission form. It does. One article's
claim had been copied into two others, so it read as corroborated, and a fourth was
written repeating it before anyone checked. Copying is not corroboration.

Where an item says *two articles disagree*, at least one is already wrong on the live
site today. Those rank above everything else.

---

## Already fixed — do not redo

Published 7 August in `e0a718a` and the two commits before it. All were provable from
inside the repo, so none needed the app:

- **Emails:** literal `**` rendering on three live pages; `oxfordabstacts.com` typo;
  menu paths to `Edit & send → Abstract management` and `Sender email`; the destroyed
  4)–7) list in `editing-the-template-emails`; assorted typos.
- **Programme:** the destroyed menu path in `publishing-your-program` (the article had
  no route to the programme builder at all); two empty headings; three broken card
  descriptions; sentence-case menu paths; `public-vs-full-access-programme` plan
  corrected to `professional conference`; typos.
- **Registration:** the stray line being used as a card description and meta
  description; empty heading; two orphaned "read the instructions here." links;
  truncated support sentence; `audience: attendees` on two attendee-facing articles;
  typos.
- **CLAUDE.md** corrected: the ~349 hand-written jump links still in `corpus/` are
  stripped from the *rendered* page by `build.py`, not removed from source — and a
  paragraph made only of fragment links is deleted outright, taking real content with
  it. That is what broke the two articles above.

---

## Tier 1 — a live page is telling somebody something untrue

### 1. Do Stripe refunds process automatically, or not? — money

| Source | Says |
|---|---|
| `07/refunding-an-attendee-through-delegate-registration.md:44` | "If the attendee paid through Stripe then you'll be able to refund automatically on Oxford Abstracts." |
| `07/how-admins-can-amend-existing-delegate-registration-orders.md:79` | "At the moment, you can only process refunds offline e.g. such as a bank transfer." |

Same button, same screen, opposite answers. An organiser following the second will bank
transfer money that Stripe has already returned — a double refund out of their own
pocket.

**Open:** Registration → Registrations table → a **card-paid** attendee → ⋯ → **Edit or
refund order** → remove a ticket → Continue. Does the final step offer an automatic
refund or only "Process Offline"?

**Blocked on the demo event:** its only order is a free £0.00 ticket with no payment
provider, so there is nothing to refund. Needs an event with a real card payment.

*Noted while looking:* the Transactions tab does have a **REFUND METHOD** column, which
implies more than one method exists. Suggestive, not proof.

### 2. Does refunding cancel the person's place?

`07/refunding…:72` — "**Refunding cancels their place.** A refund and a cancellation are
the same action" and prescribes a re-invite workaround.
`07/how-admins…:127` — "Removing tickets leaves the registration in place with nothing
on it."

**Open:** refund an order in full, then check whether the row survives and whether the
person still holds a valid ticket.

### 3. Are partial refunds really impossible?

`07/refunding…:83` — "**Partial refunds are not supported**", plus a three-step
workaround (refund in full, build an admin-only ticket at the reduced price, re-add
them) that costs the organiser both fees twice.

**Open:** Edit or refund order — is there any amount field, or only whole line items?

### 4. Two articles send organisers to support for work the app now self-serves

`06/abstract-books.md:41` — "We can create custom reports, spreadsheets and abstract
books… if the standard options don't meet your requirements."
`06/other-reports.md:64` — "If you need a spreadsheet that isn't in our standard
downloads, get in touch."

But the nav has **Advanced → Book builder**, **Custom abstract book** and **Spreadsheet
builder**, and `corpus-internal/exports-reports-and-abstract-books.md:25` describes all
three as working self-serve tools. Same stale sentence in two articles.

**Open:** Advanced → each of the three tools. Establish what an organiser can now do
unaided.

### 5. Do email attachments arrive as files, or as links?

`05/editing-the-template-emails.md:69` — "One or more attachments can be added to an
email."
`corpus-internal/emails-templates-and-merge-fields.md:53` — "**Attachments** on a
template reach the recipient as a **link** to the file in Oxford Abstracts, not as an
attached file."

Anyone sending a certificate or a programme PDF will believe it is attached.

**Open:** Emails → Edit & send → Abstract management → any manual template → attach a
file → send a test to yourself → look at what arrives.

### 6. Can a Free-plan event edit registration auto emails?

`07/editing-automated-emails-for-delegate-registration.md:16` says no; its own
frontmatter says `plan: all plans (including free Basic)`; `project/plan-feature-matrix.md:45`
lists default and custom emails on every plan including Free. Two of the three are wrong.

**Open:** the pricing page, or a Free event → Emails → Edit & send → Registration auto
emails.

### 7. "Author names cannot be removed from an abstract book"

`06/downloading-submissions-and-their-files.md:53`, stated absolutely, against
`06/abstract-books.md:41` ("containing any fields you wish") and the Book builder tool.
Organisers preparing blind-review material will act on the "cannot".

**Open:** Advanced → Custom abstract book and Book builder — check the field picker for
authors.

---

## Tier 2 — one article, likely stale, real consequences

### 8. Does a table download contain the whole table or just the page on view?

`06/export-table-data-to-excel.md:16` says the entire table; `:30`, fourteen lines later,
says the data on view. The internal note adds that the **registration** table behaves the
opposite way to the submissions table. Three statements, at most one true per table.

**Open:** Submissions → Table and Registration → Registrations table. Set Columns,
download from each, compare.

### 9. The delete-and-restore attendee flow does not match the screen

`07/managing-orders-and-edit-the-attendee-table.md:130` describes clicking a row then a
**red bin**, then `:144` a **cog wheel → View Deleted**, then `:150` **Restore selected**.
Verified today the delete route is: tick the attendee → **Delete attendees**. The whole
restore path is unverified — and matters, because deleting a paid attendee is
irreversible if restore has gone.

**Open:** Registrations table. Is there a red bin in the row panel? Delete a test
attendee and hunt for View Deleted / Restore.

### 10. Which fees are kept on a refund

`07/refunding…:68` says Oxford Abstracts keeps its service fee; `:78` says neither the
payment provider's fee nor the OA fee is returned, "so you absorb both". The second
commits Stripe and PayPal to keeping their cut. Organisers price cancellation policies
off this.

**Open:** Registration → Finance → Billing → Current Oxford Abstracts Fees, and a test
refund's Transactions row.

### 11. Is there a UK VAT tab?

`07/setting-up-payment-providers…:235,245` tells the reader to use a "UK VAT tab". The
verified Finance sub-items are only **Billing**, **Payment providers**, **Tax**. The same
file also calls Payment providers and Tax "tabs", suggesting the whole tab model here
predates the current page.

**Open:** Registration → Finance. Where do VAT receipts live now?

### 12. Authorize.net — currency restriction or country restriction?

`07/letting-attendees-pay-by-invoice-or-bank-transfer.md:82` — "only… if your event
currency is USD". `07/setting-up-payment-providers…:63` — "(For USA clients only)".
Different rules with different answers for a UK organiser charging USD.

**Open:** Registration → Finance → Payment providers with a non-USD currency set.

### 13. The public vs full-access feature table

Thirteen Yes/No rows, byte-identical in `06/public-vs-full-access-programme.md:27` and
`06/publishing-your-program.md:68`, from October 2021 screenshots. One row answers a
Yes/No question with "Admin controls".

**Open:** a Professional event, published with a non-open access type — walk both links
side by side. Whatever is true gets written **once** and cross-linked, not twice.

### 14. Can you send a template to presenters from the Emails page?

`05/emailing-presenters-and-authors-directly.md:33` describes a **RECIPIENT GROUP**
dropdown with presenter options, and repeats it in its own Common questions — the
copied-claim pattern on a single page. `corpus-internal/emails-templates-and-merge-fields.md:19`
says tables are how you reach anyone who is not a submitter.

**Open:** Emails → Edit & send → Abstract management → new template → read every option
in the recipient dropdown.

### 15. The five-recipient resend cap

`05/using-the-email-sent-log.md:44` — "select up to **five** recipients and resend".
A hard number from 2024 screenshots.

**Open:** Emails → Sent logs. Tick six and see.

### 16. Hard-bounce suppression: scope, duration, and a support promise

`05/if-your-emails-are-not-arriving.md:38` claims suppression is account-wide, spans
events, persists for years, and that support can release it "the same day". That last is
a service commitment sitting in public docs. The article has no `source_url`, so nothing
corroborates any of it.

**Ask support / Postmark** — not checkable in the UI.

### 17. Email scheduling timezone "cannot be changed"

`05/sending-and-scheduling-emails.md:88`, stated as a Note callout so it reads
authoritative.

**Open:** any manual template → Scheduling. Look for a timezone selector.

### 18. The programme timezone lock

`06/locking-and-change-the-timezone-for-your-conference.md:24` gives one path;
`08-conference-platform/setting-up-your-program-timezones.md:14` gives a different one
for the same panel and says flatly "Your delegates will set their own time zones" with no
mention that you can lock them.

**Open:** Conference → Program → Builder → Settings → Timezone.

### 19. Presenter clashes — carried over from the verification queue

`08/session-bookings.md:37` documents a **Schedule conflict count** column on Bookings,
matching surname + first initial. A July 2026 recording describes a newer warning in the
**programme builder** that a presenter is in two sessions at once. One feature or two?

Also unresolved: `08/session-bookings.md:13` says the Bookings table covers chairs, while
`corpus-internal/programme-builder-sessions-and-publishing.md:30` says chairs are "never
matched to a person of the same name".

**Blocked on the demo event** — it has one empty session, so no clash can occur. Needs an
event with a presenter genuinely scheduled twice.

---

## Tier 3 — labels and smaller claims

Cheap to confirm once somebody is on the right screen; group them by screen rather than
working down the list.

**Emails → Edit & send:** the group headings are "Automatic emails" and "Manually sent
emails" (`05/editing-the-template-emails.md:21` says "Automatic" and "Manual") ·
all-caps button labels throughout the section, including `SEND... EMAILS`, which was
never a real label · whether automatic emails only ever reach submitters, which the
public articles never say.

**Emails → Sent logs:** does **Show bounced messages** exist, top right
(`05/if-your-emails-are-not-arriving.md:23`)? `05/using-the-email-sent-log.md` describes
the same screen and never mentions it.

**Sender email:** the two-email Postmark handshake and its conditional branch
(`05/sending-emails-from-your-chosen-email-address.md:34`) · the default From/Reply-To
headers (`:13` vs the internal note) · the sending-domain list at
`05/what-domains…:22`, which is the article organisers forward to their IT department.

**Reports & downloads:** the section is named three different ways across two articles and
an internal note ("Abstracts as individual files", "question response folders", "File
upload question files") · the 100-file bulk upload cap (`06/other-reports.md:44`) ·
the html/Word/PDF format set (`06/abstract-books.md:25`) · where bespoke books appear
(`06/abstract-books.md:45` vs the internal note).

**Programme builder:** "Preview Mobile App" in the publish dropdown
(`06/viewing-the-mobile-version…:28` — this is the section's Start here article) ·
the embed URL on `virtual.oxfordabstracts.com` (`06/publishing-your-program.md:99`) ·
chairs' "+ ADD ANOTHER CHAIRS" button (`06/adding-chair-s-email-addresses.md:42`) ·
whether the schedule export produces anything but Word (`06/downloading-your-program…:53`
vs the internal note's flat "there is no direct PDF of the programme").

**Decisions → Table:** the **In Titles Page** column, **Bulk decide**, and "Add To Titles
Listing" (`06/adding-a-session-less-submission…:26,88,92`, from 2022 screenshots).

**Registration:** "Mark as paid" vs "Mark payment complete" and the card-details claim
(`07/refunding…:62`) · whether refunds are excluded from the Transactions gross total
(`:97`) · whether the payment-status block duplicated in two files describes one column
or two (`07/managing-orders…:199` vs `07/viewing-transactions…:40`) · ticket groups
versus per-ticket question toggles, described three ways (`07/creating-your-…-tickets:90`,
`07/creating-your-…-form:84`, `07/dependency-questions…:42`) · coupon labels
(`07/creating-coupon-codes…:37`) · the "one fee option" limit
(`07/adding-add-ons…:61`) · whether a ticket holder's name changes automatically
(`07/managing-orders…:193` vs the manual Assign flow in `07/changing-the-email-address…`).

*Confirmed already, 7 August:* the Transactions tab does have an **ORDER OWNER** column,
so `07/buyers-ticket-holders-and-who-receives-what.md:46` is right.

---

## Content gaps — no app access needed, just a decision and some writing

**Missing articles, ranked by how often they will be needed:**

1. **Closing registration / registration deadlines.** Nothing covers ending ticket sales:
   what an attendee sees after a ticket lapses, or how to close registration outright.
   Given what the submissions audit found about deadlines, assume nothing here.
2. **Testing an email before sending it to 400 people.** The internal notes record that a
   test send does not populate merge fields — a trap that produces empty links. No public
   article says so.
3. **Merge fields as a reference.** Six substantial limitations sit in
   `corpus-internal/emails-templates-and-merge-fields.md` and none reach a public page.
4. **The spreadsheet builder and book builder.** No article anywhere, for three tools that
   two other articles currently tell people to email support about. Same as Tier 1 item 4.
5. **Chasing unpaid invoices.** "Pending payment" is defined twice and actioned nowhere.
6. **Cancelling an event / refunding everyone.** With no partial refunds and no bulk
   action documented, an organiser cancelling a 300-person event has no route.
7. **How to build the programme.** Section 06's first group is "Building and publishing
   the programme" and every build-a-session article is in section 08, unlinked.
8. **Sold out and waiting lists**; **comped and invited attendees**; **currency and who
   absorbs the OA fee**; **GDPR erasure as distinct from deleting a registration**.

**Structural, decided in ten minutes each:**

- `06`'s **Start here** is `viewing-the-mobile-version-of-the-program-builder` — 38 lines
  on previewing a mobile view, described in the structure file as "the tour". It is not.
- `05/if-your-emails-are-not-arriving` and `06/downloading-submissions-and-their-files`
  are in no group, so both fall to "Also in this section" at the foot of their section
  page. Both are among the best articles in the corpus.
- `06/locking-and-change-the-timezone…` is two articles under one title — half to
  organisers, half to attendees — and the halves conflict when the lock is on.
- Ghost link text: "Creating exports, reports and abstract books" (twice) and "Cross
  referencing presenters and delegates" name articles that do not exist. They resolve to
  section indexes, so no check catches them.
- Three `07` titles break the sentence-case gerund convention ("Previewing and publish…",
  "Managing orders and edit…", "Registering on the behalf of…"). Renaming changes slugs
  and needs `vercel.json` entries — deliberate or not at all.
- ~349 hand-written jump links remain in `corpus/`. Convert them as you touch each
  article; a bulk sweep risks deleting content that only survives because of them.

**Weak "Common questions" worth rewriting:** `06/abstract-books.md:51` (circular, and
routes to support for self-serve work), `07/managing-orders…:208` (answered only by a
link to an article that does not exist), `07/setting-up-payment-providers…:285` (restates
its own title), `05/creating-custom-emails.md:93,97` (both circular),
`05/sending-emails-from-tables.md:99` (points elsewhere for something the same page
answers).
