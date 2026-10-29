#!/usr/bin/env python3
"""Service copy has two layers:
  BENEFIT = plain-language, benefit-led line: service page hero, hover previews, contact blocks, follow-up emails;
  SCOPE   = the client's scope-style description: the Home services slider only.
Idempotent: run again after editing the dicts below."""
import re, glob, io, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import re
SCOPE = {
 'services-mills-entry': "Market-entry structure review, company incorporation and business registration coordination, importer and exporter readiness for Bureau of Customs (BOC) registration, product and industry permit mapping, Philippine Economic Zone Authority (PEZA) and Board of Investments (BOI) coordination, first-shipment planning, and post-registration compliance.",
 'services-mills-permits': "Permit mapping and coordination of import permits, product registrations and shipment clearances with the Food and Drug Administration (FDA), Bureau of Internal Revenue (BIR), Department of Agriculture (DA) agencies, Bureau of Philippine Standards of the Department of Trade and Industry (DTI-BPS), National Telecommunications Commission (NTC) and other regulators, including renewals and amendments.",
 'services-mills-customs': "Import and export customs clearance, importer and exporter registration, tariff classification, customs valuation, duties and taxes, Philippine Economic Zone Authority (PEZA) and special transactions, examination and hold coordination, post-clearance support, and customs remedies.",
 'services-mills-packaging': "Industrial crating, export packaging, palletization, lashing and securing, container stuffing and unpacking, moisture and corrosion protection, dangerous goods packaging coordination, on-site packaging, and packing documentation for machinery, equipment and high-value cargo.",
 'services-mills-insurance': "Coordination of marine cargo, air cargo, inland transit and project cargo insurance through licensed insurance partners, including door-to-door options, shipment declarations, and claims-document support.",
 'services-mills-time-critical': "Priority clearance and expedited delivery of urgent cargo, including urgency assessment, pre-arrival document review, aircraft-on-ground (AOG) parts, vessel spares, production-critical parts, medical and infrastructure cargo, and escalation reporting.",
 'services-mills-advisory': "Trade and regulatory advisory covering import-structure review, regulatory mapping, customs-risk assessment, post-clearance readiness, government coordination, compliance program design, and coordination with legal, tax and technical professionals.",
 'services-mills-projects': "Project cargo planning and coordination for break bulk, oversized and Out of Gauge (OOG) cargo and heavy equipment, including customs and permit mapping, port and terminal coordination, route and site review, heavy-haul transport, and project reporting.",
}
SCOPE.update({
 'services-mills-marine': "Registration and documentation of commercial vessels, private yachts, pleasure crafts, and other watercraft, including Maritime Industry Authority (MARINA) and Philippine Ports Authority (PPA) permits, regulatory approvals, and related maritime compliance requirements.",
 'services-mills-dangerous-goods': "Handling and regulatory compliance of dangerous goods and hazardous cargoes, including United Nations (UN) classification, dangerous goods declarations (DGD), approved packaging, labeling, segregation, documentation, and coordination of required permits for importation, exportation, and transportation.",
 'services-mills-logistics': "Trucking, container hauling, heavy equipment transportation, warehouse transfers, inter-island shipping, and nationwide cargo distribution, including port-to-door delivery and coordination of inland freight movements.",
})
# the same scope text before the acronym standard expanded the first mention on a page
COLLAPSED = {
 'services-mills-marine': ["Registration and documentation of commercial vessels, private yachts, pleasure crafts, and other watercraft, including MARINA and PPA permits, regulatory approvals, and related maritime compliance requirements.",
                           "Registration and documentation of commercial vessels, private yachts, pleasure crafts, and other watercraft, including Maritime Industry Authority (MARINA) and PPA permits, regulatory approvals, and related maritime compliance requirements.",
                           "Registration and documentation of commercial vessels, private yachts, pleasure crafts, and other watercraft, including MARINA and Philippine Ports Authority (PPA) permits, regulatory approvals, and related maritime compliance requirements."],
 'services-mills-dangerous-goods': ["Handling and regulatory compliance of dangerous goods and hazardous cargoes, including UN classification, dangerous goods declarations (DGD), approved packaging, labeling, segregation, documentation, and coordination of required permits for importation, exportation, and transportation."],
}
BENEFIT = {
 'services-mills-entry': "Get your company, registrations and permits set up correctly before you buy, so your first shipment arrives on time and is not stopped at the port.",
 'services-mills-permits': "We find out which government approvals your product needs and handle the applications for you, so your goods are not held up because of missing paperwork.",
 'services-mills-customs': "We prepare your import and export paperwork and see your cargo through customs, so it is released sooner, you pay the right duties and you avoid costly delays.",
 'services-mills-marine': "We handle the registration, permits and customs paperwork for your vessel, yacht or marine equipment, and rush urgent spare parts to ships that are waiting.",
 'services-mills-dangerous-goods': "We make sure dangerous and hazardous cargo is identified, labeled, packed and documented correctly, so carriers accept it and it ships on schedule.",
 'services-mills-logistics': "We move your cargo from the port to its final destination, with trucking, storage and delivery planned together, so it arrives on schedule with proof of delivery.",
 'services-mills-packaging': "We pack and crate your cargo to suit its weight and journey, so machinery and valuable goods arrive undamaged and the packing records are ready for customs and insurance.",
 'services-mills-insurance': "We arrange cargo insurance through licensed partners to match your shipment's value and route, and prepare the records you need, so a claim is not delayed by missing paperwork.",
 'services-mills-time-critical': "When cargo cannot wait, we put it on a fast track with one person responsible for every document and hold-up, so urgent shipments do not sit at the port.",
 'services-mills-advisory': "Get a clear answer on the rules, permits and risks before you commit, plus a simple plan for what to do first, so you decide with facts, not guesses.",
 'services-mills-projects': "We plan and move very large and heavy cargo, from permits and customs through the port to your site, so a missed requirement does not delay your project.",
}
OTHER = [f for f in glob.glob('*.html') + glob.glob('tools/*.py') + glob.glob('n8n/**/*.json', recursive=True) + glob.glob('docs/*.md')
         if not f.endswith(('split-service-descriptions.py', 'rewrite-hero-copy.py'))]
