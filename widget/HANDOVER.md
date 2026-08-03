# In-app help widget — handover for the Oxford Abstracts engineer

Everything on our side is built, deployed and tested; what remains needs access to
the app's pages, which is why it is coming to you. Expected effort per page:
**one config line and one script include.**

## What this is

A Help launcher (bottom-right, navy pill) on every admin screen. It opens one panel
called **Help** — deliberately not Home/Ask-AI tabs — where the admin asks in their
own words and gets a plain-English answer from the help centre's answer layer
(`/api/search`, two Claude Haiku calls over the 174-article corpus), with the guides
it drew from cited underneath. Cited guides open **inside the panel** — the live KB
page, re-rooted — so there is no second copy of any article to drift out of date.

**The panel opens on a topic screen, not straight into conversation.** Six doors
under "What do you need a hand with?" — five lifecycle topics plus **Something
else**, always last, which carries no routing hint and exists so nobody stares at
five wrong labels. The door matching the current screen is listed first and badged
"You're here", and the ask bar stays live underneath, so a formed question skips
the doors entirely. Reopening mid-conversation returns to the conversation — the
doors are an entrance, not a toll booth.

**A chosen door opens onto an intro card, not the bare chat**: a deliberately
shiny navy card — topic pill, twinkling stars — saying this chat searches
everything we have ever recorded and answers in seconds, and to ask as though
speaking to a real person. It looks nothing like the plain conversation on
purpose, and it collapses away the moment the first question is sent. The chosen
topic rides on the front of the question as routing context, exactly as the
screen name does.

**Suggested questions are currently out of the flow** (a deliberate call, not an
omission — this version leads with the person's own words). The verified question
sets remain in the file marked PARKED: every entry was checked to answer
confidently against the live corpus, and that verification is the expensive part
of bringing them back.

The answering surface is titled **"Instant answers"** — deliberately not "AI chat"
or similar. Users pre-judge "AI chat" as useless; this one is not, and the name
sells the outcome rather than the technology.

The one thing each page must tell it is **which screen it is on**. That context
rides on the front of the question and measurably improves answer routing, selects
the per-screen suggested questions, and picks which door gets the badge.

Live demo (fake admin app around the real widget):
https://oa-kb-test.vercel.app/prototype/admin-help
Test harness wired to the real script and real API:
https://oa-kb-test.vercel.app/widget/test-page

Both pages load the same `/widget/help-widget.js`, so neither can drift from the
shipped behaviour again — the prototype used to carry its own inline copy of the
widget, which is exactly how it fell behind once already. The widget now carries
the prototype's visual language itself (Gloock/Outfit, cream panel, the round red
send, the always-visible Raise-a-support-ticket button, voice input) and injects
the Google Fonts link on pages that do not already load those fonts.

## Files

| File | What |
|---|---|
| `help-widget.js` (this folder; also served at `https://oa-kb-test.vercel.app/widget/help-widget.js`) | The whole feature. No dependencies, no build step, styles injected, everything namespaced `oahw-`. |
| `test-page.html` | Stand-alone harness — real script, real API, screen switcher, event console. |

Copy `help-widget.js` into the app's codebase rather than hot-linking, so the app has
no runtime dependency on our hosting. (Hot-linking works for a trial.)

## Integration

On each admin page, before `</body>`:

```html
<script>
window.OA_HELP = {
  endpoint: 'https://oa-kb-test.vercel.app',   // becomes help.oxfordabstracts.com later
  kbBase:   'https://oa-kb-test.vercel.app/',
  screen:   'Emails'        // <- the page's screen name; see the list below
};
</script>
<script src="/path/to/help-widget.js"></script>
```

`screen` should be one of the names the suggestions map knows — Dashboard,
Event setup, Emails, Abstract Management, Symposium, Speaker Management,
Website Builder, Registration, Conference, Certificates — or any other string
(unknown screens still work; they get generic suggestions and the context line
still helps routing). In a SPA, set `window.OA_HELP.screen` on route change; the
next question picks it up automatically.

