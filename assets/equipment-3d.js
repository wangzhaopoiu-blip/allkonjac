document.querySelectorAll('[data-equipment-3d]').forEach(shell=>{
  const button=shell.querySelector('[data-load-3d]'),poster=shell.querySelector('.equipment-3d-poster'),frame=shell.querySelector('iframe'),state=shell.querySelector('[role=status]');
  const offlinePreview=location.protocol==='file:'&&!!frame.dataset.srcdoc;
  const expectedOrigin=offlinePreview?'null':location.origin;
  let loaded=false,inView=false,ready=false;button.hidden=true;
  function visibility(){if(ready)frame.contentWindow.postMessage({type:'equipment-3d-visibility',visible:inView},offlinePreview?'*':location.origin);}
  function load(){if(loaded)return;loaded=true;if(frame.dataset.srcdoc)frame.srcdoc=frame.dataset.srcdoc;else frame.src=frame.dataset.src;frame.hidden=false;state.hidden=false;shell.setAttribute('aria-busy','true');}
  button.addEventListener('click',load);
  window.addEventListener('message',event=>{if(event.origin!==expectedOrigin||event.source!==frame.contentWindow)return;if(['equipment-3d-ready','equipment-3d-fallback'].includes(event.data?.type)){ready=true;state.hidden=true;poster.hidden=true;shell.setAttribute('aria-busy','false');visibility();}});
  if('IntersectionObserver'in window)new IntersectionObserver(entries=>{for(const e of entries){inView=e.isIntersecting;visibility();}},{threshold:.04}).observe(shell);else inView=true;
  load();
});
