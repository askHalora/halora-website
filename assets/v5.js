/* Halora v5 "The Pulse": opening intro + touchpoints that open into product modules.
   Vanilla JS. Content never depends on this file: without it the page shows the static layout. */
(function(){
var d=document,w=window,h=d.documentElement,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,r){return (r||d).querySelector(s)}function $$(s,r){return [].slice.call((r||d).querySelectorAll(s))}
function clamp(x){return x<0?0:x>1?1:x}
function ease(x){return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}
var rtl=h.dir==='rtl';

/* ===== The Pulse: once per session, skippable, off for reduced motion ===== */
(function(){
 var raw=d.body.getAttribute('data-pulse');var done=function(){h.classList.remove('pulse-pending')};
 if(!raw){done();return}
 var seen=false;try{seen=sessionStorage.getItem('hlPulse')==='1'}catch(e){}
 if(seen||rm){done();return}
 var D;try{D=JSON.parse(raw)}catch(e){done();return}
 try{sessionStorage.setItem('hlPulse','1')}catch(e){}
 var W=innerWidth,H=innerHeight,mob=W<700;
 var ly=Math.round(H*(mob?.5:.52)), hx=Math.round(W*(mob?.8:.8)), amp=Math.min(mob?70:110,H*.13);
 var bx=(mob?[.1,.3,.5,.68]:[.13,.29,.45,.61]).map(function(f){return Math.round(W*f)});
 var end=hx-58;
 /* heartbeat path: flat, then a P-QRS-T complex at each beat, ending in Noor's halo */
 var p='M0 '+ly;bx.forEach(function(x){p+=' L'+(x-40)+' '+ly+' Q'+(x-33)+' '+(ly-amp*.16)+' '+(x-26)+' '+ly+' L'+(x-9)+' '+ly+' L'+(x-5)+' '+(ly+amp*.2)+' L'+x+' '+(ly-amp)+' L'+(x+6)+' '+(ly+amp*.42)+' L'+(x+10)+' '+ly+' L'+(x+22)+' '+ly+' Q'+(x+33)+' '+(ly-amp*.28)+' '+(x+44)+' '+ly});p+=' L'+end+' '+ly;
 var mirror=function(x){return rtl?W-x:x};
 var DD=1.9,t0=.15,beatT=bx.map(function(x){return t0+DD*(x/end)}),iv=beatT[1]-beatT[0];
 var last=beatT[3]+1.15, ts=Math.max(2.9,last), th=ts-.2, to=ts-.25, tEnd=th+2;
 var el=d.createElement('div');el.id='pulse';el.setAttribute('role','dialog');el.setAttribute('aria-label',(D.h1+' '+D.h2));
 var hy=ly, sy=0;
 var tps='',bks='';
 D.tps.forEach(function(t,i){var x=mirror(bx[i]),y=ly-amp-38,cw=mob?150:180;x=Math.max(cw/2+8,Math.min(W-cw/2-8,x));
  var hxm=mirror(hx);tps+='<div class="tp" style="left:'+x+'px;top:'+y+'px;--t:'+beatT[i].toFixed(2)+'s;--dx:'+(hxm-x)+'px;--dy:'+(hy-y)+'px">'+t.ic+'<span><b>'+t.a+'</b><small>'+t.q+'</small></span></div>';
  bks+='<div class="pbk" style="--t:'+(beatT[i]+.75).toFixed(2)+'s"><em>'+D.ok+'</em><span>'+D.bk[i]+'</span></div>'});
 var bkX=Math.max(111,Math.min(W-111,mirror(hx))), bkY=hy+70;
 var hlTop=Math.round(H*(mob?.24:.2));
 el.innerHTML='<div class="grid"></div><svg class="ln" viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="none" aria-hidden="true"'+(rtl?' style="transform:scaleX(-1)"':'')+'><path d="'+p+'"/></svg>'+
  '<div class="nh" style="left:'+mirror(hx)+'px;top:'+hy+'px">'+D.mark+'</div>'+tps+
  '<div class="pbks" style="left:'+bkX+'px;top:'+bkY+'px">'+bks+'</div>'+
  '<div class="hl" style="top:'+hlTop+'px">'+D.h1+'<b>'+D.h2+'</b></div>'+
  '<button class="skip" type="button">'+D.skip+'</button>';
 d.body.appendChild(el);done();h.classList.add('pulse-on');
 var svg=$('svg.ln',el),path=$('path',svg),L=Math.ceil(path.getTotalLength());
 /* where the line settles: just under the headline */
 var hl=$('.hl',el),hb=hl.getBoundingClientRect().bottom;sy=Math.round(hb+46-ly);
 var st=el.style;st.setProperty('--L',L);st.setProperty('--dd',DD+'s');st.setProperty('--ly',ly+'px');st.setProperty('--sy',sy+'px');
 st.setProperty('--ts',ts+'s');st.setProperty('--th',th+'s');st.setProperty('--to',to+'s');st.setProperty('--hi',iv.toFixed(2)+'s');st.setProperty('--h0',(beatT[0]+.62).toFixed(2)+'s');
 if(rtl){svg.style.animation='none';svg.style.transformOrigin='50% '+ly+'px';setTimeout(function(){svg.style.transition='transform .8s cubic-bezier(.6,0,.2,1)';svg.style.transform='scaleX(-1) translateY('+sy+'px) scaleY(.38)'},ts*1000)}
 var fin=false,tm=[];
 function finish(){if(fin)return;fin=true;tm.forEach(clearTimeout);el.classList.add('out');h.classList.remove('pulse-on');setTimeout(function(){el.remove()},650);
  removeEventListener('keydown',key)}
 function key(e){if(e.key==='Escape'||e.key==='Enter'||e.key===' '){e.preventDefault();finish()}}
 el.addEventListener('click',finish);addEventListener('keydown',key);
 $('.skip',el).focus({preventScroll:true});
 tm.push(setTimeout(finish,tEnd*1000));
})();

/* ===== Touchpoints open into the product modules (sticky, scroll-driven) ===== */
(function(){
 var M=$('.mods');if(!M||rm||!('IntersectionObserver' in w)||!w.requestAnimationFrame)return;
 M.classList.add('anim');
 var pin=$('.pin',M),cards=$$('.mod',M),tps=$$('.tp',M),hub=$('.hub',M),from=[],on=false,queued=false,TP=[];
 function placeTps(){var mob=innerWidth<700,ox=mob?96:200,oy=mob?78:120;
  TP=[[-ox,-oy],[ox,-oy],[-ox,oy],[ox,oy]];if(rtl)TP=TP.map(function(v){return[-v[0],v[1]]});
  tps.forEach(function(t,i){t.style.transform='translate(-50%,-50%) translate('+TP[i][0]+'px,'+TP[i][1]+'px)'})}
 function measure(){placeTps();cards.forEach(function(c){c.style.transform='none'});
  var hr=hub.getBoundingClientRect(),hcx=hr.left+hr.width/2,hcy=hr.top+hr.height/2;
  from=cards.map(function(c){var r=c.getBoundingClientRect(),i=+c.getAttribute('data-from'),tx=hcx+TP[i][0],ty=hcy+TP[i][1];return[tx-(r.left+r.width/2),ty-(r.top+r.height/2)]});
  update()}
 function update(){queued=false;var r=M.getBoundingClientRect(),span=r.height-pin.offsetHeight,p=clamp(-r.top/(span||1));
  var tk=clamp((p-.06)/.22);
  tps.forEach(function(t,i){var k=clamp((p-.03-i*.02)/.1),o=k*(1-clamp((p-.3-i*.03)/.16));t.style.opacity=o.toFixed(3);
   t.style.transform='translate(-50%,-50%) translate('+TP[i][0]*(.4+.6*k)+'px,'+TP[i][1]*(.4+.6*k)+'px) scale('+(.8+.2*k).toFixed(3)+')'});
  var hk=clamp((p-.3)/.25);hub.style.opacity=(1-hk).toFixed(3);hub.style.transform='scale('+(1+.25*tk-.5*hk).toFixed(3)+')';
  cards.forEach(function(c,i){var k=ease(clamp((p-.3-i*.035)/.38)),f=from[i]||[0,0];
   c.style.opacity=k.toFixed(3);c.style.transform='translate('+(f[0]*(1-k)).toFixed(1)+'px,'+(f[1]*(1-k)).toFixed(1)+'px) scale('+(.22+.78*k).toFixed(3)+')';
   c.style.pointerEvents=k>.9?'':'none'})}
 function onScroll(){if(on&&!queued){queued=true;requestAnimationFrame(update)}}
 new IntersectionObserver(function(es){on=es[0].isIntersecting;if(on)onScroll()},{rootMargin:'100px 0px'}).observe(M);
 /* the floating ask bar would cover the cards while the section is pinned */
 new IntersectionObserver(function(es){d.body.classList.toggle('in-mods',es[0].isIntersecting)},{rootMargin:'-40% 0px -40% 0px'}).observe(M);
 addEventListener('scroll',onScroll,{passive:true});
 var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(measure,150)});
 /* keyboard users: a focused card is always fully visible */
 cards.forEach(function(c){c.addEventListener('focus',function(){var r=M.getBoundingClientRect();if(r.top>-M.offsetHeight*.75)scrollTo({top:scrollY+r.top+M.offsetHeight-pin.offsetHeight-2,behavior:'instant'})})});
 if(d.fonts&&d.fonts.ready)d.fonts.ready.then(measure);measure();
})();

