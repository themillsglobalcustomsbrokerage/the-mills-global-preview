#!/usr/bin/env python3
"""Writes docs/EMAIL-SEQUENCES.md: the plain-text copy of all 81 emails (27 segments x 3), built from each page's own copy
plus a hand-written self-check question and 'what to send us' line per segment."""
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
g = {'__file__': os.path.abspath('tools/build-n8n-lead-magnet.py')}
exec(compile(open('tools/build-n8n-lead-magnet.py').read().split("KINDS = [")[0] + "\n" + open('tools/build-n8n-lead-magnet.py').read().split("def page_facts")[1].join(["def page_facts", ""]) if False else open('tools/build-n8n-lead-magnet.py').read().split("# ------------------------------------------------------------------ capture workflow")[0], 'gen', 'exec'), g)
SERVICES, INDUSTRIES, TOPICS, G, page_facts = g['SERVICES'], g['INDUSTRIES'], g['TOPICS'], g['G'], g['page_facts']

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath('tools/build-email-copy-doc.py')))
from email_copy_data import COPY, SCENE
import json as _json
VARIANTS = _json.load(open('tools/email_variants.json'))
assert set(COPY) == set(SERVICES) | set(INDUSTRIES), set(SERVICES) ^ set(COPY)


assert set(SCENE) == set(COPY)

SAMPLE = {'first_name': 'Maria', 'first_name_lc': 'maria', 'company': 'Acme Trading Corp'}
words = lambda s: len(re.findall(r"\S+", s))


def fill(t, short='', topic='', lead='', tail='', co='{{company}}'):
    return t.replace('{lead}', lead).replace('{tail}', tail).replace('{short}', short).replace('{topic}', topic).replace('{co}', co)


def emails(slug, name, key, idx):
    f = page_facts(slug, key)
    st = f['stuck']
    check, send = COPY[slug]
    topic = TOPICS[slug]
    short = name.replace('Mills ', '').lower()
    scene = SCENE[slug][0].upper() + SCENE[slug][1:]
    lead, tail = '{{first_name_lc}}, ', ', {{first_name_lc}}'
    v1, v2 = VARIANTS['e1'][idx % len(VARIANTS['e1'])], VARIANTS['e2'][idx % len(VARIANTS['e2'])]
    v3, t2 = VARIANTS['e3'][idx % len(VARIANTS['e3'])], VARIANTS['e2tail'][idx % len(VARIANTS['e2tail'])]
    F = lambda t: fill(t, short, topic, lead, tail)
    e1 = (f"Subject: {F(v1['subject'])}\nPreview text: {F(v1['pre'])}\n\n"
          f"Hi {{{{first_name}}}},\n\n{scene}... sound familiar?\n\n{v1['line']}\n\n[Download the checklist]\n\n"
          f"Three things to check first:\n\n" + '\n'.join(f"{i + 1}. {x['t']}" for i, x in enumerate(st)) +
          f"\n\nSkim it with your own shipment in mind. If something looks off, hit reply and send me {send}. I will tell you what I would check first.\n\n"
          f"{{{{sender_name}}}}\nThe Mills Global")
    e2 = (f"Subject: {F(v2['subject'])}\nPreview text: {F(v2['pre'])}\n\n"
          f"Hi {{{{first_name}}}},\n\n{v2['open']}\n\n{check}\n\n{F(t2)}\n\n"
          f"Here is why it matters: {st[0]['d']}\n\nNot sure about {{{{company}}}}? Reply with {send} and I will tell you where I would look first.\n\n"
          f"{{{{sender_name}}}}\nThe Mills Global")
    e3 = (f"Subject: {F(v3['subject'])}\nPreview text: {F(v3['pre'])}\n\n"
          f"Hi {{{{first_name}}}},\n\n{v3['open']}\n\n"
          f"Here is the thing about {topic}... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.\n\n"
          f"If {{{{company}}}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:\n\n[Book a time]\n\n"
          f"And if now is not the time, totally fine. The checklist is yours to keep.\n\n"
          f"{{{{sender_name}}}}\nThe Mills Global\n\nP.S. Wrong person? Just tell me who handles this and I will take it from there.")
    return [e1, e2, e3], f


def body_words(e):
    body = e.split('\n\n', 2)[2]
    return words(body)


def subj(e):
    s = e.split('\n')[0][len('Subject: '):]
    return len(s.replace('{{first_name_lc}}', SAMPLE['first_name_lc']).replace('{{first_name}}', SAMPLE['first_name']).replace('{{company}}', SAMPLE['company']))


