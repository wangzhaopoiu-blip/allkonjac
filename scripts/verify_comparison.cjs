const fs=require('fs');
const path=require('path');
const {chromium}=require('C:/Users/wangzhao/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..');
const base=process.argv[2]||'http://127.0.0.1:8787';
const slug='konjac-refined-powder-vs-konjac-gum';
const output=path.join(root,'audits/comparison-2026-10-20');
fs.mkdirSync(output,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const errors=[],rows=[];
 try{
  for(const width of [390,1440]){
   const page=await browser.newPage({viewport:{width,height:1000},reducedMotion:'reduce'});
   page.on('pageerror',e=>errors.push(e.message));
   page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
   for(const lang of ['en','th','id']){
    const prefix=lang==='en'?'':'/'+lang;
    for(const suffix of ['/blog/','/blog/'+slug+'/']){
     const route=prefix+suffix;
     const response=await page.goto(base+route,{waitUntil:'networkidle'});
     const state=await page.evaluate(()=>({h1:document.querySelectorAll('h1').length,lang:document.documentElement.lang,overflow:document.documentElement.scrollWidth>innerWidth,han:/[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/u.test(document.documentElement.outerHTML),brokenImages:[...document.images].filter(x=>!x.complete||!x.naturalWidth).length,canonical:document.querySelector('link[rel=canonical]').href,alternates:[...document.querySelectorAll('link[hreflang]')].map(x=>[x.hreflang,x.href]),font:getComputedStyle(document.body).fontFamily,robot:document.querySelector('meta[name=robots]').content}));
     rows.push({width,route,status:response.status(),...state});
     if(response.status()!==200||state.h1!==1||state.lang!==lang||state.overflow||state.han||state.brokenImages||state.canonical!=='https://allkonjac.com'+route||state.alternates.length!==4||!state.robot.startsWith('index,follow'))errors.push(`Page failed: ${width} ${route}`);
     if(lang==='th'&&!state.font.includes('Noto Sans Thai'))errors.push('Thai font missing');
     if(suffix.includes(slug)){
      await page.screenshot({path:path.join(output,`${lang}-${width}.png`)});
      if(width===1440)await page.locator('.table-scroll').first().screenshot({path:path.join(output,`${lang}-table.png`)});
      const integrity=await page.evaluate(()=>({missing:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash),tables:document.querySelectorAll('.table-scroll').length,refs:document.querySelectorAll('span[id^="ref-"]').length,schema:JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent)}));
      if(integrity.missing.length||integrity.tables!==3||integrity.refs!==7||integrity.schema.datePublished!=='2026-10-20'||integrity.schema.inLanguage!==lang)errors.push('Article integrity failed: '+lang);
      if(width===390){
       const button=page.locator('.menu-button');
       await button.click();if(await button.getAttribute('aria-expanded')!=='true')errors.push('Mobile menu failed '+lang);
       await button.click();
       await page.locator('.toc-panel a').nth(3).click();
       const pos=await page.evaluate(()=>document.querySelector(location.hash).getBoundingClientRect().top);
       if(pos<50||pos>260)errors.push('TOC obscured '+lang+' '+pos);
       await page.locator('article a[href="#ref-1"]').first().click();
       if(!page.url().endsWith('#ref-1'))errors.push('Citation failed '+lang);
      }
     }else{
      await page.locator('.comparison-feature-card').screenshot({path:path.join(output,`${lang}-card-${width}.png`)});
      await page.locator('.comparison-feature-card a').first().click();
      if(!page.url().includes(slug))errors.push('Card failed '+lang);
     }
    }
   }
   await page.close();
  }
 }finally{await browser.close()}
 const report={base,rows,errors,passed:!errors.length};
 fs.writeFileSync(path.join(output,base.startsWith('https')?'production-browser.json':'browser.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({base,pages:rows.length,errors,passed:report.passed}));
 if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
