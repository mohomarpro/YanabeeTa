import os, re, json
from playwright.sync_api import sync_playwright

import sys, html as _h
# usage: python render_radar.py radar.json KIT_DIR OUT_DIR
#   KIT_DIR holds logo-white.png, logo-navy.png, fonts/ and node_modules/@phosphor-icons/core
DATA = json.load(open(sys.argv[1]))
KIT = os.path.abspath(sys.argv[2])
OUT = os.path.abspath(sys.argv[3])
ICONS = KIT + '/node_modules/@phosphor-icons/core/assets/duotone/'
os.makedirs(OUT, exist_ok=True)
def E(s): return _h.escape(str(s), quote=False)

NAVY, CY, GD = '#00214c', '#00c0ec', '#ecbc3c'
LIGHT, SUB, LN = '#f4fbfe', '#44597a', '#cdeaf4'

def ic(name, size=48, color='currentColor'):
    s = open(ICONS + name + '-duotone.svg').read()
    s = s.replace('<svg ', f'<svg width="{size}" height="{size}" style="color:{color};flex:none" ', 1)
    return s

AR = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
def n(x): return str(x).translate(AR)
import re as _re
def dg(t): return _re.sub(r'([٠-٩][٠-٩٪]*)', r'<span style="font-family:Almarai;font-weight:800">\1</span>', t)

FONTS = f'''
@font-face{{font-family:Alexandria;font-weight:500;src:url(file://{KIT}/fonts/alexandria-arabic-500-normal.woff2)}}
@font-face{{font-family:Alexandria;font-weight:700;src:url(file://{KIT}/fonts/alexandria-arabic-700-normal.woff2)}}
@font-face{{font-family:Alexandria;font-weight:800;src:url(file://{KIT}/fonts/alexandria-arabic-800-normal.woff2)}}
@font-face{{font-family:Almarai;font-weight:400;src:url(file://{KIT}/fonts/almarai-arabic-400-normal.woff2)}}
@font-face{{font-family:Almarai;font-weight:700;src:url(file://{KIT}/fonts/almarai-arabic-700-normal.woff2)}}
'''
BASE = FONTS + f'''
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:Almarai,sans-serif;direction:rtl;position:relative;overflow:hidden}}
.d{{font-family:Alexandria,sans-serif}}
'''

def page(css, body):
    return f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{BASE}.stage{{position:absolute;inset:0;width:1080px;height:1350px;overflow:hidden}}{css}</style></head><body><div class="stage">{body}</div></body></html>'

RADAR = f'''
<svg viewBox="0 0 800 800" width="900" height="900" style="position:absolute;left:-250px;top:262px;opacity:.9">
 <defs>
  <radialGradient id="sw" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{CY}" stop-opacity=".0"/><stop offset="1" stop-color="{CY}" stop-opacity=".42"/></radialGradient>
 </defs>
 <g fill="none" stroke="{CY}" stroke-opacity=".34" stroke-width="2">
  <circle cx="400" cy="400" r="390"/><circle cx="400" cy="400" r="290"/><circle cx="400" cy="400" r="190"/><circle cx="400" cy="400" r="90"/>
  <line x1="10" y1="400" x2="790" y2="400"/><line x1="400" y1="10" x2="400" y2="790"/>
 </g>
 <path d="M400 400 L400 10 A390 390 0 0 1 676 124 Z" fill="url(#sw)"/>
 <line x1="400" y1="400" x2="676" y2="124" stroke="{CY}" stroke-width="3" stroke-opacity=".8"/>
 <g fill="{GD}"><circle cx="560" cy="250" r="12"/><circle cx="470" cy="150" r="9"/><circle cx="300" cy="300" r="10"/></g>
 <g fill="none" stroke="{GD}" stroke-opacity=".5" stroke-width="2"><circle cx="560" cy="250" r="26"/><circle cx="300" cy="300" r="24"/></g>
</svg>'''

