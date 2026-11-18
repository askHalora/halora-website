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

  try { localStorage.removeItem('noor_web_chat'); } catch (e) {}
  addEventListener('pagehide', function () { try { localStorage.removeItem('noor_web_chat'); } catch (e) {} });
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
    // Demo privacy: every visit starts a fresh, anonymous chat. Nothing from earlier visits is shown or reused,
    // and the demo ID is a test number, so no real booking is made and test data is cleaned from the system.
    try { localStorage.setItem('noor_web_chat', JSON.stringify({ name: ar ? 'زائر الموقع' : 'Website visitor', phone: '9715000009' + String(Math.floor(Math.random() * 9e4) + 1e4), log: [] })); } catch (e) {}
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
  var groups = ['.sec-h', '.cols > div', '.xf', '.xb', '.ledger tbody tr', '.tl > *', '.portal > *', '.mock', '.plans > *', '.plans-note', '.pilot > *', '.founder > *', '.faq details', 'section .list > li', 'footer .wrap > *'];
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
  var L = ar ? { st: 'متصلة الآن', hi: ['صباح الخير','مساء الخير','مساء الخير'][(function(){var x=+new Date().toLocaleString('en-US',{timeZone:'Asia/Dubai',hour:'numeric',hour12:false});return x<12?0:x<17?1:2;})()] + '، معك نور من عيادة برايت سمايل. كيف أقدر أساعدك؟', demo: 'عيادة تجريبية' }
               : { st: 'Online now', hi: ['Good morning','Good afternoon','Good evening'][(function(){var x=+new Date().toLocaleString('en-US',{timeZone:'Asia/Dubai',hour:'numeric',hour12:false});return x<12?0:x<17?1:2;})()] + ', this is Noor at BrightSmile Dental. How can I help you?', demo: 'Demo clinic' };
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

