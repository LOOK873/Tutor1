# -*- coding: utf-8 -*-
"""Render tutor-mode (practice) pages from _tutor/src/*.json + _tutor/data/<key>_*.json.
Web version -> เว็บ/<sub>/drill-*.html ; standalone -> ติว/คณิต|PHY/อ่าน/ฝึกทำ-*.html"""
import json, glob, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # .../เว็บ
ROOT = os.path.dirname(BASE)                                                 # .../ติว

PAGES = {
 'tutorial':    dict(sub='calc', web='drill-tutorial-m1.html', name='Tutorial Class M1', subj='math', read='คณิต', file='ฝึกทำ-Tutorial-Class-M1.html', src='tutorial-m1.html', pdf='Tutorial-Class-M1.pdf'),
 'classmarker': dict(sub='calc', web='drill-classmarker.html', name='ClassMarker + ข้อเขียน', subj='math', read='คณิต', file='ฝึกทำ-ClassMarker-ข้อเขียน.html', src='classmarker-vs-written.html'),
 'extra':       dict(sub='calc', web='drill-extra.html', name='แบบฝึกหัดเพิ่มเติม', subj='math', read='คณิต', file='ฝึกทำ-แบบฝึกหัดเพิ่มเติม.html', src='extra-exercises.html'),
 'class':       dict(sub='calc', web='drill-class.html', name='แบบฝึกหัดในคลาส', subj='math', read='คณิต', file='ฝึกทำ-แบบฝึกหัดในคลาส.html', src='class-solutions.html'),
 'phyex':       dict(sub='phy', web='drill-phy-examplesheet.html', name='PHY Example Sheet (24 ข้อ)', subj='phy', read='PHY', file='ฝึกทำ-PHY-ExampleSheet.html', sol='phy-examplesheet.html', solfile='เฉลย-PHY-ExampleSheet.html', pdf='PHY-ExampleSheet-24ข้อ.pdf'),
 'phymock':     dict(sub='phy', web='drill-phy-mock.html', name='PHY10101 ข้อสอบจำลอง 25 ข้อ + ข้อเขียน', subj='phy', read='PHY', file='ฝึกทำ-PHY10101-ข้อสอบจำลอง.html', sol='phy-mock-exam.html', solfile='เฉลย-PHY10101-ข้อสอบจำลอง.html', pdf='PHY10101-ติว-ข้อสอบจำลอง25ข้อ.pdf'),
 'phy':         dict(sub='phy',  web='drill-phy.html', name='PHY ตัวอย่างและแบบฝึกหัด', subj='phy', read='PHY', file='ฝึกทำ-PHY.html', src='phy-summary.html'),
}

def load_data(key):
    d = {}
    for f in sorted(glob.glob(os.path.join(BASE, '_tutor', 'data', key + '_*.json'))):
        d.update(json.load(open(f, encoding='utf-8')))
    return d

import re
def _fixtext(m):
    def f(t):
        x = t.group(1)
        return '\\text{' + x.replace('·', '}\\cdot\\text{') + '}' if '·' in x else t.group(0)
    return re.sub(r'\\text\{([^{}]*)\}', f, m.group(0))
def esc(s):  # data fields are trusted HTML+LaTeX; U+00B7 inside \text{} is undefined in KaTeX
    return re.sub(r'\$[^$]+\$', _fixtext, s) if '·' in s else s

def li(items): return ''.join('<li>%s</li>' % esc(x) for x in items)

