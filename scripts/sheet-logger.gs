/**
 * Google Apps Script for the master help-performance sheet.
 *
 * One event log, every surface. The KB search, the in-app help widget and the
 * support form all POST the same seven-column row via api/log.js; article-page
 * feedback arrives via api/feedback.js. Everything on the Dashboard is a formula
 * over the Log tab, so the script only ever appends - nothing is computed here.
 *
 * The Dashboard reads as four bands: an all-surfaces strip, then one section per
 * surface - Knowledge base, Help widget, Support deflection - because the three
 * behave differently and blending them hides exactly the differences that matter.
 * Every formula carries two guards: its own surface, and "not a test row". Rows
 * whose question contains "safe to delete" are excluded from every number, so
 * connection tests can keep happening without polluting what Kristy reads.
 *
 * The Dashboard measures whether the help centre is performing. "What people ask"
 * measures something the Dashboard cannot see: what readers keep needing, whether
 * or not we answered it well. A question asked thirty times a month and answered
 * every time is not a success - it is the help centre absorbing the cost of
 * something confusing further upstream. "Topic history" keeps a monthly count so
 * that trend outlives the raw rows.
 *
 * The "Staff suggestions" tab is the exception to the pattern and deliberately so.
 * Everything else here is anonymous reader telemetry; that tab is internal staff
 * writing to a named colleague, so it carries a name and an email on purpose and
 * api/suggest.js does not scrub them. Its last two columns (Status, Notes) belong
 * to whoever triages it: a new row arrives as "New" with empty notes, and because
 * the script only ever appends, nothing already typed there can be overwritten.
 *
 * SETUP (about five minutes, once)
 *  1. Create a Google Sheet called "OA help — performance".
 *  2. Extensions → Apps Script. Delete the placeholder, paste this file, Save.
 *  3. Edit TOKEN below to a long random string of your choosing.
 *  4. Run → setup  (once). It builds every tab, the dashboard and the live views,
 *     and Google will ask you to authorise the script.
 *  5. Deploy → New deployment → Web app.
 *       Execute as: Me.   Who has access: Anyone.
 *     ("Anyone" is what lets the Vercel function post; the TOKEN is the actual lock.)
 *  6. Copy the web app URL. In Vercel → Settings → Environment Variables add:
 *       SHEET_WEBHOOK_URL = <the web app URL>
 *       SHEET_TOKEN       = <the same string as TOKEN below>
 *     Redeploy. Nothing else needs to change.
 *
 * UPDATING AN ALREADY-DEPLOYED SCRIPT
 *  - Dashboard-only changes (buildDashboard, setup): paste, Save, Run → setup.
 *    Done - the web app is not involved, so no redeploy is needed.
 *  - Anything touching doPost: paste, Save, Run → setup, then
 *    Deploy → Manage deployments → the pencil → Version: New version → Deploy.
 *    A web app keeps serving the version it was deployed at, so saving alone
 *    changes nothing the outside world can see. Skipping this is the reason a
 *    "correct" script appears to ignore a new field.
 *    The web app URL does not change, so Vercel needs no edit.
 *
 * Event vocabulary (the Log tab's last column):
 *   asked            a question completed; the Answered column says whether an
 *                    answer was shown. One per question, every surface.
 *   solved           reader clicked "This solved it"
 *   unhelpful        reader clicked "This didn't help me"
 *   ticket_created   reader clicked through to the support form (KB and widget)
 *   sent_anyway      support form: answer shown, ticket sent regardless
 *   not_interrupted  support form: answer too weak or slow to interrupt with
 *   opened_article   reader opened a suggested guide
 *
 * Rows arrive already stripped of emails and phone numbers by api/log.js.
 */

var TOKEN = 'change-me-to-something-long-and-random';

/* Set to an address to get an email whenever a staff suggestion arrives. Empty
   means no mail is sent. A failed send must never lose the row, so it is wrapped
   and happens only after the append. */
var NOTIFY = '';

var LOG       = 'Log';
var FEEDBACK  = 'Article feedback';
var SUGGEST   = 'Staff suggestions';
var DASH      = 'Dashboard';
var ASK       = 'What people ask';
var HIST      = 'Topic history';
var V_UNHELP  = "Didn't help";
var V_UNANS   = 'Unanswered';

/* Rows shown in each block of the "What people ask" tab. Bounded because two
   blocks share the tab and an unbounded list would grow into the one below it. */
var TOP_TOPICS  = 20;
var TOP_SCREENS = 15;

/* A topic gets the "Look upstream" prompt when it is asked at least this often in
   the window AND is answered well. Tune it to volume: the point is to catch a
   question that keeps being asked *despite* a good answer, which is a signal about
   the product rather than about the help centre. It is a prompt to go and look,
   never a verdict. */
var UPSTREAM_MIN_ASKS = 5;
var UPSTREAM_MIN_RATE = 0.8;

var HEAD_LOG      = ['Timestamp', 'Surface', 'Screen', 'Question', 'Answered',
                     'Articles shown', 'Event'];
var HEAD_FEEDBACK = ['Timestamp', 'Article', 'Helpful', 'Reason'];
var HEAD_SUGGEST  = ['Timestamp', 'Name', 'Team', 'Email', 'Type', 'Suggestion',
                     'Product area', 'Article or page', 'Link',
                     'Status', 'Notes'];

var STATUSES = ['New', 'Being looked at', 'Written up', 'Not needed'];

/* The site's own colours, so the sheet reads as part of the same product. */
var BRAND = {
  navy:  '#101C38',
  cream: '#EDEBE2',
  red:   '#D0432C',
  ink:   '#5F5E5A',
  faint: '#888880'
};

/* The reply carries `wrote`: the names of the things this script actually stored.
   A caller cannot otherwise tell "saved" from "did not recognise your payload" -
   an older deployment handed a kind of row it has never heard of falls straight
   through to ok:true and reports success for a write that never happened. Senders
   that care (api/suggest.js) check for their own name in this list. */
