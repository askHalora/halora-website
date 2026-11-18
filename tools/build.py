import json, os, re, html
import os
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
ORIG=os.path.join(os.path.dirname(__file__),'index.before-v4.html')

P={
'chat':'<path d="M4 5h16a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H9l-5 4V6a1 1 0 0 1 1-1z"/><path d="M8 10h8M8 13h5"/>',
'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/>',
'heart':'<path d="M12 20s-7-4.4-7-9.5A4 4 0 0 1 12 8a4 4 0 0 1 7 2.5C19 15.6 12 20 12 20z"/>',
'globe':'<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c2.5 2.5 2.5 13.5 0 16M12 4c-2.5 2.5-2.5 13.5 0 16"/>',
'cal':'<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4M9 15l2 2 4-4"/>',
'star':'<path d="M12 4l2.4 5 5.4.7-4 3.7 1 5.4L12 16.3 7.2 18.8l1-5.4-4-3.7 5.4-.7z"/>',
'bell':'<path d="M6 16v-5a6 6 0 0 1 12 0v5l2 2H4zM10 20a2 2 0 0 0 4 0"/>',
'chart':'<path d="M4 20V4M4 20h16M8 16v-4M12 16V8M16 16v-6"/>',
'mic':'<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M6 11a6 6 0 0 0 12 0M12 17v4"/>',
'tooth':'<path d="M7 4c2 0 3 1 5 1s3-1 5-1 3 2 3 5-2 4-2 7-1 4-2 4-1.5-4-4-4-3 4-4 4-2-1-2-4-2-4-2-7 1-5 3-5z"/>',
'spark':'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM18 15l.8 2.2L21 18l-2.2.8L18 21l-.8-2.2L15 18l2.2-.8z"/>',
'move':'<circle cx="13" cy="4.5" r="1.8"/><path d="M9 21l3-6 3 2v4M7 11l5-3 3 3 3 1M12 8l-1 7"/>',
'seed':'<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="8"/><path d="M12 4c3 3 3 13 0 16"/>',
'shield':'<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
'grid':'<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
'bolt':'<path d="M13 3L5 14h6l-1 7 8-11h-6z"/>',
'lang':'<path d="M4 6h9M8.5 4v2M6 6c1 4 4 7 7 8M11 6c-1 4-3 6-6 8M13 20l4-10 4 10M14.5 16.5h5"/>',
'loop':'<path d="M4 12a8 8 0 0 1 14-5.3L20 9M20 4v5h-5M20 12a8 8 0 0 1-14 5.3L4 15M4 20v-5h5"/>',
'doc':'<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
'users':'<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 5a3 3 0 0 1 0 6M18 14c2 .7 3 2.8 3 6"/>',
'building':'<path d="M4 21V5l8-2v18M12 8h8v13M8 8h.01M8 12h.01M8 16h.01M16 12h.01M16 16h.01M2 21h20"/>',
}
def ic(k): return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+P[k]+'</svg>'
def gi(k,c): return f'<span class="gi" style="--c:{c}">{ic(k)}</span>'
def ico3(k,c): return f'<span class="ico3" style="--c:{c}">{ic(k)}</span>'
MARK='<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M19.5 23.5Q32 12.5 44.5 23.5" fill="none" stroke="#D9A441" stroke-width="5.2" stroke-linecap="round"/><path d="M22.5 29v21M41.5 29v21M22.5 39.5h19" fill="none" stroke="#F3F5F2" stroke-width="6.2" stroke-linecap="round"/></svg>'
MARKSQ='<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="15" fill="#0E5C57"/><path d="M19.5 23.5Q32 12.5 44.5 23.5" fill="none" stroke="#D9A441" stroke-width="5.2" stroke-linecap="round"/><path d="M22.5 29v21M41.5 29v21M22.5 39.5h19" fill="none" stroke="#F3F5F2" stroke-width="6.2" stroke-linecap="round"/></svg>'

PRODUCTS=[('whatsapp','WhatsApp & web chat','Instant replies and bookings, 24/7','chat','#1fa971'),
 ('phone','Phone receptionist','Answers calls in a natural voice','phone','#c98f22'),
 ('growth','Reminders & reviews','Fewer no-shows, more 5-star reviews','star','#7c6cf2'),
 ('portal','Owner portal','Inbox, team take-over and reports','grid','#0e5c57')]
SPECS=[('dental','Dental clinics','Whitening, implants, aligners, emergencies','tooth','#14a3b8'),
 ('aesthetics','Aesthetics & skin','Injectables, lasers, facials, packages','spark','#d4669a'),
 ('physio','Physio & rehab','Session plans, rebooking, packages','move','#3b8f5a'),
 ('ivf','Fertility & IVF','Warm, private first-step conversations','seed','#b9811f')]

def mm(label,items,base):
    a=''.join(f'<a href="/{base}/{k}/">{gi(i,c)}<span><b>{t}</b><small>{s}</small></span></a>' for k,t,s,i,c in items)
    return f'<div class="mm"><button type="button" aria-haspopup="true">{label}</button><div class="panel">{a}</div></div>'

