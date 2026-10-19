#!/usr/bin/env python3
"""Generates the importable n8n workflows from the guide list in js/lead-magnet.js and the page copy:
   n8n/lead-magnet-services.json      capture workflow, 11 service checklists (Zoho lead + team notification)
   n8n/lead-magnet-industries.json    capture workflow, 16 industry checklists
   n8n/followups/followup-<slug>.json one email series per service / industry (Email 1 now, Email 2 day 3, Email 3 day 7)
The email HTML lives in tools/email-builder.js (brand palette, dark-mode safe, WCAG AA)."""
import re, json, uuid, os, html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
js = open('js/lead-magnet.js').read()
G, _ = json.JSONDecoder().raw_decode(js[js.index('var GUIDES = ') + len('var GUIDES = '):])
EMAIL_JS = open('tools/email-builder.js').read()
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'tools'))
from email_copy_data import COPY, SCENE
VARIANTS = json.load(open('tools/email_variants.json'))
DRIVE = json.load(open('tools/drive_links.json'))   # direct Google Drive download link per guide

SERVICES = {'entry': 'Mills Entry', 'permits': 'Mills Permits', 'customs': 'Mills Customs', 'marine': 'Mills Marine',
            'dangerous-goods': 'Mills Dangerous Goods', 'logistics': 'Mills Logistics', 'packaging': 'Mills Packaging',
            'insurance': 'Mills Insurance', 'time-critical': 'Mills Time Critical', 'advisory': 'Mills Advisory', 'projects': 'Mills Projects'}
INDUSTRIES = {'industry-construction': 'Construction', 'industry-renewable-energy': 'Renewable Energy', 'industry-data-centers': 'Data Centers',
              'industry-chemicals': 'Chemicals', 'industry-food-beverage': 'Food & Beverage', 'industry-manufacturing': 'Manufacturing',
              'industry-automotive': 'Automotive', 'industry-healthcare': 'Healthcare', 'industry-agriculture': 'Agriculture',
              'industry-electronics-telecom': 'Electronics & Telecom', 'industry-marine': 'Marine', 'industry-aviation': 'Aviation',
              'industry-retail': 'Retail', 'industry-cold-chain': 'Cold Chain', 'industry-mining': 'Mining', 'industry-freight-forwarders': 'Freight Forwarders'}
assert len(INDUSTRIES) == 16 and all(k in G for k in INDUSTRIES), set(INDUSTRIES) - set(G)
# Plain-language topic used in subject lines and sentences ("your ___ checklist", "Want us to look at Acme's ___?")
TOPICS = {'entry': 'Philippine market entry', 'permits': 'import permits', 'customs': 'customs clearance', 'projects': 'project cargo',
          'marine': 'vessel and marine equipment', 'dangerous-goods': 'dangerous goods shipping', 'logistics': 'post-clearance delivery',
          'packaging': 'export packaging', 'insurance': 'cargo insurance', 'time-critical': 'time-critical cargo', 'advisory': 'Philippine trade compliance',
          'industry-agriculture': 'agricultural imports', 'industry-automotive': 'vehicle and equipment imports', 'industry-aviation': 'aviation parts imports',
          'industry-chemicals': 'chemical imports', 'industry-cold-chain': 'cold chain cargo', 'industry-construction': 'construction equipment imports',
          'industry-data-centers': 'data center equipment imports', 'industry-electronics-telecom': 'electronics and telecom imports',
          'industry-food-beverage': 'food and beverage imports', 'industry-freight-forwarders': 'forwarder clearance', 'industry-healthcare': 'healthcare imports',
          'industry-manufacturing': 'manufacturing equipment imports', 'industry-marine': 'marine imports', 'industry-mining': 'mining imports',
          'industry-renewable-energy': 'renewable energy equipment imports', 'industry-retail': 'retail imports'}

