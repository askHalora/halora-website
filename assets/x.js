/* Halora v4 interactions. Vanilla, no dependencies. */
(function(){
var d=document,w=window,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,r){return (r||d).querySelector(s)}function $$(s,r){return [].slice.call((r||d).querySelectorAll(s))}
/* ===== opening intro (once per session, home pages only) ===== */
(function(){var tg=d.body.getAttribute('data-intro');var hp=function(){d.documentElement.classList.remove('intro-pending')};if(tg===null){hp();return}var seen=false;try{seen=sessionStorage.getItem('hlIntro')==='1'}catch(e){}
 if(seen||rm){hp();return}
 var L='Halora'.split('').map(function(ch,i){return '<span style="animation-delay:'+(1.75+i*.07)+'s">'+ch+'</span>'}).join('')+'<span style="animation-delay:2.2s"><i>.</i></span>';
 var it=d.createElement('div');it.id='intro';it.setAttribute('aria-hidden','true');
 it.innerHTML='<div class="au"></div><canvas></canvas><div class="c"><div class="mk"><svg viewBox="0 0 64 64"><rect class="sq" x="1" y="1" width="62" height="62" rx="15"/><path class="ar" d="M19.5 23.5Q32 12.5 44.5 23.5" fill="none" stroke="#D9A441" stroke-width="5.2" stroke-linecap="round"/><path class="hh" d="M22.5 29v21M41.5 29v21M22.5 39.5h19" fill="none" stroke="#F3F5F2" stroke-width="6.2" stroke-linecap="round"/></svg></div><div class="wd" dir="ltr">'+L+'</div><div class="tg">'+tg+'</div></div><div class="sk">'+(d.documentElement.lang==='ar'?'اضغط للتخطي':'Tap to skip')+'</div>';
 d.body.appendChild(it);hp();try{sessionStorage.setItem('hlIntro','1')}catch(e){}
 d.documentElement.classList.add('intro-on');
 var done=false;function end(){if(done)return;done=true;it.classList.add('out');d.documentElement.classList.remove('intro-on');setTimeout(function(){it.remove()},1100)}
 it.addEventListener('click',end);addEventListener('keydown',end,{once:true});
 /* particles converge into the mark */
 var c=it.querySelector('canvas'),x=c.getContext('2d'),dpr=Math.min(2,w.devicePixelRatio||1),W,H,P=[];
 function sz(){W=c.width=innerWidth*dpr;H=c.height=innerHeight*dpr}sz();
 var cols=['#7ff0df','#e0b34f','#c9b8ff','#3ddc84','#f59ac0'];
 for(var i=0;i<160;i++){var a=Math.random()*6.283,r=Math.max(W,H)*(.45+Math.random()*.5);P.push({a:a,r:r,r0:r,s:.012+Math.random()*.02,c:cols[i%5],z:(Math.random()*1.6+.6)*dpr,dl:Math.random()*.5})}
 var t0=performance.now();
 function f(t){var e=(t-t0)/1000;x.clearRect(0,0,W,H);var cx=W/2,cy=H/2-30*dpr;
  for(var i=0;i<P.length;i++){var p=P[i],k=Math.max(0,Math.min(1,(e-p.dl)/1.25));k=k*k*(3-2*k);var rr=p.r0*(1-k)+(k>=1?0:0);p.a+=p.s*(1-k*.6);
   var px=cx+Math.cos(p.a)*rr,py=cy+Math.sin(p.a)*rr*.82;x.globalAlpha=k<1?.9:Math.max(0,1-(e-p.dl-1.25)*3);x.fillStyle=p.c;x.beginPath();x.arc(px,py,p.z*(1-k*.4),0,6.283);x.fill();
   if(k>.05&&k<1){x.globalAlpha=.18;x.strokeStyle=p.c;x.lineWidth=p.z*.6;x.beginPath();x.moveTo(px,py);var b=p.a-p.s*6;x.lineTo(cx+Math.cos(b)*rr*1.04,cy+Math.sin(b)*rr*.82*1.04);x.stroke()}}
  if(!done&&e<3.4)requestAnimationFrame(f)}
 requestAnimationFrame(f);
 setTimeout(end,3300);
})();


/* header over dark hero */
if($('.hx,.ph')){d.body.classList.add('dark-top');var onS=function(){d.body.classList.toggle('scrolled',scrollY>($('.hx,.ph').offsetHeight-90))};addEventListener('scroll',onS,{passive:true});onS();}

/* starfield */
$$('canvas.stars').forEach(function(c){var x=c.getContext('2d'),S=[],dpr=Math.min(2,w.devicePixelRatio||1);
 function sz(){c.width=c.offsetWidth*dpr;c.height=c.offsetHeight*dpr;S=[];var n=Math.round(c.offsetWidth*c.offsetHeight/5200);for(var i=0;i<n;i++)S.push({x:Math.random()*c.width,y:Math.random()*c.height,r:(Math.random()*1.1+.2)*dpr,p:Math.random()*6.28,s:.4+Math.random()*1.2})}
 sz();addEventListener('resize',sz);
 /* only animate while the canvas is on screen and the tab is visible */
 var vis=true,run=false;function f(t){run=false;x.clearRect(0,0,c.width,c.height);for(var i=0;i<S.length;i++){var s=S[i],a=.25+.6*Math.abs(Math.sin(s.p+t/1000*s.s));x.globalAlpha=a;x.fillStyle='#e8fff9';x.beginPath();x.arc(s.x,s.y,s.r,0,6.28);x.fill()}if(!rm&&vis&&!d.hidden)go()}
 function go(){if(!run){run=true;requestAnimationFrame(f)}}
 if('IntersectionObserver' in w)new IntersectionObserver(function(es){vis=es[0].isIntersecting;if(vis)go()}).observe(c);
 d.addEventListener('visibilitychange',function(){if(!d.hidden&&vis)go()});
 go();});

/* rotating word */
$$('.rot').forEach(function(r){var s=$$('span',r),i=0;if(s.length<2||rm)return;setInterval(function(){s[i].classList.remove('on');s[i].classList.add('out');var o=s[i];setTimeout(function(){o.classList.remove('out')},700);i=(i+1)%s.length;s[i].classList.add('on')},2400)});

/* live Dubai clock + ticker */
var clk=$('[data-dxb]'),tk=$('[data-tick]');
if(clk){var T=function(){var n=new Date(Date.now()+(new Date().getTimezoneOffset()+240)*6e4);clk.textContent=('0'+n.getHours()).slice(-2)+':'+('0'+n.getMinutes()).slice(-2)+' '+(clk.getAttribute('data-dxb')||'Dubai')};T();setInterval(T,15e3)}
if(tk){var L=tk.getAttribute('data-tick').split('|'),k=0;setInterval(function(){k=(k+1)%L.length;tk.style.opacity=0;setTimeout(function(){tk.textContent=L[k];tk.style.opacity=1},300)},3200);tk.style.transition='opacity .3s'}

/* hero story: bubble -> booking card */
var st=$('.stage');
if(st){var B=$('.bubble',st),K=$('.bk',st),P=JSON.parse(st.getAttribute('data-story')||'[]'),j=0;
 function step(){if(!P.length)return;var p=P[j%P.length];B.classList.remove('on');K.classList.remove('on');
  setTimeout(function(){B.innerHTML=p.q+'<small>'+p.ch+' · '+p.t+'</small>';B.style.top=p.y+'%';B.classList.add('on')},350);
  setTimeout(function(){K.innerHTML='<i>✓</i><div><b>'+p.b+'</b><small>'+p.s+'</small></div>';K.style.top='66%';K.classList.add('on')},1900);
  j++}
 step();if(!rm)setInterval(step,4600);
 /* subtle parallax */
 if(!rm&&matchMedia('(pointer:fine)').matches){var hx=$('.hx');hx&&hx.addEventListener('mousemove',function(e){var r=hx.getBoundingClientRect(),dx=(e.clientX-r.left)/r.width-.5,dy=(e.clientY-r.top)/r.height-.5;st.style.transform='rotateY('+dx*8+'deg) rotateX('+(-dy*8)+'deg)'});st.style.transition='transform .4s ease-out';st.parentNode.style.perspective='1200px'}
}

/* count-up */
function cu(el){var to=+el.getAttribute('data-to'),pre=el.getAttribute('data-pre')||'',suf=el.getAttribute('data-suf')||'',t0=null;function f(t){t0=t0||t;var p=Math.min(1,(t-t0)/1400),v=Math.round(to*(1-Math.pow(1-p,3)));el.textContent=pre+v.toLocaleString('en-US')+suf;if(p<1)requestAnimationFrame(f)}rm?el.textContent=pre+to.toLocaleString('en-US')+suf:requestAnimationFrame(f)}

/* reveal */
var io='IntersectionObserver' in w?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');$$('[data-to]',e.target).forEach(cu);io.unobserve(e.target)}})},{threshold:.15}):null;
$$('.rv').forEach(function(e,i){if(io)io.observe(e);else e.classList.add('in')});

/* tilt cards */
if(!rm&&matchMedia('(pointer:fine)').matches)$$('.bc,.tilt').forEach(function(c){c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(900px) rotateY('+x*6+'deg) rotateX('+(-y*6)+'deg) translateY(-4px)'});c.addEventListener('mouseleave',function(){c.style.transform=''})});

/* night shift (sticky scroll) */
var ns=$('.ns');
if(ns){var ck=$('.clock b',ns),evs=$$('.ev',ns),bg=$('.bg',ns),moon=$('.moon',ns),cn=$$('.cnt b',ns);
 var tot=[+cn[0].getAttribute('data-n'),+cn[1].getAttribute('data-n'),+cn[2].getAttribute('data-n')];
 function u(){var r=ns.getBoundingClientRect(),p=Math.max(0,Math.min(1,-r.top/(r.height-innerHeight)));
  var m=18*60+p*15*60,h=Math.floor(m/60)%24,mi=Math.floor(m%60);ck.textContent=('0'+h).slice(-2)+':'+('0'+mi).slice(-2);
  evs.forEach(function(e,i){e.classList.toggle('on',p>=i/evs.length*.92)});
  cn.forEach(function(c,i){c.textContent=Math.round(tot[i]*p)});
  var dawn=Math.max(0,(p-.75)/.25);bg.style.background='linear-gradient(180deg,rgb('+Math.round(6+40*dawn)+','+Math.round(22+50*dawn)+','+Math.round(21+60*dawn)+'),rgb('+Math.round(11+170*dawn)+','+Math.round(35+95*dawn)+','+Math.round(33+40*dawn)+'))';
  moon.style.transform='translate('+p*82+'vw,'+(-Math.sin(p*3.14)*4)+'vh)';moon.style.opacity=1-dawn}
 addEventListener('scroll',u,{passive:true});u()}

/* specialties tabs with animated chat */
var spw=$('[data-sp]');
if(spw){var SP=JSON.parse(spw.getAttribute('data-sp')),tabs=$$('.sp-tabs button'),ms=$('.phone .ms'),nm=$('.phone .bar b'),info=$('.sp .info'),tm=[];
 function show(k){tm.forEach(clearTimeout);tm=[];var s=SP[k];tabs.forEach(function(t){t.classList.toggle('on',t.getAttribute('data-k')===k)});
  nm.textContent=s.clinic;info.innerHTML='<span class="label">'+s.label+'</span><h3>'+s.title+'</h3><p style="color:var(--ink-2);margin:0">'+s.text+'</p><ul>'+s.pts.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ul><p style="margin:22px 0 0"><a class="bx dark" href="'+s.href+'">'+(s.cta||('See '+s.name+' page →'))+'</a></p>';
  ms.innerHTML='';var at=200;s.chat.forEach(function(c){var who=c[0],txt=c[1];if(who==='n'){tm.push(setTimeout(function(){var ty=d.createElement('div');ty.className='ty';ty.innerHTML='<b></b><b></b><b></b>';ms.appendChild(ty);setTimeout(function(){ty.remove()},700)},at));at+=750}
   tm.push(setTimeout(function(){var e=d.createElement('div');if(who==='c'){e.className='chip'}else{e.className='w '+who+(txt==='~voice'?' v':'')}e.innerHTML=txt==='~voice'?'▶ <i></i> 0:07':txt;ms.appendChild(e);while(ms.children.length>9)ms.removeChild(ms.firstChild)},at));at+=who==='p'?900:1100})}
 tabs.forEach(function(t){t.addEventListener('click',function(){show(t.getAttribute('data-k'))})});
 var started=false;if(io){var io2=new IntersectionObserver(function(es){if(es[0].isIntersecting&&!started){started=true;show(tabs[0].getAttribute('data-k'))}},{threshold:.3});io2.observe(spw)}else show(tabs[0].getAttribute('data-k'))}

/* ROI calculator */
var roi=$('.roi');
if(roi){var inp=$$('input',roi);function calc(){var v={};inp.forEach(function(i){v[i.name]=+i.value;var o=$('[data-o="'+i.name+'"]',roi);if(o)o.textContent=(i.name==='val'?'$':'')+(+i.value).toLocaleString('en-US')+(i.name==='miss'?'%':'')});
 var lost=Math.round(v.msg*4.3*v.miss/100),won=Math.round(lost*.3),rev=won*v.val;
 $('[data-r=lost]',roi).textContent=lost.toLocaleString('en-US');$('[data-r=won]',roi).textContent=won.toLocaleString('en-US');$('[data-r=rev]',roi).textContent='$'+rev.toLocaleString('en-US');$('[data-r=x]',roi).textContent=(rev/299).toFixed(1)+'×'}
 inp.forEach(function(i){i.addEventListener('input',calc)});calc()}

/* ask bar */
var ab=$('.askbar');
if(ab){var shown=false,closed=false;try{closed=sessionStorage.getItem('hlAskX')==='1'}catch(e){}
 var tb=$('#trybar');if(tb)tb.style.display='none';
 addEventListener('scroll',function(){if(closed)return;var on=scrollY>innerHeight*.9;if(on!==shown){shown=on;ab.classList.toggle('on',on)}},{passive:true});
 $('.x',ab).addEventListener('click',function(e){e.stopPropagation();closed=true;ab.classList.remove('on');try{sessionStorage.setItem('hlAskX','1')}catch(e){}if(tb)tb.style.display=''});
 $$('.chips button',ab).forEach(function(b){b.addEventListener('click',function(){if(w.openChat)w.openChat();var q=b.textContent;setTimeout(function(){var i=d.querySelector('#hl-chat input,#hl-chat textarea,.hc-in input,.hc-in textarea,[data-chat-input]');if(i){i.value=q;i.focus();i.dispatchEvent(new Event('input',{bubbles:true}))}},500)})})}

/* mobile menu */
var mb=$('.mbtn');if(mb)mb.addEventListener('click',function(){d.body.classList.toggle('mopen')});

/* explainer video popup: built on first click, so the 6 MB video never loads unless asked for */
var vb=$$('[data-video]');
if(vb.length){var ar=d.documentElement.lang==='ar',vm,vv,last;
 function build(){vm=d.createElement('div');vm.id='hl-video';vm.setAttribute('role','dialog');vm.setAttribute('aria-modal','true');vm.setAttribute('aria-label',ar?'فيديو هالورا':'Halora demo video');
  vm.innerHTML='<div class="box"><button class="cl" type="button" aria-label="'+(ar?'إغلاق الفيديو':'Close video')+'">×</button><video controls playsinline preload="none" poster="/assets/halora-explainer-poster.jpg"></video></div>';
  d.body.appendChild(vm);vv=$('video',vm);
  vm.addEventListener('click',function(e){if(e.target===vm)close()});$('.cl',vm).addEventListener('click',close);
  vm.addEventListener('keydown',function(e){if(e.key==='Tab'){var f=[$('.cl',vm),vv];var i=f.indexOf(d.activeElement);e.preventDefault();f[(i+(e.shiftKey?f.length-1:1))%f.length].focus()}})}
 function open(src){if(!vm)build();last=d.activeElement;if(!vv.getAttribute('src'))vv.src=src;vv.muted=false;vv.volume=1;
  vm.classList.add('on');d.documentElement.classList.add('vid-open');$('.cl',vm).focus();var p=vv.play();if(p&&p.catch)p.catch(function(){})}
 function close(){if(!vm||!vm.classList.contains('on'))return;vv.pause();vm.classList.remove('on');d.documentElement.classList.remove('vid-open');if(last&&last.focus)last.focus()}
 vb.forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();open(b.getAttribute('href'))})});
 d.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
 w.closeHaloraVideo=close}
})();