function doPost(e) {
  try {
    var body = JSON.parse(e.postData.contents);
    if (body.token !== TOKEN) return out({ ok: false, error: 'bad token' });
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var wrote = [];

    if (body.row) {
      var r = body.row;
      sheet(ss, LOG, HEAD_LOG).appendRow([
        r.ts ? new Date(r.ts) : new Date(),
        r.surface || '', r.screen || '', r.question || '',
        r.answered === true, r.sources || '', r.action || ''
      ]);
      wrote.push('row');
    }
    if (body.feedback) {
      var f = body.feedback;
      sheet(ss, FEEDBACK, HEAD_FEEDBACK).appendRow([
        f.ts ? new Date(f.ts) : new Date(),
        f.path || '', f.helpful === true, f.reason || ''
      ]);
      wrote.push('feedback');
    }
    if (body.suggestion) {
      var g = body.suggestion;
      // Status starts at 'New' on the row being created and Notes starts empty.
      // Both columns belong to whoever triages: appendRow can only add a row
      // beneath their work, so nothing they have typed is ever touched.
      suggestSheet(ss).appendRow([
        g.ts ? new Date(g.ts) : new Date(),
        g.name || '', g.team || '', g.email || '', g.type || '', g.text || '',
        g.section || '', g.article || '', g.link || '',
        STATUSES[0], ''
      ]);
      wrote.push('suggestion');
      notify(g);
    }
    return out({ ok: true, wrote: wrote });
  } catch (err) {
    return out({ ok: false, error: String(err) });
  }
}

/** Builds every tab, the dashboard and the live views. Safe to run more than once. */
function setup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  sheet(ss, LOG, HEAD_LOG);
  sheet(ss, FEEDBACK, HEAD_FEEDBACK);
  suggestSheet(ss);
  // Both views carry the same two exclusions as the dashboard. They did not before,
  // which meant the Dashboard and the tab you clicked through to disagreed about
  // the same week - the dashboard dropped test rows and these two listed them.
  buildView(ss, V_UNHELP,
    ['Timestamp', 'Surface', 'Screen', 'Question', 'Articles shown'],
    '=IFERROR(QUERY(' + LOG + '!A2:G, "select A,B,C,D,F where G=\'unhelpful\' and ' +
    NOT_TEST + ' order by A desc", 0), "")');
  buildView(ss, V_UNANS,
    ['Timestamp', 'Surface', 'Screen', 'Question'],
    '=IFERROR(QUERY(' + LOG + '!A2:G, "select A,B,C,D where G=\'asked\' and E=false and ' +
    NOT_TEST + ' order by A desc", 0), "")');
  buildAskTab(ss);
  histSheet(ss);
  buildDashboard(ss);
}

/* ============================== dashboard ============================== */

/* Weeks shown in each section's history table. Bounded on purpose: three sections
   stack vertically, and an open-ended SEQUENCE under the top one would spill its
   dates straight through the sections below it. */
var WEEKS = 8;

/* One COUNTIFS criteria pair, with the Log! prefix every range needs. */
function P(col, crit) { return ',' + LOG + '!' + col + ',' + crit; }

/* Every dashboard number excludes two kinds of traffic that are not readers.

   Test rows: the connection tests and diagnostics all carry this phrase in the
   question by convention, so one guard covers them. Keep using the phrase in any
   future test row.

   The internal team: a colleague switches their browser on once with
   ?oa-internal=1 and api/log.js then stores their surface as 'kb-search-internal'
   rather than 'kb-search'. Every per-surface figure below matches its surface
   exactly, so those already exclude staff without any change; this wildcard is
   what keeps them out of the all-surfaces totals too. It is a text match on the
   Surface column, which is never empty - the same shape as the test guard, and
   chosen over a new TRUE/FALSE column precisely because a blank boolean is a cell
   a COUNTIFS can read either way. */
var GUARD = P('D:D', '"<>*safe to delete*"') + P('B:B', '"<>*-internal"');

function surf(name) { return name ? P('B:B', '"' + name + '"') : ''; }

/* COUNTIFS over the last 7 days / the 7 before, plus criteria pairs. Every tile
   is an explicit formula - an earlier draft derived the comparison row from the
   headline row with regex surgery and broke the Answer rate tile, whose formula
   does not end where the regex assumed. */
function f7(extra) {
  return '=COUNTIFS(' + LOG + '!A:A,">="&TODAY()-7' + GUARD + extra + ')';
}
function fPrev(extra) {
  return '=COUNTIFS(' + LOG + '!A:A,">="&TODAY()-14,' + LOG + '!A:A,"<"&TODAY()-7' +
         GUARD + extra + ')';
}

/* Per-week COUNTIFS against a bounded Week column at rows a0..a1. */
function fw(a0, a1, extra) {
  var wk = 'A' + a0 + ':A' + a1;
  return '=ARRAYFORMULA(IF(' + wk + '="","",COUNTIFS(' + LOG + '!A:A,">="&' + wk +
         ',' + LOG + '!A:A,"<"&' + wk + '+7' + GUARD + extra + ')))';
}

/* The Week column itself: WEEKS Mondays, oldest first so a sparkline over the
   counts reads left-to-right in time. */
function weekCol() {
  return '=ARRAYFORMULA(SEQUENCE(' + WEEKS + ',1,' +
         'TODAY()-WEEKDAY(TODAY(),3)-' + (7 * (WEEKS - 1)) + ',7))';
}

/* Top-N grouped QUERY over the last 30 days, with the same test-row guard. */
function topQ(selectCol, where, source) {
  var src = source || (LOG + '!A2:G');
  return '=IFERROR(QUERY(' + src + ', "select ' + selectCol + ', count(A) where ' +
         where + ' and A >= date \'"&TEXT(TODAY()-30,"yyyy-mm-dd")&"\' ' +
         'group by ' + selectCol + ' order by count(A) desc limit 8 ' +
         'label ' + selectCol + ' \'\', count(A) \'\'", 0), "Nothing yet")';
}
var NOT_TEST = 'not lower(D) contains \'safe to delete\' and not lower(B) contains \'-internal\'';

