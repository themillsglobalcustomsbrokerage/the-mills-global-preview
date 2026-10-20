#!/usr/bin/env python3
"""Hero subtitles for all services and industries: core offer + main benefit, concrete, not tied to one country.
Replaces each page's old subtitle everywhere it is repeated (hub cards, contact blocks)."""
import re, glob, os, html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
NEW = {
 'services-mills-entry': ('Market Entry & Import Readiness', "Set up the right company structure, registrations and permits before you buy, so your first shipment arrives compliant, on time and without costly surprises."),
 'services-mills-permits': (None, "We work out which agencies must approve your product, prepare and file every permit and registration, and match each one to your shipment, so regulated cargo is never held for missing paperwork."),
 'services-mills-customs': (None, "We classify, value and file your customs entries and manage the release, so your cargo clears correctly the first time, with accurate duties and no avoidable holds."),
 'services-mills-marine': (None, "We handle registration, port and customs requirements for vessels, yachts and marine equipment as one process, and rush critical spares to a waiting vessel."),
 'services-mills-dangerous-goods': (None, "We identify, classify, document and pack your Dangerous Goods to the rules, so carriers accept the cargo and it moves without last-minute refusals."),
 'services-mills-logistics': (None, "From customs release to the consignee's door, we run drayage, storage and trucking as one plan, with proof of delivery, so cleared cargo arrives on schedule and intact."),
 'services-mills-packaging': (None, "Export-grade crating and protective packing built around your cargo's weight, route and rules, so machinery and high-value goods arrive undamaged and pass inspection."),
 'services-mills-insurance': (None, "We arrange marine and transit cargo cover matched to your shipment's value, route and handling, and keep the records a claim needs, so a loss never turns into a dispute."),
 'services-mills-time-critical': (None, "When cargo cannot wait, we clear and deliver it on a priority track with one owner for every document and hold, so urgent shipments do not sit at the port."),
 'services-mills-advisory': (None, "Get a clear answer on the rules, permits and customs risks before you commit, plus a practical plan for what to do first, so decisions rest on facts, not assumptions."),
 'services-mills-projects': (None, "We plan and move project cargo, including break bulk and Out of Gauge (OOG) shipments, from permits and customs through port handling to the site, so one missed requirement never stalls your schedule."),
 'industries-construction': (None, "We clear and deliver cranes, excavators, steel and project materials from permit to site, including oversized pieces, so crews and schedules never wait on equipment."),
 'industries-renewable-energy': (None, "We move solar, storage, wind and hydro equipment through permits, incentives and customs to the project site, so your build stays on its delivery window."),
 'industries-data-centers': (None, "We clear and deliver servers, cooling, power and security equipment on schedule, handling batteries and mixed categories, so your facility goes live when planned."),
 'industries-chemicals': (None, "We match your substance to the permits, controlled-chemical approvals and Dangerous Goods rules it needs, then clear and deliver it, so chemical shipments are accepted, not stranded."),
 'industries-food-beverage': (None, "We align registration, labeling, tax and cold-chain requirements for food, beverage and Fast-Moving Consumer Goods (FMCG), so products clear and reach the shelf compliant and in date."),
 'industries-manufacturing': (None, "We import and deliver production machinery with correct classification and valuation, packed and sequenced for installation, so your line starts on schedule."),
 'industries-automotive': (None, "Know before you buy: we confirm a vehicle or equipment unit can be imported and what it will really cost once taxes and permits are in, then clear it and deliver it, so no unit is ever stranded at the port."),
 'industries-healthcare': (None, "We secure the right authorizations, clear medicines, vaccines and medical devices, and deliver them temperature-controlled, so patient-critical cargo is released fast and fully compliant."),
 'industries-agriculture': (None, "We coordinate plant, animal and fishery clearances across every agency involved, so perishable and live cargo clears quickly and arrives in condition."),
 'industries-electronics-telecom': (None, "We secure the approvals for radio equipment and handle batteries and classification, so connected devices and telecom hardware clear without holds and reach your channel on time."),
 'industries-marine': (None, "We handle registration, customs and port requirements for yachts, vessels, landing craft tanks (LCTs) and marine equipment, so your asset is cleared, registered and operating without delay."),
 'industries-aviation': (None, "We clear aircraft, engines and parts with the technical paperwork matched, and give Aircraft on Ground (AOG) shipments priority, so aircraft are back in service sooner."),
 'industries-retail': (None, "We clear apparel, appliances, beauty and consumer goods through the right product approvals and valuation, so inventory arrives compliant and ready to sell."),
 'industries-cold-chain': (None, "Reefer trucking, qualified cold storage and timely delivery, with permits and customs coordinated, so frozen, chilled and temperature-sensitive cargo stays in range from port to store."),
 'industries-mining': (None, "We move heavy equipment, controlled materials and mixed shipments through customs to remote sites, with explosives and reagent permits handled, so operations are not held up waiting for cargo."),
 'industries-freight-forwarders': (None, "We clear your clients' cargo, including regulated shipments, with permits and authority handled, so you offer reliable clearance without building a customs team."),
}
SUB = re.compile(r'(<p class="service-hero__subtitle">)(.*?)(</p>)', re.S)
olds = {}
for key, (h1, new) in NEW.items():
    f = key + '.html'; h = open(f).read(); o = h
    m = SUB.search(h); old = m.group(2)
    if old != html.escape(new, quote=False): olds[old] = html.escape(new, quote=False)
    if h1: h = re.sub(r'(<h1 class="service-hero__title">)(.*?)(</h1>)', lambda m: m.group(1) + html.escape(h1, quote=False) + m.group(3), h, 1, flags=re.S)
    if h != o: open(f, 'w').write(h)
n = 0
for f in glob.glob('*.html'):
    h = open(f).read(); o = h
    for old, new in olds.items():
        h = h.replace(old, new); h = h.replace(html.unescape(old), html.unescape(new))
    if h != o: open(f, 'w').write(h); n += 1
print('subtitles replaced in', n, 'pages;', len(olds), 'changed subtitles')
