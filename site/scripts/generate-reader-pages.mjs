import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const root = path.resolve(site, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'book/qrcode-manifest.json'), 'utf8'));
const activities = path.join(site, 'src/pages/activities');
fs.mkdirSync(activities, {recursive: true});
fs.writeFileSync(path.join(activities, 'index.mdx'), `# Companion activities\n\n${manifest.chapters.map((item) => `- [Chapter ${item.id}: ${item.title}](./${item.id})`).join('\n')}\n`);
for (const item of manifest.chapters) {
  const article = item.article_url ? `\n- [Read the companion article](${item.article_url})` : '';
  fs.writeFileSync(path.join(activities, `${item.id}.mdx`), `# Chapter ${item.id}: ${item.title}\n\nThis page is a reader bridge, not a copy of the course.\n\n## Explore the original source\n\n${item.activity}\n\n**Expected:** ${item.expected}\n\n- [Open the original public source](${item.source_url})${article}\n`);
}