def card(src, t, n, key):
    idx = str(src['idx'])
    h = ['<article class="q drill" id="p%d" data-idx="%s">' % (n, idx)]
    h.append('<h3><span class="num">%d</span> %s</h3>' % (n, src['title']))
    for pi in src.get('page_imgs', []):
        h.append('<details class="pgimg"><summary>🖼 ดูรูปโจทย์ต้นฉบับ (%s)</summary><img loading="lazy" src="img/%s" alt="โจทย์ต้นฉบับ" style="max-width:100%%;height:auto;background:#fff;border:1px solid #8884;border-radius:6px"></details>' % (pi, pi))
    im = {('tutorial', 6): 'tutorial-p3-fg.png', ('tutorial', 7): 'tutorial-p3-14.png'}.get((key, src['idx']))
    if im:
        h.append('<p><img src="img/%s" alt="กราฟโจทย์ (PDF หน้า 3)" style="max-width:100%%;width:420px;height:auto;background:#fff;border:1px solid #8884;border-radius:6px"></p>' % im)
    if t is None:
        h.append('<p class="alt">ยังไม่มีชุดฝึกของข้อนี้ — ดูเฉลยในหน้าเฉลยเดิม</p></article>')
        return '\n'.join(h)
    h.append('<p class="try">ลองทำเองก่อน แล้วค่อยเปิดความช่วยเหลือทีละระดับ <label class="done"><input type="checkbox" data-done="%s-%s"> ทำเองได้แล้ว</label></p>' % (key, idx))
    h.append('<textarea class="mine" data-note="%s-%s" rows="2" placeholder="เขียนความคิด/ขั้นแรกของคุณที่นี่ (บันทึกในเครื่องคุณ)"></textarea>' % (key, idx))
    h.append('<details class="lv l0"><summary>0 · แยกโจทย์: ข้อมูลที่ให้ / สิ่งที่ต้องหา / แนวคิด</summary><div class="lvb">'
             '<p><b>โจทย์ให้:</b></p><ul>%s</ul><p><b>ต้องหา:</b> %s</p><p><b>แนวคิดที่เกี่ยวข้อง:</b></p><ul>%s</ul></div></details>'
             % (li(t.get('given', [])), esc(t.get('find', '')), li(t.get('concept', []))))
    h.append('<details class="lv l1"><summary>1 · คำถามนำ</summary><div class="lvb"><p>%s</p></div></details>' % esc(t.get('h1', '')))
    h.append('<details class="lv l2"><summary>2 · หลักการที่ควรใช้</summary><div class="lvb"><p>%s</p></div></details>' % esc(t.get('h2', '')))
    h3 = t.get('h3') or {}
    h.append('<details class="lv l3"><summary>3 · ตัวอย่างคล้ายกัน (เปลี่ยนตัวเลข)</summary><div class="lvb"><p><b>โจทย์ตัวอย่าง:</b> %s</p><p><b>สาธิต:</b> %s</p></div></details>'
             % (esc(h3.get('q', '')), esc(h3.get('demo', ''))))
    steps = [s for s in src['steps'] if not s['final']]
    h.append('<details class="lv l4"><summary>4 · เฉลยทีละขั้น (เปิดเฉพาะขั้นที่ติด)</summary><div class="lvb">')
    for k, s in enumerate(steps, 1):
        h.append('<details class="stp"><summary>ขั้นที่ %d</summary><div class="steps"><div class="step"><div class="step-h">%s</div>%s</div></div></details>' % (k, s['head'], s['body']))
    h.append('</div></details>')
    # full solution
    fin = [s for s in src['steps'] if s['final']]
    h.append('<details class="lv l5"><summary>5 · เฉลยเต็ม + คำตอบ</summary><div class="lvb"><div class="steps">')
    for s in src['steps']:
        h.append('<div class="step%s"><div class="step-h">%s</div>%s</div>' % (' final' if s['final'] else '', s['head'], s['body']))
    h.append('</div>')
    if t.get('mistakes'):
        h.append('<p class="tip"><b>จุดพลาดที่พบบ่อย:</b></p><ul>%s</ul>' % li(t['mistakes']))
    h.append('</div></details>')
    # summary + practice
    sm = t.get('summary', [])
    pr = t.get('practice') or {}
    h.append('<div class="after"><p><b>สรุปหลักการ</b></p><ol>%s</ol>' % li(sm))
    if pr:
        h.append('<div class="prac"><p><b>ข้อฝึกใหม่:</b> %s</p>'
                 '<details><summary>ใบ้</summary><p>%s</p></details>'
                 '<details><summary>ดูคำตอบ</summary><p>%s</p><p class="alt">%s</p></details></div>'
                 % (esc(pr.get('q', '')), esc(pr.get('hint', '')), esc(pr.get('ans', '')), esc(pr.get('sol', ''))))
    h.append('</div></article>')
    return '\n'.join(h)

