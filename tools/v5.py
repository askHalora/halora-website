"""Halora v5 "The Pulse": light clinic look. Shared by build.py, build_ar.py and pages.py.
Pure functions only (no file writes), so it can be imported from anywhere."""
import html, json

E = lambda s: html.escape(s, quote=True)

# ---------- soft 3D "clay" icons (64x64 glyphs, white on a puffy coloured tile) ----------
GLYPH = {
 'tooth': '<path d="M21 17c4-3 7.5-1.5 11-1.5s7-1.5 11 1.5c4 3 4 9.5 2 14.5-1.7 4.3-2 9-3.2 13-.9 3-4.3 3-5.2 0l-1.9-6.6c-.8-2.4-4.6-2.4-5.4 0L26.4 44.5c-.9 3-4.3 3-5.2 0-1.2-4-1.5-8.7-3.2-13-2-5-2-11.5 3-14.5z" fill="#fff"/>',
 'heart': '<path d="M32 48S15 38.5 15 26.5a8.5 8.5 0 0 1 17-3 8.5 8.5 0 0 1 17 3C49 38.5 32 48 32 48z" fill="#fff"/>',
 'chat': '<path d="M15 23a8 8 0 0 1 8-8h18a8 8 0 0 1 8 8v11a8 8 0 0 1-8 8H30l-8.5 6.5V42H23a8 8 0 0 1-8-8z" fill="#fff"/><circle cx="25" cy="28.5" r="2.6" fill="var(--c)"/><circle cx="32" cy="28.5" r="2.6" fill="var(--c)"/><circle cx="39" cy="28.5" r="2.6" fill="var(--c)"/>',
 'phone': '<path d="M23.5 15c1.6 0 2.6.9 3.3 2.5l2.4 5.6c.6 1.5.3 2.8-.9 3.8l-2.6 2.2c1.9 4 5.2 7.3 9.2 9.2l2.2-2.6c1-1.2 2.3-1.5 3.8-.9l5.6 2.4c1.6.7 2.5 1.7 2.5 3.3v4.3c0 2.5-2 4.4-4.5 4.2C29 47.9 16.1 35 15 19.5c-.2-2.5 1.7-4.5 4.2-4.5z" fill="#fff"/>',
 'cal': '<rect x="15" y="18" width="34" height="30" rx="7" fill="#fff"/><path d="M15 25a7 7 0 0 1 7-7h20a7 7 0 0 1 7 7v2H15z" fill="var(--c)" opacity=".35"/><rect x="22" y="13" width="4.5" height="10" rx="2.25" fill="#fff"/><rect x="37.5" y="13" width="4.5" height="10" rx="2.25" fill="#fff"/><path d="M25 37.5l4.5 4.5 9.5-9.5" fill="none" stroke="var(--c)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
 'steth': '<g fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"><path d="M20 15v9a9 9 0 0 0 18 0v-9"/><path d="M29 33v4a9 9 0 0 0 18 0v-3"/></g><circle cx="47" cy="30" r="5.5" fill="#fff"/><circle cx="47" cy="30" r="2" fill="var(--c)"/>',
 'star': '<path d="M32 14l5.3 10.8 11.9 1.7-8.6 8.4 2 11.8L32 41.1l-10.6 5.6 2-11.8-8.6-8.4 11.9-1.7z" fill="#fff" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>',
 'bell': '<path d="M32 14a11 11 0 0 1 11 11v8l4 6H17l4-6v-8a11 11 0 0 1 11-11z" fill="#fff"/><circle cx="32" cy="44" r="4.5" fill="#fff"/>',
 'mega': '<path d="M16 28v8a3 3 0 0 0 3 3h4l13 8V17l-13 8h-4a3 3 0 0 0-3 3z" fill="#fff"/><path d="M42 26a8 8 0 0 1 0 12" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>',
 'dash': '<rect x="14" y="16" width="36" height="32" rx="6" fill="#fff"/><rect x="20" y="34" width="5" height="9" rx="2" fill="var(--c)"/><rect x="29" y="28" width="5" height="15" rx="2" fill="var(--c)"/><rect x="38" y="23" width="5" height="20" rx="2" fill="var(--c)"/>',
 'web': '<rect x="12" y="17" width="32" height="26" rx="5" fill="#fff"/><path d="M12 23h32" stroke="var(--c)" stroke-width="2.5" opacity=".5"/><rect x="37" y="27" width="15" height="24" rx="4" fill="#fff" stroke="var(--c)" stroke-width="2.5"/><circle cx="44.5" cy="46" r="1.6" fill="var(--c)"/>',
 'shield': '<path d="M32 13l15 6v11c0 9.5-6.4 16-15 20-8.6-4-15-10.5-15-20V19z" fill="#fff"/><path d="M25 31.5l5 5 9-9" fill="none" stroke="var(--c)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
 'plug': '<path d="M25 14v9M39 14v9" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/><path d="M19 23h26v6a13 13 0 0 1-26 0z" fill="#fff"/><path d="M32 42v8" stroke="#fff" stroke-width="5" stroke-linecap="round"/>',
 'route': '<circle cx="19" cy="19" r="5.5" fill="#fff"/><circle cx="45" cy="45" r="5.5" fill="#fff"/><path d="M24 19h13a7 7 0 0 1 0 14H27a7 7 0 0 0 0 14h12" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/>',
 'scale': '<path d="M32 15v32M22 48h20M17 21h30" stroke="#fff" stroke-width="4" stroke-linecap="round"/><path d="M17 23l-6 11a6 6 0 0 0 12 0zM47 23l-6 11a6 6 0 0 0 12 0z" fill="#fff"/>',
 'mic': '<rect x="25" y="13" width="14" height="24" rx="7" fill="#fff"/><path d="M19 31a13 13 0 0 0 26 0M32 44v6" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>',
 'globe': '<circle cx="32" cy="32" r="16" fill="#fff"/><path d="M16 32h32M32 16c5 5 5 27 0 32M32 16c-5 5-5 27 0 32" fill="none" stroke="var(--c)" stroke-width="2.5" opacity=".55"/>',
 'flag': '<path d="M21 14v36" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/><path d="M23 16h22l-5 8 5 8H23z" fill="#fff"/>',
 'tag': '<path d="M15 17v13l19 19 15-15-19-19H17a2 2 0 0 0-2 2z" fill="#fff"/><circle cx="23" cy="25" r="3.2" fill="var(--c)"/>',
 'user': '<circle cx="32" cy="24" r="9" fill="#fff"/><path d="M15 48c1-9 8-14 17-14s16 5 17 14z" fill="#fff"/>',
 'spark': '<path d="M30 13l3.6 10.4L44 27l-10.4 3.6L30 41l-3.6-10.4L16 27l10.4-3.6z" fill="#fff"/><path d="M45 37l1.8 5.2L52 44l-5.2 1.8L45 51l-1.8-5.2L38 44l5.2-1.8z" fill="#fff"/>',
 'move': '<circle cx="35" cy="15" r="4.5" fill="#fff"/><path d="M24 50l6-12 6 4v8M20 30l9-6 6 6 7 2M30 24l-2 14" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>',
 'loop': '<path d="M18 30a14 14 0 0 1 24-9l3 3M45 16v8h-8M46 34a14 14 0 0 1-24 9l-3-3M19 48v-8h8" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>',
 'doc': '<path d="M20 13h17l9 9v27a2 2 0 0 1-2 2H20a2 2 0 0 1-2-2V15a2 2 0 0 1 2-2z" fill="#fff"/><path d="M24 32h16M24 39h16M24 25h8" stroke="var(--c)" stroke-width="3" stroke-linecap="round"/>',
 'sheet': '<rect x="16" y="14" width="32" height="36" rx="5" fill="#fff"/><path d="M16 24h32M16 33h32M16 42h32M28 24v26" stroke="var(--c)" stroke-width="2.2" opacity=".6"/>',
 'users': '<circle cx="25" cy="24" r="7" fill="#fff"/><circle cx="41" cy="26" r="5.5" fill="#fff" opacity=".85"/><path d="M12 47c1-8 6-12 13-12s12 4 13 12z" fill="#fff"/><path d="M37 47c.3-4-1-7.5-3.5-9.8 1.9-1 3.8-1.3 6-1.3 6 0 10 3.6 10.8 11.1z" fill="#fff" opacity=".85"/>',
 'bolt': '<path d="M35 12L18 35h12l-3 17 17-23H32z" fill="#fff"/>',
}
def clay(k, c, cls=''):
    return f'<span class="clay{(" "+cls) if cls else ""}" style="--c:{c}" aria-hidden="true"><svg viewBox="0 0 64 64">{GLYPH[k]}</svg></span>'

