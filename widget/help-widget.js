/* Oxford Abstracts — in-app help widget.
 *
 * Drop-in: include this file on any admin screen, tell it which screen it is on,
 * and wire nothing else. One launcher (bottom-right, labelled Help), one panel.
 * Everything namespaced oahw-; no libraries, no build step.
 *
 *   <script>
 *   window.OA_HELP = { screen: 'Emails' };   // the one thing each page must set
 *   </script>
 *   <script src="/path/to/help-widget.js"></script>
 *
 * What it does: answers questions in plain English from the help centre's answer
 * layer (/api/search), cites the guides it drew from, and opens them INSIDE the
 * panel - the live KB page, re-rooted, so there is no second copy to drift. The
 * current screen rides on the front of the question as context, which measurably
 * improves routing. After every answer: "This solved it" / "This didn't help me",
 * the same verdict pair as the KB, logged as labelled outcomes.
 *
 * Design rules carried from the prototype (see HANDOVER.md; do not soften):
 *   - One surface called Help. Not Home/Ask-AI tabs.
 *   - Never a dead end, never a visible error. An outage looks like "no confident
 *     answer", which offers the KB search and the support form, one tap each.
 *   - The bot never guesses: weak answers are not shown, said honestly instead.
 */
(function () {
  'use strict';

  var CFG = Object.assign({
    enabled: true,
    endpoint: 'https://oa-kb-test.vercel.app',    // becomes help.oxfordabstracts.com later
    kbBase: 'https://oa-kb-test.vercel.app/',
    screen: '',                                   // e.g. 'Emails' - set per page
    ticketUrl: 'https://oxfordabstracts.com/resources/contact-support',
    zIndex: 999990,
    suggestions: null,                            // override the per-screen defaults below
    onEvent: null                                 // optional hook(name, detail) for testing
  }, window.OA_HELP || {});
  window.OA_HELP = CFG;
  if (!CFG.enabled) return;

  /* Per-screen suggested questions. These are the upfront prompts (kept), not the
     removed AI follow-ups. Every one returns a confident answer from the live
     corpus - checked before shipping, like the KB homepage examples. */
  var SUGGEST = CFG.suggestions || {
    'Dashboard':           ['How do I add someone to my team?', 'Where do I find my event ID?', 'What does my package include?'],
    'Event setup':         ['How do I edit my event details?', 'Can I add my own colours and logo?', 'How do I add admins to my event?'],
    'Emails':              ['Why have my submitters not received my email?', 'How do I schedule an email for later?', 'Can I send from my own address?'],
    'Abstract Management': ['How do I change the submission deadline?', 'Why can’t my reviewers see their assigned reviews?', 'Why does a submission show as incomplete?'],
    'Symposium':           ['How do I collect symposia?', 'How does someone attach their abstract to a symposium?'],
    'Speaker Management':  ['How does speaker management work?', 'How do I email session chairs?'],
    'Website Builder':     ['How do I create my event website?', 'How do I publish the homepage?'],
    'Registration':        ['How do I set up tickets?', 'How do I refund an attendee?', 'Where are the invoices?'],
    'Conference':          ['How do I create sessions?', 'How do I publish the programme?', 'Which Zoom package do I need?'],
    'Certificates':        ['How do I create a certificate?', 'Is Certificates included in my plan?'],
    '':                    ['How do I change the submission deadline?', 'What can I do with the API?', 'How do we set up the poster gallery?']
  };

  var state = { open: false, busy: false, history: [], greeted: false };

  /* ---------- styles ---------- */
  var CSS = [
    '.oahw-launch{position:fixed;right:22px;bottom:22px;z-index:Z;display:inline-flex;align-items:center;gap:9px;',
    ' background:#0A1B3E;color:#EAECE1;border:none;border-radius:9999px;padding:13px 22px;font-family:inherit;',
    ' font-size:16px;font-weight:600;cursor:pointer;box-shadow:0 8px 24px rgba(10,27,62,.35)}',
    '.oahw-launch:hover{background:#152a56}',
    '.oahw-launch svg{width:18px;height:18px}',
    '.oahw-panel{position:fixed;right:22px;bottom:22px;z-index:Z;width:390px;max-width:calc(100vw - 30px);',
    ' height:600px;max-height:calc(100vh - 44px);background:#fff;border:1px solid #d8d5c8;border-radius:14px;',
    ' box-shadow:0 18px 50px rgba(10,27,62,.3);display:flex;flex-direction:column;overflow:hidden;',
    ' font-family:inherit;color:#0A1B3E;transition:width .2s ease}',
    '.oahw-panel.oahw-wide{width:560px}',
    '.oahw-head{background:#0A1B3E;color:#EAECE1;padding:14px 18px;display:flex;align-items:center;justify-content:space-between}',
    '.oahw-head b{font-size:17px;font-weight:600}',
    '.oahw-head span{display:block;font-size:12.5px;color:rgba(234,236,225,.75);margin-top:1px}',
    '.oahw-x{background:none;border:none;color:#EAECE1;font-size:22px;line-height:1;cursor:pointer;padding:4px}',
    '.oahw-body{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px;background:#EAECE1}',
    '.oahw-row{display:flex;gap:8px;align-items:flex-end}',
    '.oahw-av{width:26px;height:26px;border-radius:50%;background:#0A1B3E;color:#EAECE1;flex:none;display:flex;',
    ' align-items:center;justify-content:center;font-size:12px;font-weight:700}',
    '.oahw-msg{max-width:85%;padding:10px 14px;border-radius:12px;font-size:14.5px;line-height:1.5}',
    '.oahw-bot{background:#fff;border:1px solid #d8d5c8;border-bottom-left-radius:4px}',
    '.oahw-bot p{margin:0 0 8px}.oahw-bot p:last-child{margin:0}',
    '.oahw-bot strong{font-weight:600}',
    '.oahw-you{background:#0A1B3E;color:#EAECE1;align-self:flex-end;border-bottom-right-radius:4px}',
    '.oahw-from{border-top:1px solid #e4e1d4;margin-top:10px;padding-top:8px}',
    '.oahw-from p{font-size:11.5px;color:#5a6377;text-transform:uppercase;letter-spacing:.05em;margin:0 0 5px}',
    '.oahw-from a{display:flex;align-items:center;gap:6px;font-size:13.5px;color:#0A1B3E;text-decoration:underline;',
    ' text-underline-offset:3px;margin-bottom:4px;cursor:pointer}',
    '.oahw-from a:hover{color:#C54538}',
    '.oahw-chips{display:flex;flex-wrap:wrap;gap:7px;align-self:flex-start;max-width:95%}',
    '.oahw-chip{border:1px solid rgba(10,27,62,.28);background:#fff;border-radius:9999px;padding:7px 13px;',
    ' font-family:inherit;font-size:13px;color:#0A1B3E;cursor:pointer}',
    '.oahw-chip:hover{border-color:#C54538;color:#C54538}',
    '.oahw-chip.oahw-solid{background:#C54538;border-color:#C54538;color:#fff;font-weight:500}',
    '.oahw-verdict{display:flex;flex-wrap:wrap;gap:8px;align-self:flex-start}',
    '.oahw-vbtn{display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(10,27,62,.18);background:#fff;',
    ' border-radius:9999px;padding:6px 13px;font-family:inherit;font-size:13px;color:#0A1B3E;cursor:pointer}',
    '.oahw-vbtn:hover{border-color:rgba(10,27,62,.45)}',
    '.oahw-vbtn svg{width:13px;height:13px;flex:none}',
    '.oahw-vyes svg{color:#4E5A31}.oahw-vno svg{color:#5a6377}',
    '.oahw-vdone{display:inline-flex;align-items:center;gap:6px;align-self:flex-start;font-size:13px;font-weight:500}',
    '.oahw-vdone svg{width:13px;height:13px;color:#4E5A31}',
    '.oahw-typing{display:inline-flex;gap:4px;padding:12px 14px;background:#fff;border:1px solid #d8d5c8;border-radius:12px;border-bottom-left-radius:4px}',
    '.oahw-typing i{width:6px;height:6px;border-radius:50%;background:#C54538;opacity:.4;animation:oahw-b 1.2s infinite ease-in-out}',
    '.oahw-typing i:nth-child(2){animation-delay:.16s}.oahw-typing i:nth-child(3){animation-delay:.32s}',
    '@keyframes oahw-b{0%,80%,100%{opacity:.3;transform:scale(.85)}40%{opacity:1;transform:scale(1)}}',
    '@media (prefers-reduced-motion:reduce){.oahw-typing i{animation:none;opacity:1}}',
    '.oahw-foot{border-top:1px solid #d8d5c8;background:#fff;padding:10px;display:flex;gap:8px}',
    '.oahw-foot input{flex:1;font-family:inherit;font-size:14.5px;padding:10px 12px;border:1.5px solid #d8d5c8;',
    ' border-radius:9999px;color:#0A1B3E;min-width:0}',
    '.oahw-foot input:focus{outline:none;border-color:#0A1B3E}',
    '.oahw-send{background:#C54538;color:#fff;border:none;border-radius:9999px;padding:0 18px;font-family:inherit;',
    ' font-size:14.5px;font-weight:600;cursor:pointer}',
    '.oahw-send[disabled]{opacity:.55;cursor:default}',
    '.oahw-reader{flex:1;overflow-y:auto;padding:20px;background:#fff}',
    '.oahw-reader h1{font-size:22px;margin:0 0 14px}',
    '.oahw-reader img{max-width:100%;height:auto;border:1px solid #e4e1d4;border-radius:6px}',
    '.oahw-rbar{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-bottom:1px solid #d8d5c8;background:#fff}',
    '.oahw-rbar button,.oahw-rbar a{font-family:inherit;font-size:13.5px;color:#0A1B3E;background:none;border:1px solid rgba(10,27,62,.25);',
    ' border-radius:9999px;padding:6px 14px;cursor:pointer;text-decoration:none}',
    '.oahw-rbar button:hover,.oahw-rbar a:hover{border-color:#C54538;color:#C54538}',
    '.oahw-hidden{display:none !important}'
  ].join('\n').replace(/Z/g, String(CFG.zIndex));

  var TICK = '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd"/></svg>';
  var CROSS = '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>';
  var QMARK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M9.1 9a3 3 0 015.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/><circle cx="12" cy="12" r="10"/></svg>';

  function emit(name, detail) { try { if (CFG.onEvent) CFG.onEvent(name, detail || {}); } catch (e) {} }

  function logEvent(question, answered, sources, action) {
    try {
      fetch(CFG.endpoint + '/api/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        keepalive: true,
        body: JSON.stringify({
          surface: 'widget', screen: CFG.screen, question: question,
          answered: answered, sources: (sources || []).map(function (s) { return s.path; }),
          action: action
        })
      }).catch(function () {});
    } catch (e) {}
    emit('log', { action: action, answered: answered });
  }

  /* ---------- DOM ---------- */
  var root, panel, body, foot, input, reader, readerBody, readerOpen;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  function build() {
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);

    root = el('div');
    var launch = el('button', 'oahw-launch');
    launch.type = 'button';
    launch.innerHTML = QMARK + 'Help';
    launch.setAttribute('aria-label', 'Open help');
    launch.addEventListener('click', open);

    panel = el('div', 'oahw-panel oahw-hidden');
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Help');
    var head = el('div', 'oahw-head');
    var ht = el('div');
    ht.appendChild(el('b', null, 'Help'));
    var where = el('span');
    where.textContent = CFG.screen ? 'You’re on ' + CFG.screen + ' — I’ll take that into account' : 'Ask in your own words';
    ht.appendChild(where);
    var x = el('button', 'oahw-x', '×');
    x.type = 'button';
    x.setAttribute('aria-label', 'Close help');
    x.addEventListener('click', close);
    head.append(ht, x);

    body = el('div', 'oahw-body');

    var rbar = el('div', 'oahw-rbar oahw-hidden');
    var back = el('button', null, '‹ Back to the conversation');
    back.type = 'button';
    back.addEventListener('click', closeReader);
    readerOpen = el('a', null, 'Open in the help centre ↗');
    readerOpen.target = '_blank'; readerOpen.rel = 'noopener';
    rbar.append(back, readerOpen);
    reader = el('div', 'oahw-reader oahw-hidden');
    readerBody = reader;

    foot = el('div', 'oahw-foot');
    input = el('input');
    input.type = 'text';
    input.placeholder = 'e.g. How do I email my reviewers?';
    input.setAttribute('aria-label', 'Your question');
    var send = el('button', 'oahw-send', 'Ask');
    send.type = 'button';
    var go = function () { var q = input.value.trim(); if (q) { input.value = ''; ask(q); } };
    send.addEventListener('click', go);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });
    foot.append(input, send);

    panel.append(head, rbar, body, reader, foot);
    root.append(launch, panel);
    document.body.appendChild(root);
    state._launch = launch; state._rbar = rbar; state._send = send;
  }

  function open() {
    state.open = true;
    state._launch.classList.add('oahw-hidden');
    panel.classList.remove('oahw-hidden');
    if (!state.greeted) {
      state.greeted = true;
      addBot('Ask me anything about running your event — in your own words, the way you’d ask a colleague. I’ll answer and show you which guide it came from.');
      addChips(SUGGEST[CFG.screen] || SUGGEST[''] || []);
    }
    input.focus();
    emit('open', { screen: CFG.screen });
  }
  function close() {
    state.open = false;
    panel.classList.add('oahw-hidden');
    state._launch.classList.remove('oahw-hidden');
    emit('close', {});
  }

  /* ---------- conversation ---------- */
  function scrollDown() { body.scrollTop = body.scrollHeight; }

  function boldify(text) {
    var esc = text.replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; });
    return esc.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  }

  function botRow() {
    var row = el('div', 'oahw-row');
    row.appendChild(el('div', 'oahw-av', 'OA'));
    return row;
  }

  function addBot(text, sources) {
    var m = el('div', 'oahw-msg oahw-bot');
    text.split('\n').forEach(function (p) {
      if (!p.trim()) return;
      var para = el('p');
      para.innerHTML = boldify(p.trim());
      m.appendChild(para);
    });
    if (sources && sources.length) {
      var from = el('div', 'oahw-from');
      from.appendChild(el('p', null, 'From these guides'));
      sources.slice(0, 2).forEach(function (s) {
        var a = el('a', null, s.title);
        a.href = CFG.kbBase + s.path.replace(/^\//, '');
        a.addEventListener('click', function (e) {
          e.preventDefault();
          var last = state.history[state.history.length - 1];
          logEvent(last ? last.q : s.title, true, [s], 'opened_article');
          openReader(s.path, a.href);
        });
        from.appendChild(a);
      });
      m.appendChild(from);
    }
    var row = botRow();
    row.appendChild(m);
    body.appendChild(row);
    scrollDown();
  }

  function addYou(text) {
    var m = el('div', 'oahw-msg oahw-you', text);
    body.appendChild(m);
    scrollDown();
  }

  function addChips(list, solidLast) {
    if (!list.length) return;
    var wrap = el('div', 'oahw-chips');
    list.forEach(function (item) {
      var c = el('button', 'oahw-chip' + (solidLast && item === list[list.length - 1] ? ' oahw-solid' : ''), item.label || item);
      c.type = 'button';
      c.addEventListener('click', function () {
        wrap.remove();
        if (item.onClick) item.onClick(); else ask(item);
      });
      wrap.appendChild(c);
    });
    body.appendChild(wrap);
    scrollDown();
  }

  function addTyping() {
    var t = el('div', 'oahw-typing');
    t.setAttribute('aria-label', 'Looking that up');
    t.append(el('i'), el('i'), el('i'));
    var row = botRow();
    row.id = 'oahw-typing-row';
    row.appendChild(t);
    body.appendChild(row);
    scrollDown();
  }
  function removeTyping() { var t = document.getElementById('oahw-typing-row'); if (t) t.remove(); }

  function addVerdict(question, sources) {
    var wrap = el('div', 'oahw-verdict');
    var yes = el('button', 'oahw-vbtn oahw-vyes');
    yes.type = 'button';
    yes.innerHTML = TICK + 'This solved it';
    var no = el('button', 'oahw-vbtn oahw-vno');
    no.type = 'button';
    no.innerHTML = CROSS + 'This didn’t help me';
    yes.addEventListener('click', function () {
      logEvent(question, true, sources, 'solved');
      var t = el('div', 'oahw-vdone');
      t.innerHTML = TICK + 'Good — glad it helped.';
      wrap.replaceWith(t);
      scrollDown();
      emit('solved', {});
    });
    no.addEventListener('click', function () {
      logEvent(question, true, sources, 'unhelpful');
      wrap.remove();
      addBot('Sorry about that — and thank you for telling us. Your click has flagged this answer for review, and feedback like this is how we improve every day.\nOur support team can give you a proper answer in the meantime.');
      addChips([{ label: 'Create support ticket', onClick: function () {
        logEvent(question, true, sources, 'ticket_created');
        window.open(CFG.ticketUrl + '?topic=' + encodeURIComponent(question.slice(0, 120)), '_blank');
      } }], true);
      emit('unhelpful', {});
    });
    wrap.append(yes, no);
    body.appendChild(wrap);
    scrollDown();
  }

  /* Page context and a short memory of the last exchange ride on the front of the
     question as one string - no endpoint change - inside the 500-char cap. A proper
     multi-turn endpoint accepting structured history is the known next step. */
  function contextualise(question) {
    var q = '';
    if (CFG.screen) q += '[The admin is on the ' + CFG.screen + ' screen of their event dashboard] ';
    var last = state.history[state.history.length - 1];
    if (last) q += '[Earlier they asked: "' + last.q.slice(0, 90) + '"] ';
    return (q + question).slice(0, 500);
  }

  function isStrong(r) {
    if (!r || !r.answer) return false;
    if (r.confidence) return r.confidence === 'strong';
    return r.answer.trim().length >= 60 && (r.sources || []).length >= 1;
  }

  function ask(question) {
    if (state.busy || !question.trim()) return;
    state.busy = true;
    state._send.disabled = true;
    Array.prototype.forEach.call(body.querySelectorAll('.oahw-chips'), function (c) { c.remove(); });
    addYou(question);
    addTyping();

    fetch(CFG.endpoint + '/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: contextualise(question) })
    })
      .then(function (r) { if (!r.ok) throw new Error('bad status'); return r.json(); })
      .catch(function () { return null; })            // outages look like no answer
      .then(function (r) {
        removeTyping();
        if (isStrong(r)) {
          addBot(r.answer, r.sources);
          state.history.push({ q: question, a: r.answer });
          logEvent(question, true, r.sources, 'asked');
          addVerdict(question, r.sources || []);
        } else {
          addBot('I couldn’t find a confident answer to that one — and I’d rather say so than guess.\nThe knowledge base search sometimes does better with a bit more detail, or our support team will pick it up quickly — no question is too small.');
          addChips([
            { label: 'Search the knowledge base', onClick: function () {
              window.open(CFG.kbBase + '?q=' + encodeURIComponent(question), '_blank');
            } },
            { label: 'Create support ticket', onClick: function () {
              logEvent(question, false, [], 'ticket_created');
              window.open(CFG.ticketUrl + '?topic=' + encodeURIComponent(question.slice(0, 120)), '_blank');
            } }
          ], true);
          state.history.push({ q: question, a: null });
          logEvent(question, false, [], 'asked');     // this row is the gap log
        }
        state.busy = false;
        state._send.disabled = false;
        emit('answered', { strong: isStrong(r) });
      });
  }

  /* ---------- the in-panel reader ---------- */
  function openReader(path, kbUrl) {
    panel.classList.add('oahw-wide');
    body.classList.add('oahw-hidden');
    foot.classList.add('oahw-hidden');
    state._rbar.classList.remove('oahw-hidden');
    reader.classList.remove('oahw-hidden');
    readerOpen.href = kbUrl;
    reader.innerHTML = '<p>Opening the guide…</p>';
    fetch(CFG.kbBase + path.replace(/^\//, ''))
      .then(function (r) { if (!r.ok) throw new Error('status'); return r.text(); })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, 'text/html');
        var title = doc.querySelector('h1');
        var prose = doc.querySelector('.prose');
        if (!prose) throw new Error('no article body');
        var base = CFG.kbBase + path.replace(/^\//, '');
        Array.prototype.forEach.call(prose.querySelectorAll('[src]'), function (n) {
          n.src = new URL(n.getAttribute('src'), base).href;
        });
        Array.prototype.forEach.call(prose.querySelectorAll('a[href]'), function (n) {
          n.href = new URL(n.getAttribute('href'), base).href;
          n.target = '_blank'; n.rel = 'noopener';
        });
        reader.innerHTML = '';
        if (title) reader.appendChild(el('h1', null, title.textContent.replace(/#$/, '')));
        Array.prototype.forEach.call(Array.prototype.slice.call(prose.childNodes), function (n) {
          reader.appendChild(n);
        });
        reader.scrollTop = 0;
        emit('reader_open', { path: path });
      })
      .catch(function () {
        // Cross-origin fetch blocked or page changed: never a dead end - open the
        // real page in a tab instead and put the conversation back.
        closeReader();
        window.open(kbUrl, '_blank');
      });
  }
  function closeReader() {
    panel.classList.remove('oahw-wide');
    reader.classList.add('oahw-hidden');
    state._rbar.classList.add('oahw-hidden');
    body.classList.remove('oahw-hidden');
    foot.classList.remove('oahw-hidden');
    scrollDown();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
