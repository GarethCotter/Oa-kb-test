/* Oxford Abstracts Help Centre — search
 *
 * Two layers, deliberately:
 *   1. Keyword search over assets/search-index.json. No backend, always works.
 *   2. A plain-English answer from /api/search, shown ABOVE the keyword links.
 *
 * If the answer endpoint is missing, slow or erroring, layer 1 still answers.
 * The user never sees a dead end, and never sees an error message about an API.
 */

const ANSWER_ENDPOINT = '/api/search';   // set to null to run keyword-only
const ANSWER_TIMEOUT_MS = 8000;

let INDEX = [];
const indexReady = fetch('assets/search-index.json')
  .then(r => r.json())
  .then(d => { INDEX = d; })
  .catch(() => { INDEX = []; });

const form = document.getElementById('searchForm');
const input = document.getElementById('searchInput');
const box = document.getElementById('results');
const list = document.getElementById('resultsList');
const rtitle = document.getElementById('resultsTitle');

/* ---------- layer 1: keyword ---------- */

const STOP = new Set(['the','and','for','how','can','you','your','with','what','why',
                      'does','from','are','was','been','this','that','into','when','where','del']);

// user vocabulary -> corpus vocabulary (from the failing HubSpot search terms)
const SYNONYMS = {
  deadline: ['closing', 'close', 'submissions'],
  deadlines: ['closing', 'close', 'submissions'],
  incomplete: ['submissions', 'table', 'mandatory'],
  template: ['templates', 'emails'],
  templates: ['template', 'emails'],
  save: ['saving', 'automatically'],
  register: ['registration'],
  registering: ['registration'],
  ticket: ['tickets', 'registration'],
  poster: ['posters', 'gallery'],
  invoice: ['invoices', 'receipts'],
  receipt: ['receipts', 'invoices'],
  refund: ['refunding', 'refunds'],
  feedback: ['reviews', 'comments'],
  withdraw: ['withdrawing', 'withdrawn'],
  delete: ['deleting'],
  password: ['logging', 'account'],
  program: ['programme'],
  programme: ['program']
};

function edit1(a, b) {
  if (a === b) return true;
  const la = a.length, lb = b.length;
  if (Math.abs(la - lb) > 1 || Math.min(la, lb) <= 4) return false;
  let i = 0, j = 0, edits = 0;
  while (i < la && j < lb) {
    if (a[i] === b[j]) { i++; j++; continue; }
    if (++edits > 1) return false;
    if (la > lb) i++;
    else if (lb > la) j++;
    else { i++; j++; }
  }
  return edits + (la - i) + (lb - j) <= 1;
}

function tokenMatch(word, token) {
  if (word.length < 3 || token.length < 3) return word === token;
  if (word === token) return true;
  // containment only for meaningful stems (avoids '' and tiny fragments matching everything)
  if (Math.min(word.length, token.length) >= 5 &&
      (word.startsWith(token) || token.startsWith(word))) return true;
  return edit1(word, token);
}

function score(article, words) {
  const titleWords = article.title.toLowerCase().split(/[^a-z0-9]+/).filter(w => w.length > 2);
  const hayWords = (article.title + ' ' + article.summary + ' ' + article.section)
    .toLowerCase().split(/[^a-z0-9]+/).filter(w => w.length > 2);
  let s = 0;
  words.forEach(w => {
    if (titleWords.some(t => tokenMatch(t, w))) s += 3;
    else if (hayWords.some(t => tokenMatch(t, w))) s += 1;
  });
  return s;
}

function keywordHits(question) {
  let words = question.toLowerCase().split(/[^a-z0-9]+/)
    .filter(w => w.length > 2 && !STOP.has(w));
  const expanded = new Set(words);
  words.forEach(w => (SYNONYMS[w] || []).forEach(x => expanded.add(x)));
  words = [...expanded];
  if (!words.length) return [];
  return INDEX.map(a => ({ a, s: score(a, words) }))
    .filter(x => x.s > 0)
    .sort((x, y) => y.s - x.s)
    .slice(0, 6)
    .map(x => x.a);
}

function renderLinks(hits) {
  if (!hits.length) {
    rtitle.textContent = 'Nothing found yet';
    list.innerHTML = '<li>No guides matched those words. Try describing it differently, ' +
      'or <a href="https://oxfordabstracts.com/resources/contact/">contact support</a>.</li>';
    return;
  }
  rtitle.textContent = 'Guides that match';
  list.innerHTML = hits.map(a =>
    `<li><a href="${a.path}">${a.title}</a> <span style="color:#4A5468">— ${a.section}</span></li>`
  ).join('');
}

/* ---------- layer 2: plain-English answer ---------- */

let thinkingTimer = null;

function clearAnswer() {
  if (thinkingTimer) { clearInterval(thinkingTimer); thinkingTimer = null; }
  const old = document.getElementById('llmAnswer');
  if (old) old.remove();
}

/* Loading state. Three jobs:
 *   1. Say something is happening, immediately.
 *   2. Reserve the space the answer will occupy, so it doesn't shove the page
 *      about when it lands.
 *   3. Keep the reader informed as it goes, in plain language.
 */
