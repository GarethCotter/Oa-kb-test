#!/usr/bin/env node
/* Update the knowledge base by describing what changed.
 *
 *   node scripts/update-article.js "Reviewers can now be assigned by category
 *   from the review tables, not just the assign page."
 *
 * What it does:
 *   1. Routes the description to the affected article(s) — same cached index
 *      the search endpoint uses.
 *   2. Sends each article's current markdown to Claude Sonnet and gets the full
 *      revised markdown back.
 *   3. Writes the files to a new git branch and opens a pull request.
 *
 * It never writes to the live site. A human reviews the diff and merges; the
 * site rebuilds on merge. Low volume and quality-critical, so Sonnet rather
 * than Haiku — the cost difference at this volume is pennies.
 */

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const CORPUS = 'corpus';                 // folder of section folders of .md files
const MODEL = 'claude-sonnet-5';
const API = 'https://api.anthropic.com/v1/messages';

const description = process.argv.slice(2).join(' ').trim();
if (!description) {
  console.error('Describe what changed, in quotes.');
  process.exit(1);
}

const index = JSON.parse(fs.readFileSync('site/assets/search-index.json', 'utf8'));
const table = index.map(a => `${a.path} | ${a.title} | ${a.section} | ${a.summary}`).join('\n');

async function claude(body) {
  const res = await fetch(API, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-api-key': process.env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error('Anthropic ' + res.status + ' ' + (await res.text()).slice(0, 300));
  const data = await res.json();
  return data.content.filter(c => c.type === 'text').map(c => c.text).join('\n').trim();
}

const mdPath = p => path.join(CORPUS, p.replace(/\.html$/, '.md'));

// ---- 1. route ----
const routed = await claude({
  model: MODEL,
  max_tokens: 300,
  system: [{
    type: 'text',
    cache_control: { type: 'ephemeral' },
    text:
      'You maintain the Oxford Abstracts knowledge base. Given a description of a ' +
      'product change, list the articles that need editing. JSON only, no fences: ' +
      '{"paths":["<path>",...]} — at most 4, most affected first. Use only paths ' +
      'from the index. If the change needs an article that does not exist yet, ' +
      'return {"paths":[],"suggest_new":"<proposed title and section>"}.\n\n' +
      'ARTICLE INDEX\npath | title | section | summary\n' + table
  }],
  messages: [{ role: 'user', content: description }]
});

let plan;
try { plan = JSON.parse(routed.replace(/```json|```/g, '').trim()); }
catch { console.error('Could not read the routing reply:\n' + routed); process.exit(1); }

if (!plan.paths || !plan.paths.length) {
  console.log('No existing article covers this change.');
  if (plan.suggest_new) console.log('Suggested new article: ' + plan.suggest_new);
  process.exit(0);
}

console.log('Editing:\n' + plan.paths.map(p => '  ' + p).join('\n'));

// ---- 2. rewrite each article ----
const EDIT_SYSTEM =
  'You edit help-centre articles for Oxford Abstracts. You are given one article ' +
  'as markdown and a description of what changed in the product. Return the ' +
  'COMPLETE revised markdown file and nothing else — no commentary, no fences.\n\n' +
  'Rules:\n' +
  '- Keep the YAML frontmatter block intact and set last_reviewed to today (YYYY-MM-DD). Update title only if the change ' +
  'renames the feature; never remove fields.\n' +
  '- Change only what the description affects. Leave untouched wording alone: ' +
  'this is an edit, not a rewrite.\n' +
  '- Match the existing voice: plain British English, short sentences, menu paths ' +
  'written as Event dashboard -> Emails.\n' +
  '- Keep existing links and image references unless the change makes them wrong.\n' +
  '- If the description does not actually affect this article, return it unchanged.';

const edited = [];
for (const p of plan.paths) {
  const file = mdPath(p);
  if (!fs.existsSync(file)) { console.warn('  missing: ' + file); continue; }
  const before = fs.readFileSync(file, 'utf8');
  const after = await claude({
    model: MODEL,
    max_tokens: 8000,
    system: EDIT_SYSTEM,
    messages: [{ role: 'user', content: `ARTICLE\n\n${before}\n\nWHAT CHANGED\n\n${description}` }]
  });
  if (after.trim() && after.trim() !== before.trim()) {
    fs.writeFileSync(file, after.trimEnd() + '\n');
    edited.push(file);
    console.log('  updated ' + file);
  } else {
    console.log('  no change needed: ' + file);
  }
}

if (!edited.length) { console.log('Nothing changed.'); process.exit(0); }

// ---- 3. branch + pull request ----
const branch = 'kb-update-' + Date.now();
const summary = description.length > 68 ? description.slice(0, 65) + '...' : description;
execSync(`git checkout -b ${branch}`, { stdio: 'inherit' });
execSync(`git add ${edited.map(f => JSON.stringify(f)).join(' ')}`, { stdio: 'inherit' });
execSync(`git commit -m ${JSON.stringify('KB update: ' + summary)}`, { stdio: 'inherit' });
execSync(`git push -u origin ${branch}`, { stdio: 'inherit' });

try {
  execSync(
    `gh pr create --title ${JSON.stringify('KB update: ' + summary)} ` +
    `--body ${JSON.stringify('Requested change:\n\n> ' + description + '\n\nEdited by the update pipeline. Please review the diff before merging.')}`,
    { stdio: 'inherit' }
  );
} catch {
  console.log('\nPushed branch ' + branch + '. Open the pull request in GitHub.');
}