function buildDashboard(ss) {
  var s = ss.getSheetByName(DASH) || ss.insertSheet(DASH, 0);
  s.clear();
  // clear() leaves merges, bandings and conditional formats behind, and a rebuilt
  // layout under stale ones looks broken in ways plain values never reveal.
  s.getRange(1, 1, 120, 20).breakApart();
  s.getBandings().forEach(function (b) { b.remove(); });
  s.setConditionalFormatRules([]);

  s.getRange('A1').setValue('Help performance').setFontWeight('bold').setFontSize(16);
  s.getRange('A2').setValue(
    'Each section counts only its own surface, so the three can be judged separately. ' +
    'Test rows ("safe to delete") are excluded from every number. ' +
    'Success = an answer was shown and the reader did not say it failed - silence counts as success.')
    .setFontSize(9).setFontColor(BRAND.ink).setFontStyle('italic');
  s.getRange('A2:N2').merge();

  /* ---- all surfaces, at a glance ---- */
  banner(s, 4, 'All surfaces — at a glance', null);
  tiles(s, 5, [
    ['Questions asked', f7(P('G:G', '"asked"')),
                        fPrev(P('G:G', '"asked"'))],
    ['Answer rate', rate7(surfNone(), 6), ratePrev(surfNone(), 7)],
    // Success = an answer was shown and the reader did not click "didn't help".
    // A deliberate assumption: silence counts as success. We never see inside the
    // reader's head, but this matches how deflection is conventionally counted.
    ['Success rate', success7(surfNone(), 6), successPrev(surfNone(), 7)],
    ['Solved', f7(P('G:G', '"solved"')), fPrev(P('G:G', '"solved"'))],
    ["Didn't help", f7(P('G:G', '"unhelpful"')), fPrev(P('G:G', '"unhelpful"'))],
    ['Unanswered', f7(P('G:G', '"asked"') + P('E:E', 'FALSE')),
                   fPrev(P('G:G', '"asked"') + P('E:E', 'FALSE'))],
    ['Escalated to a ticket', f7(P('G:G', '"ticket_created"')),
                              fPrev(P('G:G', '"ticket_created"'))]
  ]);
  s.getRange('C6:D7').setNumberFormat('0%');

  // Staff suggestions waiting for triage - the one number here that is a to-do,
  // not telemetry, which is why it sits apart from the tiles.
  var stCol = colLetter(HEAD_SUGGEST.indexOf('Status') + 1);
  s.getRange('K5').setValue('Suggestions waiting').setFontSize(9)
    .setFontColor(BRAND.ink).setFontWeight('bold');
  s.getRange('K6').setFormula(
    '=COUNTIF(\'' + SUGGEST + '\'!' + stCol + '2:' + stCol + ',"New")')
    .setFontSize(16).setFontColor(BRAND.red);

  /* ---- one section per surface ---- */
  askSection(s, 10, 'Knowledge base search', 'kb-search',
    ['What people asked and got nothing (30 days)',
     topQ('D', 'G=\'asked\' and E=false and B=\'kb-search\' and ' + NOT_TEST)],
    ['Articles readers voted "No" (30 days)',
     '=IFERROR(QUERY(\'' + FEEDBACK + '\'!A2:D, "select B, count(A) where C=false ' +
     'and A >= date \'"&TEXT(TODAY()-30,"yyyy-mm-dd")&"\' group by B ' +
     'order by count(A) desc limit 8 label B \'\', count(A) \'\'", 0), "Nothing yet")']);

  askSection(s, 26, 'Help widget (in the app)', 'widget',
    ['What people asked and got nothing (30 days)',
     topQ('D', 'G=\'asked\' and E=false and B=\'widget\' and ' + NOT_TEST)],
    ['Which app screens questions come from (30 days)',
     topQ('C', 'G=\'asked\' and B=\'widget\' and C is not null and C != \'\' and ' + NOT_TEST)]);

  deflectionSection(s, 42);

  /* ---- shared cosmetics ---- */
  s.setColumnWidth(1, 110);
  for (var c = 2; c <= 9; c++) s.setColumnWidth(c, 94);
  s.setColumnWidth(10, 14);            // J spacer
  s.setColumnWidth(11, 340);           // K list
  s.setColumnWidth(12, 64);            // L count
  s.setColumnWidth(13, 14);            // M spacer
  s.setColumnWidth(14, 340);           // N list
  s.setColumnWidth(15, 64);            // O count
  s.setFrozenRows(2);

  // Rates below half get red text. Applied to answer/success/shown-in-time
  // columns only - deflection *rate* is excluded on purpose, because 10-30% is a
  // perfectly good deflection rate and a permanently red column teaches Kristy
  // to ignore red.
  var redBelowHalf = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberLessThan(0.5).setFontColor(BRAND.red)
    .setRanges([s.getRange('C6:D7'),
                s.getRange('C12:D13'), s.getRange('C16:D23'),
                s.getRange('C28:D29'), s.getRange('C32:D39'),
                s.getRange('D44:D45'), s.getRange('D48:D55')])
    .build();
  s.setConditionalFormatRules([redBelowHalf]);
}

/* A KB-shaped or widget-shaped section: same funnel, different surface.
   Layout from `top`: banner, tiles (labels/now/before), weekly table, two lists. */