def header(home=False):
    h='' if home else '/'
    return ('<header class="top"><div class="wrap">\n  <a class="wm" href="/">Halora<span>.</span></a>\n  <nav>'
      + mm('Product',PRODUCTS,'product') + mm('Specialties',SPECS,'specialties')
      + f'<a href="{h}#roi">ROI</a><a href="{h}#plans">Pricing</a><a href="{h}#faq">Questions</a></nav>\n'
      + '  <a class="lang" href="/ar/" hreflang="ar" lang="ar">العربية</a>\n  <a class="btn line" href="/call/" data-call>Book a call</a>\n'
      + f'  <a class="btn" href="{h}#pilot">Free pilot</a>\n  <button class="mbtn" type="button" aria-label="Menu"><i></i><i></i><i></i></button>\n</div></header>')

STORY=[
 {"q":"Hi, how much is teeth whitening? Anything Saturday?","ch":"WhatsApp","t":"23:48","b":"Whitening · Sat 11:30","s":"Booked with Dr. Sara · reminder set","y":1},
 {"q":"🎙️ Voice note · 0:09 · Arabic","ch":"Voice note","t":"01:12","b":"Consultation · Sun 10:00","s":"Replied in Arabic · booked","y":46},
 {"q":"Missed call from +971 5• ••• •••","ch":"Phone","t":"13:05","b":"WhatsApp sent in 4 s","s":"Patient rebooked · Mon 16:30","y":56},
 {"q":"Can I move my Thursday cleaning?","ch":"Web chat","t":"21:20","b":"Moved · Thu → Fri 09:30","s":"Slot refilled from waitlist","y":1},
]
NODES=[('chat','#3ddc84','WhatsApp',50,7),('phone','#f0c766','Phone',92,30),('heart','#f59ac0','Social DMs',76,88),('globe','#7ff0df','Web chat',24,88),('mic','#8fb8ff','Voice notes',8,30)]

def hero():
    lines=''.join(f'<path id="pl{i}" d="M{x} {y} Q {(x+50)/2+(8 if i%2 else -8)} {(y+50)/2+(-8 if i%2 else 8)} 50 50" fill="none" stroke="url(#lg)" stroke-width=".35" stroke-dasharray="1 1.4"/>'
                  f'<circle r=".9" fill="{c}"><animateMotion dur="{2.6+i*.35}s" repeatCount="indefinite" begin="{i*.4}s"><mpath href="#pl{i}"/></animateMotion><animate attributeName="opacity" values="0;1;1;0" dur="{2.6+i*.35}s" repeatCount="indefinite" begin="{i*.4}s"/></circle>'
                  for i,(k,c,l,x,y) in enumerate(NODES))
    nodes=''.join(f'<div class="node" style="left:{x}%;top:{y}%;--c:{c};animation-delay:-{i*1.1}s">{ic(k)}<span>{l}</span></div>' for i,(k,c,l,x,y) in enumerate(NODES))
    tick='Mariam booked whitening, Sat 11:30|Missed call turned into a booking in 4 seconds|Arabic voice note answered at 01:12|Cancelled slot refilled from the waitlist|Review request sent after a visit|Morning summary sent to the owner'
    return f'''<section class="hx" id="top">
<div class="sky"><i></i></div><canvas class="stars" aria-hidden="true"></canvas><div class="grain"></div>
<div class="wrap">
 <div>
  <a class="eyebrow" href="#plans"><b>New</b>Founding clinic offer · 25% off until 31 Dec</a>
  <h1>Every patient on <span class="rot"><span class="on">WhatsApp</span><span>the phone</span><span>your website</span><span>voice notes</span></span><span class="glow">answered. Booked.</span></h1>
  <p class="lead">Meet Noor, the AI receptionist for Gulf clinics. She replies in seconds in Arabic and English, books straight into your calendar, and works the night shift your team can't.</p>
  <div class="cta">
   <a class="bx gold" href="#" data-voice>{ic('phone')}Call Noor · 1 min</a>
   <a class="bx glass" href="#" data-chat><span class="pulse"></span>Chat with Noor live</a>
  </div>
  <div class="live"><span class="pulse" style="width:9px;height:9px;border-radius:50%;background:#2fe0a0;flex:none"></span><span class="clk" data-dxb>--:-- Dubai</span><span class="tk" data-tick="{tick}">Noor is answering patients right now</span></div>
  <div class="meta"><div><b>&lt;10 s</b>first reply</div><div><b>24/7</b>incl. Fridays &amp; Eid</div><div><b>EN · ع</b>Arabic &amp; English</div><div><b>14 days</b>free pilot</div></div>
  <p class="note2">Demo opens a fictional dental clinic. Nothing is really booked. <a href="/glow/">Skin clinic demo</a> · <a href="/book/">Patient booking page</a></p>
 </div>
 <div class="stage" data-story='{html.escape(json.dumps(STORY),quote=True)}' aria-label="Animation: patient messages from every channel flow into Noor and become bookings">
  <svg class="ln" viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="lg"><stop offset="0" stop-color="#7ff0df" stop-opacity=".1"/><stop offset="1" stop-color="#e0b34f" stop-opacity=".8"/></linearGradient></defs>{lines}</svg>
  <div class="halo"></div><div class="orb">{MARK}</div>{nodes}
  <div class="bubble"></div><div class="bk"></div>
 </div>
</div>
<div class="cue">Scroll</div>
</section>'''

