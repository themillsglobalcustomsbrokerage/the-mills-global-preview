#!/usr/bin/env python3
"""Use 'and' instead of '&' in industry and service names (and on the industry/service pages themselves).
Idempotent. Run from the repo root."""
import glob, re

NAMES = [
    'Cold Chain & Temperature-Sensitive Cargo', 'Freight Forwarders & Logistics',
    'Priority Clearance & Expedited Cargo Execution', 'Domestic Logistics & Customs-Linked Cargo Execution',
    'Export & Protective Cargo Packaging', 'Dangerous Goods & Regulated Cargo Compliance',
    'Maritime & Vessel Coordination', 'Customs Brokerage & Trade Compliance',
    'Marine Cargo & Transit Insurance Coordination', 'Product Registration & Regulatory Approvals',
    'Project Cargo & Industrial Trade Execution', 'Regulatory & Government Coordination',
    'Philippine Market Entry & Import Readiness', 'Market Entry & Import Readiness',
    'Warehousing & Distribution', 'Cargo & Industries We Support', 'CARGO & INDUSTRIES',
    'Philippine Customs & Trade Execution',
    'LCL & FCL Freight Forwarding', 'Import & Export Clearance', 'Permits & Licensing',
    'Tariff & Customs Consultancy', 'Business & Legal Consultancy', 'Customs Disputes & Legal Remedies',
    'Crating & Warehousing', 'Customs Clearance & Freight',
]
VARIANTS = []
for n in NAMES:
    VARIANTS.append((n.replace('&', '&amp;'), n.replace('&', 'and')))
    VARIANTS.append((n, n.replace('&', 'and')))

FULL = re.compile(r'(industries-.*|services-.*|talk-to-a-broker)\.html$')
SEG = re.compile(r'(<script\b(?![^>]*ld\+json)[^>]*>.*?</script>|<style\b.*?</style>)', re.S)

def fix_full(s):
    parts = SEG.split(s)
    for i in range(0, len(parts), 2):          # even parts are outside script/style
        parts[i] = parts[i].replace(' &amp; ', ' and ').replace(' & ', ' and ')
    return ''.join(parts)

changed = 0
files = [f for ext in ('html', 'py', 'js', 'json', 'yml', 'md', 'xml') for f in glob.glob(f'**/*.{ext}', recursive=True)
         if not f.startswith(('node_modules', '.git/'))]
for f in files:
    if f.endswith('tools/ampersand-to-and.py'): continue
    try: s = open(f, encoding='utf-8').read()
    except Exception: continue
    o = s
    for a, b in VARIANTS: s = s.replace(a, b)
    if FULL.search(f) and '/' not in f: s = fix_full(s)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); changed += 1
print('files changed:', changed)
