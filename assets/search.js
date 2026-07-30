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

/* Both endings ship in the markup and the state class picks one, so settling the
   book never rebuilds it - it only stops the pages and reveals the bookmark or the
   blank page. Decorative throughout: the text beside it carries the meaning. */
const BOOK =
  '<span class="book" aria-hidden="true">' +
    '<span class="cover"></span>' +
    '<span class="page p2"></span><span class="page"></span>' +
    '<span class="spine"></span>' +
    '<span class="ribbon"></span>' +
    '<span class="blank"><i></i><i></i><i></i></span>' +
  '</span>';

function showThinking() {
  clearAnswer();
  const el = document.createElement('div');
  el.id = 'llmAnswer';
  el.className = 'answer-block is-loading';
  el.innerHTML =
    '<p class="thinking" role="status">' + BOOK +
      '<span class="thinking-text">' + THINKING_STEPS[0] + '</span>' +
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

/* Settle the loading state into its ending. The thinking line stays exactly where it
   is and becomes the answer's own heading, so the book never blinks out and the
   reader sees one continuous object: pages turning, then a bookmark or a blank page.
   Everything below the line is replaced. Returns the block, ready to append to.

   The block keeps 'revealed' rather than re-running the block-level fade, which
   would flicker the book; new content fades itself in with .ans-in instead. */
function settleInto(state, message) {
  if (thinkingTimer) { clearInterval(thinkingTimer); thinkingTimer = null; }
  let el = document.getElementById('llmAnswer');
  if (!el) {
    el = document.createElement('div');
    el.id = 'llmAnswer';
    box.insertBefore(el, box.firstChild);
  }
  el.className = 'answer-block revealed';
  let line = el.querySelector('.thinking');
  if (!line) {                       // no loading state ran; build the line to settle
    el.innerHTML = '<p class="thinking" role="status">' + BOOK +
      '<span class="thinking-text"></span></p>';
    line = el.querySelector('.thinking');
  }
  while (line.nextSibling) el.removeChild(line.nextSibling);   // drop the skeleton
  const t = line.querySelector('.thinking-text');
  if (t) t.textContent = message;
  line.classList.add(state);
  return el;
}

/* The model marks menu paths and button names with **double asterisks**
   (see ANSWER_SYSTEM in api/search.js), so the reader can pick out what to click
   without re-reading. Everything is HTML-escaped first; only <strong> is produced. */
function boldify(text) {
  const esc = text.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  return esc.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
}

function showAnswer(answer, sources, followups) {
  // the settled line is the answer's own heading, so there is no separate label
  const el = settleInto('found', 'Found it —');

  // the answer may contain short labelled branches; render each on its own line
  answer.split(/\n+/).filter(Boolean).forEach(line => {
    const p = document.createElement('p');
    p.className = 'ans-in';
    p.innerHTML = boldify(line);
      el.appendChild(p);
  });

  (sources || []).slice(0, 2).forEach(src => {
    const a = document.createElement('a');
    a.href = src.path;
    a.className = 'ans-in';
    a.textContent = 'Read the full guide: ' + src.title + ' \u2192';
    a.style.cssText = 'display:block;font-weight:600;color:#D0432C;text-decoration:none;margin-top:6px';
    el.appendChild(a);
  });

  // tappable narrowing: one tap beats retyping on a phone
  if (followups && followups.length) {
    const row = document.createElement('div');
    row.className = 'ans-in';
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
}

/* The gap state. Reached only on an explicit found:false - a transport error goes to
   clearAnswer() instead, because "we have not written this up" is a claim about our
   guides, and it would be a lie if the endpoint had simply failed.

   The apology sits on the settled line itself, beside the blank page, so the reader
   gets one statement rather than the same news told to her twice. */
function showEscalation(question) {
  const el = settleInto('gap',
    'Sorry — we don’t have an answer written for this yet.');
  const card = document.createElement('div');
  card.className = 'gap-card ans-in';
  const p = document.createElement('p');
  p.textContent = 'You’ve found a real gap in our guides, and that’s genuinely ' +
    'useful to us. Our support team enjoy answering the questions nobody has asked ' +
    'before, and by creating a support ticket you’ll be helping others in the future.';
  card.appendChild(p);
  const a = document.createElement('a');
  a.className = 'gap-btn';
  a.href = 'https://oxfordabstracts.com/resources/contact-support?topic=' +
    encodeURIComponent(question.slice(0, 120));
  a.textContent = 'Create support ticket →';
  card.appendChild(a);
  el.appendChild(card);
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