function askSection(s, top, title, surface, listK, listN) {
  var w0 = top + 6, w1 = w0 + WEEKS - 1;          // weekly data rows
  var SURF = surf(surface);
  var vRow = top + 2;                              // the "last 7 days" value row

  banner(s, top, title, 'B' + w0 + ':B' + w1);
  tiles(s, top + 1, [
    ['Asked', f7(P('G:G', '"asked"') + SURF), fPrev(P('G:G', '"asked"') + SURF)],
    ['Answer rate', rate7(SURF, vRow), ratePrev(SURF, vRow + 1)],
    ['Success rate', success7(SURF, vRow), successPrev(SURF, vRow + 1)],
    ['Solved', f7(P('G:G', '"solved"') + SURF), fPrev(P('G:G', '"solved"') + SURF)],
    ["Didn't help", f7(P('G:G', '"unhelpful"') + SURF),
                    fPrev(P('G:G', '"unhelpful"') + SURF)],
    ['Unanswered', f7(P('G:G', '"asked"') + P('E:E', 'FALSE') + SURF),
                   fPrev(P('G:G', '"asked"') + P('E:E', 'FALSE') + SURF)],
    ['Opened a guide', f7(P('G:G', '"opened_article"') + SURF),
                       fPrev(P('G:G', '"opened_article"') + SURF)],
    ['Escalated', f7(P('G:G', '"ticket_created"') + SURF),
                  fPrev(P('G:G', '"ticket_created"') + SURF)]
  ]);
  s.getRange(vRow, 3, 2, 2).setNumberFormat('0%');   // C:D on value+prev rows

  weeklyHead(s, top + 5, ['Week', 'Asked', 'Answer rate', 'Success', 'Solved',
                          "Didn't help", 'Unanswered', 'Escalated']);
  s.getRange('A' + w0).setFormula(weekCol());
  s.getRange('B' + w0).setFormula(fw(w0, w1, P('G:G', '"asked"') + SURF));
  // rate = answered asks / asks, per week; the inner COUNTIFS is written out in
  // full rather than derived from fw, for the same reason as the tiles
  s.getRange('C' + w0).setFormula(
    '=ARRAYFORMULA(IF(B' + w0 + ':B' + w1 + '=0,"",' +
    'COUNTIFS(' + LOG + '!A:A,">="&A' + w0 + ':A' + w1 +
    ',' + LOG + '!A:A,"<"&A' + w0 + ':A' + w1 + '+7' + GUARD +
    P('G:G', '"asked"') + P('E:E', 'TRUE') + SURF + ')/B' + w0 + ':B' + w1 + '))');
  s.getRange('D' + w0).setFormula(
    '=ARRAYFORMULA(IF(B' + w0 + ':B' + w1 + '=0,"",(' +
    'COUNTIFS(' + LOG + '!A:A,">="&A' + w0 + ':A' + w1 +
    ',' + LOG + '!A:A,"<"&A' + w0 + ':A' + w1 + '+7' + GUARD +
    P('G:G', '"asked"') + P('E:E', 'TRUE') + SURF + ')-' +
    'COUNTIFS(' + LOG + '!A:A,">="&A' + w0 + ':A' + w1 +
    ',' + LOG + '!A:A,"<"&A' + w0 + ':A' + w1 + '+7' + GUARD +
    P('G:G', '"unhelpful"') + SURF + '))/B' + w0 + ':B' + w1 + '))');
  s.getRange('E' + w0).setFormula(fw(w0, w1, P('G:G', '"solved"') + SURF));
  s.getRange('F' + w0).setFormula(fw(w0, w1, P('G:G', '"unhelpful"') + SURF));
  s.getRange('G' + w0).setFormula(fw(w0, w1, P('G:G', '"asked"') + P('E:E', 'FALSE') + SURF));
  s.getRange('H' + w0).setFormula(fw(w0, w1, P('G:G', '"ticket_created"') + SURF));
  s.getRange('A' + w0 + ':A' + w1).setNumberFormat('d mmm');
  s.getRange('C' + w0 + ':D' + w1).setNumberFormat('0%');
  s.getRange(top + 5, 1, WEEKS + 1, 8)
    .applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, true, false);

  sideList(s, top, 11, listK[0], listK[1]);
  sideList(s, top, 14, listN[0], listN[1]);
}

/* The support-deflection section. Different shape from the other two because the
   form's funnel is different: every intercepted submit logs exactly one of
   `asked` (a strong answer was shown) or `not_interrupted` (too weak or slow -
   the ticket went through untouched), and a shown answer then resolves to
   `solved` (deflected: no ticket) or `sent_anyway`. */
