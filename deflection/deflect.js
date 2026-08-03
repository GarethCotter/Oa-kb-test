/* Oxford Abstracts — support-form ticket deflection.
 *
 * Drop-in: include this file on the contact-support page, set the selectors in
 * OA_DEFLECT below (or define window.OA_DEFLECT before the script tag), and wire
 * nothing else. Everything is namespaced oadf-; no libraries, no build step.
 *
 * What it does, in one line: when the reader submits the form, their question is
 * run against the help centre's answer layer, and if - and only if - a STRONG
 * answer exists, it is offered once, with "That's solved it" and "Send my ticket
 * anyway" side by side. See HANDOVER.md alongside this file for integration steps.
 *
 * Three rules, all deliberate (from the design work, do not soften them):
 *   1. Never show a confidence percentage. The one time it is confidently wrong,
 *      trust is gone.
 *   2. Never block the send. One click past the answer, always visible. On any
 *      error, timeout or doubt, the ticket goes through untouched.
 *   3. Only interrupt on confidence === 'strong', which the endpoint decides.
 *      Absent field (older cached responses) counts as weak: no interruption.
 *
 * Every interaction logs one labelled outcome to /api/log - question, articles
 * suggested, solved / sent_anyway / not_interrupted - which is the data that shows
 * which articles actually deflect tickets. Logging never affects the reader.
 */
