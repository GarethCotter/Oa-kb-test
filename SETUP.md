# Moving this project into Claude Code

## 1. Install and clone

```bash
npm install -g @anthropic-ai/claude-code     # needs Node 18+
git clone https://github.com/GarethCotter/Oa-kb-test.git
cd Oa-kb-test
```

## 2. Add the files from this bundle

Copy these into the repo root, then commit:

- `CLAUDE.md` — project context. Claude Code reads this automatically at the start of
  every session, so it starts knowing the architecture, conventions and gotchas.
- `build.py` — replaces `build_site.py`, which had hard-coded paths from the old sandbox
  and would not run in this repo. Delete `build_site.py`.
- `corpus/` — **the 174 source markdown files. These are missing from the repo.**
  Without them nothing can be regenerated.
- `redirects.csv` — needed by the build (already at the repo root; overwrite is fine).
- `project/` — analysis, checklists and outstanding decisions.

```bash
pip install markdown beautifulsoup4 lxml
python3 build.py        # should print: 14 sections, 174 article pages
git add -A && git commit -m "Add source corpus, build script and project context"
git push
```

If `build.py` regenerates identical HTML, nothing changes on the live site — which is
the point. It proves the sources and the deployed site are in sync.

## 3. Start Claude Code

```bash
claude
```

Good first session prompts:

- *"Read CLAUDE.md and project/checklist.md, then summarise what's outstanding."*
- *"Add the five missing articles listed in project/ticket-analysis.md, following the
  conventions in CLAUDE.md. Rebuild and run the link checker."*
- *"Apply the plan-gating answers in project/plan-gating-review.csv once I've filled it in."*

## What changes for the better

- No more zip → upload → check loop. It edits files directly, runs the build, and pushes.
- It can run the link checker and see the failures itself, rather than being told.
- It can use the Vercel MCP to read build and runtime logs when something breaks.
- Multi-file jobs — a rename across 174 articles, or a voice pass — become one instruction.

## What to keep an eye on

- **It can't see the rendered page.** Layout and visual bugs still need your eyes, or a
  screenshot pasted into the session.
- **Ask it to verify, not assume.** Several bugs in this project came from an edit that
  silently did nothing. CLAUDE.md says this, but it's worth repeating in the moment.
- **Give it the Anthropic API key only via Vercel's environment variables**, never in the
  repo or in a prompt.
