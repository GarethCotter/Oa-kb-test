# What each plan includes

*Transcribed 29 July 2026 from the pricing page feature table. This is the source of
truth for the `plan:` value in article frontmatter and for the badge readers see.
Prices are deliberately not recorded here — they go stale, and every pricing answer
should point at oxfordabstracts.com/pricing.*

Four plans, cheapest first: **Free** · **Abstract Management** · **Standard
Conference** · **Professional Conference**. Separately purchased add-ons:
**Symposia**, **Multi-stage**, **Certificates** (Certificates is included with
Professional).

`AM` = Abstract Management, `SC` = Standard Conference, `PC` = Professional Conference.

---

## Abstract management

**On every plan including Free:** unlimited abstracts · custom submission form ·
assign reviewers · online reviewer workspace · track reviewer progress · submit,
review and decide table views · assign roles · default emails.

**AM and above** (i.e. everything except Free): custom review form · custom decision
form · customisable emails · additional notification emails · default abstract books ·
custom abstract books · default reports · custom reports · show reviews to submitters ·
restrict submissions · IEEE incorporation · committee category filter · allow
submission fees · add logo to forms · reduced Oxford Abstracts branding · customise
form design · manage awards, prizes and proposals · additional forms for each author.

## Virtual conference

**Nothing in this section is available on Free or Abstract Management.**

**SC and above:** program/schedule builder · quick links to live video content ·
pre-recorded and on-demand content · include abstracts and posters · allow submitters
to hide their abstracts · set conference time zone · highlight contributors · search
and filter content · conference logo · **Zoom integration**.

**PC only:** custom splash page · comments feature · poster gallery · event chat ·
private chat · group chat · video chat · complete access controls · name badges for
attendees · customise event portal · sponsorship · exhibitor space.

## Delegate registration

**On every plan including Free**, all of it: register delegates with a custom form ·
process payments · multi-level ticket options · delegate table · default emails ·
custom emails · custom coupon codes · integrate with abstract management.

This is worth knowing — registration is often assumed to be a paid extra and is not.

## Support

**On every plan including Free:** online help files · helpdesk support.

## Access

* **Event data access for one year** — every plan, including Free.
* **API access** — AM and above. **Not on Free.**

---

## How this maps to the `plan:` frontmatter value

| Frontmatter value | Badge shown | Use for |
|---|---|---|
| `all plans (including free Basic)` | *(no badge)* | anything in the Free column above |
| `abstract management and above` | Abstract Management and above | the AM-and-above list, plus API |
| `standard conference` | Conference plans | the SC-and-above virtual conference list |
| `professional conference` | Professional Conference | the PC-only list |
| `add-on: symposia` | Symposia add-on | symposia content |
| `add-on: multi-stage` | Multi-stage add-on | multi-stage content |
| `add-on: certificates (included in Professional)` | Certificates add-on | certificates content |

Note `abstract management` and `abstract management and above` both existed in the
corpus and produce the same badge; the longer form is now used throughout so the badge
text and the value agree.

## Still unresolved

The feature table does not name these individually, so the plan value for them is a
judgement call nobody has made yet:

* **The four third-party integration articles** — EventsAir, Cvent, idloom, Swapcard.
  They are presumably API-driven, which would make them Abstract Management and above,
  since API access is not on Free. Currently marked as available on all plans.
* **Creating your event website.** The website builder is not a row in the table. The
  closest rows are *conference logo* (SC and above) and *customise event portal* /
  *custom splash page* (PC only), which point in different directions. Currently marked
  Professional.
