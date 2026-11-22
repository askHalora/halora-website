"""The 8 'why Halora' pages, English + Arabic: /how-it-works, /pricing, /for-owners, /security,
/integrations, /about, /compare, /pilot. Called at the end of build_ar.py (needs both homepages built)."""
import os, re
import v5 as V
clay, HMARK = V.clay, V.HMARK

def _plain(s): return re.sub(r'<[^>]+>', '', s).strip()

def split(k, h2, p, visual, items=None, rev=False, id_='', band=False):
    li = ''.join(f'<li>{x}</li>' for x in (items or []))
    return (f'<section class="sx tight{" band" if band else ""}"{(" id="+chr(34)+id_+chr(34)) if id_ else ""}><div class="wrap split{" rev" if rev else ""}"><div class="rv"><span class="k2">{k}</span><h2>{h2}</h2><p>{p}</p>'
            + (f'<ul class="ticks">{li}</ul>' if li else '') + f'</div><div class="rv vis">{visual}</div></div></section>')

def cards(k, h2, p, items, bg=False, id_=''):
    c = ''.join(f'<div class="f rv">{clay(ic, col)}<h3>{t}</h3><p>{d}</p></div>' for ic, col, t, d in items)
    return (f'<section class="sx tight"{(" id="+chr(34)+id_+chr(34)) if id_ else ""}{" style=\"background:var(--mint)\"" if bg else ""}><div class="wrap">'
            f'<div class="hd2 rv"><span class="k">{k}</span><h2>{h2}</h2>{"<p>"+p+"</p>" if p else ""}</div><div class="feat{" f4" if len(items)==4 else ""}">{c}</div></div></section>')

def faqs(k, h2, qa):
    fq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in qa)
    return f'<section class="sx tight" id="faq"><div class="wrap" style="max-width:820px"><div class="hd2 rv"><span class="k">{k}</span><h2>{h2}</h2></div><div class="faq">{fq}</div></div></section>'

def hclay(*icons):
    a = ''.join(f'<span class="hc{i}">{clay(k, c, "lg")}</span>' for i, (k, c) in enumerate(icons))
    return f'<div class="hclay" aria-hidden="true"><span class="blob"></span><span class="mk">{HMARK}</span>{a}</div>'

def pdf_ui(t):
    rows = ''.join(f'<li><span>{a}</span><b>{b}</b></li>' for a, b in t['rows'])
    return (f'<div class="pdf"><div class="ph1"><span class="mk">{HMARK}</span><div><b>{t["title"]}</b><small>{t["sub"]}</small></div><em>PDF</em></div>'
            f'<ul>{rows}</ul><div class="need"><b>{t["need"]}</b><span>{t["n1"]}</span><span>{t["n2"]}</span></div></div>')

def camp_ui(t):
    return (f'<div class="camp"><div class="cmh">{clay("mega","#7c6cf2","sm")}<div><b>{t["name"]}</b><small>{t["aud"]}</small></div></div>'
            f'<div class="msg">{t["msg"]}</div><div class="cmf"><span class="ok">{t["ok"]}</span><span class="send">{t["send"]}</span></div></div>')

def toggles_ui(t):
    r = ''.join(f'<li><span>{a}</span><i class="tg{" on" if on else ""}" aria-hidden="true"></i></li>' for a, on in t)
    return f'<div class="tgl"><ul>{r}</ul></div>'

def ihub(items):
    a = ''.join(f'<div class="in">{clay(k, c)}<b>{n}</b><span class="st {s}">{l}</span></div>' for k, c, n, s, l in items)
    return f'<div class="ihub">{a}</div>'

def timeline(steps):
    s = ''.join(f'<li class="rv"><span class="n">{i+1}</span>{clay(ic, c)}<div><em>{d}</em><h3>{t}</h3><p>{p}</p></div></li>' for i, (ic, c, d, t, p) in enumerate(steps))
    return f'<ol class="tline">{s}</ol>'

