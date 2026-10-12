import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

function roundedPath(path,w,h,r) {
  const x=-w/2,y=-h/2; r=Math.min(r,w/4,h/4);
  path.moveTo(x+r,y);path.lineTo(x+w-r,y);path.quadraticCurveTo(x+w,y,x+w,y+r);
  path.lineTo(x+w,y+h-r);path.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
  path.lineTo(x+r,y+h);path.quadraticCurveTo(x,y+h,x,y+h-r);
  path.lineTo(x,y+r);path.quadraticCurveTo(x,y,x+r,y);return path;
}

function hollowTube(width,depth,length,wall) {
  if(wall<=0||wall*2>=Math.min(width,depth))throw new Error('Invalid tube wall');
  const shape=roundedPath(new THREE.Shape(),width,depth,Math.min(width,depth)*.10);
  shape.holes.push(roundedPath(new THREE.Path(),width-wall*2,depth-wall*2,Math.min(width,depth)*.05));
  const g=new THREE.ExtrudeGeometry(shape,{depth:length,steps:1,bevelEnabled:false,curveSegments:3});
  g.translate(0,0,-length/2);g.rotateX(Math.PI/2);return g;
}

function panelGeometry(p) {
  if(p.points.length<3)throw new Error('Panel needs at least three points');
  const pts=p.points.map(v=>new THREE.Vector3(...v)),origin=pts[0];
  const u=pts[1].clone().sub(origin).normalize(),n=u.clone().cross(pts[2].clone().sub(origin)).normalize(),v=n.clone().cross(u);
  if(n.length()<.99)throw new Error('Degenerate panel: '+p.id);
  const project=q=>{const d=new THREE.Vector3(...q).sub(origin);if(Math.abs(d.dot(n))>1e-5)throw new Error('Nonplanar panel: '+p.id);return new THREE.Vector2(d.dot(u),d.dot(v));};
  const shape=new THREE.Shape(pts.map(q=>project(q.toArray())));
  for(const hole of p.holes||[]){const q=project(hole.center),h=new THREE.Path();h.absarc(q.x,q.y,hole.radius,0,Math.PI*2,true);shape.holes.push(h);}
  const thickness=p.thickness||.004,bevel=Math.min(p.bevel||0,thickness*.24);
  const g=new THREE.ExtrudeGeometry(shape,{depth:thickness,steps:1,curveSegments:12,bevelEnabled:bevel>0,bevelThickness:bevel,bevelSize:bevel,bevelSegments:2});
  g.translate(0,0,-thickness/2);g.applyMatrix4(new THREE.Matrix4().makeBasis(u,v,n));g.translate(...origin.toArray());return g;
}

function brushedMaps() {
  // Deterministic local grain; exported images are embedded in GLB.
  const w=128,h=512,normal=document.createElement('canvas'),rough=document.createElement('canvas');
  normal.width=rough.width=w;normal.height=rough.height=h;
  const nc=normal.getContext('2d'),rc=rough.getContext('2d'),ni=nc.createImageData(w,h),ri=rc.createImageData(w,h);
  let seed=94103;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)|0;return(seed>>>0)/4294967296;};
  for(let y=0;y<h;y++){const grain=(rnd()-.5)*5,shade=235+rnd()*20;for(let x=0;x<w;x++){const i=(y*w+x)*4;ni.data.set([128+(rnd()-.5),128+grain,255,255],i);ri.data.set([shade,shade,shade,255],i);}}
  nc.putImageData(ni,0,0);rc.putImageData(ri,0,0);
  const make=c=>{const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(2,3);return t;};
  return {normal:make(normal),roughness:make(rough)};
}

export function buildModel(spec) {
  if(spec.schema_version!==1||!Array.isArray(spec.parts)||!spec.parts.length)throw new Error('Invalid model specification');
  const root=new THREE.Group();root.name=spec.name||'Equipment';
  root.userData={provenance:spec.provenance,scale_status:spec.scale_status,uncertainties:spec.uncertainties,revision:spec.revision||'v001'};
  const materials={};let grain;
  for(const[name,params]of Object.entries(spec.materials)){
    const {finish,...p}=params;
    materials[name]=new THREE.MeshStandardMaterial({...p,side:THREE.DoubleSide});materials[name].name=name;
    if(finish==='brushed'){grain??=brushedMaps();materials[name].normalMap=grain.normal;materials[name].normalScale.set(.12,.12);materials[name].roughnessMap=grain.roughness;}
  }
  const ids=new Set();
  for(const p of spec.parts){
    if(ids.has(p.id))throw new Error('Duplicate part ID: '+p.id);ids.add(p.id);
    let geometry,position=p.position||[0,0,0],quaternion=null;
    if(p.type==='box')geometry=new THREE.BoxGeometry(...p.size);
    else if(p.type==='rounded_box')geometry=new RoundedBoxGeometry(...p.size,p.segments||1,Math.min(p.radius||.003,Math.min(...p.size)*.49));
    else if(p.type==='ellipsoid')geometry=new THREE.SphereGeometry(1,48,32);
    else if(p.type==='cylinder')geometry=new THREE.CylinderGeometry(p.radiusTop??p.radius,p.radius,p.length,p.segments||48);
    else if(p.type==='lathe')geometry=new THREE.LatheGeometry(p.profile.map(v=>new THREE.Vector2(...v)),p.segments||64);
    else if(p.type==='torus')geometry=new THREE.TorusGeometry(p.radius,p.tube,p.radialSegments||8,p.segments||48);
    else if(p.type==='beam'){
      const a=new THREE.Vector3(...p.from),b=new THREE.Vector3(...p.to),v=b.clone().sub(a),length=v.length();
      if(length<1e-8)throw new Error('Zero length beam: '+p.id);
      geometry=p.round?new THREE.CylinderGeometry(p.radius,p.radius,length,32):p.profile==='hollow_square'?hollowTube(p.width,p.depth||p.width,length,p.wall||.003):new THREE.BoxGeometry(p.width,length,p.depth||p.width);
      position=a.add(b).multiplyScalar(.5).toArray();quaternion=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());
    }else if(p.type==='panel')geometry=panelGeometry(p);
    else throw new Error('Unknown primitive '+p.type);
    if(!materials[p.material])throw new Error('Unknown material '+p.material);
    const mesh=new THREE.Mesh(geometry,materials[p.material]);mesh.name=p.id;
    mesh.position.fromArray(position);if(quaternion)mesh.quaternion.copy(quaternion);
    if(p.rotation)mesh.rotation.set(...p.rotation);if(p.scale)mesh.scale.fromArray(p.scale);
    mesh.castShadow=true;mesh.receiveShadow=true;
    mesh.userData={label:p.label||p.id,evidence:p.evidence||[],status:p.status||'reference_based',note:p.note||'',group:p.group||'main'};root.add(mesh);
  }
  root.updateMatrixWorld(true);const bounds=new THREE.Box3().setFromObject(root);if(bounds.isEmpty())throw new Error('Empty model');return root;
}
