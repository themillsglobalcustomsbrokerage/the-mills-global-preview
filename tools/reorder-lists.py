#!/usr/bin/env python3
"""Puts every list of services and industries in the agreed order (Oct 2026):
   services: Mills Projects last; industries: Construction, Renewable Energy, Data Centers, Chemicals, Food & Beverage first,
   Freight Forwarders last. Idempotent."""
import re, glob, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SERVICE_ORDER = ['entry', 'permits', 'customs', 'marine', 'dangerous-goods', 'logistics', 'packaging', 'insurance', 'time-critical', 'advisory', 'projects']
INDUSTRY_ORDER = ['construction', 'renewable-energy', 'data-centers', 'chemicals', 'food-beverage', 'manufacturing', 'automotive', 'healthcare',
                  'agriculture', 'electronics-telecom', 'marine', 'aviation', 'retail', 'cold-chain', 'mining', 'freight-forwarders']
S = {k: i for i, k in enumerate(SERVICE_ORDER)}; I = {k: i for i, k in enumerate(INDUSTRY_ORDER)}


def rank(href):
    m = re.match(r'services-mills-([\w-]+)\.html', href)
    if m: return ('S', S[m.group(1)])
    m = re.match(r'industries-([\w-]+)\.html', href)
    if m: return ('I', I[m.group(1)])


ANCH = re.compile(r'(<li[^>]*>\s*)?<a\b[^>]*href="((?:services-mills|industries)-[\w-]+\.html)"[^>]*>.*?</a>(\s*</li>)?', re.S)


def reorder_runs(h, rank_of, pattern):
    items = [(m.start(), m.end(), m.group(0), rank_of(m)) for m in pattern.finditer(h)]
    runs, cur = [], []
    for it in items:
        if cur and h[cur[-1][1]:it[0]].strip() == '' and cur[-1][3][0] == it[3][0]: cur.append(it)
        else:
            if len(cur) >= 3: runs.append(cur)
            cur = [it]
    if len(cur) >= 3: runs.append(cur)
    for run in reversed(runs):
        order = sorted(run, key=lambda x: x[3][1])
        if [x[0] for x in order] == [x[0] for x in run]: continue
        seps = [h[run[k][1]:run[k + 1][0]] for k in range(len(run) - 1)]
        new = order[0][2]
        for k, sep in enumerate(seps): new += sep + order[k + 1][2]
        h = h[:run[0][0]] + new + h[run[-1][1]:]
    return h


total = 0
for f in sorted(glob.glob('*.html')):
    h = open(f).read(); o = h
    h = reorder_runs(h, lambda m: rank(m.group(2)), ANCH)
    # home slider cards
    if f == 'index.html':
        art = re.compile(r'<article class="service-slide".*?</article>', re.S)
        h = reorder_runs(h, lambda m: ('S', S[re.search(r'services-mills-([\w-]+)\.html', m.group(0)).group(1)]), art)
    # learning pavilion checklist cards
    if f == 'learning-pavilion.html':
        card = re.compile(r'<article class="lead-magnet resource-card".*?</article>', re.S)
        def crank(m):
            slug = re.search(r'data-open="([\w-]+)"', m.group(0)).group(1)
            return ('S', S[slug]) if not slug.startswith('industry-') else ('S', 100 + I[slug[len('industry-'):]])
        h = reorder_runs(h, crank, card)
    if h != o: open(f, 'w').write(h); total += 1
print('pages reordered:', total)