HMARK = '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="15" fill="#0E5C57"/><path d="M19.5 23.5Q32 12.5 44.5 23.5" fill="none" stroke="#D9A441" stroke-width="5.2" stroke-linecap="round"/><path d="M22.5 29v21M41.5 29v21M22.5 39.5h19" fill="none" stroke="#F3F5F2" stroke-width="6.2" stroke-linecap="round"/></svg>'

def ecg_path(w=600, h=64, beats=(0.18, 0.5, 0.82), amp=1.0):
    """A clean PQRST heartbeat line for an SVG viewBox w x h."""
    y = h * .62; a = h * .5 * amp
    d = f'M0 {y:.1f}'
    for b in beats:
        x = w * b
        d += (f' L{x-46:.1f} {y:.1f} Q{x-38:.1f} {y-a*.18:.1f} {x-30:.1f} {y:.1f} L{x-10:.1f} {y:.1f} L{x-5:.1f} {y+a*.22:.1f}'
              f' L{x:.1f} {y-a:.1f} L{x+6:.1f} {y+a*.42:.1f} L{x+11:.1f} {y:.1f} L{x+24:.1f} {y:.1f} Q{x+36:.1f} {y-a*.3:.1f} {x+48:.1f} {y:.1f}')
    return d + f' L{w} {y:.1f}'