function deflectionSection(s, top) {
  var w0 = top + 6, w1 = w0 + WEEKS - 1;
  var SURF = surf('ticket-form');
  var vRow = top + 2;
  var checked = function (fn) {
    return '=' + fn(P('G:G', '"asked"') + SURF).slice(1) +
           '+' + fn(P('G:G', '"not_interrupted"') + SURF).slice(1);
  };

  banner(s, top, 'Support deflection (ticket form)', 'B' + w0 + ':B' + w1);
  tiles(s, top + 1, [
    ['Tickets checked', checked(f7), checked(fPrev)],
    ['Answer shown', f7(P('G:G', '"asked"') + P('E:E', 'TRUE') + SURF),
                     fPrev(P('G:G', '"asked"') + P('E:E', 'TRUE') + SURF)],
    // The prefetch-window watch metric from the other side: when this falls, the
    // answer is arriving too slowly or too weakly to be shown at all.
    ['Shown in time', '=IFERROR(IF(B' + vRow + '=0,"",C' + vRow + '/B' + vRow + '),"")',
                      '=IFERROR(IF(B' + (vRow + 1) + '=0,"",C' + (vRow + 1) + '/B' + (vRow + 1) + '),"")'],
    ['Not interrupted', f7(P('G:G', '"not_interrupted"') + SURF),
                        fPrev(P('G:G', '"not_interrupted"') + SURF)],
    ['Deflected', f7(P('G:G', '"solved"') + SURF),
                  fPrev(P('G:G', '"solved"') + SURF)],
    ['Sent anyway', f7(P('G:G', '"sent_anyway"') + SURF),
                    fPrev(P('G:G', '"sent_anyway"') + SURF)],
    ['Deflection rate', '=IFERROR(IF(B' + vRow + '=0,"",F' + vRow + '/B' + vRow + '),"")',
                        '=IFERROR(IF(B' + (vRow + 1) + '=0,"",F' + (vRow + 1) + '/B' + (vRow + 1) + '),"")']
  ]);
  s.getRange(vRow, 4, 2, 1).setNumberFormat('0%');   // Shown in time
  s.getRange(vRow, 8, 2, 1).setNumberFormat('0%');   // Deflection rate

  weeklyHead(s, top + 5, ['Week', 'Checked', 'Answer shown', 'Shown %',
                          'Not interrupted', 'Deflected', 'Sent anyway', 'Deflection %']);
  s.getRange('A' + w0).setFormula(weekCol());
  s.getRange('B' + w0).setFormula(
    '=ARRAYFORMULA(IF(A' + w0 + ':A' + w1 + '="","",' +
    'COUNTIFS(' + LOG + '!A:A,">="&A' + w0 + ':A' + w1 +
    ',' + LOG + '!A:A,"<"&A' + w0 + ':A' + w1 + '+7' + GUARD +
    P('G:G', '"asked"') + SURF + ')+' +
    'COUNTIFS(' + LOG + '!A:A,">="&A' + w0 + ':A' + w1 +
    ',' + LOG + '!A:A,"<"&A' + w0 + ':A' + w1 + '+7' + GUARD +
    P('G:G', '"not_interrupted"') + SURF + ')))');
  s.getRange('C' + w0).setFormula(fw(w0, w1, P('G:G', '"asked"') + P('E:E', 'TRUE') + SURF));
  s.getRange('D' + w0).setFormula(
    '=ARRAYFORMULA(IF(B' + w0 + ':B' + w1 + '=0,"",C' + w0 + ':C' + w1 + '/B' + w0 + ':B' + w1 + '))');
  s.getRange('E' + w0).setFormula(fw(w0, w1, P('G:G', '"not_interrupted"') + SURF));
  s.getRange('F' + w0).setFormula(fw(w0, w1, P('G:G', '"solved"') + SURF));
  s.getRange('G' + w0).setFormula(fw(w0, w1, P('G:G', '"sent_anyway"') + SURF));
  s.getRange('H' + w0).setFormula(
    '=ARRAYFORMULA(IF(B' + w0 + ':B' + w1 + '=0,"",F' + w0 + ':F' + w1 + '/B' + w0 + ':B' + w1 + '))');
  s.getRange('A' + w0 + ':A' + w1).setNumberFormat('d mmm');
  s.getRange('D' + w0 + ':D' + w1).setNumberFormat('0%');
  s.getRange('H' + w0 + ':H' + w1).setNumberFormat('0%');
  s.getRange(top + 5, 1, WEEKS + 1, 8)
    .applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, true, false);

  sideList(s, top, 11, 'Sent anyway — answer shown, ticket still sent (30 days)',
    topQ('D', 'G=\'sent_anyway\' and B=\'ticket-form\' and ' + NOT_TEST));
  sideList(s, top, 14, 'Too slow or weak to interrupt (30 days)',
    topQ('D', 'G=\'not_interrupted\' and B=\'ticket-form\' and ' + NOT_TEST));
}

/* ---- small layout helpers ---- */

/* Navy band with the section name; the cell to its right holds a cream sparkline
   of weekly volume so each section carries its own trend at a glance. */
function banner(s, row, title, sparkRange) {
  s.getRange(row, 1, 1, 8).merge().setValue(title)
    .setBackground(BRAND.navy).setFontColor(BRAND.cream)
    .setFontWeight('bold').setFontSize(11).setVerticalAlignment('middle');
  s.getRange(row, 9).setBackground(BRAND.navy);
  if (sparkRange) {
    s.getRange(row, 9).setFormula(
      '=IFERROR(SPARKLINE(TRANSPOSE(' + sparkRange + '),' +
      '{"charttype","column";"color","' + BRAND.cream + '"}),"")');
  }
  s.setRowHeight(row, 28);
}

/* labels / this-week / last-week rows, tiles starting at column B. */
function tiles(s, labelRow, defs) {
  s.getRange(labelRow + 1, 1).setValue('Last 7 days').setFontColor(BRAND.ink).setFontSize(9);
  s.getRange(labelRow + 2, 1).setValue('7 before').setFontColor(BRAND.faint).setFontSize(9);
  for (var i = 0; i < defs.length; i++) {
    s.getRange(labelRow, 2 + i).setValue(defs[i][0])
      .setFontSize(9).setFontColor(BRAND.ink).setFontWeight('bold');
    s.getRange(labelRow + 1, 2 + i).setFormula(defs[i][1]).setFontSize(16);
    s.getRange(labelRow + 2, 2 + i).setFormula(defs[i][2])
      .setFontSize(9).setFontColor(BRAND.faint);
  }
}

function weeklyHead(s, row, head) {
  s.getRange(row, 1, 1, head.length).setValues([head])
    .setFontWeight('bold').setFontSize(9).setFontColor(BRAND.ink);
}

function sideList(s, top, col, title, formula) {
  s.getRange(top, col).setValue(title).setFontWeight('bold').setFontSize(10);
  s.getRange(top + 1, col).setFormula(formula);
  s.getRange(top + 1, col, WEEKS + 5, 1).setWrap(true).setFontSize(9)
    .setVerticalAlignment('top');
}

/* Answer-rate and success-rate tiles. The denominator references the Asked tile
   in the same row rather than repeating its COUNTIFS, matching the original. */
