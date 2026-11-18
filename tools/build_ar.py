import json, re, html, sys, os
sys.path.insert(0,os.path.dirname(__file__))
import build as B
ic,gi,ico3=B.ic,B.gi,B.ico3
ROOT=B.ROOT
ORIG=os.path.join(os.path.dirname(__file__),'ar.before-v4.html')

PR=[('whatsapp','واتساب ودردشة الموقع','ردود وحجوزات فورية على مدار الساعة','chat','#1fa971'),
 ('phone','موظفة الاستقبال الهاتفية','ترد على المكالمات بصوت طبيعي','phone','#c98f22'),
 ('growth','التذكيرات والتقييمات','غياب أقل وتقييمات خمس نجوم أكثر','star','#7c6cf2'),
 ('portal','بوابة المالك','صندوق رسائل وتدخل الفريق وتقارير','grid','#0e5c57')]
SP=[('dental','عيادات الأسنان','تبييض، زراعة، تقويم شفاف، حالات طارئة','tooth','#14a3b8'),
 ('aesthetics','التجميل والجلدية','حقن، ليزر، عناية بالبشرة، باقات','spark','#d4669a'),
 ('physio','العلاج الطبيعي','خطط الجلسات وإعادة الحجز والباقات','move','#3b8f5a'),
 ('ivf','الخصوبة وأطفال الأنابيب','خطوة أولى دافئة وخاصة','seed','#b9811f')]
def mm(label,items,base):
    a=''.join(f'<a href="/{base}/{k}/">{gi(i,c)}<span><b>{t}</b><small>{s}</small></span></a>' for k,t,s,i,c in items)
    return f'<div class="mm"><button type="button" aria-haspopup="true">{label}</button><div class="panel">{a}</div></div>'
def header():
    return ('<header class="top"><div class="wrap">\n  <a class="wm" href="/ar/" lang="en" dir="ltr">Halora<span>.</span></a>\n  <nav>'
      + mm('المنتج',PR,'product') + mm('التخصصات',SP,'specialties')
      + '<a href="#roi">العائد</a><a href="#plans">الأسعار</a><a href="#faq">أسئلة</a></nav>\n'
      + '  <a class="lang" href="/" hreflang="en" lang="en">English</a>\n  <a class="btn line" href="/call/?lang=ar" data-call>احجز مكالمة</a>\n'
      + '  <a class="btn" href="#pilot">تجربة مجانية</a>\n  <button class="mbtn" type="button" aria-label="القائمة"><i></i><i></i><i></i></button>\n</div></header>')

STORY=[
 {"q":"مرحبا، كم سعر تبييض الأسنان؟ في موعد السبت؟","ch":"واتساب","t":"23:48","b":"تبييض · السبت 11:30","s":"تم الحجز مع د. سارة · التذكير مُفعّل","y":1},
 {"q":"🎙️ رسالة صوتية · 0:09","ch":"رسالة صوتية","t":"01:12","b":"استشارة · الأحد 10:00","s":"ردّت بالعربية · تم الحجز","y":46},
 {"q":"مكالمة فائتة من ‎+971 5• ••• •••","ch":"الهاتف","t":"13:05","b":"أُرسلت رسالة واتساب خلال 4 ثوانٍ","s":"أعاد المريض الحجز · الاثنين 16:30","y":56},
 {"q":"ممكن أغيّر موعد تنظيف الخميس؟","ch":"دردشة الموقع","t":"21:20","b":"نُقل · من الخميس إلى الجمعة 09:30","s":"شُغل الموعد من قائمة الانتظار","y":1},
]
NODES=[('chat','#3ddc84','واتساب',50,7),('phone','#f0c766','الهاتف',92,30),('heart','#f59ac0','رسائل التواصل',76,88),('globe','#7ff0df','دردشة الموقع',24,88),('mic','#8fb8ff','الرسائل الصوتية',8,30)]