# ---------- strings ----------
T = {
'en': dict(
  dir='ltr', pre='',
  eyebrow_b='New', eyebrow='Founding clinic offer · 25% off until 31 Dec',
  h1a='Every patient,', h1b='answered.',
  lead="Noor is the AI receptionist for clinics in Dubai and the Gulf. She answers WhatsApp, calls, voice notes and website chat in Arabic and English, and books patients straight into your calendar, day and night.",
  call='Call Noor · 1 min', chat='Chat with Noor live',
  dxb='Dubai', live='Noor is answering patients right now',
  tick='Mariam booked whitening, Sat 11:30|Missed call turned into a booking in 4 seconds|Arabic voice note answered at 01:12|Cancelled slot refilled from the waitlist|Review request sent after a visit|Morning summary sent to the owner',
  meta=[('&lt;10 s','first reply'),('24/7','incl. Fridays &amp; Eid'),('EN · ع','Arabic &amp; English'),('14 days','free pilot')],
  note='Demo opens a fictional dental clinic. Nothing is really booked. <a href="/glow/">Skin clinic demo</a> · <a href="/book/">Patient booking page</a>',
  vk='Product demo · sound on', vt='Watch Halora in 74 seconds', vs='WhatsApp, phone, owner dashboard and patient app',
  clinic='Pearl Dental (demo)', online='Noor · online',
  wa=[('p','Hi! How much is teeth whitening? Anything Saturday?'),('n','Hi Mariam 😊 Whitening is AED 1,200 and takes about 90 minutes. Saturday I have 10:00 or 11:30 with Dr. Sara.'),('p','11:30 please'),('n','Booked ✅ Saturday 11:30 with Dr. Sara. I’ll remind you the day before.')],
  wachip='Added to calendar · reminder set',
  cal_day='Saturday', cal_rows=[('10:00','Cleaning · Ahmed K.','t'),('11:30','Whitening · Mariam S.','b'),('13:00','Free','f')], booked='Booked by Noor',
  call_t='Missed call · 23:12', call_s='Answered by Noor · booked Thu 11:00',
  ariah='Animation: a patient chat on WhatsApp, a calendar slot booked by Noor and a missed call answered by Noor',
  # modules
  mk='The modules', mh='Every touchpoint opens into <b>a complete front desk.</b>', mp='Patients reach you four ways. Noor turns each one into bookings, reminders, reviews and reports. Scroll to open them up.',
  tps=[('chat','#1fa971','WhatsApp','Price for whitening?'),('phone','#c98f22','Phone call','Missed call · 23:12'),('mic','#5b7fd6','Voice note','🎙️ 0:09 · Arabic'),('globe','#14a3b8','Website chat','Open on Friday?')],
  mods=[('phone','#c98f22','AI phone receptionist','Answers on the first ring, books by voice, and texts every missed caller.','/product/phone/',1),
        ('chat','#1fa971','WhatsApp & web chat','Replies in seconds, day and night, in Arabic and English.','/product/whatsapp/',0),
        ('cal','#0e5c57','Bookings & calendar','Offers real free slots and books straight into Google Calendar.','/integrations/#calendar',3),
        ('bell','#d4669a','Reminders & waitlist','Fewer no-shows. Cancelled slots refilled from the waitlist.','/product/growth/',2),
        ('star','#d9a441','Google reviews','Asks happy patients for a review. Unhappy ones reach you first.','/product/growth/',0),
        ('mega','#7c6cf2','Campaigns','Approved recall and offer messages to the right patients.','/for-owners/#campaigns',1),
        ('dash','#0e5c57','Owner dashboard','Every chat and booking in one place, plus a daily PDF report.','/for-owners/',2),
        ('web','#14a3b8','Clinic website & patient app','A fast website and patient app with booking and Noor built in.','/sample/',3)],
  more='Explore',
  # intro
  skip='Skip intro', bk=['Whitening · Sat 11:30','Cleaning · Thu 11:00','Consultation · Sun 10:00','Check-up · Fri 16:30'], bookedv='Booked ✓',
  # call mock
  cm_name='Noor · Pearl Dental (demo)', cm_state='On call · 00:42', cm=[('p','I need a cleaning this week.'),('n','Of course. Wednesday 4 pm or Thursday 11 am?'),('p','Thursday.'),('n','Booked for Thursday at 11. A WhatsApp confirmation is on its way.')], cm_chip='Booked ✓ Thu 11:00', cm_btn=['Mute','Speaker','Transfer'],
  # dashboard mock
  dm_title='Overview', dm_tabs=['Overview','Inbox','Requests','Campaigns'], dm_k=[('38','Bookings by Noor'),('61%','Replies after hours'),('8 s','Typical first reply')], dm_chart='Bookings this week', dm_days=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
  dm_rows=[('09:30','Cleaning · Dr. Sara','Confirmed','ok'),('11:00','Implant consult · Dr. Omar','Booked by Noor','nb'),('16:30','Aligners review · Dr. Lina','Reminder sent','rm')], dm_cap='Illustration with sample data.',
  # calendar mock
  cw_title='This week', cw_days=['Sun','Mon','Tue','Wed','Thu'], cw_legend='Booked by Noor', cw_after='after hours',
),
'ar': dict(
  dir='rtl', pre='/ar',
  eyebrow_b='جديد', eyebrow='عرض العيادات المؤسِّسة · خصم 25% حتى 31 ديسمبر',
  h1a='كل مريض،', h1b='يجد ردًّا.',
  lead='نور هي موظفة الاستقبال الذكية لعيادات دبي والخليج. ترد على واتساب والمكالمات والرسائل الصوتية ودردشة الموقع بالعربية والإنجليزية، وتحجز المرضى مباشرة في تقويمك، ليلًا ونهارًا.',
  call='اتصل بنور · دقيقة واحدة', chat='تحدّث مع نور الآن',
  dxb='دبي', live='نور ترد على المرضى الآن',
  tick='مريم حجزت تبييض الأسنان، السبت 11:30|مكالمة فائتة تحوّلت إلى حجز خلال 4 ثوانٍ|ردّت نور على رسالة صوتية بالعربية الساعة 01:12|موعد ملغى امتلأ من قائمة الانتظار|أُرسل طلب تقييم بعد الزيارة|وصل ملخص الصباح لصاحب العيادة',
  meta=[('<span dir="ltr">&lt;10 ث</span>','أول رد'),('24/7','حتى الجمعة والأعياد'),('ع · EN','عربي وإنجليزي'),('14 يومًا','تجربة مجانية')],
  note='التجربة تفتح عيادة أسنان وهمية، ولا يتم حجز أي موعد حقيقي. <a href="/glow/">تجربة عيادة الجلدية</a> · <a href="/book/">صفحة الحجز للمرضى</a>',
  vk='فيديو تعريفي · بالصوت', vt='شاهد هالورا في 74 ثانية', vs='واتساب والهاتف ولوحة المالك وتطبيق المرضى',
  clinic='عيادة بيرل للأسنان (تجريبية)', online='نور · متصلة',
  wa=[('p','مرحبا، كم سعر تبييض الأسنان؟ في موعد السبت؟'),('n','أهلًا مريم 😊 التبييض 1,200 درهم ويستغرق حوالي 90 دقيقة. يوم السبت عندي 10:00 أو 11:30 مع د. سارة.'),('p','11:30 لو سمحتي'),('n','تم الحجز ✅ السبت 11:30 مع د. سارة. بذكّرك قبلها بيوم.')],
  wachip='أُضيف للتقويم · التذكير مُفعّل',
  cal_day='السبت', cal_rows=[('10:00','تنظيف · أحمد ك.','t'),('11:30','تبييض · مريم س.','b'),('13:00','متاح','f')], booked='حجزته نور',
  call_t='مكالمة فائتة · 23:12', call_s='ردّت نور · حجز الخميس 11:00',
  ariah='رسوم متحركة: محادثة مريض على واتساب، وموعد حجزته نور في التقويم، ومكالمة فائتة ردّت عليها نور',
  mk='الوحدات', mh='كل نقطة تواصل تتحول إلى <b>مكتب استقبال متكامل.</b>', mp='يتواصل معك المرضى بأربع طرق، ونور تحوّل كل واحدة منها إلى حجوزات وتذكيرات وتقييمات وتقارير. مرّر للأسفل لتراها تنفتح.',
  tps=[('chat','#1fa971','واتساب','كم سعر التبييض؟'),('phone','#c98f22','مكالمة','مكالمة فائتة · 23:12'),('mic','#5b7fd6','رسالة صوتية','🎙️ 0:09 · عربي'),('globe','#14a3b8','دردشة الموقع','تفتحون يوم الجمعة؟')],
  mods=[('phone','#c98f22','موظفة استقبال هاتفية ذكية','ترد من أول رنّة، وتحجز بالصوت، وتراسل كل من فاتته مكالمة.','/ar/product/phone/',1),
        ('chat','#1fa971','واتساب ودردشة الموقع','ترد خلال ثوانٍ ليلًا ونهارًا بالعربية والإنجليزية.','/ar/product/whatsapp/',0),
        ('cal','#0e5c57','الحجوزات والتقويم','تعرض المواعيد المتاحة فعلًا وتحجزها مباشرة في تقويم Google.','/ar/integrations/#calendar',3),
        ('bell','#d4669a','التذكيرات وقائمة الانتظار','غياب أقل، والمواعيد الملغاة تُملأ من قائمة الانتظار.','/ar/product/growth/',2),
        ('star','#d9a441','تقييمات Google','تطلب التقييم من المرضى الراضين، وغير الراضين يصلونك أولًا.','/ar/product/growth/',0),
        ('mega','#7c6cf2','الحملات','رسائل متابعة وعروض توافق عليها للمرضى المناسبين.','/ar/for-owners/#campaigns',1),
        ('dash','#0e5c57','لوحة المالك','كل المحادثات والحجوزات في مكان واحد، مع تقرير PDF يومي.','/ar/for-owners/',2),
        ('web','#14a3b8','موقع العيادة وتطبيق المرضى','موقع سريع وتطبيق للمرضى مع الحجز ونور مدمجة.','/sample/',3)],
  more='اكتشف',
  skip='تخطَّ المقدمة', bk=['تبييض · السبت 11:30','تنظيف · الخميس 11:00','استشارة · الأحد 10:00','فحص · الجمعة 16:30'], bookedv='تم الحجز ✓',
  cm_name='نور · عيادة بيرل (تجريبية)', cm_state='مكالمة جارية · 00:42', cm=[('p','أبي موعد تنظيف هالأسبوع.'),('n','أكيد. الأربعاء 4 العصر أو الخميس 11 الصبح؟'),('p','الخميس.'),('n','تم الحجز الخميس الساعة 11، وبيوصلك تأكيد على واتساب.')], cm_chip='تم الحجز ✓ الخميس 11:00', cm_btn=['كتم','مكبّر الصوت','تحويل'],
  dm_title='نظرة عامة', dm_tabs=['نظرة عامة','الرسائل','الطلبات','الحملات'], dm_k=[('38','حجز عبر نور'),('61%','ردود بعد الدوام'),('8 ث','متوسط أول رد')], dm_chart='الحجوزات هذا الأسبوع', dm_days=['أحد','اثنين','ثلاثاء','أربعاء','خميس','جمعة','سبت'],
  dm_rows=[('09:30','تنظيف · د. سارة','مؤكد','ok'),('11:00','استشارة زراعة · د. عمر','حجزته نور','nb'),('16:30','مراجعة تقويم · د. لينا','أُرسل التذكير','rm')], dm_cap='صورة توضيحية ببيانات تجريبية.',
  cw_title='هذا الأسبوع', cw_days=['الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس'], cw_legend='حجزته نور', cw_after='بعد الدوام',
),
}

