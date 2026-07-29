# Oxford Abstracts KB — reorganised corpus (v1)

Generated 28 Jul 2026 from a full crawl of help.oxfordabstracts.com/knowledge,
restructured per the approved 14-section plan and merge plan.

- One folder per section (01–11 organisers, 12–14 participants), one markdown file per article.
- Frontmatter on every file: title, section, audience, plan, source_url, and
  merged_from where content was consolidated.
- redirects.csv maps every old URL to its new path.
- plan: values are confirmed only for Professional features and the two add-ons;
  everything else says "all (review: confirm plan gating)" pending a review pass.
- Consolidated symposia articles carry an editorial_note — the sources were
  concatenated, not rewritten; they need a smoothing pass (a good early job for
  the update-LLM pipeline).
- _review-unmapped-faq.md (if present) holds FAQ answers whose target could not
  be matched automatically — place these by hand.
