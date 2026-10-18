#!/usr/bin/env python3
"""Applies the Oct 16 copy-review meeting revisions to the site: terminology, value statements, capitalization,
and the "Why ... usually get stuck" heading. Idempotent: running it twice changes nothing more."""
import re, glob, os, html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SMALL = {'and', 'or', 'of', 'for', 'to', 'with', 'the', 'in', 'on', 'a', 'an', 'at', 'by'}


def title_case(s):
    def word(w, first):
        if not w or not w[0].isalpha(): return w
        if any(c.isupper() for c in w[1:]) or any(c.isdigit() for c in w): return w[0].upper() + w[1:]
        if '-' in w: return '-'.join(word(p, True) for p in w.split('-'))
        if not first and w.lower() in SMALL: return w.lower()
        return w[0].upper() + w[1:]
    parts = s.split(' ')
    return ' '.join(word(w, i == 0) for i, w in enumerate(parts))


def cap_first(s):
    return s[0].upper() + s[1:] if s and s[0].isalpha() else s


def dg(s):
    return re.sub(r'(?i)dangerous[- ]goods', 'Dangerous Goods', s)


# ---------------------------------------------------------------- per-industry content (value statements: how we help each team)
IND = {
 'agriculture': dict(
   sub='Coordinate sanitary, phytosanitary, quarantine and customs requirements for plants, live animals, meat, fish and other agricultural commodities.',
   teams=['We line up sanitary and phytosanitary clearances before the cargo arrives.', 'We keep grains, feeds and ingredients moving on a recurring schedule.',
          'We coordinate quarantine and inspection for animal products and live animals.', 'We match permits and cold storage so fish and seafood stay compliant and fresh.',
          'We guide agricultural exporters through the approvals and importer rules of the Philippine market.']),
 'automotive': dict(
   teams=['We check admissibility, taxes and permits so imported vehicles reach resale on time.', 'We clear trucks and buses for operations and plan delivery to your depot.',
          'We handle forklifts, cranes and earthmoving equipment from permit review to site delivery.', 'We manage the extra requirements for ambulances and other special-purpose vehicles.',
          'We confirm admissibility first, so units shipped to the Philippines are not stuck at the port.']),
 'aviation': dict(
   sub='Coordinate customs and aviation documentation for aircraft, engines, parts and urgent Aircraft on Ground (AOG) shipments.',
   teams=['We clear parts and engines quickly so aircraft return to service.', 'We handle customs and documentation for rotables, tools and components moving across borders.',
          'We clear aircraft, engines and records correctly the first time.', 'We import ground-support equipment and deliver it ready for operations.',
          'We give priority clearance support when an aircraft is grounded and time matters.']),
 'chemicals': dict(
   sub='Connect substance identity to environmental permits, controlled-chemical authority, Dangerous Goods rules and customs.',
   teams=['We clear raw materials and finished products on a regular schedule, with the right permits in place.', 'We coordinate reagents and small-volume controlled materials from authority to delivery.',
          'We handle flammable and regulated liquids with careful packing, labeling and transport.', 'We move cylinders, fuels and bulk products safely under Dangerous Goods rules.',
          'We secure authority from the right controlling agency before the cargo ships.']),
 'cold-chain': dict(
   sub='Reliable reefer trucking, qualified cold storage and timely delivery for frozen, chilled and temperature-sensitive cargo, with permits and customs coordinated.',
   cargo=['Frozen and Chilled Food', 'Meat', 'Seafood', 'Dairy', 'Pharmaceuticals', 'Vaccines', 'Biological Materials and Specialty Chemicals'],
   teams=['We arrange reefer trucks and qualified cold storage so meat, seafood and dairy stay cold from port to warehouse.', 'We coordinate permits, customs release and temperature-controlled delivery from port to cold store.',
          'We match the permit, storage and transport to each item\'s narrow temperature window.', 'We schedule deliveries so perishable stock arrives on time and in condition.',
          'We handle the customs and permit side so your teams can focus on the cargo they hold.'],
   agencies=['FDA', 'BAI', 'BFAR', 'NMIS', 'Product-specific permits']),
 'construction': dict(
   teams=['We bring in machinery and materials for your project, from permit review to site delivery.', 'We clear cranes, excavators and generators for sale or lease.',
          'We handle steel, cement products and structural materials with the right classification.', 'We deliver project equipment to site on schedule.',
          'We clear your equipment through customs and get it to the site.']),
 'data-centers': dict(
   sub='We clear and deliver servers, cooling, power, security and telecommunications equipment on schedule, so critical digital infrastructure goes live when planned.',
   teams=['We deliver servers, cooling and power equipment on schedule for new halls.', 'We get rack equipment to your client sites cleared and in good condition.',
          'We bring in imported hardware so capacity expands on plan.', 'We clear and deliver your own equipment so your space is fitted out on time.',
          'We keep shipments into the Philippines moving against project deadlines.']),
 'electronics-telecom': dict(
   sub='Secure handling and compliant clearance of sensitive electronic hardware, radio peripherals and IoT devices, with NTC, BPS, OMB and customs requirements coordinated.',
   teams=['We clear radios, routers and infrastructure equipment with the right NTC approvals.', 'We clear phones, computers and accessories with the right approvals, so stock reaches shelves without holds.',
          'We handle equipment with radio or wireless components, including NTC approvals.', 'We clear components and finished goods with the right classification.',
          'We sort certifications and approvals before sale.']),
 'food-beverage': dict(
   sub='Align FDA, labeling, tax, cold-chain and customs requirements so food, beverage and Fast-Moving Consumer Goods (FMCG) arrive compliant and ready for the shelf.',
   teams=['We align registration, labeling and customs so finished products reach retail and food service compliant.', 'We keep a steady, compliant supply of ingredients for your production.',
          'We coordinate FDA requirements for supplements and nutrition products.', 'We handle excise and labeling rules correctly for alcohol imports.',
          'We keep mixed Fast-Moving Consumer Goods (FMCG) shipments compliant and moving, from registration to delivery.']),
 'freight-forwarders': dict(
   sub='A dependable customs and permit execution layer for freight forwarders, ocean and air carriers and logistics companies, so client cargo clears reliably and safely.',
   teams=['We provide Philippine customs and permit execution for your clients\' cargo.', 'We add clearance support without you building a full in-house team.',
          'We handle Philippine-bound cargo as your local partner.', 'We move regulated items through customs.', 'We partner with you on permits and complex clearances.']),
 'healthcare': dict(
   sub='Coordinate FDA authorization, customs and temperature-controlled delivery for medicines, vaccines, medical devices and healthcare equipment.',
   teams=['We prepare the FDA authorization and clearance for medicines and vaccines coming into the country.', 'We coordinate FDA authorization and clearance for devices and diagnostic machines.',
          'We deliver equipment and supplies directly to your facility, cleared and on schedule.', 'We clear and deliver equipment and materials imported for research.',
          'We guide your products through the right approvals for entering the Philippines.'],
   agencies=['FDA', 'PDEA or DDB', 'PNRI where applicable', 'BIR ATRIG in qualified cases'],
   stuck=[('Unregistered or mismatched documents', 'FDA authorization must be in place and match what is on the shipment.'),
          ('Controlled and temperature-sensitive products', 'Controlled medicines need PDEA or DDB approval, and temperature-sensitive products need reefer trucks arranged before release.'),
          ('Urgent medical cargo', 'Delays affect patients, so we prioritize fast, compliant release.')]),
 'manufacturing': dict(
   sub='Import production machinery with correct classification and valuation, and deliver it packed and sequenced for installation, so your line starts on schedule.',
   teams=['We bring in production equipment and lines for new capacity, classified, valued and delivered in the right order.', 'We align customs entries with your Board of Investments (BOI) and PEZA incentives.',
          'We classify and value CNC machines, presses and compressors correctly, avoiding customs disputes.', 'We deliver and position equipment on schedule so installation starts on time.',
          'We deliver your machines to Philippine factories, cleared and in good condition.'],
   agencies=['BOC', 'PEZA or BOI (Board of Investments)', 'BPS where applicable', 'BIR', 'DENR and product-specific safety or technical controls'],
   stuck=[('Classification and valuation of machinery', 'Complex equipment with no proper classification or valuation is easy to undervalue, which causes customs delays.'),
          ('Incentive paperwork', 'Board of Investments (BOI) or PEZA treatment needs the right documents on the entry.'),
          ('Packing and installation sequence', 'Machines damaged or delivered out of order hold up production start.')]),
 'marine': dict(
   sub='Compliance-driven registration, customs and port coordination for yachts, vessels, LCTs and marine equipment.',
   teams=['We import vessels, engines and equipment correctly, with MARINA and port requirements covered.', 'We handle registration and customs for leisure vessels brought into the country.',
          'We move spares and equipment on short notice.', 'We clear workboats and vessel machinery.', 'We deliver navigation gear and parts to vessels.']),
 'mining': dict(
   teams=['We move heavy machinery and drilling equipment from port to site.', 'We clear processing systems and plant components.',
          'We coordinate regulated process inputs with the right permits.', 'We handle PNP-FEO and related approvals alongside customs.', 'We move samples and equipment correctly.']),
 'renewable-energy': dict(
   sub='Customs and project execution for solar, storage, wind and hydro equipment: panels, batteries, turbines, cables and utility gear entering the Philippines.',
   teams=['We clear panels, inverters and turbine components with the right incentive paperwork.', 'We deliver equipment to project sites on schedule.',
          'We handle battery systems under Dangerous Goods rules.', 'We clear transformers, cables and control systems.', 'We support your supply to Philippine renewable projects.']),
 'retail': dict(
   teams=['We clear apparel, appliances and household goods compliantly.', 'We give your inventory a compliant path into the country.', 'We handle FDA-regulated products correctly.',
          'We meet standards and labeling requirements before stock ships.', 'We sort approvals, valuation and customs before stock arrives.']),
}