def marquee():
    it=[('chat','#1fa971','WhatsApp Business'),('globe','#14a3b8','Website chat'),('phone','#c98f22','Phone line'),('mic','#5b7fd6','Voice notes'),('cal','#0e5c57','Google Calendar'),('star','#d9a441','Google reviews'),('lang','#7c6cf2','Arabic + English'),('bell','#d4669a','Reminders'),('loop','#3b8f5a','Waitlist refill'),('doc','#61706c','Daily PDF report'),('grid','#0e5c57','Owner portal'),('shield','#0f2523','Human handover')]
    s=''.join(f'<span class="it">{gi(k,c)}{t}</span>' for k,c,t in it)
    return f'<div class="mq" aria-label="What Halora connects"><div class="tr">{s}{s}</div></div>'

def bento():
    return f'''<section class="sx" id="product"><div class="wrap">
<div class="hd2 rv"><span class="k">The product</span><h2>One receptionist. <b>Every channel.</b> No gaps.</h2><p>Each part works on its own, and together they close every leak between a patient's first message and a 5-star review.</p></div>
<div class="bento">
 <a class="bc dk w4 rv" href="/product/whatsapp/">{ico3('chat','#1fa971')}<h3>WhatsApp &amp; website chat</h3><p>Answers prices, location and insurance questions, offers real free slots and books them. Understands voice notes and replies in the patient's language.</p>
  <div class="mini"><div class="m p">Do you have anything after 6 tomorrow?</div><div class="m n">Yes, 6:30 or 7:15 with Dr. Lina. Which one?</div><div class="m p">7:15 👍</div><div class="m n">Booked ✅ See you tomorrow.</div></div><span class="go">Explore chat</span></a>
 <a class="bc w2 rv" href="/product/phone/">{ico3('phone','#c98f22')}<h3>Phone receptionist</h3><p>Picks up on the first ring in a natural voice. Missed calls get a WhatsApp in seconds.</p><span class="go">Explore phone</span></a>
 <a class="bc w3 rv" href="/product/growth/">{ico3('star','#7c6cf2')}<h3>Reminders, reviews &amp; recalls</h3><p>Reminders cut no-shows, cancelled slots get refilled from the waitlist, and happy patients are asked for a Google review.</p><span class="go">Explore growth</span></a>
 <a class="bc w3 rv" href="/product/portal/">{ico3('grid','#0e5c57')}<h3>Owner portal &amp; reports</h3><p>Every conversation in one inbox. Take over any chat in one click. A morning summary lands on your WhatsApp.</p><span class="go">Explore portal</span></a>
 <a class="bc w2 rv" href="/product/whatsapp/#voice">{ico3('mic','#5b7fd6')}<h3>Voice notes, both ways</h3><p>Patients talk, Noor listens and answers.</p><span class="go">Hear how</span></a>
 <a class="bc w2 rv" href="/specialties/dental/">{ico3('lang','#d4669a')}<h3>Gulf Arabic &amp; English</h3><p>Switches language mid-chat, naturally.</p><span class="go">See examples</span></a>
 <a class="bc w2 rv" href="/product/whatsapp/#safety">{ico3('shield','#0f2523')}<h3>Safe by design</h3><p>No medical advice, no ID requests, instant handover.</p><span class="go">How it stays safe</span></a>
</div></div></section>'''

EVENTS=[('18:42','WhatsApp · "Price for aligners?"','Gave the price range, booked a free consultation for Sunday.'),
('19:15','Missed call','WhatsApp sent in 4 seconds. Patient booked a cleaning.'),
('20:30','Arabic voice note','Transcribed, answered in Arabic, slot offered and confirmed.'),
('22:47','Cancellation','Thursday 10:00 freed and offered to the waitlist. Refilled at 22:52.'),
('00:13','Toothache at midnight','Marked urgent, owner alerted, first slot 09:00 held.'),
('02:40','Website chat · insurance question','Answered from your list. Team will confirm coverage.'),
('07:30','Reminders','14 visits reminded. 2 reschedules handled.'),
('08:55','Morning summary','PDF report sent to the owner on WhatsApp.')]
def night():
    ev=''.join(f'<div class="ev"><time>{t}</time><div><b>{a}</b><p>{b}</p></div></div>' for t,a,b in EVENTS)
    return f'''<section class="ns" aria-label="A night with Noor"><div class="pin"><div class="bg"></div><div class="moon"></div>
<div class="in"><div><span class="k">The night shift</span><h2>Your clinic closes at 6.<br>Noor doesn't.</h2>
<div class="clock"><b>18:00</b><small>Scroll through one night</small></div>
<div class="cnt"><div><b data-n="37">0</b><span>conversations</span></div><div><b data-n="9">0</b><span>bookings</span></div><div><b data-n="14">0</b><span>reminders</span></div></div>
<p style="font-size:12px;color:#7f9c96;margin-top:14px">An illustration of a typical night. Numbers vary by clinic.</p></div>
<div class="feed">{ev}</div></div></div></section>'''