Optional config: `ticketUrl` (default: the contact-support page), `suggestions`
(override the per-screen question map), `topics` (override the six doors — each is
`{key, label, hint, icon, qs}`; every question in `qs` must return a confident
answer from the live corpus, which is a checked rule, not a style preference),
`zIndex`, `enabled: false` (kill switch — removing the script tag is the other
one), `onEvent(name, detail)` (hook for your own analytics).

If the app's CSP restricts `connect-src`, allow `https://oa-kb-test.vercel.app`.
CORS is already open server-side for `app.oxfordabstracts.com`,
`oxfordabstracts.com`, `www.` and any `localhost` port; the KB's static pages also
send `Access-Control-Allow-Origin: *` so the in-panel reader can fetch article HTML.

## Behaviour that is deliberate (please do not soften)

- **Never a dead end, never a visible error.** An outage or a weak answer both look
  the same: an honest "I couldn't find a confident answer", with the KB search and
  the support form one tap away. The endpoint's `confidence` field decides;
  the bot never shows a guess.
- **After every answer: "This solved it" / "This didn't help me"** — the same
  verdict pair as the KB search, same wording, sage tick / muted cross. "Didn't
  help" apologises, flags the answer for review (true — it lands in the log), and
  offers the ticket.
- **No admin UI.** Questions the bot cannot answer are logged; a human writes a
  short note into the KB's internal corpus and commits. The file system is the
  answer queue.

## What gets measured (already wired)

Each interaction POSTs a row to `/api/log` (fire-and-forget, never affects the
reader; emails/phone numbers stripped server-side). Rows land in the
"Help Dashboard" Google Sheet, `Log` tab, surface `widget`, with the screen name
in its own column:

| Event | Meaning |
|---|---|
| `asked` | a question completed; `Answered` column says whether an answer was shown |
| `solved` / `unhelpful` | verdict clicks |
| `opened_article` | a cited guide was opened in the panel |
| `ticket_created` | clicked through to the support form |

When a door was chosen, it rides in the screen column as
`Emails · Registration & payments` — no schema change, and the sheet can group by
it to show which topics people reach for against which screens they stand on.

The dashboard's Widget column and answer/success rates fill in automatically.

## Known limitation (documented, not a bug)

Multi-turn memory is one exchange deep: the previous question rides along as a
prefix inside the 500-character cap. Proper multi-turn needs the endpoint to accept
structured history — that is a planned change on our side and needs nothing from
you now.

## Testing checklist

On https://oa-kb-test.vercel.app/widget/test-page (or locally — CORS allows localhost):

- [ ] Open Help → the topic doors, Emails first with a "You're here" badge,
      Something else last, ask bar live below. No suggested questions anywhere.
- [ ] Click a door (say Registration & payments) → the shiny intro card with the
      topic as a pill; send a question → the card collapses and the conversation
      begins, with asked rows logging the screen as
      `Emails · Registration & payments`.
- [ ] Type a question on the doors screen without picking one → straight into the
      conversation; no door, no intro card.
- [ ] ‹ back returns to the doors; close and reopen mid-conversation returns to
      the conversation, not the doors.
- [ ] Ask "why have my submitters not received my email" → answer with bolded menu
      paths, two cited guides, verdict buttons.
- [ ] Click a cited guide → article opens inside the panel; Back returns to the
      conversation; "Open in the help centre" goes to the real page.
- [ ] Click "This didn't help me" → apology + Create support ticket chip.
- [ ] Ask "do you sell conference lanyards" → honest miss, KB search + ticket chips.
- [ ] Devtools offline, ask anything → same honest miss, no visible error.
- [ ] Switch the pretend screen and ask again → the event console shows the new
      screen on the logged rows.

Test rows appear in the interaction-log sheet under surface `widget` — delete them
after testing.

## Who to talk to

Repo: https://github.com/GarethCotter/Oa-kb-test — this folder, `api/search.js` and
`api/log.js` are the moving parts. Gareth owns the product behaviour; changes to the
deliberate behaviours above should go through him.
