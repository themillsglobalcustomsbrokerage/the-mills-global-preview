#!/usr/bin/env python3
"""Adds the 'Tagged ...' keyword line at the bottom of each page (SEO), as on the reference site Jill shared.
Idempotent: replaces an existing block."""
import re, glob, os, html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
COMMON = ['#TheMillsGlobal', 'Customs Broker Philippines', 'Customs Clearance Philippines', 'Port of Manila Customs Clearance']
SERVICE = {
 'entry': ['Philippine Market Entry', 'Company Registration Philippines', 'Importer Registration Philippines', 'First Shipment Planning Philippines', 'Foreign Company Import Philippines'],
 'permits': ['Import Permits Philippines', 'FDA Product Registration Philippines', 'Regulatory Approvals Philippines', 'BIR ATRIG Philippines', 'Product Standards Certification Philippines'],
 'customs': ['Customs Brokerage Philippines', 'Tariff Classification Philippines', 'Customs Valuation Philippines', 'Import Clearance Philippines', 'Customs Hold Support Philippines'],
 'projects': ['Project Cargo Philippines', 'Break Bulk Cargo Philippines', 'Out of Gauge Cargo Philippines', 'Heavy Equipment Import Philippines', 'Heavy Haul Transport Philippines'],
 'marine': ['Vessel Import Philippines', 'Yacht Import Philippines', 'MARINA Registration Philippines', 'Marine Equipment Customs Clearance', 'Vessel Spares Delivery Philippines'],
 'dangerous-goods': ['Dangerous Goods Shipping Philippines', 'Hazardous Cargo Customs Clearance', 'Dangerous Goods Packaging Philippines', 'Chemical Import Permits Philippines', 'Lithium Battery Shipping Philippines'],
 'logistics': ['Domestic Logistics Philippines', 'Port Drayage Philippines', 'Bonded Warehousing Philippines', 'Cold Chain Storage Philippines', 'Last-Mile Delivery Philippines'],
 'packaging': ['Industrial Crating Philippines', 'Export Packaging Philippines', 'ISPM 15 Wooden Crates', 'Heavy Equipment Packaging', 'Container Stuffing Philippines'],
 'insurance': ['Marine Cargo Insurance Philippines', 'Cargo Insurance Claims Documentation', 'Air Cargo Insurance Philippines', 'Project Cargo Insurance Philippines', 'Transit Insurance Philippines'],
 'time-critical': ['Urgent Customs Clearance Philippines', 'Expedited Cargo Philippines', 'AOG Parts Clearance Philippines', 'Priority Customs Clearance', 'Emergency Cargo Clearance Philippines'],
 'advisory': ['Trade Compliance Philippines', 'Customs Advisory Philippines', 'Import Regulation Advice Philippines', 'Customs Audit Readiness Philippines', 'Philippine Trade Regulation'],
}
INDUSTRY = {
 'agriculture': ['Agricultural Import Philippines', 'Live Animal Import Philippines', 'Plant Import Permits Philippines', 'Seafood Import Philippines', 'BPI BAI BFAR Import Clearance'],
 'automotive': ['Vehicle Import Philippines', 'Used Vehicle Import Philippines', 'Heavy Equipment Import Philippines', 'Special-Purpose Vehicle Import Philippines', 'Imported Vehicle Excise Tax Philippines'],
 'aviation': ['Aircraft Parts Import Philippines', 'AOG Shipment Philippines', 'Aviation Customs Clearance Philippines', 'Aircraft Engine Import Philippines', 'CAAP Customs Documentation'],
 'chemicals': ['Chemical Import Philippines', 'DENR-EMB Chemical Permits', 'Controlled Chemicals Import Philippines', 'Laboratory Reagents Import Philippines', 'Dangerous Goods Chemical Shipping'],
 'cold-chain': ['Cold Chain Logistics Philippines', 'Reefer Trucking Philippines', 'Frozen Food Import Philippines', 'Vaccine Import Philippines', 'Temperature-Sensitive Cargo Philippines'],
 'construction': ['Construction Equipment Import Philippines', 'Heavy Machinery Import Philippines', 'Crane Import Philippines', 'Infrastructure Project Cargo Philippines', 'Used Equipment Import Rules Philippines'],
 'data-centers': ['Data Center Equipment Import Philippines', 'Server Import Philippines', 'UPS Battery Import Philippines', 'Digital Infrastructure Logistics Philippines', 'Data Center Project Logistics'],
 'electronics-telecom': ['Electronics Import Philippines', 'NTC Type Approval Philippines', 'Telecom Equipment Import Philippines', 'IoT Device Import Philippines', 'Lithium Battery Electronics Shipping'],
 'food-beverage': ['Food Import Philippines', 'Beverage Import Philippines', 'FDA Food Import Clearance Philippines', 'FMCG Import Philippines', 'Alcohol Import Philippines'],
 'freight-forwarders': ['Customs Broker for Freight Forwarders', 'Freight Forwarder Customs Support Philippines', 'NVOCC Customs Clearance Philippines', 'Philippine Clearance Partner for Forwarders', 'Logistics Provider Customs Support'],
 'healthcare': ['Medicine Import Philippines', 'Medical Device Import Philippines', 'FDA Import Authorization Philippines', 'Vaccine Logistics Philippines', 'Pharmaceutical Customs Clearance Philippines'],
 'manufacturing': ['Machinery Import Philippines', 'CNC Machine Import Philippines', 'PEZA Machinery Import', 'BOI Incentive Customs Entry', 'Production Line Import Philippines'],
 'marine': ['Yacht Import Philippines', 'Vessel Registration Philippines', 'LCT Import Philippines', 'Marine Engine Import Philippines', 'MARINA PPA Clearance'],
 'mining': ['Mining Equipment Import Philippines', 'Explosives Import Permits Philippines', 'Mineral Samples Shipping Philippines', 'Mining Reagents Import Philippines', 'Heavy Equipment Site Delivery Philippines'],
 'renewable-energy': ['Solar Equipment Import Philippines', 'Solar Panel Customs Clearance Philippines', 'Battery Energy Storage Import Philippines', 'Wind Turbine Logistics Philippines', 'Renewable Energy Logistics Philippines'],
 'retail': ['Retail Import Philippines', 'E-Commerce Import Philippines', 'Consumer Goods Customs Clearance', 'Apparel Import Philippines', 'Cosmetics Import Philippines'],
}
GENERAL = {
 'index.html': ['Customs Brokerage Philippines', 'Philippine Customs Clearance', 'Import Compliance Philippines', 'Freight and Customs Solutions Philippines', 'Trade Execution Philippines'],
 'about.html': ['Philippine Trade Execution', 'Compliance-First Customs Brokerage', 'Customs Brokerage Manila', 'Trade Without Limits', 'Import Compliance Philippines'],
 'industries.html': ['Industry Import Compliance Philippines', 'Industrial Customs Clearance Philippines', 'Sector Customs Brokerage Philippines', 'Regulated Cargo Philippines', 'Import Permits by Industry'],
 'location.html': ['Customs Broker Manila', 'BGC Taguig Customs Broker', 'Binondo Customs Broker', 'Global Trade Network Philippines', 'International Customs Partners'],
 'contact.html': ['Customs Broker Contact Philippines', 'Customs Clearance Quote Philippines', 'Import Consultation Philippines'],
 'book-a-call.html': ['Customs Consultation Philippines', 'Book a Customs Broker', 'Import Consultation Philippines'],
 'blog.html': ['Customs News Philippines', 'Bureau of Customs Updates', 'Philippine Import Guides', 'Customs Memorandum Orders'],
 'learning-pavilion.html': ['Import Guides Philippines', 'Customs Readiness Checklists', 'Philippine Customs Resources', 'Free Import Checklists'],
}


