/**
 * Google Apps Script for the master help-performance sheet.
 *
 * One event log, every surface. The KB search, the in-app help widget and the
 * support form all POST the same seven-column row via api/log.js; article-page
 * feedback arrives via api/feedback.js. Everything on the Dashboard is a formula
 * over the Log tab, so the script only ever appends - nothing is computed here.
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
 * Event vocabulary (the Log tab's last column):
 *   asked            a question completed; the Answered column says whether an
 *                    answer was shown. One per question, every surface.
 *   solved           reader clicked "This solved it"
 *   unhelpful        reader clicked "This didn't help me"
 *   ticket_created   reader clicked through to the support form
 *   sent_anyway      support form: answer shown, ticket sent regardless
 *   not_interrupted  support form: answer too weak to interrupt with
 *   opened_article   reader opened a suggested guide
 *
 * Rows arrive already stripped of emails and phone numbers by api/log.js.
 */

var TOKEN = 'change-me-to-something-long-and-random';

var LOG       = 'Log';
var FEEDBACK  = 'Article feedback';
var DASH      = 'Dashboard';
var V_UNHELP  = "Didn't help";
var V_UNANS   = 'Unanswered';

var HEAD_LOG      = ['Timestamp', 'Surface', 'Screen', 'Question', 'Answered',
                     'Articles shown', 'Event'];
var HEAD_FEEDBACK = ['Timestamp', 'Article', 'Helpful', 'Reason'];

function doPost(e) {
  try {
    var body = JSON.parse(e.postData.contents);
    if (body.token !== TOKEN) return out({ ok: false, error: 'bad token' });
    var ss = SpreadsheetApp.getActiveSpreadsheet();

    if (body.row) {
      var r = body.row;
      sheet(ss, LOG, HEAD_LOG).appendRow([
        r.ts ? new Date(r.ts) : new Date(),
        r.surface || '', r.screen || '', r.question || '',
        r.answered === true, r.sources || '', r.action || ''
      ]);
    }
    if (body.feedback) {
      var f = body.feedback;
      sheet(ss, FEEDBACK, HEAD_FEEDBACK).appendRow([
        f.ts ? new Date(f.ts) : new Date(),
        f.path || '', f.helpful === true, f.reason || ''
      ]);
    }
    return out({ ok: true });
  } catch (err) {
    return out({ ok: false, error: String(err) });
  }
}

/** Builds every tab, the dashboard and the live views. Safe to run more than once. */
function setup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  sheet(ss, LOG, HEAD_LOG);
  sheet(ss, FEEDBACK, HEAD_FEEDBACK);
  buildView(ss, V_UNHELP,
    ['Timestamp', 'Surface', 'Screen', 'Question', 'Articles shown'],
    '=IFERROR(QUERY(' + LOG + '!A2:G, "select A,B,C,D,F where G=\'unhelpful\' ' +
    'order by A desc", 0), "")');
  buildView(ss, V_UNANS,
    ['Timestamp', 'Surface', 'Screen', 'Question'],
    '=IFERROR(QUERY(' + LOG + '!A2:G, "select A,B,C,D where G=\'asked\' and E=false ' +
    'order by A desc", 0), "")');
  buildDashboard(ss);
}

