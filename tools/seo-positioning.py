"""Adds the crawlable 'at a glance' fact block and positioning metadata (home, about, locations,
services/industries hubs) so search and AI answers can quote the numbers, services and industries."""
import re, json, html
SERVICES = [('services-mills-entry.html','Mills Entry'),('services-mills-permits.html','Mills Permits'),('services-mills-customs.html','Mills Customs'),
 ('services-mills-projects.html','Mills Projects'),('services-mills-marine.html','Mills Marine'),('services-mills-dangerous-goods.html','Mills Dangerous Goods'),
 ('services-mills-logistics.html','Mills Logistics'),('services-mills-packaging.html','Mills Packaging'),('services-mills-insurance.html','Mills Insurance'),
 ('services-mills-time-critical.html','Mills Time Critical'),('services-mills-advisory.html','Mills Advisory')]
ih = open('industries.html').read()
INDUSTRIES = [(a, html.unescape(b)) for a, b in re.findall(r'<a href="(industries-[\w-]+\.html)"[^>]*>.*?<h3[^>]*>(.*?)</h3>', ih, re.S)]
assert len(INDUSTRIES) == 16, len(INDUSTRIES)
STATS = [('15+', 'years of experience'), ('50K+', 'shipments cleared annually'), ('98.7%', 'compliance rate'), ('24/7', 'support availability'),
         ('33+', 'partners abroad'), ('50+', 'partners in Russia'), ('37', 'countries and territories')]
LEAD = ('The Mills Global is a Philippine customs brokerage and trade-execution firm based in Manila. It offers 11 core services, from customs clearance and import permits to project cargo, marine, dangerous goods and logistics, for 16 core industries.')

def block():
    st = ''.join(f'<li><strong>{n}</strong><span>{l}</span></li>' for n, l in STATS)
    sv = ''.join(f'<li><a href="{u}">{n}</a></li>' for u, n in SERVICES)
    ind = ''.join(f'<li><a href="{u}">{html.escape(n)}</a></li>' for u, n in INDUSTRIES)
    return f'''  <section class="section section--paper glance" id="at-a-glance">
    <div class="container">
      <p class="section__eyebrow animate-in">What We Do</p>
      <h2 class="services-intro__heading animate-in" data-delay="1">Core services and core industries.</h2>
      <p class="glance__lead animate-in" data-delay="2">{LEAD}</p>
      <div class="glance__cols">
        <div>
          <h3 class="glance__title">11 core services</h3>
          <ul class="glance__list">{sv}</ul>
        </div>
        <div>
          <h3 class="glance__title">16 core industries</h3>
          <ul class="glance__list">{ind}</ul>
        </div>
      </div>
    </div>
  </section>

'''

def setmeta(h, title, desc):
    h = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title, quote=False)}</title>', h, 1, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + html.escape(desc) + '"', h, 1)
    for k in ('og:title', 'twitter:title'):
        h = re.sub(rf'(<meta (?:property|name)="{k}" content=")[^"]*"', lambda m: m.group(1) + html.escape(title, quote=False) + '"', h, 1)
    for k in ('og:description', 'twitter:description'):
        h = re.sub(rf'(<meta (?:property|name)="{k}" content=")[^"]*"', lambda m: m.group(1) + html.escape(desc) + '"', h, 1)
    return h

ORG_DESC = LEAD
def update_org(h):
    def fix(m):
        o = json.loads(m.group(1))
        if o.get('@type') != ['Organization', 'ProfessionalService']: return m.group(0)
        o['description'] = ORG_DESC
        o['slogan'] = 'Philippine customs brokerage and trade execution'
        o['knowsAbout'] = [n for _, n in INDUSTRIES] + ['Customs brokerage', 'Import permits', 'Tariff classification', 'Project cargo']
        o['hasOfferCatalog'] = {"@type": "OfferCatalog", "name": "Core services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": 'https://themillsglobal.com/' + u}} for u, n in SERVICES]}
        o['additionalProperty'] = [{"@type": "PropertyValue", "name": l.capitalize(), "value": n} for n, l in STATS]
        return '<script type="application/ld+json">\n' + json.dumps(o, indent=2, ensure_ascii=False) + '\n  </script>'
    return re.sub(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', fix, h, flags=re.S)

def edit(f, fn):
    h = open(f).read(); n = fn(h)
    if n != h: open(f, 'w').write(n); print('updated', f)

TITLE_HOME = 'The Mills Global | Philippine Customs Broker: 33+ Partners Abroad, 11 Core Services'
DESC_HOME = ('Philippine customs brokerage with 33+ partners abroad across 37 countries and territories. 15+ years, 50K+ shipments cleared annually, 98.7% compliance, '
             '24/7 support. 11 core services across 16 industries.')

def home(h):
    h = setmeta(h, TITLE_HOME, DESC_HOME)
    if 'id="at-a-glance"' not in h:
        h = h.replace('  <section class="section section--dark" id="faq">', block() + '  <section class="section section--dark" id="faq">', 1)
    return update_org(h)
def about(h):
    h = setmeta(h, 'About The Mills Global | Philippine Customs Broker with a Global Partner Network',
                'The Mills Global is a Philippine customs brokerage and trade-execution firm with 33+ partners abroad, 11 core services and 16 core industries.')
    if 'id="at-a-glance"' not in h:
        i = h.index('<section class="section section--sky">')
        h = h[:i] + block() + '  ' + h[i:]
    return update_org(h)
def loc(h):
    h = setmeta(h, 'Customs Broker Locations: 33+ Partners Abroad in 37 Countries and Territories | The Mills Global',
                'The Mills Global is based in Manila (BGC and Binondo) with a partner network across 37 countries and territories, including Singapore, Dubai, London and New York.')
    return update_org(h)
def hub_services(h): return h
def hub_ind(h):
    return setmeta(h, 'Customs Brokerage for 16 Industries in the Philippines | The Mills Global',
                   'The Mills Global handles Philippine import compliance for 16 core industries, including healthcare, food and beverage, agriculture, data centers, manufacturing, marine and aviation.')

edit('index.html', home); edit('about.html', about); edit('location.html', loc); edit('industries.html', hub_ind)