def hero():
    lines=''.join(f'<path id="pl{i}" d="M{x} {y} Q {(x+50)/2+(8 if i%2 else -8)} {(y+50)/2+(-8 if i%2 else 8)} 50 50" fill="none" stroke="url(#lg)" stroke-width=".35" stroke-dasharray="1 1.4"/>'
                  f'<circle r=".9" fill="{c}"><animateMotion dur="{2.6+i*.35}s" repeatCount="indefinite" begin="{i*.4}s"><mpath href="#pl{i}"/></animateMotion><animate attributeName="opacity" values="0;1;1;0" dur="{2.6+i*.35}s" repeatCount="indefinite" begin="{i*.4}s"/></circle>'
                  for i,(k,c,l,x,y) in enumerate(NODES))
    nodes=''.join(f'<div class="node" style="left:{x}%;top:{y}%;--c:{c};animation-delay:-{i*1.1}s">{ic(k)}<span>{l}</span></div>' for i,(k,c,l,x,y) in enumerate(NODES))
    tick='مريم حجزت تبييض الأسنان، السبت 11:30|مكالمة فائتة تحوّلت إلى حجز خلال 4 ثوانٍ|ردّت نور على رسالة صوتية بالعربية الساعة 01:12|موعد ملغى امتلأ من قائمة الانتظار|أُرسل طلب تقييم بعد الزيارة|وصل ملخص الصباح لصاحب العيادة'
    return f'''<section class="hx" id="top">
<div class="sky"><i></i></div><canvas class="stars" aria-hidden="true"></canvas><div class="grain"></div>
<div class="wrap">
 <div>
  <a class="eyebrow" href="#plans"><b>جديد</b>عرض العيادات المؤسِّسة · خصم 25% حتى 31 ديسمبر</a>
  <h1>كل مريض عبر <span class="rot"><span class="on">واتساب</span><span>الهاتف</span><span>موقعك</span><span>الرسائل الصوتية</span></span><span class="glow">يجد ردًّا وموعدًا.</span></h1>
  <p class="lead">تعرّف على نور، موظفة الاستقبال الذكية لعيادات الخليج. ترد خلال ثوانٍ بالعربية والإنجليزية، وتحجز مباشرة في تقويمك، وتعمل في المناوبة الليلية التي لا يستطيع فريقك تغطيتها.</p>
  <div class="cta">
   <a class="bx gold" href="#" data-voice>{ic('phone')}اتصل بنور · دقيقة واحدة</a>
   <a class="bx glass" href="#" data-chat><span class="pulse"></span>تحدّث مع نور الآن</a>
  </div>
  <div class="live"><span class="pulse" style="width:9px;height:9px;border-radius:50%;background:#2fe0a0;flex:none"></span><span class="clk" data-dxb="دبي">--:-- دبي</span><span class="tk" data-tick="{tick}">نور ترد على المرضى الآن</span></div>
  <div class="meta"><div><b dir="ltr">&lt;10 ث</b>أول رد</div><div><b>24/7</b>حتى الجمعة والأعياد</div><div><b>ع · EN</b>عربي وإنجليزي</div><div><b>14 يومًا</b>تجربة مجانية</div></div>
  <p class="note2">التجربة تفتح عيادة أسنان وهمية، ولا يتم حجز أي موعد حقيقي. <a href="/glow/">تجربة عيادة الجلدية</a> · <a href="/book/">صفحة الحجز للمرضى</a></p>
 </div>
 <div class="stage" data-story='{html.escape(json.dumps(STORY,ensure_ascii=False),quote=True)}' aria-label="رسوم متحركة: رسائل المرضى من كل القنوات تصل إلى نور وتتحول إلى حجوزات">
  <svg class="ln" viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="lg"><stop offset="0" stop-color="#7ff0df" stop-opacity=".1"/><stop offset="1" stop-color="#e0b34f" stop-opacity=".8"/></linearGradient></defs>{lines}</svg>
  <div class="halo"></div><div class="orb">{B.MARK}</div>{nodes}
  <div class="bubble" dir="rtl"></div><div class="bk" dir="rtl"></div>
 </div>
</div>
<div class="cue">مرّر</div>
</section>'''

