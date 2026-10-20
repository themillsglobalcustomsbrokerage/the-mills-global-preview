# Email sequences: all 27 services and industries

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

# Services

## Mills Entry

`entry` | topic: Philippine market entry | checklist: Philippine Market Entry Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 29 characters (sample names) | Body: 96 words*

```
Subject: {{first_name_lc}}, your checklist is here
Preview text: ready when you are... plus 3 things to check first

Hi {{first_name}},

Buying stock before the company setup is even sorted... sound familiar?

That is exactly what this checklist is for. Here it is:

[Download the checklist]

Three things to check first:

1. Buying before the structure is ready
2. Registration steps in the wrong order
3. A first shipment that becomes a test

Skim it with your own shipment in mind. If something looks off, hit reply and send me the product you plan to bring in and where you plan to sell it. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 34 characters (sample names) | Body: 97 words*

```
Subject: {{first_name_lc}}, honest question about entry
Preview text: a 10 second gut check for {{company}}...

Hi {{first_name}},

Honest question...

Is your company structure settled, and are your registrations in the right order, before the first purchase order goes out?

If your honest answer is "um... probably?", that is the part of Philippine market entry where things tend to go sideways.

Here is why it matters: Companies order stock before deciding who the importer of record is or which registrations apply.

Not sure about {{company}}? Reply with the product you plan to bring in and where you plan to sell it and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 23 characters (sample names) | Body: 97 words*

```
Subject: last one from me, {{first_name_lc}}
Preview text: no hard feelings either way...

Hi {{first_name}},

I will stop filling your inbox after this one, promise.

Here is the thing about Philippine market entry... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mills Permits

`permits` | topic: import permits | checklist: Import Permit and Product Registration Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 29 characters (sample names) | Body: 89 words*

```
Subject: here is that checklist, {{first_name_lc}}
Preview text: inside: 3 spots worth a look first

Hi {{first_name}},

Finding out which agency you needed after the cargo is already booked... sound familiar?

So we put together a checklist for exactly that. Here you go:

[Download the checklist]

Three things to check first:

1. Not knowing which agency applies
2. Approvals that arrive too late
3. Approvals that do not match the shipment

Skim it with your own shipment in mind. If something looks off, hit reply and send me the product name and description. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 31 characters (sample names) | Body: 87 words*

```
Subject: can i ask you something, {{first_name_lc}}?
Preview text: it is about permits, and it is a short one

Hi {{first_name}},

Can I ask you something?

Do you know which agency approves your product, and does that approval describe the goods exactly as they will be shipped?

If you had to think about it, that is usually where import permits starts to wobble.

Here is why it matters: The same product can touch several regulators, and its commercial name rarely tells you which.

Not sure about {{company}}? Reply with the product name and description and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 23 characters (sample names) | Body: 92 words*

```
Subject: {{first_name_lc}}, closing the loop
Preview text: one last note, and an easy way to say not now

Hi {{first_name}},

Last note from me, I promise.

Here is the thing about import permits... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mills Customs

`customs` | topic: customs clearance | checklist: Customs Clearance Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 29 characters (sample names) | Body: 89 words*

```
Subject: {{first_name_lc}}, your customs checklist
Preview text: grab it now, skim it later...

Hi {{first_name}},

The invoice says one thing, the permit says another, and nobody notices until customs does... sound familiar?

Good news, we built a checklist for it. It is yours:

[Download the checklist]

Three things to check first:

1. Paperwork that does not match
2. Classification and valuation doubts
3. Holds with no clear owner

Skim it with your own shipment in mind. If something looks off, hit reply and send me a draft invoice and packing list. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 27 characters (sample names) | Body: 84 words*

```
Subject: {{first_name_lc}}, gut check on customs
Preview text: answer in your head, no need to reply yet...

Hi {{first_name}},

Gut check time...

Do your invoice, packing list and permits all describe the goods in exactly the same way?

A "hmm, not sure" is common here. It is also where customs clearance tends to get stuck.

Here is why it matters: Invoices, packing lists and permits that disagree with each other are a common reason cargo is queried.

Not sure about {{company}}? Reply with a draft invoice and packing list and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 32 characters (sample names) | Body: 103 words*

```
Subject: should i close your file, {{first_name_lc}}?
Preview text: no pressure either way...

Hi {{first_name}},

I do not want to be the person who keeps emailing, so this is the last one.

Here is the thing about customs clearance... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mills Marine

`marine` | topic: vessel and marine equipment | checklist: Vessel and Marine Equipment Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 23 characters (sample names) | Body: 81 words*

```
Subject: checklist inside, {{first_name_lc}}
Preview text: short read, three things to check first

Hi {{first_name}},

A vessel part that needs three different agencies to say yes... sound familiar?

Here is the checklist you asked for:

[Download the checklist]

Three things to check first:

1. Vessel and equipment rules across agencies
2. Spares needed fast
3. Imported assets with no clear path

Skim it with your own shipment in mind. If something looks off, hit reply and send me the vessel or equipment details. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 29 characters (sample names) | Body: 95 words*

