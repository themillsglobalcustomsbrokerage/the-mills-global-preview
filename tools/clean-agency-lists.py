#!/usr/bin/env python3
"""Rebuilds the 'agencies and controls that usually apply' list on each industry page so it names agencies only
(no rules, processes or services), each spelled out in full."""
import re, os, html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
g = {'__file__': os.path.abspath('tools/apply-copy-standards.py')}
exec(open('tools/apply-copy-standards.py').read().split("SERVICE_PAGES =")[0], g)
expand_text = g['expand_text']

AG = {
 'agriculture': ['BAI', 'BPI', 'BFAR', 'NMIS', 'FPA', 'PCA', 'SRA', 'NTA', 'NFA where currently applicable', 'FDA', 'BOC'],
 'automotive': ['DTI-FTEB', 'LTO', 'BIR for the ATRIG and excise tax', 'BOC'],
 'aviation': ['CAAP', 'NTC for radio equipment', 'BOC', 'BIR'],
 'chemicals': ['DENR-EMB for the PICCS, PMPIN and CCO requirements', 'PDEA or DDB', 'PNRI', 'FPA', 'FDA', 'BIR', 'BOC'],
 'cold-chain': ['FDA', 'BAI', 'BFAR', 'NMIS', 'Product-specific permits'],
 'construction': ['DTI-BPS', 'DTI-FTEB', 'LTO', 'DENR', 'BIR for the ATRIG', 'BOC'],
 'data-centers': ['NTC', 'DTI-BPS', 'DENR-EMB', 'PEZA or BOI', 'BOC'],
 'electronics-telecom': ['NTC', 'DTI-BPS', 'OMB', 'FDA for certain radiation or health products', 'BIR', 'BOC'],
 'food-beverage': ['FDA', 'BAI', 'BPI', 'BFAR', 'NMIS', 'BIR for the ATRIG and excise rules', 'DTI for labeling and standards', 'BOC'],
 'freight-forwarders': ['BOC', 'The agencies that issue permits for regulated client cargo'],
 'healthcare': ['FDA', 'PDEA or DDB', 'PNRI where applicable', 'BIR ATRIG in qualified cases'],
 'manufacturing': ['BOC', 'PEZA or BOI', 'DTI-BPS where applicable', 'BIR', 'DENR'],
 'marine': ['MARINA', 'PPA', 'NTC', 'BOC', 'BIR'],
 'mining': ['DENR', 'DENR-MGB where applicable', 'PNP-FEO', 'PDEA', 'BIR for the ATRIG', 'BOC'],
 'renewable-energy': ['DOE', 'DTI-BPS', 'DENR-EMB', 'PEZA or BOI', 'BIR', 'BOC'],
 'retail': ['FDA', 'DTI-BPS', 'NTC', 'OMB', 'BOC'],
}
n = 0
for slug, items in AG.items():
    f = f'industries-{slug}.html'; h = open(f).read()
    s2 = h.find('Regulatory Focus'); s3 = h.find('Common Challenges')
    block = h[s2:s3]
    first = re.search(r'<li class="audience-list__item">(<svg.*?</svg>)', block, re.S)
    icon = first.group(1)
    lis = [m for m in re.finditer(r'[ \t]*<li class="audience-list__item">.*?</li>\n?', block, re.S)]
    start, end = lis[0].start(), lis[-1].end()
    new = ''.join(f'        <li class="audience-list__item">{icon}<span>{html.escape(expand_text(t, set(), all_occurrences=True), quote=False)}</span></li>\n' for t in items)
    nb = block[:start] + new + block[end:]
    if nb != block: open(f, 'w').write(h[:s2] + nb + h[s3:]); n += 1
print('industry agency lists rebuilt:', n)