(function () {
  'use strict';

  var CFG = Object.assign({
    enabled: true,
    endpoint: 'https://oa-kb-test.vercel.app',   // move to help.oxfordabstracts.com when live
    kbBase: 'https://oa-kb-test.vercel.app/',    // where cited guides open

    // The form. Selectors for the real page; all four are required.
    formSelector: '#supportForm',
    subjectSelector: '#subject',                 // TICKET.subject
    contentSelector: '#content',                 // TICKET.content
    submitSelector: '#submitBtn',

    // When a ticket is sent after an answer was shown, append what was suggested to
    // the ticket content so support can see what the reader already tried.
    attachToContent: true,

    maxWaitMs: 2500,     // never hold the reader longer than this at Submit
    minShowMs: 1100,     // never flash the check too briefly to read
    prefetchOnBlur: true, // start the search when they leave the description field

    onEvent: null        // optional hook(eventName, detail) for testing/analytics
  }, window.OA_DEFLECT || {});
  window.OA_DEFLECT = CFG;

  if (!CFG.enabled) return;

  var $ = function (sel) { return document.querySelector(sel); };
  var state = { pending: null, shown: false, suggested: [], settled: false };
  var TIMED_OUT = {};

  /* ---------- styles, injected and namespaced ---------- */
  var CSS = [
    '.oadf-box{margin:18px 0;font-family:inherit;color:#0A1B3E}',
    '.oadf-checking{display:flex;align-items:center;gap:14px;padding:18px 20px;border:1px solid #E5E7EB;border-radius:6px;background:#fbfbf8}',
    '.oadf-checking b{display:block;font-weight:600;font-size:16px;margin-bottom:2px}',
    '.oadf-checking span{display:block;font-size:14px;color:#5a6377}',
    '.oadf-spin{width:22px;height:22px;flex:none;border:3px solid #E5E7EB;border-top-color:#C54538;border-radius:50%;animation:oadf-r 0.9s linear infinite}',
    '@keyframes oadf-r{to{transform:rotate(360deg)}}',
    '@media (prefers-reduced-motion:reduce){.oadf-spin{animation:none}}',
    '.oadf-answer{border:1px solid #E5E7EB;border-left:4px solid #1F6F5C;border-radius:6px;background:#fbfcfa;padding:20px}',
    '.oadf-answer h3{font-size:17px;font-weight:600;margin:0 0 10px}',
    '.oadf-answer .oadf-body{font-size:16px;line-height:1.55;margin:0 0 14px}',
    '.oadf-answer .oadf-body strong{font-weight:600}',
    /* Procedural answers arrive as numbered steps. Rendered as a tight list, not
       cards - this box interrupts a ticket mid-send, so it earns its height. */
    '.oadf-anst{font-size:16.5px;font-weight:600;margin:0 0 8px}',
    '.oadf-steps{margin:0 0 14px;padding-left:22px}',
    '.oadf-steps>li{margin:0 0 10px;font-size:15.5px;line-height:1.5}',
    '.oadf-steps>li>b{display:block;font-weight:600}',
    '.oadf-path{display:block;font-size:13.5px;color:#1F6F5C;font-weight:600;margin:1px 0 2px;overflow-wrap:break-word}',
    '.oadf-det{display:block;font-size:14.5px}',
    '.oadf-det strong{font-weight:600}',
    '.oadf-steps ul{margin:3px 0 0 16px;padding:0;font-size:14px}',
    '.oadf-src{border-top:1px solid #E5E7EB;padding-top:12px;margin-bottom:14px}',
    '.oadf-src p{font-size:13px;color:#5a6377;margin:0 0 6px}',
    '.oadf-src a{display:block;font-size:15px;color:#0A1B3E;text-decoration:underline;text-underline-offset:3px;margin-bottom:5px}',
    '.oadf-src a:hover{color:#C54538}',
    '.oadf-row{display:flex;flex-wrap:wrap;gap:10px}',
    '.oadf-btn{display:inline-flex;align-items:center;gap:8px;font:inherit;font-size:16px;border-radius:9999px;padding:10px 20px;cursor:pointer}',
    '.oadf-yes{background:#C54538;border:1px solid #C54538;color:#fff}',
    '.oadf-yes:hover{background:#ab3a2f}',
    '.oadf-no{background:transparent;border:1px solid #0A1B3E;color:#0A1B3E}',
    '.oadf-no:hover{background:rgba(10,27,62,.05)}',
    '.oadf-done{border:1px solid #E5E7EB;border-left:4px solid #1F6F5C;border-radius:6px;padding:18px 20px}',
    '.oadf-done h3{font-size:17px;font-weight:600;margin:0 0 6px}',
    '.oadf-done p{font-size:15px;color:#5a6377;margin:0}',
    '.oadf-hidden{display:none}'
  ].join('\n');

  /* ---------- helpers ---------- */
  function emit(name, detail) {
    try { if (CFG.onEvent) CFG.onEvent(name, detail || {}); } catch (e) {}
  }

  function logEvent(question, answered, sources, action) {
    try {
      fetch(CFG.endpoint + '/api/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        keepalive: true,
        body: JSON.stringify({
          surface: 'ticket-form', screen: '', question: question,
          answered: answered, sources: (sources || []).map(function (s) { return s.path; }),
          action: action
        })
      }).catch(function () {});
    } catch (e) {}
    emit('log', { action: action, answered: answered });
  }

  function questionFrom() {
    var s = ($(CFG.subjectSelector) || {}).value || '';
    var c = ($(CFG.contentSelector) || {}).value || '';
    s = s.trim(); c = c.trim();
    if (!s && !c) return null;
    return (s + (s && c ? '. ' : '') + c).slice(0, 500);
  }

  function ask(question) {
    return fetch(CFG.endpoint + '/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: question })
    }).then(function (r) {
      if (!r.ok) throw new Error('bad status');
      return r.json();
    });
  }

  function isStrong(r) {
    return !!(r && r.answer && r.confidence === 'strong');
  }

  function withTimeout(p, ms) {
    return Promise.race([p, new Promise(function (res) {
      setTimeout(function () { res(TIMED_OUT); }, ms);
    })]);
  }

  function prefetch() {
    if (!CFG.prefetchOnBlur) return;
    var q = questionFrom();
    if (!q) return;
    if (state.pending && state.pending.q === q) return;
    var rec = { q: q, done: false, promise: null };
    rec.promise = ask(q)
      .then(function (r) { rec.done = true; return r; })
      .catch(function () { rec.done = true; return null; });
    state.pending = rec;
    emit('prefetch', { question: q });
  }

  /* Menu paths arrive **bolded**; escape everything, then render only <strong>. */
  function boldify(text) {
    var esc = text.replace(/[&<>]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c];
    });
    return esc.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  }

  /* ---------- UI ---------- */
  var box = null;
  function ui() {
    if (box) return box;
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);
    box = document.createElement('div');
    box.className = 'oadf-box oadf-hidden';
    var form = $(CFG.formSelector);
    form.parentNode.insertBefore(box, form.nextSibling);
    return box;
  }

  function showChecking() {
    ui().className = 'oadf-box';
    box.innerHTML =
      '<div class="oadf-checking" role="status">' +
        '<div class="oadf-spin" aria-hidden="true"></div>' +
        '<div><b>One moment — checking whether we can answer this right now</b>' +
        '<span class="oadf-step">Reading what you’ve written</span></div>' +
      '</div>';
    var steps = ['Reading what you’ve written', 'Searching the guides', 'Putting an answer together'];
    var i = 0;
    return setInterval(function () {
      i += 1;
      if (i < steps.length) box.querySelector('.oadf-step').textContent = steps[i];
    }, 720);
  }

  function showAnswer(result, question, sendTicket) {
    state.shown = true;
    state.suggested = (result.sources || []).slice(0, 2);
    /* Steps replace the paragraph when the endpoint provides them; boldify escapes
       every string on the way in, so nothing from the model reaches the page raw. */
    var instructions;
    if (result.steps && result.steps.length) {
      instructions =
        (result.title ? '<p class="oadf-anst">' + boldify(result.title) + '</p>' : '') +
        '<ol class="oadf-steps">' +
        result.steps.map(function (s) {
          return '<li>' +
            (s.title ? '<b>' + boldify(s.title) + '</b>' : '') +
            (s.path ? '<span class="oadf-path">' + boldify(s.path) + '</span>' : '') +
            (s.detail ? '<span class="oadf-det">' + boldify(s.detail) + '</span>' : '') +
            ((s.bullets && s.bullets.length)
              ? '<ul>' + s.bullets.map(function (b) { return '<li>' + boldify(b) + '</li>'; }).join('') + '</ul>'
              : '') +
            '</li>';
        }).join('') + '</ol>';
    } else {
      instructions = '<p class="oadf-body">' + boldify(result.answer) + '</p>';
    }
    box.innerHTML =
      '<div class="oadf-answer">' +
        '<h3>This might be what you’re after —</h3>' +
        instructions +
        (state.suggested.length
          ? '<div class="oadf-src"><p>Where this came from</p>' +
            state.suggested.map(function (s) {
              return '<a href="' + CFG.kbBase + s.path.replace(/^\//, '') +
                     '" target="_blank" rel="noopener">' + s.title + '</a>';
            }).join('') + '</div>'
          : '') +
        '<div class="oadf-row">' +
          '<button type="button" class="oadf-btn oadf-yes">That’s solved it</button>' +
          '<button type="button" class="oadf-btn oadf-no">Send my ticket anyway</button>' +
        '</div>' +
      '</div>';
    box.querySelector('.oadf-yes').addEventListener('click', function () {
      logEvent(question, true, state.suggested, 'solved');
      box.innerHTML =
        '<div class="oadf-done"><h3>Glad that sorted it</h3>' +
        '<p>No ticket was sent — there is nothing else for you to do.</p></div>';
      emit('solved', {});
    });
    box.querySelector('.oadf-no').addEventListener('click', function () {
      logEvent(question, true, state.suggested, 'sent_anyway');
      if (CFG.attachToContent) {
        var el = $(CFG.contentSelector);
        if (el) {
          el.value = el.value +
            '\n\n--- Help centre suggestion (shown to the reader before sending) ---\n' +
            state.suggested.map(function (s) {
              return '- ' + s.title + ' (' + CFG.kbBase + s.path.replace(/^\//, '') + ')';
            }).join('\n') +
            '\nOutcome: sent anyway';
        }
      }
      box.className = 'oadf-box oadf-hidden';
      emit('sent_anyway', {});
      sendTicket();
    });
    emit('answer_shown', { sources: state.suggested });
  }

  /* ---------- wiring ---------- */
  function init() {
    var form = $(CFG.formSelector);
    if (!form) return;             // selectors not matching: do nothing at all
    var subject = $(CFG.subjectSelector), content = $(CFG.contentSelector);
    if (subject) subject.addEventListener('blur', prefetch);
    if (content) content.addEventListener('blur', prefetch);

    var bypass = false;
    form.addEventListener('submit', function (e) {
      if (bypass || state.settled) return;      // deflection already had its one chance
      var question = questionFrom();
      if (!question) return;                    // let native validation speak
      e.preventDefault();
      e.stopImmediatePropagation();
      state.settled = true;                     // one interruption per form, ever

      var sendTicket = function () {
        bypass = true;
        if (typeof form.requestSubmit === 'function') form.requestSubmit();
        else form.submit();
      };

      var promise, ready = false;
      if (state.pending && state.pending.q === question) {
        promise = state.pending.promise;
        ready = state.pending.done;
      } else {
        promise = ask(question).catch(function () { return null; });
      }

      var sb = $(CFG.submitSelector);
      if (sb) sb.disabled = true;
      var timer = showChecking();
      var t0 = Date.now();

      withTimeout(promise, CFG.maxWaitMs).then(function (result) {
        var wait = Math.max(0, CFG.minShowMs - (Date.now() - t0));
        setTimeout(function () {
          clearInterval(timer);
          if (sb) sb.disabled = false;
          if (result === TIMED_OUT || !isStrong(result)) {
            // Weak, slow or broken: never interrupt. The ticket goes through as if
            // this script did not exist.
            logEvent(question, !!(result && result !== TIMED_OUT && result.answer),
                     [], 'not_interrupted');
            box.className = 'oadf-box oadf-hidden';
            sendTicket();
            return;
          }
          logEvent(question, true, result.sources, 'asked');
          showAnswer(result, question, sendTicket);
        }, wait);
      });
    }, true);   // capture: runs before the page's own submit handlers

    emit('ready', {});
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