KINDS = [
    dict(key='service', label='Service', plural='services', names=SERVICES, field='Service', file='n8n/lead-magnet-services.json',
         path='mills-lead-magnet', config='WEBHOOK_URL', wf='Mills | Lead magnet - all 11 services'),
    dict(key='industry', label='Industry', plural='industries', names=INDUSTRIES, field='Industry_Segment', file='n8n/lead-magnet-industries.json',
         path='mills-lead-magnet-industry', config='WEBHOOK_URL_INDUSTRY', wf='Mills | Lead magnet - all 16 industries'),
]


def page_facts(slug, kind):
    f = ('services-mills-%s.html' % slug) if kind == 'service' else ('industries-%s.html' % slug[len('industry-'):])
    h = open(f).read()
    sub = re.search(r'service-hero__subtitle[^>]*>(.*?)</p>', h, re.S)
    stuck = re.findall(r'<li><strong>(.*?)</strong><span>(.*?)</span></li>', h[h.find('stuck-list'):h.find('stuck-list') + 3000], re.S) if 'stuck-list' in h else []
    if not stuck:   # industry pages use info cards under "Where ... usually get stuck"
        i = h.find('usually get stuck')
        stuck = re.findall(r'<h4 class="info-card__title">(.*?)</h4><p class="info-card__text">(.*?)</p>', h[i:i + 2500], re.S) if i > 0 else []
    clean = lambda t: html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
    def sentence(t):   # the pages now use Title Case for card titles; emails read better in sentence case
        w = clean(t).split(' ')
        return ' '.join(x if (i == 0 and x[:1].isupper()) or any(c.isupper() for c in x[1:]) or x.isupper() else x.lower() for i, x in enumerate(w))
    return {'summary': clean(sub.group(1)) if sub else '', 'url': 'https://themillsglobal.com/' + f,
            'stuck': [{'t': sentence(a), 'd': clean(b)} for a, b in stuck][:3]}


nid = lambda: str(uuid.uuid4())
link = lambda n: {'node': n['name'], 'type': 'main', 'index': 0}
ORIGINS = 'https://themillsglobal.com,https://www.themillsglobal.com,https://themillsglobalcustomsbrokerage.github.io'

# ------------------------------------------------------------------ capture workflow (form -> Zoho lead + team notification)
CAPTURE_CODE = '''// Mills lead magnet (%(plural)s): validate, normalize and enrich one form submission.
const GUIDES = %(guides)s;

// Who is notified for each %(key)s. Replace the addresses with the person who owns it.
const DEFAULT_OWNER = 'inquiry@themillsglobal.com';
const OWNERS = %(owners)s;

const b = $input.first().json.body || {};
const clean = (v) => String(v == null ? '' : v).trim();
const guide = clean(b.guide);
const email = clean(b.email).toLowerCase();
const digits = clean(b.phone).replace(/\\D/g, '');
const g = GUIDES[guide];

let error = '';
if (clean(b.hp)) error = 'spam';
else if (!g) error = 'unknown guide: ' + guide;
else if (clean(b.name).length < 2) error = 'name';
else if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) error = 'email';
else if (digits.length < 7 || digits.length > 15) error = 'phone';
else if (clean(b.company).length < 2) error = 'company';

const name = clean(b.name);
const FREE = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com', 'live.com', 'proton.me', 'protonmail.com'];
const domain = email.split('@')[1] || '';
const fromAd = !!(clean(b.gclid) || clean(b.gbraid) || clean(b.wbraid));
// Hot = came from a Google ad, or used a company email address
const priority = (fromAd || (domain && !FREE.includes(domain))) ? 'Hot' : 'Normal';
return [{ json: {
  notify_to: (g && OWNERS[g.%(key)s]) || DEFAULT_OWNER,
  priority,
  valid: !error,
  error,
  submitted_at: clean(b.submitted_at) || new Date().toISOString(),
  guide,
  %(key)s: g ? g.%(key)s : '',
  guide_title: g ? g.title : clean(b.guide_title),
  name,
  first_name: name.split(/\\s+/).length > 1 ? name.split(/\\s+/)[0] : '',
  last_name: name.split(/\\s+/).length > 1 ? name.split(/\\s+/).slice(1).join(' ') : name,
  email,
  phone: clean(b.phone),
  company: clean(b.company),
  page: clean(b.page),
  gclid: clean(b.gclid), gbraid: clean(b.gbraid), wbraid: clean(b.wbraid),
  utm_source: clean(b.utm_source), utm_medium: clean(b.utm_medium), utm_campaign: clean(b.utm_campaign),
  utm_term: clean(b.utm_term), utm_content: clean(b.utm_content),
  lead_source: 'lead_magnet'
} }];'''


