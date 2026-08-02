# Staff suggestions — how it works and how to switch it on

A one-page form where anyone at Oxford Abstracts can send Kristy something the help
centre should say. Rows land in the master sheet, on a new **Staff suggestions** tab.

Live at **`/suggest`** once deployed. Nothing else in the repo depends on it, and
`build.py` does not touch this folder.

## Files

| File | What |
|---|---|
| `suggest/index.html` | The whole page. Self-contained — no build step, no shared CSS. |
| `api/suggest.js` | Validates, then forwards to the Apps Script webhook. Holds the roster. |
| `scripts/sheet-logger.gs` | The `Staff suggestions` tab, its dropdown, and the optional email. |
| `assets/img/team/*.webp` | 18 staff photos, 160×160, 129 KB the lot. |

It reuses `SHEET_WEBHOOK_URL` and `SHEET_TOKEN`, which are **already set in Vercel** —
`GET /api/log?check=1` confirms both. No new environment variables, no second store.

## Switching it on — two steps, and the second is the one people skip

1. Open the sheet → **Extensions → Apps Script**, paste the new `sheet-logger.gs`,
   **Save**, then **Run → setup**. This adds the tab. Safe to run again; it does not
   touch existing rows.
2. **Deploy → Manage deployments → pencil → Version: New version → Deploy.**

A web app keeps serving the version it was deployed at, so saving alone changes
nothing the outside world can see. The URL does not change, so Vercel needs no edit.

**Until both steps are done the form refuses honestly rather than lying.** This is
worth understanding, because the obvious version of this feature gets it wrong. The
old deployed script handles `body.row` and `body.feedback`; a suggestion matches
neither, so it falls through to `return out({ok:true})` having written nothing — and
a caller that trusts `ok:true` would thank people for suggestions that went nowhere.

So the script now reports **what it actually stored** (`{ok:true, wrote:['suggestion']}`)
and `api/suggest.js` treats a reply that cannot confirm storing this one as a failure:
*"The suggestions sheet has not been switched on yet, so this was not saved."* The
page keeps every word and offers the copy button. Deploying the page before the script
is therefore safe. Do not relax that check to "ok:true is good enough" — failing
loudly on an un-updated script is the whole point of it.

Optional: set `NOTIFY` at the top of the script to an address to get an email per
suggestion. Empty means no mail. It is sent after the row is written and wrapped in a
try/catch, so a bounce can never cost a suggestion.

## What Kristy gets

Eleven columns: Timestamp, Name, **Team**, Email, Type, Suggestion, Product area,
Article or page, Link, **Status**, **Notes**.

Team is derived from the roster in `api/suggest.js`, never taken from the form, so it
cannot be spoofed or drift out of step with the name. It costs the sender nothing and
tells Kristy where a signal came from — the same suggestion means something different
from Customer Support than from Engineering.

The last two are hers. A new row arrives as `New`, and Status is a dropdown —
`New / Being looked at / Written up / Not needed` — so the tab works as a queue rather
than a dump. The script only ever appends, so nothing she types can be overwritten.

The dropdown is re-extended on every append rather than painted onto a fixed range
once. A 1,000-row range stops applying silently at row 1,001, and a tab that quietly
loses its dropdown is the kind of thing nobody notices for a year.

## The form, and why these fields

Three required — type, the suggestion, and who you are. Everything else is optional
and labelled as such, because a form that feels like paperwork gets one submission a
month.

**You say who you are by clicking your own face.** The 18 photos come from
oxfordabstracts.com/about, cropped square by Storyblok's image service and committed
to `assets/img/team/` — hotlinking them would break the moment marketing reorganises
the about page, and the house rule is that images are committed. Picking a face sets
the name and derives the team.

That is also why **email is optional**: everyone on the wall is someone Kristy can
already reach, so asking for an address is friction that buys nothing. The one branch
that needs it is **"I'm not here"** — a new starter, or anyone the about page has not
caught up with — which reveals a name box, makes email required, and relabels itself
to say why. It must never be a dead end.

**Keeping the roster current:** the names and teams live in `ROSTER` in
`api/suggest.js`, the tiles in `suggest/index.html`, and the photos in
`assets/img/team/`. A joiner or leaver means editing all three. A name in `ROSTER`
with no photo shows a broken circle; a tile whose value is not in `ROSTER` still
submits, but arrives with no team and demands an email, which is a soft failure
rather than a lost suggestion.