def edit_industry(slug, f, d):
    h = open(f).read(); o = h
    if d.get('sub'):
        h = re.sub(r'(<p class="service-hero__subtitle">)(.*?)(</p>)', lambda m: m.group(1) + html.escape(d['sub'], quote=False) + m.group(3), h, 1, flags=re.S)
    # cargo titles
    cargo_new = d.get('cargo')
    it = iter(cargo_new) if cargo_new else None
    def cargo(m):
        t = next(it) if it else dg(title_case(m.group(2)))
        return m.group(1) + html.escape(t, quote=False).replace('&amp;amp;', '&amp;') + m.group(3)
    h = re.sub(r'(cargo-card__title">)(.*?)(</h3>)', cargo, h, flags=re.S)
    # teams
    s1 = h.find('Teams we support'); s2 = h.find('Regulatory Focus')
    if d.get('teams') and s1 > 0:
        block = h[s1:s2]; ti = iter(d['teams'])
        block = re.sub(r'(<p class="info-card__text">)(.*?)(</p>)', lambda m: m.group(1) + html.escape(next(ti), quote=False) + m.group(3), block, flags=re.S)
        h = h[:s1] + block + h[s2:]
    # agencies
    s2 = h.find('Regulatory Focus'); s3 = h.find('Common Challenges')
    block = h[s2:s3]
    ag = iter(d['agencies']) if d.get('agencies') else None
    def agency(m):
        if ag:
            try: t = next(ag)
            except StopIteration: return ''
        else:
            t = cap_first(dg(html.unescape(m.group(2))))
        return m.group(1) + html.escape(t, quote=False) + m.group(3)
    block = re.sub(r'(<li class="audience-list__item">.*?<span>)(.*?)(</span></li>)', agency, block, flags=re.S)
    block = re.sub(r'\n\s*(?=\n)', '\n', block) if ag else block
    h = h[:s2] + block + h[s3:]
    # stuck cards
    if d.get('stuck'):
        s3 = h.find('Common Challenges'); s4 = h.find('Connected Services')
        block = h[s3:s4]; si = iter(d['stuck'])
        def card(m):
            t, x = next(si); return f'<h4 class="info-card__title">{html.escape(t, quote=False)}</h4><p class="info-card__text">{html.escape(x, quote=False)}</p>'
        block = re.sub(r'<h4 class="info-card__title">.*?</h4><p class="info-card__text">.*?</p>', card, block, flags=re.S)
        h = h[:s3] + block + h[s4:]
    # heading: the cards answer "why", so the heading asks "why"
    h = re.sub(r'Where ([\w &;,-]+?) shipments usually get stuck\.', r'Why \1 shipments usually get stuck.', h)
    if h != o: open(f, 'w').write(h); return True
    return False


