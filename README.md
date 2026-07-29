# Oxford Abstracts Help Centre

Static help centre generated from a markdown corpus, with an optional
Claude-powered answer layer on search.

## What's here

```
index.html                  landing page
01-getting-started/ ...     14 section folders, 174 article pages
assets/style.css            the whole design system
assets/search-index.json    routing index (title, section, audience, summary)
assets/articles.json        full article text, used by the answer endpoint
assets/search.js            front-end search: keyword + optional LLM answer
api/search.js               serverless endpoint, two Haiku calls
scripts/update-article.js   describe a change -> Sonnet edits -> pull request
vercel.json                 199 redirects from the old HubSpot URLs
redirects.csv               the same map, if your host wants a different format
docs/search-pipeline.md     how the two pipelines work and what they cost
```

The site works with no backend at all. Search falls back to keyword matching
over `search-index.json`, so nothing breaks if the API is off, slow or unpaid.

## Deploying

Vercel is the shortest path, since `api/search.js` runs as-is:

```bash
vercel deploy
vercel env add ANTHROPIC_API_KEY     # server-side only, never in the page
```

Any static host works too (Netlify, Cloudflare Pages, S3) — drop the `api`
folder and the site runs keyword-only, or point `ANSWER_ENDPOINT` in
`assets/search.js` at wherever you host the function.

Then repoint `help.oxfordabstracts.com` at the new deployment. `vercel.json`
already maps every old `/knowledge/...` URL to its new page with a 301, so
existing links and search rankings survive the move.

## Editing content

Articles live in the `corpus/` folder as markdown with frontmatter — that is
the source of truth, not the HTML. Edit the markdown and rebuild; never edit
the generated HTML.

```bash
python3 build_site.py        # regenerates the whole site
```

To update by describing a change instead:

```bash
node scripts/update-article.js "Reviewers can now be assigned by category from
the review tables."
```

That routes to the affected articles, rewrites them, and opens a pull request
for a human to approve.

## Known follow-ups

- The six consolidated symposia articles in `09-add-ons/` are stitched from
  their source pages and need a smoothing pass.
- `plan:` in frontmatter says "review: confirm plan gating" on most articles.
  Only the Professional features and the two add-ons are confirmed.
- `corpus/_review-unmapped-faq.md` holds two FAQ answers that need a home.
- The "Most popular" list on the landing page is a guess until the real
  HubSpot analytics go in.