def header(i, total, dark=False):
    col = '#fff' if dark else NAVY
    return f'''<div style="position:absolute;top:56px;right:64px;left:64px;display:flex;align-items:center;justify-content:space-between;color:{col}">
      <div class="d" style="display:flex;align-items:center;gap:14px;font-size:30px;font-weight:700">{ic('broadcast',40,CYT if not dark else CY)}<span>الرادار التربوي</span></div>
      <div style="font-size:30px;font-weight:700;opacity:.75;font-family:Almarai">{n(i)} / {n(total)}</div></div>'''
CYT = '#0091b5'

def footer(dark=False):
    logo = 'logo-white.png' if dark else 'logo-navy.png'
    col = '#fff' if dark else NAVY
    return f'''<div style="position:absolute;bottom:48px;right:64px;left:64px;display:flex;align-items:center;justify-content:space-between;color:{col}">
      <img src="file://{KIT}/{logo}" style="height:78px">
      <div class="d" style="font-size:28px;font-weight:700;letter-spacing:.5px;opacity:.85;direction:ltr">@YanabeeTa</div></div>'''

EVENTS = DATA['events']
WEEK = DATA['week_label']
TOTAL = len(EVENTS) + 2

def cover():
    css = f'''body,.stage{{background:radial-gradient(120% 90% at 20% 30%,#06356f 0%,{NAVY} 60%,#001634 100%);color:#fff}}'''
    body = f'''{RADAR}
    <div style="position:absolute;top:70px;left:64px;direction:ltr;display:flex;flex-direction:column;align-items:center;gap:14px"><img src="file://{KIT}/logo-white.png" style="height:96px"><div class="d" style="font-size:26px;font-weight:700;letter-spacing:.5px;color:#9fb6d6;direction:ltr">@YanabeeTa</div><div style="display:flex;align-items:center;gap:16px;direction:ltr">{ic('telegram-logo',30,'#fff')}{ic('facebook-logo',30,'#fff')}{ic('instagram-logo',30,'#fff')}{ic('x-logo',30,'#fff')}{ic('threads-logo',30,'#fff')}</div></div>
    <div style="position:absolute;top:250px;right:64px;left:64px">
      <div class="d" style="display:inline-flex;align-items:center;gap:12px;background:rgba(0,192,236,.16);border:2px solid {CY};color:{CY};border-radius:999px;padding:11px 26px;font-size:27px;font-weight:700">{ic('target',34,CY)}<span>فقرة أسبوعية</span></div>
      <div class="d" style="font-size:150px;font-weight:800;line-height:1.1;margin-top:58px">الرادار<br><span style="color:{GD}">التربوي</span></div>
      <div style="font-size:42px;font-weight:700;line-height:1.55;margin-top:56px;max-width:820px;color:#dbe8f7">ما يهم الأسرة<br>خلال الأسبوع</div>
    </div>
    <div style="position:absolute;bottom:162px;right:64px;display:flex;align-items:center;gap:22px">
      <div class="d" style="display:flex;align-items:center;gap:16px;background:{GD};color:{NAVY};border-radius:999px;padding:20px 42px;font-size:37px;font-weight:800">اسحب لترى الأحداث {ic('arrow-left',44,NAVY)}</div>
    </div>
    <div class="d" style="position:absolute;bottom:60px;right:64px;left:64px;display:flex;justify-content:space-between;align-items:center;font-size:22px;font-weight:700;color:#9fb6d6">
      <span>{E(WEEK)}</span><span>{E(DATA.get('author','محمد عمر'))}</span></div>'''
    return page(css, body)