changed = 0
for f in sorted(glob.glob('industries-*.html')):
    slug = f[len('industries-'):-5]
    if edit_industry(slug, f, IND.get(slug, {})): changed += 1
print('industry pages updated:', changed)

# ---------------------------------------------------------------- site-wide wording
def sub_all(pairs):
    n = 0
    for f in glob.glob('*.html'):
        h = open(f).read(); o = h
        for a, b in pairs: h = h.replace(a, b)
        if h != o: open(f, 'w').write(h); n += 1
    return n

print('wording files:', sub_all([
    ('right structure, registrations, import readiness', 'right structure, registration, import readiness'),
    ('designed to protect the shipment, support compliance and reduce handling risk', 'designed to protect the shipment and reduce handling risk'),
    ('Cargo protection arranged through licensed insurance partners, with coordinated support from quotation to claims documentation.', 'Cargo insurance with coordinated support from quotation to claims documentation.'),
    ('Complex cargo planned from permit mapping and customs clearance to port handling and final project-site delivery.', 'Project cargo, including break bulk and Out of Gauge (OOG) shipments, planned from permit mapping and customs clearance to port handling and final project-site delivery.'),
    ('Dangerous goods managed through', 'Dangerous Goods managed through'),
]))

h = open('index.html').read(); o = h
h = h.replace('We navigate the complexity of international maritime trade so your goods flow freely. Full container, LCL, and breakbulk, cleared at origin, compliant at destination.',
              'International ocean freight with customs built in. Full Container Load (FCL), Less-than-Container Load (LCL) and break bulk, cleared at origin and compliant at destination.')
