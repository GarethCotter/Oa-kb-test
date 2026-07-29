/* POST /api/feedback — records article feedback in the function logs.
 * Day-one storage is the Vercel log stream (search "kb-feedback"); swap for a
 * proper store when volume justifies it. */
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();
  try {
    const b = typeof req.body === 'object' ? req.body : JSON.parse(req.body || '{}');
    console.log('kb-feedback', JSON.stringify({
      path: (b.path || '').slice(0, 200),
      helpful: !!b.helpful,
      reason: (b.reason || '').slice(0, 40),
      ts: b.ts || Date.now()
    }));
  } catch (e) { /* malformed beacons are ignored */ }
  return res.status(204).end();
}