def event(i, e):
    css = f'''body,.stage{{background:{LIGHT};color:{NAVY}}}'''
    body = f'''{header(i + 1, TOTAL)}
    <div style="position:absolute;top:150px;right:64px;left:64px;bottom:150px;display:flex;flex-direction:column">
      <div style="display:flex;align-items:center;gap:22px">
        <div class="d" style="width:104px;height:104px;border-radius:50%;background:{NAVY};color:{GD};display:flex;align-items:center;justify-content:center;font-size:66px;font-weight:800;flex:none;font-family:Almarai">{n(i)}</div>
        <div class="d" style="background:#fff;border:2px solid {LN};color:{CYT};border-radius:999px;padding:10px 26px;font-size:28px;font-weight:700">{E(e['tag'])}</div>
      </div>
      <div class="d" style="font-size:64px;font-weight:800;line-height:1.38;margin-top:40px">{dg(E(e['title']))}</div>
      <div style="font-size:39px;line-height:1.7;color:{SUB};margin-top:34px;font-weight:400">{E(e['fact'])} <span dir="rtl" style="unicode-bidi:isolate;white-space:nowrap">({E(e['src'])})</span></div>
      <div style="margin-top:auto;background:#fff;border:3px solid {GD};border-radius:34px;padding:38px 42px 40px;box-shadow:0 10px 30px rgba(0,33,76,.07)">
        <div class="d" style="display:flex;align-items:center;gap:14px;color:#a87800;font-size:30px;font-weight:700">{ic('lightbulb',44,GD)}<span>التوصية التربوية</span></div>
        <div style="font-size:37px;line-height:1.7;margin-top:22px;color:{NAVY};font-weight:700">{E(e['act'])}</div>
        <div style="font-size:31px;line-height:1.6;margin-top:22px;color:{SUB}">قل له: «{E(e['say'])}»</div>
      </div>
    </div>
    {footer()}'''
    return page(css, body)

def cta():
    css = f'''body,.stage{{background:radial-gradient(120% 90% at 80% 20%,#06356f 0%,{NAVY} 60%,#001634 100%);color:#fff}}'''
    def row(icon, text, sub=''):
        return f'''<div style="display:flex;align-items:center;gap:26px;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.16);border-radius:30px;padding:20px 34px">
          {ic(icon,58,CY)}<div><div class="d" style="font-size:40px;font-weight:700">{text}</div>{f'<div style="font-size:29px;color:#b9cbe4;margin-top:6px;direction:ltr;text-align:right">{sub}</div>' if sub else ''}</div></div>'''
    body = f'''{header(TOTAL, TOTAL, True)}
    <div style="position:absolute;top:170px;right:64px;left:64px">
      <div class="d" style="font-size:88px;font-weight:800;line-height:1.3">أرسل الرادار<br><span style="color:{GD}">لشريكك في التربية</span></div>
      <div style="font-size:42px;line-height:1.6;color:#dbe8f7;margin-top:26px">لكل أب وأم ومعلّم يهمّه أمر أبنائه</div>
      <div style="display:flex;flex-direction:column;gap:18px;margin-top:40px">
        {row('share-network','شارك المنشور الآن')}
        {row('chat-circle-dots','هل رأيت خبرًا لم نذكره؟ اكتبه لنا')}
        {row('telegram-logo','اشترك في القناة','t.me/YanabeeTa')}
        {row('whatsapp-logo','واتس','wa.me/967702242300')}
      </div>
    </div>
    {footer(True)}'''
    return page(css, body)

pages = [('radar-01', cover())] + [(f'radar-{i+2:02d}', event(i + 1, e)) for i, e in enumerate(EVENTS)] + [(f'radar-{TOTAL:02d}', cta())]
report = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html in pages:
        path = f'{OUT}/{name}.html'
        open(path, 'w').write(html)
        pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=2)
        pg.goto('file://' + path)
        pg.wait_for_timeout(500)
        # overflow: any text element whose box leaves the 1080x1350 stage, or event body overlapping the recommendation box
        issues = pg.evaluate("""() => {
          const out = [];
          for (const el of document.querySelectorAll('.stage *')) {
            if (!el.childElementCount && el.textContent.trim()) {
              const r = el.getBoundingClientRect();
              if (r.right > 1080 + 1 || r.left < -1 || r.bottom > 1350 + 1 || r.top < -1) out.push('خارج الإطار: ' + el.textContent.trim().slice(0, 30));
            }
          }
          return out;
        }""")
        pg.screenshot(path=f'{OUT}/{name}.png')
        report.append({'file': name + '.png', 'issues': issues})
        pg.close()
    b.close()
print(json.dumps(report, ensure_ascii=False, indent=1))
