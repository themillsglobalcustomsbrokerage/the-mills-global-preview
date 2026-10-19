# Lead magnet automations: build handoff

**Audience:** whoever is building the n8n and Zoho automations for The Mills Global website. The email copy is being prepared separately and will be handed over; everything else is specified here.

## Ownership

**Ken owns the Zoho and n8n setup:** creating the three custom Lead fields (section 3), the 27 Zoho Workflow Rules that call the follow-up webhooks (section 5), and setting the shared `TOKEN` in every follow-up workflow. Emails are signed by Ari or Joshua (picked per lead, the same person for all three emails). Email content is prepared separately and handed over.

## 1. What this is

The website offers 27 free readiness checklists (PDFs): 11 for services, 16 for industries. A visitor fills in a popup (name, email, phone, company) and downloads the checklist. We need:

1. **Capture:** the form submission becomes a Lead in Zoho CRM, tagged with its service or industry, and the right person is notified.
2. **Email series:** each lead then receives a short series of emails written for that specific service or industry (Email 1 immediately with the checklist, Email 2 on day 3, Email 3 on day 7), and the series stops once someone has been in touch.

Self-hosted n8n: `https://n8n.themillsglobal.com`. CRM: Zoho CRM. Email: Gmail node (change if you prefer another sender).

## 2. Webhooks the website already calls

The site posts the form as `application/x-www-form-urlencoded` (a CORS "simple request", so there is no preflight). Method **POST**.

| Workflow | Production URL | Used for |
|---|---|---|
| Service checklists | `https://n8n.themillsglobal.com/webhook/mills-lead-magnet` | the 11 service guides |
| Industry checklists | `https://n8n.themillsglobal.com/webhook/mills-lead-magnet-industry` | the 16 industry guides |

Both are already set in `js/lead-magnet.js` (`WEBHOOK_URL`, `WEBHOOK_URL_INDUSTRY`).

**Webhook node settings**
- HTTP Method `POST`, Authentication `None` (a secret in browser code is not a secret; protection is validation plus allowed origins).
- Respond: **Using "Respond to Webhook" node**. Reply `200` with JSON `{"ok": true}` as soon as the payload validates, `400` with `{"ok": false, "error": "..."}` when it does not. Do the slow work (Zoho, email) after responding so the popup never waits.
- **Allowed Origins (CORS)**: `https://themillsglobal.com,https://www.themillsglobal.com,https://themillsglobalcustomsbrokerage.github.io` (remove the github.io one when the preview is retired). Without this the browser blocks the response and the popup shows an error even though n8n received the lead.
- The Test URL only works while listening in the editor; the site must use the **Production URL** of an **activated** workflow.

**Payload fields** (read from `$json.body`)

