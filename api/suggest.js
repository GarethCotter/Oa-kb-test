/* POST /api/suggest — one staff suggestion for the knowledge base.
 *
 * Backs the form at /suggest. Forwards to the master sheet's "Staff suggestions"
 * tab through the same Apps Script webhook as api/log.js, using the same
 * SHEET_WEBHOOK_URL and SHEET_TOKEN. No new plumbing, no second store.
 *
 * This file deliberately inverts the two rules api/log.js exists to enforce, and
 * the difference is the whole point of it being a separate endpoint:
 *
 *   1. api/log.js STRIPS emails, because it records anonymous reader telemetry
 *      that gets read casually and widely. This is a named colleague writing to
 *      another named colleague about work, and it is useless without a way to go
 *      back and ask "what did you mean?" - so name and email are required and kept
 *      exactly as typed. Nothing here is anonymous and nothing here pretends to be.
 *
 *   2. api/log.js returns 204 on EVERY path, because a reader must never see a
 *      logging error. Here a person has just typed several paragraphs and pressed a
 *      button. Swallowing a failure would silently throw their work away, which is
 *      the worse failure by a wide margin. So this reports honestly: 200 only when
 *      the sheet has actually taken the row, and a real error otherwise, which the
 *      page turns into "that didn't send - here is your text, copy it".
 *
 * The page is open to anyone with the link, by decision. The defences are therefore
 * proportionate rather than absolute: a honeypot field, per-instance rate limiting,
 * and hard caps on every string. A determined person could still post rows; the
 * bar this clears is drive-by bots, and the sheet is not sensitive.
 */

const TYPES = new Set([
  "Something's wrong or out of date",
  "A question we get asked but don't answer",
  'A new or changed feature to document',
  'Something else'
]);

const AREAS = new Set([
  'Not sure', 'Getting started', 'Submissions', 'Reviewing', 'Decisions', 'Emails',
  'Programme & reports', 'Registration', 'Conference platform',
  'Symposia & Certificates', 'Integrations & API', 'Account administration',
  'Submitting (participants)', 'Reviewing (participants)', 'Attending (participants)',
  'More than one / the whole site'
]);

/* The team, from oxfordabstracts.com/about. Two jobs: the team name is derived here
   rather than trusted from the form, so it cannot drift or be spoofed; and being on
   this list is what makes an email address optional, since Kristy can already reach
   anyone on it. Someone not listed - a new starter, or anyone the about page has not
   caught up with - picks "I'm not here", types a name, and must give an email.

   When the about page changes, this list and assets/img/team/ both need the edit.
   A name here with no matching photo just shows a broken circle, so change both. */
const ROSTER = new Map([
  ['Geoff', 'Founder & GM'],
  ['Sandra', 'Accounts'],
  ['Nori', 'Customer Support'],
  ['Diego', 'Customer Support'],
  ['Rory', 'Engineering'],
  ['Finn', 'Engineering'],
  ['Sebastián', 'Engineering'],
  ['Justin', 'Engineering'],
  ['Conor', 'Customer Success'],
  ['Neha', 'Customer Success'],
  ['Angela', 'Customer Success'],
  ['Jen', 'Design'],
  ['Ji', 'Design'],
  ['Farihah', 'Product Management'],
  ['Rosie', 'Product Management'],
  ['Gareth', 'Marketing'],
  ['Kristy', 'Content Manager'],
  ['Lou', 'UX Researcher']
]);

const EMAIL_SHAPE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const clip = (v, n) => String(v == null ? '' : v).trim().slice(0, n);

/* Best-effort, per-instance. Vercel runs several instances and recycles them, so
   this is a speed bump rather than a lock - which is the right size of defence for
   an open page writing to a non-sensitive sheet. */
const HITS = new Map();
const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 6;

