# Internal corpus

Notes the AI search can use but that never appear as pages on the help centre.

Use this for:
- Quick answers to questions the bot couldn't answer (check the gap log), when
  a full article isn't worth it yet
- Observed behaviour the articles don't cover (error states, edge cases,
  quirks) — including anything the app-testing agent records

Rules:
- One topic per file, filename says what it answers
- Frontmatter: title, last_reviewed, and `internal: true`
- Write nothing customer-specific: these notes surface verbatim-ish to ANY
  user who asks the right question
- Date every note; delete notes when the behaviour changes or an article
  covers it
- When a note keeps getting used, promote it: ask the update pipeline to turn
  it into a real article, then delete the note
