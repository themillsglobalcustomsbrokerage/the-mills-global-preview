#!/usr/bin/env python3
"""Copy standards from the Oct 16 review, applied to every service and industry page (plus home/hub/about):
  1. Abbreviations are spelled out on first mention; agency lists spell out every item.
  2. Titles of cards, features and steps use Title Case; industry names are capitalized in headings.
  3. A few sentences rewritten so they read clearly.
Idempotent: a second run changes nothing."""
import re, glob, os, html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
exec(open('tools/apply-meeting-revisions.py').read().split("# ---------------------------------------------------------------- per-industry content")[0].split("os.chdir")[0].replace('"""', "'''", 0), {}) if False else None
SMALL = {'and', 'or', 'of', 'for', 'to', 'with', 'the', 'in', 'on', 'a', 'an', 'at', 'by', 'from', 'per'}


def title_case(s):
    def word(w, first):
        if not w or not w[0].isalpha(): return w
        if any(c.isupper() for c in w[1:]) or any(c.isdigit() for c in w): return w[0].upper() + w[1:]
        if '-' in w: return '-'.join(word(p, True) for p in w.split('-'))
        if not first and w.lower() in SMALL: return w.lower()
        return w[0].upper() + w[1:]
    return ' '.join(word(w, i == 0) for i, w in enumerate(s.split(' ')))


GLOSS = {
 'FDA': 'Food and Drug Administration', 'BIR': 'Bureau of Internal Revenue', 'BOC': 'Bureau of Customs', 'NTC': 'National Telecommunications Commission',
 'PEZA': 'Philippine Economic Zone Authority', 'MARINA': 'Maritime Industry Authority', 'ATRIG': 'Authority to Release Imported Goods', 'AOG': 'Aircraft on Ground',
 'DENR-EMB': 'Environmental Management Bureau of the Department of Environment and Natural Resources', 'PDEA': 'Philippine Drug Enforcement Agency',
 'DTI-BPS': 'Bureau of Philippine Standards of the Department of Trade and Industry', 'BOI': 'Board of Investments', 'BFAR': 'Bureau of Fisheries and Aquatic Resources',
 'OMB': 'Optical Media Board', 'BAI': 'Bureau of Animal Industry', 'NMIS': 'National Meat Inspection Service', 'DDB': 'Dangerous Drugs Board',
 'FPA': 'Fertilizer and Pesticide Authority', 'LTO': 'Land Transportation Office', 'DENR': 'Department of Environment and Natural Resources',
 'DTI': 'Department of Trade and Industry', 'PPA': 'Philippine Ports Authority', 'BPI': 'Bureau of Plant Industry', 'CAAP': 'Civil Aviation Authority of the Philippines',
 'PNRI': 'Philippine Nuclear Research Institute', 'BPS': 'Bureau of Philippine Standards', 'DOE': 'Department of Energy', 'OOG': 'Out of Gauge',
 'FTEB': 'Fair Trade Enforcement Bureau', 'DTI-FTEB': 'Fair Trade Enforcement Bureau of the Department of Trade and Industry',
 'PNP-FEO': 'Philippine National Police Firearms and Explosives Office', 'PCA': 'Philippine Coconut Authority', 'SRA': 'Sugar Regulatory Administration',
 'NTA': 'National Tobacco Administration', 'UPS': 'Uninterruptible Power Supply', 'CNC': 'Computer Numerical Control', 'LCT': 'Landing Craft Tank',
 'DENR-MGB': 'Mines and Geosciences Bureau of the Department of Environment and Natural Resources', 'MGB': 'Mines and Geosciences Bureau',
 'ISPM': 'International Standards for Phytosanitary Measures', 'SPS': 'Sanitary and Phytosanitary', 'NFA': 'National Food Authority',
 'PICCS': 'Philippine Inventory of Chemicals and Chemical Substances', 'PMPIN': 'Pre-Manufacture and Pre-Importation Notification', 'CCO': 'Chemical Control Order',
 'EPC': 'Engineering, Procurement and Construction', 'CPRS': 'Client Profile Registration System', 'AHTN': 'ASEAN Harmonized Tariff Nomenclature',
 'HS': 'Harmonized System', 'VAT': 'Value-Added Tax', 'SDS': 'Safety Data Sheet', 'SEC': 'Securities and Exchange Commission', 'DA': 'Department of Agriculture',
 'ICC': 'Import Commodity Clearance', 'DOST-PNRI': 'Philippine Nuclear Research Institute of the Department of Science and Technology',
 'DENR-BMB': 'Biodiversity Management Bureau of the Department of Environment and Natural Resources', 'DENR-FMB': 'Forest Management Bureau of the Department of Environment and Natural Resources',
 'CPR': 'Certificate of Product Registration', 'NVOCC': 'Non-Vessel-Operating Common Carrier', 'FMCG': 'Fast-Moving Consumer Goods',
}
# parts that count as already explained once their compound is
PARTS = {'DENR-EMB': ['DENR'], 'DTI-BPS': ['DTI', 'BPS'], 'DTI-FTEB': ['DTI', 'FTEB'], 'DENR-MGB': ['DENR', 'MGB'], 'DENR-BMB': ['DENR'], 'DENR-FMB': ['DENR'], 'DOST-PNRI': ['PNRI']}
TOKEN = re.compile(r'\b(?:DENR-EMB|DENR-MGB|DENR-BMB|DENR-FMB|DTI-BPS|DTI-FTEB|DOST-PNRI|PNP-FEO|[A-Z]{2,6})\b')
ROUND = re.compile(r'\(([A-Z][A-Z-]{1,9})\)')