function rateLimited(ip) {
  const now = Date.now();
  const seen = (HITS.get(ip) || []).filter(t => now - t < WINDOW_MS);
  seen.push(now);
  HITS.set(ip, seen);
  if (HITS.size > 500) {                       // bounded: never grow without limit
    for (const [k, v] of HITS) if (!v.some(t => now - t < WINDOW_MS)) HITS.delete(k);
  }
  return seen.length > MAX_PER_WINDOW;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'POST only' });

  let b;
  try {
    b = typeof req.body === 'object' && req.body ? req.body : JSON.parse(req.body || '{}');
  } catch {
    return res.status(400).json({ ok: false, error: 'Could not read that submission.' });
  }

  /* The honeypot is a field no human sees and no human fills. Answer 200 so a bot
     that fills it learns nothing and does not come back to try a different shape. */
  if (clip(b.company, 200)) return res.status(200).json({ ok: true });

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (rateLimited(ip)) {
    return res.status(429).json({
      ok: false,
      error: 'That is a lot of suggestions at once. Give it ten minutes and try again.'
    });
  }

  const name = clip(b.name, 80);
  const onRoster = ROSTER.has(name);

  const s = {
    ts: new Date().toISOString(),
    name,
    // Derived, never taken from the request: a client cannot claim a team it is not on.
    team: onRoster ? ROSTER.get(name) : '',
    email: clip(b.email, 120),
    type: clip(b.type, 60),
    text: clip(b.text, 4000),
    section: clip(b.section, 60),
    article: clip(b.article, 300),
    link: clip(b.link, 300)
  };

  // Required fields, named individually so the page can say which one is missing
  // rather than "invalid input".
  const missing = [];
  if (!s.name) missing.push('who you are');
  // Only off-roster senders must leave an address; see the note on ROSTER.
  if (!s.email && !onRoster) missing.push('your email');
  if (!s.type) missing.push('what kind of suggestion this is');
  if (!s.text) missing.push('the suggestion itself');
  if (missing.length) {
    return res.status(400).json({ ok: false, error: 'Still needed: ' + missing.join(', ') + '.' });
  }
  // Optional, but if given it has to be usable - a typo'd address is worse than none,
  // because it looks like a reply route and is not one.
  if (s.email && !EMAIL_SHAPE.test(s.email)) {
    return res.status(400).json({ ok: false, error: 'That email address does not look right.' });
  }

  // Closed vocabularies keep the sheet groupable. An unrecognised value is recorded
  // rather than rejected - losing a real suggestion over a stale dropdown would be
  // the wrong trade - but it is marked so a drifted form is visible in the column.
  if (!TYPES.has(s.type)) s.type = s.type + ' (unrecognised)';
  if (s.section && !AREAS.has(s.section)) s.section = '';

  // Written before the forward, so a suggestion survives even a total sheet outage:
  // search the Vercel logs for "kb-suggestion" to recover one by hand.
  console.log('kb-suggestion', JSON.stringify(s));

  const url = process.env.SHEET_WEBHOOK_URL;
  if (!url) {
    return res.status(503).json({
      ok: false,
      error: 'The suggestions sheet is not connected yet. Your text is safe below — please send it to Kristy directly.'
    });
  }

  try {
    // 8s, not log.js's 5s: there, a reader is mid-search and speed wins. Here
    // someone has pressed Send and is watching, and an Apps Script cold start can
    // take several seconds. Waiting beats losing the row.
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), 8000);
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: process.env.SHEET_TOKEN || '', suggestion: s }),
      signal: ctl.signal
    });
    clearTimeout(t);

    // Apps Script answers 200 with {ok:false} on a bad token, so the status code
    // alone is not proof the row landed. Read the body and believe that instead.
    const body = await r.text();
    let parsed = null;
    try { parsed = JSON.parse(body); } catch { /* non-JSON means something is wrong */ }

    if (!r.ok || !parsed || parsed.ok !== true) {
      console.error('kb-suggestion-failed', r.status, body.slice(0, 300));
      return res.status(502).json({
        ok: false,
        error: 'The sheet did not accept that. Your text is safe below — copy it and we will get it in.'
      });
    }

    /* ok:true is necessary but not sufficient. A deployment of sheet-logger.gs from
       before staff suggestions existed handles body.row and body.feedback, matches
       neither, and falls through to a cheerful ok:true having written nothing - so
       the form would thank people for suggestions that went nowhere. The script now
       reports what it actually stored, and anything that cannot confirm storing this
       one is treated as a failure. Failing loudly on an un-updated script is the
       entire point; do not relax this to "ok:true is good enough". */
    if (!Array.isArray(parsed.wrote) || !parsed.wrote.includes('suggestion')) {
      console.error('kb-suggestion-not-stored', body.slice(0, 300));
      return res.status(502).json({
        ok: false,
        error: 'The suggestions sheet has not been switched on yet, so this was not saved. Your text is safe below — copy it and send it to Kristy directly.'
      });
    }
  } catch (e) {
    console.error('kb-suggestion-error', e.message);
    return res.status(502).json({
      ok: false,
      error: 'Could not reach the suggestions sheet. Your text is safe below — copy it and try again shortly.'
    });
  }

  return res.status(200).json({ ok: true });
}