SPD={
'dental':dict(name='dental',label='Dental',clinic='Pearl Dental (demo)',title='Price questions, emergencies and recalls',text='Most dental enquiries are the same ten questions. Noor answers them from your price list, books the right chair time, and flags emergencies.',href='/specialties/dental/',
 pts=['Whitening, implants and aligner prices from your list','Toothache at night → urgent flag + first slot held','6-month recall reminders that rebook themselves'],
 chat=[['p','Hi, how much are clear aligners?'],['n','Clear aligners start from AED 9,500, depending on your case. The first consultation with scan is free. Would you like Saturday 11:00 or Sunday 17:30?'],['p','Sunday please'],['n','Booked ✅ Sunday 17:30 with Dr. Omar. I\'ll send a reminder the day before.'],['c','Added to calendar · reminder scheduled']]),
'aesthetics':dict(name='aesthetics',label='Aesthetics & skin',clinic='Lumière Skin (demo)',title='Consultations, packages and discreet replies',text='Patients compare clinics fast. Noor replies first, explains treatments in plain words and books a consultation. Medical questions go to your doctor.',href='/specialties/aesthetics/',
 pts=['Treatment and package prices explained clearly','Medical questions handed to the doctor, never guessed','Review requests after each visit'],
 chat=[['p','~voice'],['n','Hi! Laser hair removal for full legs is AED 650 per session, and packages of 6 save 20%. A free skin consultation comes first. Is Tuesday 4 pm good?'],['p','Can I do it if I\'m on medication?'],['n','That\'s a great question for our doctor. I\'ve noted it so she can check at your consultation. Shall I keep Tuesday 4 pm?'],['p','Yes'],['c','Booked · doctor note added']]),
'physio':dict(name='physio',label='Physio & rehab',clinic='Motion Physio (demo)',title='Session plans that patients finish',text='Physio works when patients come back. Noor books the full plan, nudges people who miss a session and fills cancelled slots.',href='/specialties/physio/',
 pts=['Books multi-session plans in one conversation','Follow-up when a session is missed','Waitlist refill for last-minute cancellations'],
 chat=[['p','I need to cancel tomorrow\'s 8am session'],['n','No problem, cancelled. Your plan has 4 sessions left. I can move this one to Thursday 8:00 or Saturday 9:30.'],['p','Thursday'],['n','Done ✅ Thursday 8:00 with Ahmed. See you then!'],['c','Tomorrow 8:00 offered to waitlist']]),
'ivf':dict(name='fertility',label='Fertility & IVF',clinic='Hope Fertility (demo)',title='A warm, private first step',text='The first message is often the hardest one to send. Noor answers kindly at any hour, books the first consultation and connects the patient to your coordinator.',href='/specialties/ivf/',
 pts=['Gentle tone, Arabic or English, any hour','Fast handover to your patient coordinator','Never discusses results or medical details'],
 chat=[['p','Hi, we\'ve been trying for 2 years. How do we start?'],['n','Thank you for reaching out, I\'m glad you did. The first step is a consultation with Dr. Rana, for both partners. She has Monday 10:30 or Wednesday 18:00.'],['p','Wednesday please'],['n','Booked for Wednesday at 18:00. Our coordinator Hala will message you tomorrow with what to bring.'],['c','Coordinator notified']]),
'multi':dict(name='group',label='Multi-specialty',clinic='Al Noor Medical (demo)',title='One front desk for every department',text='For polyclinics and groups. Noor routes each patient to the right department, doctor and branch, and every manager sees their own numbers.',href='/#plans',
 pts=['Routes by department, doctor and branch','One inbox per branch or team','Group reports for the owner'],
 chat=[['p','Do you have a pediatrician in Al Barsha today?'],['n','Yes. Dr. Huda at our Al Barsha branch has 15:40 or 17:00 today.'],['p','17:00'],['n','Booked ✅ Pediatrics, Al Barsha, 17:00 with Dr. Huda.'],['c','Routed to Al Barsha front desk']]),
}
def specialties():
    tabs=''.join(f'<button type="button" data-k="{k}">{gi(i,c)}{t}</button>' for k,t,i,c in [('dental','Dental','tooth','#14a3b8'),('aesthetics','Aesthetics','spark','#d4669a'),('physio','Physio','move','#3b8f5a'),('ivf','Fertility','seed','#b9811f'),('multi','Multi-specialty','building','#0e5c57')])
    return f'''<section class="sx" id="specialties" style="background:var(--paper-2)"><div class="wrap">
<div class="hd2 rv"><span class="k">Specialties</span><h2>Trained for <b>your kind</b> of clinic.</h2><p>Pick a specialty and watch Noor handle a real-style conversation.</p></div>
<div data-sp='{html.escape(json.dumps(SPD),quote=True)}'><div class="sp-tabs">{tabs}</div>
<div class="sp"><div class="info"></div><div class="phone"><div class="scr"><div class="bar"><span class="av">{MARKSQ.replace('<svg','<svg width="26" height="26"')}</span><div><b>Clinic</b><small>Noor · replies instantly</small></div></div><div class="ms"></div></div></div></div></div>
</div></section>'''

