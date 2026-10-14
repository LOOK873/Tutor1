# -*- coding: utf-8 -*-
import json, sys
from bs4 import BeautifulSoup
PAGES = {
 'tutorial': 'calc/tutorial-m1.html',
 'classmarker': 'calc/classmarker-vs-written.html',
 'extra': 'calc/extra-exercises.html',
 'class': 'calc/class-solutions.html',
 'phy': 'phy/phy-summary.html',
}
inner = lambda t: ''.join(str(c) for c in t.contents)
for key, path in PAGES.items():
    d = BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')
    out = []
    for i, q in enumerate(d.select('div.q')):
        h = q.find(['h2', 'h3', 'h4'])
        det = q.find('details')
        if h is None: continue
        steps = []
        if det:
            for st in det.select('div.step'):
                hd = st.select_one('.step-h')
                hd_t = inner(hd) if hd else ''
                if hd: hd.extract()
                steps.append({'head': hd_t, 'body': inner(st), 'final': 'final' in (st.get('class') or [])})
            for c in det.select('.steps > p'):  # check lines inside steps
                pass
        extras = [str(p) for p in q.find_all('p', recursive=False)]
        out.append({'idx': i, 'title': inner(h), 'steps': steps, 'extras': extras,
                    'answer_line': next((inner(p) for p in q.find_all('p', recursive=False) if 'คำตอบ' in p.get_text()[:8]), '')})
    json.dump(out, open('_tutor/src/%s.json' % key, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(key, len(out), 'steps total', sum(len(o['steps']) for o in out))
