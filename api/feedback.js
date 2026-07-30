/* POST /api/feedback — records article-page feedback (the Yes/No under each guide).
 *
 * Forwards to the master sheet's "Article feedback" tab via the same Apps Script
 * webhook as api/log.js, and always also logs to the Vercel stream (search
 * "kb-feedback"), so nothing is lost if the webhook is down or not yet configured.
 *
 * Same two rules as api/log.js: nothing about who clicked is stored, and logging
 * must never affect the reader - every path returns 204. */
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  let fb = null;
  try {
    const b = typeof req.body === 'object' ? req.body : JSON.parse(req.body || '{}');
    fb = {
      ts: new Date().toISOString(),
      path: String(b.path || '').slice(0, 200),
      helpful: b.helpful === true,
      reason: String(b.reason || '').slice(0, 40)
    };
  } catch (e) {
    return res.status(204).end();          // malformed beacons are ignored
  }

  if (!fb.path) return res.status(204).end();
  console.log('kb-feedback', JSON.stringify(fb));

  const url = process.env.SHEET_WEBHOOK_URL;
  if (url) {
    try {
      // Bounded: a slow sheet must never hold the reader's request open.
      const ctl = new AbortController();
      const t = setTimeout(() => ctl.abort(), 2500);
      await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: process.env.SHEET_TOKEN || '', feedback: fb }),
        signal: ctl.signal
      });
      clearTimeout(t);
    } catch {
      // Already in the Vercel stream above, so nothing is lost that matters.
    }
  }

  return res.status(204).end();
}
