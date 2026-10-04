// Render the same SVG frame sources used by the still illustrations.
// Requires sharp. PROFILE_NODE_MODULES may point to a shared package directory.
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require(process.env.PROFILE_NODE_MODULES ? path.join(process.env.PROFILE_NODE_MODULES, 'sharp') : 'sharp');
const root = path.resolve(__dirname, '..');
const sources = path.join(root, '.preview', 'animation-frames');

(async () => {
  const supported = ['header', 'header-mobile', 'lumen-process', 'lumen-process-mobile', 'project-systems', 'project-systems-mobile'];
  const selected = process.argv.slice(2);
  for (const name of selected.length ? selected : supported) {
    if (!supported.includes(name)) throw new Error(`Unknown storyboard: ${name}`);
    const dir = path.join(sources, name);
    const frames = (await fs.readdir(dir)).filter(name => /^\d{3}\.svg$/.test(name)).sort();
    // Bound memory while rendering independent frame images.
    for (let start = 0; start < frames.length; start += 4) {
      await Promise.all(frames.slice(start, start + 4).map(async file => {
        await sharp(path.join(dir, file)).png().toFile(path.join(dir, file.replace('.svg', '.png')));
      }));
    }
    console.log(`${name}: rendered ${frames.length} frames`);
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
