# Pull the support reply for each row in project/ticket-gaps.csv.
#
# Output goes to a folder OUTSIDE the git repo. The repo is public and these replies
# contain real academics' names and email addresses, so raw material never goes near
# it - only distilled notes and article drafts get committed later.
#
# Read-only throughout: search tickets, read associations, read emails.

$ErrorActionPreference = 'Stop'
$t = [Environment]::GetEnvironmentVariable('HUBSPOT_TOKEN','User')
if (-not $t) { throw 'HUBSPOT_TOKEN not set' }
$H = @{ Authorization = "Bearer $t" }

$REPO = 'C:\Users\Gareth\Desktop\Claude\Oa-kb-test'
$OUT  = 'C:\Users\Gareth\Desktop\Claude\oa-support-replies'   # sibling of the repo, not inside it
New-Item -ItemType Directory -Force -Path $OUT | Out-Null

function Call-HS($method, $url, $body) {
  for ($try = 0; $try -lt 4; $try++) {
    try {
      if ($body) { return Invoke-RestMethod -Uri $url -Method $method -Headers $H -ContentType 'application/json' -Body $body -ErrorAction Stop }
      else       { return Invoke-RestMethod -Uri $url -Method $method -Headers $H -ErrorAction Stop }
    } catch {
      $code = if ($_.Exception.Response) { $_.Exception.Response.StatusCode.value__ } else { 0 }
      if ($code -eq 429) { Start-Sleep -Seconds (2 * ($try + 1)); continue }   # rate limited
      return $null
    }
  }
  return $null
}

# Cut the quoted original off a reply, and strip contact details. Names are left as
# they are - they cannot be detected reliably - which is exactly why this output
# stays out of the repo.
function Clean-Reply($s) {
  if (-not $s) { return '' }
  $s = $s -replace '(?s)\r?\n\s*On .{0,120}?wrote:.*$', ''      # On <date>, <name> wrote:
  $s = $s -replace '(?s)-{2,}\s*Original Message\s*-{2,}.*$', ''
  $s = $s -replace '(?s)\r?\nFrom:.*?\r?\nSent:.*$', ''
  $s = ($s -split "\r?\n" | Where-Object { $_ -notmatch '^\s*>' }) -join "`n"
  $s = $s -replace '[\w.+-]+@[\w-]+\.[\w.-]+', '[email]'
  $s = $s -replace '\+?\d[\d\s().-]{9,}\d', '[number]'
  $s = $s -replace '<[^>]+>', ' '
  $s = $s -replace '&nbsp;', ' '
  $s = $s -replace '[ \t]+', ' '
  $s = $s -replace '(\r?\n){3,}', "`n`n"
  return $s.Trim()
}

$rows = Import-Csv (Join-Path $REPO 'project\ticket-gaps.csv')
$total = $rows.Count
$results = New-Object System.Collections.ArrayList
$i = 0; $matched = 0; $withReply = 0

foreach ($r in $rows) {
  $i++
  if ($i % 25 -eq 0) { Write-Output ("... {0}/{1}  matched {2}  with reply {3}" -f $i, $total, $matched, $withReply) }

  $d = [datetime]::Parse($r.date)
  $from = [DateTimeOffset]::new($d.AddDays(-2)).ToUnixTimeMilliseconds()
  $to   = [DateTimeOffset]::new($d.AddDays(3)).ToUnixTimeMilliseconds()

  $body = @{
    filterGroups = @(@{ filters = @(
      @{ propertyName='subject';    operator='EQ';  value=$r.subject },
      @{ propertyName='createdate'; operator='GTE'; value="$from" },
      @{ propertyName='createdate'; operator='LTE'; value="$to" }) })
    properties = @('subject','createdate','content')
    limit = 3
  } | ConvertTo-Json -Depth 8
  $s = Call-HS 'POST' 'https://api.hubapi.com/crm/v3/objects/tickets/search' $body
  Start-Sleep -Milliseconds 130

  if (-not $s -or $s.total -eq 0) {
    # fall back to subject alone, then pick whichever is closest to the CSV date
    $body2 = @{ filterGroups = @(@{ filters = @(@{ propertyName='subject'; operator='EQ'; value=$r.subject }) })
                properties = @('subject','createdate','content'); limit = 10 } | ConvertTo-Json -Depth 8
    $s = Call-HS 'POST' 'https://api.hubapi.com/crm/v3/objects/tickets/search' $body2
    Start-Sleep -Milliseconds 130
  }
  if (-not $s -or -not $s.results -or $s.results.Count -eq 0) { continue }

  $best = $s.results | Sort-Object { [Math]::Abs(([datetime]$_.properties.createdate - $d).TotalDays) } | Select-Object -First 1
  $matched++
  $id = $best.id

  $a = Call-HS 'GET' ("https://api.hubapi.com/crm/v4/objects/tickets/{0}/associations/emails?limit=20" -f $id) $null
  Start-Sleep -Milliseconds 130
  if (-not $a -or -not $a.results) { continue }

  $replies = @()
  foreach ($eid in ($a.results | ForEach-Object { $_.toObjectId })) {
    $props = 'hs_email_direction,hs_email_text,hs_timestamp'
    $e = Call-HS 'GET' ("https://api.hubapi.com/crm/v3/objects/emails/{0}?properties={1}" -f $eid, $props) $null
    Start-Sleep -Milliseconds 130
    if (-not $e) { continue }
    if ($e.properties.hs_email_direction -ne 'EMAIL') { continue }   # outgoing = our reply
    $clean = Clean-Reply $e.properties.hs_email_text
    if ($clean.Length -ge 40) { $replies += [pscustomobject]@{ at = $e.properties.hs_timestamp; text = $clean } }
  }
  if ($replies.Count -eq 0) { continue }
  $withReply++

  [void]$results.Add([pscustomobject]@{
    theme    = $r.'gap theme'
    date     = $r.date
    subject  = $r.subject
    question = $r.'ticket text (truncated, personal data removed)'
    ticketId = $id
    replies  = @($replies | Sort-Object at | ForEach-Object { $_.text })
  })
}

$results | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $OUT 'replies.json') -Encoding UTF8

# readable digest, grouped by theme
$md = New-Object System.Collections.ArrayList
[void]$md.Add("# Support replies for the gap tickets`n")
[void]$md.Add("Pulled $(Get-Date -Format 'd MMM yyyy') from HubSpot, read-only. $withReply of $total rows have a reply.`n")
[void]$md.Add("**Not for the repo** - contains real names.`n")
foreach ($g in ($results | Group-Object theme | Sort-Object Count -Descending)) {
  [void]$md.Add("`n---`n`n## $($g.Name)  ($($g.Count) with replies)`n")
  foreach ($x in $g.Group) {
    [void]$md.Add("### $($x.subject)  _$($x.date)_")
    [void]$md.Add("**Asked:** $($x.question)`n")
    foreach ($rep in $x.replies) { [void]$md.Add("**Replied:** $rep`n") }
  }
}
$md -join "`n" | Set-Content (Join-Path $OUT 'replies.md') -Encoding UTF8

Write-Output ''
Write-Output ("DONE  rows {0}  matched {1}  with reply {2}" -f $total, $matched, $withReply)
Write-Output ("written to {0}" -f $OUT)
