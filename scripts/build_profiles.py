"""Build the six organization READMEs and localized activity calendars."""
from pathlib import Path
from datetime import date, datetime, timedelta
from html import escape
import json

ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/'profile'
LANGUAGES=json.loads((ROOT/'i18n/profile.json').read_text())
DATA=json.loads((PROFILE/'assets/activity-data.json').read_text())
RAW='https://raw.githubusercontent.com/Workraken/.github/main/profile/'
BRAND='https://raw.githubusercontent.com/Workraken/WorKraken/main/assets/'
SPACER=BRAND+'team/spacer.svg'
PEOPLE=[('Ailin Pizarro','CEO','ailin-pizarro','https://www.linkedin.com/in/ailin-pizarro/'),('Joaquín Benítez','CTO','joaquin-benitez','https://www.linkedin.com/in/joaquinn-benitez/')]
SOCIAL=[('Instagram','instagram','https://www.instagram.com/WorKraken/'),('Facebook','facebook','https://www.facebook.com/WorKraken'),('LinkedIn','linkedin','https://www.linkedin.com/company/WorKraken'),('TikTok','tiktok','https://www.tiktok.com/@WorKraken'),('YouTube','youtube','https://www.youtube.com/@WorKraken'),('Pinterest','pinterest','https://www.pinterest.com/Workraken/'),('Threads','threads','https://www.threads.com/@workraken'),('X','x','https://x.com/WorKrakenApp')]
START=date.fromisoformat(DATA['start']); END=date.fromisoformat(DATA['end'])
UPDATED=datetime.fromisoformat(DATA['updated_at'])

def filename(code):
    return 'README.md' if code=='es' else f'README.{code}.md'

def calendar_name(code,theme):
    return f'activity-{theme}.svg' if code=='es' else f'activity-{theme}.{code}.svg'

def context(t):
    count=f'{DATA["unique_commits_last_year"]:,}'.replace(',',t['thousands'])
    stamp=f'{UPDATED.day}{"." if t["locale"]=="de-DE" else ""} {t["months"][UPDATED.month-1]} {UPDATED.year} · {UPDATED:%H:%M} (UTC−3)'
    return dict(count=count,days=DATA['active_days'],repos=DATA['repository_count'],stamp=stamp,start=START.strftime('%d/%m/%Y'),end=END.strftime('%d/%m/%Y'))

def selector(active):
    lines=['<p align="center">']
    for code,t in LANGUAGES.items():
        url='https://github.com/Workraken' if code=='es' else 'https://github.com/Workraken/.github/blob/main/profile/'+filename(code)
        src=RAW+f'assets/flags/{t["flag"]}-{"active" if code==active else "inactive"}.svg'
        lines.append(f'  <a href="{url}" title="{t["name"]}"><img src="{src}" alt="{t["name"]}" width="48" height="48" /></a>')
    return '\n'.join(lines+['</p>'])

def image_link(url,src,alt,title,width=64,height=64):
    return f'<a href="{escape(url,quote=True)}" title="{escape(title,quote=True)}"><img width="{width}" height="{height}" alt="{escape(alt,quote=True)}" src="{src}"></a>'

def build_readme(code,t):
    c=context(t)
    benefits='\n'.join(f'- **{lead}** {body}' for lead,body in t['benefits'])
    people=f'<img width="84" height="1" alt="" src="{SPACER}">'.join(image_link(url,BRAND+f'team/{slug}-circle.png',t['person_alt'].format(person=name,role=role),t['person_title'].format(person=name),96,96) for name,role,slug,url in PEOPLE)
    names=f'<img width="42" height="1" alt="" src="{SPACER}">'.join(f'<strong>{name}</strong> · {role}' for name,role,_,_ in PEOPLE)
    social='&nbsp;&nbsp;\n  '.join(image_link(url,BRAND+f'social/{slug}.svg',t['social_alt'].format(network=name),name) for name,slug,url in SOCIAL)
    email=image_link('mailto:workraken@gmail.com',BRAND+'social/email.svg',t['email_alt'],'Gmail')
    whatsapp=image_link('https://wa.me/542995050253',BRAND+'social/whatsapp.svg',t['whatsapp_alt'],'WhatsApp')
    alt=escape(t['calendar_alt'].format(**c),quote=True)
    return f'''{selector(code)}

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{BRAND}WorKraken-marca-oscura.png">
    <source media="(prefers-color-scheme: light)" srcset="{BRAND}WorKraken-marca-clara.png">
    <img src="{BRAND}WorKraken-marca-clara.png" width="560" alt="WorKraken">
  </picture>
</p>

<h1 align="center">{t['headline']}</h1>

<h3><strong>{t['subhead']}</strong></h3>

<p>{t['intro']}</p>

<h2>🧭 {t['manage']}</h2>

{benefits}

<h2>🛠️ {t['tools']}</h2>

- **{t['web_name']}** {t['web']}
- **{t['mobile_name']}** {t['mobile']}

<h2 align="center">👥 {t['team']}</h2>

<p align="center">
  {people}
</p>

<p align="center">
  {names}
</p>

<h2 align="center">🌐 {t['social']}</h2>

<p align="center">
  {social}<img width="1" height="72" alt="" src="{SPACER}">
</p>

<h2 align="center">📫 {t['contact']}</h2>

<p align="center">
  {email}&nbsp;&nbsp;
  {whatsapp}<img width="1" height="72" alt="" src="{SPACER}">
</p>

<h2 align="center">🔗 {t['discover']}</h2>

<p align="center">
  <a href="https://workraken.com" title="WorKraken"><img src="{BRAND}WorKraken-logo.png" width="360" alt="{t['visit']}"></a>
</p>

<!-- WORKRAKEN-ACTIVITY:START -->
<h2>{t['activity']}</h2>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{RAW}assets/{calendar_name(code,'dark')}">
    <source media="(prefers-color-scheme: light)" srcset="{RAW}assets/{calendar_name(code,'light')}">
    <img width="900" src="{RAW}assets/{calendar_name(code,'dark')}" alt="{alt}">
  </picture>
</p>

<p align="center">
  {t['individual']}
  <a href="https://github.com/Rey-de-Amarillo?tab=overview&amp;org=Workraken">Joaquín</a> ·
  <a href="https://github.com/Soy-Red?tab=overview&amp;org=Workraken">Ailin</a>
</p>

<details>
<summary>{t['method_title']}</summary>

{t['method_1'].format(**c)}

{t['method_2']}

</details>
<!-- WORKRAKEN-ACTIVITY:END -->
'''