def build(k):
    key, label = k['key'], k['label']
    cfg = {s: {key: n, 'title': G[s]['title'], 'pdf': G[s]['pdf']} for s, n in k['names'].items()}
    owners = '{\n  ' + ',\n  '.join(f"{json.dumps(n)}: DEFAULT_OWNER" for n in k['names'].values()) + '\n}'
    code = CAPTURE_CODE % dict(plural=k['plural'], key=key, guides=json.dumps(cfg, indent=2), owners=owners)
    webhook = {'parameters': {'httpMethod': 'POST', 'path': k['path'], 'responseMode': 'responseNode', 'options': {'allowedOrigins': ORIGINS}},
               'id': nid(), 'name': 'Webhook - lead magnet form', 'type': 'n8n-nodes-base.webhook', 'typeVersion': 2, 'position': [0, 0], 'webhookId': nid()}
    codeN = {'parameters': {'jsCode': code}, 'id': nid(), 'name': 'Validate and normalize', 'type': 'n8n-nodes-base.code', 'typeVersion': 2, 'position': [240, 0]}
    ifN = {'parameters': {'conditions': {'options': {'caseSensitive': True, 'leftValue': '', 'typeValidation': 'strict'},
           'conditions': [{'id': nid(), 'leftValue': '={{ $json.valid }}', 'rightValue': '', 'operator': {'type': 'boolean', 'operation': 'true', 'singleValue': True}}],
           'combinator': 'and'}, 'options': {}}, 'id': nid(), 'name': 'Valid submission?', 'type': 'n8n-nodes-base.if', 'typeVersion': 2.2, 'position': [480, 0]}
    ok = {'parameters': {'respondWith': 'json', 'responseBody': '={{ JSON.stringify({ ok: true }) }}', 'options': {'responseCode': 200}},
          'id': nid(), 'name': 'Respond 200', 'type': 'n8n-nodes-base.respondToWebhook', 'typeVersion': 1.1, 'position': [720, -100]}
    bad = {'parameters': {'respondWith': 'json', 'responseBody': '={{ JSON.stringify({ ok: false, error: $json.error }) }}', 'options': {'responseCode': 400}},
           'id': nid(), 'name': 'Respond 400', 'type': 'n8n-nodes-base.respondToWebhook', 'typeVersion': 1.1, 'position': [720, 160]}
    desc = ('Lead magnet: {{ $json.guide_title }}\n%s: {{ $json.%s }}\nPriority: {{ $json.priority }}\nPage: {{ $json.page }}\n'
            'Ad source: {{ $json.utm_source }} / {{ $json.utm_medium }} / {{ $json.utm_campaign }}\nGCLID: {{ $json.gclid }}\nSubmitted: {{ $json.submitted_at }}') % (label, key)
    zoho = {'parameters': {'resource': 'lead', 'operation': 'upsert', 'lastName': '={{ $json.last_name }}',
            'additionalFields': {'First_Name': '={{ $json.first_name }}', 'Company': '={{ $json.company }}', 'Email': '={{ $json.email }}', 'Phone': '={{ $json.phone }}',
                                 'Lead_Source': 'Website', 'Lead_Status': 'Not Contacted', 'Description': '=' + desc,
                                 'customFields': {'customFields': [{'fieldId': k['field'], 'value': '={{ $json.%s }}' % key}, {'fieldId': 'Priority', 'value': '={{ $json.priority }}'}]}}},
            'id': nid(), 'name': 'Create or update lead in Zoho CRM', 'type': 'n8n-nodes-base.zohoCrm', 'typeVersion': 1, 'position': [960, -100], 'onError': 'continueRegularOutput'}
    notif = '''<p><strong>New lead magnet download</strong></p>
<p>%s: {{ $json.%s }}<br>Checklist: {{ $json.guide_title }}</p>
<p>Name: {{ $json.name }}<br>Company: {{ $json.company }}<br>Email: {{ $json.email }}<br>Phone: {{ $json.phone }}</p>
<p>Page: {{ $json.page }}<br>Ad source: {{ $json.utm_source }} / {{ $json.utm_campaign }} {{ $json.gclid ? '(gclid ' + $json.gclid + ')' : '' }}</p>''' % (label, key)
    mail = {'parameters': {'sendTo': '={{ $json.notify_to }}', 'subject': '=New lead: {{ $json.%s }} - {{ $json.company }}' % key, 'emailType': 'html', 'message': '=' + notif,
            'options': {'appendAttribution': False}},
            'id': nid(), 'name': 'Notify the team', 'type': 'n8n-nodes-base.gmail', 'typeVersion': 2.1, 'position': [960, 120], 'onError': 'continueRegularOutput'}
    values = ', '.join(k['names'].values())
    note_text = (f"## {k['wf']} (Zoho CRM)\n**Webhook:** POST, form-urlencoded (what the site sends). The Respond nodes return JSON so the site sees a 200.\n**Setup:**\n"
                 f"1. Pick your Zoho CRM (OAuth2, your data center) and Gmail credentials on the two action nodes.\n"
                 f"2. **Segmentation.** In Zoho create custom Lead fields: {label} (picklist, API name {k['field']}) with the values: {values}. And Priority (picklist: Hot, Normal; API name Priority). Then make one Custom View per {key} filtered on that field.\n"
                 f"3. The emails (checklist now, follow-ups on day 3 and day 7) are sent by the separate follow-up workflows in n8n/followups/, triggered from Zoho when this workflow creates the lead.\n"
                 f"4. Set each {key} owner's email in the OWNERS list in the code node; the team notification goes to that person.\n"
                 f"5. Activate, then copy the **Production URL** into js/lead-magnet.js ({k['config']}).\n"
                 f"**Test:** use the Test URL once, then switch to Production.")
    note = {'parameters': {'content': note_text, 'height': 440, 'width': 480, 'color': 5}, 'id': nid(), 'name': 'Setup notes', 'type': 'n8n-nodes-base.stickyNote',
            'typeVersion': 1, 'position': [-20, -520]}
    conn = {webhook['name']: {'main': [[link(codeN)]]}, codeN['name']: {'main': [[link(ifN)]]},
            ifN['name']: {'main': [[link(ok)], [link(bad)]]}, ok['name']: {'main': [[link(zoho), link(mail)]]}}
    wf = {'name': k['wf'], 'nodes': [note, webhook, codeN, ifN, ok, bad, zoho, mail], 'connections': conn,
          'active': False, 'settings': {'executionOrder': 'v1'}, 'pinData': {}, 'meta': {'templateCredsSetupCompleted': False}}
    os.makedirs('n8n', exist_ok=True)
    json.dump(wf, open(k['file'], 'w'), indent=2)
    print('written', k['file'], len(json.dumps(wf)), 'bytes;', len(cfg), k['plural'])