def marquee():
    it=[('chat','#1fa971','واتساب للأعمال'),('globe','#14a3b8','دردشة الموقع'),('phone','#c98f22','خط الهاتف'),('mic','#5b7fd6','الرسائل الصوتية'),('cal','#0e5c57','تقويم Google'),('star','#d9a441','تقييمات Google'),('lang','#7c6cf2','عربي + إنجليزي'),('bell','#d4669a','التذكيرات'),('loop','#3b8f5a','ملء المواعيد الملغاة'),('doc','#61706c','تقرير PDF يومي'),('grid','#0e5c57','بوابة المالك'),('shield','#0f2523','تحويل لموظف')]
    s=''.join(f'<span class="it" dir="rtl">{gi(k,c)}{t}</span>' for k,c,t in it)
    return f'<div class="mq" aria-label="ما تربطه هالورا"><div class="tr">{s}{s}</div></div>'

def bento():
    return f'''<section class="sx" id="product"><div class="wrap">
<div class="hd2 rv"><span class="k">المنتج</span><h2>موظفة استقبال واحدة. <b>كل القنوات.</b> بلا ثغرات.</h2><p>كل جزء يعمل وحده، ومعًا تُغلق كل ثغرة بين أول رسالة من المريض وتقييم الخمس نجوم.</p></div>
<div class="bento">
 <a class="bc dk w4 rv" href="/product/whatsapp/">{ico3('chat','#1fa971')}<h3>واتساب ودردشة الموقع</h3><p>تجيب عن الأسعار والموقع والتأمين، وتعرض مواعيد متاحة فعلًا وتحجزها. تفهم الرسائل الصوتية وترد بلغة المريض.</p>
  <div class="mini"><div class="m p">عندكم موعد بعد الساعة 6 بكرة؟</div><div class="m n">نعم، 6:30 أو 7:15 مع د. لينا. أيهما يناسبك؟</div><div class="m p">7:15 👍</div><div class="m n">تم الحجز ✅ نراك غدًا.</div></div><span class="go">اكتشف الدردشة</span></a>
 <a class="bc w2 rv" href="/product/phone/">{ico3('phone','#c98f22')}<h3>موظفة الاستقبال الهاتفية</h3><p>ترد من أول رنّة بصوت طبيعي. والمكالمات الفائتة تصلها رسالة واتساب خلال ثوانٍ.</p><span class="go">اكتشف الهاتف</span></a>
 <a class="bc w3 rv" href="/product/growth/">{ico3('star','#7c6cf2')}<h3>التذكيرات والتقييمات واستعادة المرضى</h3><p>التذكيرات تقلل الغياب، والمواعيد الملغاة تُملأ من قائمة الانتظار، والمرضى الراضون يُطلب منهم تقييم على Google.</p><span class="go">اكتشف النمو</span></a>
 <a class="bc w3 rv" href="/product/portal/">{ico3('grid','#0e5c57')}<h3>بوابة المالك والتقارير</h3><p>كل المحادثات في صندوق واحد. تدخّل في أي محادثة بنقرة. وملخص الصباح يصلك على واتساب.</p><span class="go">اكتشف البوابة</span></a>
 <a class="bc w2 rv" href="/product/whatsapp/#voice">{ico3('mic','#5b7fd6')}<h3>رسائل صوتية في الاتجاهين</h3><p>المريض يتكلم، ونور تسمع وترد.</p><span class="go">اعرف كيف</span></a>
 <a class="bc w2 rv" href="/specialties/dental/">{ico3('lang','#d4669a')}<h3>عربي خليجي وإنجليزي</h3><p>تنتقل بين اللغتين في المحادثة بشكل طبيعي.</p><span class="go">شاهد أمثلة</span></a>
 <a class="bc w2 rv" href="/product/whatsapp/#safety">{ico3('shield','#0f2523')}<h3>آمنة من الأساس</h3><p>لا نصائح طبية، لا طلب للهوية، وتحويل فوري لفريقك.</p><span class="go">كيف تبقى آمنة</span></a>
</div></div></section>'''