# ---------- UI mock-ups ----------
def chat_ui(t, clinic=None, msgs=None, chip=None, cls=''):
    clinic = clinic or t['clinic']; msgs = msgs or t['wa']; chip = t['wachip'] if chip is None else chip
    m = ''.join(f'<div class="b {w}" style="--d:{.25+i*.5:.2f}s">{x}</div>' for i, (w, x) in enumerate(msgs))
    if chip: m += f'<div class="ck" style="--d:{.25+len(msgs)*.5:.2f}s">{chip}</div>'
    return (f'<div class="dev wa {cls}"><div class="scr"><div class="wh"><span class="av">{HMARK}</span><div><b>{clinic}</b><small>{t["online"]}</small></div></div>'
            f'<div class="wmsg">{m}</div></div></div>')

def call_ui(t):
    bars = ''.join(f'<i style="--h:{h}"></i>' for h in (30,55,80,45,95,60,35,70,50,85,40,65,30))
    tr = ''.join(f'<div class="b {w}" style="--d:{.3+i*.55:.2f}s">{x}</div>' for i, (w, x) in enumerate(t['cm']))
    btn = ''.join(f'<span>{b}</span>' for b in t['cm_btn'])
    return (f'<div class="dev call"><div class="scr"><div class="ch"><span class="av lg">{HMARK}</span><b>{t["cm_name"]}</b><small>{t["cm_state"]}</small>'
            f'<div class="wave" aria-hidden="true">{bars}</div></div><div class="tr">{tr}<div class="ck" style="--d:{.3+len(t["cm"])*.55:.2f}s">{t["cm_chip"]}</div></div>'
            f'<div class="cb">{btn}<span class="end" aria-hidden="true"></span></div></div></div>')

