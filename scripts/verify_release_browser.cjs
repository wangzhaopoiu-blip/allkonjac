const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const pw = require(process.env.ALL_KONJAC_PLAYWRIGHT_MODULE || 'playwright');

const base = process.env.ALL_KONJAC_PREVIEW_URL || 'http://127.0.0.1:8790';
const root = path.resolve(__dirname, '..');
const out = path.join(root, 'audits', 'release-browser-2026-10-20');
fs.mkdirSync(out, {recursive: true});
const paths = [...fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8').matchAll(/<loc>(https:\/\/allkonjac\.com[^<]+)<\/loc>/g)]
  .map(match => new URL(match[1]).pathname);
const errors = [];

(async () => {
  const browser = await pw.chromium.launch({headless: true, executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  try {
    assert.equal(paths.length, 33);
    for (const width of [390, 1440]) {
      const context = await browser.newContext({viewport: {width, height: 850}, javaScriptEnabled: false});
      for (const urlPath of paths) {
        const page = await context.newPage();
        const response = await page.goto(base + urlPath);
        assert.equal(response.status(), 200, urlPath);
        const expectedLang = urlPath.startsWith('/th/') ? 'th' : urlPath.startsWith('/id/') ? 'id' : 'en';
        assert.equal(await page.locator('html').getAttribute('lang'), expectedLang, urlPath);
        assert.equal(await page.locator('h1').count(), 1, urlPath);
        assert.equal(await page.locator('link[rel="canonical"]').getAttribute('href'), 'https://allkonjac.com' + urlPath, urlPath);
        assert(await page.locator('main').isVisible(), urlPath);
        assert(await page.locator('nav').first().isVisible(), urlPath);
        const overflow = await page.evaluate(() => ({wide: document.documentElement.scrollWidth > innerWidth + 1,
          nodes: [...document.querySelectorAll('body *')].filter(el => el.getBoundingClientRect().right > innerWidth + 1)
            .slice(0, 8).map(el => `${el.tagName}.${el.className} right=${Math.round(el.getBoundingClientRect().right)}`)}));
        assert(!overflow.wide, `${urlPath} width ${width} overflow: ${overflow.nodes.join(', ')}`);
        if (width === 390 && ['/blog/', '/th/blog/', '/id/blog/'].includes(urlPath)) {
          await page.screenshot({path: path.join(out, expectedLang + '-blog-mobile.png')});
        }
        await page.close();
      }
      await context.close();
    }
    const context = await browser.newContext({viewport: {width: 390, height: 850}});
    for (const lang of ['en', 'th', 'id']) {
      const page = await context.newPage();
      const prefix = lang === 'en' ? '' : '/' + lang;
      await page.goto(base + prefix + '/blog/');
      const menu = page.locator(lang === 'en' ? '.menu-button' : '.menu-toggle');
      await menu.click();
      assert.equal(await menu.getAttribute('aria-expanded'), 'true', `${lang} menu`);
      assert(await page.locator(lang === 'en' ? '#site-nav' : '#primary-navigation').isVisible(), `${lang} navigation`);
      assert.equal(await page.locator('.brand').first().getAttribute('href'), prefix + '/', `${lang} home`);
      await page.close();
    }
    await context.close();
    const report = {date: '2026-10-20', status: 'passed', pages: paths.length, layouts: [390, 1440], checks: 'HTTP, language, h1, canonical, visible content and navigation without JavaScript, horizontal overflow, mobile interactive menu and brand home link', errors};
    fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 2));
    console.log(JSON.stringify(report));
  } catch (error) {
    errors.push(error.message);
    fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify({date: '2026-10-20', status: 'failed', errors}, null, 2));
    throw error;
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode = 1;});