def build_calendar(code,t,theme):
    c=context(t)
    dark=theme=='dark'
    bg='#0d1117' if dark else '#ffffff'; fg='#e6edf3' if dark else '#1f2328'
    muted='#9198a1' if dark else '#59636e'; border='#3d444d' if dark else '#d1d9e0'
    empty='#161b22' if dark else '#eff2f5'
    colors=[empty]+(['#0e4429','#006d32','#26a641','#39d353'] if dark else ['#9be9a8','#40c463','#30a14e','#216e39'])
    grid_start=START-timedelta(days=(START.weekday()+1)%7)
    nonzero=sorted(DATA['daily_commits'].values())
    thresholds=[nonzero[int((len(nonzero)-1)*q)] for q in (.25,.5,.75)]
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="420" viewBox="0 0 900 420" role="img" aria-labelledby="title desc" xml:lang="{t["locale"]}">',f'<title id="title">{escape(t["calendar_title"].format(**c))}</title>',f'<desc id="desc">{escape(t["calendar_alt"].format(**c))}</desc>',f'<rect x=".5" y=".5" width="899" height="419" rx="7" fill="{bg}" stroke="{border}"/>',f'<g font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" fill="{fg}">']
    def text(x,y,value,size=14,color=None,anchor='start',weight=400):
        out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color or fg}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(value))}</text>')
    text(24,38,t['calendar_title'].format(**c),20,weight=500)
    text(876,37,f'{START.year}–{END.year}',14,muted,'end')
    previous_month=None
    for week in range(53):
        day=grid_start+timedelta(days=week*7)
        if day.month!=previous_month and week<51:
            text(66+week*15,74,t['months'][day.month-1],12,muted)
            previous_month=day.month
        for row in range(7):
            current=day+timedelta(days=row)
            if not START<=current<=END: continue
            count=DATA['daily_commits'].get(str(current),0)
            level=0 if count==0 else 1+sum(count>value for value in thresholds)
            out.append(f'<rect x="{66+week*15}" y="{90+row*15}" width="11" height="11" rx="2" fill="{colors[level]}"><title>{current}: {count} {"commit" if code=="it" else "commits"}</title></rect>')
    for row,label in zip((1,3,5),t['weekdays']):text(24,90+row*15+10,label,12,muted)
    text(24,218,t['calendar_scope'],12,muted)
    text(729,218,t['less'],12,muted,'end')
    for i,color in enumerate(colors):out.append(f'<rect x="{738+i*16}" y="208" width="11" height="11" rx="2" fill="{color}"/>')
    text(826,218,t['more'],12,muted)
    out.append(f'<path d="M1 242H899" stroke="{border}"/>')
    text(24,271,t['overview'],16,weight=500)
    values=[DATA['active_days'],DATA['opened_pull_requests_last_year'],DATA['opened_issues_last_year'],DATA['repository_count']]
    for i,(value,label) in enumerate(zip(values,t['metrics'])):
        x=24+i*218
        if i:out.append(f'<path d="M{x-16}293V349" stroke="{border}"/>')
        text(x,321,value,29,weight=500); text(x,346,label,13,muted)
    out.append(f'<path d="M1 373H899" stroke="{border}"/>')
    text(24,400,t['as_of']+' '+c['stamp'],12,muted);text(876,400,'WorKraken',12,muted,'end')
    out.append('</g></svg>')
    return '\n'.join(out)+'\n'

for code,t in LANGUAGES.items():
    assert set(t)==set(LANGUAGES['es']),f'Incomplete translation: {code}'
    (PROFILE/filename(code)).write_text(build_readme(code,t))
    for theme in ('dark','light'):
        (PROFILE/'assets'/calendar_name(code,theme)).write_text(build_calendar(code,t,theme))
    print(f'{code}: README + dark/light calendars')
