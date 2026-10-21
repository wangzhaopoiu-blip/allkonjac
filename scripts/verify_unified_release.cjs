const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {chromium} = require(process.env.ALL_KONJAC_PLAYWRIGHT_MODULE || 'playwright');
const base = process.env.ALL_KONJAC_PREVIEW_URL || 'http://127.0.0.1:8790';
const root = path.resolve(__dirname, '..');
const out = path.join(root, 'audits', 'unified-browser-2026-10-21');
fs.mkdirSync(out, {recursive:true});
const samples = JSON.parse(fs.readFileSync(path.join(root, 'source/data/coa-reference-en.json'), 'utf8')).samples;
const errors = [];
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', args:['--use-angle=d3d11']});
  try {
    const context = await browser.newContext({reducedMotion:'reduce'});
    const page = await context.newPage();
    page.on('pageerror', e => errors.push(e.message));
    for (const lang of ['en','th','id']) {
      const prefix = lang === 'en' ? '' : '/' + lang;
      await page.goto(base + prefix + '/blog/');
      const urls = await page.locator('main a').evaluateAll(nodes => [...new Set(nodes.map(n=>new URL(n.href).pathname).filter(p=>/\/blog\/[^/]+\/$/.test(p)))]);
      assert.equal(urls.length, 6, lang + ' six articles on index');
      assert(urls.every(url=>url.startsWith(prefix + '/blog/')), lang + ' localized article links');
      for (const width of [360,390,768,1440]) {
        await page.setViewportSize({width,height:950});
        await page.goto(base + prefix + '/ingredients/');
        assert.equal(await page.locator('.quality-card').count(), 2);
        await page.locator('#quality-documents').scrollIntoViewIfNeeded();
        assert((await page.locator('.quality-card').nth(1).innerText()).includes('93'));
        assert.equal(await page.locator('#buyer-brief').count(),1);
        assert(!await page.evaluate(()=>document.documentElement.scrollWidth > innerWidth+1),lang+' ingredients '+width);
        await page.goto(base + prefix + '/ingredients/coa-reference/');
        assert.equal(await page.locator('.report-row').count(),17);
        assert.equal(await page.locator('.supplier-row').count(),1);
        assert.equal(await page.locator('.supplier-row td').nth(3).textContent(),'93');
        assert(!/88\.9|SEMUA KONJ|คอนแจคทั้งหมด/.test(await page.content()));
        const switches=await page.locator('.language-options a').evaluateAll(nodes=>nodes.map(n=>new URL(n.href).pathname));
        assert.deepEqual(switches.sort(),['/ingredients/coa-reference/','/th/ingredients/coa-reference/','/id/ingredients/coa-reference/'].sort());
        const schema=JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());
        assert.equal(schema.inLanguage,lang);
        assert.equal(schema.url,'https://allkonjac.com'+prefix+'/ingredients/coa-reference/');
        for(const sample of samples) {
          const rows=page.locator('#'+sample.id+' tbody tr');
          assert.equal(await rows.count(),sample.rows.length);
          for(let i=0;i<sample.rows.length;i++) {
            const expected=sample.rows[i].result;
            if(/^\d+(\.\d+)?$/.test(expected)) assert.equal(await rows.nth(i).locator('td').nth(3).textContent(),expected);
          }
        }
        assert(!await page.evaluate(()=>document.documentElement.scrollWidth > innerWidth+1),lang+' COA '+width);
        if(width===390 || width===1440) {
          await page.locator('#sample-2026').screenshot({path:path.join(out,lang+'-coa-'+width+'.png')});
        }
        await page.goto(base + prefix + '/drying-lines/');
        assert.equal(await page.locator('.material-card').count(),2);
        assert.equal(await page.locator('#buyer-brief').count(),1);
        await page.locator('#machine-dried-chips').scrollIntoViewIfNeeded();
        await page.waitForFunction(()=>[...document.querySelectorAll('.material-card img')].every(i=>i.complete&&i.naturalWidth>0));
        assert(!await page.evaluate(()=>document.documentElement.scrollWidth > innerWidth+1),lang+' drying '+width);
        await page.locator('.material-card a').first().click();
        assert(await page.locator('dialog').evaluate(el=>el.open));
        await page.keyboard.press('Escape');
        assert(!await page.locator('dialog').evaluate(el=>el.open));
        if(width===390) await page.locator('#machine-dried-chips').screenshot({path:path.join(out,lang+'-materials-mobile.png')});
      }
    }
    assert.deepEqual(errors,[]);
    fs.writeFileSync(path.join(out,'report.json'),JSON.stringify({passed:true,languages:['en','th','id'],widths:[360,390,768,1440],checks:['six localized articles','quality provenance and exact numeric results','COA language switch and schema','buyer briefs','material images and lightbox','no horizontal overflow'],errors},null,2));
    console.log('Unified content and browser checks passed.');
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