md = []
md.append("""# Email sequences: all 27 services and industries

Plain-text copy for the 81 emails (27 segments x 3). Merge fields use `{{double braces}}`. Each segment's wording is built from that page's own approved copy (its "where clients usually get stuck" points), so it stays consistent with the website.

## How these were written (best practices applied)

Principles drawn from four sources: [Success Knocks](https://successknocks.com/b2b-follow-up-email-templates/), [Artemis Leads](https://www.artemisleads.com/resources-outbound-lead-generation/ultimate-guide-to-follow-up-email-sequences-for-b2b), [Peer to Peer Marketing](https://peertopeermarketing.co/b2b-email-marketing-best-practices/) and [MailerLite](https://www.mailerlite.com/blog/b2b-email-marketing-examples). Several of their statistics are unsourced and MailerLite is a vendor, so the rules below are the practices they agree on, not their numbers.

| Principle | How it shows up here |
|---|---|
| Keep it to 3 or 4 touches; more raises unsubscribes and spam complaints | 3 emails per series |
| Space follow-ups 2 to 3 days apart, then a longer gap; give the reader a day or two after a download | Day 0, day 3, day 7 |
| Every email adds something new, never "just checking in" | E1 delivers and sets up, E2 gives one self-check question, E3 gives a time-and-cost angle and closes |
| One clear call to action per email, easy to say yes to | E1 download, E2 reply with one specific thing, E3 book a time |
| Short, skimmable, mobile friendly | roughly 75 to 100 words each (counts below), one idea per paragraph, single column |
| Personalize beyond the first name: company, industry, the problem | The first name in every email; the company name in Emails 2 and 3 only, so it never feels like a mail merge; the segment's own scenario and pain point throughout |
| Short, specific subject lines (about 40 characters so they show on mobile) | about 25 to 50 characters; lowercase and personal, like a note from a colleague; no "free", no exclamation marks |
| Align preview text with the subject | Every email has preview text |
| Breakup email with easy exits ("wrong person", "wrong timing") | E3 and its P.S. |
| Lead with value and education, a conversational but professional tone | Casual, expert voice: it opens with a scene the reader recognises, then shows we know where it goes wrong; the sale is a low-pressure offer |
| Segment by industry and lead source | A separate series per service and industry |
| Permission-based, with an unsubscribe route | Footer line: reply "stop"; honor opt-outs in Zoho |

## Voice and formatting

- **Sounds like a person who has seen this before.** Each series opens with a relatable scene from that segment ("the invoice says one thing, the permit says another..."), asks a question the reader can answer in their head, then shows the expert answer. That is what keeps people reading and gives them a reason to reply.
- **Casual on purpose.** Short sentences, ellipses for a beat of curiosity, "um... probably?", "promise", "no pitch deck, no pressure". Lowercase subject lines and preview text look like a colleague's message, not a campaign.
- **Name always, company sometimes.** The first name is in every subject, greeting and sign-off context; the company appears in Emails 2 and 3 where it reads naturally.
- **No real small caps or special characters.** Unicode "small caps" letters are read out as gibberish by screen readers and can trip spam filters, so lowercase gives the same casual look safely.
- **Honest claims only.** No statistics, no invented client results, no urgency that is not real. The only facts are the checklist itself and each page's own "where clients usually get stuck" points.

**Rotated wording.** To stop every series sounding the same, the subject lines, preview text, opening lines and one connecting sentence rotate through a set of variants (8 for Email 1, 10 for Email 2, 6 for Email 3), assigned so neighbouring segments never match. The variant set lives in `tools/email_variants.json`; add or edit variants there. Each variant is still written to the rules above.

## Sequence blueprint

| Email | Send | Job | Single CTA |
|---|---|---|---|
| 1 | Immediately | Deliver the checklist, name the three pitfalls, make a human offer | Download the checklist |
| 2 | Day 3 | One self-check question tied to the biggest pitfall, and why it matters | Reply with one specific item |
| 3 | Day 7 | Different angle (cost of finding out late), clear close, easy exits | Book a time |

Send Tuesday to Thursday, mornings in Manila time where the tool allows. The series stops automatically when the lead's status is no longer "Not Contacted" or they opt out.

## Merge fields

`{{first_name}}` and `{{company}}` come from the form (fall back to "there" and "your team" if blank). `{{first_name_lc}}` is the first name in lowercase, for the lowercase subject lines. `{{sender_name}}` is **Ari or Joshua**, picked per lead (from the lead's email address, so the same person signs all three emails). Replies to a named person perform better than to a team address, and the Gmail sender name reads "Ari from The Mills Global" or "Joshua from The Mills Global". Links: `[Download the checklist]` is the segment's Google Drive download link (all 27 are listed in docs/AUTOMATION-HANDOFF.md); `[Book a time]` is `https://themillsglobal.com/book-a-call.html`.

## Design

The HTML shell (brand colors with accessible contrast, dark-mode safe, single column) is in `tools/email-builder.js`. Its built-in wording is an earlier draft and is superseded by the copy below; drop this copy into the shell. Navy `#212431` text and buttons on white, slate `#4F5D75` for secondary text, orange `#EA5C1F` only as decoration (it fails the contrast minimum for text).

---
""")
idx = 0
for kind, names in (('service', SERVICES), ('industry', INDUSTRIES)):
    md.append(f"\n# {'Services' if kind == 'service' else 'Industries'}\n")
    for slug, name in names.items():
        es, f = emails(slug, name, kind, idx); idx += 1
        md.append(f"\n## {name}\n\n`{slug}` | topic: {TOPICS[slug]} | checklist: {G[slug]['title']}\n")
        labels = ['Email 1: Day 0, deliver the checklist', 'Email 2: Day 3, a quick check', 'Email 3: Day 7, closing the loop']
        for lab, e in zip(labels, es):
            md.append(f"\n### {lab}\n\n*Subject length: {subj(e)} characters (sample names) | Body: {body_words(e)} words*\n\n```\n{e}\n```\n")
        md.append("\n---\n")
open('docs/EMAIL-SEQUENCES.md', 'w').write(''.join(md))
print('written')
