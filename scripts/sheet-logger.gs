/**
 * Google Apps Script for the interaction log.
 *
 * SETUP (about five minutes, once)
 *  1. Create a Google Sheet called "OA help centre — interaction log".
 *  2. Extensions → Apps Script. Delete the placeholder, paste this file, Save.
 *  3. Edit TOKEN below to a long random string of your choosing.
 *  4. Run → setup  (once). It builds the three tabs and the weekly formulas, and
 *     Google will ask you to authorise the script.
 *  5. Deploy → New deployment → Web app.
 *       Execute as: Me.   Who has access: Anyone.
 *     ("Anyone" is what lets the Vercel function post; the TOKEN is the actual lock.)
 *  6. Copy the web app URL. In Vercel → Settings → Environment Variables add:
 *       SHEET_WEBHOOK_URL = <the web app URL>
 *       SHEET_TOKEN       = <the same string as TOKEN below>
 *     Redeploy. Nothing else needs to change.
 *
 * Rows arrive already stripped of emails and phone numbers by api/log.js.
 */

var TOKEN = 'change-me-to-something-long-and-random';

var ANSWERED   = 'Answered';
var UNANSWERED = 'Unanswered';
var SUMMARY    = 'Weekly summary';

var HEAD_ANSWERED   = ['Timestamp', 'Surface', 'Screen', 'Question', 'Articles shown', 'Outcome'];
var HEAD_UNANSWERED = ['Timestamp', 'Surface', 'Screen', 'Question', 'Outcome'];

function doPost(e) {
  try {
    var body = JSON.parse(e.postData.contents);
    if (body.token !== TOKEN) return out({ ok: false, error: 'bad token' });

    var r = body.row || {};
    var ts = r.ts ? new Date(r.ts) : new Date();
    var ss = SpreadsheetApp.getActiveSpreadsheet();

    if (r.answered) {
      sheet(ss, ANSWERED, HEAD_ANSWERED)
        .appendRow([ts, r.surface || '', r.screen || '', r.question || '',
                    r.sources || '', r.action || '']);
    } else {
      sheet(ss, UNANSWERED, HEAD_UNANSWERED)
        .appendRow([ts, r.surface || '', r.screen || '', r.question || '', r.action || '']);
    }
    return out({ ok: true });
  } catch (err) {
    return out({ ok: false, error: String(err) });
  }
}

/** Builds the tabs and the weekly summary. Safe to run more than once. */
function setup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  sheet(ss, ANSWERED, HEAD_ANSWERED);
  sheet(ss, UNANSWERED, HEAD_UNANSWERED);

  var s = ss.getSheetByName(SUMMARY) || ss.insertSheet(SUMMARY);
  s.clear();
  s.getRange('A1:E1')
    .setValues([['Week beginning', 'Answered', 'Unanswered', 'Total', 'Success rate']])
    .setFontWeight('bold');

  // Every week from the first logged row to today, counted from both tabs. Written as
  // formulas rather than computed here, so the numbers stay live as rows arrive.
  s.getRange('A2').setFormula(
    '=IFERROR(LET(' +
    'a, FILTER(' + ANSWERED + '!A2:A, ' + ANSWERED + '!A2:A<>""),' +
    'u, FILTER(' + UNANSWERED + '!A2:A, ' + UNANSWERED + '!A2:A<>""),' +
    'first, MIN(IFERROR(MIN(a),TODAY()), IFERROR(MIN(u),TODAY())),' +
    'start, INT(first) - WEEKDAY(INT(first), 3),' +
    'SEQUENCE(MAX(1, ROUNDUP((TODAY()-start+1)/7)), 1, start, 7)), "")');

  s.getRange('B2').setFormula(
    '=ARRAYFORMULA(IF(A2:A="","",COUNTIFS(' + ANSWERED + '!A:A,">="&A2:A,' +
    ANSWERED + '!A:A,"<"&A2:A+7)))');
  s.getRange('C2').setFormula(
    '=ARRAYFORMULA(IF(A2:A="","",COUNTIFS(' + UNANSWERED + '!A:A,">="&A2:A,' +
    UNANSWERED + '!A:A,"<"&A2:A+7)))');
  s.getRange('D2').setFormula('=ARRAYFORMULA(IF(A2:A="","",B2:B+C2:C))');
  s.getRange('E2').setFormula('=ARRAYFORMULA(IF(A2:A="","",IF(D2:D=0,"",B2:B/D2:D)))');

  s.getRange('A2:A').setNumberFormat('d mmm yyyy');
  s.getRange('E2:E').setNumberFormat('0%');
  s.setColumnWidth(1, 130);
  s.setFrozenRows(1);
}

function sheet(ss, name, head) {
  var s = ss.getSheetByName(name);
  if (!s) {
    s = ss.insertSheet(name);
    s.appendRow(head);
    s.getRange(1, 1, 1, head.length).setFontWeight('bold');
    s.setFrozenRows(1);
    s.setColumnWidth(1, 155);                     // timestamp
    s.setColumnWidth(head.indexOf('Question') + 1, 420);
    s.getRange('A2:A').setNumberFormat('d mmm yyyy, HH:mm');
  }
  return s;
}

function out(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