# ------------------------------------------------------------------ follow-up workflow (Zoho -> Email 1 now, Email 2 day 3, Email 3 day 7)
FOLLOW_HEAD = '''// Prepare the lead sent by the Zoho workflow rule and build all three emails for this %(key)s.
const TOKEN = 'CHANGE_ME';   // must match the "token" parameter set in the Zoho webhook
const SITE = 'https://themillsglobal.com/';   // checklist PDFs and links are served from here
const SEG = %(seg)s;

const b = $input.first().json.body || {};
const clean = (v) => String(v == null ? '' : v).trim();
const esc = (t) => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const email = clean(b.email).toLowerCase();
// Each lead is signed by Ari or Joshua, chosen from the email address so the same person signs all three emails
const SENDERS = ['Ari', 'Joshua'];
let hsh = 0;
for (const ch of email) hsh = (hsh * 31 + ch.charCodeAt(0)) >>> 0;
const sender = SENDERS[hsh %% SENDERS.length];
const valid = clean(b.token) === TOKEN && /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email) && !!clean(b.lead_id);
const out = {
  valid,
  lead_id: clean(b.lead_id),
  email,
  first_name_greeting: clean(b.first_name) || 'there',
  company: clean(b.company),
  segment: SEG.name,
  topic: SEG.topic,
  short: SEG.short,
  scene: SEG.scene,
  check: SEG.check,
  send: SEG.send,
  v: SEG.v,
  sender_name: sender,
  first_name: clean(b.first_name),
  guide_title: SEG.guide_title,
  pdf_url: SEG.drive,   // Google Drive direct download link (works before the website domain is live)
  page_url: SEG.url,
  book_url: SITE + 'book-a-call.html',
  stuck: SEG.stuck
};
'''


