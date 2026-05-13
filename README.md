# Campaign Readiness Monitor

Campaign Readiness Monitor compares planned campaign items against configured product, price, stock and channel data, then turns mismatches into actionable review cards.

The campaign plan describes intention. The system data describes truth. The dashboard shows the gap.

## Framing

Systems are truth. Plans are intentions. Operations is the gap between them.

A campaign plan defines what the business intends to sell. Product, pricing, inventory and channel systems show what is actually configured. The app compares intention against truth and summons only the exceptions that need human judgement.

## Core operating question

For each upcoming campaign: Are the planned campaign items actually ready in the system for the campaign period?

## Demo data

All data is synthetic. The demo models two data sources:

1. **Campaign plan** — uploaded/planned Excel-like campaign data (intention)
2. **System truth** — actual configured state across channels (truth)

When no file is uploaded, the app uses the synthetic campaign plan. A basic uploader can also read `.xlsx` and `.csv` campaign plans and compare them against the mocked system truth data.

Uploaded plans are fitted against the campaign plan schema before comparison. The Python schema lives in `campaign_schema.py`, and a machine-readable copy lives in `schemas/campaign_plan_schema.json`. The app also exposes downloadable schema and blank template CSV files in the upload panel.

Minimum upload columns:

- `campaign_id`
- `campaign_name`
- `planned_start`
- `planned_end`
- `channel`
- `item_id`
- `planned_price`

Optional upload columns:

- `campaign_source`
- `planned_category`
- `planned_visibility`
- `planned_owner`

## Exception types detected

- Planned item missing from system
- System item active but missing from plan (unplanned promotions)
- Campaign price missing
- Price mismatch
- Price starts too late / ends too early
- Duplicate / conflicting active prices
- Item not active in target channel
- Wrong category or campaign placement
- Missing image / content
- Stock below forecast demand
- Owner missing

## UI

- Fix First section for the highest-pressure exceptions
- Campaign readiness lane matrix across Plan, PIM, Price, Channel, Content, Stock and Owner
- Mock source freshness panel for campaign plan, product, pricing, inventory and channel visibility data
- Excel vs system check showing uploaded plan values beside matched system values
- KPI cards at top (starting soon, active now, readiness, critical, warnings, unplanned activity)
- Campaign timeline list with readiness percentages
- Exception cards — one actionable case per card with severity, risk, owner, and suggested action
- Filters by campaign, channel, severity
- Business / Technical view modes
- Handoff payload grouped by team and owner, with copyable per-team text payloads

## Future project list

### Mock phase

- Keep using synthetic campaign and system data while the workflow is tested
- Model an Excel-style campaign plan with campaign ID, campaign name, channel, SKU, planned price, start date, end date, category and owner
- Model system truth data with SKU, product status, channel availability, active price, price window, content readiness, image readiness, stock and system owner
- Compare campaign plan rows against system rows and generate exception cards
- Add clear sample cases for missing SKU, wrong price, missing price, inactive channel, missing content, low stock and missing owner
- Add a mock handoff payload grouped by team so the dashboard shows who needs to act

### Excel import

- Improve `.xlsx` and `.csv` upload support with richer examples
- Add downloadable example campaign plan templates generated from the schema
- Validate optional business columns and recommend fixes before comparison
- Show row-level import errors instead of file-level errors only
- Normalize more Excel issues such as empty cells, mixed date formats, extra spaces and inconsistent channel names
- Keep the synthetic data as a demo mode when no file is uploaded

### Campaign vs system comparison

- Compare each planned campaign SKU against the mocked system data
- Detect items in the plan that do not exist in the system
- Detect active system campaign prices that are not present in the plan
- Compare planned price against system price with a configurable tolerance
- Compare planned campaign dates against system price start and end dates
- Compare planned channel against active system channel
- Compare planned category or campaign placement against system category
- Compare forecast demand against available stock

### Dashboard improvements

- Add a side-by-side row inspector for selected exceptions
- Add export buttons for exception queue and team handoff payload
- Add filters for owner, issue type, due date and team
- Add a portfolio view for all campaigns and a focused view for one campaign

### Later integration ideas

- Replace mocked system data with a real product/PIM export
- Add pricing system export or API data
- Add inventory export or API data
- Add content/image readiness data from the e-commerce platform
- Save comparison runs so readiness can be tracked over time
- Add review states such as open, accepted, fixed and deferred
- Add notifications or handoff routing to Teams, email or ticketing tools

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Non-goals

- No real company data
- No live integrations
- No SharePoint/email/server fetching
- Not a full ERP/PIM replacement
- Not a generic dashboard — the value is the exception queue and handoff
