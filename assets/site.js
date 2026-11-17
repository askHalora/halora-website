/* Halora site: loads the live Noor chat only when a visitor asks for it (saves server runs), and sends the pilot form. */
(function () {
  var N8N = 'https://autova.app.n8n.cloud/webhook/';
  var root = document.documentElement, ar = root.lang === 'ar';
  // Every "Book a call" button opens Halora's own booking page (free slots from Ziad's Google Calendar).
  var CALL_URL = ar ? '/call/?lang=ar' : '/call/';
  document.querySelectorAll('[data-call]').forEach(function (a) { a.href = CALL_URL; });
  var T = ar
    ? { sending: 'جارٍ الإرسال…', ok: 'شكراً لك. سنتواصل معك على واتساب خلال 24 ساعة.', bad: 'يرجى مراجعة البيانات والمحاولة مرة أخرى.', net: 'تعذّر الاتصال. حاول مرة أخرى.', loading: 'جارٍ فتح المحادثة…' }
    : { sending: 'Sending…', ok: 'Thank you. We will message you on WhatsApp within 24 hours.', bad: 'Please check the form and try again.', net: 'Connection problem. Please try again.', loading: 'Opening the chat…' };

  var loaded = false, bar = document.getElementById('trybar');
  function clickOpen() {
    var b = document.getElementById('nw-b'); if (!b) return false;
    var p = document.getElementById('nw-p'); if (!p || !p.classList.contains('o')) b.click();
    return true;
  }
  window.openChat = function () {
    if (bar) bar.classList.add('hide');
    if (loaded) { clickOpen(); return; }
    loaded = true;
    var s = document.createElement('script');
    s.src = N8N + 'noor-webchat-b218e111470c';
    var d = document.body.dataset;
    if (d.chatClinic) s.setAttribute('data-clinic', d.chatClinic);
    if (d.chatHello) s.setAttribute('data-hello', d.chatHello);
    if (d.chatDemo) s.setAttribute('data-demo', d.chatDemo);
    if (d.chatColor) s.setAttribute('data-color', d.chatColor);
    if (ar) s.setAttribute('data-lang', 'ar');
    s.onload = function () { var n = 0; (function wait() { if (clickOpen() || n++ > 40) return; setTimeout(wait, 100); })(); };
    document.body.appendChild(s);
  };
  document.querySelectorAll('[data-chat]').forEach(function (el) { el.addEventListener('click', function (e) { e.preventDefault(); window.openChat(); }); });

  var f = document.getElementById('lf');
  if (f) f.onsubmit = function (e) {
    e.preventDefault();
    var m = document.getElementById('fmsg'), b = f.querySelector('button');
    b.disabled = true; m.textContent = T.sending;
    fetch(N8N + 'noor-ai-receptionist-lead', { method: 'POST', body: new URLSearchParams(new FormData(f)) })
      .then(function (r) { return r.json(); })
      .then(function (j) { b.disabled = false; m.textContent = j.ok ? T.ok : (j.error || T.bad); if (j.ok) f.reset(); })
      .catch(function () { b.disabled = false; m.textContent = T.net; });
  };
})();

/* Motion: scroll reveal, header state, progress bar, live chat replay, active nav. No libraries. */
(function () {
  var d = document, root = d.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.classList.add('js');
  requestAnimationFrame(function () { root.classList.add('ready'); });

  var top = d.querySelector('.top'), bar = d.createElement('div');
  bar.className = 'progress'; d.body.appendChild(bar);
  function onScroll() {
    var y = window.scrollY || 0, h = d.documentElement.scrollHeight - innerHeight;
    if (top) top.classList.toggle('scrolled', y > 8);
    bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  if (!('IntersectionObserver' in window) || reduce) { d.querySelectorAll('.log .ln,.log .sys').forEach(function (e) { e.classList.add('in'); }); return; }

  // reveal groups with a light stagger
  var groups = ['.sec-h', '.cols > div', '.ledger tbody tr', '.tl > *', '.portal > *', '.mock', '.plans > *', '.plans-note', '.pilot > *', '.founder > *', '.faq details', 'section .list > li', 'footer .wrap > *'];
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  groups.forEach(function (sel) {
    d.querySelectorAll(sel).forEach(function (el, i) {
      if (el.closest('.hero') || el.classList.contains('rv')) return;
      el.classList.add('rv'); el.style.setProperty('--d', Math.min(i % 6, 5) * 0.07 + 's'); io.observe(el);
    });
  });

  // WhatsApp example replays like a real conversation when it comes into view
  var log = d.querySelector('.log');
  if (log) {
    var items = [].slice.call(log.querySelectorAll('.ln,.sys')), typing = d.createElement('div');
    typing.className = 'typing'; typing.innerHTML = '<i></i><i></i><i></i>';
    var played = false;
    new IntersectionObserver(function (es, o) {
      if (!es[0].isIntersecting || played) return; played = true; o.disconnect();
      var t = 350;
      items.forEach(function (el) {
        var isNoor = el.classList.contains('n');
        if (isNoor) {
          setTimeout(function () { el.parentNode.insertBefore(typing, el); typing.classList.add('on'); }, t);
          t += 900;
        }
        setTimeout(function () { typing.classList.remove('on'); el.classList.add('in'); }, t);
        t += isNoor ? 700 : 600;
      });
    }, { threshold: 0.35 }).observe(log);
  }

  // highlight the nav item for the section in view
  var links = {}; d.querySelectorAll('.top nav a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  var so = new IntersectionObserver(function (es) {
    es.forEach(function (e) { var a = links[e.target.id]; if (a && e.isIntersecting) { for (var k in links) links[k].classList.remove('on'); a.classList.add('on'); } });
  }, { rootMargin: '-45% 0px -50% 0px' });
  Object.keys(links).forEach(function (id) { var s = d.getElementById(id); if (s) so.observe(s); });
})();

