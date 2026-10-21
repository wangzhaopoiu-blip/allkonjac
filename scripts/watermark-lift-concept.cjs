/** Extend the approved watermark inventory with the selected drying-line concept image. */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const pw=require(process.env.EQUIPMENT_PLAYWRIGHT_MODULE||path.resolve(path.dirname(process.execPath),'../node_modules/playwright'));
const root=path.resolve(__dirname,'..'),manifestPath=path.join(root,'source/image-watermark.json');
const original=process.argv[2];if(!original)throw new Error('Supply the retained, private original concept file');
const target=path.join(root,'assets/drying-line-incline-lift-concept.webp');
if(path.resolve(original)===target)throw new Error('Use a retained original outside public assets');
const st=fs.statfsSync(path.dirname(target));if(st.bavail*st.bsize<2*1024**3+5*1024**2)throw new Error('D reserve');
const manifest=JSON.parse(fs.readFileSync(manifestPath,'utf8')),params=manifest.parameters;
if(manifest.version>=2)throw new Error('Use scripts/rebrand-watermarks.cjs with the retained original map for the current ALL KONJAC watermark');
const hash=x=>crypto.createHash('sha256').update(x).digest('hex'),input=fs.readFileSync(original),logo=fs.readFileSync(path.join(root,'assets/company-mark.jpg'));
if(hash(logo)!==manifest.logoSha256)throw new Error('Approved logo changed');
const prior=manifest.images.find(x=>x.path==='drying-line-incline-lift-concept.webp');
if(prior)throw new Error('Concept asset is already registered; use a new versioned filename for a revised image');
if(fs.existsSync(target))throw new Error('Target exists without a manifest record');
(async()=>{const browser=await pw.chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});try{const page=await browser.newPage();
const result=await page.evaluate(async({original,logo,params})=>{
const img=new Image();img.src=logo;await img.decode();const l=document.createElement('canvas');l.width=img.naturalWidth;l.height=img.naturalHeight;const lc=l.getContext('2d');lc.drawImage(img,0,0);const pixels=lc.getImageData(0,0,l.width,l.height);let left=l.width,top=l.height,right=0,bottom=0;
for(let y=0;y<l.height;y++)for(let x=0;x<l.width;x++){const i=(y*l.width+x)*4,min=Math.min(pixels.data[i],pixels.data[i+1],pixels.data[i+2]);pixels.data[i+3]=Math.round(Math.min(1,(255-min)/20)*255);if(min<235){left=Math.min(left,x);top=Math.min(top,y);right=Math.max(right,x);bottom=Math.max(bottom,y);}}
lc.putImageData(pixels,0,0);const stamp=document.createElement('canvas');stamp.width=right-left+1;stamp.height=bottom-top+1;stamp.getContext('2d').drawImage(l,left,top,stamp.width,stamp.height,0,0,stamp.width,stamp.height);
const image=new Image();image.src=original;await image.decode();const canvas=document.createElement('canvas');canvas.width=image.naturalWidth;canvas.height=image.naturalHeight;const c=canvas.getContext('2d');c.drawImage(image,0,0);const before=c.getImageData(0,0,canvas.width,canvas.height);
const w=Math.min(canvas.width,canvas.height)*params.logoWidthToShortEdge,h=w*stamp.height/stamp.width,dx=w*params.spacingFactor,dy=h*params.spacingFactor,extent=Math.hypot(canvas.width,canvas.height);
c.save();c.translate(canvas.width/2,canvas.height/2);c.rotate(params.angle*Math.PI/180);c.globalAlpha=params.opacity;for(let row=-Math.ceil(extent/dy);row<=Math.ceil(extent/dy);row++)for(let col=-Math.ceil(extent/dx);col<=Math.ceil(extent/dx);col++)c.drawImage(stamp,col*dx+(row%2?dx/2:0)-w/2,row*dy-h/2,w,h);c.restore();const after=c.getImageData(0,0,canvas.width,canvas.height);let changed=0;
for(let i=0;i<after.data.length;i+=4)if(Math.abs(after.data[i]-before.data[i])+Math.abs(after.data[i+1]-before.data[i+1])+Math.abs(after.data[i+2]-before.data[i+2])>=3)changed++;
return{data:canvas.toDataURL('image/webp',params.quality).split(',')[1],width:canvas.width,height:canvas.height,changedPixelRatio:changed/(canvas.width*canvas.height)};
},{original:'data:'+(path.extname(original).toLowerCase()==='.png'?'image/png':path.extname(original).toLowerCase()==='.webp'?'image/webp':'image/jpeg')+';base64,'+input.toString('base64'),logo:'data:image/jpeg;base64,'+logo.toString('base64'),params});
if(result.changedPixelRatio<.01)throw new Error('Insufficient watermark coverage');const bytes=Buffer.from(result.data,'base64');fs.writeFileSync(target,bytes);
manifest.images=manifest.images.filter(x=>x.path!=='drying-line-incline-lift-concept.webp');manifest.images.push({path:'drying-line-incline-lift-concept.webp',originalSha256:hash(input),watermarkedSha256:hash(bytes),width:result.width,height:result.height,format:'image/webp',changedPixelRatio:result.changedPixelRatio});fs.writeFileSync(manifestPath,JSON.stringify(manifest,null,2)+'\n');console.log(JSON.stringify({concept_watermarked:true,changed_pixel_ratio:result.changedPixelRatio}));
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