const THINKING_STEPS = [
  'Looking through the guides…',
  'Reading the ones that match…',
  'Writing your answer…',
  'Almost there…'
];

function showThinking() {
  clearAnswer();
  const el = document.createElement('div');
  el.id = 'llmAnswer';
  el.className = 'answer-block is-loading';
  el.innerHTML =
    '<p class="thinking" role="status">' +
      '<span class="thinking-text">' + THINKING_STEPS[0] + '</span>' +
      '<span class="dots"><i></i><i></i><i></i></span>' +
    '</p>' +
    '<div class="skel"><span style="width:96%"></span><span style="width:88%"></span>' +
    '<span style="width:64%"></span></div>';
  box.insertBefore(el, box.firstChild);

  let i = 0;
  thinkingTimer = setInterval(() => {
    i += 1;
    if (i >= THINKING_STEPS.length) { clearInterval(thinkingTimer); thinkingTimer = null; return; }
    const t = el.querySelector('.thinking-text');
    if (!t) return;
    t.style.opacity = '0';
    setTimeout(() => { t.textContent = THINKING_STEPS[i]; t.style.opacity = '1'; }, 180);
  }, 1900);
}

function showAnswer(answer, sources, followups) {
  if (thinkingTimer) { clearInterval(thinkingTimer); thinkingTimer = null; }
  const existing = document.getElementById('llmAnswer');
  const el = existing || document.createElement('div');
  el.id = 'llmAnswer';
  el.className = 'answer-block';
  el.innerHTML = '';

  // the answer may contain short labelled branches; render each on its own line
  answer.split(/\n+/).filter(Boolean).forEach(line => {
    const p = document.createElement('p');
    p.textContent = line;
      el.appendChild(p);
  });

  (sources || []).slice(0, 2).forEach(src => {
    const a = document.createElement('a');
    a.href = src.path;
    a.textContent = 'Read the full guide: ' + src.title + ' \u2192';
    a.style.cssText = 'display:block;font-weight:600;color:#D0432C;text-decoration:none;margin-top:6px';
    el.appendChild(a);
  });

  // tappable narrowing: one tap beats retyping on a phone
  if (followups && followups.length) {
    const row = document.createElement('div');
    row.style.cssText = 'display:flex;flex-wrap:wrap;gap:8px;margin-top:14px';
    followups.forEach(q => {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = q;
      b.style.cssText = 'background:none;border:1.5px solid rgba(16,28,56,.14);border-radius:999px;' +
        'padding:7px 14px;font-family:inherit;font-size:15px;color:#4A5468;cursor:pointer';
      b.addEventListener('click', () => { input.value = q; search(q); });
      row.appendChild(b);
    });
    el.appendChild(row);
  }

  box.insertBefore(el, box.firstChild);
}

function showEscalation(question) {
  if (thinkingTimer) { clearInterval(thinkingTimer); thinkingTimer = null; }
  const existing = document.getElementById('llmAnswer');
  const el = existing || document.createElement('div');
  el.id = 'llmAnswer';
  el.className = 'answer-block';
  el.innerHTML = '';
  const p = document.createElement('p');
  p.textContent = "We couldn't find a guide that answers that — but our support team can. " +
    'No question is too small.';
  el.appendChild(p);
  const a = document.createElement('a');
  a.href = 'https://oxfordabstracts.com/resources/contact-support?topic=' +
    encodeURIComponent(question.slice(0, 120));
  a.textContent = 'Create a support ticket \u2192';
  a.style.cssText = 'display:inline-block;background:#D0432C;color:#fff;font-weight:600;' +
    'padding:10px 20px;border-radius:999px;text-decoration:none';
  el.appendChild(a);
  if (!existing) box.insertBefore(el, box.firstChild);
  requestAnimationFrame(() => el.classList.add('revealed'));
}

async function fetchAnswer(question) {
  if (!ANSWER_ENDPOINT) return;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ANSWER_TIMEOUT_MS);
  try {
    showThinking();
    const res = await fetch(ANSWER_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
      signal: controller.signal
    });
    if (!res.ok) throw new Error('bad status');
    const data = await res.json();
    if (data && data.answer) showAnswer(data.answer, data.sources, data.followups);
    else if (data && data.found === false) showEscalation(question);
    else clearAnswer();          // transport errors stay silent
  } catch (e) {
    clearAnswer();               // never surface an API error to the reader
  } finally {
    clearTimeout(timer);
  }
}

/* ---------- wiring ---------- */

async function search(question) {
  await indexReady;
  clearAnswer();
  renderLinks(keywordHits(question));
  box.classList.add('show');
  fetchAnswer(question);
}

if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const q = input.value.trim();
    if (q) search(q);
  });
}
// arriving from an article page's header search: ?q=...
const params = new URLSearchParams(location.search);
const preset = (params.get('q') || '').trim();
if (preset) {
  input.value = preset;
  indexReady.then(() => search(preset));
}

document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    input.value = chip.textContent;
    search(chip.textContent);
  });
});