EV=[('18:42','واتساب · "كم سعر التقويم الشفاف؟"','أعطت نطاق السعر وحجزت استشارة مجانية يوم الأحد.'),
('19:15','مكالمة فائتة','أُرسلت رسالة واتساب خلال 4 ثوانٍ، وحجز المريض جلسة تنظيف.'),
('20:30','رسالة صوتية بالعربية','فهمتها وردّت بالعربية وعرضت موعدًا وأكّدته.'),
('22:47','إلغاء موعد','عُرض موعد الخميس 10:00 على قائمة الانتظار وامتلأ الساعة 22:52.'),
('00:13','ألم أسنان منتصف الليل','حُدّدت الحالة كعاجلة، وتم تنبيه المالك وحجز أول موعد 09:00.'),
('02:40','دردشة الموقع · سؤال عن التأمين','أجابت من قائمتك، وسيؤكد الفريق التغطية.'),
('07:30','التذكيرات','تذكير 14 مريضًا بمواعيد اليوم، والتعامل مع طلبَي تغيير موعد.'),
('08:55','ملخص الصباح','وصل تقرير PDF للمالك على واتساب.')]
def night():
    ev=''.join(f'<div class="ev"><time dir="ltr">{t}</time><div><b>{a}</b><p>{b}</p></div></div>' for t,a,b in EV)
    return f'''<section class="ns" aria-label="ليلة مع نور"><div class="pin"><div class="bg"></div><div class="moon"></div>
<div class="in"><div><span class="k">المناوبة الليلية</span><h2>عيادتك تُغلق الساعة 6.<br>نور لا تُغلق.</h2>
<div class="clock" dir="ltr"><b>18:00</b><small dir="rtl">مرّر لتعيش ليلة كاملة</small></div>
<div class="cnt"><div><b data-n="37">0</b><span>محادثة</span></div><div><b data-n="9">0</b><span>حجز</span></div><div><b data-n="14">0</b><span>تذكير</span></div></div>
<p style="font-size:12px;color:#7f9c96;margin-top:14px">مثال توضيحي لليلة عادية. الأرقام تختلف من عيادة لأخرى.</p></div>
<div class="feed">{ev}</div></div></div></section>'''

