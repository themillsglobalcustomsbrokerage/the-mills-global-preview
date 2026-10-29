#!/usr/bin/env python3
"""Builds talk-to-a-broker.html: a minimal-friction paid-traffic landing page (call first, form second).
Reuses markup from the live pages so styles, scripts, tracking and the loading screen stay identical.
Indexed and in the sitemap."""
import re, os, html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
book = open('book-a-call.html', encoding='utf-8').read()
about = open('about.html', encoding='utf-8').read()
PHONE_TEL, PHONE = '+639177129000', '+63 917 712 9000'
URL = 'https://themillsglobal.com/talk-to-a-broker.html'
TITLE = 'Talk to a Customs Broker Today | The Mills Global'
DESC = 'Call The Mills Global and talk to a customs broker about your shipment. Customs clearance, permits and delivery under one team, with no forms and no waiting for a callback.'

# head: reuse the real head (fonts, css, loader, analytics), swap the page-specific bits
head = book[:book.index('</head>')]
head = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', head, flags=re.S)
head = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + DESC, head)
head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*', r'\g<1>' + TITLE, head)
head = re.sub(r'(<meta (?:property="og:description"|name="twitter:description") content=")[^"]*', r'\g<1>' + DESC, head)
head = head.replace('https://themillsglobal.com/book-a-call.html', URL)
head = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
head = head.replace('<link rel="stylesheet" href="css/service-page.css?v=3">',
                    '<link rel="stylesheet" href="css/service-page.css?v=3">\n  <link rel="stylesheet" href="css/content.css?v=4">\n  <link rel="stylesheet" href="css/landing.css?v=9">')
gtm = re.search(r'<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->', book, re.S).group(0)

def ico(path): return f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'
PHONE_ICO = ico('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/>')
CAL_ICO = ico('<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>')
MAIL_ICO = ico('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>')
def call_btn(label, where, cls='btn-primary'):
    return f'<a href="tel:{PHONE_TEL}" class="{cls}" data-ga="cta_call_now" data-ga-label="{where}">{PHONE_ICO} {label}</a>'
def book_btn(where):
    return f'<a href="#schedule" class="btn-secondary" data-ga="cta_book_consultation" data-ga-label="{where}">{CAL_ICO} Schedule A Meeting Today</a>'
def mail_btn(where):
    return f'<a href="mailto:inquiry@themillsglobal.com" class="btn-secondary" data-ga="cta_email" data-ga-label="{where}">{MAIL_ICO} Email Us</a>'
def one(where): return f'<div class="cta-pair">{call_btn("Give Us A Call Today", where)}</div>'
def two(where): return f'<div class="cta-pair">{call_btn("Give Us A Call Today", where)}{book_btn(where)}</div>'

nav = f"""<nav class="nav scrolled nav--lp" id="nav">
    <div class="nav__inner container">
      <a href="index.html" class="nav__logo" aria-label="The Mills Global home"><img src="assets/images/brand/mills-logo-horizontal-white.png" alt="The Mills Global" width="538" height="158"></a>
      <a href="tel:{PHONE_TEL}" class="nav__cta nav__cta--call" data-ga="cta_call_now" data-ga-label="lp-nav">{PHONE_ICO}<span class="nav__cta-num">{PHONE}</span><span class="nav__cta-short">Call Now</span></a>
    </div>
  </nav>"""

def stat(label, target, suffix):
    return f'<div class="lp-hero__stat"><div class="stat-number" data-target="{target}" data-suffix="{suffix}">{target:,}{suffix}</div><span>{label}</span></div>'