def dash_ui(t):
    tabs = ''.join(f'<em{" class=on" if i==0 else ""}>{x}</em>' for i, x in enumerate(t['dm_tabs']))
    kp = ''.join(f'<div><b>{a}</b><small>{b}</small></div>' for a, b in t['dm_k'])
    bars = ''.join(f'<span style="--h:{h}%"><i></i><small>{d}</small></span>' for h, d in zip((42,58,51,74,66,38,88), t['dm_days']))
    rows = ''.join(f'<tr><td dir="ltr">{a}</td><td>{b}</td><td><span class="st {k}">{c}</span></td></tr>' for a, b, c, k in t['dm_rows'])
    return (f'<div class="dsh"><div class="tb"><span class="dots"><i></i><i></i><i></i></span><span class="mk">{HMARK}</span><nav>{tabs}</nav></div>'
            f'<div class="kp">{kp}</div><div class="chart"><small>{t["dm_chart"]}</small><div class="bars">{bars}</div></div>'
            f'<table>{rows}</table><div class="cap">{t["dm_cap"]}</div></div>')

def cal_ui(t):
    times = ['09:00','11:00','13:00','17:00','20:00','22:30']
    # (day index, time index, kind)  b = booked by Noor, t = taken by team
    S = {(0,0):'t',(0,4):'b',(1,1):'b',(1,2):'t',(2,0):'t',(2,3):'b',(2,5):'b',(3,2):'b',(3,4):'t',(4,1):'t',(4,3):'b',(4,5):'b',(0,2):'t',(1,4):'b',(3,0):'t'}
    head = '<div></div>' + ''.join(f'<b>{d}</b>' for d in t['cw_days'])
    body = ''
    for ti, tm in enumerate(times):
        body += f'<span class="tm" dir="ltr">{tm}</span>'
        for di in range(len(t['cw_days'])):
            k = S.get((di, ti), '')
            body += f'<i class="{k}" style="--d:{(di*6+ti)*.06:.2f}s"></i>'
    return (f'<div class="cw"><div class="cwh"><b>{t["cw_title"]}</b><span><i class="b"></i>{t["cw_legend"]}</span></div>'
            f'<div class="cg">{head}{body}</div><div class="cwa"><span></span>{t["cw_after"]}</div></div>')