SPD={
'dental':dict(label='الأسنان',clinic='عيادة بيرل للأسنان (تجريبية)',title='أسئلة الأسعار والحالات الطارئة والمتابعة الدورية',text='معظم استفسارات الأسنان هي نفس الأسئلة العشرة. نور تجيب عنها من قائمة أسعارك، وتحجز الكرسي المناسب، وتنبّه للحالات الطارئة.',href='/specialties/dental/',cta='صفحة عيادات الأسنان ←',
 pts=['أسعار التبييض والزراعة والتقويم من قائمتك','ألم ليلي ← تنبيه عاجل وحجز أول موعد','تذكير المتابعة كل 6 أشهر مع إعادة الحجز'],
 chat=[['p','مرحبا، كم سعر التقويم الشفاف؟'],['n','يبدأ التقويم الشفاف من 9,500 درهم حسب الحالة، والاستشارة الأولى مع الأشعة مجانية. يناسبك السبت 11:00 أو الأحد 17:30؟'],['p','الأحد لو سمحتي'],['n','تم الحجز ✅ الأحد 17:30 مع د. عمر. سأرسل لك تذكيرًا قبلها بيوم.'],['c','أُضيف للتقويم · التذكير مُفعّل']]),
'aesthetics':dict(label='التجميل والجلدية',clinic='لوميير للبشرة (تجريبية)',title='استشارات وباقات وردود بخصوصية',text='المرضى يقارنون بين العيادات بسرعة. نور ترد أولًا، وتشرح العلاجات بكلمات بسيطة، وتحجز استشارة. والأسئلة الطبية تذهب لطبيبك.',href='/specialties/aesthetics/',cta='صفحة عيادات التجميل ←',
 pts=['شرح واضح لأسعار العلاجات والباقات','الأسئلة الطبية تُحوَّل للطبيب ولا تُخمَّن','طلب تقييم بعد كل زيارة'],
 chat=[['p','~voice'],['n','أهلًا! جلسة الليزر للساقين كاملة 650 درهمًا، وباقة الست جلسات توفّر 20%. نبدأ باستشارة مجانية للبشرة، يناسبك الثلاثاء 4 مساءً؟'],['p','أقدر أسويه وأنا آخذ أدوية؟'],['n','سؤال مهم للطبيبة، سجّلته لها لتراجعه معك في الاستشارة. أثبّت لك الثلاثاء 4 مساءً؟'],['p','تمام'],['c','تم الحجز · أُضيفت ملاحظة للطبيبة']]),
'physio':dict(label='العلاج الطبيعي',clinic='موشن للعلاج الطبيعي (تجريبية)',title='خطط جلسات يكملها المرضى',text='العلاج الطبيعي ينجح عندما يعود المريض. نور تحجز الخطة كاملة، وتتابع من يفوّت جلسة، وتملأ المواعيد الملغاة.',href='/specialties/physio/',cta='صفحة العلاج الطبيعي ←',
 pts=['حجز خطة من عدة جلسات في محادثة واحدة','متابعة عند تفويت جلسة','ملء الإلغاءات المتأخرة من قائمة الانتظار'],
 chat=[['p','أبي ألغي جلسة بكرة الساعة 8 الصبح'],['n','تمام، أُلغيت. باقي لك 4 جلسات في خطتك. أقدر أنقلها للخميس 8:00 أو السبت 9:30.'],['p','الخميس'],['n','تم ✅ الخميس 8:00 مع أحمد. نشوفك!'],['c','عُرض موعد الغد 8:00 على قائمة الانتظار']]),
'ivf':dict(label='الخصوبة وأطفال الأنابيب',clinic='عيادة الأمل للخصوبة (تجريبية)',title='خطوة أولى دافئة وخاصة',text='أول رسالة هي الأصعب غالبًا. نور ترد بلطف في أي ساعة، وتحجز الاستشارة الأولى، وتوصل المريض بمنسقة المرضى لديكم.',href='/specialties/ivf/',cta='صفحة عيادات الخصوبة ←',
 pts=['أسلوب لطيف بالعربية أو الإنجليزية في أي ساعة','تحويل سريع لمنسقة المرضى','لا تناقش النتائج أو التفاصيل الطبية أبدًا'],
 chat=[['p','مرحبا، نحاول من سنتين. كيف نبدأ؟'],['n','شكرًا لتواصلكم، ويسعدني أنكم كتبتم. الخطوة الأولى استشارة مع د. رنا للزوجين معًا. عندها الاثنين 10:30 أو الأربعاء 18:00.'],['p','الأربعاء لو سمحتي'],['n','تم الحجز يوم الأربعاء 18:00. ستتواصل معكم المنسقة هالة غدًا بما تحتاجون إحضاره.'],['c','تم تنبيه المنسقة']]),
'multi':dict(label='متعددة التخصصات',clinic='مركز النور الطبي (تجريبي)',title='مكتب استقبال واحد لكل الأقسام',text='للمجمعات الطبية والمجموعات. نور توجّه كل مريض للقسم والطبيب والفرع الصحيح، وكل مدير يرى أرقامه.',href='#plans',cta='باقة المجموعات ←',
 pts=['توجيه حسب القسم والطبيب والفرع','صندوق رسائل لكل فرع أو فريق','تقارير المجموعة للمالك'],
 chat=[['p','عندكم طبيب أطفال في البرشاء اليوم؟'],['n','نعم. د. هدى في فرع البرشاء متاحة 15:40 أو 17:00 اليوم.'],['p','17:00'],['n','تم الحجز ✅ طب الأطفال، البرشاء، 17:00 مع د. هدى.'],['c','حُوّل لاستقبال فرع البرشاء']]),
}
def specialties():
    tabs=''.join(f'<button type="button" data-k="{k}">{gi(i,c)}{t}</button>' for k,t,i,c in [('dental','الأسنان','tooth','#14a3b8'),('aesthetics','التجميل','spark','#d4669a'),('physio','العلاج الطبيعي','move','#3b8f5a'),('ivf','الخصوبة','seed','#b9811f'),('multi','متعددة التخصصات','building','#0e5c57')])
    return f'''<section class="sx" id="specialties" style="background:var(--paper-2)"><div class="wrap">
<div class="hd2 rv"><span class="k">التخصصات</span><h2>مدرّبة على <b>نوع عيادتك</b>.</h2><p>اختر التخصص وشاهد نور تتعامل مع محادثة واقعية.</p></div>
<div data-sp='{html.escape(json.dumps(SPD,ensure_ascii=False),quote=True)}'><div class="sp-tabs">{tabs}</div>
<div class="sp"><div class="info"></div><div class="phone"><div class="scr"><div class="bar"><span class="av">{B.AV26}</span><div><b>العيادة</b><small>نور · ترد فورًا</small></div></div><div class="ms"></div></div></div></div></div>
</div></section>'''