def roi():
    return f'''<section class="sx" id="roi"><div class="wrap">
<div class="hd2 rv"><span class="k">ROI calculator</span><h2>What are unanswered messages <b>costing you?</b></h2><p>Move the sliders. Most clinics are surprised.</p></div>
<div class="roi rv"><div class="ctl">
<label>Patient messages and calls per week <b data-o="msg">120</b></label><input type="range" name="msg" min="20" max="500" step="10" value="120">
<label>Share that get no quick reply (after hours, busy desk) <b data-o="miss">30%</b></label><input type="range" name="miss" min="5" max="60" step="1" value="30">
<label>Average first-visit value <b data-o="val">$180</b></label><input type="range" name="val" min="40" max="1500" step="10" value="180">
<p class="fine">Assumes about 30% of slow-reply enquiries would have booked if answered at once. Your numbers will differ; the free pilot measures them for real.</p>
</div><div class="out"><span style="font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#9fb8b2">Revenue Noor could win back / month</span>
<div class="big" data-r="rev">$0</div>
<div style="margin-top:22px"><div class="row"><span>Enquiries slipping through / month</span><b data-r="lost">0</b></div><div class="row"><span>Extra bookings / month</span><b data-r="won">0</b></div><div class="row"><span>Return on the $299 plan</span><b data-r="x">0×</b></div></div>
<p><a class="bx gold" href="#pilot" style="margin-top:18px">Measure it free for 14 days →</a></p></div></div>
</div></section>'''

def compare():
    rows=[('Answers at 2 am, Fridays and Eid','n','y'),('First reply in under 10 seconds','~ When free','y'),('Arabic and English, voice notes too','~ Depends on staff','y'),('Never forgets a reminder or follow-up','n','y'),('Handles 20 chats at the same time','n','y'),('Warm human touch at the desk','y','Your team, freed up'),('Monthly cost','AED 4,000+ salary, visa, leave','From $299')]
    def cell(v): return '<span class="y">✓</span>' if v=='y' else '<span class="n">✕</span>' if v=='n' else v.replace('~ ','')
    tr=''.join(f'<tr><td>{a}</td><td>{cell(b)}</td><td class="h">{cell(c)}</td></tr>' for a,b,c in rows)
    return f'''<section class="sx tight"><div class="wrap" style="max-width:920px">
<div class="hd2 rv"><span class="k">Why both</span><h2>Your team + Noor <b>beats either alone.</b></h2><p>Noor doesn't replace your receptionist. She takes the repetitive and after-hours work so your team can look after the patients in front of them.</p></div>
<div class="rv" style="overflow-x:auto"><table class="cmp"><thead><tr><th></th><th>Front desk alone</th><th>Front desk + Noor</th></tr></thead><tbody>{tr}</tbody></table></div>
</div></section>'''

def askbar():
    return f'''<div class="askbar" data-chat role="button" tabindex="0" aria-label="Chat with Noor"><button class="x" type="button" aria-label="Close">×</button>
<div class="row1"><span class="av">{MARKSQ.replace('<svg','<svg width="38" height="38"')}</span><div><b>Ask Noor anything</b><small>She's the receptionist. Try her like a patient would.</small></div><span class="go">{ic('chat')}</span></div>
<div class="chips"><button type="button">How much is whitening?</button><button type="button">Book me for Saturday</button><button type="button">هل تتكلمين عربي؟</button></div></div>'''

def footer():
    pl=''.join(f'<a href="/product/{k}/">{t}</a><br>' for k,t,*_ in PRODUCTS)
    sl=''.join(f'<a href="/specialties/{k}/">{t}</a><br>' for k,t,*_ in SPECS)
    return f'''<footer><div class="wrap">
  <div><a class="wm" href="/">Halora<span>.</span></a><p>AI receptionist for clinics in Dubai and the Gulf.</p></div>
  <div><p><b>Product</b><br>{pl}</p></div>
  <div><p><b>Specialties</b><br>{sl}</p></div>
  <div><p><a href="mailto:ziad.elhoseiny@askhalora.com">ziad.elhoseiny@askhalora.com</a><br><a href="/call/">Book a call</a><br><a href="/ar/" lang="ar">النسخة العربية</a><br><a href="https://autova.app.n8n.cloud/webhook/halora-portal" rel="nofollow">Client sign-in</a></p><p>© 2026 Halora. Demo clinics shown are fictional.</p></div>
</div></footer>'''

# ---------- homepage ----------
src=open(ORIG,encoding='utf-8').read()
src=src.replace('<link rel="stylesheet" href="/assets/site.css">','<link rel="stylesheet" href="/assets/site.css">\n<link rel="stylesheet" href="/assets/x.css">',1)
src=re.sub(r'<header class="top">.*?</header>',lambda m:header(True),src,count=1,flags=re.S)
a=src.index('<div class="wrap hero">'); b=src.index('<section id="problem">')
src=src[:a]+hero()+'\n'+marquee()+'\n'+bento()+'\n'+night()+'\n'+specialties()+'\n'+roi()+'\n'+compare()+'\n'+src[b:]
src=re.sub(r'<footer>.*?</footer>',lambda m:footer(),src,count=1,flags=re.S)
src=src.replace('<button class="trybar"',askbar()+'\n<button class="trybar"',1)
src=src.replace('<script src="/assets/site.js" defer></script>','<script src="/assets/site.js" defer></script>\n<script src="/assets/x.js" defer></script>',1)
INTRO_HEAD='<script>try{if(sessionStorage.getItem("hlIntro")!=="1"&&!matchMedia("(prefers-reduced-motion: reduce)").matches){document.documentElement.classList.add("intro-pending");setTimeout(function(){document.documentElement.classList.remove("intro-pending")},4000)}}catch(e){}</script>\n'
def with_intro(h,tag): return h.replace('</head>',INTRO_HEAD+'</head>',1).replace('<body ','<body data-intro="'+tag+'" ',1)
open(f'{ROOT}/index.html','w',encoding='utf-8').write(with_intro(src,'Every patient · Answered'))

