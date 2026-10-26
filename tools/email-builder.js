// ---- Email builder: Mills brand palette, WCAG AA contrast, dark-mode safe ----
// Brand: navy #212431, slate #4F5D75, paper #F5F5F5, orange #EA5C1F (decoration only: it fails AA for text on white/paper).
// Text: navy on white 15.4:1, slate on white 6.7:1. Button: white on navy 15.4:1. Dark mode: paper on navy 14.2:1.
// The header band is already navy with a white logo, so it survives Gmail/Outlook inversion unchanged.
const NAVY = '#212431', SLATE = '#4F5D75', PAPER = '#F5F5F5', ORANGE = '#EA5C1F';
const FONT = "Arial, Helvetica, sans-serif";
const LOGO = SITE + 'assets/images/brand/mills-logo-horizontal-white.png';
const hasCo = !!out.company, hasFirst = !!out.first_name;
const first = out.first_name_greeting || 'there';
const firstLc = first.toLowerCase();
const T = out.topic;
const co = esc(out.company || 'your team');
const lead = hasFirst ? firstLc + ', ' : '';   // subject lines read like a note from a colleague
// VARIANTS (subject, preview and opener wording) is injected by the generator from tools/email_variants.json

const h = (t) => '<h1 style="margin:0 0 16px 0;font-family:' + FONT + ';font-size:24px;line-height:1.3;font-weight:700;color:' + NAVY + ';" class="dm-text">' + t + '</h1>';
const p = (t) => '<p style="margin:0 0 16px 0;font-family:' + FONT + ';font-size:16px;line-height:1.6;color:' + NAVY + ';" class="dm-text">' + t + '</p>';
const link = (href, label) => '<a href="' + href + '" style="color:' + NAVY + ';text-decoration:underline;font-weight:700;" class="dm-link">' + label + '</a>';
const btn = (href, label) =>
  '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:8px 0 24px 0;"><tr>' +
  '<td align="center" bgcolor="' + NAVY + '" class="dm-btn" style="background-color:' + NAVY + ';border-radius:999px;border:2px solid ' + NAVY + ';">' +
  '<a href="' + href + '" class="dm-btn-link" style="display:inline-block;padding:14px 28px;font-family:' + FONT + ';font-size:16px;line-height:1.2;font-weight:700;color:#FFFFFF;text-decoration:none;border-radius:999px;">' + label + '</a>' +
  '</td></tr></table>';
const bullets = (items) => '<ul style="margin:0 0 16px 0;padding:0 0 0 22px;font-family:' + FONT + ';font-size:16px;line-height:1.6;color:' + NAVY + ';" class="dm-text">' +
  items.map((s) => '<li style="margin:0 0 6px 0;">' + esc(s.t) + '</li>').join('') + '</ul>';
const stuckBlocks = (items) => items.map((s) =>
  '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 14px 0;"><tr>' +
  '<td width="4" bgcolor="' + ORANGE + '" style="background-color:' + ORANGE + ';font-size:0;line-height:0;">&nbsp;</td>' +
  '<td style="padding:2px 0 2px 14px;font-family:' + FONT + ';">' +
  '<div style="font-size:16px;line-height:1.4;font-weight:700;color:' + NAVY + ';" class="dm-text">' + esc(s.t) + '</div>' +
  '<div style="font-size:15px;line-height:1.55;color:' + SLATE + ';" class="dm-muted">' + esc(s.d) + '</div>' +
  '</td></tr></table>').join('');
const sign = p('Talk soon,<br><strong>The Mills Global team</strong><br><span style="color:' + SLATE + ';" class="dm-muted">inquiry@themillsglobal.com &middot; +63 917 712 9000</span>');

