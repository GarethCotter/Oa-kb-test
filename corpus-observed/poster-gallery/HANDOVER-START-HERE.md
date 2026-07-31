# Poster gallery run — start here

Everything a fresh session needs to run the poster gallery exploration. Step 1 of the
brief (read the articles, build a verification list) is **already done** — it is in
`META.md` in this folder. Start at step 2, the novice walk.

---

## Access

- **Demo event: 78206**, Professional Conference package. Gareth is signed in as admin
  in Chrome and the dashboard is at
  `https://app.oxfordabstracts.com/admin/events/78206/app/dashboard`
- **Use the Chrome tools** (`mcp__claude-in-chrome__*`), not the in-app Browser pane.
  The session lives in Gareth's Chrome. Load them in ONE ToolSearch call:
  `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__find,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__form_input`
  then `tabs_context_mcp{createIfEmpty:true}`.
- **If the tab lands on the sign-in page, stop and ask Gareth to sign in.** You must not
  type a password into a login form. This happened once already: the extension opens its
  own tab and it did not inherit the session.
- **Screenshots work in Chrome** (`computer` with `action:"screenshot"`). They do *not*
  work in the in-app Browser pane, which never composites frames when hidden — do not
  waste time trying.

## Ground rules that bite on this feature

- Event 78206 is a demo event and Gareth has agreed it can be altered. Even so, use
  obviously synthetic content — "Test Poster One", "An Abstract About Nothing". Never
  real names or research text, even as filler.
- **Nothing you write goes in `corpus/` or `corpus-internal/`.** Write only to
  `corpus-observed/poster-gallery/`. `build.py` reads the other two directories, so
  anything you put there reaches live answers — which is exactly what this process is
  designed to prevent. A human promotes findings later.
- Keep observation and inference apart. Tag `[inferred]` or `[untested]` and say why.
- Quote every label and error message verbatim, in quotes. A paraphrased error is
  useless for search matching.

## What is already done

- `META.md` — assignment block, what limits the run, and the **verification list: 25
  checkable claims** taken from the existing articles, plus 5 open questions the support
  tickets raise. Mark each confirmed / changed / could-not-verify as you go.
- `corpus-observed/README.md` — why this directory exists and why it is isolated.

## Suggested order for the walk

1. **Submission form question.** Event dashboard → Abstract Management → Submissions →
   Form & Setup → +QUESTION. Find the poster upload question type. Record the exact
   heading it sits under, every checkbox at the bottom of the question, and the button
   labels. Claims 5–11 on the verification list.
2. **Break it deliberately.** A multi-page PDF, a non-PDF file, a very large file, an
   empty upload. Capture every error message verbatim — the articles have none of these,
   and 85 tickets a year are file-upload failures.
3. **Decisions table.** Does the "In poster gallery" column exist before a poster
   question is created? (Support replies say no — claim 17 and open question Q1.)
   Accept a submission, tick it, check bulk selection.
4. **The gallery itself.** Where the menu item is switched on (Q3), whether the gallery
   URL works before the programme is published (Q2), and what a delegate sees.
5. **Reconcile** against the verification list, then write the dossier files, then
   `article-gaps.md` last.

## What this feature is worth

292 of 4,898 support tickets in the year to July 2026 mention the poster gallery. "How
do I set it up" is 59 of 147 question sentences in those tickets — three times the next
theme. The consistent confusion is that people do not connect the gallery to a question
on the submission form. The next themes are file format and size (19), audio/video
posters (15), cost and package (10), and who can view it and for how long (9).

Ten of the eleven screenshots in the main article date from 2021–2022, so expect visual
drift and capture replacements as you go.

## Context worth reading first

- `project/feature-exploration-brief.md` — the standing brief this run follows
- `CLAUDE.md` — house conventions; note the British English rule and the warning that
  `build.py` refuses to build if a public corpus file sits outside a section folder
- `project/ticket-analysis.md` — ticket themes by volume
- `project/context-from-conversation.md` §4 — why this agent exists and why it points at
  finding gaps rather than answering customers