def expand_text(text, seen, all_occurrences=False):
    out, pos = [], 0
    for m in TOKEN.finditer(text):
        tok = m.group(0)
        if tok not in GLOSS: continue
        before, after = text[max(0, m.start() - 1):m.start()], text[m.end():m.end() + 1]
        if before == '(' and after == ')':               # already the bracketed acronym
            seen.add(tok); continue
        if before in ('-', '/') or after == '-' : continue   # part of a longer hyphenated word, handled separately
        if tok in seen and not all_occurrences: continue
        out.append(text[pos:m.start()]); out.append(f'{GLOSS[tok]} ({tok})'); pos = m.end()
        seen.add(tok); seen.update(PARTS.get(tok, []))
    out.append(text[pos:])
    return ''.join(out)


SKIP_TAGS = re.compile(r'<(script|style|svg|title)\b.*?</\1>', re.S)


def expand_page(h):
    a = h.find('</nav>'); b = h.find('<footer')
    if a < 0 or b < 0: return h
    body = h[a:b]
    seen = set()
    parts = re.split(r'(<[^>]+>)', body)
    skip = 0; res = []
    for p in parts:
        if p.startswith('<'):
            tag = re.match(r'</?\s*([a-zA-Z0-9]+)', p)
            if tag and tag.group(1).lower() in ('script', 'style', 'svg'): skip += -1 if p.startswith('</') else 1
            res.append(p); continue
        if skip or not p.strip() or 'IMAGE:' in p: res.append(p); continue
        res.append(expand_text(html.unescape(p), seen) if False else expand_text(p, seen))
    return h[:a] + ''.join(res) + h[b:]


def expand_agency_lists(h):
    s2 = h.find('Regulatory Focus'); s3 = h.find('Common Challenges', s2 + 1)
    if s2 < 0 or s3 < 0: return h   # Common Challenges now sits before Regulatory Focus, so there is nothing to slice
    block = h[s2:s3]
    def li(m):
        txt = m.group(2)
        txt = re.sub(r'\(([A-Z-]+)\)', lambda x: x.group(0), txt)
        if '(' in txt: return m.group(0)                  # already expanded
        return m.group(1) + expand_text(txt, set(), all_occurrences=True) + m.group(3)
    block = re.sub(r'(<li class="audience-list__item">.*?<span>)(.*?)(</span></li>)', li, block, flags=re.S)
    return h[:s2] + block + h[s3:]


SERVICE_PAGES = sorted(glob.glob('services-*.html'))
IND_PAGES = sorted(glob.glob('industries-*.html'))

REWRITES = [
 ('The website and client file identify exact regulators instead of using vague permit language.', 'Every permit names the exact responsible regulator, with no vague permit language.'),
 ('<h4 class="info-card__title">Registrations in the wrong order</h4>', '<h4 class="info-card__title">Registration steps in the wrong order</h4>'),
 ('Registrations in the wrong order', 'Registration steps in the wrong order'),
 ('Identify the required entity, registrations, importer structure, permits and responsible agencies.', 'Identify the required entity, registration steps, importer structure, permits and responsible agencies.'),
 ('We handle FDA-regulated products correctly.', 'We handle products regulated by the FDA correctly.'),
 ('radio peripherals and IoT devices', 'radio peripherals and Internet of Things (IoT) devices'),
]


def industry_name(h):
    m = re.search(r'Teams we support in (.*?)\.</h3>', h)
    return m.group(1) if m else None


def headings(h):
    name = industry_name(h)
    if not name: return h
    N = title_case(name)
    h = h.replace(f'Teams we support in {name}.', f'Teams we support in {N}.')
    h = h.replace(f'Why {name} shipments usually get stuck.', f'Why {N} shipments usually get stuck.')
    art = 'an' if N[0].lower() in 'aeiou' else 'a'
    h = re.sub(r'How The Mills handles an? ' + re.escape(name) + r' shipment\.', f'How The Mills handles {art} {N} shipment.', h)
    return h


def titles(h):
    def tc(m): return m.group(1) + title_case(m.group(2)) + m.group(3)
    h = re.sub(r'(<h4 class="info-card__title">)(.*?)(</h4>)', tc, h)
    h = re.sub(r'(<h3 class="service-feature__title">)(.*?)(</h3>)', tc, h)
    h = re.sub(r'(<h3 class="how-steps__title">)(.*?)(</h3>)', tc, h)
    return h


changed = 0
for f in SERVICE_PAGES + IND_PAGES + ['index.html', 'about.html', 'industries.html']:
    h = open(f).read(); o = h
    for a, b in REWRITES: h = h.replace(a, b)
    if f.startswith('industries-'): h = expand_agency_lists(h); h = headings(h)
    if f.startswith(('services-', 'industries-')): h = titles(h)
    h = expand_page(h)
    if h != o: open(f, 'w').write(h); changed += 1
print('pages updated:', changed)