h = h.replace('Bonded, tracked, and cleared at every step of the way. Cross-border trucking and inland logistics managed with the same rigor as your international shipments.',
              'Bonded, tracked and cleared at every step. Cross-border and inland trucking managed with the same rigor as your international shipments.')
h = h.replace('Secure storage integrated with your customs workflow.', 'Secure storage integrated with your inventory workflow.')
h = h.replace('Bonded warehousing, inventory management, and distribution, all under one roof. Your goods are ready to move the moment clearance is granted.',
              'Bonded warehousing, inventory management and distribution under one roof, so your goods are ready to move the moment clearance is granted.')
h = h.replace('Fully accredited with customs authorities across every major jurisdiction.', 'Fully accredited with customs and government authorities across every major jurisdiction.')
h = h.replace('<h3 class="why-point__title">Technology-Driven</h3>', '<h3 class="why-point__title">Compliance-First, Technology-Driven</h3>')
h = h.replace('Real-time visibility into every shipment, filing, and clearance. Our platform gives you instant access to documentation, status updates, and compliance data, 24/7.',
              'Real-time visibility into every shipment, filing and clearance, built on a compliance-first approach. Our platform gives you instant access to documentation, status updates and compliance data, 24/7.')
h = h.replace('Named account managers who know your supply chain inside out. Not a call center, but a partner who anticipates problems before they become delays.',
              'Named account managers who know your supply chain, and spot problems before they become delays.')
open('index.html', 'w').write(h) if h != o else None

# marquee: add PISM and PhilExport (text badges until logo files are supplied)
CHIPS = ('<div class="marquee__logo" title="Philippine Institute for Supply Chain Management">PISM</div>\n        '
         '<div class="marquee__logo" title="Philippine Exporters Confederation">PhilExport</div>\n        ')
for f in ('index.html', 'about.html'):
    h = open(f).read()
    if 'PhilExport' in h: continue
    h2 = re.sub(r'(<div class="marquee__logo has-image"><img src="assets/images/logos/sec-philippines\.png"[^>]*></div>\n)(\s*)', lambda m: m.group(1) + m.group(2) + CHIPS, h)
    if h2 != h: open(f, 'w').write(h2); print('marquee updated:', f, h2.count('PhilExport'))

# Locations: compliance-first network messaging
l = open('location.html').read(); o = l
l = l.replace('Based in Manila, connected to the world\'s major ports and trade cities.', 'The Mills Global builds an international trade network around compliance-first customs brokerage.')
l = l.replace('<p class="section__eyebrow animate-in">Our Reach</p>', '<p class="section__eyebrow animate-in">Trade Without Limits</p>')
l = l.replace('The Mills Global is based in Manila and works with a network of partners in major trade cities across Asia, the Middle East, Europe, Oceania and North America. Drag the globe to explore.',
              'The Mills Global is based in Manila and works with a worldwide network of partner law firms, visa services and Philippine customs brokers, so you can enter and import compliantly into the country you choose. Drag the globe to explore.')
if l != o: open('location.html', 'w').write(l); print('location updated')