CSS = '''
  .drill{scroll-margin-top:4.5rem}
  .drill h3{font-size:1.1rem;margin:0 0 10px!important;display:flex;gap:.6rem;align-items:baseline}
  .drill .num{flex:none;font-weight:700;color:var(--accent,#2f6fde);background:var(--accentbg,rgba(47,111,222,.1));border-radius:8px;padding:0 .55rem;font-size:.9rem}
  .drill .try{margin:.3rem 0;color:var(--muted,#5b6370);font-size:.95rem}
  .drill .done{margin-left:.8rem;white-space:nowrap;cursor:pointer}
  .drill .mine{width:100%;box-sizing:border-box;border:1px dashed var(--line,#ccc);border-radius:10px;background:transparent;color:inherit;font:inherit;padding:8px 12px;margin:4px 0 8px;resize:vertical}
  .lv{border:1px solid var(--line,#ddd);border-radius:10px;margin:6px 0;padding:2px 12px}
  .lv>summary{cursor:pointer;font-weight:600;padding:6px 0;color:var(--accent,#2f6fde)}
  .lv .lvb{padding:2px 0 8px}
  .lv.l1{border-left:4px solid #38bdf8}.lv.l2{border-left:4px solid #818cf8}.lv.l3{border-left:4px solid #c084fc}.lv.l4{border-left:4px solid #f59e0b}.lv.l5{border-left:4px solid var(--ok,#1a7f4b)}
  .stp{margin:6px 0}.stp>summary{cursor:pointer;color:var(--muted,#5b6370)}
  .after{margin-top:12px;padding-top:8px;border-top:1px dashed var(--line,#ddd)}
  .prac{background:var(--accentbg,rgba(47,111,222,.08));border-radius:10px;padding:8px 14px;margin-top:8px}
  .alt{color:var(--muted,#5b6370);font-size:.92rem}
  .tip{color:var(--muted,#5b6370)}
  .progress{position:sticky;top:3.2rem;z-index:5;background:var(--card,#fff);border:1px solid var(--line,#ddd);border-radius:999px;padding:4px 14px;display:inline-block;font-size:.9rem;margin:0 0 12px}
  .katex-display{overflow-x:auto;overflow-y:hidden}
  @media print{details{display:block}details>*{display:block}.mine{display:none}}
'''
INLINE_THEME = '''
  :root{--bg:#fbfaf7;--fg:#1f2328;--muted:#5b6370;--card:#fff;--line:#e3e0d8;--accent:#2f6fde;--accentbg:rgba(47,111,222,.1);--link:#2f6fde;--ok:#1a7f4b;--okbg:#effaf3}
  @media(prefers-color-scheme:dark){:root{--bg:#0b0f1a;--fg:#e8ecf5;--muted:#8b93a7;--card:#131a2a;--line:#26304a;--accent:#7cc4f8;--accentbg:rgba(124,196,248,.12);--link:#7cc4f8;--ok:#4ade80;--okbg:#10281c}}
  body{background:var(--bg);color:var(--fg);font-family:'Anuphan','Sarabun',sans-serif;font-size:17px;line-height:1.95;margin:0}
  .q{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:0 0 16px}
  .steps{margin:12px 0;display:grid;gap:10px}
  .steps .step{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:10px;padding:8px 14px 4px}
  .steps .step-h{font-weight:700;color:var(--accent)}
  .steps .step.final{border-left-color:var(--ok);background:var(--okbg)}
  .steps .step.final .step-h{color:var(--ok)}
  a{color:var(--link)}
'''
WEB_BASE = '''
  main{max-width:820px;margin:0 auto;padding:24px 16px 64px}
  .q{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:0 0 16px}
  body{line-height:1.95;font-size:17px;margin:0}
'''
JS = '''<script>
(function(){
  var st={};function g(k){try{return localStorage.getItem(k)}catch(e){return null}}function s(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  var boxes=[].slice.call(document.querySelectorAll('[data-done]')),pg=document.getElementById('prog');
  function upd(){var n=boxes.filter(function(b){return b.checked}).length;if(pg)pg.textContent='ทำเองได้แล้ว '+n+' / '+boxes.length+' ข้อ'}
  boxes.forEach(function(b){var k='drill-'+b.dataset.done;b.checked=g(k)==='1';b.addEventListener('change',function(){s(k,b.checked?'1':'0');upd()})});
  [].slice.call(document.querySelectorAll('[data-note]')).forEach(function(t){var k='note-'+t.dataset.note;var v=g(k);if(v)t.value=v;t.addEventListener('input',function(){s(k,t.value)})});
  upd();
})();
</script>'''

def sol_card(src, n):
    h = ['<article class="q" id="p%d"><h3><span class="num">%d</span> %s</h3>' % (n, n, src['title'])]
    for pi in src.get('page_imgs', []):
        h.append('<details class="pgimg"><summary>🖼 ดูรูปโจทย์ต้นฉบับ (%s)</summary><img loading="lazy" src="img/%s" alt="โจทย์ต้นฉบับ" style="max-width:100%%;height:auto;background:#fff;border:1px solid #8884;border-radius:6px"></details>' % (pi, pi))
    h.append('<details><summary>ดูวิธีทำ</summary><div class="steps">')
    for s in src['steps']:
        h.append('<div class="step%s"><div class="step-h">%s</div>%s</div>' % (' final' if s['final'] else '', s['head'], s['body']))
    h.append('</div></details></article>')
    return chr(10).join(h)