```
Subject: one thing about marine, {{first_name_lc}}
Preview text: the part that is easy to skip...

Hi {{first_name}},

Here is the one I always start with...

Is it clear which agencies are involved for the vessel or equipment before it is bought or shipped?

If your honest answer is "um... probably?", that is the part of vessel and marine equipment where things tend to go sideways.

Here is why it matters: Customs, Maritime Industry Authority (MARINA), port and registration requirements all apply, and each has its own paperwork.

Not sure about {{company}}? Reply with the vessel or equipment details and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 18 characters (sample names) | Body: 97 words*

```
Subject: no pressure, {{first_name_lc}}
Preview text: one last thing, then I will leave you alone...

Hi {{first_name}},

One last thing, then I will leave you alone.

Here is the thing about vessel and marine equipment... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mills Dangerous Goods

`dangerous-goods` | topic: dangerous goods shipping | checklist: Dangerous Goods Shipping Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 26 characters (sample names) | Body: 85 words*

```
Subject: {{first_name_lc}}, this one is for you
Preview text: your checklist, plus three things to check first...

Hi {{first_name}},

Cargo booked as ordinary freight that turns out to be dangerous goods... sound familiar?

If that rings a bell, this is for you:

[Download the checklist]

Three things to check first:

1. Regulated cargo booked as ordinary cargo
2. Refusal at the last minute
3. Rules held by different bodies

Skim it with your own shipment in mind. If something looks off, hit reply and send me the product's safety data sheet. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 31 characters (sample names) | Body: 81 words*

```
Subject: {{first_name_lc}}, before you ship anything
Preview text: a 10 second check for {{company}}...

Hi {{first_name}},

Before anything ships...

Has the cargo been identified as dangerous goods before it was booked with the carrier?

If you had to think about it, that is usually where dangerous goods shipping starts to wobble.

Here is why it matters: Products with batteries, solvents or compressed gas are often shipped without being identified as dangerous goods.

Not sure about {{company}}? Reply with the product's safety data sheet and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 22 characters (sample names) | Body: 96 words*

```
Subject: {{first_name_lc}}, parting thought
Preview text: one more thing, then I am out of your inbox...

Hi {{first_name}},

Parting thought, then I am out of your inbox.

Here is the thing about dangerous goods shipping... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mills Logistics

`logistics` | topic: post-clearance delivery | checklist: Post-Clearance Delivery Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 33 characters (sample names) | Body: 86 words*

```
Subject: {{first_name_lc}}, as promised, the checklist
Preview text: no fluff, just the list...

Hi {{first_name}},

Customs releases the cargo, and then nothing, because nobody owns the last mile... sound familiar?

As promised, here it is:

[Download the checklist]

Three things to check first:

1. A gap between release and delivery
2. Handling conditions lost on the way
3. No proof when something goes wrong

Skim it with your own shipment in mind. If something looks off, hit reply and send me the delivery address and any handling requirements. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 26 characters (sample names) | Body: 77 words*

```
Subject: did you check this, {{first_name_lc}}?
Preview text: one for {{company}}, and you can answer in your head...

Hi {{first_name}},

Okay, here goes...

Is one named person responsible between customs release and the consignee's door?

A "hmm, not sure" is common here. It is also where post-clearance delivery tends to get stuck.

Here is why it matters: Cargo is cleared but nobody owns the trucking, storage and receiving that follow.

Not sure about {{company}}? Reply with the delivery address and any handling requirements and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 19 characters (sample names) | Body: 95 words*

```
Subject: {{first_name_lc}}, door is open
Preview text: no hard feelings, either way...

Hi {{first_name}},

I will leave the door open and stop here.

Here is the thing about post-clearance delivery... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mills Packaging

`packaging` | topic: export packaging | checklist: Export and Industrial Packaging Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 27 characters (sample names) | Body: 74 words*

```
Subject: {{first_name_lc}}, checklist, delivered
Preview text: fresh off the press, three things to check first

Hi {{first_name}},

Packing picked after the quote, then the crate shows up damaged... sound familiar?

Delivered, as promised:

[Download the checklist]

Three things to check first:

1. Packing chosen after the quote
2. Damage in transit
3. Packing rules missed

Skim it with your own shipment in mind. If something looks off, hit reply and send me the cargo dimensions, weight and destination. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 29 characters (sample names) | Body: 87 words*

```
Subject: {{first_name_lc}}, is this on your radar?
Preview text: about packaging, and worth a minute...

Hi {{first_name}},

Something I always ask first...

Was the packing specified for this cargo and this route, or chosen after the quote?

If your honest answer is "um... probably?", that is the part of export packaging where things tend to go sideways.

Here is why it matters: Crating is treated as an afterthought, then falls short on weight, lifting points or route conditions.

Not sure about {{company}}? Reply with the cargo dimensions, weight and destination and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 23 characters (sample names) | Body: 96 words*