hero = f"""<header class="service-hero lp-hero" style="background-image: url('assets/images/hero-warehouse.jpg');">
    <div class="container">
      <div class="service-hero__inner">
      <div class="lp-hero__grid">
        <div class="lp-hero__copy">
          <p class="section__eyebrow service-hero__eyebrow">Trade Without Limits</p>
          <h1 class="service-hero__title">One Call. Every Logistics Problem, Solved.</h1>
          <p class="service-hero__subtitle">The Mills Global handles freight forwarding, customs clearance, permits, and legal compliance under one roof. We deliver a streamlined process from the first call to final delivery. No forms, no waiting on a callback.</p>
          {one("lp-hero")}
          <p class="lp-hero__mail">Prefer email? <a href="mailto:inquiry@themillsglobal.com">inquiry@themillsglobal.com</a> &rarr;</p>
          <p class="lp-hero__rating"><span aria-hidden="true">&#9733;</span> 4.9 on Google, 200+ Reviews <i></i> Licensed Customs Brokers</p>
        </div>
        <div class="lp-hero__media">
          <div class="lp-hero__stats">
            {stat("Years of Hands-On Experience", 15, "+")}
            {stat("Shipments Processed", 48000, "+")}
            {stat("Industries Supported", 24, "+")}
          </div>
        </div>
      </div>
      </div>
    </div>
  </header>"""

quotes = [("They handled our import documentation and customs clearance smoothly, with no surprises along the way.", "Maricris Caballero"),
          ("A rare combination: a customs brokerage firm that also brings real legal strategy to the table.", "Charina Estrella"),
          ("The most reliable customs clearance provider we've worked with, hands down.", "Jhun Hector Naelgas")]
cards = ''.join(f'<figure class="lp-quote animate-in" data-delay="{i+1}"><div class="lp-quote__stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><blockquote>&ldquo;{html.escape(q)}&rdquo;</blockquote><figcaption>{html.escape(n)}</figcaption></figure>' for i, (q, n) in enumerate(quotes))
# logo strip from the About page (same section the site uses), without its own heading: the quotes above carry the section
m = re.search(r'<div class="marquee".*?</div>\s*</div>\s*</section>', about[about.index('Accredited, affiliated and recognized'):], re.S)
marquee = about[about.index('Accredited, affiliated and recognized'):]
marquee = marquee[marquee.index('<div class="marquee"'):]
marquee = marquee[:marquee.index('</section>')]
proof = f"""<section class="section section--paper lp-proof">
    <div class="container">
      <div class="services-intro" style="text-align:center; align-items:center;">
        <p class="section__eyebrow animate-in" style="justify-content:center;">Trusted By Shippers Already Moving Cargo</p>
        <h2 class="services-intro__heading animate-in" data-delay="1" style="margin-left:auto; margin-right:auto;">What Clients Say After They Call.</h2>
      </div>
      <div class="lp-quotes lp-quotes--light">{cards}</div>
      <p class="lp-recognized"><strong>Licensed and recognized by:</strong> Securities and Exchange Commission &middot; Bureau of Internal Revenue &middot; Bureau of Customs &middot; Philippine Economic Zone Authority &middot; Confederation of Truckers Association &middot; Philippine Chamber of Commerce and Industry</p>
    </div>
    {marquee}
  </section>"""

tick = '<svg class="audience-list__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
why_items = ["One licensed team handling freight, customs, permits, and legal matters together",
             "Streamlined process from inquiry to final delivery",
             "Experience supporting large-scale shipments and business expansions into fully licensed operating entities",
             "Accredited specialists and licensed customs brokers who catch compliance issues before they cost you"]
why = f"""<section class="section section--dark">
    <div class="container" style="max-width: 880px;">
      <div class="services-intro" style="text-align:center; align-items:center;">
        <p class="section__eyebrow animate-in" style="justify-content:center;">Why The Mills Global</p>
        <h2 class="services-intro__heading animate-in" data-delay="1" style="margin-left:auto; margin-right:auto;">Built To Make You Grow.</h2>
      </div>
      <p class="services-intro__lead animate-in" data-delay="2" style="text-align:center; margin-left:auto; margin-right:auto;">Freight, customs, permits, and legal compliance rarely stay in separate lanes. We handle all of it under one roof, fast, streamlined, and organized like no other.</p>
      <div class="lp-card animate-in" data-delay="3">
        <p class="lp-card__title">{tick} With The Mills Global</p>
        <ul class="audience-list" style="grid-template-columns: 1fr;">
          {''.join(f'<li class="audience-list__item">{tick}<span>{t}</span></li>' for t in why_items)}
        </ul>
      </div>
      <div class="lp-center">{two("lp-why")}</div>
    </div>
  </section>"""

