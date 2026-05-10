# Campaign Readiness Monitor

Internal codename: Goblin Manager.

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

- KPI cards at top (starting soon, active now, readiness, critical, warnings, unplanned activity)
- Campaign timeline list with readiness percentages
- Exception cards — one actionable case per card with severity, risk, owner, and suggested action
- Filters by campaign, channel, severity
- Business / Technical view modes
- Handoff payload grouped by team (Pricing, Product Data, Inventory, E-commerce, Campaign Owner)

## Run locally

```bash
pip install streamlit pandas
streamlit run app.py
```

## Non-goals

- No real company data
- No live integrations
- No SharePoint/email/server fetching
- Not a full ERP/PIM replacement
- Not a generic dashboard — the value is the exception queue and handoff