```
Subject: last one from me, {{first_name_lc}}
Preview text: no hard feelings either way...

Hi {{first_name}},

I will stop filling your inbox after this one, promise.

Here is the thing about export packaging... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mills Insurance

`insurance` | topic: cargo insurance | checklist: Marine Cargo Insurance Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 17 characters (sample names) | Body: 82 words*

```
Subject: {{first_name_lc}}, start here
Preview text: the checklist, plus where to look first...

Hi {{first_name}},

Assuming the carrier's liability has you covered, right up until you need to claim... sound familiar?

Start with this:

[Download the checklist]

Three things to check first:

1. Assuming the carrier's liability is enough
2. Policies that do not fit the shipment
3. Claims without the paperwork

Skim it with your own shipment in mind. If something looks off, hit reply and send me the cargo value and route. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 24 characters (sample names) | Body: 83 words*

```
Subject: {{first_name_lc}}, spot the problem?
Preview text: see if you can spot it before we do...

Hi {{first_name}},

Let me ask you this...

If the cargo were damaged, would the carrier's liability cover its value, and would you have the paperwork to claim?

If you had to think about it, that is usually where cargo insurance starts to wobble.

Here is why it matters: Standard carrier limits rarely match the value of the cargo being moved.

Not sure about {{company}}? Reply with the cargo value and route and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 23 characters (sample names) | Body: 92 words*

```
Subject: {{first_name_lc}}, closing the loop
Preview text: one last note, and an easy way to say not now

Hi {{first_name}},

Last note from me, I promise.

Here is the thing about cargo insurance... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mills Time Critical

`time-critical` | topic: time-critical cargo | checklist: Priority Clearance Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 29 characters (sample names) | Body: 91 words*

```
Subject: {{first_name_lc}}, your checklist is here
Preview text: ready when you are... plus 3 things to check first

Hi {{first_name}},

Cargo that needs to move now, stuck behind one missing document... sound familiar?

That is exactly what this checklist is for. Here it is:

[Download the checklist]

Three things to check first:

1. Cargo stalled on a missing document
2. No clear owner in an emergency
3. Ordinary processes for urgent cargo

Skim it with your own shipment in mind. If something looks off, hit reply and send me what is moving and the date you need it. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 36 characters (sample names) | Body: 86 words*

```
Subject: {{first_name_lc}}, real talk about time critical
Preview text: no fluff, just one question...

Hi {{first_name}},

Real talk...

If this cargo had to move this week, would you know exactly which document could hold it up?

A "hmm, not sure" is common here. It is also where time-critical cargo tends to get stuck.

Here is why it matters: A single missing paper can turn hours into days when the clock is already running.

Not sure about {{company}}? Reply with what is moving and the date you need it and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 32 characters (sample names) | Body: 103 words*

```
Subject: should i close your file, {{first_name_lc}}?
Preview text: no pressure either way...

Hi {{first_name}},

I do not want to be the person who keeps emailing, so this is the last one.

Here is the thing about time-critical cargo... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mills Advisory

`advisory` | topic: Philippine trade compliance | checklist: Philippine Trade Regulation Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 29 characters (sample names) | Body: 92 words*

```
Subject: here is that checklist, {{first_name_lc}}
Preview text: inside: 3 spots worth a look first

Hi {{first_name}},

Making big decisions before anyone has mapped the rules behind them... sound familiar?

So we put together a checklist for exactly that. Here you go:

[Download the checklist]

Three things to check first:

1. Unclear starting point
2. Decisions made before the rules are mapped
3. Exposure found too late

Skim it with your own shipment in mind. If something looks off, hit reply and send me a short description of the plan or the decision on the table. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 22 characters (sample names) | Body: 101 words*

```
Subject: {{first_name_lc}}, sound familiar?
Preview text: think about your last shipment...

Hi {{first_name}},

Think about your last shipment for a second...

Which decisions have you already made that depend on rules you have not yet mapped?

If your honest answer is "um... probably?", that is the part of Philippine trade compliance where things tend to go sideways.

Here is why it matters: Management knows a transaction needs regulatory clearance but not which agencies apply, in what order, or how customs fits in.

Not sure about {{company}}? Reply with a short description of the plan or the decision on the table and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 18 characters (sample names) | Body: 96 words*

```
Subject: no pressure, {{first_name_lc}}
Preview text: one last thing, then I will leave you alone...

Hi {{first_name}},

One last thing, then I will leave you alone.

Here is the thing about Philippine trade compliance... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mills Projects

`projects` | topic: project cargo | checklist: Project Cargo Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 30 characters (sample names) | Body: 92 words*

```
Subject: {{first_name_lc}}, your projects checklist
Preview text: grab it now, skim it later...

Hi {{first_name}},

One missing requirement and the whole project schedule slips... sound familiar?

Good news, we built a checklist for it. It is yours:

[Download the checklist]

Three things to check first:

1. One missed requirement stops the schedule
2. Cargo that does not fit the route
3. Many parties, no single plan

Skim it with your own shipment in mind. If something looks off, hit reply and send me the equipment list and the date it is needed on site. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 37 characters (sample names) | Body: 87 words*

```
Subject: {{first_name_lc}}, honest question about projects
Preview text: a 10 second gut check for {{company}}...

