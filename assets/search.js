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

const TICK =
  '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">' +
  '<path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 ' +
  '01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 ' +
  '011.05-.143z" clip-rule="evenodd"/></svg>';

/* One row per event: an 'asked' row when a question completes (answered says
   whether an answer was shown), then a row per verdict or ticket click. The master
   sheet's dashboard is computed entirely from these. Fire-and-forget: logging must
   never affect the reader (api/log.js enforces the same rule server-side). */
function logEvent(question, sources, action, answered) {
  try {
    fetch('/api/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      keepalive: true,
      body: JSON.stringify({
        surface: 'kb-search',
        question: question,
        answered: answered !== false,
        sources: (sources || []).map(s => s.path),
        action: action
      })
    }).catch(() => {});
  } catch (e) { /* logging never breaks the page */ }
}

function showAnswer(answer, sources, question) {
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

  // Follow-up question chips were removed on 30 July 2026: the model's suggestions
  // were too often a worse question than the one just asked, and a row of them under
  // the answer invited a second search instead of the guide the answer came from.
  // The example questions under the homepage search box are a different thing and stay.

  /* The verdict row. Every click is a labelled outcome - question, articles shown,
     solved or not - which is the one signal that says whether an answer WORKED
     rather than merely appeared. Rows land in the interaction-log sheet. */
  const v = document.createElement('div');
  v.className = 'verdict ans-in';
  const yes = document.createElement('button');
  yes.type = 'button';
  yes.innerHTML = TICK + 'This solved it';
  const no = document.createElement('button');
  no.type = 'button';
  no.textContent = 'This didn’t help me';

  yes.addEventListener('click', () => {
    logEvent(question, sources, 'solved');
    const t = document.createElement('p');
    t.className = 'verdict-thanks';
    t.setAttribute('role', 'status');
    t.innerHTML = TICK + 'Good — glad it helped.';
    v.replaceWith(t);
  });

  no.addEventListener('click', () => {
    logEvent(question, sources, 'unhelpful');
    const card = document.createElement('div');
    card.className = 'gap-card ans-in';
    card.setAttribute('role', 'status');
    const p = document.createElement('p');
    p.textContent = 'Sorry about that — and thank you for telling us. Your click has ' +
      'flagged this answer for review, and feedback like this is how we improve the ' +
      'system every day. In the meantime, our support team can give you a proper answer.';
    card.appendChild(p);
    const a = document.createElement('a');
    a.className = 'gap-btn';
    a.href = 'https://oxfordabstracts.com/resources/contact-support?topic=' +
      encodeURIComponent((question || '').slice(0, 120));
    a.textContent = 'Create support ticket →';
    // keepalive on the fetch means the row survives the navigation to the form
    a.addEventListener('click', () => logEvent(question, sources, 'ticket_created'));
    card.appendChild(a);
    v.replaceWith(card);
  });

  v.appendChild(yes);
  v.appendChild(no);
  el.appendChild(v);
}

/* Amplitude taught us most people type two words, not a question - "incomplete
   submissions", "reviewer emails". Those still search fine, so nothing nags while
   an answer is coming or once one has arrived. But when the answer layer comes back
   empty on a keyword-shaped query, the honest reading is "we couldn't tell what you
   were asking", not "we haven't written this up" - so those get an invitation to ask
   in full instead of the gap card, which would be claiming a content gap we have no
   evidence for. */
const QUESTION_LEADS = new Set(['how', 'why', 'what', 'where', 'when', 'who', 'which',
  'can', 'cant', 'cannot', 'could', 'do', 'does', 'did', 'is', 'are', 'am', 'was',
  'will', 'would', 'should', 'shall', 'may', 'might', 'has', 'have', 'had', 'if',
  'i', 'my', 'we', 'our', 'the']);

function looksLikeKeywords(q) {
  if (q.includes('?')) return false;
  const words = q.toLowerCase().trim().split(/\s+/);
  if (words.length >= 5) return false;      // a five-word phrase is a real attempt
  return !QUESTION_LEADS.has(words[0].replace(/[^a-z']/g, ''));
}

/* The invitation. The reader is not told off for searching in keywords - the guides
   below still carry them - just shown that one full sentence usually skips the
   digging. The button puts them back in the box with their words selected, so one
   keystroke starts the question. */
function showAskFully() {
  const el = settleInto('more', 'Want the answer, not just the guides?');
  const hasGuides = list.children.length > 0 && !list.querySelector('a[href*="contact"]');
  const card = document.createElement('div');
  card.className = 'gap-card ans-in';
  const p = document.createElement('p');
  p.textContent = (hasGuides
    ? 'The guides below should cover it. But ask in a full sentence - the way ' +
      'you’d ask a colleague, like “Why is my submission incomplete?” - ' +
      'and we can usually answer you on the spot, so you don’t have to dig.'
    : 'Those words on their own didn’t find anything, but a full question often ' +
      'will. Ask it the way you’d ask a colleague - like “Why is my ' +
      'submission incomplete?” - and if the guides cover it, we’ll answer ' +
      'you directly.');
  card.appendChild(p);
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'gap-btn';
  b.textContent = 'Ask your full question';
  b.addEventListener('click', () => { input.focus(); input.select(); });
  card.appendChild(b);
  el.appendChild(card);
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
  a.addEventListener('click', () => logEvent(question, [], 'ticket_created', false));
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
    if (data && data.answer) {
      showAnswer(data.answer, data.sources, question);
      logEvent(question, data.sources, 'asked', true);
    } else if (data && data.found === false) {
      // keywords that found nothing get "ask in full", not "we haven't written this"
      if (looksLikeKeywords(question)) showAskFully();
      else showEscalation(question);
      logEvent(question, [], 'asked', false);
    }
    // a transport error logs nothing: we know nothing about the question's fate
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
