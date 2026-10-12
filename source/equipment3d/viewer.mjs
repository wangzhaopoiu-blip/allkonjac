import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {buildModel} from './model.mjs';

const language=window.EQUIPMENT_3D_LANGUAGE||new URLSearchParams(location.search).get('lang');
const lang=['en','th','id'].includes(language)?language:'en',t=window.EQUIPMENT_3D_UI[lang];
document.documentElement.lang=lang;document.title=t.name+' · ALL KONJAC';
for(const element of document.querySelectorAll('[data-text]'))element.textContent=t[element.dataset.text];
const host=document.getElementById('model-stage'),status=document.getElementById('status');
const messageOrigin=['null','file://'].includes(location.origin)?'*':location.origin;
const expectedParentOrigin=window.EQUIPMENT_3D_PARENT_ORIGIN||location.origin;
let renderer;
try{renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'low-power',preserveDrawingBuffer:true});}
catch(error){host.innerHTML='<img class="fallback-image" src="/assets/equipment3d/equipment01-poster.webp" alt="">';status.textContent=t.unavailable;window.equipment3D={ready:false,fallback:true};document.querySelectorAll('button').forEach(b=>b.disabled=true);parent.postMessage({type:'equipment-3d-fallback'},messageOrigin);}
if(renderer){
renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.setClearColor(0xf2f4f2);
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.shadowMap.autoUpdate=false;renderer.shadowMap.needsUpdate=true;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.92;
host.appendChild(renderer.domElement);renderer.domElement.tabIndex=0;
renderer.domElement.setAttribute('role','img');renderer.domElement.setAttribute('aria-label',t.canvas);
renderer.domElement.setAttribute('aria-describedby','keyboard-help');renderer.domElement.style.touchAction='none';
const scene=new THREE.Scene(),studio=new THREE.Scene(),pmrem=new THREE.PMREMGenerator(renderer);
studio.add(new THREE.Mesh(new THREE.BoxGeometry(12,9,12),new THREE.MeshBasicMaterial({color:new THREE.Color(.22,.24,.23),side:THREE.BackSide})));
function softbox(w,h,pos,power){const p=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({color:new THREE.Color(power,power,power),side:THREE.DoubleSide}));p.position.set(...pos);p.lookAt(0,.8,0);studio.add(p);}
softbox(6,1.7,[1,4,3],3.7);softbox(5,.7,[-4,2,-2],2.5);softbox(1.6,4,[4,1,-2],1.6);
softbox(6,.3,[0,3,-4],.05);softbox(3.5,4,[2,.3,4],1.8);softbox(4.5,1,[-1,.3,-4],1.5);
scene.environment=pmrem.fromScene(studio,.025).texture;
studio.traverse(o=>{if(o.isMesh){o.geometry.dispose();o.material.dispose();}});pmrem.dispose();
const spec=window.EQUIPMENT_3D_SPEC;spec.name=t.name;const model=buildModel(spec);scene.add(model);
const bounds=new THREE.Box3().setFromObject(model),size=bounds.getSize(new THREE.Vector3()),center=bounds.getCenter(new THREE.Vector3()),extent=Math.max(size.x,size.y,size.z);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(extent*8,extent*8),new THREE.ShadowMaterial({opacity:.12}));floor.rotation.x=-Math.PI/2;floor.position.y=bounds.min.y-.006;floor.receiveShadow=true;scene.add(floor);
scene.add(new THREE.HemisphereLight(0xffffff,0x656961,.7));
const fill=new THREE.DirectionalLight(0xf6fbff,2);fill.position.set(-4,3,-4);scene.add(fill);
const key=new THREE.DirectionalLight(0xffffff,2);key.position.set(3,6,2);key.castShadow=true;key.shadow.mapSize.set(1024,1024);
Object.assign(key.shadow.camera,{left:-4,right:4,top:4,bottom:-4,near:.1,far:16});key.shadow.bias=-.0002;key.shadow.normalBias=.02;scene.add(key);
const camera=new THREE.PerspectiveCamera(36,1,.02,extent*50);
const controls=new OrbitControls(camera,renderer.domElement);controls.target.copy(center);controls.enablePan=false;
controls.enableDamping=true;controls.dampingFactor=.09;controls.minDistance=extent*.55;controls.maxDistance=extent*6;controls.autoRotateSpeed=.8;
controls.minPolarAngle=.035;controls.maxPolarAngle=Math.PI-.08;
let dirty=true,baseDistance=extent*2.5,selected='overview',chosenAuto=false,visible=parent===window;
controls.addEventListener('change',()=>{dirty=true;});
function autoState(){controls.autoRotate=chosenAuto&&visible&&!document.hidden;const b=document.getElementById('auto');b.textContent=chosenAuto?t.pause:t.auto;b.setAttribute('aria-pressed',String(chosenAuto));}
function angles(yaw,elevation,distance){const damping=controls.enableDamping;controls.enableDamping=false;controls.update();camera.position.setFromSphericalCoords(distance,THREE.MathUtils.degToRad(90-elevation),THREE.MathUtils.degToRad(yaw)).add(controls.target);controls.update();controls.enableDamping=damping;dirty=true;}
function setView(id){const v=spec.views.find(v=>v.id===id)||spec.views[0];selected=v.id;chosenAuto=false;autoState();controls.target.copy(v.target?new THREE.Vector3(...v.target):center);angles(v.yaw,v.elevation,baseDistance*(v.distance_factor||1));
document.querySelectorAll('[data-view]').forEach(b=>{const active=b.dataset.view===selected;b.classList.toggle('selected',active);b.setAttribute('aria-pressed',String(active));});document.getElementById('view-label').textContent=t.views[selected];}
for(const v of spec.views){const b=document.createElement('button');b.type='button';b.dataset.view=v.id;b.textContent=t.views[v.id];b.addEventListener('click',()=>setView(v.id));document.getElementById('views').appendChild(b);}
document.getElementById('auto').addEventListener('click',()=>{chosenAuto=!chosenAuto;autoState();});
document.getElementById('reset').addEventListener('click',()=>setView('overview'));
renderer.domElement.addEventListener('pointerdown',()=>{chosenAuto=false;autoState();});
function zoom(factor){chosenAuto=false;autoState();const d=THREE.MathUtils.clamp(camera.position.distanceTo(controls.target)*factor,controls.minDistance,controls.maxDistance);camera.position.sub(controls.target).setLength(d).add(controls.target);controls.update();dirty=true;}
document.getElementById('zoom-in').addEventListener('click',()=>zoom(.84));document.getElementById('zoom-out').addEventListener('click',()=>zoom(1.18));
renderer.domElement.addEventListener('keydown',event=>{const current=new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target));let yaw=THREE.MathUtils.radToDeg(current.theta),pitch=90-THREE.MathUtils.radToDeg(current.phi),handled=true;
if(event.key==='ArrowLeft')yaw-=8;else if(event.key==='ArrowRight')yaw+=8;else if(event.key==='ArrowUp')pitch=Math.min(86,pitch+8);else if(event.key==='ArrowDown')pitch=Math.max(-70,pitch-8);else if(event.key==='+'||event.key==='='){zoom(.84);event.preventDefault();return;}else if(event.key==='-'){zoom(1.18);event.preventDefault();return;}else if(event.key==='0'){setView('overview');event.preventDefault();return;}else handled=false;
if(handled){event.preventDefault();chosenAuto=false;autoState();angles(yaw,pitch,current.radius);}});
function resize(){const b=host.getBoundingClientRect();if(!b.width||!b.height)return;renderer.setSize(b.width,b.height);camera.aspect=b.width/b.height;camera.updateProjectionMatrix();const prior=baseDistance;const vertical=THREE.MathUtils.degToRad(camera.fov)/2,horizontal=Math.atan(Math.tan(vertical)*camera.aspect);baseDistance=size.length()*.5/Math.sin(Math.min(vertical,horizontal))*1.10;
if(window.equipment3D?.ready){camera.position.sub(controls.target).multiplyScalar(baseDistance/prior).add(controls.target);controls.update();}dirty=true;}
new ResizeObserver(resize).observe(host);
document.addEventListener('visibilitychange',autoState);window.addEventListener('message',event=>{if(event.origin!==expectedParentOrigin||event.source!==parent)return;if(event.data?.type==='equipment-3d-visibility'){visible=!!event.data.visible;autoState();}});
function renderOnce(){renderer.render(scene,camera);dirty=false;}
const clock=new THREE.Clock();
const tick=()=>{controls.update(Math.min(clock.getDelta(),.08));if(visible&&!document.hidden&&(dirty||controls.autoRotate))renderOnce();requestAnimationFrame(tick);};
window.equipment3D={ready:false,model,camera,controls,bounds,setView,renderOnce,stats:()=>({parts:model.children.length,position:camera.position.toArray(),target:controls.target.toArray(),autoRotate:controls.autoRotate,view:selected})};
resize();setView('overview');chosenAuto=!matchMedia('(prefers-reduced-motion: reduce)').matches;autoState();renderOnce();window.equipment3D.ready=true;status.textContent=t.ready;tick();parent.postMessage({type:'equipment-3d-ready'},messageOrigin);
}
