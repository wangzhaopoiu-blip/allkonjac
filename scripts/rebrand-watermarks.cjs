/** Rebuild public business images from verified retained originals. */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {chromium}=require(process.env.ALL_KONJAC_NODE_MODULES?path.join(process.env.ALL_KONJAC_NODE_MODULES,'playwright'):path.resolve(path.dirname(process.execPath),'../node_modules/playwright'));
const root=path.resolve(__dirname,'..'),manifestPath=path.join(root,'source/image-watermark.json');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
async function main(){
 const inputMap=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),old=JSON.parse(fs.readFileSync(manifestPath,'utf8'));
 const newOnly=process.argv.includes('--only-new'),existingPaths=new Set(old.images.map(x=>x.path));
 const logoPath='brand/all-konjac-wordmark.svg',logo=fs.readFileSync(path.join(root,'assets',logoPath)),pending=[];
 const params={...old.parameters,opacity:0.1,densityScale:1/3};
 for(const record of old.images){const src=inputMap[record.path];if(!src||hash(fs.readFileSync(src))!==record.originalSha256)throw Error('Original missing or changed: '+record.path);if(hash(fs.readFileSync(path.join(root,'assets',record.path)))!==record.watermarkedSha256)throw Error('Unexpected public edit: '+record.path);}
 const browser=await chromium.launch({headless:true,executablePath:(process.argv[3]&&!process.argv[3].startsWith('--')?process.argv[3]:null)||'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 try{const page=await browser.newPage();
  for(const [rel,source] of Object.entries(inputMap)){
   if(newOnly&&existingPaths.has(rel))continue;
   const target=path.resolve(root,'assets',rel);if(!target.startsWith(path.resolve(root,'assets')+path.sep))throw Error('Invalid asset path');
   const original=fs.readFileSync(source),ext=path.extname(source).toLowerCase(),mime=ext==='.png'?'image/png':ext==='.webp'?'image/webp':'image/jpeg',format=/\.webp$/i.test(rel)?'image/webp':'image/jpeg';
   const result=await page.evaluate(async({imageUrl,logoUrl,params,format})=>{
    const image=new Image(),stamp=new Image();image.src=imageUrl;stamp.src=logoUrl;await Promise.all([image.decode(),stamp.decode()]);
    const canvas=document.createElement('canvas');canvas.width=image.naturalWidth;canvas.height=image.naturalHeight;const ctx=canvas.getContext('2d');ctx.drawImage(image,0,0);const before=ctx.getImageData(0,0,canvas.width,canvas.height);
    const w=Math.min(canvas.width,canvas.height)*params.logoWidthToShortEdge,h=w*stamp.naturalHeight/stamp.naturalWidth,dx=w*params.spacingFactor,dy=Math.max(h*params.spacingFactor,w*.7),extent=Math.hypot(canvas.width,canvas.height);
    const angle=params.angle*Math.PI/180,cos=Math.cos(angle),sin=Math.sin(angle),candidates=[];
    for(let row=-Math.ceil(extent/dy);row<=Math.ceil(extent/dy);row++)for(let col=-Math.ceil(extent/dx);col<=Math.ceil(extent/dx);col++){
     const x=col*dx+(row%2?dx/2:0),y=row*dy,cx=canvas.width/2+x*cos-y*sin,cy=canvas.height/2+x*sin+y*cos;
     if(cx>=0&&cx<=canvas.width&&cy>=0&&cy<=canvas.height)candidates.push({x,y,cx,cy});
    }
    const previousStampCount=candidates.length,targetCount=Math.max(1,Math.round(previousStampCount*params.densityScale)),selected=[],pool=[...candidates];
    pool.sort((a,b)=>Math.hypot(a.cx-canvas.width/2,a.cy-canvas.height/2)-Math.hypot(b.cx-canvas.width/2,b.cy-canvas.height/2));selected.push(pool.shift());
    while(selected.length<targetCount&&pool.length){let best=0,score=-1;for(let i=0;i<pool.length;i++){const p=pool[i],distance=Math.min(...selected.map(s=>(p.cx-s.cx)**2+(p.cy-s.cy)**2));if(distance>score){score=distance;best=i;}}selected.push(pool.splice(best,1)[0]);}
    ctx.save();ctx.translate(canvas.width/2,canvas.height/2);ctx.rotate(angle);ctx.globalAlpha=params.opacity;
    for(const point of selected)ctx.drawImage(stamp,point.x-w/2,point.y-h/2,w,h);
    ctx.restore();const after=ctx.getImageData(0,0,canvas.width,canvas.height);let changed=0;for(let i=0;i<after.data.length;i+=4)if(Math.abs(after.data[i]-before.data[i])+Math.abs(after.data[i+1]-before.data[i+1])+Math.abs(after.data[i+2]-before.data[i+2])>=3)changed++;
    return{data:canvas.toDataURL(format,params.quality).split(',')[1],width:canvas.width,height:canvas.height,changedPixelRatio:changed/(canvas.width*canvas.height),stampCount:selected.length,previousStampCount};
   },{imageUrl:`data:${mime};base64,${original.toString('base64')}`,logoUrl:'data:image/svg+xml;base64,'+logo.toString('base64'),params,format});
   if(result.changedPixelRatio<.001)throw Error('Insufficient watermark: '+rel);
   const bytes=Buffer.from(result.data,'base64');pending.push({target,bytes,record:{path:rel,originalSha256:hash(original),watermarkedSha256:hash(bytes),width:result.width,height:result.height,format,changedPixelRatio:result.changedPixelRatio,stampCount:result.stampCount,previousStampCount:result.previousStampCount}});
  }
 }finally{await browser.close();}
 const manifest={version:2,brand:'ALL KONJAC',updated:'2026-10-16',parameters:params,minimumChangedPixelRatio:0.001,logoPath,logoSha256:hash(Buffer.from(logo.toString('utf8').replace(/\r\n?/g,'\n'))),images:[...(newOnly?old.images:[]),...pending.map(x=>x.record)],exempt:old.exempt.filter(x=>x.path!=='company-mark.jpg')};
 for(const x of pending){fs.mkdirSync(path.dirname(x.target),{recursive:true});fs.writeFileSync(x.target,x.bytes);}
 fs.writeFileSync(manifestPath,JSON.stringify(manifest,null,2)+'\n');
 const legacy=path.join(root,'assets/company-mark.jpg');if(fs.existsSync(legacy))fs.unlinkSync(legacy);
 console.log(JSON.stringify({brand:manifest.brand,images:pending.length,legacyLogoRemoved:true}));
}
main().catch(e=>{console.error(e);process.exitCode=1});