/* ===== hero background: floating clay shapes drift with the pointer and scroll ===== */
(function(){
 var F=$$('.bgfx .fz');if(!F.length||rm)return;
 var fine=matchMedia('(pointer:fine)').matches,mx=0,my=0,q=false;
 var hero=F[0].closest('section');
 function draw(){q=false;var r=hero.getBoundingClientRect();if(r.bottom<0)return;var sy=Math.max(0,-r.top);
  F.forEach(function(f){var k=+f.getAttribute('data-depth')||10;f.style.transform='translate3d('+(mx*k).toFixed(1)+'px,'+(my*k-sy*k/60).toFixed(1)+'px,0)'})}
 function req(){if(!q){q=true;requestAnimationFrame(draw)}}
 if(fine)hero.addEventListener('mousemove',function(e){var r=hero.getBoundingClientRect();mx=(e.clientX-r.left)/r.width-.5;my=(e.clientY-r.top)/r.height-.5;req()});
 addEventListener('scroll',req,{passive:true});
})();

/* ===== phones: the chat pill appears only after the hero, above the sticky bar ===== */
(function(){var q=false;function u(){q=false;d.body.classList.toggle('past-hero',scrollY>innerHeight*.8)}
 addEventListener('scroll',function(){if(!q){q=true;requestAnimationFrame(u)}},{passive:true});u()})();

/* ===== mobile menu: correct position, closes on link / Esc / resize, state for assistive tech ===== */
var mb=$('.mbtn');
if(mb){var hd=$('header.top');
 function setTop(){if(hd)h.style.setProperty('--hb',Math.max(0,Math.round(hd.getBoundingClientRect().bottom))+'px')}
 function close(){if(!d.body.classList.contains('mopen'))return;d.body.classList.remove('mopen');mb.setAttribute('aria-expanded','false')}
 mb.addEventListener('click',function(){setTop();mb.setAttribute('aria-expanded',d.body.classList.contains('mopen')?'true':'false')});
 $$('.top nav a').forEach(function(a){a.addEventListener('click',close)});
 addEventListener('keydown',function(e){if(e.key==='Escape'&&d.body.classList.contains('mopen')){close();mb.focus()}});
 addEventListener('resize',function(){if(innerWidth>900)close();else setTop()});
}
})();