# ---------- sub-pages ----------
head_tpl=src[:src.index('</head>')]
def page_head(title,desc,url):
    h=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',head_tpl,flags=re.S)
    h=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{desc}">',h)
    h=re.sub(r'<link rel="alternate"[^>]*>\n?','',h)
    h=h.replace('<link rel="canonical" href="https://askhalora.com/">',f'<link rel="canonical" href="https://askhalora.com{url}">')
    h=h.replace('<meta property="og:url" content="https://askhalora.com/">',f'<meta property="og:url" content="https://askhalora.com{url}">')
    h=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{title}">',h)
    return h+'</head>'

AV26=MARKSQ.replace('<svg','<svg width="26" height="26"')
def chatmock(chat,clinic):
    m=''
    for i,(w_,t) in enumerate(chat):
        st=f' style="animation-delay:{.3+i*.45}s"'
        if w_=='c': m+=f'<div class="chip"{st}>{t}</div>'
        elif t=='~voice': m+=f'<div class="w {w_} v"{st}>▶ <i></i> 0:07</div>'
        else: m+=f'<div class="w {w_}"{st}>{t}</div>'
    return f'<div class="phone tilt"><div class="scr"><div class="bar"><span class="av">{AV26}</span><div><b>{clinic}</b><small>Noor · replies instantly</small></div></div><div class="ms">{m}</div></div></div>'

def subpage(path,crumb,title,h1,lead,iconk,color,chat,clinic,feats,steps,faqs,extra=''):
    fe=''.join(f'<div class="f rv">{ico3(k,c)}<h3>{t}</h3><p>{p}</p></div>' for k,c,t,p in feats)
    stp=''.join(f'<div class="rv"><b>{t}</b><p>{p}</p></div>' for t,p in steps)
    fq=''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)
    body=f'''<body data-chat-clinic="BrightSmile Dental (demo)" data-chat-hello="Hi, I'm Noor at BrightSmile Dental, a demo clinic. Ask me about prices, opening hours, or book a visit.">
<a class="offer-bar" id="offerbar" href="/#plans" data-end="2026-12-31T23:59:00+04:00"><b>Founding clinic offer</b> · 25% off for 12 months + 25% off setup · <span class="cd" data-cd>Ends 31 December</span> →</a>
{header()}
<main>
<section class="ph"><div class="sky"><i></i></div><canvas class="stars" aria-hidden="true"></canvas>
<div class="wrap"><div>
<div class="crumbs"><a href="/">Halora</a> / {crumb}</div>
<div style="margin-top:26px">{ico3(iconk,color)}</div>
<h1>{h1}</h1><p class="lead">{lead}</p>
<div class="cta" style="display:flex;gap:12px;flex-wrap:wrap"><a class="bx gold" href="#" data-chat><span class="pulse"></span>Try Noor now</a><a class="bx glass" href="/call/" data-call>Book a 15-min call</a></div>
</div>{chatmock(chat,clinic)}</div></section>
<section class="sx"><div class="wrap"><div class="hd2 rv"><span class="k">What you get</span><h2>Built for the way <b>Gulf clinics</b> work.</h2></div><div class="feat">{fe}</div></div></section>
{extra}
<section class="sx tight" style="background:var(--paper-2)"><div class="wrap"><div class="hd2 rv"><span class="k">Going live</span><h2>Live in <b>about a week.</b> We do the setup.</h2></div><div class="steps4">{stp}</div></div></section>
<section class="sx tight"><div class="wrap" style="max-width:820px"><div class="hd2 rv"><span class="k">Questions</span><h2>Good to know</h2></div><div class="faq">{fq}</div></div></section>
<section class="sx tight"><div class="wrap"><div class="cta-band rv"><h2>Try it free for 14 days. <b>Pay only if it brings in patients.</b></h2><div style="display:flex;gap:12px;flex-wrap:wrap"><a class="bx gold" href="/#pilot">Start the free pilot</a><a class="bx glass" href="/#plans">See pricing</a></div></div></div></section>
</main>
{footer()}
{askbar()}
<button class="trybar" id="trybar" data-chat>Talk to Noor</button>
<script src="/assets/site.js" defer></script>
<script src="/assets/x.js" defer></script>
</body></html>'''
    os.makedirs(f'{ROOT}{path}',exist_ok=True)
    open(f'{ROOT}{path}index.html','w',encoding='utf-8').write(page_head(title,lead.replace('"',''),path)+'\n'+body)

STEPS=[('15-minute call','We learn your services, prices, doctors and hours.'),('We build your Noor','Your knowledge, your tone, your calendar. You change nothing.'),('Your team tests it','Try it on your own phones and tell us what to adjust.'),('Go live','Switch on with a free 14-day pilot and watch the bookings.')]
FQ_COMMON=[('Does Noor give medical advice?','No. Noor answers practical questions (prices, times, location, insurance) and hands anything medical to your team.'),('Can my team take over a chat?','Yes, at any moment, from the owner portal or WhatsApp. Noor steps back and can pick up again later.'),('Do I need to change my WhatsApp number?','We connect your WhatsApp Business number to the official WhatsApp Cloud API. We guide you through it and handle the technical part.')]

