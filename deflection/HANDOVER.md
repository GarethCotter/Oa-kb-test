# Ticket deflection — handover for the Oxford Abstracts engineer

Everything on our side is built, deployed and tested. What remains needs access to
the live contact-support page, which is why it is coming to you. Expected effort:
**one script include and four selectors**, then testing.

## What this is

When someone submits the support form, their question (ticket name + description) is
run against the help centre's answer layer (`/api/search` — two Claude Haiku calls
over the 174-article corpus). If — and only if — a **strong** answer exists, it is
shown once, with two buttons: **That's solved it** and **Send my ticket anyway**.

Live demo of the finished behaviour: https://oa-kb-test.vercel.app/prototype/support-deflection
Test harness wired to the real script and real API: https://oa-kb-test.vercel.app/deflection/test-form

Three product rules are load-bearing. Please don't soften them in integration:

1. **Never show a confidence percentage.** The endpoint decides strong/weak; the
   reader never sees a number.
2. **Never block the send.** One click past the answer, always. On any error,
   timeout (2.5s cap) or weak answer, the ticket goes through exactly as if the
   script did not exist. The failure mode of this feature is "nothing happens".
3. **One interruption per form, ever.** After "Send my ticket anyway", the script
   never fires again on that page.

## Files

| File | What |
|---|---|
| `deflect.js` (this folder, also served at `https://oa-kb-test.vercel.app/deflection/deflect.js`) | The whole feature. No dependencies, no build step, all styles injected and namespaced `oadf-`. |
| `test-form.html` | Stand-alone harness — real script, real API, pretend sender, event console. |

Copy `deflect.js` into your codebase rather than hot-linking it, so your page has no
runtime dependency on our hosting. (Hot-linking works for a trial.)

## Integration steps

1. On the contact-support page, before `</body>`:

   ```html
   <script>
   window.OA_DEFLECT = {
     endpoint: 'https://oa-kb-test.vercel.app',   // becomes help.oxfordabstracts.com later
     kbBase:   'https://oa-kb-test.vercel.app/',
     formSelector:    '#yourFormId',
     subjectSelector: '[name="TICKET.subject"]',   // or your input's id
     contentSelector: '[name="TICKET.content"]',
     submitSelector:  'button[type=submit]'
   };
   </script>
   <script src="/path/to/deflect.js"></script>
   ```

2. That's the integration. The script listens for `submit` in the capture phase,
   shows the check/answer UI in a `div` it inserts **after the form**, and when the
   ticket should really send it calls `form.requestSubmit()` — your existing submit
   handling runs unchanged.

3. If your page's CSP restricts `connect-src`, allow `https://oa-kb-test.vercel.app`.

4. CORS is already handled server-side: our endpoints accept
   `https://oxfordabstracts.com`, `https://www.oxfordabstracts.com`,
   `https://app.oxfordabstracts.com`, and any `localhost` port for your local testing.
   If the form lives on another origin (e.g. a HubSpot-hosted page), tell us the
   origin and we add it — one line.

## Things that vary by how the form is built

- **Custom form posting to the HubSpot API** (what the prototype assumes): works as
  above, nothing else needed.
- **HubSpot embedded form rendered inline** (`hbspt.forms.create`, classic embed):
  works, but set the selectors to HubSpot's generated names
  (`[name="TICKET.subject"]` etc.) and load `deflect.js` in HubSpot's `onFormReady`
  callback so the fields exist first.
- **HubSpot form inside an iframe** (newer embeds default to this): a page script
  cannot reach inside the iframe. Two options: switch the embed to inline rendering,
  or tell us — the deflection UI would need to sit outside the iframe using
  HubSpot's form events API, which is a different (still small) integration.

- **Attaching what was suggested**: when a ticket is sent after an answer was shown,
  the script appends a plain-text block to the description field —
  suggested article titles, URLs, and `Outcome: sent anyway` — so support sees what
  the reader already tried. That needs no schema change. If you'd rather it in a
  dedicated ticket property, set `attachToContent: false` and read
  `window.OA_DEFLECT` state in your own submit handler.

## What gets measured (already wired)

Each interaction POSTs one row to `/api/log` (fire-and-forget; never affects the
reader; emails/phone numbers stripped server-side). Rows land in the
"Help Dashboard" Google Sheet, `Log` tab, surface `ticket-form`:

| Event | Meaning |
|---|---|
| `asked` | question ran; `Answered` column says if a strong answer existed |
| `solved` | reader clicked "That's solved it" — **a deflected ticket** |
| `sent_anyway` | answer shown, ticket sent regardless — the answer failed |
| `not_interrupted` | no strong answer, ticket went straight through |

Deflection rate = solved ÷ (solved + sent_anyway). The dashboard tab computes this
weekly ("Form deflected" / "Sent anyway" columns).

## The confidence signal (server-side, nothing for you to do)

`/api/search` returns `confidence: "strong" | "weak"` alongside the answer. Strong
requires the model to self-report that the guides directly answer the question, AND
no hedging language, AND a substantive answer. `deflect.js` interrupts only on
`strong`, and treats a missing field (older cached responses) as weak.

## Testing checklist

On https://oa-kb-test.vercel.app/deflection/test-form (or locally — CORS allows localhost):

- [ ] Covered question ("my reviewers cannot see their assigned submissions") →
      answer card appears; "That's solved it" ends with no send; event console shows
      `solved`.
- [ ] Repeat, click "Send my ticket anyway" → pretend send fires, description gains
      the attached-suggestions block, console shows `sent_anyway`.
- [ ] Uncovered question ("do you sell conference lanyards") → brief check, ticket
      goes straight through, console shows `not_interrupted`.
- [ ] Kill the network (devtools offline) and submit → ticket goes through, no error
      visible anywhere.
- [ ] Set `enabled: false` in the config → script is inert. This is the kill switch;
      removing the script tag is the other one.

Test rows appear in the interaction-log sheet under surface `ticket-form` — delete
them after testing.

## Who to talk to

The repo is https://github.com/GarethCotter/Oa-kb-test — this folder, `api/search.js`
and `api/log.js` are the moving parts. Gareth owns the product behaviour; changes to
the three rules above should go through him.