def block(page, kws):
    items = []
    for k in kws:
        text = html.escape(k)
        href = 'index.html' if k.startswith('#') else TARGET.get(k, 'index.html#services')
        items.append(f'<span>{text}</span>' if href == page else f'<a href="{href}">{text}</a>')
    return ('  <section class="page-tags" aria-label="Related topics">\n    <div class="container">\n      <p class="page-tags__line"><span class="page-tags__label">Tagged</span> '
            + ', '.join(items) + '</p>\n    </div>\n  </section>\n\n')


TARGET = {}
for s, ks in SERVICE.items():
    for k in ks: TARGET[k] = f'services-mills-{s}.html'
for s, ks in INDUSTRY.items():
    for k in ks: TARGET[k] = f'industries-{s}.html'
for k in COMMON: TARGET[k] = 'index.html' if k.startswith('#') else 'index.html#services'
TARGET['Customs Broker Philippines'] = 'services-mills-customs.html'
TARGET['Customs Clearance Philippines'] = 'services-mills-customs.html'
TARGET['Port of Manila Customs Clearance'] = 'services-mills-customs.html'

n = 0
for f in sorted(glob.glob('*.html')):
    name = f[:-5]
    if name.startswith('services-mills-'): kws = COMMON + SERVICE[name[len('services-mills-'):]]
    elif name.startswith('industries-'): kws = COMMON + INDUSTRY[name[len('industries-'):]]
    elif f in GENERAL: kws = ['#TheMillsGlobal'] + GENERAL[f]
    else: continue
    h = open(f).read(); o = h
    h = re.sub(r'  <section class="page-tags".*?</section>\n\n', '', h, flags=re.S)
    i = h.find('<footer class="footer">')
    if i < 0: continue
    h = h[:i] + block(f, kws).lstrip(' ').rjust(0) + '  ' + h[i:] if False else h[:i].rstrip(' ') + block(f, kws) + '  ' + h[i:]
    if h != o: open(f, 'w').write(h); n += 1
print('pages tagged:', n)
