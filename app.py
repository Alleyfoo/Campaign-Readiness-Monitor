import pandas as pd
import streamlit as st
from datetime import date, timedelta
import os
import json


ANCHOR = date(2026, 6, 1)
CHANNELS = ["webshop", "B2B", "mail order", "local store"]
SEVERITY_COLORS = {"Critical": "#DC2626", "Warning": "#D97706", "OK": "#059669"}


def load_design_css():
    css_path = os.path.join(os.path.dirname(__file__), "design", "design.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        return f"<style>\n{css}\n</style>"
    except Exception:
        return ""


def generate_campaign_plan() -> pd.DataFrame:
    rows = [
        {"campaign_id": "CAMP-001", "campaign_name": "Summer Launch", "campaign_source": "Excel plan",
         "planned_start": ANCHOR, "planned_end": ANCHOR + timedelta(days=13),
         "channel": "webshop", "item_id": "SKU-001", "planned_price": 19.90,
         "planned_category": "Summer Essentials", "planned_visibility": True,
         "planned_owner": "Alice (Campaigns)"},
        {"campaign_id": "CAMP-001", "campaign_name": "Summer Launch", "campaign_source": "Excel plan",
         "planned_start": ANCHOR, "planned_end": ANCHOR + timedelta(days=13),
         "channel": "webshop", "item_id": "SKU-002", "planned_price": 24.90,
         "planned_category": "Summer Essentials", "planned_visibility": True,
         "planned_owner": "Alice (Campaigns)"},
        {"campaign_id": "CAMP-001", "campaign_name": "Summer Launch", "campaign_source": "Excel plan",
         "planned_start": ANCHOR, "planned_end": ANCHOR + timedelta(days=13),
         "channel": "webshop", "item_id": "SKU-003", "planned_price": 34.50,
         "planned_category": "Summer Essentials", "planned_visibility": True,
         "planned_owner": "Alice (Campaigns)"},
        {"campaign_id": "CAMP-001", "campaign_name": "Summer Launch", "campaign_source": "Excel plan",
         "planned_start": ANCHOR, "planned_end": ANCHOR + timedelta(days=13),
         "channel": "webshop", "item_id": "SKU-004", "planned_price": 15.00,
         "planned_category": "Summer Essentials", "planned_visibility": True,
         "planned_owner": "Alice (Campaigns)"},
        {"campaign_id": "CAMP-001", "campaign_name": "Summer Launch", "campaign_source": "Excel plan",
         "planned_start": ANCHOR, "planned_end": ANCHOR + timedelta(days=13),
         "channel": "webshop", "item_id": "SKU-005", "planned_price": 9.99,
         "planned_category": "Summer Essentials", "planned_visibility": True,
         "planned_owner": "Alice (Campaigns)"},
        {"campaign_id": "CAMP-001", "campaign_name": "Summer Launch", "campaign_source": "Excel plan",
         "planned_start": ANCHOR, "planned_end": ANCHOR + timedelta(days=13),
         "channel": "webshop", "item_id": "SKU-006", "planned_price": 42.00,
         "planned_category": "Summer Essentials", "planned_visibility": True,
         "planned_owner": "Alice (Campaigns)"},
        {"campaign_id": "CAMP-001", "campaign_name": "Summer Launch", "campaign_source": "Excel plan",
         "planned_start": ANCHOR, "planned_end": ANCHOR + timedelta(days=13),
         "channel": "webshop", "item_id": "SKU-007", "planned_price": 29.90,
         "planned_category": "Summer Essentials", "planned_visibility": True,
         "planned_owner": "Alice (Campaigns)"},
        {"campaign_id": "CAMP-002", "campaign_name": "B2B Q3 Price List", "campaign_source": "SharePoint upload",
         "planned_start": ANCHOR - timedelta(days=5), "planned_end": ANCHOR + timedelta(days=25),
         "channel": "B2B", "item_id": "SKU-010", "planned_price": 89.00,
         "planned_category": "Bulk Hardware", "planned_visibility": True,
         "planned_owner": "Bob (B2B Sales)"},
        {"campaign_id": "CAMP-002", "campaign_name": "B2B Q3 Price List", "campaign_source": "SharePoint upload",
         "planned_start": ANCHOR - timedelta(days=5), "planned_end": ANCHOR + timedelta(days=25),
         "channel": "B2B", "item_id": "SKU-011", "planned_price": 120.00,
         "planned_category": "Bulk Hardware", "planned_visibility": True,
         "planned_owner": "Bob (B2B Sales)"},
        {"campaign_id": "CAMP-002", "campaign_name": "B2B Q3 Price List", "campaign_source": "SharePoint upload",
         "planned_start": ANCHOR - timedelta(days=5), "planned_end": ANCHOR + timedelta(days=25),
         "channel": "B2B", "item_id": "SKU-012", "planned_price": 55.00,
         "planned_category": "Bulk Hardware", "planned_visibility": True,
         "planned_owner": "Bob (B2B Sales)"},
        {"campaign_id": "CAMP-002", "campaign_name": "B2B Q3 Price List", "campaign_source": "SharePoint upload",
         "planned_start": ANCHOR - timedelta(days=5), "planned_end": ANCHOR + timedelta(days=25),
         "channel": "B2B", "item_id": "SKU-013", "planned_price": 210.00,
         "planned_category": "Bulk Hardware", "planned_visibility": True,
         "planned_owner": ""},
        {"campaign_id": "CAMP-003", "campaign_name": "Local Store Promo", "campaign_source": "Manual plan",
         "planned_start": ANCHOR + timedelta(days=2), "planned_end": ANCHOR + timedelta(days=8),
         "channel": "local store", "item_id": "SKU-014", "planned_price": 7.50,
         "planned_category": "Impulse Buys", "planned_visibility": True,
         "planned_owner": "Carol (Local)"},
        {"campaign_id": "CAMP-003", "campaign_name": "Local Store Promo", "campaign_source": "Manual plan",
         "planned_start": ANCHOR + timedelta(days=2), "planned_end": ANCHOR + timedelta(days=8),
         "channel": "local store", "item_id": "SKU-015", "planned_price": 12.00,
         "planned_category": "Impulse Buys", "planned_visibility": True,
         "planned_owner": "Carol (Local)"},
        {"campaign_id": "CAMP-003", "campaign_name": "Local Store Promo", "campaign_source": "Manual plan",
         "planned_start": ANCHOR + timedelta(days=2), "planned_end": ANCHOR + timedelta(days=8),
         "channel": "local store", "item_id": "SKU-016", "planned_price": 3.99,
         "planned_category": "Impulse Buys", "planned_visibility": True,
         "planned_owner": "Carol (Local)"},
        {"campaign_id": "CAMP-004", "campaign_name": "Mail Order June", "campaign_source": "Email attachment",
         "planned_start": ANCHOR + timedelta(days=10), "planned_end": ANCHOR + timedelta(days=30),
         "channel": "mail order", "item_id": "SKU-020", "planned_price": 64.00,
         "planned_category": "Home & Garden", "planned_visibility": True,
         "planned_owner": "Dave (Mail Order)"},
        {"campaign_id": "CAMP-004", "campaign_name": "Mail Order June", "campaign_source": "Email attachment",
         "planned_start": ANCHOR + timedelta(days=10), "planned_end": ANCHOR + timedelta(days=30),
         "channel": "mail order", "item_id": "SKU-021", "planned_price": 38.00,
         "planned_category": "Home & Garden", "planned_visibility": True,
         "planned_owner": "Dave (Mail Order)"},
    ]
    return pd.DataFrame(rows)

def generate_system_truth() -> pd.DataFrame:
    rows = [
        {"item_id": "SKU-001", "product_name": "Beach Towel XL", "product_exists": True,
         "master_category": "Summer Essentials", "system_channel": "webshop",
         "system_price": 19.90, "price_start": ANCHOR, "price_end": ANCHOR + timedelta(days=13),
         "webshop_visible": True, "content_ready": True, "image_ready": True,
         "stock_on_hand": 500, "forecast_demand": 300, "stock_risk": "low", "owner": "Pricing Team"},
        {"item_id": "SKU-002", "product_name": "Sunglasses Pro", "product_exists": True,
         "master_category": "Summer Essentials", "system_channel": "webshop",
         "system_price": 27.90, "price_start": ANCHOR, "price_end": ANCHOR + timedelta(days=13),
         "webshop_visible": True, "content_ready": True, "image_ready": True,
         "stock_on_hand": 200, "forecast_demand": 250, "stock_risk": "medium", "owner": "Pricing Team"},
        {"item_id": "SKU-003", "product_name": "Cooler Bag 20L", "product_exists": True,
         "master_category": "Summer Essentials", "system_channel": "webshop",
         "system_price": 34.50, "price_start": ANCHOR + timedelta(days=2), "price_end": ANCHOR + timedelta(days=13),
         "webshop_visible": True, "content_ready": True, "image_ready": True,
         "stock_on_hand": 150, "forecast_demand": 120, "stock_risk": "low", "owner": "Pricing Team"},
        {"item_id": "SKU-004", "product_name": "Flip Flops Basic", "product_exists": True,
         "master_category": "Summer Essentials", "system_channel": "webshop",
         "system_price": 15.00, "price_start": ANCHOR, "price_end": ANCHOR + timedelta(days=10),
         "webshop_visible": True, "content_ready": True, "image_ready": True,
         "stock_on_hand": 800, "forecast_demand": 600, "stock_risk": "low", "owner": "Pricing Team"},
        {"item_id": "SKU-005", "product_name": "Water Bottle 500ml", "product_exists": False,
         "master_category": "", "system_channel": "", "system_price": 0,
         "price_start": None, "price_end": None, "webshop_visible": False,
         "content_ready": False, "image_ready": False, "stock_on_hand": 0,
         "forecast_demand": 0, "stock_risk": "N/A", "owner": ""},
        {"item_id": "SKU-006", "product_name": "Sun Hat Wide Brim", "product_exists": True,
         "master_category": "Accessories", "system_channel": "webshop",
         "system_price": 42.00, "price_start": ANCHOR, "price_end": ANCHOR + timedelta(days=13),
         "webshop_visible": True, "content_ready": True, "image_ready": True,
         "stock_on_hand": 100, "forecast_demand": 180, "stock_risk": "high", "owner": "Pricing Team"},
        {"item_id": "SKU-007", "product_name": "Picnic Blanket", "product_exists": True,
         "master_category": "Summer Essentials", "system_channel": "webshop",
         "system_price": 29.90, "price_start": ANCHOR, "price_end": ANCHOR + timedelta(days=13),
         "webshop_visible": False, "content_ready": True, "image_ready": False,
         "stock_on_hand": 60, "forecast_demand": 100, "stock_risk": "high", "owner": "Pricing Team"},
        {"item_id": "SKU-010", "product_name": "Industrial Drill Kit", "product_exists": True,
         "master_category": "Bulk Hardware", "system_channel": "B2B",
         "system_price": 89.00, "price_start": ANCHOR - timedelta(days=5), "price_end": ANCHOR + timedelta(days=25),
         "webshop_visible": False, "content_ready": True, "image_ready": True,
         "stock_on_hand": 45, "forecast_demand": 40, "stock_risk": "low", "owner": "B2B Pricing"},
        {"item_id": "SKU-011", "product_name": "Steel Fastener Set", "product_exists": True,
         "master_category": "Bulk Hardware", "system_channel": "B2B",
         "system_price": 135.00, "price_start": ANCHOR - timedelta(days=5), "price_end": ANCHOR + timedelta(days=25),
         "webshop_visible": False, "content_ready": True, "image_ready": True,
         "stock_on_hand": 200, "forecast_demand": 150, "stock_risk": "low", "owner": "B2B Pricing"},
        {"item_id": "SKU-012", "product_name": "Safety Goggles Pro", "product_exists": True,
         "master_category": "Bulk Hardware", "system_channel": "B2B",
         "system_price": 55.00, "price_start": ANCHOR - timedelta(days=5), "price_end": ANCHOR + timedelta(days=25),
         "webshop_visible": False, "content_ready": True, "image_ready": True,
         "stock_on_hand": 300, "forecast_demand": 100, "stock_risk": "low", "owner": "B2B Pricing"},
        {"item_id": "SKU-012", "product_name": "Safety Goggles Pro", "product_exists": True,
         "master_category": "Bulk Hardware", "system_channel": "webshop",
         "system_price": 59.00, "price_start": ANCHOR - timedelta(days=5), "price_end": ANCHOR + timedelta(days=25),
         "webshop_visible": True, "content_ready": True, "image_ready": True,
         "stock_on_hand": 300, "forecast_demand": 100, "stock_risk": "low", "owner": "B2B Pricing"},
        {"item_id": "SKU-013", "product_name": "Hydraulic Pump 2T", "product_exists": True,
         "master_category": "Bulk Hardware", "system_channel": "B2B",
         "system_price": 210.00, "price_start": ANCHOR - timedelta(days=5), "price_end": ANCHOR + timedelta(days=25),
         "webshop_visible": False, "content_ready": True, "image_ready": True,
         "stock_on_hand": 12, "forecast_demand": 15, "stock_risk": "medium", "owner": ""},
        {"item_id": "SKU-014", "product_name": "Chewing Gum Pack", "product_exists": True,
         "master_category": "Impulse Buys", "system_channel": "local store",
         "system_price": 7.50, "price_start": ANCHOR + timedelta(days=2), "price_end": ANCHOR + timedelta(days=8),
         "webshop_visible": False, "content_ready": True, "image_ready": True,
         "stock_on_hand": 2000, "forecast_demand": 1500, "stock_risk": "low", "owner": "Local Ops"},
        {"item_id": "SKU-015", "product_name": "Chocolate Bar 100g", "product_exists": True,
         "master_category": "Impulse Buys", "system_channel": "local store",
         "system_price": 0, "price_start": None, "price_end": None,
         "webshop_visible": False, "content_ready": True, "image_ready": True,
         "stock_on_hand": 500, "forecast_demand": 400, "stock_risk": "low", "owner": "Local Ops"},
        {"item_id": "SKU-016", "product_name": "Energy Drink Can", "product_exists": True,
         "master_category": "Beverages", "system_channel": "local store",
         "system_price": 3.99, "price_start": ANCHOR + timedelta(days=2), "price_end": ANCHOR + timedelta(days=8),
         "webshop_visible": False, "content_ready": True, "image_ready": True,
         "stock_on_hand": 1000, "forecast_demand": 800, "stock_risk": "low", "owner": "Local Ops"},
        {"item_id": "SKU-020", "product_name": "Garden Hose 15m", "product_exists": True,
         "master_category": "Home & Garden", "system_channel": "mail order",
         "system_price": 64.00, "price_start": ANCHOR + timedelta(days=10), "price_end": ANCHOR + timedelta(days=30),
         "webshop_visible": False, "content_ready": True, "image_ready": True,
         "stock_on_hand": 80, "forecast_demand": 90, "stock_risk": "medium", "owner": "Mail Order Team"},
        {"item_id": "SKU-021", "product_name": "Plant Pot Set 3pk", "product_exists": True,
         "master_category": "Home & Garden", "system_channel": "mail order",
         "system_price": 38.00, "price_start": ANCHOR + timedelta(days=10), "price_end": ANCHOR + timedelta(days=30),
         "webshop_visible": False, "content_ready": False, "image_ready": False,
         "stock_on_hand": 30, "forecast_demand": 60, "stock_risk": "high", "owner": "Mail Order Team"},
        {"item_id": "SKU-099", "product_name": "LED Lantern Camping", "product_exists": True,
         "master_category": "Outdoor", "system_channel": "webshop",
         "system_price": 22.00, "price_start": ANCHOR, "price_end": ANCHOR + timedelta(days=10),
         "webshop_visible": True, "content_ready": True, "image_ready": True,
         "stock_on_hand": 120, "forecast_demand": 100, "stock_risk": "low", "owner": "Pricing Team"},
        {"item_id": "SKU-100", "product_name": "Portable Speaker BT", "product_exists": True,
         "master_category": "Electronics", "system_channel": "local store",
         "system_price": 45.00, "price_start": ANCHOR + timedelta(days=2), "price_end": ANCHOR + timedelta(days=8),
         "webshop_visible": False, "content_ready": True, "image_ready": True,
         "stock_on_hand": 25, "forecast_demand": 40, "stock_risk": "high", "owner": ""},
    ]
    df = pd.DataFrame(rows)
    for col in ["price_start", "price_end"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def compare_plan_vs_system(plan: pd.DataFrame, system: pd.DataFrame) -> list[dict]:
    exceptions = []
    today = ANCHOR
    plan_campaigns = plan.groupby("campaign_id")
    planned_ids = set(plan["item_id"].unique())
    for campaign_id, group in plan_campaigns:
        campaign_name = group["campaign_name"].iloc[0]
        campaign_source = group["campaign_source"].iloc[0]
        p_start = pd.Timestamp(group["planned_start"].iloc[0])
        p_end = pd.Timestamp(group["planned_end"].iloc[0])
        channel = group["channel"].iloc[0]
        for _, row in group.iterrows():
            item_id = row["item_id"]
            planned_price = row["planned_price"]
            planned_category = row["planned_category"]
            planned_owner = row["planned_owner"]
            sys_rows = system[system["item_id"] == item_id]
            sys_channel_rows = sys_rows[sys_rows["system_channel"] == channel]
            if sys_rows.empty or not sys_rows["product_exists"].any():
                exceptions.append({
                    "campaign_id": campaign_id, "campaign_name": campaign_name,
                    "campaign_source": campaign_source, "channel": channel,
                    "item_id": item_id, "product_name": "Unknown",
                    "issue_type": "Planned item missing from system",
                    "severity": "Critical",
                    "plan_value": f"Price {planned_price:.2f}, Category: {planned_category}",
                    "system_value": "Not found in any system",
                    "risk": "Customer-facing item unavailable during campaign",
                    "owner": planned_owner or "Unassigned",
                    "action": "Create item in system or remove from campaign plan",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                })
                continue
            if sys_channel_rows.empty:
                other_channels = sys_rows["system_channel"].unique().tolist()
                exceptions.append({
                    "campaign_id": campaign_id, "campaign_name": campaign_name,
                    "campaign_source": campaign_source, "channel": channel,
                    "item_id": item_id,
                    "product_name": sys_rows["product_name"].iloc[0],
                    "issue_type": "Item not active in target channel",
                    "severity": "Critical",
                    "plan_value": f"Channel: {channel}",
                    "system_value": f"Found in: {', '.join(other_channels)}",
                    "risk": "Campaign item not visible in planned channel",
                    "owner": planned_owner or sys_rows["owner"].iloc[0] or "Unassigned",
                    "action": "Add item to target channel or reassign campaign",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                })
                continue
            sys_row = sys_channel_rows.iloc[0]
            product_name = sys_row["product_name"]
            sys_price = sys_row["system_price"]
            price_s = sys_row["price_start"]
            price_e = sys_row["price_end"]
            sys_owner = sys_row["owner"]
            if len(sys_channel_rows) > 1:
                exceptions.append({
                    "campaign_id": campaign_id, "campaign_name": campaign_name,
                    "campaign_source": campaign_source, "channel": channel,
                    "item_id": item_id, "product_name": product_name,
                    "issue_type": "Duplicate / conflicting active prices",
                    "severity": "Critical",
                    "plan_value": f"Price {planned_price:.2f}",
                    "system_value": f"{len(sys_channel_rows)} price records in {channel}",
                    "risk": "Multiple active prices cause checkout errors",
                    "owner": planned_owner or sys_owner or "Unassigned",
                    "action": "Resolve duplicate pricing, keep one active record",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                })
            if pd.isna(price_s) or sys_price == 0:
                exceptions.append({
                    "campaign_id": campaign_id, "campaign_name": campaign_name,
                    "campaign_source": campaign_source, "channel": channel,
                    "item_id": item_id, "product_name": product_name,
                    "issue_type": "Campaign price missing in system",
                    "severity": "Critical",
                    "plan_value": f"Price {planned_price:.2f}",
                    "system_value": "No price configured",
                    "risk": "Customer-facing price unavailable during campaign",
                    "owner": planned_owner or sys_owner or "Unassigned",
                    "action": "Create price record / exclude item / mark reviewed",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                })
                continue
            if abs(sys_price - planned_price) > planned_price * 0.01:
                exceptions.append({
                    "campaign_id": campaign_id, "campaign_name": campaign_name,
                    "campaign_source": campaign_source, "channel": channel,
                    "item_id": item_id, "product_name": product_name,
                    "issue_type": "Price mismatch",
                    "severity": "Warning",
                    "plan_value": f"Plan: {planned_price:.2f}",
                    "system_value": f"System: {sys_price:.2f}",
                    "risk": "Wrong price visible to customers",
                    "owner": planned_owner or sys_owner or "Unassigned",
                    "action": "Align system price with campaign plan or update plan",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                })
            if pd.notna(price_s) and price_s > p_start:
                exceptions.append({
                    "campaign_id": campaign_id, "campaign_name": campaign_name,
                    "campaign_source": campaign_source, "channel": channel,
                    "item_id": item_id, "product_name": product_name,
                    "issue_type": "Price starts too late",
                    "severity": "Warning",
                    "plan_value": f"Campaign starts: {p_start.date()}",
                    "system_value": f"System price starts: {price_s.date()}",
                    "risk": f"Wrong price visible for first {(price_s - p_start).days} campaign days",
                    "owner": planned_owner or sys_owner or "Unassigned",
                    "action": "Fix start date / accept exception",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                })
            if pd.notna(price_e) and price_e < p_end:
                exceptions.append({
                    "campaign_id": campaign_id, "campaign_name": campaign_name,
                    "campaign_source": campaign_source, "channel": channel,
                    "item_id": item_id, "product_name": product_name,
                    "issue_type": "Price ends too early",
                    "severity": "Warning",
                    "plan_value": f"Campaign ends: {p_end.date()}",
                    "system_value": f"System price ends: {price_e.date()}",
                    "risk": "Price reverts before campaign ends",
                    "owner": planned_owner or sys_owner or "Unassigned",
                    "action": "Extend price validity to match campaign end",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                })
            if planned_category and sys_row["master_category"] != planned_category:
                exceptions.append({
                    "campaign_id": campaign_id, "campaign_name": campaign_name,
                    "campaign_source": campaign_source, "channel": channel,
                    "item_id": item_id, "product_name": product_name,
                    "issue_type": "Wrong category / campaign placement",
                    "severity": "Warning",
                    "plan_value": f"Plan: {planned_category}",
                    "system_value": f"System: {sys_row['master_category']}",
                    "risk": "Item may appear in wrong navigation or campaign section",
                    "owner": planned_owner or sys_owner or "Unassigned",
                    "action": "Update master category or campaign placement",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                })
            if channel == "webshop":
                if not sys_row["webshop_visible"]:
                    exceptions.append({
                        "campaign_id": campaign_id, "campaign_name": campaign_name,
                        "campaign_source": campaign_source, "channel": channel,
                        "item_id": item_id, "product_name": product_name,
                        "issue_type": "Item not visible in webshop",
                        "severity": "Critical",
                        "plan_value": "Planned: visible",
                        "system_value": "System: hidden",
                        "risk": "Campaign item not findable by customers",
                        "owner": planned_owner or sys_owner or "Unassigned",
                        "action": "Enable webshop visibility flag",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                    })
                if not sys_row["image_ready"] or not sys_row["content_ready"]:
                    missing = []
                    if not sys_row["image_ready"]: missing.append("image")
                    if not sys_row["content_ready"]: missing.append("content")
                    exceptions.append({
                        "campaign_id": campaign_id, "campaign_name": campaign_name,
                        "campaign_source": campaign_source, "channel": channel,
                        "item_id": item_id, "product_name": product_name,
                        "issue_type": "Missing image / content",
                        "severity": "Warning",
                        "plan_value": "Expected: ready",
                        "system_value": f"Missing: {', '.join(missing)}",
                        "risk": "Poor customer experience, lower conversion",
                        "owner": planned_owner or sys_owner or "Unassigned",
                        "action": "Upload missing assets before campaign start",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                    })
            stock = sys_row["stock_on_hand"]
            forecast = sys_row["forecast_demand"]
            if stock < forecast:
                exceptions.append({
                    "campaign_id": campaign_id, "campaign_name": campaign_name,
                    "campaign_source": campaign_source, "channel": channel,
                    "item_id": item_id, "product_name": product_name,
                    "issue_type": "Stock below forecast demand",
                    "severity": "Warning",
                    "plan_value": f"Forecast: {forecast}",
                    "system_value": f"Stock: {stock}",
                    "risk": f"Potential stockout, risk: {sys_row['stock_risk']}",
                    "owner": planned_owner or sys_owner or "Unassigned",
                    "action": "Replenish stock / adjust forecast / reduce campaign scope",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                })
            if not planned_owner and not sys_owner:
                exceptions.append({
                    "campaign_id": campaign_id, "campaign_name": campaign_name,
                    "campaign_source": campaign_source, "channel": channel,
                    "item_id": item_id, "product_name": product_name,
                    "issue_type": "Owner missing",
                    "severity": "Warning",
                    "plan_value": "No plan owner", "system_value": "No system owner",
                    "risk": "No one accountable for resolution",
                    "owner": "Unassigned",
                    "action": "Assign owner in plan or system",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                })
    system_active = system[system["price_start"].notna() & (system["system_price"] > 0)]
    for _, srow in system_active.iterrows():
        sid = srow["item_id"]
        if sid not in planned_ids:
            s_start = srow["price_start"]
            s_end = srow["price_end"]
            if pd.notna(s_start) and pd.notna(s_end):
                exceptions.append({
                    "campaign_id": "SYSTEM-DETECTED", "campaign_name": "Unplanned active campaign price",
                    "campaign_source": "System detected", "channel": srow["system_channel"],
                    "item_id": sid, "product_name": srow["product_name"],
                    "issue_type": "System item active but missing from any plan",
                    "severity": "Warning",
                    "plan_value": "Not in any campaign plan",
                    "system_value": f"Active price {srow['system_price']:.2f} in {srow['system_channel']}",
                    "risk": "Unplanned customer-facing promotion or stale price",
                    "owner": srow["owner"] or "Unassigned",
                    "action": "Add to plan / remove price / investigate",
                    "date_window": f"{s_start.date()} - {s_end.date()}",
                })
    return exceptions

def build_campaign_summary(plan: pd.DataFrame, exceptions: list[dict]) -> pd.DataFrame:
    campaigns = plan.groupby("campaign_id").agg(
        campaign_name=("campaign_name", "first"),
        campaign_source=("campaign_source", "first"),
        planned_start=("planned_start", "first"),
        planned_end=("planned_end", "first"),
        channel=("channel", "first"),
        item_count=("item_id", "nunique"),
    ).reset_index()
    for _, row in campaigns.iterrows():
        cid = row["campaign_id"]
        c_exc = [e for e in exceptions if e["campaign_id"] == cid]
        total = row["item_count"]
        crit = sum(1 for e in c_exc if e["severity"] == "Critical")
        warn = sum(1 for e in c_exc if e["severity"] == "Warning")
        ready = total - crit - warn
        campaigns.loc[campaigns["campaign_id"] == cid, "ready_items"] = max(ready, 0)
        campaigns.loc[campaigns["campaign_id"] == cid, "critical_count"] = crit
        campaigns.loc[campaigns["campaign_id"] == cid, "warning_count"] = warn
        campaigns.loc[campaigns["campaign_id"] == cid, "readiness_pct"] = (
            int(max(ready, 0) / total * 100) if total > 0 else 0
        )
    return campaigns


def render_kpi_cards(plan: pd.DataFrame, exceptions: list[dict]):
    today = ANCHOR
    campaigns = plan.groupby("campaign_id").agg(
        planned_start=("planned_start", "first"),
        planned_end=("planned_end", "first"),
    )
    starting_soon = sum(
        1 for _, r in campaigns.iterrows()
        if pd.Timestamp(r["planned_start"]) > today
        and (pd.Timestamp(r["planned_start"]) - today).days <= 7
    )
    active_now = sum(
        1 for _, r in campaigns.iterrows()
        if pd.Timestamp(r["planned_start"]) <= today <= pd.Timestamp(r["planned_end"])
    )
    total_planned = plan["item_id"].nunique()
    crit_count = sum(1 for e in exceptions if e["severity"] == "Critical")
    warn_count = sum(1 for e in exceptions if e["severity"] == "Warning")
    ready = total_planned - sum(
        1 for e in exceptions
        if e["issue_type"] != "System item active but missing from any plan"
        and e["campaign_id"] != "SYSTEM-DETECTED"
    )
    ready = max(ready, 0)
    unplanned = sum(1 for e in exceptions if e["campaign_id"] == "SYSTEM-DETECTED")
    missing_owners = sum(1 for e in exceptions if e["issue_type"] == "Owner missing")
    html = f"""
    <div class="kpi-grid">
      <div class="kpi-card kpi-teal"><div class="kpi-label">Starting Soon</div><div class="kpi-value">{starting_soon}</div></div>
      <div class="kpi-card kpi-teal"><div class="kpi-label">Active Now</div><div class="kpi-value">{active_now}</div></div>
      <div class="kpi-card"><div class="kpi-label">Total Planned Items</div><div class="kpi-value">{total_planned}</div></div>
      <div class="kpi-card kpi-ok"><div class="kpi-label">Ready Items</div><div class="kpi-value">{ready}</div></div>
      <div class="kpi-card kpi-crit"><div class="kpi-label">Critical</div><div class="kpi-value">{crit_count}</div></div>
      <div class="kpi-card kpi-warn"><div class="kpi-label">Warnings</div><div class="kpi-value">{warn_count}</div></div>
      <div class="kpi-card kpi-grey"><div class="kpi-label">Unplanned Activity</div><div class="kpi-value">{unplanned}</div></div>
      <div class="kpi-card kpi-warn"><div class="kpi-label">Missing Owners</div><div class="kpi-value">{missing_owners}</div></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_campaign_list(campaigns_df: pd.DataFrame):
    st.subheader("Campaigns")
    for _, row in campaigns_df.iterrows():
        pct = int(row.get("readiness_pct", 0))
        crit = int(row.get("critical_count", 0))
        warn = int(row.get("warning_count", 0))
        status_color = "#059669" if crit == 0 and warn == 0 else ("#DC2626" if crit > 0 else "#D97706")
        status_label = "Ready" if crit == 0 and warn == 0 else ("Critical" if crit > 0 else "Warning")
        col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1.5, 1, 1])
        with col1:
            st.markdown(f"**{row['campaign_name']}**")
            st.caption(f"{row['campaign_source']} . {row['channel']}")
        with col2:
            st.caption(f"{row['planned_start']} - {row['planned_end']}")
        with col3:
            st.metric("Items", row["item_count"])
        with col4:
            st.metric("Readiness", f"{pct}%")
        with col5:
            st.markdown(
                f"<span style='color:{status_color};font-weight:600'>{status_label}</span> "
                f"<span style='font-size:0.8em'>({crit}c/{warn}w)</span>",
                unsafe_allow_html=True,
            )
        st.divider()


def render_exception_cards(exceptions: list[dict], view_mode: str):
    if not exceptions:
        st.info("No exceptions found. All campaign items match system state.")
        return
    st.subheader(f"Exception Cards ({len(exceptions)})")
    for exc in exceptions:
        sev = exc["severity"]
        color = SEVERITY_COLORS.get(sev, "#6B7280")
        bg = {"Critical": "#FEF2F2", "Warning": "#FFFBEB", "OK": "#F0FDF4"}.get(sev, "#F9FAFB")
        border = {"Critical": "#FECACA", "Warning": "#FDE68A", "OK": "#BBF7D0"}.get(sev, "#E5E7EB")
        html = f"""
        <div class="exception-card" style="border-left:4px solid {color}; background:{bg}; border:1px solid {border}">
          <div class="exc-header">
            <span class="exc-severity" style="background:{color}">{sev}</span>
            <span class="exc-type">{exc['issue_type']}</span>
          </div>
          <div class="exc-body">
            <div class="exc-item"><strong>{exc['item_id']}</strong> / {exc['product_name']}</div>
            <div class="exc-campaign">{exc['campaign_name']} . {exc['date_window']} . {exc['channel']}</div>
            <div class="exc-values">
              <div><span class="exc-label">Plan</span> {exc['plan_value']}</div>
              <div><span class="exc-label">System</span> {exc['system_value']}</div>
            </div>
            <div class="exc-risk"><span class="exc-label">Risk</span> {exc['risk']}</div>
            <div class="exc-owner"><span class="exc-label">Owner</span> {exc['owner']}</div>
            <div class="exc-action"><span class="exc-label">Action</span> {exc['action']}</div>
        """
        if view_mode == "Technical":
            html += f"""
            <div class="exc-tech">
              <div><span class="exc-label">Host status</span> Synthetic . Up</div>
              <div><span class="exc-label">Module status</span> {sev}</div>
              <div><span class="exc-label">Evidence source</span> Synthetic comparison engine</div>
            </div>
            """
        html += "</div></div>"
        st.markdown(html, unsafe_allow_html=True)

def render_handoff_payload(exceptions: list[dict], selected_campaign: str | None):
    st.subheader("Handoff Payload")
    teams = {
        "Pricing Team": [], "Product Data Team": [],
        "Inventory / Logistics": [], "E-commerce / Channel": [],
        "Campaign Owner": [],
    }
    for exc in exceptions:
        if selected_campaign and selected_campaign != "All" and exc["campaign_id"] != selected_campaign:
            continue
        owner = exc["owner"]
        if "Pricing" in owner:
            teams["Pricing Team"].append(exc)
        elif "Campaign" in owner or "Sales" in owner or "Local" in owner or "Mail" in owner:
            teams["Campaign Owner"].append(exc)
        elif "stock" in exc["issue_type"].lower() or "Stock" in exc["issue_type"]:
            teams["Inventory / Logistics"].append(exc)
        elif "channel" in exc["issue_type"].lower() or "visible" in exc["issue_type"].lower() or "image" in exc["issue_type"].lower() or "content" in exc["issue_type"].lower():
            teams["E-commerce / Channel"].append(exc)
        else:
            teams["Product Data Team"].append(exc)
    team_tabs = st.tabs(list(teams.keys()))
    for tab, (team, items) in zip(team_tabs, teams.items()):
        with tab:
            if not items:
                st.caption("No items for this team.")
                continue
            payload = []
            for exc in items:
                payload.append({
                    "campaign_id": exc["campaign_id"], "campaign_name": exc["campaign_name"],
                    "item_id": exc["item_id"], "issue_type": exc["issue_type"],
                    "severity": exc["severity"], "plan_value": exc["plan_value"],
                    "system_value": exc["system_value"],
                    "recommended_action": exc["action"], "owner": exc["owner"],
                    "timestamp": ANCHOR.isoformat(),
                })
            st.caption(f"{len(payload)} items")
            st.json(payload, expanded=False)


def main():
    st.set_page_config(page_title="Campaign Readiness Monitor", layout="wide")
    st.markdown(load_design_css(), unsafe_allow_html=True)
    st.markdown("""
    <div class="brand-bar">
      <span class="brand">Campaign Readiness Monitor</span>
      <span style="color:var(--ink-3);font-size:13px;font-family:var(--mono)">Goblin Manager</span>
    </div>
    """, unsafe_allow_html=True)

    plan = generate_campaign_plan()
    system = generate_system_truth()
    exceptions = compare_plan_vs_system(plan, system)
    campaigns_df = build_campaign_summary(plan, exceptions)

    with st.sidebar:
        st.markdown("### Filters")
        view_mode = st.radio("View mode", ["Business", "Technical"], horizontal=True)
        selected_campaign = st.selectbox(
            "Campaign",
            ["All"] + campaigns_df["campaign_id"].tolist(),
            format_func=lambda x: "All Campaigns" if x == "All" else
                campaigns_df[campaigns_df["campaign_id"] == x]["campaign_name"].iloc[0],
        )
        severity_filter = st.multiselect(
            "Severity", ["Critical", "Warning", "OK"],
            default=["Critical", "Warning"],
        )
        channel_filter = st.multiselect(
            "Channel", CHANNELS, default=CHANNELS,
        )

    filtered = [e for e in exceptions
                if e["severity"] in severity_filter
                and e["channel"] in channel_filter]
    if selected_campaign != "All":
        filtered = [e for e in filtered if e["campaign_id"] == selected_campaign]

    render_kpi_cards(plan, exceptions)
    st.divider()
    render_campaign_list(campaigns_df)
    st.divider()
    render_exception_cards(filtered, view_mode)
    st.divider()
    render_handoff_payload(exceptions, selected_campaign)


if __name__ == "__main__":
    main()
