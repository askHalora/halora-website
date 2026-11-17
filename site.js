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