subpage('/product/whatsapp/','Product / WhatsApp & web chat','WhatsApp & web chat · Halora','Every message answered <span class="glow">in seconds,</span> day and night.',
 'Noor replies to patients on WhatsApp and your website chat, answers their questions from your own price list, and books real free slots straight into your calendar.',
 'chat','#1fa971',SPD['dental']['chat'],'Pearl Dental (demo)',
 [('bolt','#c98f22','Replies in seconds','24/7, including Fridays, holidays and Eid. The first clear answer usually wins the booking.'),
  ('cal','#0e5c57','Books real slots','Checks your calendar, offers 2–3 times, confirms, reschedules and cancels.'),
  ('mic','#5b7fd6','Voice notes in and out','Understands WhatsApp voice notes in Arabic and English, and can reply by voice.'),
  ('lang','#7c6cf2','Gulf Arabic & English','Answers in the patient\'s language and switches when they do.'),
  ('users','#d4669a','Hands over to your team','Anything sensitive or unusual goes to a person, instantly, with the full chat.'),
  ('shield','#0f2523','Safe by design','No medical advice, never asks for ID or card details, and only confirms bookings that really happened.')],
 STEPS,FQ_COMMON,
 extra=f'<section class="sx tight" id="voice"><div class="wrap"><div class="cta-band rv" style="background:radial-gradient(120% 140% at 0 0,#24346e,#0b1530 60%)"><h2>Patients send voice notes. <b>Noor listens.</b> Try it on the demo: tap the mic in the chat.</h2><a class="bx gold" href="#" data-chat>{ic("mic")}Send Noor a voice note</a></div></div></section><section class="sx tight" id="safety"><div class="wrap" style="max-width:900px"><div class="hd2 rv"><span class="k">Safety</span><h2>Guardrails <b>built in.</b></h2><p>Noor never gives medical advice, never asks for Emirates ID, cards or medical history, never invents a booking, and alerts your team the moment a patient is upset or urgent.</p></div></div></section>')

subpage('/product/phone/','Product / Phone receptionist','Phone receptionist · Halora','Your phone line, answered <span class="glow">on the first ring.</span>',
 'Noor answers calls in a natural voice in Arabic and English, books and reschedules, and turns every missed call into a WhatsApp conversation within seconds.',
 'phone','#c98f22',[['c','Incoming call · 13:05'],['n','Good afternoon, this is Noor at Pearl Dental. How can I help?'],['p','I need a cleaning this week'],['n','Of course. I have Wednesday 4 pm or Thursday 11 am. Which suits you?'],['p','Thursday'],['n','Booked for Thursday at 11. You\'ll get a WhatsApp confirmation now.'],['c','Call summary sent to the team']],'Pearl Dental (demo)',
 [('phone','#c98f22','Every call answered','No more busy tones or voicemail during the rush hour or after closing.'),
  ('chat','#1fa971','Missed call → WhatsApp','If a call is missed, the patient gets a WhatsApp in seconds and the conversation continues.'),
  ('cal','#0e5c57','Books by voice','Finds a free slot, confirms it out loud and sends a WhatsApp confirmation.'),
  ('lang','#7c6cf2','Natural voice, two languages','Warm, clear Arabic and English. Patients can switch any time.'),
  ('users','#d4669a','Transfers to your team','Urgent or complex calls go straight to a person.'),
  ('doc','#61706c','Call summaries','Every call is summarised in the portal and the daily report.')],
 STEPS,[('Which plan includes calls?','Phone answering is part of the Front Desk + Phone plan and the Group plan.'),('Can patients still reach a person?','Yes. Noor transfers calls or arranges a callback whenever a patient asks for a person.')]+FQ_COMMON[:1])

subpage('/product/growth/','Product / Reminders & reviews','Reminders, reviews & recalls · Halora','Fewer no-shows. <span class="glow">More five-star reviews.</span>',
 'Noor reminds every patient before their visit, refills cancelled slots from your waitlist, asks happy patients for a Google review and brings old patients back with approved recall messages.',
 'star','#7c6cf2',[['n','Hi Sara, a reminder of your visit tomorrow at 10:00 with Dr. Omar. Reply 1 to confirm or 2 to reschedule.'],['p','1'],['n','Confirmed ✅ See you tomorrow!'],['c','Next day · after the visit'],['n','How was your visit today? If you were happy, a short Google review would mean a lot to us ⭐'],['p','Loved it, done!']],'Pearl Dental (demo)',
 [('bell','#d4669a','Smart reminders','24 hours and 2 hours before each visit, with one-tap confirm or reschedule.'),
  ('loop','#3b8f5a','Waitlist refill','A cancelled slot is offered to waiting patients automatically.'),
  ('star','#d9a441','Google review requests','Sent after each visit. Unhappy replies alert you privately first.'),
  ('users','#7c6cf2','Recall campaigns','Approved messages to the right patients, such as 6-month cleanings.'),
  ('chart','#0e5c57','Results you can see','Weekly and monthly reports of bookings, no-shows and reviews.'),
  ('shield','#0f2523','Opt-out respected','Patients can stop messages any time; Noor never spams.')],
 STEPS,FQ_COMMON[:2])