Hi {{first_name}},

Honest question...

Has someone confirmed that every piece of the cargo can actually travel the planned route, from port to site?

If you had to think about it, that is usually where project cargo starts to wobble.

Here is why it matters: A permit, route restriction or lifting limit discovered late can delay an entire project.

Not sure about {{company}}? Reply with the equipment list and the date it is needed on site and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 22 characters (sample names) | Body: 95 words*

```
Subject: {{first_name_lc}}, parting thought
Preview text: one more thing, then I am out of your inbox...

Hi {{first_name}},

Parting thought, then I am out of your inbox.

Here is the thing about project cargo... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

# Industries

## Construction

`industry-construction` | topic: construction equipment imports | checklist: Construction and Infrastructure Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 23 characters (sample names) | Body: 83 words*

```
Subject: checklist inside, {{first_name_lc}}
Preview text: short read, three things to check first

Hi {{first_name}},

A machine that is too big for the route, or too used for the rules... sound familiar?

Here is the checklist you asked for:

[Download the checklist]

Three things to check first:

1. Machinery and Used-Equipment rules
2. Oversized pieces
3. Project schedules that cannot slip

Skim it with your own shipment in mind. If something looks off, hit reply and send me the equipment list and the site schedule. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 31 characters (sample names) | Body: 96 words*

```
Subject: can i ask you something, {{first_name_lc}}?
Preview text: it is about construction, and it is a short one

Hi {{first_name}},

Can I ask you something?

Is any of the machinery used, and does any piece exceed what the planned route can handle?

A "hmm, not sure" is common here. It is also where construction equipment imports tends to get stuck.

Here is why it matters: Rules and permits differ for new and used equipment. We check eligibility before you commit, so you do not buy machinery you cannot import.

Not sure about {{company}}? Reply with the equipment list and the site schedule and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 19 characters (sample names) | Body: 96 words*

```
Subject: {{first_name_lc}}, door is open
Preview text: no hard feelings, either way...

Hi {{first_name}},

I will leave the door open and stop here.

Here is the thing about construction equipment imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Renewable Energy

`industry-renewable-energy` | topic: renewable energy equipment imports | checklist: Renewable Energy and Power Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 26 characters (sample names) | Body: 81 words*

```
Subject: {{first_name_lc}}, this one is for you
Preview text: your checklist, plus three things to check first...

Hi {{first_name}},

Solar and storage gear on a project clock, waiting on approvals... sound familiar?

If that rings a bell, this is for you:

[Download the checklist]

Three things to check first:

1. Incentives and approvals
2. Batteries and large components
3. Project delivery windows

Skim it with your own shipment in mind. If something looks off, hit reply and send me the equipment list and the project delivery window. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 36 characters (sample names) | Body: 98 words*

```
Subject: {{first_name_lc}}, gut check on renewable energy
Preview text: answer in your head, no need to reply yet...

Hi {{first_name}},

Gut check time...

Are the incentive approvals secured before the equipment arrives, and are batteries and large components planned for?

If your honest answer is "um... probably?", that is the part of renewable energy equipment imports where things tend to go sideways.

Here is why it matters: Incentive treatment depends on documents prepared before arrival. We get them in place early, so the benefit is applied when the cargo clears.

Not sure about {{company}}? Reply with the equipment list and the project delivery window and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 23 characters (sample names) | Body: 98 words*

```
Subject: last one from me, {{first_name_lc}}
Preview text: no hard feelings either way...

Hi {{first_name}},

I will stop filling your inbox after this one, promise.

Here is the thing about renewable energy equipment imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Data Centers

`industry-data-centers` | topic: data center equipment imports | checklist: Data Centers and Digital Infrastructure Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 33 characters (sample names) | Body: 79 words*

```
Subject: {{first_name_lc}}, as promised, the checklist
Preview text: no fluff, just the list...

Hi {{first_name}},

Servers, cooling, batteries and power gear in one project, each clearing differently... sound familiar?

As promised, here it is:

[Download the checklist]

Three things to check first:

1. Many categories in one project
2. Batteries and dangerous goods
3. Fit-Out dates

Skim it with your own shipment in mind. If something looks off, hit reply and send me the bill of materials and the fit-out date. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 35 characters (sample names) | Body: 103 words*

```
Subject: one thing about data centers, {{first_name_lc}}
Preview text: the part that is easy to skip...

Hi {{first_name}},

Here is the one I always start with...

Have the categories in the project (servers, cooling, power, batteries) been separated by what each one needs to clear?

If you had to think about it, that is usually where data center equipment imports starts to wobble.

Here is why it matters: Servers, batteries, generators and cooling each follow different rules. We separate and clear each category, so one regulated item does not hold the whole shipment.

Not sure about {{company}}? Reply with the bill of materials and the fit-out date and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 23 characters (sample names) | Body: 94 words*

```
Subject: {{first_name_lc}}, closing the loop
Preview text: one last note, and an easy way to say not now

