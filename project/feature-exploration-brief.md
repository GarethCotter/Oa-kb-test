# Feature exploration brief

*The standing instructions for an agent session whose job is to learn one Oxford
Abstracts feature inside out by using it. Copy this whole file into the session, fill in
the assignment block, and let it run.*

---

## Assignment

- **Feature:** <e.g. "the submission form builder">
- **Plans to explore under:** <e.g. Basic (free), Abstract Management, Professional>
- **Test account(s):** <credentials reference — never a live customer account>
- **App version / date:** <fill in at the start of the run>
- **Existing articles covering this feature:** <paths in corpus/>

---

## Your job

Become the resident expert on this one feature — by using it, not by reading about it.
The written articles say what the feature is *supposed* to do. Your job is to record what
it *actually* does: the exact labels, the limits, the error states, the differences
between plans, and the places a first-time user would get stuck.

You are producing two things:

1. **A feature dossier** — structured notes in `corpus-observed/<feature-slug>/` that
   future sessions (and humans) can rely on.
2. **An article gap list** — what the public knowledge base should say about this feature
   and currently doesn't, with evidence.

You are NOT producing customer-facing answers. Nothing you write goes into `corpus/` or
`corpus-internal/` directly — a human promotes findings after checking them.

## Ground rules

1. **Test events only. Never touch a live customer event.** Use obviously synthetic data
   ("Test Submitter One", "An Abstract About Nothing") — never real names, emails or
   research content, even as filler.
2. **Record the run**: app version if visible, date, plan, account used. Observations rot;
   undated observations are worthless.
3. **Observation and inference are different things, and you must keep them separate.**
   "The button is labelled Open submissions" is an observation. "This probably closes at
   midnight server time" is an inference — mark it `[inferred]` and say why. If you did
   not see it happen, you do not know it.
4. **Quote the interface verbatim.** Button labels, menu paths, error messages —
   exact text, in quotes. A paraphrased error message is useless for search matching.
5. **When something is ambiguous, try it.** Don't speculate about what a toggle does —
   toggle it and record what changed. If you can't test it safely, write `[untested]`.
6. **Screenshot every distinct state** you describe: the default view, each meaningful
   setting change, every error. Name files by state, not by sequence number
   (`submission-form-over-word-limit-error.png`, not `screenshot-14.png`).

## Method — work through these in order

**1. Read first, then forget you read it.** Read the existing articles for this feature
and write down every checkable claim they make (menu paths, step counts, limits, plan
availability). This is your verification list. Then approach the feature as if you had
never seen the articles.

**2. Walk the happy path as a novice.** Do the feature's main task start to finish,
recording every step: what you clicked, what it was called, what happened. Note anywhere
you hesitated — if *you* had to look for something, the persona (a middle-aged organiser
who is not confident with software) is lost.

**3. Probe systematically.** For every screen in the feature:
   - Change each setting and record what it actually affects
   - Feed it boundary values: empty, one character, the stated maximum, one over
   - Do things in the wrong order; go back mid-flow; refresh mid-task
   - Trigger every error you can, and record the message verbatim
   - Note what is saved automatically versus what needs an explicit action

**4. Repeat the walk under each assigned plan.** Record precisely what appears,
disappears, or is disabled between plans — feature by feature, not impressionistically.
This section is load-bearing: it settles plan gating empirically.

**5. Reconcile against the articles.** For every claim on your verification list:
confirmed, changed (say what it is now), or could-not-verify. A renamed button or an
extra step is a finding, not a footnote.

**6. Write the dossier** (structure below). Then, last, write the article gap list —
grounded in what you observed and, where possible, cross-referenced against
`project/ticket-analysis.md` and the failing search terms in
`project/context-from-conversation.md`.

## Dossier structure

```
corpus-observed/<feature-slug>/
  META.md           assignment block, filled in; anything that limited the run
  overview.md       what the feature is and the mental model a user needs (one page max)
  walkthrough.md    the happy path, step by step, labels verbatim, screenshots referenced
  behaviour.md      settings and what each actually does; save/autosave behaviour; limits
  by-plan.md        exactly what differs under each plan — table format
  errors.md         every error state: trigger → verbatim message → what fixes it
  stumbling.md      where a non-technical first-timer would get stuck, and why
  article-gaps.md   proposed articles/edits, each with: title, one-line scope, evidence
  screenshots/
```

Every file starts with frontmatter:

```yaml
---
feature: <slug>
observed: true
app_version: <if visible, else "unknown">
explored: 2026-07-29
plan: <plan(s) this file's facts were observed under>
---
```

Every factual line should be standalone and checkable. Prefer many short dated facts to
flowing prose. Tag anything not directly observed: `[inferred]` or `[untested]`.

## What good looks like

The test of the dossier: **could a support agent answer a customer's question about this
feature from your notes alone, without opening the app — and trust the answer?** If a
fact wouldn't survive that test, mark it or cut it.

The test of the gap list: each proposed article names the evidence — "error state
undocumented, observed under all plans" beats "this might be useful".

## What happens to your output

- `article-gaps.md` feeds the writing queue; a human decides what gets written.
- Verified facts get promoted into `corpus-internal/` (quick answers) or full articles.
- The dossier itself becomes the baseline for the next run of this brief on the same
  feature: the diff between runs is the drift report — what the product changed that the
  documentation doesn't know about yet.
- Your screenshots replace the 2021–2023 ones currently in the articles.
