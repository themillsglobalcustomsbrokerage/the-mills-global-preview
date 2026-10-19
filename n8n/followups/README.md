# Email series workflows (one per service and industry)

Each file here is an importable n8n workflow. A Zoho CRM Workflow Rule (Leads, on create, with the field below equal to the value) calls its webhook. Email 1 (the checklist) goes out immediately; Email 2 on day 3 and Email 3 on day 7, only while the lead is still "Not Contacted" in Zoho.

Zoho webhook body parameters: `lead_id` = Lead Id, `email` = Email, `first_name` = First Name, `company` = Company, `token` = the TOKEN you set in each code node.

| Segment | Zoho field = value | n8n webhook path | File |
|---|---|---|---|
| Mills Entry | Service = Mills Entry | `/webhook/mills-followup-entry` | `followup-entry.json` |
| Mills Permits | Service = Mills Permits | `/webhook/mills-followup-permits` | `followup-permits.json` |
| Mills Customs | Service = Mills Customs | `/webhook/mills-followup-customs` | `followup-customs.json` |
| Mills Marine | Service = Mills Marine | `/webhook/mills-followup-marine` | `followup-marine.json` |
| Mills Dangerous Goods | Service = Mills Dangerous Goods | `/webhook/mills-followup-dangerous-goods` | `followup-dangerous-goods.json` |
| Mills Logistics | Service = Mills Logistics | `/webhook/mills-followup-logistics` | `followup-logistics.json` |
| Mills Packaging | Service = Mills Packaging | `/webhook/mills-followup-packaging` | `followup-packaging.json` |
| Mills Insurance | Service = Mills Insurance | `/webhook/mills-followup-insurance` | `followup-insurance.json` |
| Mills Time Critical | Service = Mills Time Critical | `/webhook/mills-followup-time-critical` | `followup-time-critical.json` |
| Mills Advisory | Service = Mills Advisory | `/webhook/mills-followup-advisory` | `followup-advisory.json` |
| Mills Projects | Service = Mills Projects | `/webhook/mills-followup-projects` | `followup-projects.json` |
| Construction | Industry_Segment = Construction | `/webhook/mills-followup-industry-construction` | `followup-industry-construction.json` |
| Renewable Energy | Industry_Segment = Renewable Energy | `/webhook/mills-followup-industry-renewable-energy` | `followup-industry-renewable-energy.json` |
| Data Centers | Industry_Segment = Data Centers | `/webhook/mills-followup-industry-data-centers` | `followup-industry-data-centers.json` |
| Chemicals | Industry_Segment = Chemicals | `/webhook/mills-followup-industry-chemicals` | `followup-industry-chemicals.json` |
| Food & Beverage | Industry_Segment = Food & Beverage | `/webhook/mills-followup-industry-food-beverage` | `followup-industry-food-beverage.json` |
| Manufacturing | Industry_Segment = Manufacturing | `/webhook/mills-followup-industry-manufacturing` | `followup-industry-manufacturing.json` |
| Automotive | Industry_Segment = Automotive | `/webhook/mills-followup-industry-automotive` | `followup-industry-automotive.json` |
| Healthcare | Industry_Segment = Healthcare | `/webhook/mills-followup-industry-healthcare` | `followup-industry-healthcare.json` |
| Agriculture | Industry_Segment = Agriculture | `/webhook/mills-followup-industry-agriculture` | `followup-industry-agriculture.json` |
| Electronics & Telecom | Industry_Segment = Electronics & Telecom | `/webhook/mills-followup-industry-electronics-telecom` | `followup-industry-electronics-telecom.json` |
| Marine | Industry_Segment = Marine | `/webhook/mills-followup-industry-marine` | `followup-industry-marine.json` |
| Aviation | Industry_Segment = Aviation | `/webhook/mills-followup-industry-aviation` | `followup-industry-aviation.json` |
| Retail | Industry_Segment = Retail | `/webhook/mills-followup-industry-retail` | `followup-industry-retail.json` |
| Cold Chain | Industry_Segment = Cold Chain | `/webhook/mills-followup-industry-cold-chain` | `followup-industry-cold-chain.json` |
| Mining | Industry_Segment = Mining | `/webhook/mills-followup-industry-mining` | `followup-industry-mining.json` |
| Freight Forwarders | Industry_Segment = Freight Forwarders | `/webhook/mills-followup-industry-freight-forwarders` | `followup-industry-freight-forwarders.json` |