| Field | Notes |
|---|---|
| `guide` | the slug, for example `customs` or `industry-healthcare`; routes everything |
| `guide_title` | checklist title |
| `name`, `email`, `phone`, `company` | required; validate again server-side (name 2+ chars, email format, phone 7 to 15 digits, company 2+ chars) |
| `page` | URL the form was submitted from |
| `submitted_at` | ISO timestamp |
| `gclid`, `gbraid`, `wbraid`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content` | present only when the visitor arrived from an ad; keep them |

Reject unknown `guide` values with a 400.

## 3. Zoho CRM setup

Create these **custom Lead fields** (Ken):

| Field | Type | API name | Values |
|---|---|---|---|
| Service | picklist | `Service` | the 11 service names in section 6 |
| Industry | picklist | `Industry_Segment` | the 16 industry names in section 6 (do not use Zoho's built-in Industry field; it has a fixed list) |
| Priority | picklist | `Priority` | Hot, Normal |

Then one **Custom View per service and industry** filtered on that field, so each team sees its own leads.

**Lead defaults:** Lead Source `Website`, Lead Status `Not Contacted`. Put the checklist title, page, ad source, GCLID and submission time in Description.

**Priority rule:** `Hot` if the lead has a `gclid`, `gbraid` or `wbraid`, or used a company email address (not gmail, yahoo, outlook, hotmail, icloud, live, proton). Otherwise `Normal`.

Use "create or update" (upsert on email) so one person downloading two checklists is not duplicated.

## 4. Workflow A: capture (two workflows: services, industries)

1. Webhook (section 2).
2. Code or Set node: validate, normalize (trim, lowercase email), look up the guide in a map (slug to name, title, PDF), compute Priority, split the name into first and last (Zoho requires a last name; a single word goes in last name only).
3. IF valid: respond 200 and continue; else respond 400.
4. In parallel after responding:
   - Create or update the Zoho Lead with the fields above.
   - Notify the owner of that service or industry by email (a map of segment to owner address; default `inquiry@themillsglobal.com` until owners are assigned).

Set each node's error handling to continue so one failure does not stop the others.

## 5. Workflow B: email series (27 workflows, one per service and industry)

One workflow per segment is deliberate: the team can edit one segment's emails without touching the others. Each is triggered from Zoho.

**Trigger:** a Zoho **Workflow Rule** on Leads: when a record is created and the segment field equals the value (section 6), run a **Webhook** action to that segment's URL (last column of the tables). Send these body parameters (form-urlencoded or JSON):

| Parameter | Zoho merge field |
|---|---|
| `lead_id` | Lead Id |
| `email` | Email |
| `first_name` | First Name |
| `company` | Company |
| `token` | a shared secret (the same constant checked in each workflow; keep it out of the repo) |

**Flow**
1. Webhook node (respond immediately, `onReceived`).
2. Validate the token, a well-formed email and a non-empty `lead_id`. Stop if invalid.
3. **Email 1** now: the checklist (button links to the PDF).
4. **Wait 3 days**, then fetch the lead from Zoho by `lead_id`. Continue only if `Lead_Status` is still `Not Contacted` and `Email_Opt_Out` is false; otherwise end the run.
5. **Email 2**.
6. **Wait 4 more days (day 7)**, fetch the lead again, same check.
7. **Email 3**.

Runs sit in "Waiting" while they wait; that is normal.

Replies of "stop" are not detected automatically: someone must mark the lead as opted out or change its status in Zoho, which ends the series at the next check.

**Values available to the email templates** (so copy can be personal): first name, company, segment name, a plain-language topic (for example "customs clearance"), checklist title, PDF link, the segment's page URL, the booking URL `https://themillsglobal.com/book-a-call.html`, and the three "where clients usually get stuck" points from that segment's page. Fall back gracefully when company or first name is empty.

## 6. Segments

### Services (field `Service`)