function rate7(SURF, vRow) {
  return '=IFERROR(' + f7(P('G:G', '"asked"') + P('E:E', 'TRUE') + SURF).slice(1) +
         '/B' + vRow + ', "")';
}
function ratePrev(SURF, pRow) {
  return '=IFERROR(' + fPrev(P('G:G', '"asked"') + P('E:E', 'TRUE') + SURF).slice(1) +
         '/B' + pRow + ', "")';
}
function success7(SURF, vRow) {
  return '=IFERROR(MAX(0,' + f7(P('G:G', '"asked"') + P('E:E', 'TRUE') + SURF).slice(1) +
         '-' + f7(P('G:G', '"unhelpful"') + SURF).slice(1) + ')/B' + vRow + ', "")';
}
function successPrev(SURF, pRow) {
  return '=IFERROR(MAX(0,' + fPrev(P('G:G', '"asked"') + P('E:E', 'TRUE') + SURF).slice(1) +
         '-' + fPrev(P('G:G', '"unhelpful"') + SURF).slice(1) + ')/B' + pRow + ', "")';
}
function surfNone() { return ''; }

function colLetter(n) { return String.fromCharCode(64 + n); }

/* ============================ end dashboard ============================ */

/* ========================= what people ask =========================
 *
 * The dashboard answers "are we performing?". This tab answers a different and
 * arguably more valuable question: "what do people keep needing to ask?" - which
 * matters even when the answer was perfect. A question asked thirty times a month
 * and answered every time is not a help-centre success story; it is a signal that
 * something upstream in the product is confusing, and the help centre is quietly
 * absorbing the cost.
 *
 * Nothing new is logged for this. The question has always been stored verbatim in
 * Log!D. What was missing was a way to see that thirteen rows reading "how do i
 * assign a reviewer", "how do i assgn reviewers?" and "Assigning reviewers. How do
 * I assign reviewers to submissions?" are one topic.
 *
 * The grouping key is **the first article the router chose**, not the words typed.
 * That is the trick: the routing call has already done the semantic clustering, and
 * its answer is sitting unused in Log!F. Questions with no article - the ones we
 * failed - fall back to the lowercased question text and are marked "(no match)",
 * so total demand stays honest rather than quietly dropping the failures.
 *
 * WHAT THIS CANNOT DO. There is no session or visitor id in the log, by design
 * (api/log.js: "Never store who asked"). So "Asks" counts questions, not people -
 * one person retrying six times looks like six. "Days seen" is the honest
 * discriminator: thirty asks across eighteen days is real recurring demand; thirty
 * asks on one day is one frustrated person, or a test session. Read the two
 * together, never Asks alone.
 */

/* The topic expression, shared by both blocks so they can never drift apart.
   Written without backslashes on purpose: "\." in a JS string silently becomes "."
   and would turn the escape into a match-anything, so the .html suffix is removed
   with SUBSTITUTE rather than a regex. */
function topicExpr(a, q) {
  var fallback = '"(no match) "&LOWER(TRIM(' + q + '))';
  var pretty = 'SUBSTITUTE(SUBSTITUTE(REGEXREPLACE(TRIM(REGEXEXTRACT(' + a +
               '&"","^[^|]+")),"^.*/",""),".html",""),"-"," ")';
  return 'IF(TRIM(' + a + '&"")="",' + fallback + ',IFERROR(' + pretty + ',' + fallback + '))';
}

/* The window filter every block shares: inside the chosen period, one row per
   completed question, test traffic excluded. */
function askKeep(extra) {
  return '(ts<>"")*(ts>=TODAY()-win)*(' + LOG + '!G2:G="asked")' +
         '*ISERROR(SEARCH("safe to delete",' + LOG + '!D2:D))' +
         '*ISERROR(SEARCH("-internal",' + LOG + '!B2:B))' + (extra || '');
}