function buildDashboard(ss) {
  var s = ss.getSheetByName(DASH) || ss.insertSheet(DASH, 0);
  s.clear();

  s.getRange('A1').setValue('Help performance — all surfaces').setFontWeight('bold')
    .setFontSize(14);

  // ---- headline tiles: last 7 days (row 4) and the 7 before (row 5) ----
  // c7/cPrev produce plain COUNTIFS strings so every tile is an explicit formula -
  // an earlier draft derived row 5 from row 4 with regex surgery and broke the
  // Answer rate tile, whose formula does not end where the regex assumed.
  var tiles = [
    ['Questions asked', c7('G:G,"asked"'),
                        cPrev('G:G,"asked"')],
    ['Answer rate',     '=IFERROR(' + c7('G:G,"asked",' + LOG + '!E:E,TRUE').slice(1) + '/B4, "")',
                        '=IFERROR(' + cPrev('G:G,"asked",' + LOG + '!E:E,TRUE').slice(1) + '/B5, "")'],
    ['Solved',          c7('G:G,"solved"'),
                        cPrev('G:G,"solved"')],
    ["Didn't help",     c7('G:G,"unhelpful"'),
                        cPrev('G:G,"unhelpful"')],
    ['Unanswered',      c7('G:G,"asked",' + LOG + '!E:E,FALSE'),
                        cPrev('G:G,"asked",' + LOG + '!E:E,FALSE')],
    ['Tickets created', c7('G:G,"ticket_created"'),
                        cPrev('G:G,"ticket_created"')]
  ];
  for (var i = 0; i < tiles.length; i++) {
    var col = String.fromCharCode(66 + i);                       // B..G
    s.getRange(col + '3').setValue(tiles[i][0]).setFontWeight('bold');
    s.getRange(col + '4').setFormula(tiles[i][1]).setFontSize(16);
    s.getRange(col + '5').setFormula(tiles[i][2]).setFontColor('#888880');
  }
  s.getRange('A4').setValue('Last 7 days').setFontColor('#5F5E5A');
  s.getRange('A5').setValue('7 before').setFontColor('#888880');
  s.getRange('C4:C5').setNumberFormat('0%');

  // ---- by week ----
  s.getRange('A8').setValue('By week').setFontWeight('bold');
  var head = ['Week', 'Asked', 'Answer rate', 'KB', 'Widget', 'Form', 'Solved',
              "Didn't help", 'Tickets', 'Form deflected', 'Sent anyway'];
  s.getRange(9, 1, 1, head.length).setValues([head]).setFontWeight('bold');

  s.getRange('A10').setFormula(
    '=IFERROR(LET(t, FILTER(' + LOG + '!A2:A, ' + LOG + '!A2:A<>""), ' +
    'first, MIN(t), start, INT(first) - WEEKDAY(INT(first), 3), ' +
    'SEQUENCE(MAX(1, ROUNDUP((TODAY()-start+1)/7)), 1, start, 7)), "")');
  var wk = [
    wcount('G:G,"asked"'),
    // rate = answered asks / asks, per week; the inner COUNTIFS is written out in
    // full rather than derived from wcount, for the same reason as the tiles
    '=ARRAYFORMULA(IF(A10:A="","",IF(B10:B=0,"",' +
      'COUNTIFS(' + LOG + '!A:A,">="&A10:A,' + LOG + '!A:A,"<"&A10:A+7,' +
      LOG + '!G:G,"asked",' + LOG + '!E:E,TRUE)/B10:B)))',
    wcount('G:G,"asked",' + LOG + '!B:B,"kb-search"'),
    wcount('G:G,"asked",' + LOG + '!B:B,"widget"'),
    wcount('G:G,"asked",' + LOG + '!B:B,"ticket-form"'),
    wcount('G:G,"solved"'),
    wcount('G:G,"unhelpful"'),
    wcount('G:G,"ticket_created"'),
    wcount('G:G,"solved",' + LOG + '!B:B,"ticket-form"'),
    wcount('G:G,"sent_anyway"')
  ];
  for (var j = 0; j < wk.length; j++)
    s.getRange(10, 2 + j).setFormula(wk[j]);
  s.getRange('A10:A').setNumberFormat('d mmm yyyy');
  s.getRange('C10:C').setNumberFormat('0%');

  // ---- what to write next / what to fix ----
  s.getRange('M3').setValue('Top unanswered, last 30 days').setFontWeight('bold');
  s.getRange('M4').setFormula(
    '=IFERROR(QUERY(' + LOG + '!A2:G, "select D, count(A) where G=\'asked\' and ' +
    'E=false and A >= date \'"&TEXT(TODAY()-30,"yyyy-mm-dd")&"\' group by D ' +
    'order by count(A) desc limit 10 label D \'Question\', count(A) \'Times\'", 0),' +
    ' "Nothing yet")');

  s.getRange('M17').setValue('Articles voted No, last 30 days').setFontWeight('bold');
  s.getRange('M18').setFormula(
    '=IFERROR(QUERY(\'' + FEEDBACK + '\'!A2:D, "select B, count(A) where C=false ' +
    'and A >= date \'"&TEXT(TODAY()-30,"yyyy-mm-dd")&"\' group by B ' +
    'order by count(A) desc limit 10 label B \'Article\', count(A) \'No votes\'", 0),' +
    ' "Nothing yet")');

  s.setColumnWidth(1, 110);
  s.setColumnWidth(13, 340);
  s.setFrozenRows(1);
}

/* COUNTIFS over the last 7 days, plus any extra criteria pairs. */
function c7(extra) {
  return '=COUNTIFS(' + LOG + '!A:A,">="&TODAY()-7,' + LOG + '!' + extra + ')';
}

/* The 7 days before that, for the comparison row. */
function cPrev(extra) {
  return '=COUNTIFS(' + LOG + '!A:A,">="&TODAY()-14,' + LOG + '!A:A,"<"&TODAY()-7,' +
         LOG + '!' + extra + ')';
}

/* Per-week ARRAYFORMULA COUNTIFS against the Week column. */
function wcount(extra) {
  return '=ARRAYFORMULA(IF(A10:A="","",COUNTIFS(' + LOG + '!A:A,">="&A10:A,' +
         LOG + '!A:A,"<"&A10:A+7,' + LOG + '!' + extra + ')))';
}

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