Hi {{first_name}},

Last note from me, I promise.

Here is the thing about data center equipment imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Chemicals

`industry-chemicals` | topic: chemical imports | checklist: Chemicals and Controlled Materials Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 27 characters (sample names) | Body: 72 words*

```
Subject: {{first_name_lc}}, checklist, delivered
Preview text: fresh off the press, three things to check first

Hi {{first_name}},

A chemical shipment where the substance decides every single rule... sound familiar?

Delivered, as promised:

[Download the checklist]

Three things to check first:

1. The substance decides everything
2. Controlled-Chemical authority
3. Dangerous-Goods acceptance

Skim it with your own shipment in mind. If something looks off, hit reply and send me the chemical name and its safety data sheet. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 31 characters (sample names) | Body: 95 words*

```
Subject: {{first_name_lc}}, before you ship anything
Preview text: a 10 second check for {{company}}...

Hi {{first_name}},

Before anything ships...

Is the exact substance identified, and have you checked whether it is a controlled chemical and dangerous goods?

A "hmm, not sure" is common here. It is also where chemical imports tends to get stuck.

Here is why it matters: What the material is decides which permits, transport rules and customs treatment apply. We identify the substance first, so every later step is right.

Not sure about {{company}}? Reply with the chemical name and its safety data sheet and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 32 characters (sample names) | Body: 103 words*

```
Subject: should i close your file, {{first_name_lc}}?
Preview text: no pressure either way...

Hi {{first_name}},

I do not want to be the person who keeps emailing, so this is the last one.

Here is the thing about chemical imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Food & Beverage

`industry-food-beverage` | topic: food and beverage imports | checklist: Food, Beverage and FMCG Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 17 characters (sample names) | Body: 74 words*

```
Subject: {{first_name_lc}}, start here
Preview text: the checklist, plus where to look first...

Hi {{first_name}},

Stock that ships before the labels and registration are sorted... sound familiar?

Start with this:

[Download the checklist]

Three things to check first:

1. Labeling and registration
2. Excise and tax questions
3. Temperature and shelf life

Skim it with your own shipment in mind. If something looks off, hit reply and send me the product list and the label artwork. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 26 characters (sample names) | Body: 107 words*

```
Subject: did you check this, {{first_name_lc}}?
Preview text: one for {{company}}, and you can answer in your head...

Hi {{first_name}},

Okay, here goes...

Are the labels and product registration in order before the stock ships, and do you know how tax applies to it?

If your honest answer is "um... probably?", that is the part of food and beverage imports where things tend to go sideways.

Here is why it matters: Products can be held when labels or registrations do not match the shipment. We check both before you ship, so stock is not stuck while a label is fixed.

Not sure about {{company}}? Reply with the product list and the label artwork and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 18 characters (sample names) | Body: 97 words*

```
Subject: no pressure, {{first_name_lc}}
Preview text: one last thing, then I will leave you alone...

Hi {{first_name}},

One last thing, then I will leave you alone.

Here is the thing about food and beverage imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Manufacturing

`industry-manufacturing` | topic: manufacturing equipment imports | checklist: Manufacturing and Industrial Machinery Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 29 characters (sample names) | Body: 85 words*

```
Subject: {{first_name_lc}}, your checklist is here
Preview text: ready when you are... plus 3 things to check first

Hi {{first_name}},

A production line that cannot start because the machinery is stuck in customs... sound familiar?

That is exactly what this checklist is for. Here it is:

[Download the checklist]

Three things to check first:

1. Classification and valuation of machinery
2. Incentive paperwork
3. Packing and installation sequence

Skim it with your own shipment in mind. If something looks off, hit reply and send me the machine list and the installation date. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 29 characters (sample names) | Body: 97 words*

```
Subject: {{first_name_lc}}, is this on your radar?
Preview text: about manufacturing, and worth a minute...

Hi {{first_name}},

Something I always ask first...

Has the machinery been classified and valued, and is the packing sequence planned around installation?

If you had to think about it, that is usually where manufacturing equipment imports starts to wobble.

Here is why it matters: Complex equipment and spare parts are easy to misclassify or undervalue, which causes customs delays. We settle classification and value before filing, so the entry clears first time.

Not sure about {{company}}? Reply with the machine list and the installation date and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 22 characters (sample names) | Body: 96 words*

```
Subject: {{first_name_lc}}, parting thought
Preview text: one more thing, then I am out of your inbox...

Hi {{first_name}},

Parting thought, then I am out of your inbox.

Here is the thing about manufacturing equipment imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Automotive

`industry-automotive` | topic: vehicle and equipment imports | checklist: Automotive, Heavy Equipment and Special-Purpose Vehicles Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 29 characters (sample names) | Body: 87 words*

```
Subject: here is that checklist, {{first_name_lc}}
Preview text: inside: 3 spots worth a look first

Hi {{first_name}},

Buying the vehicle first and finding out it is not admissible after... sound familiar?

