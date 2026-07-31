# Observed corpus

Dossiers written by walking the product, one folder per feature. See
`project/feature-exploration-brief.md` for the standing instructions.

**Nothing in here is customer-facing and nothing here is answerable.** `build.py`
reads `corpus/` and `corpus-internal/` only, so these notes cannot reach the answer
layer. That is deliberate: an agent misreading a screen produces plausible,
confidently wrong notes, and a wrong menu path in a live answer becomes a support
ticket nobody can trace. A human promotes findings from here into `corpus/` or
`corpus-internal/` after checking them.

Each dossier records the date, the plan and the account used, because observations
rot faster than prose. The diff between two runs of the same feature is the drift
report: what the product changed that the documentation does not know about yet.

Observation and inference are kept apart. Anything not directly seen is tagged
`[inferred]` or `[untested]`.
