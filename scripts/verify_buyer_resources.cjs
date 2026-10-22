const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {chromium}=require(process.env.ALL_KONJAC_PLAYWRIGHT_MODULE || 'playwright');
const base=process.env.ALL_KONJAC_PREVIEW_URL||'http://127.0.0.1:8791',root=path.resolve(__dirname,'..');
const out=path.join(root,'audits/buyer-quotation-browser');fs.mkdirSync(out,{recursive:true});
const data=JSON.parse(fs.readFileSync(path.join(root,'source/data/buyer-resources.json'),'utf8'));
const briefs=JSON.parse(fs.readFileSync(path.join(root,'source/buyer-briefs.json'),'utf8'));
const checks=[];
(async()=>{const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
try{for(const lang of ['en','th','id']){
 const prefix=lang==='en'?'':'/'+lang;
 const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
 const page=await context.newPage();
 for(const business of ['ingredients','equipment','drying-lines','technology']){
  await page.goto(base+prefix+'/'+business+'/');
  const text=await page.locator('#enquiry-template').textContent();assert.equal(text,briefs[lang][business].message);
  const wa=new URL(await page.locator('#contact a[href^="https://wa.me"]').getAttribute('href'));
  const email=new URL(await page.locator('#contact a[href^="mailto:"]').getAttribute('href'));
  assert.equal(wa.searchParams.get('text'),text);assert.equal(email.searchParams.get('body'),text);
  assert(email.searchParams.get('subject').includes(briefs[lang][business].heading));
  await page.locator('[data-copy-enquiry]').click();assert.equal((await page.evaluate(()=>navigator.clipboard.readText())).replace(/\r\n/g,'\n'),text);
  assert.equal(await page.locator('.copy-status').innerText(),data[lang].copied);
  await page.evaluate(()=>Object.defineProperty(navigator.clipboard,'writeText',{value:async()=>{throw Error('clipboard denied')},configurable:true}));
  await page.locator('[data-copy-enquiry]').click();assert.equal(await page.locator('.copy-status').innerText(),data[lang].failed);
  for(const width of [360,1440]){await page.setViewportSize({width,height:950});assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1));}
  checks.push(lang+'/'+business+' prefill, clipboard success/failure, layout');
 }
 for(const width of [390,1440]){
  await page.setViewportSize({width,height:950});await page.goto(base+prefix+'/');await page.screenshot({path:path.join(out,lang+'-home-'+width+'.png')});
  const links=await page.locator('#business .card a').evaluateAll(n=>n.map(a=>new URL(a.href).pathname));assert.equal(links.length,4);assert(links.every(h=>h.startsWith(prefix+'/')));
  await page.goto(base+prefix+'/ingredients/#quotation-example');await page.locator('#quotation-example').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,lang+'-quotation-'+width+'.png')});
 }
 const link=page.locator('.quote-download');assert.equal(await link.getAttribute('href'),'/assets/documents/quotation-example-'+lang+'.pdf');
 const pdf=await page.request.get(base+await link.getAttribute('href'));assert.equal(pdf.status(),200);assert((await pdf.body()).subarray(0,4).equals(Buffer.from('%PDF')));
 const text=await page.locator('#quotation-example').innerText();assert(text.includes('194,000.00'));assert(!/HuBei|HuiPu|Wang Zhao|about:blank|20\/11\/2026|[\u3400-\u9fff]/u.test(text));
 await context.close();
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:850}});const p=await nojs.newPage();await p.goto(base+prefix+'/ingredients/');assert(await p.locator('#enquiry-template').isVisible());assert(await p.locator('.quote-download').isVisible());assert(!await p.locator('[data-copy-enquiry]').isVisible());await nojs.close();
 checks.push(lang+' anonymous PDF, numeric total, no-JS template and download');
}
fs.writeFileSync(path.join(out,'report.json'),JSON.stringify({status:'passed',checks,sentMessages:0},null,2));console.log('Buyer-resource checks passed: '+checks.length);
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