So we put together a checklist for exactly that. Here you go:

[Download the checklist]

Three things to check first:

1. Buying before checking admissibility
2. Taxes and permits that change the real cost
3. Delivery after release

Skim it with your own shipment in mind. If something looks off, hit reply and send me the make, model and year. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 24 characters (sample names) | Body: 107 words*

```
Subject: {{first_name_lc}}, spot the problem?
Preview text: see if you can spot it before we do...

Hi {{first_name}},

Let me ask you this...

Has someone confirmed the vehicle or equipment can be imported, and what it will really cost with taxes and permits, before you buy?

A "hmm, not sure" is common here. It is also where vehicle and equipment imports tends to get stuck.

Here is why it matters: Used and special-purpose units can fail eligibility rules after you have paid for them. We check admissibility before you buy, so you never commit to a unit you cannot import.

Not sure about {{company}}? Reply with the make, model and year and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 19 characters (sample names) | Body: 97 words*

```
Subject: {{first_name_lc}}, door is open
Preview text: no hard feelings, either way...

Hi {{first_name}},

I will leave the door open and stop here.

Here is the thing about vehicle and equipment imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Healthcare

`industry-healthcare` | topic: healthcare imports | checklist: Pharmaceuticals, Medical Devices and Healthcare Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 32 characters (sample names) | Body: 83 words*

```
Subject: {{first_name_lc}}, your healthcare checklist
Preview text: grab it now, skim it later...

Hi {{first_name}},

Medical cargo waiting on an approval that does not match the shipment... sound familiar?

Good news, we built a checklist for it. It is yours:

[Download the checklist]

Three things to check first:

1. Unregistered or mismatched documents
2. Controlled and Temperature-Sensitive products
3. Urgent medical cargo

Skim it with your own shipment in mind. If something looks off, hit reply and send me the product and its authorization details. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 33 characters (sample names) | Body: 99 words*

```
Subject: {{first_name_lc}}, real talk about healthcare
Preview text: no fluff, just one question...

Hi {{first_name}},

Real talk...

Is the FDA authorization in place, and does it match what is on the shipment before it arrives?

If your honest answer is "um... probably?", that is the part of healthcare imports where things tend to go sideways.

Here is why it matters: Authorization must be in place and match what is on the shipment. We check every document against the cargo before it ships, so nothing is rejected on arrival.

Not sure about {{company}}? Reply with the product and its authorization details and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 23 characters (sample names) | Body: 96 words*

```
Subject: last one from me, {{first_name_lc}}
Preview text: no hard feelings either way...

Hi {{first_name}},

I will stop filling your inbox after this one, promise.

Here is the thing about healthcare imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Agriculture

`industry-agriculture` | topic: agricultural imports | checklist: Agriculture, Plants, Animals and Fisheries Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 23 characters (sample names) | Body: 83 words*

```
Subject: checklist inside, {{first_name_lc}}
Preview text: short read, three things to check first

Hi {{first_name}},

One shipment, three agencies, and clearances that do not quite match... sound familiar?

Here is the checklist you asked for:

[Download the checklist]

Three things to check first:

1. Several agencies, one shipment
2. Clearances that do not match
3. Perishable cargo on the clock

Skim it with your own shipment in mind. If something looks off, hit reply and send me the product, its origin and the arrival date. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 22 characters (sample names) | Body: 101 words*

```
Subject: {{first_name_lc}}, sound familiar?
Preview text: think about your last shipment...

Hi {{first_name}},

Think about your last shipment for a second...

Do you know every agency that needs to clear this product, and do their clearances describe the shipment the same way?

If you had to think about it, that is usually where agricultural imports starts to wobble.

Here is why it matters: Several agencies can each have a say, depending on the product. We map every clearance before shipping, so no agency surprises the cargo.

Not sure about {{company}}? Reply with the product, its origin and the arrival date and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 23 characters (sample names) | Body: 92 words*

```
Subject: {{first_name_lc}}, closing the loop
Preview text: one last note, and an easy way to say not now

Hi {{first_name}},

Last note from me, I promise.

Here is the thing about agricultural imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Electronics & Telecom

`industry-electronics-telecom` | topic: electronics and telecom imports | checklist: Telecommunications, Electronics and IT Hardware Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 26 characters (sample names) | Body: 77 words*

```
Subject: {{first_name_lc}}, this one is for you
Preview text: your checklist, plus three things to check first...

Hi {{first_name}},

A gadget with a radio or a battery inside that nobody flagged... sound familiar?

If that rings a bell, this is for you:

[Download the checklist]

Three things to check first:

1. Approvals for radio equipment
2. Batteries inside the product
3. Classification errors

Skim it with your own shipment in mind. If something looks off, hit reply and send me the product models. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 50 characters (sample names) | Body: 88 words*

```
Subject: {{first_name_lc}}, honest question about electronics & telecom
Preview text: a 10 second gut check for {{company}}...

Hi {{first_name}},

Honest question...

Does any item contain radio equipment or a battery, and has its classification been confirmed?

