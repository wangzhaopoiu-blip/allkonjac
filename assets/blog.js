const menuButton=document.querySelector('.menu-button');
const siteNav=document.querySelector('.site-nav');
if(menuButton&&siteNav){
  menuButton.addEventListener('click',()=>{
    const open=menuButton.getAttribute('aria-expanded')!=='true';
    menuButton.setAttribute('aria-expanded',String(open));
    siteNav.classList.toggle('open',open);
  });
  siteNav.addEventListener('click',event=>{
    if(event.target.closest('a')){siteNav.classList.remove('open');menuButton.setAttribute('aria-expanded','false');}
  });
}
const progress=document.querySelector('.reading-progress');
if(progress){
  const update=()=>{
    const max=document.documentElement.scrollHeight-innerHeight;
    progress.style.width=`${max>0?Math.min(100,Math.max(0,scrollY/max*100)):0}%`;
  };
  addEventListener('scroll',update,{passive:true});
  addEventListener('resize',update);
  update();
}
const tocLinks=[...document.querySelectorAll('.toc-panel a[href^="#section-"]')];
if(tocLinks.length&&'IntersectionObserver' in window){
  const observer=new IntersectionObserver(entries=>{
    for(const entry of entries){
      if(entry.isIntersecting){
        tocLinks.forEach(link=>link.classList.toggle('active',link.hash===`#${entry.target.id}`));
      }
    }
  },{rootMargin:'-110px 0px -68% 0px',threshold:0});
  document.querySelectorAll('h2[id^="section-"]').forEach(heading=>observer.observe(heading));
}