function buildAskTab(ss) {
  var s = ss.getSheetByName(ASK) || ss.insertSheet(ASK);

  // Kristy's chosen window survives a rebuild. setup() is safe to re-run, and a
  // re-run that silently reset her 90-day view back to 30 would be a small betrayal
  // of that promise.
  var win = 30;
  var existing = s.getRange('B4').getValue();
  if (existing && Number(existing) > 0) win = Number(existing);

  s.clear();
  s.getBandings().forEach(function (b) { b.remove(); });
  s.getRange(1, 1, 60, 8).clearDataValidations();

  s.getRange('A1').setValue('What people ask').setFontWeight('bold').setFontSize(14);
  s.getRange('A2').setValue(
    'Grouped by the article the answer came from, so every wording of the same question ' +
    'counts once. "Asks" counts questions, not people - there is no visitor id - so read ' +
    'it alongside "Days seen": 30 asks over 18 days is real demand, 30 in one afternoon is ' +
    'one person or a test.').setFontSize(9).setFontColor(BRAND.ink).setFontStyle('italic');
  s.getRange('A2:G2').merge().setWrap(true);
  s.setRowHeight(2, 30);

  s.getRange('A4').setValue('Show the last').setFontColor(BRAND.ink).setFontSize(10);
  s.getRange('B4').setValue(win).setFontWeight('bold')
    .setDataValidation(SpreadsheetApp.newDataValidation()
      .requireValueInList(['7', '30', '90', '365'], true).setAllowInvalid(true).build());
  s.getRange('C4').setValue('days').setFontColor(BRAND.ink).setFontSize(10);

  /* ---- block 1: topics across every surface ---- */
  var head = ['What they were asking about', 'Asks', 'Days seen', 'Answered',
              'Where from', 'Last asked', 'Worth a look?'];
  s.getRange(6, 1, 1, head.length).setValues([head])
    .setFontWeight('bold').setFontSize(9).setFontColor(BRAND.ink);

  s.getRange('A7').setFormula(
    '=IFERROR(LET(' +
    'win, IFERROR(IF(N($B$4)>0,N($B$4),30),30),' +
    'ts, ' + LOG + '!A2:A,' +
    'f, FILTER({ts,' + LOG + '!B2:B,' + LOG + '!D2:D,' + LOG + '!E2:E,' + LOG + '!F2:F}, ' +
      askKeep() + '),' +
    'topic, MAP(INDEX(f,,5),INDEX(f,,3),LAMBDA(a,q,' + topicExpr('a', 'q') + ')),' +
    'u, UNIQUE(topic),' +
    'asks, MAP(u,LAMBDA(t,SUM((topic=t)*1))),' +
    'days, MAP(u,LAMBDA(t,COUNTUNIQUE(FILTER(INT(INDEX(f,,1)),topic=t)))),' +
    'rate, MAP(u,LAMBDA(t,SUM((topic=t)*(INDEX(f,,4)=TRUE))/SUM((topic=t)*1))),' +
    'from, MAP(u,LAMBDA(t,TEXTJOIN(", ",1,UNIQUE(FILTER(INDEX(f,,2),topic=t))))),' +
    'seen, MAP(u,LAMBDA(t,MAX(FILTER(INDEX(f,,1),topic=t)))),' +
    'flag, MAP(asks,rate,LAMBDA(n,r,IF(AND(n>=' + UPSTREAM_MIN_ASKS + ',r>=' +
      UPSTREAM_MIN_RATE + '),"Look upstream",IF(r<0.5,"Needs content","")))),' +
    'ARRAY_CONSTRAIN(SORT({u,asks,days,rate,from,seen,flag},2,FALSE),' + TOP_TOPICS + ',7)' +
    '), "Nothing yet")');

  var last1 = 6 + TOP_TOPICS;
  s.getRange(7, 4, TOP_TOPICS, 1).setNumberFormat('0%');
  s.getRange(7, 6, TOP_TOPICS, 1).setNumberFormat('d mmm yyyy');
  s.getRange(6, 1, TOP_TOPICS + 1, 7)
    .applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, true, false);

  s.getRange(last1 + 1, 1).setValue(
    '"Look upstream" = asked ' + UPSTREAM_MIN_ASKS + '+ times and answered well. The help ' +
    'centre is coping; the question is why so many people arrive needing it. ' +
    '"Needs content" = we are answering it badly.')
    .setFontSize(9).setFontColor(BRAND.ink).setFontStyle('italic');
  s.getRange(last1 + 1, 1, 1, 7).merge().setWrap(true);

  /* ---- block 2: the widget's own signal, which no other surface has ---- *
   * The widget knows which admin screen the reader was on. Topic alone says what
   * to write; topic *and* screen says where in the product to fix it.          */
  var r2 = last1 + 3;
  s.getRange(r2, 1).setValue('In the app — what gets asked, and from which screen')
    .setFontWeight('bold').setFontSize(11);
  s.getRange(r2 + 1, 1, 1, 2).setValues([['Screen  —  what they asked about', 'Asks']])
    .setFontWeight('bold').setFontSize(9).setFontColor(BRAND.ink);
  s.getRange(r2 + 2, 1).setFormula(
    '=IFERROR(LET(' +
    'win, IFERROR(IF(N($B$4)>0,N($B$4),30),30),' +
    'ts, ' + LOG + '!A2:A,' +
    'f, FILTER({' + LOG + '!C2:C,' + LOG + '!D2:D,' + LOG + '!F2:F}, ' +
      askKeep('*(' + LOG + '!B2:B="widget")*(' + LOG + '!C2:C<>"")') + '),' +
    'k, INDEX(f,,1)&"  —  "&MAP(INDEX(f,,3),INDEX(f,,2),LAMBDA(a,q,' +
      topicExpr('a', 'q') + ')),' +
    'u, UNIQUE(k),' +
    'n, MAP(u,LAMBDA(t,SUM((k=t)*1))),' +
    'ARRAY_CONSTRAIN(SORT({u,n},2,FALSE),' + TOP_SCREENS + ',2)' +
    '), "Nothing yet")');
  s.getRange(r2 + 1, 1, TOP_SCREENS + 1, 2)
    .applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, true, false);

  s.setColumnWidth(1, 400);
  s.setColumnWidth(2, 60);
  s.setColumnWidth(3, 80);
  s.setColumnWidth(4, 80);
  s.setColumnWidth(5, 150);
  s.setColumnWidth(6, 110);
  s.setColumnWidth(7, 120);
  s.setFrozenRows(6);
  return s;
}

/* ---- durable history ----
 *
 * The tab above is a live view: it only ever knows what is still in the Log. This
 * appends a fixed monthly count per topic, so the trend survives however the raw
 * rows are eventually pruned, and so "is this getting better?" can be answered a
 * year from now.
 *
 * Run it from a monthly trigger: Apps Script → Triggers → Add trigger →
 * snapshotMonth → Time-driven → Month timer → 1st, early morning.
 *
 * Idempotent by design. It writes the *previous complete* month and returns early
 * if that month is already present, so a double-fired trigger or a curious manual
 * run cannot double-count.
 */
function snapshotMonth() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var hist = histSheet(ss);
  var now = new Date();
  var from = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  var to = new Date(now.getFullYear(), now.getMonth(), 1);
  var label = Utilities.formatDate(from, Session.getScriptTimeZone(), 'yyyy-MM');

  var seen = hist.getLastRow() > 1
    ? hist.getRange(2, 1, hist.getLastRow() - 1, 1).getValues().map(function (r) {
        return r[0] instanceof Date
          ? Utilities.formatDate(r[0], Session.getScriptTimeZone(), 'yyyy-MM')
          : String(r[0]);
      })
    : [];
  if (seen.indexOf(label) !== -1) return label + ' already recorded';

  var log = ss.getSheetByName(LOG);
  if (!log || log.getLastRow() < 2) return 'nothing to record';
  var rows = log.getRange(2, 1, log.getLastRow() - 1, 7).getValues();

  var acc = {};
  for (var i = 0; i < rows.length; i++) {
    var ts = rows[i][0], surface = rows[i][1], q = rows[i][3],
        answered = rows[i][4], articles = rows[i][5], event = rows[i][6];
    if (!(ts instanceof Date) || ts < from || ts >= to) continue;
    if (event !== 'asked') continue;
    if (String(q).toLowerCase().indexOf('safe to delete') !== -1) continue;
    var key = surface + ' ' + topicOf(articles, q);
    if (!acc[key]) acc[key] = { asks: 0, answered: 0, days: {} };
    acc[key].asks++;
    if (answered === true) acc[key].answered++;
    acc[key].days[ts.getFullYear() + '-' + ts.getMonth() + '-' + ts.getDate()] = 1;
  }

  var out = [];
  for (var k in acc) {
    var parts = k.split(' ');
    out.push([label, parts[0], parts[1], acc[k].asks,
              Object.keys(acc[k].days).length, acc[k].answered / acc[k].asks]);
  }
  if (!out.length) return 'nothing to record for ' + label;
  out.sort(function (a, b) { return b[3] - a[3]; });
  hist.getRange(hist.getLastRow() + 1, 1, out.length, 6).setValues(out);
  hist.getRange(2, 6, hist.getLastRow(), 1).setNumberFormat('0%');
  return 'recorded ' + out.length + ' topics for ' + label;
}

