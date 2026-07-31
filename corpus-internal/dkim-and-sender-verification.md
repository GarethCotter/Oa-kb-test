---
title: "DKIM added but the sender still shows unverified — domain and address are two steps"
internal: true
last_reviewed: 2026-07-31
---

DKIM not verifying, added the DKIM record but still unverified, return path not
verified, sender address unverified, verify sender, sending from our own domain,
CNAME and TXT added, DNS records added but nothing changed.

Distilled from support replies in the year to July 2026. The pattern is always the
same: the records are correct and the screen still says unverified.

**Two things verify separately, and both must pass.**

- **The domain** — the DKIM record, and the **return path**, which is a separate
  record people routinely miss. A domain can show DKIM verified and return path not.
- **Each individual sending address** on that domain. Verifying the domain does not
  verify the addresses. Each one gets an email with a link that has to be clicked.

**When an address stays stubbornly unverified**, removing it and adding it again
triggers a fresh confirmation email — that clears most of these.

**DNS propagation is not instant.** Records added within the last day may simply not
have propagated yet, so a re-check tomorrow is a legitimate answer rather than a
brush-off.

**Support can verify manually from their end** once the records are genuinely in
place, and frequently does. If the organiser is confident the DNS is right and the
screen disagrees, that is the escalation — not more DNS edits.
