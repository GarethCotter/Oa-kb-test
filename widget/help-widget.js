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
 *
 * The panel now opens on a topic screen rather than straight into conversation:
 * six doors ("What do you need a hand with?"), the one matching the current screen
 * marked, with the ask bar still live underneath - a formed question skips the
 * doors entirely, because nobody mid-crisis should pay a tax of two taps. A chosen
 * topic rides on the front of the question exactly as the screen name does (no
 * endpoint change) and swaps in that topic's suggested questions. The answering
 * surface is titled "Instant answers" - deliberately not "AI chat": it names the
 * outcome, not the technology.
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

  /* PARKED - per-screen suggested questions. Nothing reads this since suggested
     questions came out of the flow (2 Aug 2026, Gareth's call: this version leads
     with the person's own words). Kept, like TOPICS.qs, because every entry was
     verified to answer confidently against the live corpus and that verification
     is the expensive part of bringing them back. */
  var SUGGEST = CFG.suggestions || {
    /* 'Where do I find my event ID?' and 'What does my package include?' were shipped
       here and FAIL the every-suggestion-answers-confidently rule when actually asked
       (none and weak respectively, checked 2 Aug 2026). Replaced with checked ones. */
    'Dashboard':           ['How do I add someone to my team?', 'How do I edit my event details?', 'What’s the difference between the free plan and paid plans?'],
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

  /* The six doors: five lifecycle topics and Something else, which always sits
     last and carries no routing hint - it exists so nobody stares at five wrong
     labels. `hint` is the routing phrase that rides on the question; `icon` is a
     24-box stroke path. Override with CFG.topics if the app needs different doors.

     `qs` is PARKED: suggested questions were taken out of the flow on 2 Aug 2026
     (Gareth's call - this version leads with the person's own question). The data
     stays because every entry was verified to answer strongly against the live
     corpus, and re-verifying is the expensive part of bringing them back. */
  var TOPICS = CFG.topics || [
    { key: 'submissions', label: 'Submissions', hint: 'collecting abstract submissions or the submission form',
      icon: '<path d="M14 3H6a1 1 0 00-1 1v16a1 1 0 001 1h12a1 1 0 001-1V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h6"/>',
      qs: ['How do I change the submission deadline?', 'Why does a submission show as incomplete?', 'How do I make a submission on behalf of someone else?'] },
    { key: 'reviewing', label: 'Reviewing & decisions', hint: 'reviewing, reviewers or recording decisions',
      icon: '<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6-10-6-10-6z"/><circle cx="12" cy="12" r="2.6"/>',
      qs: ['How do I assign submissions to reviewers?', 'Why can’t my reviewers see their assigned reviews?', 'How do I let submitters know their outcome?'] },
    { key: 'emails', label: 'Emails', hint: 'sending emails from the system',
      icon: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
      qs: ['Why have my submitters not received my email?', 'How do I schedule an email for later?', 'Can I send from my own address?'] },
    { key: 'registration', label: 'Registration & payments', hint: 'delegate registration, tickets, payments or invoices',
      icon: '<path d="M3 9V7a2 2 0 012-2h14a2 2 0 012 2v2a2 2 0 000 6v2a2 2 0 01-2 2H5a2 2 0 01-2-2v-2a2 2 0 000-6z"/><path d="M13 5v2M13 11v2M13 17v2"/>',
      qs: ['How do I set up tickets?', 'How do I refund an attendee?', 'Can attendees pay by bank transfer or invoice?'] },
    { key: 'conference', label: 'Conference platform', hint: 'the conference platform, programme or sessions',
      icon: '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/>',
      qs: ['How do I create sessions?', 'How do I publish the programme?', 'How do we set up the poster gallery?'] },
    { key: 'other', label: 'Something else', hint: '',
      icon: '<circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/>',
      qs: [] }
  ];

  /* Which door matches the screen the admin is standing on. Only confident matches;
     an unmapped screen (Dashboard, Event setup...) simply shows no badge. */
  var SCREEN_TOPIC = {
    'Abstract Management': 'submissions', 'Symposium': 'submissions',
    'Emails': 'emails',
    'Registration': 'registration',
    'Conference': 'conference', 'Speaker Management': 'conference', 'Website Builder': 'conference'
  };

  var state = { open: false, busy: false, history: [], started: false, topic: null, view: 'home' };

  /* ---------- styles ----------
     The visual language is the admin-help prototype's, ported wholesale on Gareth's
     call (2 Aug 2026): cream panel, Gloock display headings over Outfit body, the
     round red send, and the full-width Raise-a-support-ticket button that is always
     in view - escalation must be unmissable without shouting. The widget injects
     the Google Fonts link itself, because the pages it drops into do not load
     these fonts. */
  var FONT = "'Outfit',ui-sans-serif,system-ui,sans-serif";
  var DISPLAY = "'Gloock',Georgia,serif";
  var CSS = [
    '.oahw-launch{position:fixed;right:22px;bottom:22px;z-index:Z;display:inline-flex;align-items:center;gap:9px;',
    ' background:#0A1B3E;color:#fff;border:none;border-radius:9999px;padding:13px 20px;font-family:FONT;',
    ' font-size:16px;font-weight:500;cursor:pointer;box-shadow:0 10px 30px rgba(10,27,62,.35)}',
    '.oahw-launch:hover{background:#16254a}',
    '.oahw-launch svg{width:19px;height:19px;flex-shrink:0}',
    '.oahw-panel{position:fixed;right:22px;bottom:22px;z-index:Z;width:400px;max-width:calc(100vw - 24px);',
    ' height:600px;max-height:calc(100vh - 44px);background:#EAECE1;border:1px solid #0A1B3E;border-radius:14px;',
    ' box-shadow:0 24px 60px rgba(10,27,62,.35);display:flex;flex-direction:column;overflow:hidden;',
    ' font-family:FONT;color:#0A1B3E;transform-origin:bottom right;animation:oahw-pop .22s ease-out;transition:width .2s ease}',
    '.oahw-panel.oahw-wide{width:680px;height:calc(100vh - 44px)}',
    '@keyframes oahw-pop{from{opacity:0;transform:scale(.94) translateY(8px)}to{opacity:1;transform:none}}',
    '@keyframes oahw-rise{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}',
    '.oahw-head{padding:18px 20px 14px;border-bottom:1px solid rgba(10,27,62,.14);display:flex;',
    ' align-items:flex-start;justify-content:space-between;gap:12px}',
    '.oahw-head b{font-family:DISPLAY;font-weight:400;font-size:24px;line-height:1.1;letter-spacing:-.01em;display:block}',
    '.oahw-head span{display:flex;align-items:center;gap:6px;font-size:13px;color:#5a6377;margin-top:5px}',
    '.oahw-pin{width:7px;height:7px;border-radius:50%;background:#1F6F5C;flex:none}',
    '.oahw-x{background:none;border:none;color:#0A1B3E;cursor:pointer;padding:4px;border-radius:6px;line-height:0}',
    '.oahw-x:hover{background:rgba(10,27,62,.08)}',
    '.oahw-back{background:none;border:none;color:#0A1B3E;font-size:24px;line-height:1;cursor:pointer;',
    ' padding:0 10px 0 0;flex:none;margin-top:1px}',
    '.oahw-back:hover{color:#C54538}',
    '.oahw-hgroup{display:flex;align-items:flex-start;min-width:0}',
    /* the topic screen */
    '.oahw-home{flex:1;overflow-y:auto;padding:20px 16px 14px}',
    '.oahw-hh{font-family:DISPLAY;font-weight:400;font-size:22px;letter-spacing:-.01em;margin:0 0 4px}',
    '.oahw-hsub{font-size:13.5px;color:#5a6377;margin:0 0 14px}',
    '.oahw-tiles{display:grid;grid-template-columns:1fr 1fr;gap:9px}',
    '.oahw-tile{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:8px;text-align:left;',
    ' background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:12px 12px 11px;font-family:FONT;',
    ' font-size:13.5px;font-weight:600;line-height:1.25;color:#0A1B3E;cursor:pointer;min-height:74px;',
    ' box-shadow:0 1px 2px rgba(10,27,62,.04)}',
    '.oahw-tile:hover{border-color:#C54538}',
    '.oahw-tile:hover svg{color:#C54538}',
    '.oahw-tile svg{width:19px;height:19px;color:#0A1B3E;flex:none}',
    '.oahw-here{position:absolute;top:9px;right:10px;font-size:10px;font-weight:700;letter-spacing:.05em;',
    ' text-transform:uppercase;color:#C54538;background:rgba(197,69,56,.1);border-radius:9999px;padding:3px 8px}',
    /* the shiny intro card */
    '.oahw-intro{position:relative;overflow:hidden;border-radius:14px;padding:22px 20px 20px;color:#EAECE1;',
    ' background:radial-gradient(120% 90% at 85% -10%,rgba(197,69,56,.55),transparent 55%),',
    ' radial-gradient(100% 80% at -10% 110%,rgba(78,90,49,.5),transparent 55%),linear-gradient(135deg,#0A1B3E,#1b2f63);',
    ' box-shadow:0 10px 28px rgba(10,27,62,.35);transition:opacity .4s ease,transform .4s ease}',
    '.oahw-intro.oahw-igone{opacity:0;transform:translateY(-12px) scale(.97)}',
    '.oahw-ipill{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;',
    ' border:1px solid rgba(234,236,225,.45);border-radius:9999px;padding:4px 12px;margin-bottom:12px;',
    ' color:#EAECE1;position:relative;z-index:1}',
    '.oahw-ihead{margin:0 0 8px;font-family:DISPLAY;font-weight:400;font-size:24px;line-height:1.15;position:relative;z-index:1}',
    '.oahw-ihead span{color:#e9a89e}',
    '.oahw-ibody{margin:0 0 12px;font-size:14.5px;line-height:1.55;color:rgba(234,236,225,.92);position:relative;z-index:1}',
    '.oahw-iask{margin:0;font-size:13.5px;font-weight:600;color:#e9a89e;position:relative;z-index:1;',
    ' animation:oahw-nudge 2.2s ease-in-out infinite}',
    '.oahw-st{position:absolute;font-style:normal;font-size:13px;color:rgba(234,236,225,.8);pointer-events:none;',
    ' animation:oahw-tw 2.8s ease-in-out infinite}',
    '@keyframes oahw-tw{0%,100%{opacity:.15;transform:scale(.7) rotate(-10deg)}50%{opacity:.95;transform:scale(1.1) rotate(12deg)}}',
    '@keyframes oahw-nudge{0%,100%{transform:translateY(0)}50%{transform:translateY(3px)}}',
    '@media (prefers-reduced-motion:reduce){.oahw-st{animation:none;opacity:.6}.oahw-iask{animation:none}',
    ' .oahw-intro{transition:none}}',
    '.oahw-body{flex:1;overflow-y:auto;padding:18px 16px;display:flex;flex-direction:column;gap:14px}',
    '.oahw-row{display:flex;gap:8px;align-items:flex-end;max-width:88%;align-self:flex-start;animation:oahw-rise .25s ease-out}',
    '.oahw-av{width:26px;height:26px;border-radius:50%;background:#fff;border:1px solid #E5E7EB;flex:none;',
    ' display:grid;place-items:center}',
    '.oahw-av svg{width:15px;height:13px;display:block}',
    '.oahw-msg{max-width:88%;padding:12px 15px;border-radius:12px;font-size:15.5px;line-height:1.5;animation:oahw-rise .25s ease-out}',
    '.oahw-row .oahw-msg{max-width:100%;animation:none}',
    '.oahw-bot{background:#fff;border:1px solid #E5E7EB;border-bottom-left-radius:4px}',
    '.oahw-bot p{margin:0 0 10px}.oahw-bot p:last-child{margin:0}',
    '.oahw-bot strong{font-weight:600}',
    '.oahw-you{background:#0A1B3E;color:#fff;align-self:flex-end;border-bottom-right-radius:4px}',
    '.oahw-from{border-top:1px solid #E5E7EB;margin-top:11px;padding-top:10px}',
    '.oahw-from p{font-size:12.5px;color:#5a6377;margin:0 0 5px}',
    '.oahw-from a{display:flex;align-items:center;gap:7px;font-size:14.5px;color:#0A1B3E;text-decoration:underline;',
    ' text-underline-offset:3px;text-decoration-thickness:1px;padding:3px 0;cursor:pointer}',
    '.oahw-from a:hover{color:#C54538}',
    '.oahw-from a svg{width:13px;height:13px;flex:none;color:#C54538}',
    '.oahw-chips{display:flex;flex-wrap:wrap;gap:8px;align-self:flex-start;max-width:95%}',
    '.oahw-chip{border:1px solid rgba(10,27,62,.28);background:#fff;border-radius:9999px;padding:8px 14px;',
    ' font-family:FONT;font-size:14px;color:#0A1B3E;cursor:pointer;text-align:left}',
    '.oahw-chip:hover{border-color:#C54538;color:#C54538}',
    '.oahw-chip.oahw-solid{background:#C54538;border-color:#C54538;color:#fff;font-weight:500}',
    '.oahw-chip.oahw-solid:hover{background:#ab3a2f;color:#fff}',
    '.oahw-verdict{display:flex;flex-wrap:wrap;gap:8px;align-self:flex-start;max-width:95%}',
    '.oahw-vbtn{display:inline-flex;align-items:center;gap:7px;border:1px solid rgba(10,27,62,.18);background:#fff;',
    ' border-radius:9999px;padding:7px 14px;font-family:FONT;font-size:13.5px;color:#0A1B3E;cursor:pointer}',
    '.oahw-vbtn:hover{border-color:rgba(10,27,62,.45)}',
    '.oahw-vbtn svg{width:14px;height:14px;flex:none}',
    '.oahw-vyes svg{color:#4E5A31}.oahw-vno svg{color:#5a6377}',
    '.oahw-vdone{display:inline-flex;align-items:center;gap:7px;align-self:flex-start;font-size:13.5px;font-weight:500}',
    '.oahw-vdone svg{width:14px;height:14px;color:#4E5A31}',
    '.oahw-typing{display:inline-flex;align-items:center;gap:5px;background:#fff;border:1px solid #E5E7EB;',
    ' border-radius:12px;border-bottom-left-radius:4px;padding:14px 16px}',
    '.oahw-typing i{width:7px;height:7px;border-radius:50%;background:#9aa3b5;animation:oahw-b 1.2s infinite}',
    '.oahw-typing i:nth-child(2){animation-delay:.2s}.oahw-typing i:nth-child(3){animation-delay:.4s}',
    '@keyframes oahw-b{0%,80%,100%{opacity:.35;transform:translateY(0)}40%{opacity:1;transform:translateY(-3px)}}',
    '@media (prefers-reduced-motion:reduce){.oahw-typing i,.oahw-panel,.oahw-msg,.oahw-row{animation:none}}',
    '.oahw-foot{border-top:1px solid rgba(10,27,62,.14);padding:12px 16px}',
    '.oahw-ask{display:flex;gap:8px}',
    '.oahw-ask input{flex:1;font-family:FONT;font-size:15.5px;padding:11px 14px;border:1px solid rgba(10,27,62,.3);',
    ' border-radius:9999px;background:#fff;color:#0A1B3E;min-width:0}',
    '.oahw-ask input::placeholder{color:#8a92a3}',
    '.oahw-ask input:focus{outline:none;border-color:#0A1B3E}',
    '.oahw-send{background:#C54538;border:none;color:#fff;border-radius:50%;width:44px;height:44px;',
    ' cursor:pointer;flex:none;display:grid;place-items:center}',
    '.oahw-send:hover{background:#ab3a2f}',
    '.oahw-send[disabled]{opacity:.5;cursor:not-allowed}',
    '.oahw-send svg{width:18px;height:18px}',
    '.oahw-mic{background:#fff;border:1px solid rgba(10,27,62,.3);color:#0A1B3E;border-radius:50%;width:44px;height:44px;',
    ' cursor:pointer;flex:none;display:grid;place-items:center}',
    '.oahw-mic:hover{border-color:#0A1B3E}',
    '.oahw-mic svg{width:18px;height:18px}',
    '.oahw-mic.oahw-listening{background:#C54538;border-color:#C54538;color:#fff;animation:oahw-micpulse 1.2s ease-in-out infinite}',
    '@keyframes oahw-micpulse{0%,100%{box-shadow:0 0 0 0 rgba(197,69,56,.35)}50%{box-shadow:0 0 0 9px rgba(197,69,56,0)}}',
    '@media (prefers-reduced-motion:reduce){.oahw-mic.oahw-listening{animation:none}}',
    /* Escalation must be unmissable without shouting: a real button, full width,
       always in view - not a line of small print. Carried from the prototype. */
    '.oahw-ticket{display:flex;align-items:center;justify-content:center;gap:9px;margin-top:10px;',
    ' padding:11px 16px;border:1.5px solid #0A1B3E;border-radius:9999px;background:#fff;color:#0A1B3E;',
    ' font-family:FONT;font-size:15px;font-weight:500;text-decoration:none;cursor:pointer}',
    '.oahw-ticket:hover{background:#0A1B3E;color:#fff}',
    '.oahw-ticket svg{width:17px;height:17px;flex:none}',
    '.oahw-reader{flex:1;overflow-y:auto;padding:22px 28px;background:#fff}',
    '.oahw-reader h1{font-family:DISPLAY;font-weight:400;font-size:26px;line-height:1.15;margin:0 0 16px}',
    '.oahw-reader h2{font-size:19px;font-weight:600;margin:22px 0 8px}',
    '.oahw-reader h3{font-size:16.5px;font-weight:600;margin:18px 0 6px}',
    '.oahw-reader p{margin:0 0 12px;font-size:15.5px}',
    '.oahw-reader ul,.oahw-reader ol{margin:0 0 14px 22px;font-size:15.5px}',
    '.oahw-reader li{margin-bottom:6px}',
    '.oahw-reader img{max-width:100%;height:auto;border:1px solid #E5E7EB;border-radius:8px;margin:6px 0 14px}',
    '.oahw-reader a{color:#C54538;text-underline-offset:3px}',
    '.oahw-reader strong{font-weight:600}',
    '.oahw-reader .anchor{display:none}',
    '.oahw-rbar{display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid #E5E7EB;background:#fff}',
    '.oahw-rbar button{display:inline-flex;align-items:center;gap:7px;background:none;border:none;cursor:pointer;',
    ' color:#0A1B3E;font-family:FONT;font-size:15px;font-weight:500;padding:6px 10px;border-radius:8px}',
    '.oahw-rbar button:hover{background:rgba(10,27,62,.07)}',
    '.oahw-rbar button svg{width:16px;height:16px;flex:none}',
    '.oahw-rbar a{margin-left:auto;font-family:FONT;font-size:13.5px;color:#5a6377;text-decoration:underline;',
    ' text-underline-offset:3px}',
    '.oahw-rbar a:hover{color:#C54538}',
    '@media (max-width:700px){.oahw-panel{right:8px;bottom:8px;left:8px;width:auto;height:calc(100vh - 16px)}}',
    '.oahw-hidden{display:none !important}'
  ].join('\n').replace(/Z/g, String(CFG.zIndex))
   .replace(/FONT/g, FONT).replace(/DISPLAY/g, DISPLAY);

  /* The OA mark from the brand favicon, inlined with an explicit navy fill: the
     favicon file itself flips white under prefers-color-scheme:dark, which on a
     white avatar circle would vanish. Carried from the prototype. */
  var AVATAR = '<svg viewBox="0 0 50 44" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' +
    '<path fill="#0A1B3E" d="M44.4549 11.7562L37.8931 15.5549C40.8961 17.6207 42.8754 21.0864 42.8822 25.0006C42.8822 31.2933 37.7643 36.451 31.4601 36.4442C25.4677 36.4442 20.5124 31.7757 20.0514 25.8772L13.4761 29.6827C15.5707 37.6471 22.8917 43.6339 31.4601 43.6271C41.6892 43.6203 50.0406 35.2279 49.9999 24.987C49.9796 19.7953 47.8646 15.1132 44.4617 11.7494L44.4549 11.7562Z"/>' +
    '<path fill="#0A1B3E" d="M34.1716 6.61202L45.6005 0H31.6296L0 18.3071H13.971L14.1201 18.2187C13.2931 20.3186 12.8321 22.595 12.8254 24.9871C12.8254 25.0822 12.8254 25.1705 12.8321 25.2657L40.8961 9.01763C38.876 7.80803 36.5984 6.97898 34.1716 6.61202Z"/>' +
    '<path fill="#0A1B3E" d="M3.77575 20.2642C1.6879 20.2642 0 21.9631 0 24.0493V27.4403H7.15834V23.6552C7.15834 21.7796 5.64668 20.2642 3.77575 20.2642Z"/></svg>';
  var BUBBLE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg>';
  var PLANE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 20-7z"/></svg>';
  var MIC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2a3 3 0 013 3v6a3 3 0 01-6 0V5a3 3 0 013-3z"/><path d="M19 10v1a7 7 0 01-14 0v-1"/><path d="M12 18v4"/><path d="M8 22h8"/></svg>';
  var XICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" width="20" height="20"><path d="M18 6L6 18M6 6l12 12"/></svg>';
  var ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>';
  var LINKOUT = '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"/><path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"/></svg>';
  var TICK = '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd"/></svg>';
  var CROSS = '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>';

  function emit(name, detail) { try { if (CFG.onEvent) CFG.onEvent(name, detail || {}); } catch (e) {} }

  /* Canonical URL for a KB path. The API returns paths ending .html; under the KB's
     cleanUrls those answer with a 308 redirect, and the redirect carries no CORS
     header - so a cross-origin fetch dies there even though the page itself allows
     it. Fetching the extensionless URL goes straight to the page. */
  function kbUrl(path) {
    return CFG.kbBase + path.replace(/^\//, '').replace(/\.html$/, '');
  }

  function logEvent(question, answered, sources, action) {
    try {
      fetch(CFG.endpoint + '/api/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        keepalive: true,
        body: JSON.stringify({
          /* The chosen door rides in the screen column ("Emails · Registration &
             payments") - no schema change, and the sheet can group by it. The
             server caps this at 60 chars. */
          surface: 'widget',
          screen: CFG.screen + (state.topic ? ' · ' + state.topic.label : ''),
          question: question,
          answered: answered, sources: (sources || []).map(function (s) { return s.path; }),
          action: action
        })
      }).catch(function () {});
    } catch (e) {}
    emit('log', { action: action, answered: answered });
  }

  /* ---------- DOM ---------- */
  var root, panel, home, body, foot, input, reader, readerBody, readerOpen;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  function build() {
    /* The brand fonts, injected only when the page has not already loaded them -
       the admin app's pages do not carry Gloock or Outfit. */
    if (!document.querySelector('link[href*="family=Gloock"]')) {
      ['https://fonts.googleapis.com', 'https://fonts.gstatic.com'].forEach(function (h) {
        var pc = document.createElement('link');
        pc.rel = 'preconnect'; pc.href = h;
        if (h.indexOf('gstatic') >= 0) pc.crossOrigin = '';
        document.head.appendChild(pc);
      });
      var fl = document.createElement('link');
      fl.rel = 'stylesheet';
      fl.href = 'https://fonts.googleapis.com/css2?family=Gloock&family=Outfit:wght@300;400;500;600&display=swap';
      document.head.appendChild(fl);
    }

    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);

    root = el('div');
    var launch = el('button', 'oahw-launch');
    launch.type = 'button';
    launch.innerHTML = BUBBLE + 'Help';
    launch.setAttribute('aria-label', 'Open help');
    launch.addEventListener('click', open);

    panel = el('div', 'oahw-panel oahw-hidden');
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Help');
    var head = el('div', 'oahw-head');
    var hgroup = el('div', 'oahw-hgroup');
    var backHome = el('button', 'oahw-back oahw-hidden', '‹');
    backHome.type = 'button';
    backHome.setAttribute('aria-label', 'Back to topics');
    backHome.addEventListener('click', showHome);
    var ht = el('div');
    var title = el('b', null, 'Help');
    ht.appendChild(title);
    var where = el('span');
    var pin = el('i', 'oahw-pin');
    pin.setAttribute('aria-hidden', 'true');
    var subText = el('span');
    where.append(pin, subText);
    ht.appendChild(where);
    hgroup.append(backHome, ht);
    var x = el('button', 'oahw-x');
    x.type = 'button';
    x.innerHTML = XICON;
    x.setAttribute('aria-label', 'Close help');
    x.addEventListener('click', close);
    head.append(hgroup, x);
    state._title = title; state._sub = subText; state._back = backHome;

    home = el('div', 'oahw-home oahw-hidden');

    body = el('div', 'oahw-body');

    var rbar = el('div', 'oahw-rbar oahw-hidden');
    var back = el('button');
    back.type = 'button';
    back.innerHTML = ARROW + 'Back to chat';
    back.addEventListener('click', closeReader);
    readerOpen = el('a', null, 'Open in the help centre ↗');
    readerOpen.target = '_blank'; readerOpen.rel = 'noopener';
    rbar.append(back, readerOpen);
    reader = el('div', 'oahw-reader oahw-hidden');
    readerBody = reader;

    foot = el('div', 'oahw-foot');
    var askRow = el('div', 'oahw-ask');
    input = el('input');
    input.type = 'text';
    input.placeholder = 'Ask in your own words…';
    input.setAttribute('aria-label', 'Your question');
    var mic = el('button', 'oahw-mic');
    mic.type = 'button';
    mic.innerHTML = MIC;
    mic.setAttribute('aria-label', 'Ask by voice');
    mic.setAttribute('aria-pressed', 'false');
    mic.title = 'Ask by voice — the words appear in the box for you to check';
    var send = el('button', 'oahw-send');
    send.type = 'button';
    send.innerHTML = PLANE;
    send.setAttribute('aria-label', 'Send');
    var go = function () { var q = input.value.trim(); if (q) { input.value = ''; ask(q); } };
    send.addEventListener('click', go);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });
    askRow.append(input, mic, send);

    /* Escalation, always in view - carried from the prototype, where it was a rule:
       a person one tap away, never buried behind a failure state. */
    var ticket = el('a', 'oahw-ticket');
    ticket.href = CFG.ticketUrl;
    ticket.target = '_blank'; ticket.rel = 'noopener';
    ticket.title = 'A person will pick it up — no question is too small';
    ticket.innerHTML = PLANE + 'Raise a support ticket';
    ticket.addEventListener('click', function () { emit('ticket', { from: 'footer' }); });
    foot.append(askRow, ticket);
    wireVoice(mic);

    panel.append(head, rbar, home, body, reader, foot);
    root.append(launch, panel);
    document.body.appendChild(root);
    state._launch = launch; state._rbar = rbar; state._send = send;
  }

  /* ---------- the topic screen ---------- */
  /* Rebuilt on every visit rather than once: in a SPA the screen name changes under
     us, and the badge and popular questions must follow it. */
  function renderHome() {
    home.innerHTML = '';
    home.appendChild(el('p', 'oahw-hh', 'What do you need a hand with?'));
    home.appendChild(el('p', 'oahw-hsub', 'Pick a topic — or just type your question below.'));

    var hereKey = SCREEN_TOPIC[CFG.screen] || null;
    var tiles = el('div', 'oahw-tiles');
    /* The door matching their screen leads, but the other five keep lifecycle
       order - a fully re-sorted grid would put familiar doors somewhere new on
       every screen. */
    var ordered = TOPICS.slice().sort(function (a, b) {
      return (b.key === hereKey) - (a.key === hereKey);
    });
    ordered.forEach(function (t) {
      var tile = el('button', 'oahw-tile');
      tile.type = 'button';
      tile.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" ' +
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + t.icon + '</svg>';
      tile.appendChild(el('span', null, t.label));
      if (t.key === hereKey) tile.appendChild(el('span', 'oahw-here', 'You’re here'));
      tile.addEventListener('click', function () { enterTopic(t); });
      tiles.appendChild(tile);
    });
    home.appendChild(tiles);

    /* No "prefer a person?" line here any more: the full-width ticket button now
       lives in the footer, in view on this screen too. One escalation, not two. */
  }

  function showHome() {
    state.view = 'home';
    renderHome();
    home.classList.remove('oahw-hidden');
    body.classList.add('oahw-hidden');
    state._back.classList.add('oahw-hidden');
    state._title.textContent = 'Help';
    state._sub.textContent = CFG.screen
      ? 'You’re on ' + CFG.screen + ' — I’ll take that into account'
      : 'Answers from the people who built it';
    input.placeholder = 'Instant answers — ask in your own words…';
    emit('home', { screen: CFG.screen });
  }

  function showChat() {
    state.view = 'chat';
    state.started = true;
    home.classList.add('oahw-hidden');
    body.classList.remove('oahw-hidden');
    state._back.classList.remove('oahw-hidden');
    state._title.textContent = 'Instant answers';
    state._sub.textContent = state.topic
      ? state.topic.label
      : (CFG.screen ? 'You’re on ' + CFG.screen + ' — I’ll take that into account' : 'Ask in your own words');
    input.placeholder = 'Ask in your own words…';
    scrollDown();
  }

  function enterTopic(t) {
    state.topic = t;
    showChat();
    addIntro(t);
    input.focus();
    emit('topic', { key: t.key, label: t.label });
  }

  /* The moment between choosing a door and typing: a short, deliberately shiny
     card that says what this thing actually is. It looks nothing like the plain
     chat that follows on purpose - the contrast is the excitement - and it
     collapses away the instant the first question is asked. */
  function addIntro(t) {
    var old = body.querySelector('.oahw-intro');
    if (old) old.remove();
    var card = el('div', 'oahw-intro');
    card.innerHTML =
      '<i class="oahw-st" style="left:8%;top:14%;animation-delay:0s">✦</i>' +
      '<i class="oahw-st" style="right:10%;top:22%;animation-delay:.7s;font-size:11px">✦</i>' +
      '<i class="oahw-st" style="left:16%;bottom:18%;animation-delay:1.3s;font-size:10px">✦</i>' +
      '<i class="oahw-st" style="right:7%;bottom:26%;animation-delay:.4s">✦</i>';
    card.appendChild(el('span', 'oahw-ipill', t.label));
    var h = el('p', 'oahw-ihead');
    h.innerHTML = 'Instant answers <span aria-hidden="true">✦</span>';
    card.appendChild(h);
    card.appendChild(el('p', 'oahw-ibody',
      'This chat searches everything we’ve ever recorded about running events and answers in seconds.'));
    card.appendChild(el('p', 'oahw-iask', 'Ask as though you were speaking to a real person ↓'));
    body.appendChild(card);
    scrollDown();
  }

  function collapseIntro() {
    var card = body.querySelector('.oahw-intro');
    if (!card) return;
    card.classList.add('oahw-igone');
    setTimeout(function () { card.remove(); }, 450);
  }

  function open() {
    state.open = true;
    state._launch.classList.add('oahw-hidden');
    panel.classList.remove('oahw-hidden');
    /* First open lands on the topic doors. Reopening mid-conversation goes back to
       the conversation - the doors are an entrance, not a toll booth. */
    if (state.started) showChat(); else showHome();
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
    var av = el('span', 'oahw-av');
    av.innerHTML = AVATAR;
    row.appendChild(av);
    return row;
  }

  /* Voice input, carried from the prototype with its trust rule intact: the
     transcript lands in the box to be read and edited, never auto-sent, because
     acting on a silent mishearing costs more trust than two seconds of review.
     No browser support means no button; typing always works. */
  function wireVoice(btn) {
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { btn.classList.add('oahw-hidden'); return; }
    var rec = null, listening = false;
    btn.addEventListener('click', function () {
      if (listening) { try { rec.stop(); } catch (e) {} return; }
      rec = new SR();
      rec.lang = 'en-GB';
      rec.interimResults = true;     // words appear as they are spoken
      rec.continuous = false;        // one question, stops itself on silence
      rec.onstart = function () {
        listening = true;
        btn.classList.add('oahw-listening');
        btn.setAttribute('aria-pressed', 'true');
        input.placeholder = 'Listening…';
      };
      rec.onresult = function (e) {
        var t = '';
        for (var i = 0; i < e.results.length; i++) t += e.results[i][0].transcript;
        input.value = t.trim();
      };
      rec.onerror = function () {};  // denied mic must never block the box
      rec.onend = function () {
        listening = false;
        btn.classList.remove('oahw-listening');
        btn.setAttribute('aria-pressed', 'false');
        input.placeholder = 'Ask in your own words…';
        input.focus();
      };
      try { rec.start(); } catch (e) {}
    });
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
        var a = el('a');
        a.innerHTML = LINKOUT;
        a.appendChild(document.createTextNode(s.title));
        a.href = kbUrl(s.path);
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
    if (state.topic && state.topic.hint) q += '[Their question is about ' + state.topic.hint + '] ';
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
    if (state.view !== 'chat') showChat();     // typing from the doors skips them
    collapseIntro();                           // the shiny card yields to the conversation
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
  /* pageUrl, not kbUrl: a parameter named kbUrl shadowed the kbUrl() helper above,
     so fetch(kbUrl(path)) called a string and threw before fetching anything. */
  function openReader(path, pageUrl) {
    panel.classList.add('oahw-wide');
    body.classList.add('oahw-hidden');
    foot.classList.add('oahw-hidden');
    state._back.classList.add('oahw-hidden');   // the reader bar has its own Back
    state._rbar.classList.remove('oahw-hidden');
    reader.classList.remove('oahw-hidden');
    readerOpen.href = pageUrl;
    reader.innerHTML = '<p>Opening the guide…</p>';
    fetch(kbUrl(path))
      .then(function (r) { if (!r.ok) throw new Error('status'); return r.text(); })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, 'text/html');
        var title = doc.querySelector('h1');
        var prose = doc.querySelector('.prose');
        if (!prose) throw new Error('no article body');
        var base = CFG.kbBase + path.replace(/^\//, '');   // .html kept: relative srcs resolve the same
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
        window.open(pageUrl, '_blank');
      });
  }
  function closeReader() {
    panel.classList.remove('oahw-wide');
    reader.classList.add('oahw-hidden');
    state._rbar.classList.add('oahw-hidden');
    body.classList.remove('oahw-hidden');
    foot.classList.remove('oahw-hidden');
    state._back.classList.remove('oahw-hidden'); // always returns to the conversation
    scrollDown();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