def roi():
    return '''<section class="sx" id="roi"><div class="wrap">
<div class="hd2 rv"><span class="k">حاسبة العائد</span><h2>كم تكلّفك الرسائل <b>التي لا يُرد عليها؟</b></h2><p>حرّك المؤشرات، فأغلب العيادات تتفاجأ.</p></div>
<div class="roi rv"><div class="ctl">
<label>رسائل ومكالمات المرضى أسبوعيًا <b data-o="msg">120</b></label><input type="range" name="msg" min="20" max="500" step="10" value="120">
<label>نسبة ما لا يحصل على رد سريع (بعد الدوام، ضغط الاستقبال) <b data-o="miss">30%</b></label><input type="range" name="miss" min="5" max="60" step="1" value="30">
<label>متوسط قيمة الزيارة الأولى <b data-o="val">$180</b></label><input type="range" name="val" min="40" max="1500" step="10" value="180">
<p class="fine">نفترض أن حوالي 30% من الاستفسارات المتأخرة كانت ستتحول لحجز لو رُد عليها فورًا. أرقامك ستختلف، والتجربة المجانية تقيسها فعليًا.</p>
</div><div class="out"><span style="font-size:14px;color:#9fb8b2">الإيراد الذي قد تستعيده نور شهريًا</span>
<div class="big" data-r="rev" dir="ltr">$0</div>
<div style="margin-top:22px"><div class="row"><span>استفسارات تضيع شهريًا</span><b data-r="lost">0</b></div><div class="row"><span>حجوزات إضافية شهريًا</span><b data-r="won">0</b></div><div class="row"><span>العائد على باقة 299$</span><b data-r="x" dir="ltr">0×</b></div></div>
<p><a class="bx gold" href="#pilot" style="margin-top:18px">قِسها مجانًا لمدة 14 يومًا ←</a></p></div></div>
</div></section>'''

