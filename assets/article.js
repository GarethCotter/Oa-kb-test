/* Article page behaviour: click-to-enlarge screenshots. */
(function () {
  var box = document.getElementById('lightbox');
  if (!box) return;
  var big = box.querySelector('img');

  function open(src, alt) {
    big.src = src;
    big.alt = alt || '';
    box.hidden = false;
    document.body.style.overflow = 'hidden';
  }
  function close() {
    box.hidden = true;
    big.src = '';
    document.body.style.overflow = '';
  }

  document.querySelectorAll('.prose img.zoomable').forEach(function (img) {
    img.addEventListener('click', function () { open(img.src, img.alt); });
    img.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(img.src, img.alt); }
    });
  });
  box.addEventListener('click', close);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !box.hidden) close();
  });
})();

/* Diagnostic feedback: Yes, or No -> one-tap reason. Best-effort beacon; UI
 * thanks the reader either way. */
(function () {
  var box = document.querySelector('.feedback');
  if (!box) return;
  var reasons = box.querySelector('.fb-reasons');
  var thanks = box.querySelector('.fb-thanks');
  var row = box.querySelector('.fb-row');

  /* Article feedback from the internal team is dropped rather than marked, which is
     the opposite of what /api/log does with a staff question - and deliberately so.
     A question carries demand ("people keep needing this"), which is worth keeping
     even when a colleague asked it. A colleague's thumbs-down carries no demand at
     all, and it would sit in the same "Articles voted No" list that decides what
     gets rewritten. Staff already have a better channel for that opinion, with room
     to say why: the suggestion form at /suggest. */
  function isInternal() {
    try { return localStorage.getItem('oa-internal') === '1'; } catch (e) { return false; }
  }

  function send(payload) {
    if (isInternal()) return;
    payload.path = box.getAttribute('data-path');
    payload.ts = Date.now();
    try {
      navigator.sendBeacon('/api/feedback',
        new Blob([JSON.stringify(payload)], { type: 'application/json' }));
    } catch (e) { /* logging is best-effort */ }
  }
  function done() {
    row.hidden = true;
    reasons.hidden = true;
    thanks.hidden = false;
  }
  box.querySelectorAll('[data-fb]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (b.getAttribute('data-fb') === 'yes') { send({ helpful: true }); done(); }
      else { row.hidden = true; reasons.hidden = false; }
    });
  });
  box.querySelectorAll('[data-reason]').forEach(function (b) {
    b.addEventListener('click', function () {
      send({ helpful: false, reason: b.getAttribute('data-reason') });
      done();
    });
  });
})();
