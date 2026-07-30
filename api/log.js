/* POST /api/log — one row per interaction, from every surface.
 *
 * Body: { surface, screen, question, answered, sources[], action }
 *   surface   kb-search | widget | ticket-form
 *   screen    the admin screen the widget was opened on ('' elsewhere)
 *   question  the reader's own words
 *   answered  true when a confident answer was shown
 *   sources   article paths shown
 *   action    asked | solved | unhelpful | ticket_created | sent_anyway |
 *             not_interrupted | opened_article | followup | none
 *
 * 'asked' is one row per completed question from any surface (answered says whether
 * an answer was shown); everything else is a subsequent event on that question.
 * The master sheet's Dashboard tab computes all of its numbers from these rows.
 *
 * Forwards to a Google Sheet via an Apps Script web app (see scripts/sheet-logger.gs).
 * Set SHEET_WEBHOOK_URL and SHEET_TOKEN in Vercel's environment variables. With no
 * webhook configured it still logs to the Vercel stream, so this is safe to deploy
 * before the sheet exists.
 *
 * Two rules this file exists to enforce:
 *   1. Never store who asked. Emails and phone-shaped numbers are stripped from the
 *      question before it goes anywhere. This data gets read casually and widely.
 *   2. Never let logging affect the reader. Every path returns 204, including
 *      malformed bodies and a dead webhook.
 */

const EMAIL = /[\w.+-]+@[\w-]+\.[\w.-]+/g;
const PHONE = /\+?\d[\d\s().-]{7,}\d/g;

const scrub = s => String(s || '')
  .replace(EMAIL, '[email removed]')
  .replace(PHONE, '[number removed]')
  .slice(0, 500)
  .trim();

const ACTIONS = new Set(['asked', 'solved', 'unhelpful', 'ticket_created',
                         'sent_anyway', 'not_interrupted', 'opened_article',
                         'followup', 'none']);

export default async function handler(req, res) {
  /* GET /api/log?check=1 — is the sheet wired up? Reports only whether each
     variable is present and, on ?check=ping, what the webhook actually answered.
     Never returns the URL or the token. Exists because every failure path here is
     deliberately silent, which is right for readers and hopeless for diagnosis. */
  if (req.method === 'GET' && req.query && req.query.check) {
    const url = process.env.SHEET_WEBHOOK_URL;
    const out = {
      webhookUrl: url ? 'set' : 'MISSING',
      webhookHost: url ? new URL(url).host : null,
      urlEndsWithExec: url ? url.endsWith('/exec') : null,
      token: process.env.SHEET_TOKEN ? 'set' : 'MISSING'
    };
    if (req.query.check === 'ping' && url) {
      try {
        const r = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            token: process.env.SHEET_TOKEN || '',
            row: { ts: new Date().toISOString(), surface: 'kb-search', screen: '',
                   question: 'CONNECTION TEST - safe to delete', answered: true,
                   sources: '', action: 'asked' }
          })
        });
        out.ping = { status: r.status, body: (await r.text()).slice(0, 300) };
      } catch (e) {
        out.ping = { error: e.message };
      }
    }
    return res.status(200).json(out);
  }

  if (req.method !== 'POST') return res.status(405).end();

  let row = null;
  try {
    const b = typeof req.body === 'object' ? req.body : JSON.parse(req.body || '{}');
    row = {
      ts: new Date().toISOString(),
      surface: ['kb-search', 'widget', 'ticket-form'].includes(b.surface) ? b.surface : 'unknown',
      screen: String(b.screen || '').slice(0, 60),
      question: scrub(b.question),
      answered: b.answered === true,
      sources: (Array.isArray(b.sources) ? b.sources : []).slice(0, 3)
        .map(s => String(s && s.path ? s.path : s).slice(0, 160)).join(' | '),
      action: ACTIONS.has(b.action) ? b.action : 'none'
    };
  } catch {
    return res.status(204).end();          // malformed beacons are ignored
  }

  if (!row.question) return res.status(204).end();
  console.log('kb-log', JSON.stringify(row));

  const url = process.env.SHEET_WEBHOOK_URL;
  if (url) {
    try {
      // Bounded: a slow sheet must never hold the reader's request open.
      const ctl = new AbortController();
      // 5s, not 2.5: an Apps Script web app that has not been hit recently cold-starts
      // for several seconds, and aborting mid-flight loses the row.
      const t = setTimeout(() => ctl.abort(), 5000);
      await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: process.env.SHEET_TOKEN || '', row }),
        signal: ctl.signal
      });
      clearTimeout(t);
    } catch {
      // Already in the Vercel stream above, so nothing is lost that matters.
    }
  }

  return res.status(204).end();
}