A "hmm, not sure" is common here. It is also where electronics and telecom imports tends to get stuck.

Here is why it matters: Radio equipment needs approval before it can be sold or used. We secure it in advance, so units are not held or turned back.

Not sure about {{company}}? Reply with the product models and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 32 characters (sample names) | Body: 105 words*

```
Subject: should i close your file, {{first_name_lc}}?
Preview text: no pressure either way...

Hi {{first_name}},

I do not want to be the person who keeps emailing, so this is the last one.

Here is the thing about electronics and telecom imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Marine

`industry-marine` | topic: marine imports | checklist: Marine, Vessels and Yachts Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 33 characters (sample names) | Body: 78 words*

```
Subject: {{first_name_lc}}, as promised, the checklist
Preview text: no fluff, just the list...

Hi {{first_name}},

A vessel or marine asset waiting on registration and port requirements... sound familiar?

As promised, here it is:

[Download the checklist]

Three things to check first:

1. Registration and port requirements
2. Large assets with complex handling
3. Spares for vessels in service

Skim it with your own shipment in mind. If something looks off, hit reply and send me the vessel or asset details. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 31 characters (sample names) | Body: 91 words*

```
Subject: can i ask you something, {{first_name_lc}}?
Preview text: it is about marine, and it is a short one

Hi {{first_name}},

Can I ask you something?

Are the registration and port requirements for this vessel or asset clear before it moves?

If your honest answer is "um... probably?", that is the part of marine imports where things tend to go sideways.

Here is why it matters: Maritime authority and port requirements run alongside customs. We coordinate all three, so your asset is registered and cleared without gaps.

Not sure about {{company}}? Reply with the vessel or asset details and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 18 characters (sample names) | Body: 95 words*

```
Subject: no pressure, {{first_name_lc}}
Preview text: one last thing, then I will leave you alone...

Hi {{first_name}},

One last thing, then I will leave you alone.

Here is the thing about marine imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Aviation

`industry-aviation` | topic: aviation parts imports | checklist: Aviation and Aerospace Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 27 characters (sample names) | Body: 85 words*

```
Subject: {{first_name_lc}}, checklist, delivered
Preview text: fresh off the press, three things to check first

Hi {{first_name}},

An aircraft on the ground, waiting on a part that is waiting on paperwork... sound familiar?

Delivered, as promised:

[Download the checklist]

Three things to check first:

1. Aircraft on the ground waiting for parts
2. Technical paperwork that must match
3. Regulated items inside the shipment

Skim it with your own shipment in mind. If something looks off, hit reply and send me the part numbers and how urgent they are. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 28 characters (sample names) | Body: 93 words*

```
Subject: {{first_name_lc}}, gut check on aviation
Preview text: answer in your head, no need to reply yet...

Hi {{first_name}},

Gut check time...

For urgent parts, are the technical documents ready to match the shipment before it lands?

If you had to think about it, that is usually where aviation parts imports starts to wobble.

Here is why it matters: Every hour a grounded aircraft waits has a cost. We prepare documents right the first time and prioritize release, so parts reach the aircraft sooner.

Not sure about {{company}}? Reply with the part numbers and how urgent they are and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 22 characters (sample names) | Body: 96 words*

```
Subject: {{first_name_lc}}, parting thought
Preview text: one more thing, then I am out of your inbox...

Hi {{first_name}},

Parting thought, then I am out of your inbox.

Here is the thing about aviation parts imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Retail

`industry-retail` | topic: retail imports | checklist: Retail, Consumer Goods and E-Commerce Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 17 characters (sample names) | Body: 75 words*

```
Subject: {{first_name_lc}}, start here
Preview text: the checklist, plus where to look first...

Hi {{first_name}},

Inventory landing before anyone checked the rules for each product category... sound familiar?

Start with this:

[Download the checklist]

Three things to check first:

1. Product rules vary by category
2. Labeling and intellectual property
3. Valuation of mixed shipments

Skim it with your own shipment in mind. If something looks off, hit reply and send me the product list by category. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 29 characters (sample names) | Body: 93 words*

```
Subject: one thing about retail, {{first_name_lc}}
Preview text: the part that is easy to skip...

Hi {{first_name}},

Here is the one I always start with...

Do you know the rules for each product category in the shipment, including labels?

A "hmm, not sure" is common here. It is also where retail imports tends to get stuck.

Here is why it matters: Different agencies can apply to different items in one shipment. We map requirements per product before shipping, so no item holds back the rest.

Not sure about {{company}}? Reply with the product list by category and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 19 characters (sample names) | Body: 95 words*

```
Subject: {{first_name_lc}}, door is open
Preview text: no hard feelings, either way...

Hi {{first_name}},

I will leave the door open and stop here.

Here is the thing about retail imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Cold Chain

`industry-cold-chain` | topic: cold chain cargo | checklist: Cold Chain and Temperature-Sensitive Cargo Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 29 characters (sample names) | Body: 92 words*

