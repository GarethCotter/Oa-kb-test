# Search & update pipelines — how they work and what they cost

Two pipelines, deliberately using different models: search is high volume and
simple, updates are low volume and quality-critical.

## Search — two Claude Haiku 4.5 calls

**Call 1, route.** Input is the question plus a routing table built from
`assets/search-index.json`: path, title, section, audience and a one-line
summary for all 174 articles, roughly 10k tokens. It returns JSON only — up to
three article paths.

That table is byte-identical on every request, so it sits behind a
`cache_control: {type: "ephemeral"}` breakpoint. After the first call it bills
at the cached input rate rather than full price. This is where nearly all of
the saving comes from; without it you would pay full price for 10k tokens on
every single search.

**Call 2, answer.** Input is only the text of the routed articles (2–4k tokens)
plus the question. It returns 2–4 sentences of plain English and the guide to
read. The system prompt forbids guessing: if the guides do not answer it, it
says so and points to support. For this audience a confident wrong answer is
worse than no answer.

At Haiku 4.5 rates ($1/M input, $5/M output, cached input ~90% cheaper) a
question costs well under a cent. Answers are cached at the CDN for a day, so
repeated questions cost nothing at all.

**Failure behaviour is the important part.** The endpoint returns `200` with a
null answer on any error, and the front end silently falls back to keyword
links. The reader never sees an API error, and never sees an empty page.

## Updates — Claude Sonnet, writing to a pull request

`scripts/update-article.js "what changed"`:

1. Routes the description to the affected articles using the same cached index.
2. Sends each article's current markdown and returns the complete revised
   markdown, with frontmatter preserved.
3. Commits to a branch and opens a pull request.

It never writes to the live site. A human reads the diff and merges; the site
rebuilds from the corpus on merge. The edit prompt is explicit that this is an
edit and not a rewrite — untouched wording stays untouched, which keeps diffs
small enough to actually review.

## Logging worth adding on day one

Log the question, the routed paths, and whether the reader then clicked a
source. Questions that route badly or get no click are your content gaps — that
log is the roadmap for which articles to write next, and it is the thing the
old HubSpot KB could never tell you.

## First jobs once the pipeline runs

- Smooth the six consolidated symposia articles in `09-add-ons/`.
- Fill in `plan:` where it still reads "review: confirm plan gating".
- Place the two unmapped FAQ answers in `corpus/_review-unmapped-faq.md`.
