---
title: "Links cannot be set to open in a new tab"
internal: true
last_reviewed: 2026-08-11
---

Open in a new tab, open link in new window, make a link open separately, target blank,
link in an email opens in the same tab, link in the submission form navigates away,
can I add something to the URL to open a new tab.

**No, and there is nothing to add to the URL that would do it.** Confirmed with Gareth,
11 August 2026.

Two separate reasons, and the first one is worth explaining because people go looking
for a setting that cannot exist:

- **A URL cannot control where it opens.** It is only an address. What opens a link in a
  new tab is an attribute on the link itself — `target="_blank"` in the HTML — not any
  part of the web address. So no query string, parameter or suffix will ever do it, and
  somebody hunting for one will hunt forever.
- **Oxford Abstracts does not let you edit the link HTML.** The rich text editors — form
  question descriptions, the form header and footer, email templates — insert links for
  you and do not expose that attribute. So the option is not hidden somewhere; it is not
  offered.

**One more thing to head off, because it is the usual follow-up:** even where
`target="_blank"` is available on other platforms, it cannot choose a *tab* over a
*window*. It asks the browser for a new browsing context, and whether that appears as a
tab or a window is the reader's own browser setting. Nobody on our side can decide that.

**What to tell them instead.** Readers can open any link in a new tab themselves —
middle-click, or Ctrl+click on Windows, Cmd+click on a Mac. If the worry is a submitter
losing a part-completed form by clicking away, the reassurance is that answers save as
they move between fields and the submission stays available as incomplete — see
[[example-autosave]]. Clicking a link and coming back does not lose their work.
