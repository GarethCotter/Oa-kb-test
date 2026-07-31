# DRAFT — not for `corpus/` until reviewed

**Proposed path:** `corpus/08-conference-platform/why-your-poster-gallery-is-empty.md`

Drafted 31 July 2026 from the observed run in
`corpus-observed/poster-gallery/`. A human promotes this; it is deliberately
sitting in `project/` so `build.py` cannot pick it up (see `CLAUDE.md` gotcha 9).

**Before promoting, check:**

- Cause 5 ("Show submission contents") is quoted from the product's own help
  text, **not** observed by experiment — I did not change the demo event's
  access settings. Either verify it or soften the wording.
- If the inline-viewer failure recorded in `corpus-observed/poster-gallery/errors.md`
  reproduces on a real customer event, this article needs a seventh cause:
  "the posters are listed but each one shows a spinner".
- Screenshots: none captured this run. The two worth adding are the empty
  gallery state and the decisions table with the "In poster gallery" column.
  House rule is two or three per article, at decision points only.

---

```yaml
---
title: Why your poster gallery is empty
section: 08-conference-platform
audience: organisers
plan: professional conference
source_url:
last_reviewed: 2026-07-31
---
```

*`source_url` is blank because this is a new article, not a migrated one. Confirm
that `build.py` and the redirect check tolerate an empty `source_url` before
promoting — every existing article has one.*

---

# Why your poster gallery is empty

The guidance below is for event organisers.

You have set up a poster question, your submitters have uploaded their posters,
and the poster gallery still shows **"Sorry, we couldn't find any posters"**.

The gallery offers you a **Clear filters** button, but a filter is almost never
the reason. A poster only appears when several separate things are all true, and
the gallery cannot tell you which one is missing. Work down this list in order —
the first two causes account for most cases.

## 1. The submissions are accepted as well as ticked

This is the most common cause by a distance.

Ticking **In poster gallery** in the decisions table is not enough on its own.
The submission must **also** have a decision of **Accepted**. A submission that
is still **Pending** will not appear, however many boxes you tick.

Go to **Event dashboard → Abstract Management → Decisions → Table** and check
the **Decision** column for the posters you expect to see.

Note: **Accepted: Poster** is a decision type, not a gallery setting. Choosing it
does not add anything to the poster gallery. You still need the **In poster
gallery** box ticked.

## 2. No question on your submission form is marked as the poster gallery upload

The poster gallery is created by a single question on your submission form. If
no question has the **Poster gallery upload (1 allowed per event)** box ticked,
there is no gallery to fill — and the **In poster gallery** column will not
appear in your decisions table at all.

If you cannot find that column, this is why.

Go to **Event dashboard → Abstract Management → Submissions → Form & setup** and
look for your poster question. Open it and check that **Poster gallery upload
(1 allowed per event)** is ticked.

If there is no poster question at all, click **+ QUESTION** and choose
**Poster upload** under **Poster questions**.

Remember: **Event dashboard → Abstract Management → Submissions → Form & setup**
is the submission form. **Decisions** has a **Form & setup** page too, and it is
a different form.

## 3. Your submitters have not uploaded anything

A submission with no file attached to the poster question will not appear, even
if it is accepted and ticked.

In the decisions table, click **COLUMNS**, type `poster` in the search box, and
tick **Poster** under **Submission responses**. That column shows you who has
actually uploaded a file.

## 4. The Poster gallery menu item has been switched off

Go to **Event dashboard → Conference → Program → Builder → DISPLAY → Program
menu** and check that **Poster gallery** is ticked.

The name in that box is editable, so if someone has renamed it, the menu item in
your programme will show the new name.

## 5. Submission contents are hidden from the programme

Go to **Event dashboard → Conference → Program → Builder → DISPLAY**, or the
**User access** button on the Conference card of your dashboard, and check that
**Show submission contents** is ticked.

Please note: unticking that box hides all submission data from your programme,
including the whole poster gallery. It is ticked by default, so this only
applies if someone has changed it.

## 6. A filter is still applied

If you have typed something into **Search posters**, or ticked anything in the
**Topics** or **Keywords** dropdowns, the gallery is showing you a filtered view.
Click **Clear filters** to see everything.

One thing worth knowing about that search box: it searches poster **titles** and
**author affiliations**. It does not search abstracts or poster keywords. To
find posters by keyword, use the **Keywords** dropdown instead.

## Still empty?

If you have worked through all six and your gallery is still empty, contact
support with your event ID and the ID of one submission you expect to see. That
is enough for us to check it directly.

---

## Where this should be linked from

- `corpus/08-conference-platform/professional-conference-the-poster-gallery.md`
  — a link near the end of the setup steps.
- The section page for `08-conference-platform` — this is a troubleshooting
  article, so it belongs in the same group as the setup article rather than as
  the "Start here" card.
- Consider adding **poster gallery empty** to the `SYNONYMS` map in
  `assets/search.js` only if the search analytics later show it failing. The
  existing evidence is that "poster gallery" already works as a search term
  (1.0 average result clicks), so this is a content gap, not a naming one, and
  a synonym would not have helped.