```
Subject: {{first_name_lc}}, your checklist is here
Preview text: ready when you are... plus 3 things to check first

Hi {{first_name}},

The temperature clock that starts ticking the second the cargo hits the port... sound familiar?

That is exactly what this checklist is for. Here it is:

[Download the checklist]

Three things to check first:

1. The temperature clock starts at the port
2. Permits and storage must line up
3. Proof of temperature

Skim it with your own shipment in mind. If something looks off, hit reply and send me the product, its temperature range and the arrival date. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 31 characters (sample names) | Body: 99 words*

```
Subject: {{first_name_lc}}, before you ship anything
Preview text: a 10 second check for {{company}}...

Hi {{first_name}},

Before anything ships...

From the moment the cargo reaches the port, are the cold storage and the permit timing lined up?

If your honest answer is "um... probably?", that is the part of cold chain cargo where things tend to go sideways.

Here is why it matters: Time in customs counts against shelf life. We plan release and pickup together, so the temperature clock is not wasted at the port.

Not sure about {{company}}? Reply with the product, its temperature range and the arrival date and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 23 characters (sample names) | Body: 97 words*

```
Subject: last one from me, {{first_name_lc}}
Preview text: no hard feelings either way...

Hi {{first_name}},

I will stop filling your inbox after this one, promise.

Here is the thing about cold chain cargo... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Mining

`industry-mining` | topic: mining imports | checklist: Mining, Minerals and Industrial Materials Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 29 characters (sample names) | Body: 79 words*

```
Subject: here is that checklist, {{first_name_lc}}
Preview text: inside: 3 spots worth a look first

Hi {{first_name}},

Heavy equipment and controlled materials mixed into one shipment, headed somewhere remote... sound familiar?

So we put together a checklist for exactly that. Here you go:

[Download the checklist]

Three things to check first:

1. Controlled materials
2. Heavy, remote deliveries
3. Mixed shipments

Skim it with your own shipment in mind. If something looks off, hit reply and send me the equipment and materials list. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 26 characters (sample names) | Body: 85 words*

```
Subject: did you check this, {{first_name_lc}}?
Preview text: one for {{company}}, and you can answer in your head...

Hi {{first_name}},

Okay, here goes...

Are the controlled materials separated from the rest, and is the final delivery to site planned?

If you had to think about it, that is usually where mining imports starts to wobble.

Here is why it matters: Explosives and reagents bring extra agency requirements. We secure each approval before shipping, so controlled cargo clears when it lands.

Not sure about {{company}}? Reply with the equipment and materials list and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 23 characters (sample names) | Body: 92 words*

```
Subject: {{first_name_lc}}, closing the loop
Preview text: one last note, and an easy way to say not now

Hi {{first_name}},

Last note from me, I promise.

Here is the thing about mining imports... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---

## Freight Forwarders

`industry-freight-forwarders` | topic: forwarder clearance | checklist: Freight Forwarders and Logistics Providers Import Readiness Checklist

### Email 1: Day 0, deliver the checklist

*Subject length: 40 characters (sample names) | Body: 84 words*

```
Subject: {{first_name_lc}}, your freight forwarders checklist
Preview text: grab it now, skim it later...

Hi {{first_name}},

Your client's cargo turning out to be regulated, with your name on it... sound familiar?

Good news, we built a checklist for it. It is yours:

[Download the checklist]

Three things to check first:

1. Client cargo, your reputation
2. Regulated shipments
3. Confidentiality and authority

Skim it with your own shipment in mind. If something looks off, hit reply and send me the type of cargo your clients move most. I will tell you what I would check first.

{{sender_name}}
The Mills Global
```

### Email 2: Day 3, a quick check

*Subject length: 29 characters (sample names) | Body: 96 words*

```
Subject: {{first_name_lc}}, is this on your radar?
Preview text: about freight forwarders, and worth a minute...

Hi {{first_name}},

Something I always ask first...

When a client's cargo turns out to be regulated, who handles the permits, and under whose authority?

A "hmm, not sure" is common here. It is also where forwarder clearance tends to get stuck.

Here is why it matters: A clearance problem lands on the forwarder even when the cause was paperwork. We handle the filing and follow-up, so your name stays clear.

Not sure about {{company}}? Reply with the type of cargo your clients move most and I will tell you where I would look first.

{{sender_name}}
The Mills Global
```

### Email 3: Day 7, closing the loop

*Subject length: 32 characters (sample names) | Body: 103 words*

```
Subject: should i close your file, {{first_name_lc}}?
Preview text: no pressure either way...

Hi {{first_name}},

I do not want to be the person who keeps emailing, so this is the last one.

Here is the thing about forwarder clearance... it is usually much easier to sort out before the cargo moves than after it is sitting at the port.

If {{company}} has something coming up, grab a time and we will go through it together. No pitch deck, no pressure:

[Book a time]

And if now is not the time, totally fine. The checklist is yours to keep.

{{sender_name}}
The Mills Global

P.S. Wrong person? Just tell me who handles this and I will take it from there.
```

---