def esc(t): return t.replace('&', '&amp;')
def jesc(t): return t.replace('"', '\\"')
HERO_RE = re.compile(r'(<p class="service-hero__subtitle">)(.*?)(</p>)', re.S)
SLIDE_RE = r'(service-slide__title">%s</h3>\s*<p class="service-slide__text">)(.*?)(</p>)'
changed = set()
def put(path, text):
    io.open(path, 'w', encoding='utf-8').write(text); changed.add(path)
# 1) benefit line (plain language) replaces whatever service text is there, on every page except the Home slider
for slug in BENEFIT:
    hero_page = slug + '.html'
    page = io.open(hero_page, encoding='utf-8').read()
    cur_hero = HERO_RE.search(page).group(2).strip()
    old_variants = {cur_hero, esc(SCOPE[slug])} | {esc(v) for v in COLLAPSED.get(slug, [])}
    for g in OTHER:
        t = io.open(g, encoding='utf-8').read(); o = t
        for v in old_variants:
            for form in {v, v.replace('&amp;', '&'), jesc(v), jesc(v.replace('&amp;', '&'))}:
                if form in t: t = t.replace(form, esc(BENEFIT[slug]) if g.endswith('.html') else jesc(BENEFIT[slug]))
        if t != o: put(g, t)
# 2) slider keeps the scope-style description
idx = io.open('index.html', encoding='utf-8').read(); o = idx
for slug, scope in SCOPE.items():
    title = re.search(r'service-hero__eyebrow">([^<]*)<', io.open(slug + '.html', encoding='utf-8').read()).group(1).strip()
    idx = re.sub(SLIDE_RE % re.escape(title), lambda m: m.group(1) + esc(scope) + m.group(3), idx, count=1, flags=re.S)
if idx != o: put('index.html', idx)
print(len(changed), 'files changed', sorted(changed)[:6])
