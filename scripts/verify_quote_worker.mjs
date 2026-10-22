import assert from 'node:assert/strict';
import worker from '../worker.mjs';
const env={ASSETS:{fetch:async()=>new Response('asset',{headers:{'Content-Type':'application/pdf'}})}};
const redirect=await worker.fetch(new Request('http://allkonjac.com/th/ingredients/?a=1&b=2'),env);
assert.equal(redirect.status,301);assert.equal(redirect.headers.get('location'),'https://allkonjac.com/th/ingredients/?a=1&b=2');
for(const lang of ['en','th','id']){
 const r=await worker.fetch(new Request('https://allkonjac.com/assets/documents/quotation-example-'+lang+'.pdf?download=1'),env);
 assert.equal(r.headers.get('x-robots-tag'),'noindex');assert.equal(await r.text(),'asset');assert.equal(r.headers.get('content-type'),'application/pdf');
}
assert.equal((await worker.fetch(new Request('https://allkonjac.com/ingredients/'),env)).headers.get('x-robots-tag'),null);
console.log('HTTPS redirect and selective PDF noindex passed.');
