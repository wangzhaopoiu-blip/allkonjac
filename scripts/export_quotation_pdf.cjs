const fs=require('fs'),path=require('path');
const {chromium}=require(process.env.ALL_KONJAC_PLAYWRIGHT_MODULE || 'playwright');
const root=path.resolve(__dirname,'..'),out=path.join(root,'assets/documents');
const base=process.env.ALL_KONJAC_PREVIEW_URL || 'http://127.0.0.1:8791';
(async()=>{fs.mkdirSync(out,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
try{for(const lang of ['en','th','id']){const page=await browser.newPage();await page.goto(base+'/audits/quotation-print/'+lang+'.html');await page.evaluate(()=>document.fonts.ready);await page.pdf({path:path.join(out,'quotation-example-'+lang+'.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:false,tagged:true});await page.close();console.log('Exported '+lang);}}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
