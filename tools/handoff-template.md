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

@@HDR@@
@@SERVICES@@

### Industries (field `Industry_Segment`)

@@HDR@@
@@INDUSTRIES@@

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