/* The same grouping rule as topicExpr, in JS. The two must agree, or the live tab
   and the history would tell different stories about the same month. */
function topicOf(articles, question) {
  var a = String(articles || '').split('|')[0].trim();
  if (!a) return '(no match) ' + String(question || '').toLowerCase().trim();
  return a.replace(/^.*\//, '').replace(/\.html$/, '').replace(/-/g, ' ');
}

function histSheet(ss) {
  var s = ss.getSheetByName(HIST);
  if (!s) {
    s = ss.insertSheet(HIST);
    s.appendRow(['Month', 'Surface', 'What they were asking about', 'Asks',
                 'Days seen', 'Answered']);
    s.getRange(1, 1, 1, 6).setFontWeight('bold');
    s.setFrozenRows(1);
    s.setColumnWidth(1, 90);
    s.setColumnWidth(2, 110);
    s.setColumnWidth(3, 400);
  }
  return s;
}

/* ======================= end what people ask ======================= */

function buildView(ss, name, head, formula) {
  var s = ss.getSheetByName(name) || ss.insertSheet(name);
  s.clear();
  s.appendRow(head);
  s.getRange(1, 1, 1, head.length).setFontWeight('bold');
  s.setFrozenRows(1);
  s.getRange('A2').setFormula(formula);
  s.getRange('A2:A').setNumberFormat('d mmm yyyy, HH:mm');
  s.setColumnWidth(head.indexOf('Question') + 1 || 4, 420);
}

/* The staff suggestions tab. Formatted by hand rather than through sheet(), because
   it is the one tab a person reads down rather than charts: the suggestion column is
   wide and wrapped, and Status is a dropdown so triage is a click.

   Validation is re-extended on every append rather than painted onto a huge range
   once. A fixed 1,000-row range silently stops applying at row 1,001, and the tab
   that loses its dropdown is the one nobody notices for a year. */
function suggestSheet(ss) {
  // Everything positional is looked up by header name. Inserting "Team" as column 3
  // silently shifted Status from J to K, and hand-numbered widths, wraps and the
  // validation range would each have had to be found and renumbered - one missed
  // and the dropdown lands on the wrong column.
  function col(header) { return HEAD_SUGGEST.indexOf(header) + 1; }

  var s = ss.getSheetByName(SUGGEST);
  if (!s) {
    s = ss.insertSheet(SUGGEST);
    s.appendRow(HEAD_SUGGEST);
    s.getRange(1, 1, 1, HEAD_SUGGEST.length).setFontWeight('bold');
    s.setFrozenRows(1);

    var widths = {
      'Timestamp': 155, 'Name': 130, 'Team': 160, 'Email': 210, 'Type': 190,
      'Suggestion': 520, 'Product area': 170, 'Article or page': 240,
      'Link': 240, 'Status': 130, 'Notes': 320
    };
    for (var h in widths) if (col(h)) s.setColumnWidth(col(h), widths[h]);

    s.getRange(2, col('Timestamp'), s.getMaxRows() - 1, 1)
      .setNumberFormat('d mmm yyyy, HH:mm');
    s.getRange(2, col('Suggestion'), s.getMaxRows() - 1, 1).setWrap(true);
    s.getRange(2, col('Notes'), s.getMaxRows() - 1, 1).setWrap(true);
  }
  var rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(STATUSES, true).setAllowInvalid(false).build();
  s.getRange(2, col('Status'), Math.max(s.getLastRow(), 1) + 50, 1)
    .setDataValidation(rule);
  return s;
}

/* Optional mail on arrival. Wrapped whole: the row is already saved by the time this
   runs, so a bounced address or a hit quota must not turn a stored suggestion into
   an error the sender sees. */
function notify(g) {
  if (!NOTIFY) return;
  try {
    MailApp.sendEmail({
      to: NOTIFY,
      subject: 'KB suggestion from ' + (g.name || 'a colleague') + ': ' + (g.type || ''),
      body: [
        (g.name || '') + (g.team ? ' (' + g.team + ')' : '') +
          (g.email ? ' <' + g.email + '>' : ''),
        'Type: ' + (g.type || '-'),
        'Product area: ' + (g.section || '-'),
        'Article or page: ' + (g.article || '-'),
        'Link: ' + (g.link || '-'),
        '',
        g.text || '',
        '',
        SpreadsheetApp.getActiveSpreadsheet().getUrl()
      ].join('\n')
    });
  } catch (err) {
    // The row is in the sheet; a missing email is a nuisance, not a loss.
  }
}

function sheet(ss, name, head) {
  var s = ss.getSheetByName(name);
  if (!s) {
    s = ss.insertSheet(name);
    s.appendRow(head);
    s.getRange(1, 1, 1, head.length).setFontWeight('bold');
    s.setFrozenRows(1);
    s.setColumnWidth(1, 155);
    var q = head.indexOf('Question');
    if (q >= 0) s.setColumnWidth(q + 1, 420);
    s.getRange('A2:A').setNumberFormat('d mmm yyyy, HH:mm');
  }
  return s;
}

function out(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