/* 1-minute voice demo: talk to Noor in the browser (ElevenLabs), auto-ends after 60s, max 3 tries per visitor per day. */
(function () {
  var d = document, ar = d.documentElement.lang === 'ar';
  var AGENT = 'agent_1601m7axax44ejb9ffwxa8t3gs2e', LIMIT = 60, MAXDAY = 3;
  var LIB = 'https://unpkg.com/@elevenlabs/client@1.32.1/dist/lib.iife.js';
  var T = ar ? { t: 'مكالمة تجريبية مع نور', pick: 'اختر لغة المكالمة', con: 'جارٍ الاتصال…', mic: 'اسمح باستخدام الميكروفون للبدء', lis: 'نور تستمع… تكلّم الآن', spk: 'نور تتكلم…', end: 'إنهاء المكالمة', done: 'انتهت المكالمة. أعجبتك؟', book: 'احجز مكالمة', pilot: 'ابدأ تجربة مجانية', close: 'إغلاق', left: 'ثانية متبقية', err: 'تعذّر الاتصال. تأكد من السماح بالميكروفون وحاول مرة أخرى.', lim: 'وصلت للحد اليومي للتجربة. احجز مكالمة لترى العرض كاملاً.', note: 'عيادة تجريبية. جرّب: «أبي أحجز تنظيف أسنان بكرة». لا تشارك معلومات صحية شخصية.' }
             : { t: 'Demo call with Noor', pick: 'Choose the call language', con: 'Connecting…', mic: 'Allow the microphone to start', lis: 'Noor is listening… go ahead and speak', spk: 'Noor is speaking…', end: 'End call', done: 'Call ended. Liked it?', book: 'Book a call', pilot: 'Start a free pilot', close: 'Close', left: 's left', err: 'Could not connect. Please allow the microphone and try again.', lim: "You've reached today's demo limit. Book a call to see the full demo.", note: 'Demo clinic. Try: "I\'d like to book a cleaning tomorrow." Please don\'t share personal health details.' };
  function load(cb) { if (window.ElevenLabsClient) return cb(); var s = d.createElement('script'); s.src = LIB; s.onload = function () { cb(); }; s.onerror = function () { cb(new Error('load')); }; d.head.appendChild(s); }
  function tries() { try { var o = JSON.parse(localStorage.getItem('hl_vd') || '{}'), k = new Date().toDateString(); return o.d === k ? o.n : 0; } catch (e) { return 0; } }
  function addTry() { try { var k = new Date().toDateString(); localStorage.setItem('hl_vd', JSON.stringify({ d: k, n: tries() + 1 })); } catch (e) {} }
  function open() {
    var C = 2 * Math.PI * 68, ov = d.createElement('div'); ov.className = 'vd'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true');
    ov.innerHTML = '<div class="vd-box"><div class="vd-ring"><svg viewBox="0 0 148 148"><circle class="bg" cx="74" cy="74" r="68"/><circle class="fg" cx="74" cy="74" r="68" stroke-dasharray="' + C + '" stroke-dashoffset="0"/></svg><div class="vd-av">' + (ar ? 'ن' : 'N') + '</div></div>' +
      '<h3>' + T.t + '</h3><p class="st"></p><div class="tm"></div><div class="acts"></div><p class="note">' + T.note + '</p></div>';
    d.body.appendChild(ov);
    var st = ov.querySelector('.st'), tm = ov.querySelector('.tm'), acts = ov.querySelector('.acts'), fg = ov.querySelector('.fg');
    var conv = null, timer = null, left = LIMIT, ended = false;
    function btn(txt, cls, fn, href) { var b = d.createElement(href ? 'a' : 'button'); b.className = 'btn ' + (cls || ''); b.textContent = txt; if (href) b.href = href; if (fn) b.onclick = fn; acts.appendChild(b); return b; }
    function close() { finish(); ov.remove(); }
    function finish(msg) {
      if (ended) return; ended = true; clearInterval(timer); ov.classList.remove('speaking');
      try { conv && conv.endSession(); } catch (e) {}
      st.textContent = msg || T.done; tm.textContent = ''; acts.innerHTML = '';
      btn(T.book, '', null, ar ? '/call/?lang=ar' : '/call/'); btn(T.pilot, 'line', function () { close(); }, '#pilot'); btn(T.close, 'line', close);
    }
    ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
    d.addEventListener('keydown', function esc(e) { if (e.key === 'Escape') { d.removeEventListener('keydown', esc); close(); } });
    if (tries() >= MAXDAY) { finish(T.lim); return; }
    // Step 1: the visitor chooses the call language.
    st.textContent = T.pick;
    btn('English', 'lang-btn', function () { go('en'); });
    btn('العربية', 'lang-btn', function () { go('ar'); });
    function go(lang) {
      acts.innerHTML = ''; st.textContent = T.mic; btn(T.close, 'line', close);
      var G = lang === 'ar'
        ? { first: 'أهلاً وسهلاً! معك نور من استقبال عيادة برايت سمايل. كيف أقدر أساعدك اليوم؟', ctx: 'The caller chose Arabic. Speak natural Gulf Arabic for the whole call unless the caller switches to English.' }
        : { first: "Hello! This is Noor from BrightSmile Dental reception. How can I help you today?", ctx: 'The caller chose English. Speak English for the whole call. Switch to Arabic only if the caller clearly speaks Arabic.' };
      load(function (err) {
        if (err || !window.ElevenLabsClient) return finish(T.err);
        start(true);
      });
      function start(withOverrides) {
        st.textContent = T.con;
        var connected = false, retried = false;
        var opts = {
          agentId: AGENT, connectionType: 'websocket',
          onConnect: function () {
            connected = true; addTry(); st.textContent = T.lis;
            setTimeout(function () { try { conv && conv.sendContextualUpdate(G.ctx); } catch (e) {} }, 250);
            acts.innerHTML = ''; btn(T.end, 'end', function () { finish(); });
            timer = setInterval(function () { left--; tm.textContent = left + ' ' + T.left; fg.setAttribute('stroke-dashoffset', String(C * (1 - left / LIMIT))); if (left <= 0) finish(); }, 1000);
            tm.textContent = left + ' ' + T.left;
          },
          onModeChange: function (m) { if (ended) return; var sp = m && m.mode === 'speaking'; ov.classList.toggle('speaking', sp); st.textContent = sp ? T.spk : T.lis; },
          onDisconnect: function () { if (ended) return; if (withOverrides && !retried && left > LIMIT - 4) { retried = true; clearInterval(timer); left = LIMIT; conv = null; start(false); return; } finish(); },
          onError: function () { if (ended) return; if (withOverrides && !retried && left > LIMIT - 4) { retried = true; clearInterval(timer); left = LIMIT; conv = null; start(false); return; } finish(T.err); }
        };
        // Ask the agent to open in the chosen language. If the agent doesn't allow this, we reconnect without it
        // and steer the language with a contextual message instead.
        if (withOverrides) opts.overrides = { agent: { language: lang, firstMessage: G.first } };
        window.ElevenLabsClient.Conversation.startSession(opts)
          .then(function (c) { conv = c; if (ended) { try { c.endSession(); } catch (e) {} } })
          .catch(function () { if (withOverrides && !retried) { retried = true; start(false); } else finish(T.err); });
      }
    }
  }
  d.querySelectorAll('[data-voice]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); open(); }); });
})();

/* Voice notes in the website chat: tap the mic to record (up to 60 s), tap again to send. Noor transcribes it and replies. */
(function () {
  var d = document, ar = d.documentElement.lang === 'ar';
  var URL_V = 'https://autova.app.n8n.cloud/webhook/noor-webchat-b218e111470c-voice';
  if (!window.MediaRecorder || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) return;
  var L = ar ? { rec: 'تسجيل… اضغط للإرسال', vn: 'رسالة صوتية', ty: 'نور تكتب...', no: 'اسمح للموقع باستخدام الميكروفون لإرسال رسالة صوتية.', er: 'مشكلة في الاتصال، حاول مرة أخرى.', mic: 'تسجيل رسالة صوتية' }
             : { rec: 'Recording · tap ■ to send', vn: 'Voice note', ty: 'Noor is typing...', no: 'Please allow microphone access to send a voice note.', er: 'Connection problem. Please try again.', mic: 'Record a voice note' };
  var css = '#nw-mic{flex:none;width:40px;height:40px;border-radius:50%;border:0;background:#E7EFED;color:#0E5C57;display:grid;place-items:center;cursor:pointer;margin-inline-end:6px;transition:background .2s,color .2s}' +
    '#nw-mic svg{width:19px;height:19px}#nw-mic.rec{background:#E5484D;color:#fff;animation:nwp 1.2s infinite}' +
    '@keyframes nwp{0%{box-shadow:0 0 0 0 rgba(229,72,77,.45)}100%{box-shadow:0 0 0 10px rgba(229,72,77,0)}}' +
    '.nw-vn{display:flex;align-items:center;gap:8px}.nw-vn i{font-style:normal;opacity:.75;font-size:12px}.nw-tr{display:block;font-size:12.5px;opacity:.8;margin-top:5px;font-style:italic}';
  var MIC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>';
  var STOP = '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="7" y="7" width="10" height="10" rx="2"/></svg>';
  var rec = null, chunks = [], started = 0, timer = null, ph = '';

  function st() { try { return JSON.parse(localStorage.getItem('noor_web_chat') || '{}'); } catch (e) { return {}; } }
  function bubble(cls, html) { var M = d.getElementById('nw-m'); var x = d.createElement('div'); x.className = 'nw-q ' + cls; x.innerHTML = html; M.appendChild(x); M.scrollTop = M.scrollHeight; return x; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function fmt(s) { return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); }

  function send(blob, secs) {
    var s = st();
    var me = bubble('nw-u', '<span class="nw-vn">🎙️ ' + L.vn + ' <i>' + fmt(secs) + '</i></span>');
    var fd = new FormData();
    fd.append('phone', s.phone || ''); fd.append('name', s.name || ''); fd.append('lang', ar ? 'ar' : 'en'); fd.append('page', location.href.slice(0, 200));
    fd.append('file', blob, 'voice.' + (/mp4|aac/.test(blob.type) ? 'm4a' : 'webm'));
    var t0 = Date.now(), later = function (f) { setTimeout(f, Math.max(0, 600 - (Date.now() - t0))); };
    fetch(URL_V, { method: 'POST', body: fd }).then(function (r) { return r.json(); }).then(function (j) { later(function () {
      if (j.transcript) me.insertAdjacentHTML('beforeend', '<span class="nw-tr">“' + esc(j.transcript) + '”</span>');
      bubble('nw-a', esc(j.reply || L.er));
    }); }).catch(function () { later(function () { bubble('nw-a', esc(L.er)); }); });
  }

  function stop(cancel) {
    clearInterval(timer);
    var b = d.getElementById('nw-mic'), i = d.getElementById('nw-i');
    if (b) { b.classList.remove('rec'); b.innerHTML = MIC; }
    if (i) { i.placeholder = ph; i.disabled = false; }
    if (rec && rec.state !== 'inactive') { rec._cancel = !!cancel; rec.stop(); }
  }

  function start() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
      chunks = []; started = Date.now();
      var type = ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4'].filter(function (t) { return MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(t); })[0];
      rec = type ? new MediaRecorder(stream, { mimeType: type }) : new MediaRecorder(stream);
      rec.ondataavailable = function (e) { if (e.data && e.data.size) chunks.push(e.data); };
      rec.onstop = function () {
        stream.getTracks().forEach(function (t) { t.stop(); });
        var secs = Math.max(1, Math.round((Date.now() - started) / 1000));
        if (!rec._cancel && chunks.length && secs >= 1) send(new Blob(chunks, { type: rec.mimeType || 'audio/webm' }), secs);
      };
      rec.start();
      var b = d.getElementById('nw-mic'), i = d.getElementById('nw-i');
      b.classList.add('rec'); b.innerHTML = STOP;
      ph = i.placeholder; i.value = ''; i.disabled = true;
      var tick = function () { var s = Math.round((Date.now() - started) / 1000); i.placeholder = fmt(s) + '  ' + L.rec; if (s >= 60) stop(false); };
      tick(); timer = setInterval(tick, 500);
    }).catch(function () { bubble('nw-a', esc(L.no)); });
  }

  function mount() {
    var f = d.getElementById('nw-f');
    if (!f || d.getElementById('nw-mic')) return !!f;
    var s = d.createElement('style'); s.textContent = css; d.head.appendChild(s);
    var b = d.createElement('button'); b.type = 'button'; b.id = 'nw-mic'; b.setAttribute('aria-label', L.mic); b.title = L.mic; b.innerHTML = MIC;
    b.onclick = function () { if (rec && rec.state === 'recording') stop(false); else start(); };
    var i = d.getElementById('nw-i'); f.insertBefore(b, i ? i.nextSibling : f.firstChild);
    return true;
  }
  if (!mount()) { var mo = new MutationObserver(function () { if (mount()) mo.disconnect(); }); mo.observe(d.body, { childList: true, subtree: true }); }
})();
