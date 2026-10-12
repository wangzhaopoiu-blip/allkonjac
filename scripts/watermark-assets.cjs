/* Prepare approved website watermarks from PRIVATE original assets, never from outputs. */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const runtime = process.env.ALL_KONJAC_NODE_MODULES;
const { chromium } = require(runtime ? path.join(runtime, 'playwright') : 'playwright');
const ROOT = path.resolve(__dirname, '..');
const ASSETS = path.join(ROOT, 'assets');
const MANIFEST = path.join(ROOT, 'source/image-watermark.json');
const EXEMPT = ['company-mark.jpg', 'wechat-qr.png', 'flags/gb.svg', 'flags/th.svg', 'flags/id.svg'];
const PARAMS = { angle: -30, opacity: 0.2, logoWidthToShortEdge: 0.25, spacingFactor: 1.8, quality: 0.95 };
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
function images(dir, prefix = '') {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    const rel = prefix + entry.name;
    return entry.isDirectory() ? images(path.join(dir, entry.name), rel + '/')
      : /\.(jpe?g|png|webp|svg)$/i.test(entry.name) ? [rel] : [];
  }).sort();
}

async function main() {
  const [originalDirectory, executablePath] = process.argv.slice(2);
  if (!originalDirectory || !executablePath) throw new Error('Usage: node scripts/watermark-assets.cjs <private-original-assets-directory> <browser-executable>');
  const originals = fs.realpathSync(originalDirectory);
  if (originals.toLowerCase() === fs.realpathSync(ASSETS).toLowerCase()) throw new Error('Input must be private originals, not public watermarked assets');
  const files = images(ASSETS);
  const originalFiles = images(originals);
  if (JSON.stringify(files) !== JSON.stringify(originalFiles)) throw new Error('Public/original image inventory differs; classify new images before proceeding');
  const business = files.filter(file => !EXEMPT.includes(file));
  if (business.some(file => /\.svg$/i.test(file))) throw new Error('Unclassified vector image requires explicit review');
  const existing = fs.existsSync(MANIFEST) ? JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) : null;
  const logoBytes = fs.readFileSync(path.join(originals, 'company-mark.jpg'));
  if (existing && hash(logoBytes) !== existing.logoSha256) throw new Error('Approved logo changed');
  for (const file of business) {
    const original = fs.readFileSync(path.join(originals, file));
    const current = fs.readFileSync(path.join(ASSETS, file));
    const previous = existing && existing.images.find(record => record.path === file);
    if (previous && hash(original) !== previous.originalSha256) throw new Error('Private original changed: ' + file);
    if (hash(current) !== hash(original) && (!previous || hash(current) !== previous.watermarkedSha256)) throw new Error('Unexpected public edit; preserve it before regeneration: ' + file);
  }
  for (const file of EXEMPT) if (hash(fs.readFileSync(path.join(ASSETS, file))) !== hash(fs.readFileSync(path.join(originals, file)))) throw new Error('Exempt asset changed: ' + file);
  const browser = await chromium.launch({ headless: true, executablePath });
  const manifest = { version: 1, parameters: PARAMS, logoSha256: hash(logoBytes), images: [], exempt: [] };
  const pending = [];
  try {
    const page = await browser.newPage();
    await page.evaluate(async logo => {
      const image = new Image(); image.src = logo; await image.decode();
      const canvas = document.createElement('canvas'); canvas.width = image.naturalWidth; canvas.height = image.naturalHeight;
      const ctx = canvas.getContext('2d'); ctx.drawImage(image, 0, 0);
      const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height);
      let left = canvas.width, top = canvas.height, right = 0, bottom = 0;
      for (let y = 0; y < canvas.height; y++) for (let x = 0; x < canvas.width; x++) {
        const i = (y * canvas.width + x) * 4;
        const min = Math.min(pixels.data[i], pixels.data[i + 1], pixels.data[i + 2]);
        pixels.data[i + 3] = Math.round(Math.min(1, (255 - min) / 20) * 255);
        if (min < 235) { left = Math.min(left, x); top = Math.min(top, y); right = Math.max(right, x); bottom = Math.max(bottom, y); }
      }
      ctx.putImageData(pixels, 0, 0);
      window.approvedLogo = document.createElement('canvas'); approvedLogo.width = right - left + 1; approvedLogo.height = bottom - top + 1;
      approvedLogo.getContext('2d').drawImage(canvas, left, top, approvedLogo.width, approvedLogo.height, 0, 0, approvedLogo.width, approvedLogo.height);
    }, 'data:image/jpeg;base64,' + logoBytes.toString('base64'));
    for (const file of business) {
      const original = fs.readFileSync(path.join(originals, file));
      const mime = /\.webp$/i.test(file) ? 'image/webp' : /\.png$/i.test(file) ? 'image/png' : 'image/jpeg';
      const rendered = await page.evaluate(async ({ original, mime, params }) => {
        const image = new Image(); image.src = original; await image.decode();
        const canvas = document.createElement('canvas'); canvas.width = image.naturalWidth; canvas.height = image.naturalHeight;
        const ctx = canvas.getContext('2d'); ctx.drawImage(image, 0, 0);
        const before = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const w = Math.min(canvas.width, canvas.height) * params.logoWidthToShortEdge;
        const h = w * approvedLogo.height / approvedLogo.width;
        const dx = w * params.spacingFactor, dy = h * params.spacingFactor, extent = Math.hypot(canvas.width, canvas.height);
        ctx.save(); ctx.translate(canvas.width / 2, canvas.height / 2); ctx.rotate(params.angle * Math.PI / 180); ctx.globalAlpha = params.opacity;
        for (let row = -Math.ceil(extent / dy); row <= Math.ceil(extent / dy); row++) for (let col = -Math.ceil(extent / dx); col <= Math.ceil(extent / dx); col++) ctx.drawImage(approvedLogo, col * dx + (row % 2 ? dx / 2 : 0) - w / 2, row * dy - h / 2, w, h);
        ctx.restore(); const after = ctx.getImageData(0, 0, canvas.width, canvas.height); let changed = 0;
        for (let i = 0; i < after.data.length; i += 4) if (Math.abs(after.data[i] - before.data[i]) + Math.abs(after.data[i + 1] - before.data[i + 1]) + Math.abs(after.data[i + 2] - before.data[i + 2]) >= 3) changed++;
        const encoded = canvas.toDataURL(mime, params.quality);
        if (!encoded.startsWith('data:' + mime + ';base64,')) throw new Error('Browser cannot encode ' + mime);
        return { data: encoded.split(',')[1], width: canvas.width, height: canvas.height, changedPixelRatio: changed / (canvas.width * canvas.height) };
      }, { original: `data:${mime};base64,${original.toString('base64')}`, mime, params: PARAMS });
      if (rendered.changedPixelRatio < 0.01) throw new Error('Insufficient watermark coverage: ' + file);
      const bytes = Buffer.from(rendered.data, 'base64');
      pending.push({ file, bytes });
      manifest.images.push({ path: file, originalSha256: hash(original), watermarkedSha256: hash(bytes), width: rendered.width, height: rendered.height, format: mime, changedPixelRatio: rendered.changedPixelRatio });
    }
    for (const file of EXEMPT) manifest.exempt.push({ path: file, sha256: hash(fs.readFileSync(path.join(ASSETS, file))) });
    // Validate every image before touching outputs; always start from the retained originals.
    for (const { file, bytes } of pending) fs.writeFileSync(path.join(ASSETS, file), bytes);
    fs.writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2) + '\n');
    console.log(JSON.stringify({ processed: business.length, exempt: EXEMPT.length, manifest: MANIFEST }));
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
