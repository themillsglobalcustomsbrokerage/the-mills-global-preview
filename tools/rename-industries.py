#!/usr/bin/env python3
"""Renames 14 industries (name + page address) to the client's SEO list. Cold Chain and Freight Forwarders keep their pages.
Safe to re-run: it only acts on old names/addresses."""
import re, glob, os, io, subprocess, json
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# old slug -> (new slug, new name, old names as they appear on the site)
M = {
 'construction': ('construction-and-infrastructure', 'Construction and Infrastructure', ['Construction & Infrastructure']),
 'renewable-energy': ('renewable-energy-and-power', 'Renewable Energy and Power', ['Renewable Energy & Power']),
 'mining': ('mining-and-minerals', 'Mining and Minerals', ['Mining, Minerals & Industrial Materials']),
 'manufacturing': ('industrial-manufacturing', 'Industrial Manufacturing', ['Manufacturing & Industrial Machinery', 'Manufacturing & Machinery']),
 'chemicals': ('chemicals-and-dangerous-goods', 'Chemicals and Dangerous Goods', ['Chemicals & Controlled Materials']),
 'data-centers': ('data-centers', 'Data Centers', ['Data Centers & Digital Infrastructure']),
 'marine': ('marine-and-offshore', 'Marine and Offshore', ['Marine, Vessels & Yachts']),
 'aviation': ('aviation-and-aerospace', 'Aviation and Aerospace', ['Aviation & Aerospace']),
 'healthcare': ('healthcare-and-pharmaceuticals', 'Healthcare and Pharmaceuticals', ['Pharma, Medical Devices & Healthcare', 'Pharma & Healthcare', 'Pharmaceuticals, Medical Devices & Healthcare']),
 'electronics-telecom': ('electronics-and-semiconductors', 'Electronics and Semiconductors', ['Telecom, Electronics & IT Hardware', 'Telecommunications, Electronics & IT Hardware']),
 'agriculture': ('agriculture-and-fisheries', 'Agriculture and Fisheries', ['Agriculture, Plants & Fisheries', 'Agriculture, Plants, Animals & Fisheries']),
 'food-beverage': ('fast-moving-consumer-goods', 'Fast-Moving Consumer Goods (FMCG)', ['Food, Beverage & Fast-Moving Consumer Goods (FMCG)', 'Food, Beverage & FMCG']),
 'automotive': ('automotive', 'Automotive', ['Automotive, Heavy Equipment & Special-Purpose Vehicles', 'Automotive & Heavy Equipment']),
 'retail': ('retail-and-e-commerce', 'Retail and E-Commerce', ['Retail, Consumer Goods & E-Commerce']),
}
# 1) rename the files
for old, (new, name, _) in M.items():
    src, dst = f'industries-{old}.html', f'industries-{new}.html'
    if src != dst and os.path.exists(src): subprocess.run(['git', 'mv', src, dst], check=True)
files = [f for f in glob.glob('*.html') + glob.glob('articles/*.html') + glob.glob('news/*.html') + glob.glob('tools/*.py') + glob.glob('tools/*.js') + glob.glob('n8n/**/*.json', recursive=True) + glob.glob('js/*.js') + ['sitemap.xml']
         if os.path.isfile(f) and not f.endswith('rename-industries.py')]
def both(s): return {s, s.replace('&', '&amp;')}
n = 0
for f in files:
    t = io.open(f, encoding='utf-8').read(); o = t
    for old, (new, name, olds) in M.items():
        # page address (not part of a longer word)
        t = re.sub(r'(?<![A-Za-z0-9_-])industries-' + re.escape(old) + r'(?![A-Za-z0-9_-])', 'industries-' + new, t)
        # names, longest first so "Pharma, Medical Devices & Healthcare" wins over "Pharma & Healthcare"
        for nm in sorted(olds, key=len, reverse=True):
            for v in both(nm): t = t.replace(v, name)
    if t != o: io.open(f, 'w', encoding='utf-8').write(t); n += 1
# 2) page headings: "Teams we support in X.", "Why X shipments usually get stuck.", "How The Mills handles X shipments."
for old, (new, name, _) in M.items():
    f = f'industries-{new}.html'; h = io.open(f, encoding='utf-8').read(); o = h
    m = re.search(r'Teams we support in (.*?)\.</h3>', h)
    if m and m.group(1) != name:
        short = re.escape(m.group(1))
        h = re.sub(r'Teams we support in ' + short + r'\.', f'Teams we support in {name}.', h)
        h = re.sub(r'Why ' + short + r' shipments usually get stuck\.', f'Why {name} shipments usually get stuck.', h)
        h = re.sub(r'How The Mills handles (?:an? )?' + short + r' shipments?\.', f'How The Mills handles {name} shipments.', h)
    if h != o: io.open(f, 'w', encoding='utf-8').write(h); n += 1
# 3) redirects from the old addresses
v = json.load(open('vercel.json')); have = {r['source'] for r in v['redirects']}
for old, (new, _, _) in M.items():
    if old == new: continue
    src = f'/industries-{old}(/)?'
    if src not in have: v['redirects'].append({'source': src, 'destination': f'/industries-{new}', 'permanent': True})
json.dump(v, open('vercel.json', 'w'), indent=2); open('vercel.json', 'a').write('\n')
print('renamed; files edited:', n)