def page(key, standalone, mode='drill'):
    cfg = PAGES[key]
    sp = os.path.join(BASE, '_tutor', 'src', key + '.json')
    if os.path.exists(sp):
        src = json.load(open(sp, encoding='utf-8'))
    else:
        src = []
        for f in sorted(glob.glob(os.path.join(BASE, '_tutor', 'src_parts', key + '_*.json'))):
            src += json.load(open(f, encoding='utf-8'))
        src.sort(key=lambda x: x['idx'])
    data = load_data(key)
    for s_ in src:
        s_['title'] = esc(s_['title'])
        for st_ in s_['steps']:
            st_['head'], st_['body'] = esc(st_['head']), esc(st_['body'])
    cards = []
    done = 0
    for n, s in enumerate(src, 1):
        t = data.get(str(s['idx']))
        if t: done += 1
        cards.append(sol_card(s, n) if mode == 'sol' else card(s, t, n, key))
    srclink = ((cfg.get('src') or cfg.get('sol') or '') if not standalone else '')
    title = ('เฉลย · ' if mode == 'sol' else 'ฝึกทำ · ') + cfg['name']
    pdf = ''
    if mode == 'sol':
        intro = '<h1>เฉลย · %s (%d ข้อ)</h1><p class="sub">เฉลยทีละขั้น · ต้นฉบับ: <a href="%s" target="_blank" rel="noopener">%s</a>%s</p>' % (cfg['name'], len(src), (cfg.get('pdf') or ''), (cfg.get('pdf') or ''), ('' if standalone else ' · <a href="%s">โหมดฝึกทำ</a>' % cfg['web']))
    else:
      intro = ('<h1>ฝึกทำ · %s (%d ข้อ)</h1><p class="sub">โหมดติวเตอร์: ลองคิดเองก่อน → เปิดคำใบ้ทีละระดับ (0 แยกโจทย์ · 1 คำถามนำ · 2 หลักการ · 3 ตัวอย่างคล้ายกัน · 4 เฉลยทีละขั้น · 5 เฉลยเต็ม) → สรุปหลักการ → ทำข้อฝึกใหม่ ' % (cfg['name'], len(src)))
      if srclink: intro += '· <a href="%s">ดูหน้าเฉลยเต็มแบบเดิม</a>' % srclink
      intro += '</p><div class="progress" id="prog"></div>'
    head = '''<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],strict:false})"></script>
<link href="https://fonts.googleapis.com/css2?family=Anuphan:wght@300;400;500;600;700&family=Bai+Jamjuree:wght@500;600;700&display=swap" rel="stylesheet">
<style>%s%s</style>
%s
</head>
<body>
<main>
%s
%s
</main>
%s
</body>
</html>
'''
    if standalone:
        return head % (title, INLINE_THEME + WEB_BASE, CSS, '', intro, '\n'.join(cards), JS), done, len(src)
    return head % (title, WEB_BASE, CSS, '<link rel="stylesheet" href="../theme.css"><script src="../exams.js"></script><script src="../theme.js"></script>', intro, '\n'.join(cards), JS), done, len(src)

if __name__ == '__main__':
    keys = sys.argv[1:] or list(PAGES)
    for k in keys:
        cfg = PAGES[k]
        html, done, total = page(k, False)
        with open(os.path.join(BASE, cfg['sub'], cfg['web']), 'w', encoding='utf-8') as f: f.write(html)
        html2, _, _ = page(k, True)
        d = os.path.join(ROOT, cfg['read'], 'อ่าน')
        if os.path.isdir(d):
            with open(os.path.join(d, cfg['file']), 'w', encoding='utf-8') as f: f.write(html2)
        print(k, 'data for %d/%d problems' % (done, total))
        if cfg.get('sol'):
            h3_, _, _ = page(k, False, 'sol')
            with open(os.path.join(BASE, cfg['sub'], cfg['sol']), 'w', encoding='utf-8') as f: f.write(h3_)
            h4_, _, _ = page(k, True, 'sol')
            if os.path.isdir(d):
                with open(os.path.join(d, cfg['solfile']), 'w', encoding='utf-8') as f: f.write(h4_)