function shell(preheader, inner) {
  return '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark"><title>The Mills Global</title>' +
    '<style>:root{color-scheme:light dark;supported-color-schemes:light dark;}' +
    '@media (prefers-color-scheme: dark){.dm-page{background-color:#181A24 !important;}.dm-card{background-color:#212431 !important;}.dm-text{color:#F5F5F5 !important;}.dm-muted{color:#D6D7D7 !important;}' +
    '.dm-link{color:#F5F5F5 !important;}.dm-btn{background-color:#F5F5F5 !important;border-color:#F5F5F5 !important;}.dm-btn-link{color:#212431 !important;}}' +
    '[data-ogsc] .dm-text{color:#F5F5F5 !important;}[data-ogsc] .dm-muted{color:#D6D7D7 !important;}[data-ogsc] .dm-link{color:#F5F5F5 !important;}' +
    '[data-ogsb] .dm-card{background-color:#212431 !important;}[data-ogsb] .dm-page{background-color:#181A24 !important;}' +
    '@media (max-width:620px){.wrap{width:100% !important;}.pad{padding:24px 20px !important;}}</style></head>' +
    '<body style="margin:0;padding:0;background-color:' + PAPER + ';" class="dm-page" bgcolor="' + PAPER + '">' +
    '<div style="display:none;max-height:0;overflow:hidden;opacity:0;font-size:1px;line-height:1px;color:' + PAPER + ';">' + esc(preheader) + '&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="' + PAPER + '" class="dm-page" style="background-color:' + PAPER + ';"><tr><td align="center" style="padding:24px 12px;">' +
    '<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;">' +
    '<tr><td bgcolor="' + NAVY + '" style="background-color:' + NAVY + ';padding:22px 32px;border-radius:16px 16px 0 0;">' +
    '<img src="' + LOGO + '" alt="The Mills Global" width="150" style="display:block;border:0;height:auto;color:#FFFFFF;font-family:' + FONT + ';font-size:18px;font-weight:700;">' +
    '<div style="width:150px;margin:7px 0 0 0;font-family:' + FONT + ';font-size:9px;line-height:9px;letter-spacing:2.1px;white-space:nowrap;color:#F5F5F5;text-transform:uppercase;">Trade without limits<sup style="font-size:6px;line-height:0;letter-spacing:0;vertical-align:baseline;position:relative;top:-3px;">&reg;</sup></div></td></tr>' +
    '<tr><td bgcolor="' + ORANGE + '" style="background-color:' + ORANGE + ';height:4px;font-size:0;line-height:0;">&nbsp;</td></tr>' +
    '<tr><td class="pad dm-card" bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:32px;">' + inner + '</td></tr>' +
    '<tr><td class="pad dm-card" bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:0 32px 28px 32px;border-radius:0 0 16px 16px;">' +
    '<p style="margin:0;border-top:1px solid #D6D7D7;padding-top:16px;font-family:' + FONT + ';font-size:13px;line-height:1.6;color:' + SLATE + ';" class="dm-muted">' +
    'You are getting this because you asked for the ' + esc(out.guide_title) + '. Not useful? Reply &ldquo;stop&rdquo; and we will stop the follow-ups. ' +
    '<a href="' + SITE + 'legal-privacy-policy.html" style="color:' + SLATE + ';text-decoration:underline;" class="dm-muted">Privacy policy</a><br>' +
    'The Mills Global &middot; Level 24 Philippine Stock Exchange Tower, 5th Ave. cor. 28th St., BGC, Taguig City</p>' +
    '</td></tr></table></td></tr></table></body></html>';
}

const numbered = (items) => '<ol style="margin:0 0 16px 0;padding:0 0 0 22px;font-family:' + FONT + ';font-size:16px;line-height:1.6;color:' + NAVY + ';" class="dm-text">' +
  items.map((s) => '<li style="margin:0 0 6px 0;">' + esc(s.t) + '</li>').join('') + '</ol>';
const cap = (t) => t.charAt(0).toUpperCase() + t.slice(1);
const sign2 = p('<span style="display:block;">' + esc(out.sender_name || 'The Mills Global team') + '</span><span style="color:' + SLATE + ';" class="dm-muted">The Mills Global</span>');

const fillv = (t, co2) => t.replace('{lead}', lead).replace('{tail}', hasFirst ? ', ' + firstLc : '').replace('{short}', out.short).replace('{topic}', T).replace('{co}', co2);
const V1 = VARIANTS.e1[out.v % VARIANTS.e1.length], V2 = VARIANTS.e2[out.v % VARIANTS.e2.length];
const V3 = VARIANTS.e3[out.v % VARIANTS.e3.length], T2 = VARIANTS.e2tail[out.v % VARIANTS.e2tail.length];
const coPlain = out.company || 'your team';

const EMAILS = {
  1: {
    subject: fillv(V1.subject, coPlain),
    pre: fillv(V1.pre, coPlain),
    body: p('Hi ' + esc(first) + ',') +
      p(esc(cap(out.scene)) + '... sound familiar?') +
      p(esc(V1.line)) +
      btn(out.pdf_url, 'Download the checklist') +
      p('Three things to check first:') + numbered(out.stuck) +
      p('Skim it with your own shipment in mind. If something looks off, hit reply and send me ' + esc(out.send) + '. I will tell you what I would check first.') + sign2
  },
  2: {
    subject: fillv(V2.subject, coPlain),
    pre: fillv(V2.pre, coPlain),
    body: p('Hi ' + esc(first) + ',') + p(esc(V2.open)) +
      '<p style="margin:0 0 16px 0;font-family:' + FONT + ';font-size:18px;line-height:1.5;font-weight:700;color:' + NAVY + ';" class="dm-text">' + esc(out.check) + '</p>' +
      p(esc(fillv(T2, coPlain))) +
      p('<strong>Here is why it matters:</strong> ' + esc(out.stuck[0].d)) +
      p('Not sure about ' + co + '? Reply with ' + esc(out.send) + ' and I will tell you where I would look first.') + sign2
  },
  3: {
    subject: fillv(V3.subject, coPlain),
    pre: fillv(V3.pre, coPlain),
    body: p('Hi ' + esc(first) + ',') +
      p(esc(V3.open)) +
      p('Here is the thing about ' + esc(T) + '... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.') +
      p('If ' + co + ' has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:') +
      btn(out.book_url, 'Book a time') +
      p('And if now is not the time, totally fine. The checklist is yours to keep.') + sign2 +
      '<p style="margin:0 0 8px 0;font-family:' + FONT + ';font-size:15px;line-height:1.55;color:' + SLATE + ';" class="dm-muted"><strong>P.S.</strong> Wrong person? Just tell me who handles this and I will take it from there.</p>'
  }
};
for (const n of [1, 2, 3]) {
  out['subject' + n] = EMAILS[n].subject;
  out['html' + n] = shell(EMAILS[n].pre, EMAILS[n].body);
}
return [{ json: out }];