| Name | Guide slug | Zoho field value | Checklist title | PDF file | Drive download | Email-series webhook path |
|---|---|---|---|---|---|---|
| Mills Entry | `entry` | Service = Mills Entry | Philippine Market Entry Readiness Checklist | `entry-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=15WuBkbHH1j-I5-4zoPAHlSGaDtDVIH3A) | `/webhook/mills-followup-entry` |
| Mills Permits | `permits` | Service = Mills Permits | Import Permit and Product Registration Checklist | `permits-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1ATG_DlzqelapbWHLZEeaf7svxiikO6W4) | `/webhook/mills-followup-permits` |
| Mills Customs | `customs` | Service = Mills Customs | Customs Clearance Readiness Checklist | `customs-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=15wIUs1BZFzwvcpXs5URhz2q8IhZHyZrf) | `/webhook/mills-followup-customs` |
| Mills Marine | `marine` | Service = Mills Marine | Vessel and Marine Equipment Readiness Checklist | `marine-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1UVnuzpEdNRhkoC0zCRqD_Nqp88SqSMne) | `/webhook/mills-followup-marine` |
| Mills Dangerous Goods | `dangerous-goods` | Service = Mills Dangerous Goods | Dangerous Goods Shipping Readiness Checklist | `dangerous-goods-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=11SDPrFhCB-T1M8AhnVdd803G61pnVNGi) | `/webhook/mills-followup-dangerous-goods` |
| Mills Logistics | `logistics` | Service = Mills Logistics | Post-Clearance Delivery Readiness Checklist | `logistics-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1rX39BT9coo4kC3Sa9Ro8I6SDP4C3VcEw) | `/webhook/mills-followup-logistics` |
| Mills Packaging | `packaging` | Service = Mills Packaging | Export and Industrial Packaging Readiness Checklist | `packaging-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1CG3MPCCEKuDfHU_b8MYZ9Ny6tdxFj1T8) | `/webhook/mills-followup-packaging` |
| Mills Insurance | `insurance` | Service = Mills Insurance | Marine Cargo Insurance Readiness Checklist | `insurance-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1Nr7V1Z0beUJZ6sCdNTgcvctaTMdMLadj) | `/webhook/mills-followup-insurance` |
| Mills Time Critical | `time-critical` | Service = Mills Time Critical | Priority Clearance Readiness Checklist | `time-critical-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1Te6TMfw5IgvDIQfusiEVq7kkuGo2kGfg) | `/webhook/mills-followup-time-critical` |
| Mills Advisory | `advisory` | Service = Mills Advisory | Philippine Trade Regulation Readiness Checklist | `advisory-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1fCRMuRzN4EmpNURD1wrCw3WHBUo-2hYT) | `/webhook/mills-followup-advisory` |
| Mills Projects | `projects` | Service = Mills Projects | Project Cargo Readiness Checklist | `projects-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1f5psxqjY2m4lAvqTpH5UCTHBCIaK1u0C) | `/webhook/mills-followup-projects` |

### Industries (field `Industry_Segment`)

| Name | Guide slug | Zoho field value | Checklist title | PDF file | Drive download | Email-series webhook path |
|---|---|---|---|---|---|---|
| Construction | `industry-construction` | Industry_Segment = Construction | Construction and Infrastructure Import Readiness Checklist | `industry-construction-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1DV4_2BSolup2Kzm6Z21dje4PA1t_G_hM) | `/webhook/mills-followup-industry-construction` |
| Renewable Energy | `industry-renewable-energy` | Industry_Segment = Renewable Energy | Renewable Energy and Power Import Readiness Checklist | `industry-renewable-energy-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1wZPKyeRK3JtbzQKEvbuLgYKe0QlAppTh) | `/webhook/mills-followup-industry-renewable-energy` |
| Data Centers | `industry-data-centers` | Industry_Segment = Data Centers | Data Centers and Digital Infrastructure Import Readiness Checklist | `industry-data-centers-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1K29_Jvm2H503QM7kX82kJTWzCBm4-SGQ) | `/webhook/mills-followup-industry-data-centers` |
| Chemicals | `industry-chemicals` | Industry_Segment = Chemicals | Chemicals and Controlled Materials Import Readiness Checklist | `industry-chemicals-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=14I7U0d77S7R8FdH_DQb46t7H9S4zmd24) | `/webhook/mills-followup-industry-chemicals` |
| Food & Beverage | `industry-food-beverage` | Industry_Segment = Food & Beverage | Food, Beverage and FMCG Import Readiness Checklist | `industry-food-beverage-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=19ktBZQNNabRybkUHYSAv5w1MSvsyCDom) | `/webhook/mills-followup-industry-food-beverage` |
| Manufacturing | `industry-manufacturing` | Industry_Segment = Manufacturing | Manufacturing and Industrial Machinery Import Readiness Checklist | `industry-manufacturing-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1CUMKVA6i8AgEYPZhgg9ycUoFzXXsi3_K) | `/webhook/mills-followup-industry-manufacturing` |
| Automotive | `industry-automotive` | Industry_Segment = Automotive | Automotive, Heavy Equipment and Special-Purpose Vehicles Import Readiness Checklist | `industry-automotive-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1h9hfXEYqCB18SN6XoaDJktWWhM4xFMm5) | `/webhook/mills-followup-industry-automotive` |
| Healthcare | `industry-healthcare` | Industry_Segment = Healthcare | Pharmaceuticals, Medical Devices and Healthcare Import Readiness Checklist | `industry-healthcare-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1fg-nIrXmE1s_0P2x3f2Hj6_AqyzhBS5h) | `/webhook/mills-followup-industry-healthcare` |
| Agriculture | `industry-agriculture` | Industry_Segment = Agriculture | Agriculture, Plants, Animals and Fisheries Import Readiness Checklist | `industry-agriculture-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1GM4y-jmUBy40mFIHbGpHT2RP-zVXk_El) | `/webhook/mills-followup-industry-agriculture` |
| Electronics & Telecom | `industry-electronics-telecom` | Industry_Segment = Electronics & Telecom | Telecommunications, Electronics and IT Hardware Import Readiness Checklist | `industry-electronics-telecom-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1jOufpu3EhWuuhiy-7Z2A3WjDK3W9e4Kc) | `/webhook/mills-followup-industry-electronics-telecom` |
| Marine | `industry-marine` | Industry_Segment = Marine | Marine, Vessels and Yachts Import Readiness Checklist | `industry-marine-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1SOSCYPOQ0blVgnKulqEwhW4lU-SGbmLF) | `/webhook/mills-followup-industry-marine` |
| Aviation | `industry-aviation` | Industry_Segment = Aviation | Aviation and Aerospace Import Readiness Checklist | `industry-aviation-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1zutnZTbkGdxI8TrZcy8lsyhFfyK0GzCe) | `/webhook/mills-followup-industry-aviation` |
| Retail | `industry-retail` | Industry_Segment = Retail | Retail, Consumer Goods and E-Commerce Import Readiness Checklist | `industry-retail-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1vYw8TMxsFAJObb65RKUae_6N3co_LcH8) | `/webhook/mills-followup-industry-retail` |
| Cold Chain | `industry-cold-chain` | Industry_Segment = Cold Chain | Cold Chain and Temperature-Sensitive Cargo Import Readiness Checklist | `industry-cold-chain-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1Qub3QeB752Jkn_ICn7O2aeXpz__mZRsK) | `/webhook/mills-followup-industry-cold-chain` |
| Mining | `industry-mining` | Industry_Segment = Mining | Mining, Minerals and Industrial Materials Import Readiness Checklist | `industry-mining-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1HpEU-cGKy92mFb6EAXuVfpaqE_TNykWe) | `/webhook/mills-followup-industry-mining` |
| Freight Forwarders | `industry-freight-forwarders` | Industry_Segment = Freight Forwarders | Freight Forwarders and Logistics Providers Import Readiness Checklist | `industry-freight-forwarders-readiness-checklist.pdf` | [link](https://drive.google.com/uc?export=download&id=1PVLpYoc0QTTsoS6uQCn3URsWyIR6_BSJ) | `/webhook/mills-followup-industry-freight-forwarders` |

The checklist download button in Email 1 uses the **Drive download link** in the table. Each is a direct-download link to the PDF in the themillsglobalph Google Drive, so it works before the website domain is live. Each file's sharing must be "Anyone with the link can view" for leads to download it without signing in. The same PDFs also live on the site at `https://themillsglobal.com/assets/lead-magnets/<file>` and in the repo under `assets/lead-magnets/`.

## 7. Starter files (optional)

The repo contains importable n8n JSON generated from the above, if you want a head start: `n8n/lead-magnet-services.json`, `n8n/lead-magnet-industries.json` and 27 files in `n8n/followups/`. They are untested: verify node versions and Zoho field names in your n8n and Zoho before relying on them.

## 8. Acceptance checklist

- [ ] POSTing a valid payload to each production URL returns `200` and creates or updates one Zoho Lead with the right Service or Industry_Segment and Priority.
- [ ] An invalid payload (bad email, unknown guide) returns `400` and creates nothing.
- [ ] The popup on the site shows success (the response is readable cross-origin).
- [ ] The owner notification arrives at the right address for that segment.
- [ ] A new Lead triggers its own segment's series, and no other.
- [ ] Email 1 arrives immediately with a working checklist link.
- [ ] Changing the Lead Status to anything other than "Not Contacted" before day 3 stops Email 2 and Email 3.
- [ ] Setting Email Opt Out stops the series.
- [ ] Ad attribution fields (`gclid`, UTMs) reach Zoho.