subpage('/product/portal/','Product / Owner portal','Owner portal · Halora','See every patient Noor <span class="glow">brought in.</span>',
 'One place for the owner and the team: every conversation, every booking, every request. Take over any chat in one click and get a summary on WhatsApp each morning.',
 'grid','#0e5c57',[['c','Morning summary · 08:55'],['n','Good morning Dr. Omar ☀️ Yesterday Noor handled 37 conversations and booked 9 visits (3 after hours). 2 requests need your team. Full PDF attached.'],['p','Who needs a callback?'],['n','Ahmed K. (insurance question) and Layla S. (wants Dr. Sara only). Both are in the Requests tab.']],'Halora for owners',
 [('grid','#0e5c57','Live dashboard','Conversations, bookings and revenue Noor brought in, by day, week and month.'),
  ('chat','#1fa971','Shared inbox','Every chat in one place. Take over with one click, then hand it back.'),
  ('doc','#61706c','Requests board','Callbacks, waitlist, invoices: each with a status your team updates.'),
  ('users','#d4669a','Team access','Give each receptionist or manager their own login.'),
  ('bell','#c98f22','Daily PDF report','A short summary on WhatsApp every morning.'),
  ('star','#7c6cf2','Campaigns','Send approved recall and offer messages to the right patients.')],
 STEPS,[('Which plan includes the portal?','The portal comes with Front Desk + Phone and Group plans. The Front Desk plan includes the daily PDF summary on WhatsApp.')]+FQ_COMMON[1:2])

SPEC_PAGES={
'dental':('Dental clinics','The AI receptionist for <span class="glow">dental clinics.</span>','tooth','#14a3b8',
 [('tooth','#14a3b8','Treatment prices, explained','Whitening, implants, aligners and veneers answered from your own price list.'),('bolt','#c98f22','Emergencies flagged','Toothache at night? Marked urgent, first slot held, owner alerted.'),('loop','#3b8f5a','6-month recalls','Patients due a check-up get a friendly reminder that rebooks itself.'),('cal','#0e5c57','Right chair time','Books the right duration for each treatment and doctor.'),('shield','#0f2523','Insurance questions','Answers which insurers you work with; your team confirms coverage.'),('star','#d9a441','Reviews after visits','Happy patients asked for a Google review, every time.')]),
'aesthetics':('Aesthetics & skin','The AI receptionist for <span class="glow">aesthetic clinics.</span>','spark','#d4669a',
 [('spark','#d4669a','Treatments in plain words','Injectables, lasers, facials and packages explained clearly with your prices.'),('users','#7c6cf2','Doctor handles medical','Questions about medication or suitability go to the doctor, never guessed.'),('chat','#1fa971','Fast replies win','Patients message several clinics. Noor answers first, day or night.'),('loop','#3b8f5a','Course rebooking','Laser and facial courses rebooked at the right interval.'),('star','#d9a441','Reviews and referrals','Review requests after each session.'),('lang','#5b7fd6','Discreet, warm tone','Polite, private, in Arabic or English.')]),
'physio':('Physio & rehab','The AI receptionist for <span class="glow">physio clinics.</span>','move','#3b8f5a',
 [('cal','#0e5c57','Whole plans booked','Books a full series of sessions in one conversation.'),('bell','#d4669a','Missed session follow-up','A friendly nudge when a session is missed, with new times.'),('loop','#3b8f5a','Waitlist refill','Last-minute cancellations offered to waiting patients.'),('shield','#0f2523','Insurance & referrals','Practical questions answered; your team confirms details.'),('doc','#61706c','Package tracking','Tells patients how many sessions they have left.'),('star','#d9a441','Reviews at discharge','Asks for a review when the plan is complete.')]),
'ivf':('Fertility & IVF','The AI receptionist for <span class="glow">fertility clinics.</span>','seed','#b9811f',
 [('heart','#d4669a','Kind first replies','A warm, respectful tone for one of the hardest messages to send.'),('users','#7c6cf2','Coordinator handover','Patients are connected to your coordinator quickly.'),('shield','#0f2523','Private by design','Never discusses results or medical details, never asks for ID.'),('lang','#5b7fd6','Arabic & English','Patients choose the language they feel comfortable in.'),('cal','#0e5c57','First consultations','Books couples\' consultations with the right doctor.'),('bolt','#c98f22','Any hour','Many people reach out late at night. Noor is there.')]),
}
for k,(crumb,h1,ik,col,feats) in SPEC_PAGES.items():
    s=SPD[k]
    subpage(f'/specialties/{k}/',f'Specialties / {crumb}',f'{crumb} · AI receptionist · Halora',h1,s['text']+' In Arabic and English, 24/7.',ik,col,s['chat'],s['clinic'],feats,STEPS,FQ_COMMON)

# sitemap
urls=['/','/ar/','/call/','/book/','/sample/','/glow/']+[f'/product/{k}/' for k,*_ in PRODUCTS]+[f'/specialties/{k}/' for k,*_ in SPECS]
open(f'{ROOT}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>https://askhalora.com{u}</loc></url>\n' for u in urls)+'</urlset>\n')
print('ok')