/* Chat feel: a warm, human-style receptionist look for the demo chat (avatar, online status, typing, timestamps). */
(function () {
  var d = document, ar = d.documentElement.lang === 'ar';
  var L = ar ? { st: 'متصلة الآن', hi: 'أهلاً وسهلاً! معك نور من استقبال العيادة 😊 كيف أقدر أساعدك اليوم؟ تقدر تسألني عن الأسعار أو المواعيد أو تحجز زيارة.', demo: 'عيادة تجريبية' }
               : { st: 'Online now', hi: "Hi there! I'm Noor from the front desk 😊 How can I help you today? Ask me about prices, opening hours, or book a visit.", demo: 'Demo clinic' };
  var css = '#nw-h{display:flex;align-items:center;gap:12px}#nw-h .nw-av{width:40px;height:40px;border-radius:50%;flex:none;position:relative;display:grid;place-items:center;font-weight:600;font-size:17px;color:#0E5C57;background:linear-gradient(145deg,#f6ecd6,#e7d3a8)}' +
    '#nw-h .nw-av:after{content:"";position:absolute;right:0;bottom:1px;width:11px;height:11px;border-radius:50%;background:#25D366;border:2px solid #0E5C57}' +
    '#nw-h small .nw-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#25D366;margin-inline-end:6px;vertical-align:1px}' +
    '#nw-m .nw-a{position:relative}#nw-m .nw-time{display:block;font-size:10.5px;opacity:.55;margin-top:4px;text-align:end}' +
    '.nw-typing{display:inline-flex;gap:4px;padding:12px 14px;background:#fff;border-radius:16px;margin:4px 0;box-shadow:0 1px 1px rgba(0,0,0,.04)}' +
    '.nw-typing i{width:7px;height:7px;border-radius:50%;background:#0E5C57;opacity:.3;animation:nwT 1s infinite}.nw-typing i:nth-child(2){animation-delay:.15s}.nw-typing i:nth-child(3){animation-delay:.3s}' +
    '@keyframes nwT{0%,80%,100%{opacity:.25;transform:none}40%{opacity:1;transform:translateY(-3px)}}' +
    '#nw-m>div{animation:nwIn .3s ease both}@keyframes nwIn{from{opacity:0;transform:translateY(6px)}}';
  function now() { var t = new Date(); return ('0' + t.getHours()).slice(-2) + ':' + ('0' + t.getMinutes()).slice(-2); }
  function stamp(el) { if (el.querySelector('.nw-time')) return; var s = d.createElement('span'); s.className = 'nw-time'; s.textContent = now(); el.appendChild(s); }
  function enhance(p) {
    if (p.dataset.human) return; p.dataset.human = '1';
    var st = d.createElement('style'); st.textContent = css; d.head.appendChild(st);
    var h = p.querySelector('#nw-h'), info = h && h.querySelector('div'), b = info && info.querySelector('b'), sm = info && info.querySelector('small');
    if (h && info) {
      var av = d.createElement('div'); av.className = 'nw-av'; av.textContent = ar ? 'ن' : 'N'; h.insertBefore(av, info);
      var clinic = (b.textContent || '').replace(/\s*\(demo\)\s*/i, '').trim();
      b.textContent = (ar ? 'نور · ' : 'Noor · ') + clinic;
      sm.innerHTML = '<span class="nw-dot"></span>' + L.st + ' · ' + L.demo;
    }
    var m = p.querySelector('#nw-m'); if (!m) return;
    var first = m.querySelector('.nw-a'); if (first) { first.textContent = L.hi; stamp(first); }
    var typing = d.createElement('div'); typing.className = 'nw-typing'; typing.innerHTML = '<i></i><i></i><i></i>';
    new MutationObserver(function (ms) {
      ms.forEach(function (mu) {
        [].forEach.call(mu.addedNodes, function (n) {
          if (n.nodeType !== 1 || n === typing || !n.classList.contains('nw-q')) return;
          stamp(n);
          if (n.classList.contains('nw-a')) { if (typing.parentNode) typing.remove(); }
          else { setTimeout(function () { m.appendChild(typing); m.scrollTop = m.scrollHeight; }, 350); }
        });
      });
    }).observe(m, { childList: true });
  }
  var mo = new MutationObserver(function () { var p = d.getElementById('nw-p'); if (p) enhance(p); });
  mo.observe(d.body, { childList: true, subtree: true });
})();
