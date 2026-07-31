---
title: "Network failure, page will not load, failed to fetch — usually the network, not us"
internal: true
last_reviewed: 2026-07-31
---

Network failure, failed to fetch, page cannot be displayed, dashboard will not load,
checkbox will not tick, error parsing response, cannot open the review link, spinner
never stops, works on my phone but not the office computer.

Distilled from around 30 support tickets in the year to July 2026 — the most common
"it is broken" report, and usually not a fault in the software.

**Work down this list before escalating. It resolves most of them:**

1. **An incognito or private window.** A cached session or a second signed-in account
   is the commonest single cause, and this rules it out in seconds.
2. **A different network — mobile data is the quickest test.** University and hospital
   firewalls block Oxford Abstracts often enough that "Network Failure" on the
   submission or sign-up page should be read as a network block until proved
   otherwise. The fix on their side is asking IT to allow the domain.
3. **Chrome on a desktop**, rather than an unusual or very old browser.
4. **Clear the cache**, or try another device.

**Go direct rather than through the dashboard.** A reviewer who cannot get past the
dashboard can often open their review form straight from the stage review URL, and a
submitter can reach a form from its stage submitter URL. If a link in a notification
email will not open, the dashboard always holds their submissions and feedback.

**What to gather if none of that works:** the exact error text, the URL they were on,
the email address they signed in with, and whether it happens on another network. An
error quoting an internal `/purs-api/...` path is a genuine application error worth
passing on — the rest of the list above is not.