def compare():
    rows=[('ترد الساعة 2 فجرًا والجمعة والأعياد','n','y'),('أول رد خلال أقل من 10 ثوانٍ','~ عند التفرغ','y'),('عربي وإنجليزي ورسائل صوتية','~ حسب الموظف','y'),('لا تنسى أي تذكير أو متابعة','n','y'),('20 محادثة في نفس الوقت','n','y'),('لمسة إنسانية دافئة في الاستقبال','y','فريقك، بوقت أكثر'),('التكلفة الشهرية','راتب +4,000 درهم، إقامة، إجازات','من 299$')]
    def cell(v): return '<span class="y">✓</span>' if v=='y' else '<span class="n">✕</span>' if v=='n' else v.replace('~ ','')
    tr=''.join(f'<tr><td>{a}</td><td>{cell(b)}</td><td class="h">{cell(c)}</td></tr>' for a,b,c in rows)
    return f'''<section class="sx tight"><div class="wrap" style="max-width:920px">
<div class="hd2 rv"><span class="k">لماذا الاثنان معًا</span><h2>فريقك + نور <b>أفضل من أيٍّ منهما وحده.</b></h2><p>نور لا تحل محل موظفة الاستقبال، بل تتولى العمل المتكرر وما بعد الدوام ليهتم فريقك بالمرضى الموجودين أمامه.</p></div>
<div class="rv" style="overflow-x:auto"><table class="cmp"><thead><tr><th></th><th>الاستقبال وحده</th><th>الاستقبال + نور</th></tr></thead><tbody>{tr}</tbody></table></div>
</div></section>'''

def askbar():
    return f'''<div class="askbar" data-chat role="button" tabindex="0" aria-label="تحدّث مع نور"><button class="x" type="button" aria-label="إغلاق">×</button>
<div class="row1"><span class="av">{B.MARKSQ.replace('<svg','<svg width="38" height="38"')}</span><div><b>اسأل نور أي شيء</b><small>هي موظفة الاستقبال. جرّبها كما يفعل المريض.</small></div><span class="go">{ic('chat')}</span></div>
<div class="chips"><button type="button">كم سعر التبييض؟</button><button type="button">احجزي لي يوم السبت</button><button type="button">Do you speak English?</button></div></div>'''

def footer():
    pl=''.join(f'<a href="/product/{k}/">{t}</a><br>' for k,t,*_ in PR)
    sl=''.join(f'<a href="/specialties/{k}/">{t}</a><br>' for k,t,*_ in SP)
    return f'''<footer><div class="wrap">
  <div><a class="wm" href="/ar/" lang="en" dir="ltr">Halora<span>.</span></a><p>موظفة استقبال ذكية للعيادات في دبي والخليج.</p></div>
  <div><p><b>المنتج</b><br>{pl}</p></div>
  <div><p><b>التخصصات</b><br>{sl}</p></div>
  <div><p><a href="mailto:ziad.elhoseiny@askhalora.com" dir="ltr">ziad.elhoseiny@askhalora.com</a><br><a href="/call/?lang=ar">احجز مكالمة</a><br><a href="/" lang="en">English version</a><br><a href="https://autova.app.n8n.cloud/webhook/halora-portal" rel="nofollow">دخول العملاء</a></p><p>© 2026 هالورا. العيادات التجريبية المعروضة غير حقيقية.</p></div>
</div></footer>'''

src=open(ORIG,encoding='utf-8').read()
src=src.replace('<link rel="stylesheet" href="/assets/site.css">','<link rel="stylesheet" href="/assets/site.css">\n<link rel="stylesheet" href="/assets/x.css">',1)
src=re.sub(r'<header class="top">.*?</header>',lambda m:header(),src,count=1,flags=re.S)
a=src.index('<div class="wrap hero">'); b=src.index('<section id="problem">')
src=src[:a]+hero()+'\n'+marquee()+'\n'+bento()+'\n'+night()+'\n'+specialties()+'\n'+roi()+'\n'+compare()+'\n'+src[b:]
src=re.sub(r'<footer>.*?</footer>',lambda m:footer(),src,count=1,flags=re.S)
src=src.replace('<button class="trybar"',askbar()+'\n<button class="trybar"',1)
src=src.replace('<script src="/assets/site.js" defer></script>','<script src="/assets/site.js" defer></script>\n<script src="/assets/x.js" defer></script>',1)
open(f'{ROOT}/ar/index.html','w',encoding='utf-8').write(B.with_intro(src,'كل مريض · يجد ردًّا'))
print('ar ok')