steps = [("Call &amp; Assessment", "Tell us your cargo, shipment type, and destination on the call."),
         ("Planning &amp; Documentation", "We map the right freight and customs plan and prepare the paperwork."),
         ("Customs Clearance &amp; Freight", "Licensed brokers manage clearance, permits, and duty planning."),
         ("Delivery &amp; Support", "Your shipment is delivered on schedule, with support that continues after.")]
HERE = '<span class="lp-here">You Are Here</span>'
def step_html(i, t, d):
    cls = ' how-steps__item--here' if i == 0 else ''
    badge = HERE if i == 0 else ''
    return f'<li class="how-steps__item{cls}">{badge}<span class="how-steps__num">0{i+1}</span><h3 class="how-steps__title">{t}</h3><p class="how-steps__text">{d}</p></li>'
steps_html = ''.join(step_html(i, t, d) for i, (t, d) in enumerate(steps))
services = ["LCL &amp; FCL Freight Forwarding", "Import &amp; Export Clearance", "Permits &amp; Licensing", "PEZA Shipments", "Tariff &amp; Customs Consultancy", "Business &amp; Legal Consultancy", "Customs Disputes &amp; Legal Remedies", "Crating &amp; Warehousing"]
how = f"""<section class="section section--paper lp-how">
    <div class="container">
      <div class="services-intro" style="text-align:center; align-items:center;">
        <p class="section__eyebrow animate-in" style="justify-content:center;">How Your Shipment Moves</p>
        <h2 class="services-intro__heading animate-in" data-delay="1" style="margin-left:auto; margin-right:auto;">Four Steps Of The Process, Done Fast.</h2>
      </div>
      <p class="services-intro__lead animate-in" data-delay="2" style="text-align:center; margin-left:auto; margin-right:auto;">A structured path from your first call to final delivery.</p>
      <ol class="how-steps">{steps_html}</ol>
      <div class="lp-center">{two("lp-how")}</div>
      <ul class="lp-tags lp-tags--center">{''.join(f"<li>{x}</li>" for x in services)}</ul>
    </div>
  </section>"""

broker = f"""<section class="section section--dark lp-call">
    <div class="container">
      <p class="section__eyebrow animate-in">Talk To A Broker Now</p>
      <h2 class="services-intro__heading animate-in" data-delay="1">Talk To A Broker In The Next Five Minutes.</h2>
      <p class="services-intro__lead animate-in" data-delay="2">No forms, no queue. Call the number below and describe your shipment. We'll take it from there.</p>
      <div class="cta-pair lp-call__buttons">{call_btn("Give Us A Call Today", "lp-broker")}</div>
      <p class="lp-call__sub animate-in" data-delay="4">Email <a href="mailto:inquiry@themillsglobal.com">inquiry@themillsglobal.com</a></p>
    </div>
  </section>"""

# booking section: the site's own, with one call button (as on the original page) above the Cal.com embed
cal = re.search(r'<section class="section section--paper book-call" id="book-call">.*?</section>', book, re.S).group(0)
cal = cal.replace('id="book-call"', 'id="schedule"')
cal = re.sub(r'<div class="book-call__actions">.*?</div>', '<div class="book-call__actions">' + call_btn("Give Us A Call Today", "lp-schedule") + '</div>', cal, count=1, flags=re.S)

# the same footer as every other page
footer = about[about.index('<footer class="footer">'):about.index('</footer>') + 9]
sticky = f'<a href="tel:{PHONE_TEL}" class="lp-callbar" data-ga="cta_call_now" data-ga-label="lp-sticky">{PHONE_ICO} Call {PHONE}</a>'

scripts = """<script src="js/vendor/lenis.min.js"></script>
  <script src="js/smooth.js?v=1"></script>
  <script src="js/cursor.js?v=7"></script>
  <script src="js/analytics.js"></script>
  <script src="js/animations.js?v=7"></script>
  <script src="js/cal-embed.js" defer></script>"""
page = f"""{head}
</head>
<body class="lp">
  {gtm}

  {nav}

  {hero}

  {proof}

  {why}

  {how}

  {broker}

  {cal}

  {footer}
  {sticky}

  {scripts}

</body>
</html>
"""
open('talk-to-a-broker.html', 'w', encoding='utf-8').write(page)
print('wrote talk-to-a-broker.html', len(page), 'bytes')