**There was a "How often does this come up?" field; it was cut on 2 August 2026** to
keep the form short. If prioritising the queue later turns out to be the hard part,
that is the field to bring back — the argument for it was that this corpus is
prioritised by volume, and frequency is the one thing that cannot be reconstructed
from the text afterwards. Kristy can still ask.

**Screenshots are a link, not an upload** — a decision, not a limitation. A sheet cell
cannot hold an image, and the alternatives (Drive uploads through Apps Script, Vercel
Blob) each add a store, a permission model and a failure mode to a form that gets a
handful of uses a week. The field says to drop the image in Drive or Slack and paste
the link, which is what people already do.

## Two rules from `api/log.js` this deliberately inverts

Both are load-bearing. If either is "tidied" to match the other endpoints, the feature
quietly stops doing its job.

1. **Emails are not scrubbed.** `log.js` strips them because it records anonymous
   reader telemetry read casually and widely. This is a named colleague writing to
   another named colleague, and a suggestion you cannot follow up on is half a
   suggestion. Nothing here is anonymous and nothing pretends to be.

2. **Failure is reported, not swallowed.** `log.js` returns 204 on every path because
   a reader must never see a logging error. Here someone has just typed several
   paragraphs and pressed a button. So the endpoint returns 200 only when the sheet has
   actually taken the row — it reads the Apps Script response body, because a bad token
   comes back as HTTP 200 with `{ok:false}` — and on any failure the page keeps every
   field as typed and offers **Copy what I wrote**.

Every suggestion is also `console.log`ged as `kb-suggestion` before the forward, so
even a total sheet outage leaves a recoverable copy in the Vercel logs.

## Access

Open to anyone with the link, by decision, with `noindex, nofollow` on the page. The
defences are proportionate rather than absolute:

- a honeypot field (`company`) — filled only by bots; the response is a cheerful 200
  and the row is dropped, so nothing is learned by trying again
- per-instance rate limiting, 6 per ten minutes per IP
- hard caps on every string, and closed vocabularies for type and product area

Note that `vercel.json` sets `Access-Control-Allow-Origin: *` for the whole site, so
`/api/suggest` is callable cross-origin. That is consistent with the page being open;
if the sheet ever needs protecting, a shared passphrase checked server-side is about
fifteen lines and the cleanest next step.

## Tested

Verified against the real `api/suggest.js` handler and a stand-in Apps Script:

- empty submit → names the missing field, focus lands on it
- full submit → success panel; payload arrives with **name and email intact**, and
  type/area matching the closed vocabularies exactly
- honeypot filled → 200, no row written
- malformed email, missing fields → 400 naming what is wrong
- unrecognised type → written but marked `(unrecognised)`, so a drifted form is
  visible in the column rather than losing a real suggestion
- 7th post in ten minutes → 429, page keeps the text and offers the copy button
- "Send another" → keeps who you are, clears the rest
- all 19 tiles render, all 18 photos load at 160×160, none broken
- picking a face and leaving email blank → accepted, team derived correctly
- claiming `team: "Chief Executive"` while named Nori → stored as Customer Support;
  the roster wins, the request does not
- "I'm not here" → reveals the name box, relabels email as required, and blocks on
  either being missing without making a request
- `Sebastián` survives the round trip intact (9 chars, U+00E1) — verified in the
  browser, since PowerShell's console mangles it on the way out and it looks broken
  when it is not
- 375px wide → no horizontal overflow; 4 faces per row over 5 rows, 74px tap targets;
  brand values exact (cream `#EDEBE2`, navy `#101C38`, red `#D0432C`, Gloock + Outfit)

The storage-confirmation guard was negative-controlled against all three states a
real script can be in — the fault was injected and confirmed to fail before the fix
was confirmed to pass:

| Apps Script replies | Result |
|---|---|
| `{ok:true}` — the old deployment, wrote nothing | **502**, "has not been switched on yet", nothing stored |
| `{ok:false}` — bad token | **502**, "the sheet did not accept that" |
| `{ok:true, wrote:['suggestion']}` — updated | **200**, row stored |

**Not yet tested end to end against the real sheet** — that needs steps 1 and 2 above
done first. Send one suggestion afterwards and delete the row.
