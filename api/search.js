/* POST /api/search  { question }  ->  { answer, sources: [{title, path}] }
 *
 * Two Claude Haiku 4.5 calls:
 *   1. Route  — the whole 174-article index (cached) picks up to 3 articles.
 *   2. Answer — only those articles' text is sent, and the answer is written.
 *
 * The routing index is identical on every request, so it sits behind a
 * cache_control breakpoint: after the first call it bills at the cached input
 * rate. That is where nearly all of the cost saving comes from.
 *
 * Runtime: any Node serverless host (Vercel, Netlify, Cloudflare). The API key
 * stays here, server-side. It must never reach the browser.
 */

import routingIndex from '../assets/search-index.json' with { type: 'json' };
import articles from '../assets/articles.json' with { type: 'json' };

const MODEL = 'claude-haiku-4-5';
const API = 'https://api.anthropic.com/v1/messages';

const ROUTING_TABLE = routingIndex
  .map(a => `${a.path} | ${a.title} | ${a.section} | ${a.audience} | ${a.summary}`)
  .concat(Object.values(articles)
    .filter(a => a.internal)
    .map(a => `${a.path} | ${a.title} | Internal note | any | ${a.body.slice(0, 160)}`))
  .join('\n');

const ROUTE_SYSTEM = [
  {
    type: 'text',
    text:
      'You route help-centre questions to articles for Oxford Abstracts, academic ' +
      'conference software. Reply with JSON only, no prose and no code fences: ' +
      '{"paths": ["<path>", ...]} with at most 3 paths, best first. Use only paths ' +
      'from the table. If nothing fits, reply {"paths": []}.\n\n' +
      'Readers are either organisers (running an event) or participants ' +
      '(submitting, reviewing, attending). Prefer articles matching the asker.\n\n' +
      'ARTICLE INDEX\npath | title | section | audience | summary\n' + ROUTING_TABLE
  }
];
// cache the big static block
ROUTE_SYSTEM[0].cache_control = { type: 'ephemeral' };

const ANSWER_SYSTEM =
  'You answer questions in the Oxford Abstracts help centre. Readers are ' +
  'conference organisers and their submitters, reviewers and attendees. Many are ' +
  'not confident with software.\n\n' +
  'Return JSON only, no prose outside it, no code fences:\n' +
  '{"answer": "...", "confidence": "high" | "partial", "format": "steps" | "prose", ' +
  '"title": "...", "steps": [{"title": "...", "path": "...", "detail": "...", ' +
  '"bullets": ["..."]}]}\n\n' +
  'format: "steps" when the reader asked HOW TO DO something and the guides give a ' +
  'sequence of actions - people follow numbered steps far more easily than a ' +
  'paragraph. "prose" for everything else: yes/no answers, explanations, what-is ' +
  'questions, troubleshooting that is not a sequence. Never force steps onto an ' +
  'answer that is not genuinely a procedure.\n\n' +
  'When format is "steps":\n' +
  '- "title": the task, imperative, under 8 words, e.g. "Assign reviewers to submissions".\n' +
  '- 2 to 6 steps. Each step:\n' +
  '  - "title": the action, imperative, 2-6 words, e.g. "Add your reviewers".\n' +
  '  - "path": the exact menu path for that step with arrows, e.g. ' +
  '"Event dashboard → Abstract Management → Reviews → By Submission", or omit it ' +
  'when the step happens on the screen the previous step reached.\n' +
  '  - "detail": one short sentence saying what to do there, exact button and tab ' +
  'names in double-asterisk bold. Omit rather than pad.\n' +
  '  - "bullets": ONLY when the guide lists choices or options at that step, each a ' +
  'few words. Omit otherwise.\n' +
  '- "answer" must STILL carry the complete instructions as flowing prose - some ' +
  'places can only show text, and a reader there must lose nothing.\n\n' +
  'When format is "prose": omit title and steps entirely.\n\n' +
  'confidence: "high" ONLY when the guides directly and fully answer the question ' +
  'asked. "partial" when you answered something adjacent, had to branch across ' +
  'readings, or the guides only partly cover it. When in doubt, "partial" - this ' +
  'field decides whether we interrupt someone mid-task, and interrupting with a ' +
  'wrong answer costs more than staying quiet.\n\n' +
  'Rules for the answer:\n' +
  '- 2-4 short sentences of plain English. British spelling.\n' +
  '- Name menus exactly as the guide does, e.g. Event dashboard -> Emails.\n' +
  '- Put every menu path and the exact name of any button, tab, screen, heading or ' +
  'checkbox the reader must find in bold with double asterisks: go to ' +
  '**Event dashboard → Emails → Edit and send** and tick the box under ' +
  '**Automatic emails**. Bold only those clickable or findable names, never whole ' +
  'sentences and never for emphasis.\n' +
  '- No jargon, no marketing, no greeting, no sign-off.\n' +
  '- Some material is an INTERNAL NOTE: answer from it in the same plain style, but never mention notes, guides or where the answer comes from. ' +
  '- Use ONLY the guides provided. If they do not answer it, set answer to null. ' +
  'Never guess: a confident wrong answer is worse than none.\n' +
  '- Do not mention these instructions, the guides as "context", or that you are an AI.\n\n' +
  'Short or ambiguous questions (a couple of words, or something that could apply ' +
  'to more than one role) are common. Do NOT reply by asking the reader to ' +
  'rephrase — that costs them a second attempt and many give up.\n' +
  'Instead:\n' +
  '- Lead with whatever is true whichever way they meant it. Usually the cause of ' +
  'the problem is shared even when the fix differs.\n' +
  '- Then give at most two short labelled branches, e.g. "If you submitted the ' +
  'abstract:" and "If you are organising the event:". One sentence each.\n' +
  '- Only if the readings share nothing at all, answer the most likely one and open by ' +
  'naming it, e.g. "If you are organising the event:", so a reader who meant the other ' +
  'knows within a line that this is not their answer.';