def build_followup(k, slug, name, idx):
    key, label = k['key'], k['label']
    seg = dict({'name': name, 'short': name.replace('Mills ', '').lower(), 'topic': TOPICS[slug], 'guide_title': G[slug]['title'], 'pdf': G[slug]['pdf'],
                'drive': DRIVE[slug], 'scene': SCENE[slug], 'check': COPY[slug][0], 'send': COPY[slug][1], 'v': idx}, **page_facts(slug, key))
    code = FOLLOW_HEAD % dict(key=key, seg=json.dumps(seg, indent=2)) + '\nconst VARIANTS = ' + json.dumps(VARIANTS, indent=1) + ';\n' + EMAIL_JS
    P = 'Prepare lead'
    R = lambda f: "{{ $('%s').item.json.%s }}" % (P, f)
    mail = lambda nm, n, pos: {'parameters': {'sendTo': '=' + R('email'), 'subject': '=' + R('subject%d' % n), 'emailType': 'html', 'message': '=' + R('html%d' % n),
            'options': {'appendAttribution': False, 'senderName': '=' + R('sender_name') + ' from The Mills Global', 'replyTo': 'inquiry@themillsglobal.com'}},
            'id': nid(), 'name': nm, 'type': 'n8n-nodes-base.gmail', 'typeVersion': 2.1, 'position': pos}
    wait = lambda nm, days, pos: {'parameters': {'amount': days, 'unit': 'days'}, 'id': nid(), 'name': nm, 'type': 'n8n-nodes-base.wait', 'typeVersion': 1.1, 'position': pos, 'webhookId': nid()}
    getlead = lambda nm, pos: {'parameters': {'resource': 'lead', 'operation': 'get', 'leadId': '=' + R('lead_id')}, 'id': nid(), 'name': nm,
            'type': 'n8n-nodes-base.zohoCrm', 'typeVersion': 1, 'position': pos}
    cond = lambda nm, expr, pos: {'parameters': {'conditions': {'options': {'caseSensitive': True, 'leftValue': '', 'typeValidation': 'strict'},
            'conditions': [{'id': nid(), 'leftValue': expr, 'rightValue': '', 'operator': {'type': 'boolean', 'operation': 'true', 'singleValue': True}}], 'combinator': 'and'}, 'options': {}},
            'id': nid(), 'name': nm, 'type': 'n8n-nodes-base.if', 'typeVersion': 2.2, 'position': pos}
    still = "={{ $json.Lead_Status === 'Not Contacted' && !$json.Email_Opt_Out }}"
    hook = {'parameters': {'httpMethod': 'POST', 'path': 'mills-followup-' + slug, 'responseMode': 'onReceived', 'options': {}},
            'id': nid(), 'name': 'Webhook from Zoho', 'type': 'n8n-nodes-base.webhook', 'typeVersion': 2, 'position': [0, 0], 'webhookId': nid()}
    prep = {'parameters': {'jsCode': code}, 'id': nid(), 'name': P, 'type': 'n8n-nodes-base.code', 'typeVersion': 2, 'position': [240, 0]}
    valid = cond('Valid request?', '={{ $json.valid }}', [480, 0])
    e1 = mail('Email 1 - checklist (now)', 1, [720, 0])
    w1 = wait('Wait 3 days', 3, [960, 0]); g1 = getlead('Check lead in Zoho (day 3)', [1200, 0]); c1 = cond('Still not contacted? (day 3)', still, [1440, 0])
    e2 = mail('Email 2 - quick check (day 3)', 2, [1680, 0])
    w2 = wait('Wait 4 more days', 4, [1920, 0]); g2 = getlead('Check lead in Zoho (day 7)', [2160, 0]); c2 = cond('Still not contacted? (day 7)', still, [2400, 0])
    e3 = mail('Email 3 - closing the loop (day 7)', 3, [2640, 0])
    note_text = (f"## Email series: {name}\n**Trigger:** a Zoho CRM Workflow Rule on Leads (when created, and {label} = {name}) calls this webhook with body parameters: "
                 "lead_id, email, first_name, company, token (= the TOKEN constant in the code node).\n"
                 "**Flow:** Email 1 (the checklist download) goes out immediately. After 3 days, if the lead is still 'Not Contacted' and has not opted out, Email 2 goes out; "
                 "after 4 more days (day 7), under the same condition, Email 3. The email HTML (brand colors, dark-mode safe) is built in the 'Prepare lead' code node.\n"
                 "**Setup:** pick Zoho CRM and Gmail credentials, change TOKEN, activate, copy the Production URL into the Zoho webhook. "
                 "Set SITE at the top of the code node if the checklist PDFs are served from a different domain.")
    note = {'parameters': {'content': note_text, 'height': 330, 'width': 560, 'color': 5}, 'id': nid(), 'name': 'Setup notes', 'type': 'n8n-nodes-base.stickyNote', 'typeVersion': 1, 'position': [-20, -400]}
    chain = [hook, prep, valid, e1, w1, g1, c1, e2, w2, g2, c2, e3]
    conn = {n['name']: {'main': [[link(chain[i + 1])]]} for i, n in enumerate(chain[:-1])}   # IF nodes: only the true output continues
    wf = {'name': 'Mills | Email series - ' + name, 'nodes': [note] + chain, 'connections': conn, 'active': False, 'settings': {'executionOrder': 'v1'}, 'pinData': {}, 'meta': {'templateCredsSetupCompleted': False}}
    os.makedirs('n8n/followups', exist_ok=True)
    json.dump(wf, open('n8n/followups/followup-%s.json' % slug, 'w'), indent=2)
    return slug, name, 'mills-followup-' + slug, label


for kind in KINDS:
    build(kind)

rows = []
idx = 0
for kind in KINDS:
    for slug, name in kind['names'].items():
        rows.append(build_followup(kind, slug, name, idx)); idx += 1
md = ['# Email series workflows (one per service and industry)', '',
      'Each file here is an importable n8n workflow. A Zoho CRM Workflow Rule (Leads, on create, with the field below equal to the value) calls its webhook. '
      'Email 1 (the checklist) goes out immediately; Email 2 on day 3 and Email 3 on day 7, only while the lead is still "Not Contacted" in Zoho.', '',
      'Zoho webhook body parameters: `lead_id` = Lead Id, `email` = Email, `first_name` = First Name, `company` = Company, `token` = the TOKEN you set in each code node.', '',
      '| Segment | Zoho field = value | n8n webhook path | File |', '|---|---|---|---|']
for slug, name, path, label in rows:
    fld = 'Service' if label == 'Service' else 'Industry_Segment'
    md.append(f'| {name} | {fld} = {name} | `/webhook/{path}` | `followup-{slug}.json` |')
open('n8n/followups/README.md', 'w').write('\n'.join(md) + '\n')
print(len(rows), 'email-series workflows written to n8n/followups/')