def hero_visual(t):
    rows = ''.join(f'<div class="r {k}"><time dir="ltr">{a}</time><span>{b}</span>{"<em>"+t["booked"]+"</em>" if k=="b" else ""}</div>' for a, b, k in t['cal_rows'])
    return (f'<div class="hv" role="img" aria-label="{E(t["ariah"])}">'
            f'<span class="blob" aria-hidden="true"></span>{chat_ui(t)}'
            f'<div class="fc fcal"><div class="fh">{clay("cal","#0e5c57","sm")}<b>{t["cal_day"]}</b></div>{rows}</div>'
            f'<div class="fc fcall">{clay("phone","#c98f22","sm")}<div><b>{t["call_t"]}</b><small>{t["call_s"]}</small></div></div>'
            f'<span class="fl f1">{clay("tooth","#14a3b8")}</span><span class="fl f2">{clay("heart","#d4669a","sm")}</span><span class="fl f3">{clay("steth","#0e5c57","sm")}</span>'
            '</div>')

def hero(t, video_card):
    meta = ''.join(f'<div><b>{a}</b>{b}</div>' for a, b in t['meta'])
    W = 600
    return f'''<section class="v5h" id="top">
<div class="wrap">
 <div class="cp">
  <a class="eyebrow" href="#plans"><b>{t['eyebrow_b']}</b>{t['eyebrow']}</a>
  <h1><span>{t['h1a']}</span> <span class="g">{t['h1b']}</span></h1>
  <svg class="ecg" viewBox="0 0 {W} 64" preserveAspectRatio="none" aria-hidden="true"><path class="base" d="{ecg_path(W)}"/><path class="run" d="{ecg_path(W)}"/></svg>
  <p class="lead">{t['lead']}</p>
  <div class="cta">
   <a class="bx gold" href="#" data-voice><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/></svg>{t['call']}</a>
   <a class="bx glass" href="#" data-chat><span class="pulse"></span>{t['chat']}</a>
  </div>
  {video_card}
  <div class="live"><span class="pulse"></span><span class="clk" data-dxb="{t['dxb']}">--:-- {t['dxb']}</span><span class="tk" data-tick="{t['tick']}">{t['live']}</span></div>
  <div class="meta">{meta}</div>
  <p class="note2">{t['note']}</p>
 </div>
 {hero_visual(t)}
</div>
</section>'''