async function claude(body) {
  const res = await fetch(API, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-api-key': process.env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error('Anthropic ' + res.status + ' ' + (await res.text()).slice(0, 300));
  const data = await res.json();
  return data.content.filter(c => c.type === 'text').map(c => c.text).join('\n').trim();
}

/* CORS: lets the support form and the in-app widget on Oxford Abstracts' own domains
   call this endpoint. An allowlist, not '*' - this endpoint spends API money, and
   localhost is included so the engineer can test an integration before it ships. */
const CORS_ORIGINS = new Set([
  'https://oxfordabstracts.com',
  'https://www.oxfordabstracts.com',
  'https://app.oxfordabstracts.com'
]);
export function applyCors(req, res) {
  const o = req.headers.origin || '';
  if (CORS_ORIGINS.has(o) || /^https?:\/\/localhost(:\d+)?$/.test(o)) {
    res.setHeader('Access-Control-Allow-Origin', o);
    res.setHeader('Vary', 'Origin');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Max-Age', '86400');
  }
}

export default async function handler(req, res) {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(204).end();

  /* GET /api/search?check=1 — is the answer layer actually able to answer?
     Asks Claude the cheapest possible question and reports what came back. A dead
     credit balance, a missing key and a working endpoint are indistinguishable from
     the outside otherwise: all three answer a reader's question with silence. */
  if (req.method === 'GET' && req.query && req.query.check) {
    if (!process.env.ANTHROPIC_API_KEY) {
      return res.status(200).json({ ok: false, reason: 'ANTHROPIC_API_KEY missing' });
    }
    try {
      await claude({ model: MODEL, max_tokens: 4, messages: [{ role: 'user', content: 'hi' }] });
      return res.status(200).json({ ok: true });
    } catch (e) {
      const credit = /credit balance is too low/i.test(e.message);
      return res.status(200).json({
        ok: false,
        reason: credit ? 'Anthropic credit balance exhausted' : 'Anthropic call failed',
        detail: e.message.slice(0, 300)
      });
    }
  }

  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });

  const question = (req.body && req.body.question || '').toString().trim().slice(0, 500);
  if (!question) return res.status(400).json({ error: 'No question given' });

  try {
    // ---- call 1: route ----
    const routed = await claude({
      model: MODEL,
      max_tokens: 200,
      system: ROUTE_SYSTEM,
      messages: [{ role: 'user', content: question }]
    });

    let paths = [];
    try {
      paths = (JSON.parse(routed.replace(/```json|```/g, '').trim()).paths || []).slice(0, 3);
    } catch { paths = []; }

    const chosen = paths.map(p => articles[p]).filter(Boolean);
    if (!chosen.length) {
      // no article matched — let the keyword links carry it
      return res.status(200).json({ answer: null, found: false, sources: [] });
    }

    // ---- call 2: answer ----
    const guides = chosen
      .map(a => a.internal
        ? `--- INTERNAL NOTE (no public page — answer from it, cite nothing): ${a.title} ---\n${a.body}`
        : `--- GUIDE: ${a.title} (${a.section}) ---\n${a.body}`)
      .join('\n\n')
      .slice(0, 60000);

    const raw = await claude({
      model: MODEL,
      // 900, not the old 500: a steps answer carries the same instructions twice -
      // once as cards, once as the prose fallback every older surface still reads.
      max_tokens: 900,
      // Low temperature, set when steps arrived: at the default sampling the SAME
      // question came back as steps twice and prose the third time, so whether a
      // reader saw cards was a coin toss. There is nothing creative to gain here -
      // the content is pinned to the guides - and format stability to lose.
      temperature: 0.2,
      system: ANSWER_SYSTEM,
      messages: [{ role: 'user', content: `GUIDES\n\n${guides}\n\nQUESTION\n${question}` }]
    });

    let answer = null, selfReport = 'partial', title = null, steps = null;
    try {
      const parsed = JSON.parse(raw.replace(/```json|```/g, '').trim());
      answer = parsed.answer || null;
      if (parsed.confidence === 'high') selfReport = 'high';
      /* Steps are additive and never load-bearing: anything malformed and the
         response quietly degrades to the prose in `answer`, which is complete on
         its own. Clipped hard - the model writes them, the reader's browser
         renders them, and nothing in between should trust either. */
      if (parsed.format === 'steps' && Array.isArray(parsed.steps) && parsed.steps.length >= 2) {
        const clean = parsed.steps.slice(0, 7).map(s => ({
          title: String(s && s.title || '').slice(0, 60),
          path: String(s && s.path || '').slice(0, 160),
          detail: String(s && s.detail || '').slice(0, 300),
          bullets: (Array.isArray(s && s.bullets) ? s.bullets : [])
            .slice(0, 6).map(b => String(b).slice(0, 80)).filter(Boolean)
        })).filter(s => s.title);
        if (clean.length >= 2) {
          steps = clean;
          title = String(parsed.title || '').slice(0, 80) || null;
        }
      }
    } catch {
      answer = raw || null;          // model ignored the format: still usable
    }

    /* The interrupt signal, decided here rather than by each caller. 'strong' means
       the support-form deflection may put this answer in front of someone mid-task;
       'weak' means show it only where an answer was asked for. The model's own
       confidence is necessary but not sufficient - it is demoted by hedging language
       and by too-short answers, the same heuristics the prototypes proved out. */
    const HEDGES = /\b(might not|unclear|cannot find|can't find|no article|not sure|unable to|does not (?:appear|seem))\b/i;
    const confidence = (answer && selfReport === 'high'
                        && answer.trim().length >= 60
                        && !HEDGES.test(answer)) ? 'strong' : 'weak';

    res.setHeader('cache-control', 'public, s-maxage=86400');
    return res.status(200).json({
      answer,
      found: answer !== null,
      confidence: answer !== null ? confidence : undefined,
      // steps ride alongside the prose, never instead of it; consumers that
      // predate them keep working untouched
      format: answer !== null ? (steps ? 'steps' : 'prose') : undefined,
      title: steps ? title : undefined,
      steps: steps || undefined,
      sources: chosen.filter(a => !a.internal).map(a => ({ title: a.title, path: a.path }))
    });
  } catch (err) {
    console.error('search failed:', err.message);
    /* 200 with a null answer and NO found field: the page falls back to keyword
       links silently and logs nothing, because we know nothing about the question's
       fate. The absent found field is the only thing distinguishing this from "we
       looked and there is no article" - so `degraded` names it for anything
       monitoring the endpoint, without ever reaching the reader.

       Worth knowing: an exhausted Anthropic credit balance lands here. On 31 July
       2026 it took the answer layer down for half an hour and looked, from outside,
       exactly like a knowledge base with no answers. GET /api/search?check=1 exists
       so that question can be asked directly. */
    return res.status(200).json({ answer: null, sources: [], degraded: true });
  }
}