def cmp3(head, rows, hl=3):
    def cell(v):
        if v == 'y': return '<span class="y">✓</span>'
        if v == 'n': return '<span class="n">✕</span>'
        return v
    th = ''.join(f'<th{" class=h" if i==hl else ""}>{h or chr(60)+"span class=vh>"+("المعيار" if any("\u0600"<=ch<="\u06ff" for ch in head[1]) else "What matters")+chr(60)+"/span>"}</th>' for i, h in enumerate(head))
    tr = ''.join('<tr>' + ''.join(f'<td data-l="{head[i]}"{" class=h" if i==hl else ""}>{cell(v)}</td>' for i, v in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="rv tscroll"><table class="cmp cmp3"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

C = {}  # content per language, filled below

def build(B, AR, home_en, home_ar):
    for lang, L, home in (('en', B.EN, home_en), ('ar', AR, home_ar)):
        c = C[lang]; p = L['pre']
        plans = re.search(r'<section id="plans">.*?</section>', home, re.S).group(0).replace('href="#pilot"', f'href="{p}/pilot/"')
        pilot = re.search(r'<section id="pilot">.*?</section>', home, re.S).group(0)
        homefaq = dict(re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', home[home.index('id="faq"'):], re.S))
        for slug, pg in c['pages'].items():
            body = pg['body'](c, plans, pilot, homefaq, p)
            page(B, L, lang, '/' + slug + '/', pg, body)

def page(B, L, lang, path, pg, body):
    url = L['pre'] + path; en, ar = path, '/ar' + path
    alt = ar if lang == 'en' else en
    c = C[lang]
    if pg.get('legal'):
        hero = f'''<section class="ph pg legal-h">
<div class="wrap"><div>
<div class="crumbs"><a href="{L['home']}">{L['crumb_home']}</a> / {pg['crumb']}</div>
<h1>{pg['h1']}</h1><p class="lead">{pg['lead']}</p>
</div></div></section>'''
    else:
      hero = f'''<section class="ph pg">
{V.bgfx()}
<div class="wrap"><div>
<div class="crumbs"><a href="{L['home']}">{L['crumb_home']}</a> / {pg['crumb']}</div>
<div style="margin-top:22px">{clay(pg['icon'][0], pg['icon'][1], 'lg')}</div>
<h1>{pg['h1']}</h1><p class="lead">{pg['lead']}</p>
<div class="cta cta1"><a class="bx gold go1" href="{V.T[lang]['gsurl']}">{V.T[lang]['gsfree']}<span class="ar" aria-hidden="true"></span></a><a class="bx quiet" href="/call/" data-call>{V.T[lang]['callq']}</a></div>
</div>{pg['visual']}</div></section>'''
    band = f'<section class="sx tight"><div class="wrap"><div class="cta-band rv"><h2>{L["band"]}</h2><div style="display:flex;gap:12px;flex-wrap:wrap"><a class="bx gold" href="{V.T[lang]["gsurl"]}">{V.T[lang]["gsfree"]}</a><a class="bx glass" href="{L["pre"]}/pricing/">{L["band2"]}</a></div></div></div></section>'
    html_ = f'''{L['body']}
{L['offer']}
{L['header'](alt)}
<main>
{hero}
{body}
{band if pg.get('band', True) else ''}
</main>
{L['footer'](alt)}
{L['askbar']()}
<button class="trybar" id="trybar" data-chat>{L['trybar']}</button>
<script src="/assets/site.js" defer></script>
<script src="/assets/x.js" defer></script>
<script src="/assets/v5.js" defer></script>
</body></html>'''
    ld = [B.crumbs_ld([(L['crumb_home'], L['home']), (_plain(pg['crumb']), url)]),
          {"@context": "https://schema.org", "@type": pg.get('type', 'WebPage'), "name": pg['title'], "description": pg['desc'], "url": B.SITE + url, "inLanguage": lang, "isPartOf": {"@type": "WebSite", "name": "Halora", "url": B.SITE + "/"}, "publisher": {"@id": B.SITE + "/#org"}}]
    qa = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', body)
    if qa: ld.append(B.faq_ld(qa))
    head = B.seo(L['head'] if 'head' in L else B.HEAD_EN, lang, pg['title'], pg['desc'], url, en, ar, ld)
    os.makedirs(f'{B.ROOT}{url}', exist_ok=True)
    open(f'{B.ROOT}{url}index.html', 'w', encoding='utf-8').write(head + '</head>\n' + html_)
    if lang == 'en' and path not in B.SUBPAGES: B.SUBPAGES.append(path)

# =====================================================================================
# English
# =====================================================================================
T = V.T
EN_STEPS = [('doc', '#0e5c57', 'Day 1', 'Setup form or a 20-minute call', 'Fill in the setup form in about 15 minutes, or go through it with us on a call. No preparation needed.'),
 ('cal', '#c98f22', 'Days 2–4', 'We build your Noor', 'Your price list, doctors, hours, insurance list and tone of voice. We connect your WhatsApp Business number and Google Calendar. You change nothing.'),
 ('users', '#7c6cf2', 'Days 4–6', 'Your team tests it', 'Message and call Noor from your own phones and tell us what to adjust. Approval mode lets you check replies before they are sent.'),
 ('flag', '#1f9d6b', 'Day 7', 'Go live with a free 14-day pilot', 'Noor starts answering real patients. After 14 days we look at the numbers together, and you decide.')]

C['en'] = dict(cta1='Start the free pilot', pages={
'how-it-works': dict(crumb='How it works', icon=('route', '#0e5c57'), title='How Halora works: live in about a week · Halora',
  desc='From a 20-minute call to Noor answering your patients: the four steps to go live with Halora, what we need from your clinic and what happens after launch.',
  h1='From first call to live <span class="glow">in about a week.</span>', lead='We do the setup. You give us your prices, doctors and hours, test Noor with your team, and switch her on with a free 14-day pilot.',
  visual=V.cal_ui(T['en']),
  body=lambda c, plans, pilot, hf, p: (
   f'<section class="sx tight"><div class="wrap" style="max-width:920px"><div class="hd2 rv"><span class="k">The four steps</span><h2>A clear path, <b>no surprises.</b></h2></div>{timeline(EN_STEPS)}</div></section>'
   + cards('What we need from you', 'Six things, <b>one short call.</b>', 'Send them by WhatsApp or email. Photos of a printed price list are fine.', [
     ('doc', '#0e5c57', 'Price list', 'Services and prices, or price ranges, that Noor may share.'), ('users', '#7c6cf2', 'Doctors & schedule', 'Who works when, and which services each doctor offers.'),
     ('cal', '#c98f22', 'Hours & holidays', 'Opening hours, Fridays, Ramadan timings and public holidays.'), ('shield', '#0f2523', 'Insurance list', 'Which insurers you accept. Your team confirms coverage.'),
     ('chat', '#1fa971', 'WhatsApp Business number', 'Access to connect it to the official WhatsApp Business API.'), ('sheet', '#14a3b8', 'A Google account', 'For the shared calendar and patient list.')], bg=True)
   + cards('After go-live', 'Noor keeps <b>getting better.</b>', '', [
     ('dash', '#0e5c57', 'Morning summary', 'A short report on WhatsApp every morning: bookings, after-hours replies and anything that needs your team.'),
     ('loop', '#3b8f5a', 'Weekly tweaks', 'New questions Noor could not answer are added to her knowledge, with your approval.'),
     ('star', '#d9a441', 'Monthly review', 'We go through bookings, no-shows and reviews with you and plan the next month.')])
   + faqs('Questions', 'Good to know', [('How long until Noor is live?', 'Usually about a week from the first call. The build itself takes about 48 hours once we have your prices, doctors and hours.'), ('Do I need technical skills?', 'No. We connect WhatsApp, the calendar and the website chat for you and train your team.'), ('Can we start with WhatsApp only?', 'Yes. Many clinics start with WhatsApp and website chat, then add the phone line later.')]))),

'pricing': dict(crumb='Pricing', icon=('tag', '#c98f22'), title='Pricing: plans, founding offer and free pilot · Halora',
  desc='Halora plans for clinics in Dubai and the Gulf, the founding clinic offer (25% off until 31 December 2026) and a free 14-day pilot on your own WhatsApp number.',
  h1='Simple monthly plans. <span class="glow">Start free for 14 days.</span>', lead='Every plan starts with a free 14-day pilot on your real WhatsApp number. Monthly, no long contract. Founding clinics get 25% off until 31 December.',
  visual=hclay(('tag', '#c98f22'), ('cal', '#0e5c57'), ('star', '#d9a441')), type='WebPage',
  body=lambda c, plans, pilot, hf, p: (plans
   + cards('Setup, explained', 'What the one-time <b>setup covers.</b>', '', [
     ('doc', '#0e5c57', 'Built with your information', 'Your services, prices, doctors, hours and policies, written into Noor’s knowledge.'),
     ('chat', '#1fa971', 'Your WhatsApp connected', 'Your clinic’s own WhatsApp Business number on the official API.'),
     ('cal', '#c98f22', 'Calendar and website chat', 'Google Calendar booking and the chat widget on your website.'),
     ('users', '#7c6cf2', 'Team training', 'How to take over a chat, use the portal and read the reports.')], bg=True)
   + faqs('Questions', 'About pricing', [(q, hf[q]) for q in ('What does WhatsApp charge?', 'How long does setup take?') if q in hf] + [('What happens after the free pilot?', 'If you continue, you pay the one-time setup and your first month. If Noor does not bring you bookings, you walk away and pay nothing.')]))),

'for-owners': dict(crumb='For owners', icon=('dash', '#7c6cf2'), title='For clinic owners: dashboard, inbox and daily report · Halora',
  desc='See every patient Noor brought in: the owner dashboard, inbox take-over in one click, a daily PDF report on WhatsApp and approved recall campaigns.',
  h1='See exactly what <span class="glow">Noor brought in.</span>', lead='A private portal for you and your team: every conversation, booking and request in one place, a summary on WhatsApp each morning, and campaigns that bring patients back.',
  visual=V.dash_ui(T['en']),
  body=lambda c, plans, pilot, hf, p: (
   split('Owner dashboard', 'Bookings, replies and revenue, <b>at a glance.</b>', 'Bookings made by Noor and their value, after-hours replies, phone calls and where patients came from, by day, week and month.', V.cal_ui(T['en']), ['Bookings by Noor and their value', 'After-hours replies and calls', 'Where patients came from'], band=True)
   + split('Inbox take-over', 'Step in <b>with one click.</b>', 'Every chat lives in one inbox. Take over any conversation from the portal or WhatsApp; Noor steps back and can pick up again later.',
           V.chat_ui(T['en'], 'Pearl Dental (demo)', [('p', 'Can Dr. Sara see my son after school?'), ('n', 'Let me check with the team for you.'), ('n', 'Hi, this is Reem from reception. Dr. Sara can see him at 16:00 tomorrow 😊')], 'Reem took over · Noor paused'), ['Owners see everything', 'Reception sees the inbox and requests', 'Hand back to Noor any time'], rev=True)
   + split('Daily PDF report', 'Your clinic’s night, <b>in one message.</b>', 'A short report lands on your WhatsApp every morning, with weekly and monthly summaries.',
           pdf_ui(dict(title='Morning summary', sub='Pearl Dental (demo) · Sunday', rows=[('Conversations', '37'), ('Bookings by Noor', '9'), ('After hours', '3'), ('Reminders sent', '14'), ('New Google reviews', '2')], need='Needs your team', n1='Ahmed K. · insurance question', n2='Layla S. · wants Dr. Sara only')), ['Bookings, calls and reminders', 'Who needs a callback', 'Weekly and monthly trends'])
   + split('Campaigns', 'Bring patients back, <b>with your approval.</b>', 'Send an approved WhatsApp message to the right patients, such as a 6-month cleaning recall. Patients can opt out any time.',
           camp_ui(dict(name='6-month cleaning recall', aud='84 patients due this month (sample)', msg='Hi {name}, it’s been 6 months since your last cleaning at Pearl Dental. Would you like us to book you in? Reply with a day that suits you.', ok='Approved ✓', send='Send')), ['Templates approved by you', 'Right patients, right time', 'Opt-out respected'], rev=True, id_='campaigns'))),

'security': dict(crumb='Safety & guardrails', icon=('shield', '#0f2523'), title='Safety and guardrails: what Noor will never do · Halora',
  desc='How Noor stays safe for clinics: no medical advice, never asks for ID or card details, instant human handover, switches you control, and data that stays in your own accounts.',
  h1='Built for a clinic, <span class="glow">not a call centre.</span>', lead='Noor answers only from information you approve, hands anything clinical or sensitive to your team, and you can switch every part on or off.',
  visual=toggles_ui([('Phone answering', True), ('After-hours only', False), ('Approval mode', True), ('Reminders', True), ('Review requests', True), ('Campaigns', False)]),
  body=lambda c, plans, pilot, hf, p: (
   cards('Guardrails', 'What Noor will <b>never do.</b>', '', [
     ('steth', '#0e5c57', 'No medical advice', 'Noor answers practical questions only. Clinical questions go to your doctors.'),
     ('shield', '#0f2523', 'No ID or card details', 'Noor never asks for Emirates ID, card numbers or medical history in chat.'),
     ('users', '#7c6cf2', 'A human when it matters', 'Complaints, bills and anything sensitive are handed to your staff straight away.'),
     ('bolt', '#e5484d', 'Emergencies first', 'Severe pain, bleeding or injury: the patient is told to get urgent care and your team is alerted.'),
     ('cal', '#1f9d6b', 'Only real bookings', 'Noor confirms a booking only after it is in your calendar. She never invents one.'),
     ('loop', '#c98f22', 'Approval mode', 'For the first weeks, you can approve Noor’s replies before they are sent.')])
   + split('Your data', 'Your data stays <b>in your accounts.</b>', 'Noor works on top of the accounts your clinic already owns. If you stop, everything stays with you.',
           ihub([('chat', '#1fa971', 'WhatsApp Business', 'ok', 'Your account'), ('cal', '#0e5c57', 'Google Calendar', 'ok', 'Your account'), ('sheet', '#14a3b8', 'Google Sheets', 'ok', 'Your account'), ('doc', '#61706c', 'Reports', 'ok', 'Sent to you')]),
           ['Conversations on your own WhatsApp Business number', 'Bookings in your own Google Calendar', 'Patient lists in your own Google Sheets', 'Noor collects only what is needed to book'], rev=True)
   + faqs('Questions', 'Good to know', [('Can I switch Noor off?', 'Yes, at any time, for one channel or all of them. Your team can also take over any single conversation.'), ('What if Noor does not know the answer?', 'She tells the patient a team member will reply, alerts your staff, and logs the question so you can add the answer for next time.'), ('Who can see the conversations?', 'You decide. Owners see everything; reception can be limited to the inbox and requests.')]))),

'integrations': dict(crumb='Integrations', icon=('plug', '#14a3b8'), title='Integrations: WhatsApp, phone, Google Calendar and more · Halora',
  desc='What Noor connects to today: the official WhatsApp Business API, your phone line (voice by ElevenLabs), Google Calendar, Google Sheets, a website chat widget and PDF reports. EMR on request.',
  h1='Works with the tools <span class="glow">you already use.</span>', lead='Noor connects to your WhatsApp Business number, your phone line, Google Calendar and Google Sheets. Practice management systems are possible on request.',
  visual=ihub([('chat', '#1fa971', 'WhatsApp', 'ok', 'Live'), ('phone', '#c98f22', 'Phone line', 'ok', 'Live'), ('cal', '#0e5c57', 'Google Calendar', 'ok', 'Live'), ('sheet', '#14a3b8', 'Google Sheets', 'ok', 'Live'), ('globe', '#5b7fd6', 'Website chat', 'ok', 'Live'), ('steth', '#b9811f', 'EMR / PMS', 'rq', 'On request')]),
  body=lambda c, plans, pilot, hf, p: (
   '<section class="sx tight"><div class="wrap"><div class="hd2 rv"><span class="k">Connected today</span><h2>Real integrations, <b>no surprises.</b></h2></div><div class="ints">'
   + ''.join(f'<div class="int rv"{" id="+chr(34)+i+chr(34) if i else ""}>{clay(k, col)}<div><h3>{n} <span class="st {s}">{l}</span></h3><p>{d}</p></div></div>' for k, col, n, s, l, d, i in [
     ('chat', '#1fa971', 'WhatsApp Business API', 'ok', 'Live', 'Your clinic’s own number on Meta’s official WhatsApp Cloud API. Text and voice notes, in and out.', 'whatsapp'),
     ('phone', '#c98f22', 'Phone line', 'ok', 'Live', 'Noor answers calls in a natural voice powered by ElevenLabs, on your existing line or a new one.', 'phone'),
     ('cal', '#0e5c57', 'Google Calendar', 'ok', 'Live', 'Noor checks real free slots and books, moves and cancels appointments in your shared calendar.', 'calendar'),
     ('sheet', '#14a3b8', 'Google Sheets', 'ok', 'Live', 'Patient lists, waitlist and requests kept in a sheet your team can open any time.', 'sheets'),
     ('globe', '#5b7fd6', 'Website chat widget', 'ok', 'Live', 'The same Noor on your website, so visitors book instead of leaving.', 'web'),
     ('doc', '#61706c', 'PDF reports', 'ok', 'Live', 'A daily summary on WhatsApp, plus weekly and monthly reports.', 'reports'),
     ('heart', '#d4669a', 'Instagram & Facebook messages', 'rq', 'On request', 'Noor can answer direct messages on your Instagram and Facebook pages. Set up on request; ask us on the call.', 'social'),
     ('steth', '#b9811f', 'EMR / practice management', 'rq', 'On request', 'Tell us which system you use. We check what is possible during the call; nothing is promised before that.', 'emr')])
   + '</div></div></section>'
   + faqs('Questions', 'Good to know', [('Do I need a new WhatsApp number?', 'No. Noor runs on your clinic’s WhatsApp Business number. We guide you through connecting it.'), ('Which calendar does it use?', 'Noor books into a shared Google Calendar. If your clinic uses a practice management system, tell us which one and we will check the options.')]))),

'about': dict(crumb='About', icon=('heart', '#b9811f'), title='About Halora: why we built Noor · Halora',
  desc='Halora was founded by Ziad Elhoseiny after seeing how many patient messages clinics in the Gulf never answer after hours. Why we built Noor and how we work.',
  h1='Clinics shouldn’t lose patients <span class="glow">after 6 pm.</span>', lead='Halora builds Noor, an AI receptionist for clinics in Dubai and the Gulf. We started with one simple observation: patients message when nobody is free to answer.',
  visual='<div class="letter rv"><span class="mk">' + HMARK + '</span><p>“Noor is not here to replace your receptionist. She is the colleague who covers the night shift, the weekend and the rush hour, and never forgets to follow up.”</p><b>Ziad Elhoseiny</b><small>Founder, Halora</small></div>',
  body=lambda c, plans, pilot, hf, p: (
   '<section class="sx tight"><div class="wrap story rv"><span class="k2">Why Halora exists</span><h2>A simple problem, <b>every evening.</b></h2>'
   '<p>Clinics in the Gulf get a large share of their enquiries in the evening, on Fridays and during the busy hour at reception. Many patients message several clinics at once on WhatsApp, and the first clear answer with a time often wins the booking.</p>'
   '<p>Ziad started Halora after seeing how many of those messages went unanswered, not because clinics did not care, but because nobody was free at the right moment. Noor is the answer to that: a receptionist who replies in seconds, in Arabic and English, and books straight into the clinic’s calendar.</p>'
   '<p>We are a small, founder-led company. When you start a pilot, Ziad sets it up with you personally and stays on WhatsApp with you until it works the way your clinic needs.</p></div></section>'
   + cards('How we work', 'What we <b>believe.</b>', '', [
     ('users', '#7c6cf2', 'Noor helps your team', 'She takes the repetitive and after-hours work so your team can look after the patients in front of them.'),
     ('shield', '#0f2523', 'Honest by default', 'Our demo clinics are fictional and labelled as such. We show sample numbers as samples.'),
     ('sheet', '#14a3b8', 'Your clinic, your data', 'Noor works on your own WhatsApp, calendar and sheets. If you leave, everything stays with you.')], bg=True)
   + '<section class="sx tight"><div class="wrap" style="max-width:820px;text-align:center"><div class="rv"><span class="k2">Talk to the founder</span><h2 class="h2c">Questions? <b>Write to Ziad directly.</b></h2><p class="muted"><a href="mailto:ziad.elhoseiny@askhalora.com" dir="ltr">ziad.elhoseiny@askhalora.com</a></p><p><a class="bx dark" href="/call/" data-call>Book a 20-minute call</a></p></div></div></section>')),

'compare': dict(crumb='Compare', icon=('scale', '#d4669a'), title='Front desk vs call centre vs Noor: an honest comparison · Halora',
  desc='An honest comparison of three ways to answer clinic patients: your front desk alone, an outsourced call centre, and your front desk with Noor, the AI receptionist.',
  h1='Front desk, call centre <span class="glow">or Noor?</span>', lead='An honest look at three ways to answer your patients. Noor works best alongside your team, not instead of it.',
  visual=hclay(('users', '#7c6cf2'), ('phone', '#c98f22'), ('chat', '#1fa971')),
  body=lambda c, plans, pilot, hf, p: (
   '<section class="sx tight"><div class="wrap" style="max-width:1040px"><div class="hd2 rv"><span class="k">Side by side</span><h2>What each option <b>really covers.</b></h2></div>'
   + cmp3(['', 'Front desk only', 'Outsourced call centre', 'Front desk + Noor'], [
     ('Answers at 2 am, Fridays and Eid', 'n', 'Often, at extra cost', 'y'),
     ('First reply on WhatsApp in under 10 seconds', 'When someone is free', 'Depends on the queue', 'y'),
     ('Knows your prices, doctors and policies', 'y', 'From a script', 'From your approved info'),
     ('Books straight into your calendar', 'y', 'Often takes a message', 'y'),
     ('Arabic and English, voice notes too', 'Depends on staff', 'Depends on the agent', 'y'),
     ('Handles many chats at the same time', 'n', 'One per agent', 'y'),
     ('Reminders, waitlist and review requests', 'When remembered', 'n', 'y'),
     ('Warm, in-person care at the desk', 'y', 'n', 'Your team, freed up'),
     ('You see every conversation', 'Partly', 'Reports on request', 'Owner dashboard'),
     ('Cost', 'Salary, visa and leave', 'Per-agent or per-minute fees', f'<a href="{p}/pricing/">See plans</a>')])
   + '</div></section>'
   + cards('Where each one shines', 'Honest <b>strengths.</b>', '', [
     ('users', '#7c6cf2', 'Your front desk', 'Warmth, judgement and care for the patients standing in front of them. Nothing replaces that.'),
     ('phone', '#c98f22', 'A call centre', 'Useful for very high call volumes that need a human on every call, if the budget allows.'),
     ('chat', '#1fa971', 'Noor', 'The repetitive questions, after-hours messages, bookings, reminders and follow-ups, in seconds.')], bg=True))),

'pilot': dict(crumb='Free pilot', icon=('flag', '#3b8f5a'), title='Free 14-day pilot: try Noor on your own patients · Halora',
  desc='Try Noor free for 14 days on your clinic’s real WhatsApp number. We set it up with your prices, doctors and hours. If it does not bring bookings, you pay nothing.',
  h1='Try Noor on your own patients, <span class="glow">free for 14 days.</span>', lead='We set everything up with your real prices, doctors and hours. If Noor does not bring you bookings, you walk away and pay nothing.',
  visual=V.chat_ui(T['en']), band=False,
  body=lambda c, plans, pilot, hf, p: (
   cards('What the pilot includes', 'Everything, <b>for real.</b>', 'Not a sandbox: Noor answers your actual patients on your own number.', [
     ('doc', '#0e5c57', 'Built with your information', 'Services, prices, doctors, hours and policies.'), ('chat', '#1fa971', 'Your own WhatsApp number', 'Connected to the official WhatsApp Business API.'),
     ('cal', '#c98f22', 'Your calendar', 'Real bookings in your Google Calendar.'), ('loop', '#c98f22', 'Approval mode', 'Check Noor’s replies before they go out, if you like.'),
     ('users', '#7c6cf2', 'Team training', 'How to take over a chat and read the reports.'), ('dash', '#0e5c57', 'A review after 14 days', 'We go through the numbers together. You decide.')], bg=True)
   + pilot
   + faqs('Questions', 'About the pilot', [('What does the pilot cost?', 'Nothing. If you continue after 14 days, you pay the one-time setup and your first month, as shown on the pricing page.'), ('Do I need to sign a contract?', 'No. Plans are monthly with no long contract.'), ('What if it does not work for us?', 'You walk away and pay nothing. Your WhatsApp number, calendar and data stay yours.')]))),
})
# =====================================================================================
# Arabic
# =====================================================================================
AR_STEPS = [('doc', '#0e5c57', 'اليوم 1', 'نموذج الإعداد أو مكالمة 20 دقيقة', 'املأ نموذج الإعداد في حوالي 15 دقيقة، أو راجعه معنا في مكالمة. لا تحتاج أي تحضير.'),
 ('cal', '#c98f22', 'الأيام 2–4', 'نجهّز نور لعيادتك', 'قائمة أسعارك وأطباؤك ومواعيدك وشركات التأمين وأسلوبكم في الكلام. نربط رقم واتساب للأعمال وتقويم Google، دون أن تغيّر شيئًا.'),
 ('users', '#7c6cf2', 'الأيام 4–6', 'فريقك يجرّبها', 'راسلوا نور واتصلوا بها من هواتفكم وأخبرونا بما تريدون تعديله. وضع الموافقة يتيح لك مراجعة الردود قبل إرسالها.'),
 ('flag', '#1f9d6b', 'اليوم 7', 'الإطلاق مع تجربة مجانية 14 يومًا', 'تبدأ نور بالرد على مرضى حقيقيين. وبعد 14 يومًا نراجع الأرقام معًا، والقرار لك.')]
TA = T['ar']
C['ar'] = dict(cta1='ابدأ التجربة المجانية', pages={
'how-it-works': dict(crumb='كيف تعمل', icon=('route', '#0e5c57'), title='كيف تعمل هالورا: جاهزة خلال أسبوع تقريبًا · هالورا',
  desc='من مكالمة 20 دقيقة إلى نور ترد على مرضاك: أربع خطوات للإطلاق مع هالورا، وما نحتاجه من عيادتك، وماذا يحدث بعد الإطلاق.',
  h1='من أول مكالمة إلى الإطلاق <span class="glow">خلال أسبوع تقريبًا.</span>', lead='نحن نتولى الإعداد. ترسل لنا أسعارك وأطباءك ومواعيدك، ويجرّب فريقك نور، ثم تبدأ مع تجربة مجانية لمدة 14 يومًا.',
  visual=V.cal_ui(TA),
  body=lambda c, plans, pilot, hf, p: (
   f'<section class="sx tight"><div class="wrap" style="max-width:920px"><div class="hd2 rv"><span class="k">الخطوات الأربع</span><h2>طريق واضح، <b>بلا مفاجآت.</b></h2></div>{timeline(AR_STEPS)}</div></section>'
   + cards('ما نحتاجه منك', 'ستة أشياء، <b>ومكالمة قصيرة.</b>', 'أرسلها عبر واتساب أو البريد. صورة لقائمة أسعار مطبوعة تكفي.', [
     ('doc', '#0e5c57', 'قائمة الأسعار', 'الخدمات والأسعار أو نطاقاتها التي يمكن لنور مشاركتها.'), ('users', '#7c6cf2', 'الأطباء والجدول', 'من يعمل ومتى، وما الخدمات التي يقدّمها كل طبيب.'),
     ('cal', '#c98f22', 'المواعيد والعطلات', 'ساعات الدوام والجمعة ومواعيد رمضان والعطل الرسمية.'), ('shield', '#0f2523', 'شركات التأمين', 'شركات التأمين التي تتعاملون معها، وفريقك يؤكد التغطية.'),
     ('chat', '#1fa971', 'رقم واتساب للأعمال', 'صلاحية لربطه بمنصة واتساب للأعمال الرسمية.'), ('sheet', '#14a3b8', 'حساب Google', 'للتقويم المشترك وقائمة المرضى.')], bg=True)
   + cards('بعد الإطلاق', 'نور <b>تتحسن باستمرار.</b>', '', [
     ('dash', '#0e5c57', 'ملخص الصباح', 'تقرير قصير على واتساب كل صباح: الحجوزات والردود بعد الدوام وما يحتاج فريقك.'),
     ('loop', '#3b8f5a', 'تحسينات أسبوعية', 'الأسئلة الجديدة التي لم تعرف نور إجابتها تُضاف لمعرفتها بموافقتك.'),
     ('star', '#d9a441', 'مراجعة شهرية', 'نراجع معك الحجوزات والغياب والتقييمات ونخطط للشهر القادم.')])
   + faqs('أسئلة', 'معلومات تهمّك', [('متى تصبح نور جاهزة؟', 'عادةً خلال أسبوع تقريبًا من أول مكالمة. والإعداد نفسه يستغرق حوالي 48 ساعة بعد استلام الأسعار والأطباء والمواعيد.'), ('هل أحتاج خبرة تقنية؟', 'لا. نحن نربط واتساب والتقويم ودردشة الموقع وندرّب فريقك.'), ('هل نستطيع البدء بواتساب فقط؟', 'نعم. كثير من العيادات تبدأ بواتساب ودردشة الموقع، ثم تضيف خط الهاتف لاحقًا.')]))),

'pricing': dict(crumb='الأسعار', icon=('tag', '#c98f22'), title='الأسعار: الباقات وعرض المؤسسين والتجربة المجانية · هالورا',
  desc='باقات هالورا لعيادات دبي والخليج، وعرض العيادات المؤسِّسة (خصم 25% حتى 31 ديسمبر 2026)، وتجربة مجانية لمدة 14 يومًا على رقم واتساب عيادتك.',
  h1='باقات شهرية بسيطة. <span class="glow">ابدأ مجانًا لمدة 14 يومًا.</span>', lead='كل باقة تبدأ بتجربة مجانية لمدة 14 يومًا على رقم واتساب الحقيقي. اشتراك شهري بدون عقد طويل، وخصم 25% للعيادات المؤسِّسة حتى 31 ديسمبر.',
  visual=hclay(('tag', '#c98f22'), ('cal', '#0e5c57'), ('star', '#d9a441')),
  body=lambda c, plans, pilot, hf, p: (plans
   + cards('الإعداد بالتفصيل', 'ماذا يشمل <b>الإعداد لمرة واحدة.</b>', '', [
     ('doc', '#0e5c57', 'مبنية بمعلوماتك', 'خدماتك وأسعارك وأطباؤك ومواعيدك وسياساتك في معرفة نور.'),
     ('chat', '#1fa971', 'ربط واتساب عيادتك', 'رقم واتساب للأعمال الخاص بعيادتك على المنصة الرسمية.'),
     ('cal', '#c98f22', 'التقويم ودردشة الموقع', 'الحجز في تقويم Google ونافذة الدردشة على موقعك.'),
     ('users', '#7c6cf2', 'تدريب الفريق', 'كيف تتدخّل في محادثة، وتستخدم البوابة، وتقرأ التقارير.')], bg=True)
   + faqs('أسئلة', 'عن الأسعار', [(q, hf[q]) for q in ('كم تكلفة رسائل واتساب؟', 'كم يستغرق التجهيز؟') if q in hf] + [('ماذا يحدث بعد التجربة المجانية؟', 'إذا قررت الاستمرار، تدفع رسوم الإعداد لمرة واحدة والشهر الأول. وإذا لم تجلب نور حجوزات، تنسحب دون أن تدفع شيئًا.')]))),

'for-owners': dict(crumb='لأصحاب العيادات', icon=('dash', '#7c6cf2'), title='لأصحاب العيادات: لوحة التحكم والرسائل والتقرير اليومي · هالورا',
  desc='شاهد كل مريض جاء عن طريق نور: لوحة المالك، والتدخل في المحادثة بنقرة، وتقرير PDF يومي على واتساب، وحملات متابعة توافق عليها.',
  h1='شاهد بالضبط ما <span class="glow">جلبته نور.</span>', lead='بوابة خاصة لك ولفريقك: كل محادثة وحجز وطلب في مكان واحد، وملخص على واتساب كل صباح، وحملات تعيد المرضى.',
  visual=V.dash_ui(TA),
  body=lambda c, plans, pilot, hf, p: (
   split('لوحة المالك', 'الحجوزات والردود والإيراد <b>بنظرة واحدة.</b>', 'الحجوزات التي تمت عن طريق نور وقيمتها، والردود بعد الدوام، والمكالمات، ومصدر المرضى، يوميًا وأسبوعيًا وشهريًا.', V.cal_ui(TA), ['الحجوزات عبر نور وقيمتها', 'الردود والمكالمات بعد الدوام', 'من أين جاء المرضى'], band=True)
   + split('التدخل في المحادثة', 'تدخّل <b>بنقرة واحدة.</b>', 'كل المحادثات في صندوق واحد. تدخّل في أي محادثة من البوابة أو من واتساب، ونور تتوقف ويمكنها أن تكمل لاحقًا.',
           V.chat_ui(TA, 'عيادة بيرل للأسنان (تجريبية)', [('p', 'ممكن د. سارة تشوف ولدي بعد المدرسة؟'), ('n', 'خليني أتأكد لك من الفريق.'), ('n', 'مرحبا، معك ريم من الاستقبال. د. سارة تقدر تشوفه بكرة الساعة 4 العصر 😊')], 'تدخّلت ريم · نور متوقفة'), ['المالك يرى كل شيء', 'الاستقبال يرى الرسائل والطلبات', 'أعد المحادثة لنور متى شئت'], rev=True)
   + split('تقرير PDF يومي', 'ليلة عيادتك <b>في رسالة واحدة.</b>', 'تقرير قصير يصلك على واتساب كل صباح، مع ملخص أسبوعي وشهري.',
           pdf_ui(dict(title='ملخص الصباح', sub='عيادة بيرل (تجريبية) · الأحد', rows=[('المحادثات', '37'), ('حجوزات عبر نور', '9'), ('بعد الدوام', '3'), ('تذكيرات مُرسلة', '14'), ('تقييمات Google جديدة', '2')], need='يحتاج فريقك', n1='أحمد ك. · سؤال عن التأمين', n2='ليلى س. · تفضّل د. سارة فقط')), ['الحجوزات والمكالمات والتذكيرات', 'من يحتاج اتصالًا', 'اتجاهات أسبوعية وشهرية'])
   + split('الحملات', 'أعد المرضى، <b>بموافقتك.</b>', 'أرسل رسالة واتساب توافق عليها للمرضى المناسبين، مثل تذكير التنظيف كل 6 أشهر. ويمكن للمريض إيقاف الرسائل في أي وقت.',
           camp_ui(dict(name='تذكير التنظيف كل 6 أشهر', aud='84 مريضًا مستحقًا هذا الشهر (مثال)', msg='مرحبا {الاسم}، مرّت 6 أشهر على آخر تنظيف في عيادة بيرل. تحب نحجز لك موعد؟ أرسل لنا اليوم المناسب لك.', ok='تمت الموافقة ✓', send='إرسال')), ['رسائل توافق عليها أنت', 'المرضى المناسبون في الوقت المناسب', 'احترام إلغاء الاشتراك'], rev=True, id_='campaigns'))),

'security': dict(crumb='الأمان والضوابط', icon=('shield', '#0f2523'), title='الأمان والضوابط: ما لن تفعله نور أبدًا · هالورا',
  desc='كيف تبقى نور آمنة للعيادات: لا نصائح طبية، ولا طلب للهوية أو بيانات البطاقة، وتحويل فوري لموظف، ومفاتيح تتحكم بها، وبيانات تبقى في حسابات عيادتك.',
  h1='مصمّمة لعيادة، <span class="glow">لا لمركز اتصال.</span>', lead='نور تجيب فقط من معلومات توافق عليها، وتحوّل أي أمر طبي أو حساس لفريقك، ويمكنك تشغيل أو إيقاف كل جزء منها.',
  visual=toggles_ui([('الرد على المكالمات', True), ('بعد الدوام فقط', False), ('وضع الموافقة', True), ('التذكيرات', True), ('طلبات التقييم', True), ('الحملات', False)]),
  body=lambda c, plans, pilot, hf, p: (
   cards('الضوابط', 'ما لن تفعله نور <b>أبدًا.</b>', '', [
     ('steth', '#0e5c57', 'لا نصائح طبية', 'نور تجيب عن الأسئلة العملية فقط، والأسئلة الطبية تذهب لأطبائك.'),
     ('shield', '#0f2523', 'لا هوية ولا بيانات بطاقة', 'نور لا تطلب الهوية الإماراتية أو أرقام البطاقات أو التاريخ المرضي في المحادثة.'),
     ('users', '#7c6cf2', 'موظف عند الحاجة', 'الشكاوى والفواتير وأي أمر حساس تُحوَّل لفريقك فورًا.'),
     ('bolt', '#e5484d', 'الحالات الطارئة أولًا', 'ألم شديد أو نزيف أو إصابة: يُنصح المريض بطلب رعاية عاجلة ويُنبَّه فريقك.'),
     ('cal', '#1f9d6b', 'حجوزات حقيقية فقط', 'لا تؤكد نور الحجز إلا بعد إضافته فعلًا في تقويمك، ولا تخترع حجزًا.'),
     ('loop', '#c98f22', 'وضع الموافقة', 'في الأسابيع الأولى يمكنك الموافقة على ردود نور قبل إرسالها.')])
   + split('بياناتك', 'بياناتك تبقى <b>في حساباتك.</b>', 'نور تعمل فوق الحسابات التي تملكها عيادتك أصلًا. وإذا توقفت، يبقى كل شيء معك.',
           ihub([('chat', '#1fa971', 'واتساب للأعمال', 'ok', 'حسابك'), ('cal', '#0e5c57', 'تقويم Google', 'ok', 'حسابك'), ('sheet', '#14a3b8', 'Google Sheets', 'ok', 'حسابك'), ('doc', '#61706c', 'التقارير', 'ok', 'تُرسل لك')]),
           ['المحادثات على رقم واتساب للأعمال الخاص بك', 'الحجوزات في تقويم Google الخاص بك', 'قوائم المرضى في Google Sheets الخاصة بك', 'نور تجمع فقط ما يلزم للحجز'], rev=True)
   + faqs('أسئلة', 'معلومات تهمّك', [('هل أستطيع إيقاف نور؟', 'نعم، في أي وقت، لقناة واحدة أو لكل القنوات. ويمكن لفريقك التدخل في أي محادثة.'), ('ماذا لو لم تعرف نور الإجابة؟', 'تخبر المريض أن أحد الفريق سيرد، وتنبّه موظفيك، وتسجّل السؤال لتضيف إجابته لاحقًا.'), ('من يستطيع رؤية المحادثات؟', 'أنت تقرر. المالك يرى كل شيء، ويمكن حصر الاستقبال في الرسائل والطلبات.')]))),

'integrations': dict(crumb='التكاملات', icon=('plug', '#14a3b8'), title='التكاملات: واتساب والهاتف وتقويم Google والمزيد · هالورا',
  desc='ما تتصل به نور اليوم: منصة واتساب للأعمال الرسمية، وخط هاتفك (صوت من ElevenLabs)، وتقويم Google، وGoogle Sheets، ودردشة الموقع، وتقارير PDF. وأنظمة الملفات الطبية عند الطلب.',
  h1='تعمل مع الأدوات <span class="glow">التي تستخدمها أصلًا.</span>', lead='نور تتصل برقم واتساب للأعمال وخط هاتفك وتقويم Google وGoogle Sheets. وأنظمة إدارة العيادات ممكنة عند الطلب.',
  visual=ihub([('chat', '#1fa971', 'واتساب', 'ok', 'متاح'), ('phone', '#c98f22', 'خط الهاتف', 'ok', 'متاح'), ('cal', '#0e5c57', 'تقويم Google', 'ok', 'متاح'), ('sheet', '#14a3b8', 'Google Sheets', 'ok', 'متاح'), ('globe', '#5b7fd6', 'دردشة الموقع', 'ok', 'متاح'), ('steth', '#b9811f', 'الملف الطبي', 'rq', 'عند الطلب')]),
  body=lambda c, plans, pilot, hf, p: (
   '<section class="sx tight"><div class="wrap"><div class="hd2 rv"><span class="k">متصلة اليوم</span><h2>تكاملات حقيقية، <b>بلا مفاجآت.</b></h2></div><div class="ints">'
   + ''.join(f'<div class="int rv"{" id="+chr(34)+i+chr(34) if i else ""}>{clay(k, col)}<div><h3>{n} <span class="st {s}">{l}</span></h3><p>{d}</p></div></div>' for k, col, n, s, l, d, i in [
     ('chat', '#1fa971', 'واتساب للأعمال (API)', 'ok', 'متاح', 'رقم عيادتك على منصة واتساب السحابية الرسمية من Meta. نصوص ورسائل صوتية في الاتجاهين.', 'whatsapp'),
     ('phone', '#c98f22', 'خط الهاتف', 'ok', 'متاح', 'نور ترد على المكالمات بصوت طبيعي من ElevenLabs، على خطك الحالي أو خط جديد.', 'phone'),
     ('cal', '#0e5c57', 'تقويم Google', 'ok', 'متاح', 'نور تتحقق من المواعيد المتاحة فعلًا وتحجزها وتغيّرها وتلغيها في تقويمك المشترك.', 'calendar'),
     ('sheet', '#14a3b8', 'Google Sheets', 'ok', 'متاح', 'قوائم المرضى وقائمة الانتظار والطلبات في ملف يفتحه فريقك متى شاء.', 'sheets'),
     ('globe', '#5b7fd6', 'دردشة الموقع', 'ok', 'متاح', 'نفس نور على موقعك، ليحجز الزوار بدل أن يغادروا.', 'web'),
     ('doc', '#61706c', 'تقارير PDF', 'ok', 'متاح', 'ملخص يومي على واتساب، مع تقارير أسبوعية وشهرية.', 'reports'),
     ('heart', '#d4669a', 'رسائل إنستغرام وفيسبوك', 'rq', 'عند الطلب', 'يمكن لنور الرد على الرسائل الخاصة في صفحات إنستغرام وفيسبوك. تُفعَّل عند الطلب، اسألنا في المكالمة.', 'social'),
     ('steth', '#b9811f', 'الملف الطبي / نظام إدارة العيادة', 'rq', 'عند الطلب', 'أخبرنا بالنظام الذي تستخدمه، ونتحقق من الإمكانيات خلال المكالمة. لا نعد بشيء قبل ذلك.', 'emr')])
   + '</div></div></section>'
   + faqs('أسئلة', 'معلومات تهمّك', [('هل أحتاج رقم واتساب جديد؟', 'لا. نور تعمل على رقم واتساب للأعمال الخاص بعيادتك، ونرشدك في ربطه.'), ('أي تقويم تستخدم؟', 'نور تحجز في تقويم Google مشترك. وإذا كانت عيادتك تستخدم نظام إدارة، أخبرنا به ونتحقق من الخيارات.')]))),

'about': dict(crumb='عن هالورا', icon=('heart', '#b9811f'), title='عن هالورا: لماذا بنينا نور · هالورا',
  desc='أسّس زياد الحسيني هالورا بعد أن رأى كم رسالة من المرضى لا تُرد في عيادات الخليج بعد الدوام. لماذا بنينا نور وكيف نعمل.',
  h1='العيادات لا يجب أن تخسر مرضاها <span class="glow">بعد السادسة مساءً.</span>', lead='هالورا تبني نور، موظفة الاستقبال الذكية لعيادات دبي والخليج. بدأنا من ملاحظة بسيطة: المرضى يراسلون حين لا يكون أحد متفرغًا للرد.',
  visual='<div class="letter rv"><span class="mk">' + HMARK + '</span><p>«نور ليست هنا لتحل محل موظفة الاستقبال، بل هي الزميلة التي تغطي المناوبة الليلية وعطلة نهاية الأسبوع ووقت الذروة، ولا تنسى المتابعة أبدًا.»</p><b>زياد الحسيني</b><small>مؤسس هالورا</small></div>',
  body=lambda c, plans, pilot, hf, p: (
   '<section class="sx tight"><div class="wrap story rv"><span class="k2">لماذا هالورا</span><h2>مشكلة بسيطة، <b>كل مساء.</b></h2>'
   '<p>تصل لعيادات الخليج نسبة كبيرة من الاستفسارات في المساء وأيام الجمعة ووقت الذروة في الاستقبال. كثير من المرضى يراسلون عدة عيادات في نفس الوقت على واتساب، وأول رد واضح بموعد يكسب الحجز غالبًا.</p>'
   '<p>بدأ زياد هالورا بعد أن رأى كم من هذه الرسائل يبقى بلا رد، ليس لأن العيادات لا تهتم، بل لأن لا أحد متفرغ في اللحظة المناسبة. نور هي الحل: موظفة استقبال ترد خلال ثوانٍ بالعربية والإنجليزية وتحجز مباشرة في تقويم العيادة.</p>'
   '<p>نحن شركة صغيرة يقودها المؤسس. عندما تبدأ التجربة، يجهّزها زياد معك شخصيًا ويبقى معك على واتساب حتى تعمل بالطريقة التي تحتاجها عيادتك.</p></div></section>'
   + cards('كيف نعمل', 'ما <b>نؤمن به.</b>', '', [
     ('users', '#7c6cf2', 'نور تساعد فريقك', 'تتولى العمل المتكرر وما بعد الدوام ليهتم فريقك بالمرضى الموجودين أمامه.'),
     ('shield', '#0f2523', 'الصدق أولًا', 'عياداتنا التجريبية وهمية ومكتوب عليها ذلك، والأرقام النموذجية نعرضها كأمثلة.'),
     ('sheet', '#14a3b8', 'عيادتك وبياناتك', 'نور تعمل على واتساب وتقويم وملفات عيادتك. وإذا غادرت، يبقى كل شيء معك.')], bg=True)
   + '<section class="sx tight"><div class="wrap" style="max-width:820px;text-align:center"><div class="rv"><span class="k2">تحدّث مع المؤسس</span><h2 class="h2c">لديك سؤال؟ <b>راسل زياد مباشرة.</b></h2><p class="muted"><a href="mailto:ziad.elhoseiny@askhalora.com" dir="ltr">ziad.elhoseiny@askhalora.com</a></p><p><a class="bx dark" href="/call/?lang=ar" data-call>احجز مكالمة 20 دقيقة</a></p></div></div></section>')),

'compare': dict(crumb='المقارنة', icon=('scale', '#d4669a'), title='الاستقبال أم مركز الاتصال أم نور: مقارنة صادقة · هالورا',
  desc='مقارنة صادقة بين ثلاث طرق للرد على مرضى العيادة: الاستقبال وحده، ومركز اتصال خارجي، والاستقبال مع نور موظفة الاستقبال الذكية.',
  h1='الاستقبال، مركز اتصال، <span class="glow">أم نور؟</span>', lead='نظرة صادقة على ثلاث طرق للرد على مرضاك. نور تعمل بأفضل شكل إلى جانب فريقك، لا بدلًا منه.',
  visual=hclay(('users', '#7c6cf2'), ('phone', '#c98f22'), ('chat', '#1fa971')),
  body=lambda c, plans, pilot, hf, p: (
   '<section class="sx tight"><div class="wrap" style="max-width:1040px"><div class="hd2 rv"><span class="k">جنبًا إلى جنب</span><h2>ما الذي يغطيه <b>كل خيار فعلًا.</b></h2></div>'
   + cmp3(['', 'الاستقبال وحده', 'مركز اتصال خارجي', 'الاستقبال + نور'], [
     ('ترد الساعة 2 فجرًا والجمعة والأعياد', 'n', 'غالبًا، بتكلفة إضافية', 'y'),
     ('أول رد على واتساب خلال أقل من 10 ثوانٍ', 'عند التفرغ', 'حسب الانتظار', 'y'),
     ('تعرف أسعارك وأطباءك وسياساتك', 'y', 'من نص مكتوب', 'من معلوماتك المعتمدة'),
     ('تحجز مباشرة في تقويمك', 'y', 'غالبًا تأخذ رسالة', 'y'),
     ('عربي وإنجليزي ورسائل صوتية', 'حسب الموظف', 'حسب الموظف', 'y'),
     ('محادثات كثيرة في نفس الوقت', 'n', 'محادثة لكل موظف', 'y'),
     ('تذكيرات وقائمة انتظار وطلبات تقييم', 'عند التذكر', 'n', 'y'),
     ('رعاية إنسانية دافئة في الاستقبال', 'y', 'n', 'فريقك، بوقت أكثر'),
     ('ترى كل محادثة', 'جزئيًا', 'تقارير عند الطلب', 'لوحة المالك'),
     ('التكلفة', 'راتب وإقامة وإجازات', 'رسوم لكل موظف أو دقيقة', f'<a href="{p}/pricing/">اطّلع على الباقات</a>')])
   + '</div></section>'
   + cards('أين يتميز كل خيار', 'نقاط قوة <b>بصدق.</b>', '', [
     ('users', '#7c6cf2', 'فريق الاستقبال', 'الدفء وحسن التقدير والاهتمام بالمرضى الموجودين أمامهم. لا شيء يعوّض ذلك.'),
     ('phone', '#c98f22', 'مركز الاتصال', 'مفيد عند حجم مكالمات كبير جدًا يحتاج موظفًا في كل مكالمة، إذا سمحت الميزانية.'),
     ('chat', '#1fa971', 'نور', 'الأسئلة المتكررة ورسائل ما بعد الدوام والحجوزات والتذكيرات والمتابعة، خلال ثوانٍ.')], bg=True))),

'pilot': dict(crumb='التجربة المجانية', icon=('flag', '#3b8f5a'), title='تجربة مجانية 14 يومًا: جرّب نور مع مرضاك · هالورا',
  desc='جرّب نور مجانًا لمدة 14 يومًا على رقم واتساب عيادتك الحقيقي. نجهّزها بأسعارك وأطبائك ومواعيدك، وإذا لم تجلب حجوزات لا تدفع شيئًا.',
  h1='جرّب نور مع مرضاك الحقيقيين <span class="glow">مجانًا لمدة 14 يومًا.</span>', lead='نجهّز كل شيء بأسعارك وأطبائك ومواعيدك الحقيقية. وإذا لم تجلب لك نور حجوزات، تنسحب دون أن تدفع شيئًا.',
  visual=V.chat_ui(TA), band=False,
  body=lambda c, plans, pilot, hf, p: (
   cards('ماذا تشمل التجربة', 'كل شيء، <b>بشكل حقيقي.</b>', 'ليست بيئة تجريبية: نور ترد على مرضاك الفعليين على رقمك.', [
     ('doc', '#0e5c57', 'مبنية بمعلوماتك', 'الخدمات والأسعار والأطباء والمواعيد والسياسات.'), ('chat', '#1fa971', 'رقم واتساب عيادتك', 'مربوط بمنصة واتساب للأعمال الرسمية.'),
     ('cal', '#c98f22', 'تقويمك', 'حجوزات حقيقية في تقويم Google الخاص بك.'), ('loop', '#c98f22', 'وضع الموافقة', 'راجع ردود نور قبل إرسالها إذا أردت.'),
     ('users', '#7c6cf2', 'تدريب الفريق', 'كيف تتدخّل في محادثة وتقرأ التقارير.'), ('dash', '#0e5c57', 'مراجعة بعد 14 يومًا', 'نراجع الأرقام معًا، والقرار لك.')], bg=True)
   + pilot
   + faqs('أسئلة', 'عن التجربة', [('كم تكلّف التجربة؟', 'لا شيء. وإذا استمررت بعد 14 يومًا، تدفع رسوم الإعداد لمرة واحدة والشهر الأول كما في صفحة الأسعار.'), ('هل أحتاج توقيع عقد؟', 'لا. الباقات شهرية بدون عقد طويل.'), ('ماذا لو لم تناسبنا؟', 'تنسحب دون أن تدفع شيئًا، ويبقى رقم واتساب والتقويم والبيانات ملكك.')]))),
})


# =====================================================================================
# Legal pages (plain language; have them reviewed by a lawyer before relying on them)
# =====================================================================================
UPDATED = {'en': 'Last updated: 22 November 2026', 'ar': 'آخر تحديث: 22 نوفمبر 2026'}
def article(lang, sections):
    toc = ''.join(f'<li><a href="#s{i+1}">{h}</a></li>' for i, (h, _) in enumerate(sections))
    body = ''.join(f'<section id="s{i+1}"><h2>{h}</h2>{t}</section>' for i, (h, t) in enumerate(sections))
    return (f'<section class="sx tight legal"><div class="wrap"><div class="lg-grid"><nav class="toc" aria-label="{"On this page" if lang=="en" else "في هذه الصفحة"}"><b>{"On this page" if lang=="en" else "في هذه الصفحة"}</b><ol>{toc}</ol></nav>'
            f'<article class="doc"><p class="upd">{UPDATED[lang]}</p>{body}</article></div></div></section>')

MAIL = '<a href="mailto:ziad.elhoseiny@askhalora.com" dir="ltr">ziad.elhoseiny@askhalora.com</a>'
PRIV_EN = [
 ('Who we are', f'<p>Halora builds Noor, an AI receptionist for clinics in Dubai and the Gulf. In this policy, “we” means Halora. You can reach us at {MAIL}.</p>'),
 ('What we collect on this website', '<ul><li><b>Forms:</b> when you fill in the setup form, the pilot form or book a call, we collect what you type: your name, clinic name, WhatsApp number, email, city and the clinic details you share.</li><li><b>Demo chat and voice demo:</b> messages you send to the demo Noor are processed to generate replies. The demo clinics are fictional and no real appointment is made.</li><li><b>Basic technical data:</b> our hosting provider may log standard information such as your IP address and browser type for security.</li></ul>'),
 ('How we use it', '<p>To reply to you, set up and run your pilot or subscription, book calls, improve Noor and keep the service secure. We do not sell your data and we do not use it for third-party advertising.</p>'),
 ('Patient data at clinics using Noor', '<p>When a clinic uses Noor, the clinic decides how its patient data is used, and we process it on the clinic’s behalf only to provide the service. Conversations run on the clinic’s own WhatsApp Business number, bookings go into the clinic’s own Google Calendar and patient lists stay in the clinic’s own Google Sheets.</p><p><b>Data & safety:</b> Noor never asks patients for ID numbers, card details or medical history, never gives medical advice, and hands anything sensitive to the clinic’s team.</p>'),
 ('Service providers', '<p>To run the service we use trusted providers, for example: Meta (WhatsApp Business Platform), Google (Calendar and Sheets), our automation and hosting providers, ElevenLabs for the phone voice, and AI model providers that process messages to write Noor’s replies. They only receive what they need to do their part.</p>'),
 ('How long we keep data', '<p>We keep enquiry and form data while we are in contact with you, and for as long as you are a customer. Demo chat data is cleaned up regularly. You can ask us to delete your data at any time.</p>'),
 ('Your choices and rights', f'<p>You can ask to see, correct or delete the personal data we hold about you, or ask us to stop contacting you. Email {MAIL} and we will reply within a reasonable time.</p>'),
 ('Cookies and storage', '<p>We do not use advertising or tracking cookies. The website uses your browser’s local and session storage only for small conveniences, for example to remember that you have already seen the opening animation.</p>'),
 ('Changes', '<p>If we change this policy, we will update this page and the date at the top.</p>'),
]
PRIV_AR = [
 ('من نحن', f'<p>هالورا تبني نور، موظفة استقبال ذكية للعيادات في دبي والخليج. في هذه السياسة، «نحن» تعني هالورا. يمكنك التواصل معنا عبر {MAIL}.</p>'),
 ('ما نجمعه على هذا الموقع', '<ul><li><b>النماذج:</b> عندما تملأ نموذج الإعداد أو نموذج التجربة أو تحجز مكالمة، نجمع ما تكتبه: اسمك واسم العيادة ورقم واتساب والبريد الإلكتروني والمدينة وتفاصيل العيادة التي تشاركها.</li><li><b>الدردشة والعرض الصوتي التجريبي:</b> الرسائل التي ترسلها لنور التجريبية تُعالَج لكتابة الردود. العيادات التجريبية وهمية ولا يتم حجز أي موعد حقيقي.</li><li><b>بيانات تقنية أساسية:</b> قد يسجّل مزوّد الاستضافة معلومات عادية مثل عنوان IP ونوع المتصفح لأغراض الأمان.</li></ul>'),
 ('كيف نستخدمها', '<p>للرد عليك، وتجهيز وتشغيل التجربة أو الاشتراك، وحجز المكالمات، وتحسين نور، والحفاظ على أمان الخدمة. لا نبيع بياناتك ولا نستخدمها لإعلانات جهات أخرى.</p>'),
 ('بيانات المرضى في العيادات التي تستخدم نور', '<p>عندما تستخدم عيادة نور، فالعيادة هي من تقرر كيفية استخدام بيانات مرضاها، ونحن نعالجها نيابة عنها فقط لتقديم الخدمة. المحادثات تتم على رقم واتساب للأعمال الخاص بالعيادة، والحجوزات في تقويم Google الخاص بها، وقوائم المرضى في ملفات Google Sheets الخاصة بها.</p><p><b>البيانات والأمان:</b> نور لا تطلب من المرضى أرقام الهوية أو بيانات البطاقات أو التاريخ المرضي، ولا تقدّم نصائح طبية، وتحوّل أي أمر حساس لفريق العيادة.</p>'),
 ('مزوّدو الخدمة', '<p>لتشغيل الخدمة نستعين بمزوّدين موثوقين، مثل: Meta (منصة واتساب للأعمال)، وGoogle (التقويم وSheets)، ومزوّدي الأتمتة والاستضافة، وElevenLabs للصوت في الهاتف، ومزوّدي نماذج الذكاء الاصطناعي التي تعالج الرسائل لكتابة ردود نور. ولا يحصلون إلا على ما يحتاجونه لأداء دورهم.</p>'),
 ('مدة الاحتفاظ بالبيانات', '<p>نحتفظ ببيانات الاستفسارات والنماذج طوال فترة تواصلنا معك، وطوال فترة اشتراكك. وتُحذف بيانات الدردشة التجريبية بشكل دوري. يمكنك أن تطلب منا حذف بياناتك في أي وقت.</p>'),
 ('خياراتك وحقوقك', f'<p>يمكنك أن تطلب الاطلاع على بياناتك الشخصية لدينا أو تصحيحها أو حذفها، أو أن نتوقف عن التواصل معك. راسلنا على {MAIL} وسنرد خلال وقت معقول.</p>'),
 ('ملفات تعريف الارتباط والتخزين', '<p>لا نستخدم ملفات تعريف ارتباط إعلانية أو للتتبّع. يستخدم الموقع التخزين المحلي في متصفحك لأمور بسيطة فقط، مثل تذكّر أنك شاهدت مقدمة الموقع.</p>'),
 ('التغييرات', '<p>إذا غيّرنا هذه السياسة، سنحدّث هذه الصفحة والتاريخ في أعلاها.</p>'),
]
TERMS_EN = [
 ('The service', '<p>Halora provides Noor, an AI receptionist that answers a clinic’s patients on WhatsApp, website chat and, on some plans, the phone, books appointments and sends reports. Optional add-ons include a clinic website and reminders & reviews.</p>'),
 ('Free 14-day pilot', '<p>Every plan starts with a free 14-day pilot. You do not pay anything during the pilot. If you decide not to continue, you pay nothing.</p>'),
 ('Plans, prices and payment', '<p>Plans are monthly with no long contract. Prices are in US dollars, or the same amount in AED at a fixed rate, and are shown on the <a href="/pricing/">pricing page</a>. If you continue after the pilot, you pay the one-time setup fee (where it applies) and your first month. WhatsApp message fees from Meta are billed to your own WhatsApp account.</p>'),
 ('Founding clinic offer', '<p>Clinics that join by 31 December 2026 get founding prices (25% off the monthly price and the setup fee), locked for 12 months. After that, regular prices apply.</p>'),
 ('Cancelling', f'<p>You can cancel at any time by emailing {MAIL}. Noor stops answering at the end of the month you have paid for. Your WhatsApp number, calendar and data stay yours.</p>'),
 ('Your responsibilities', '<ul><li>Give us accurate information about your services, prices, doctors and hours, and tell us when it changes.</li><li>Make sure you are allowed to message your patients, including reminders and campaigns.</li><li>All medical decisions stay with your clinic’s qualified staff.</li></ul>'),
 ('What Noor does and does not do', '<p>Noor answers from the information you approve, never gives medical advice and hands sensitive or unusual conversations to your team. Like any software, Noor can make mistakes, so your team can review and take over any conversation at any time.</p>'),
 ('Demos', '<p>Demo clinics on this website, such as BrightSmile Dental, Glow Skin Clinic, Lumina Dental and Pearl Demo Dental, are fictional. Nothing booked in a demo is real.</p>'),
 ('Liability', '<p>We work hard to keep Noor reliable, but we cannot promise the service will always be uninterrupted or error-free. To the extent the law allows, our total liability is limited to the amount you paid us in the three months before the event.</p>'),
 ('Contact', f'<p>Questions about these terms? Email {MAIL}.</p>'),
]
TERMS_AR = [
 ('الخدمة', '<p>تقدّم هالورا نور، موظفة استقبال ذكية ترد على مرضى العيادة عبر واتساب ودردشة الموقع، والهاتف في بعض الباقات، وتحجز المواعيد وترسل التقارير. ومن الإضافات الاختيارية موقع العيادة والتذكير والتقييمات.</p>'),
 ('تجربة مجانية لمدة 14 يومًا', '<p>كل باقة تبدأ بتجربة مجانية لمدة 14 يومًا، ولا تدفع شيئًا خلالها. وإذا قررت عدم الاستمرار، لا تدفع شيئًا.</p>'),
 ('الباقات والأسعار والدفع', '<p>الباقات شهرية بدون عقد طويل. الأسعار بالدولار الأمريكي، أو ما يعادلها بالدرهم بسعر صرف ثابت، وهي موضحة في <a href="/ar/pricing/">صفحة الأسعار</a>. إذا استمررت بعد التجربة، تدفع رسوم الإعداد لمرة واحدة (إن وُجدت) والشهر الأول. ورسوم رسائل واتساب من Meta تُحسب على حساب واتساب الخاص بعيادتك.</p>'),
 ('عرض العيادات المؤسِّسة', '<p>العيادات التي تنضم حتى 31 ديسمبر 2026 تحصل على الأسعار المؤسِّسة (خصم 25% على السعر الشهري ورسوم الإعداد)، ثابتة لمدة 12 شهرًا، ثم تُطبَّق الأسعار العادية.</p>'),
 ('الإلغاء', f'<p>يمكنك الإلغاء في أي وقت بمراسلتنا على {MAIL}. تتوقف نور عن الرد في نهاية الشهر المدفوع. ويبقى رقم واتساب والتقويم والبيانات ملكك.</p>'),
 ('مسؤولياتك', '<ul><li>تزويدنا بمعلومات صحيحة عن خدماتك وأسعارك وأطبائك ومواعيدك، وإبلاغنا عند تغييرها.</li><li>التأكد من أنك مسموح لك بمراسلة مرضاك، بما في ذلك التذكيرات والحملات.</li><li>كل القرارات الطبية تبقى لدى الكادر المؤهل في عيادتك.</li></ul>'),
 ('ما تفعله نور وما لا تفعله', '<p>نور تجيب من المعلومات التي توافق عليها، ولا تقدّم نصائح طبية أبدًا، وتحوّل المحادثات الحساسة أو غير المعتادة لفريقك. وككل برنامج، قد تخطئ نور أحيانًا، لذلك يستطيع فريقك مراجعة أي محادثة والتدخّل فيها في أي وقت.</p>'),
 ('العروض التجريبية', '<p>العيادات التجريبية على هذا الموقع، مثل عيادة برايت سمايل وعيادة جلو للبشرة وعيادة لومينا للأسنان وعيادة بيرل التجريبية، عيادات وهمية، ولا يُعدّ أي حجز فيها حجزًا حقيقيًا.</p>'),
 ('المسؤولية', '<p>نعمل بجد لتبقى نور موثوقة، لكن لا يمكننا أن نعد بأن تعمل الخدمة دائمًا دون انقطاع أو أخطاء. وفي الحدود التي يسمح بها القانون، تقتصر مسؤوليتنا الإجمالية على المبلغ الذي دفعته لنا خلال الأشهر الثلاثة السابقة للحدث.</p>'),
 ('التواصل', f'<p>لديك سؤال عن هذه الشروط؟ راسلنا على {MAIL}.</p>'),
]
C['en']['pages']['privacy'] = dict(crumb='Privacy policy', icon=('shield', '#0f2523'), legal=True, band=False, visual='',
  title='Privacy policy · Halora', desc='How Halora collects, uses and protects personal data on askhalora.com and in the Noor AI receptionist service, in plain language.',
  h1='Privacy policy', lead='How we collect, use and protect personal data, in plain language.', body=lambda c, plans, pilot, hf, p: article('en', PRIV_EN))
C['en']['pages']['terms'] = dict(crumb='Terms', icon=('doc', '#0e5c57'), legal=True, band=False, visual='',
  title='Terms of service · Halora', desc='The terms for using Halora and Noor, the AI receptionist for clinics: free 14-day pilot, monthly plans, founding offer, cancelling and responsibilities.',
  h1='Terms of service', lead='The simple rules for using Halora and Noor.', body=lambda c, plans, pilot, hf, p: article('en', TERMS_EN))
C['ar']['pages']['privacy'] = dict(crumb='سياسة الخصوصية', icon=('shield', '#0f2523'), legal=True, band=False, visual='',
  title='سياسة الخصوصية · هالورا', desc='كيف تجمع هالورا البيانات الشخصية وتستخدمها وتحميها على موقع askhalora.com وفي خدمة نور، موظفة الاستقبال الذكية، بلغة واضحة.',
  h1='سياسة الخصوصية', lead='كيف نجمع البيانات الشخصية ونستخدمها ونحميها، بلغة واضحة.', body=lambda c, plans, pilot, hf, p: article('ar', PRIV_AR))
C['ar']['pages']['terms'] = dict(crumb='الشروط', icon=('doc', '#0e5c57'), legal=True, band=False, visual='',
  title='شروط الخدمة · هالورا', desc='شروط استخدام هالورا ونور، موظفة الاستقبال الذكية للعيادات: التجربة المجانية لمدة 14 يومًا، والباقات الشهرية، وعرض المؤسسين، والإلغاء والمسؤوليات.',
  h1='شروط الخدمة', lead='القواعد البسيطة لاستخدام هالورا ونور.', body=lambda c, plans, pilot, hf, p: article('ar', TERMS_AR))