def modules(t):
    tps = ''.join(f'<div class="tp" data-i="{i}">{clay(k,c,"sm")}<span><b>{a}</b><small>{q}</small></span></div>' for i, (k, c, a, q) in enumerate(t['tps']))
    cards = ''.join(f'<a class="mod" href="{u}" data-from="{f}">{clay(k,c)}<h3>{a}</h3><p>{p}</p><span class="go">{t["more"]}</span></a>' for k, c, a, p, u, f in t['mods'])
    return f'''<section class="mods" id="modules" aria-labelledby="mods-h">
<div class="pin"><div class="wrap">
 <div class="hd2"><span class="k">{t['mk']}</span><h2 id="mods-h">{t['mh']}</h2><p>{t['mp']}</p></div>
 <div class="mst">
  <div class="hub" aria-hidden="true"><span class="ring"></span>{HMARK}</div>
  <div class="tps" aria-hidden="true">{tps}</div>
  <div class="g8">{cards}</div>
 </div>
</div></div>
</section>'''

def pulse_data(t):
    tps = [{'ic': clay(k, c, 'sm'), 'a': a, 'q': q} for k, c, a, q in t['tps']]
    return E(json.dumps({'h1': t['h1a'], 'h2': t['h1b'], 'skip': t['skip'], 'tps': tps, 'bk': t['bk'], 'ok': t['bookedv'], 'mark': HMARK}, ensure_ascii=False))

PULSE_HEAD = ('<script>try{if(sessionStorage.getItem("hlPulse")!=="1"&&!matchMedia("(prefers-reduced-motion: reduce)").matches)'
              '{document.documentElement.classList.add("pulse-pending");setTimeout(function(){document.documentElement.classList.remove("pulse-pending")},1800)}}catch(e){}</script>\n')
