import pandas as pd
import streamlit as st
from datetime import date, timedelta
import os
import json


ANCHOR = date(2026, 6, 1)
CHANNELS = ["webshop", "B2B", "mail order", "local store"]
from textwrap import dedent as _dedent


def _md(html: str) -> None:
    cleaned = "\n".join(line.lstrip() for line in html.splitlines())
    getattr(st, "markdown")(cleaned.strip(), unsafe_allow_html=True)


SEVERITY_COLORS = {"Critical": "#DC2626", "Warning": "#D97706", "OK": "#059669"}

ISSUE_CATEGORIES = ("plan", "pim", "price", "content", "stock", "channel", "owner", "unplanned", "other")


def _categorize_issue(issue_type: str) -> str:
    s = issue_type.lower()
    if "missing from any plan" in s or "active but missing" in s:
        return "unplanned"
    if "missing from system" in s or "not active in target channel" in s or "missing from pim" in s:
        return "pim"
    if "price" in s or "duplicate / conflicting" in s:
        return "price"
    if "not visible in webshop" in s or "visible" in s:
        return "channel"
    if "image" in s or "content" in s or "category" in s:
        return "content"
    if "stock" in s:
        return "stock"
    if "owner" in s:
        return "owner"
    if "duplicate campaign item" in s or "missing sku" in s or "end date" in s or "in plan" in s:
        return "plan"
    return "other"


def attach_categories(items: list[dict]) -> list[dict]:
    for e in items:
        if "issue_category" not in e:
            e["issue_category"] = _categorize_issue(e.get("issue_type", ""))
    return items


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
        {
            "campaign_id": "CAMP-001",
            "campaign_name": "Summer Launch",
            "campaign_source": "Excel plan",
            "planned_start": ANCHOR,
            "planned_end": ANCHOR + timedelta(days=13),
            "channel": "webshop",
            "item_id": "SKU-001",
            "planned_price": 19.90,
            "planned_category": "Summer Essentials",
            "planned_visibility": True,
            "planned_owner": "Alice (Campaigns)",
        },
        {
            "campaign_id": "CAMP-001",
            "campaign_name": "Summer Launch",
            "campaign_source": "Excel plan",
            "planned_start": ANCHOR,
            "planned_end": ANCHOR + timedelta(days=13),
            "channel": "webshop",
            "item_id": "SKU-002",
            "planned_price": 24.90,
            "planned_category": "Summer Essentials",
            "planned_visibility": True,
            "planned_owner": "Alice (Campaigns)",
        },
        {
            "campaign_id": "CAMP-001",
            "campaign_name": "Summer Launch",
            "campaign_source": "Excel plan",
            "planned_start": ANCHOR,
            "planned_end": ANCHOR + timedelta(days=13),
            "channel": "webshop",
            "item_id": "SKU-003",
            "planned_price": 34.50,
            "planned_category": "Summer Essentials",
            "planned_visibility": True,
            "planned_owner": "Alice (Campaigns)",
        },
        {
            "campaign_id": "CAMP-001",
            "campaign_name": "Summer Launch",
            "campaign_source": "Excel plan",
            "planned_start": ANCHOR,
            "planned_end": ANCHOR + timedelta(days=13),
            "channel": "webshop",
            "item_id": "SKU-004",
            "planned_price": 15.00,
            "planned_category": "Summer Essentials",
            "planned_visibility": True,
            "planned_owner": "Alice (Campaigns)",
        },
        {
            "campaign_id": "CAMP-001",
            "campaign_name": "Summer Launch",
            "campaign_source": "Excel plan",
            "planned_start": ANCHOR,
            "planned_end": ANCHOR + timedelta(days=13),
            "channel": "webshop",
            "item_id": "SKU-005",
            "planned_price": 9.99,
            "planned_category": "Summer Essentials",
            "planned_visibility": True,
            "planned_owner": "Alice (Campaigns)",
        },
        {
            "campaign_id": "CAMP-001",
            "campaign_name": "Summer Launch",
            "campaign_source": "Excel plan",
            "planned_start": ANCHOR,
            "planned_end": ANCHOR + timedelta(days=13),
            "channel": "webshop",
            "item_id": "SKU-006",
            "planned_price": 42.00,
            "planned_category": "Summer Essentials",
            "planned_visibility": True,
            "planned_owner": "Alice (Campaigns)",
        },
        {
            "campaign_id": "CAMP-001",
            "campaign_name": "Summer Launch",
            "campaign_source": "Excel plan",
            "planned_start": ANCHOR,
            "planned_end": ANCHOR + timedelta(days=13),
            "channel": "webshop",
            "item_id": "SKU-007",
            "planned_price": 29.90,
            "planned_category": "Summer Essentials",
            "planned_visibility": True,
            "planned_owner": "Alice (Campaigns)",
        },
        {
            "campaign_id": "CAMP-002",
            "campaign_name": "B2B Q3 Price List",
            "campaign_source": "SharePoint upload",
            "planned_start": ANCHOR - timedelta(days=5),
            "planned_end": ANCHOR + timedelta(days=25),
            "channel": "B2B",
            "item_id": "SKU-010",
            "planned_price": 89.00,
            "planned_category": "Bulk Hardware",
            "planned_visibility": True,
            "planned_owner": "Bob (B2B Sales)",
        },
        {
            "campaign_id": "CAMP-002",
            "campaign_name": "B2B Q3 Price List",
            "campaign_source": "SharePoint upload",
            "planned_start": ANCHOR - timedelta(days=5),
            "planned_end": ANCHOR + timedelta(days=25),
            "channel": "B2B",
            "item_id": "SKU-011",
            "planned_price": 120.00,
            "planned_category": "Bulk Hardware",
            "planned_visibility": True,
            "planned_owner": "Bob (B2B Sales)",
        },
        {
            "campaign_id": "CAMP-002",
            "campaign_name": "B2B Q3 Price List",
            "campaign_source": "SharePoint upload",
            "planned_start": ANCHOR - timedelta(days=5),
            "planned_end": ANCHOR + timedelta(days=25),
            "channel": "B2B",
            "item_id": "SKU-012",
            "planned_price": 55.00,
            "planned_category": "Bulk Hardware",
            "planned_visibility": True,
            "planned_owner": "Bob (B2B Sales)",
        },
        {
            "campaign_id": "CAMP-002",
            "campaign_name": "B2B Q3 Price List",
            "campaign_source": "SharePoint upload",
            "planned_start": ANCHOR - timedelta(days=5),
            "planned_end": ANCHOR + timedelta(days=25),
            "channel": "B2B",
            "item_id": "SKU-013",
            "planned_price": 210.00,
            "planned_category": "Bulk Hardware",
            "planned_visibility": True,
            "planned_owner": "",
        },
        {
            "campaign_id": "CAMP-003",
            "campaign_name": "Local Store Promo",
            "campaign_source": "Manual plan",
            "planned_start": ANCHOR + timedelta(days=2),
            "planned_end": ANCHOR + timedelta(days=8),
            "channel": "local store",
            "item_id": "SKU-014",
            "planned_price": 7.50,
            "planned_category": "Impulse Buys",
            "planned_visibility": True,
            "planned_owner": "Carol (Local)",
        },
        {
            "campaign_id": "CAMP-003",
            "campaign_name": "Local Store Promo",
            "campaign_source": "Manual plan",
            "planned_start": ANCHOR + timedelta(days=2),
            "planned_end": ANCHOR + timedelta(days=8),
            "channel": "local store",
            "item_id": "SKU-015",
            "planned_price": 12.00,
            "planned_category": "Impulse Buys",
            "planned_visibility": True,
            "planned_owner": "Carol (Local)",
        },
        {
            "campaign_id": "CAMP-003",
            "campaign_name": "Local Store Promo",
            "campaign_source": "Manual plan",
            "planned_start": ANCHOR + timedelta(days=2),
            "planned_end": ANCHOR + timedelta(days=8),
            "channel": "local store",
            "item_id": "SKU-016",
            "planned_price": 3.99,
            "planned_category": "Impulse Buys",
            "planned_visibility": True,
            "planned_owner": "Carol (Local)",
        },
        {
            "campaign_id": "CAMP-004",
            "campaign_name": "Mail Order June",
            "campaign_source": "Email attachment",
            "planned_start": ANCHOR + timedelta(days=10),
            "planned_end": ANCHOR + timedelta(days=30),
            "channel": "mail order",
            "item_id": "SKU-020",
            "planned_price": 64.00,
            "planned_category": "Home & Garden",
            "planned_visibility": True,
            "planned_owner": "Dave (Mail Order)",
        },
        {
            "campaign_id": "CAMP-004",
            "campaign_name": "Mail Order June",
            "campaign_source": "Email attachment",
            "planned_start": ANCHOR + timedelta(days=10),
            "planned_end": ANCHOR + timedelta(days=30),
            "channel": "mail order",
            "item_id": "SKU-021",
            "planned_price": 38.00,
            "planned_category": "Home & Garden",
            "planned_visibility": True,
            "planned_owner": "Dave (Mail Order)",
        },
    ]
    return pd.DataFrame(rows)


def generate_system_truth() -> pd.DataFrame:
    rows = [
        {
            "item_id": "SKU-001",
            "product_name": "Beach Towel XL",
            "product_exists": True,
            "master_category": "Summer Essentials",
            "system_channel": "webshop",
            "system_price": 19.90,
            "price_start": ANCHOR,
            "price_end": ANCHOR + timedelta(days=13),
            "webshop_visible": True,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 500,
            "forecast_demand": 300,
            "stock_risk": "low",
            "owner": "Pricing Team",
        },
        {
            "item_id": "SKU-002",
            "product_name": "Sunglasses Pro",
            "product_exists": True,
            "master_category": "Summer Essentials",
            "system_channel": "webshop",
            "system_price": 27.90,
            "price_start": ANCHOR,
            "price_end": ANCHOR + timedelta(days=13),
            "webshop_visible": True,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 200,
            "forecast_demand": 250,
            "stock_risk": "medium",
            "owner": "Pricing Team",
        },
        {
            "item_id": "SKU-003",
            "product_name": "Cooler Bag 20L",
            "product_exists": True,
            "master_category": "Summer Essentials",
            "system_channel": "webshop",
            "system_price": 34.50,
            "price_start": ANCHOR + timedelta(days=2),
            "price_end": ANCHOR + timedelta(days=13),
            "webshop_visible": True,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 150,
            "forecast_demand": 120,
            "stock_risk": "low",
            "owner": "Pricing Team",
        },
        {
            "item_id": "SKU-004",
            "product_name": "Flip Flops Basic",
            "product_exists": True,
            "master_category": "Summer Essentials",
            "system_channel": "webshop",
            "system_price": 15.00,
            "price_start": ANCHOR,
            "price_end": ANCHOR + timedelta(days=10),
            "webshop_visible": True,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 800,
            "forecast_demand": 600,
            "stock_risk": "low",
            "owner": "Pricing Team",
        },
        {
            "item_id": "SKU-005",
            "product_name": "Water Bottle 500ml",
            "product_exists": False,
            "master_category": "",
            "system_channel": "",
            "system_price": 0,
            "price_start": None,
            "price_end": None,
            "webshop_visible": False,
            "content_ready": False,
            "image_ready": False,
            "stock_on_hand": 0,
            "forecast_demand": 0,
            "stock_risk": "N/A",
            "owner": "",
        },
        {
            "item_id": "SKU-006",
            "product_name": "Sun Hat Wide Brim",
            "product_exists": True,
            "master_category": "Accessories",
            "system_channel": "webshop",
            "system_price": 42.00,
            "price_start": ANCHOR,
            "price_end": ANCHOR + timedelta(days=13),
            "webshop_visible": True,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 100,
            "forecast_demand": 180,
            "stock_risk": "high",
            "owner": "Pricing Team",
        },
        {
            "item_id": "SKU-007",
            "product_name": "Picnic Blanket",
            "product_exists": True,
            "master_category": "Summer Essentials",
            "system_channel": "webshop",
            "system_price": 29.90,
            "price_start": ANCHOR,
            "price_end": ANCHOR + timedelta(days=13),
            "webshop_visible": False,
            "content_ready": True,
            "image_ready": False,
            "stock_on_hand": 60,
            "forecast_demand": 100,
            "stock_risk": "high",
            "owner": "Pricing Team",
        },
        {
            "item_id": "SKU-010",
            "product_name": "Industrial Drill Kit",
            "product_exists": True,
            "master_category": "Bulk Hardware",
            "system_channel": "B2B",
            "system_price": 89.00,
            "price_start": ANCHOR - timedelta(days=5),
            "price_end": ANCHOR + timedelta(days=25),
            "webshop_visible": False,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 45,
            "forecast_demand": 40,
            "stock_risk": "low",
            "owner": "B2B Pricing",
        },
        {
            "item_id": "SKU-011",
            "product_name": "Steel Fastener Set",
            "product_exists": True,
            "master_category": "Bulk Hardware",
            "system_channel": "B2B",
            "system_price": 135.00,
            "price_start": ANCHOR - timedelta(days=5),
            "price_end": ANCHOR + timedelta(days=25),
            "webshop_visible": False,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 200,
            "forecast_demand": 150,
            "stock_risk": "low",
            "owner": "B2B Pricing",
        },
        {
            "item_id": "SKU-012",
            "product_name": "Safety Goggles Pro",
            "product_exists": True,
            "master_category": "Bulk Hardware",
            "system_channel": "B2B",
            "system_price": 55.00,
            "price_start": ANCHOR - timedelta(days=5),
            "price_end": ANCHOR + timedelta(days=25),
            "webshop_visible": False,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 300,
            "forecast_demand": 100,
            "stock_risk": "low",
            "owner": "B2B Pricing",
        },
        {
            "item_id": "SKU-012",
            "product_name": "Safety Goggles Pro",
            "product_exists": True,
            "master_category": "Bulk Hardware",
            "system_channel": "webshop",
            "system_price": 59.00,
            "price_start": ANCHOR - timedelta(days=5),
            "price_end": ANCHOR + timedelta(days=25),
            "webshop_visible": True,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 300,
            "forecast_demand": 100,
            "stock_risk": "low",
            "owner": "B2B Pricing",
        },
        {
            "item_id": "SKU-013",
            "product_name": "Hydraulic Pump 2T",
            "product_exists": True,
            "master_category": "Bulk Hardware",
            "system_channel": "B2B",
            "system_price": 210.00,
            "price_start": ANCHOR - timedelta(days=5),
            "price_end": ANCHOR + timedelta(days=25),
            "webshop_visible": False,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 12,
            "forecast_demand": 15,
            "stock_risk": "medium",
            "owner": "",
        },
        {
            "item_id": "SKU-014",
            "product_name": "Chewing Gum Pack",
            "product_exists": True,
            "master_category": "Impulse Buys",
            "system_channel": "local store",
            "system_price": 7.50,
            "price_start": ANCHOR + timedelta(days=2),
            "price_end": ANCHOR + timedelta(days=8),
            "webshop_visible": False,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 2000,
            "forecast_demand": 1500,
            "stock_risk": "low",
            "owner": "Local Ops",
        },
        {
            "item_id": "SKU-015",
            "product_name": "Chocolate Bar 100g",
            "product_exists": True,
            "master_category": "Impulse Buys",
            "system_channel": "local store",
            "system_price": 0,
            "price_start": None,
            "price_end": None,
            "webshop_visible": False,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 500,
            "forecast_demand": 400,
            "stock_risk": "low",
            "owner": "Local Ops",
        },
        {
            "item_id": "SKU-016",
            "product_name": "Energy Drink Can",
            "product_exists": True,
            "master_category": "Beverages",
            "system_channel": "local store",
            "system_price": 3.99,
            "price_start": ANCHOR + timedelta(days=2),
            "price_end": ANCHOR + timedelta(days=8),
            "webshop_visible": False,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 1000,
            "forecast_demand": 800,
            "stock_risk": "low",
            "owner": "Local Ops",
        },
        {
            "item_id": "SKU-020",
            "product_name": "Garden Hose 15m",
            "product_exists": True,
            "master_category": "Home & Garden",
            "system_channel": "mail order",
            "system_price": 64.00,
            "price_start": ANCHOR + timedelta(days=10),
            "price_end": ANCHOR + timedelta(days=30),
            "webshop_visible": False,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 80,
            "forecast_demand": 90,
            "stock_risk": "medium",
            "owner": "Mail Order Team",
        },
        {
            "item_id": "SKU-021",
            "product_name": "Plant Pot Set 3pk",
            "product_exists": True,
            "master_category": "Home & Garden",
            "system_channel": "mail order",
            "system_price": 38.00,
            "price_start": ANCHOR + timedelta(days=10),
            "price_end": ANCHOR + timedelta(days=30),
            "webshop_visible": False,
            "content_ready": False,
            "image_ready": False,
            "stock_on_hand": 30,
            "forecast_demand": 60,
            "stock_risk": "high",
            "owner": "Mail Order Team",
        },
        {
            "item_id": "SKU-099",
            "product_name": "LED Lantern Camping",
            "product_exists": True,
            "master_category": "Outdoor",
            "system_channel": "webshop",
            "system_price": 22.00,
            "price_start": ANCHOR,
            "price_end": ANCHOR + timedelta(days=10),
            "webshop_visible": True,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 120,
            "forecast_demand": 100,
            "stock_risk": "low",
            "owner": "Pricing Team",
        },
        {
            "item_id": "SKU-100",
            "product_name": "Portable Speaker BT",
            "product_exists": True,
            "master_category": "Electronics",
            "system_channel": "local store",
            "system_price": 45.00,
            "price_start": ANCHOR + timedelta(days=2),
            "price_end": ANCHOR + timedelta(days=8),
            "webshop_visible": False,
            "content_ready": True,
            "image_ready": True,
            "stock_on_hand": 25,
            "forecast_demand": 40,
            "stock_risk": "high",
            "owner": "",
        },
    ]
    df = pd.DataFrame(rows)
    for col in ["price_start", "price_end"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def check_plan_quality(plan: pd.DataFrame) -> list[dict]:
    issues = []
    for campaign_id, group in plan.groupby("campaign_id"):
        campaign_name = group["campaign_name"].iloc[0]
        campaign_source = group["campaign_source"].iloc[0]
        p_start = pd.Timestamp(group["planned_start"].iloc[0])
        p_end = pd.Timestamp(group["planned_end"].iloc[0])
        channel = group["channel"].iloc[0]

        if p_end < p_start:
            issues.append(
                {
                    "campaign_id": campaign_id,
                    "campaign_name": campaign_name,
                    "campaign_source": campaign_source,
                    "channel": channel,
                    "item_id": "N/A",
                    "product_name": "Campaign-level",
                    "issue_type": "End date before start date",
                    "severity": "Critical",
                    "plan_value": f"Start: {p_start.date()}, End: {p_end.date()}",
                    "system_value": "N/A",
                    "risk": "Campaign window is inverted, impossible to execute",
                    "owner": "Campaign Owner",
                    "action": "Correct campaign dates in plan",
                    "date_window": f"{p_start.date()} - {p_end.date()}",
                    "issue_origin": "Plan issue",
                }
            )

        seen_items = {}
        for _, row in group.iterrows():
            item_id = row["item_id"]
            planned_price = row["planned_price"]
            planned_category = row["planned_category"]
            planned_owner = row["planned_owner"]

            if not item_id or str(item_id).strip() == "":
                issues.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": "MISSING",
                        "product_name": "Unknown",
                        "issue_type": "Missing SKU in plan",
                        "severity": "Critical",
                        "plan_value": "No item ID provided",
                        "system_value": "N/A",
                        "risk": "Untrackable campaign line, cannot verify readiness",
                        "owner": planned_owner or "Unassigned",
                        "action": "Add valid SKU or remove line from plan",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "Plan issue",
                    }
                )
                continue

            if item_id in seen_items:
                issues.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": "Duplicate entry",
                        "issue_type": "Duplicate campaign item",
                        "severity": "Warning",
                        "plan_value": f"Appears {seen_items[item_id] + 1} times in plan",
                        "system_value": "N/A",
                        "risk": "Conflicting or double-counted campaign line",
                        "owner": planned_owner or "Unassigned",
                        "action": "Deduplicate campaign plan entries",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "Plan issue",
                    }
                )
            seen_items[item_id] = seen_items.get(item_id, 0) + 1

            if planned_price is None or planned_price == 0:
                issues.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": "Plan entry",
                        "issue_type": "Missing or zero price in plan",
                        "severity": "Critical",
                        "plan_value": f"Price: {planned_price}",
                        "system_value": "N/A",
                        "risk": "Cannot validate pricing, possible revenue loss",
                        "owner": planned_owner or "Unassigned",
                        "action": "Set valid campaign price in plan",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "Plan issue",
                    }
                )

            if not planned_owner or str(planned_owner).strip() == "":
                issues.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": "Plan entry",
                        "issue_type": "Missing owner in plan",
                        "severity": "Warning",
                        "plan_value": "No owner assigned",
                        "system_value": "N/A",
                        "risk": "No one accountable for this campaign item",
                        "owner": "Unassigned",
                        "action": "Assign owner in campaign plan",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "Plan issue",
                    }
                )

            if planned_category and str(planned_category).strip() == "":
                issues.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": "Plan entry",
                        "issue_type": "Missing category in plan",
                        "severity": "Warning",
                        "plan_value": "No category assigned",
                        "system_value": "N/A",
                        "risk": "Item may appear in wrong navigation or campaign section",
                        "owner": planned_owner or "Unassigned",
                        "action": "Assign category in campaign plan",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "Plan issue",
                    }
                )

    return issues


def compare_plan_vs_system(plan: pd.DataFrame, system: pd.DataFrame) -> list[dict]:
    exceptions = []
    today = pd.Timestamp(ANCHOR)
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
                exceptions.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": "Unknown",
                        "issue_type": "Planned item missing from system",
                        "severity": "Critical",
                        "plan_value": f"Price {planned_price:.2f}, Category: {planned_category}",
                        "system_value": "Not found in any system",
                        "risk": "Customer-facing item unavailable during campaign",
                        "owner": planned_owner or "Unassigned",
                        "action": "Create item in system or remove from campaign plan",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "System issue",
                    }
                )
                continue
            if sys_channel_rows.empty:
                other_channels = sys_rows["system_channel"].unique().tolist()
                exceptions.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": sys_rows["product_name"].iloc[0],
                        "issue_type": "Item not active in target channel",
                        "severity": "Critical",
                        "plan_value": f"Channel: {channel}",
                        "system_value": f"Found in: {', '.join(other_channels)}",
                        "risk": "Campaign item not visible in planned channel",
                        "owner": planned_owner
                        or sys_rows["owner"].iloc[0]
                        or "Unassigned",
                        "action": "Add item to target channel or reassign campaign",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "System issue",
                    }
                )
                continue
            sys_row = sys_channel_rows.iloc[0]
            product_name = sys_row["product_name"]
            sys_price = sys_row["system_price"]
            price_s = sys_row["price_start"]
            price_e = sys_row["price_end"]
            sys_owner = sys_row["owner"]
            active_sys_rows = sys_rows[
                (sys_rows["system_price"] > 0) & sys_rows["price_start"].notna()
            ]
            if len(active_sys_rows) >= 2:
                price_summary = " · ".join(
                    f"{r['system_channel']} {r['system_price']:.2f} €"
                    for _, r in active_sys_rows.iterrows()
                )
                if len(sys_channel_rows) > 1:
                    sys_value = f"{len(sys_channel_rows)} price records in {channel}"
                else:
                    sys_value = f"Active in {len(active_sys_rows)} channels: {price_summary}"
                exceptions.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": product_name,
                        "issue_type": "Duplicate / conflicting active prices",
                        "severity": "Critical",
                        "plan_value": f"Plan: {channel} at {planned_price:.2f} €",
                        "system_value": sys_value,
                        "risk": "Multiple active prices cause checkout errors or wrong-channel exposure",
                        "owner": planned_owner or sys_owner or "Unassigned",
                        "action": "Keep one canonical price per channel; remove stale records",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "System issue",
                    }
                )
            if pd.isna(price_s) or sys_price == 0:
                exceptions.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": product_name,
                        "issue_type": "Campaign price missing in system",
                        "severity": "Critical",
                        "plan_value": f"Price {planned_price:.2f}",
                        "system_value": "No price configured",
                        "risk": "Customer-facing price unavailable during campaign",
                        "owner": planned_owner or sys_owner or "Unassigned",
                        "action": "Create price record / exclude item / mark reviewed",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "System issue",
                    }
                )
                continue
            if abs(sys_price - planned_price) > planned_price * 0.01:
                exceptions.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": product_name,
                        "issue_type": "Price mismatch",
                        "severity": "Warning",
                        "plan_value": f"Plan: {planned_price:.2f}",
                        "system_value": f"System: {sys_price:.2f}",
                        "risk": "Wrong price visible to customers",
                        "owner": planned_owner or sys_owner or "Unassigned",
                        "action": "Align system price with campaign plan or update plan",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "Cross-system mismatch",
                    }
                )
            if pd.notna(price_s) and price_s > p_start:
                exceptions.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": product_name,
                        "issue_type": "Price starts too late",
                        "severity": "Warning",
                        "plan_value": f"Campaign starts: {p_start.date()}",
                        "system_value": f"System price starts: {price_s.date()}",
                        "risk": f"Wrong price visible for first {(price_s - p_start).days} campaign days",
                        "owner": planned_owner or sys_owner or "Unassigned",
                        "action": "Fix start date / accept exception",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "Cross-system mismatch",
                    }
                )
            if pd.notna(price_e) and price_e < p_end:
                exceptions.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": product_name,
                        "issue_type": "Price ends too early",
                        "severity": "Warning",
                        "plan_value": f"Campaign ends: {p_end.date()}",
                        "system_value": f"System price ends: {price_e.date()}",
                        "risk": "Price reverts before campaign ends",
                        "owner": planned_owner or sys_owner or "Unassigned",
                        "action": "Extend price validity to match campaign end",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "Cross-system mismatch",
                    }
                )
            if planned_category and sys_row["master_category"] != planned_category:
                exceptions.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": product_name,
                        "issue_type": "Wrong category / campaign placement",
                        "severity": "Warning",
                        "plan_value": f"Plan: {planned_category}",
                        "system_value": f"System: {sys_row['master_category']}",
                        "risk": "Item may appear in wrong navigation or campaign section",
                        "owner": planned_owner or sys_owner or "Unassigned",
                        "action": "Update master category or campaign placement",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "Cross-system mismatch",
                    }
                )
            if channel == "webshop":
                if not sys_row["webshop_visible"]:
                    exceptions.append(
                        {
                            "campaign_id": campaign_id,
                            "campaign_name": campaign_name,
                            "campaign_source": campaign_source,
                            "channel": channel,
                            "item_id": item_id,
                            "product_name": product_name,
                            "issue_type": "Item not visible in webshop",
                            "severity": "Critical",
                            "plan_value": "Planned: visible",
                            "system_value": "System: hidden",
                            "risk": "Campaign item not findable by customers",
                            "owner": planned_owner or sys_owner or "Unassigned",
                            "action": "Enable webshop visibility flag",
                            "date_window": f"{p_start.date()} - {p_end.date()}",
                            "issue_origin": "System issue",
                        }
                    )
                if not sys_row["image_ready"] or not sys_row["content_ready"]:
                    missing = []
                    if not sys_row["image_ready"]:
                        missing.append("image")
                    if not sys_row["content_ready"]:
                        missing.append("content")
                    exceptions.append(
                        {
                            "campaign_id": campaign_id,
                            "campaign_name": campaign_name,
                            "campaign_source": campaign_source,
                            "channel": channel,
                            "item_id": item_id,
                            "product_name": product_name,
                            "issue_type": "Missing image / content",
                            "severity": "Warning",
                            "plan_value": "Expected: ready",
                            "system_value": f"Missing: {', '.join(missing)}",
                            "risk": "Poor customer experience, lower conversion",
                            "owner": planned_owner or sys_owner or "Unassigned",
                            "action": "Upload missing assets before campaign start",
                            "date_window": f"{p_start.date()} - {p_end.date()}",
                            "issue_origin": "System issue",
                        }
                    )
            stock = sys_row["stock_on_hand"]
            forecast = sys_row["forecast_demand"]
            if stock < forecast:
                exceptions.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": product_name,
                        "issue_type": "Stock below forecast demand",
                        "severity": "Warning",
                        "plan_value": f"Forecast: {forecast}",
                        "system_value": f"Stock: {stock}",
                        "risk": f"Potential stockout, risk: {sys_row['stock_risk']}",
                        "owner": planned_owner or sys_owner or "Unassigned",
                        "action": "Replenish stock / adjust forecast / reduce campaign scope",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "System issue",
                    }
                )
            if not planned_owner and not sys_owner:
                exceptions.append(
                    {
                        "campaign_id": campaign_id,
                        "campaign_name": campaign_name,
                        "campaign_source": campaign_source,
                        "channel": channel,
                        "item_id": item_id,
                        "product_name": product_name,
                        "issue_type": "Owner missing",
                        "severity": "Warning",
                        "plan_value": "No plan owner",
                        "system_value": "No system owner",
                        "risk": "No one accountable for resolution",
                        "owner": "Unassigned",
                        "action": "Assign owner in plan or system",
                        "date_window": f"{p_start.date()} - {p_end.date()}",
                        "issue_origin": "Cross-system mismatch",
                    }
                )
    system_active = system[system["price_start"].notna() & (system["system_price"] > 0)]
    for _, srow in system_active.iterrows():
        sid = srow["item_id"]
        if sid not in planned_ids:
            s_start = srow["price_start"]
            s_end = srow["price_end"]
            if pd.notna(s_start) and pd.notna(s_end):
                exceptions.append(
                    {
                        "campaign_id": "SYSTEM-DETECTED",
                        "campaign_name": "Unplanned active campaign price",
                        "campaign_source": "System detected",
                        "channel": srow["system_channel"],
                        "item_id": sid,
                        "product_name": srow["product_name"],
                        "issue_type": "System item active but missing from any plan",
                        "severity": "Warning",
                        "plan_value": "Not in any campaign plan",
                        "system_value": f"Active price {srow['system_price']:.2f} in {srow['system_channel']}",
                        "risk": "Unplanned customer-facing promotion or stale price",
                        "owner": srow["owner"] or "Unassigned",
                        "action": "Add to plan / remove price / investigate",
                        "date_window": f"{s_start.date()} - {s_end.date()}",
                        "issue_origin": "Inferred/unplanned activity",
                    }
                )
    return exceptions


def build_campaign_summary(plan: pd.DataFrame, exceptions: list[dict]) -> pd.DataFrame:
    campaigns = (
        plan.groupby("campaign_id")
        .agg(
            campaign_name=("campaign_name", "first"),
            campaign_source=("campaign_source", "first"),
            planned_start=("planned_start", "first"),
            planned_end=("planned_end", "first"),
            channel=("channel", "first"),
            item_count=("item_id", "nunique"),
        )
        .reset_index()
    )
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


SEVERITY_COLORS = {"Critical": "#C7372F", "Warning": "#A55B0B", "OK": "#138A57"}
SEVERITY_ORDER = {"Critical": 0, "Warning": 1, "OK": 2}
CAMPAIGN_SOURCE_SHORT = {
    "Excel plan": "Excel",
    "SharePoint upload": "SharePoint",
    "Manual plan": "Manual",
    "Email attachment": "Email",
    "System detected": "System",
}


def _campaign_slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def _channel_short(ch: str) -> str:
    return {"webshop": "Webshop", "B2B": "B2B", "mail order": "Mail order", "local store": "Local store"}.get(ch, ch)


def _days_to(target: date) -> float:
    return (pd.Timestamp(target) - pd.Timestamp(ANCHOR)).total_seconds() / 86400.0


def _format_days(days: float, end_date: date | None = None) -> tuple[str, str]:
    if days > 0:
        return (f"{days:.1f}d", "until start")
    if end_date is not None and pd.Timestamp(ANCHOR) <= pd.Timestamp(end_date):
        return ("live", "active now")
    return ("ended", "past window")


def compute_pipeline_stages(plan: pd.DataFrame, system: pd.DataFrame, exceptions: list[dict], campaign_id: str | None) -> list[dict]:
    if campaign_id and campaign_id != "ALL":
        scope_plan = plan[plan["campaign_id"] == campaign_id]
        scope_exc = [e for e in exceptions if e["campaign_id"] == campaign_id]
    else:
        scope_plan = plan
        scope_exc = exceptions
    total = scope_plan["item_id"].nunique() if not scope_plan.empty else 0

    def _count_cat(*cats: str) -> tuple[int, int]:
        cat_set = set(cats)
        crit = sum(1 for e in scope_exc if e.get("issue_category") in cat_set and e["severity"] == "Critical")
        warn = sum(1 for e in scope_exc if e.get("issue_category") in cat_set and e["severity"] == "Warning")
        return crit, warn

    pim_crit, pim_warn = _count_cat("pim")
    price_crit, price_warn = _count_cat("price")
    content_crit, content_warn = _count_cat("content")
    stock_crit, stock_warn = _count_cat("stock")
    channel_crit, channel_warn = _count_cat("channel")

    def _status(crit: int, warn: int) -> str:
        if crit > 0:
            return "crit"
        if warn > 0:
            return "warn"
        return "ok"

    def _stage(label: str, glyph: str, ok: int, crit: int, warn: int, hint: str) -> dict:
        return {
            "label": label,
            "glyph": glyph,
            "ok": ok,
            "of": total,
            "crit": crit,
            "warn": warn,
            "status": _status(crit, warn),
            "hint": hint,
        }

    svg_plan = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" width="16" height="16"><rect x="3" y="3.5" width="10" height="9" rx="1.5"/><path d="M3 7h10M7 3.5v9"/></svg>'
    svg_pim = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" width="16" height="16"><path d="M3 6l5-3 5 3v4l-5 3-5-3z"/><path d="M3 6l5 3 5-3M8 9v4"/></svg>'
    svg_price = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" width="16" height="16"><circle cx="8" cy="8" r="5.5"/><path d="M8 4.5v3.5l2.5 1.5"/></svg>'
    svg_content = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" width="16" height="16"><rect x="2.5" y="4" width="11" height="8" rx="1"/><path d="M5 4V2.5h6V4M5 8h6"/></svg>'
    svg_inventory = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" width="16" height="16"><path d="M3 5l5-2.5L13 5v6L8 13.5 3 11z"/><path d="M3 5l5 2.5L13 5M8 7.5v6"/></svg>'
    svg_channel = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" width="16" height="16"><circle cx="8" cy="8" r="5.5"/><path d="M2.5 8h11M8 2.5c2 2 2 9 0 11M8 2.5c-2 2-2 9 0 11"/></svg>'
    stages = [
        _stage("01 · Plan", svg_plan, total, 0, 0, "all logged"),
        _stage("02 · Product (PIM)", svg_pim, max(total - pim_crit, 0), pim_crit, pim_warn,
               f"{pim_crit} missing from PIM" if pim_crit else "all items found"),
        _stage("03 · Pricing", svg_price, max(total - price_crit - price_warn, 0), price_crit, price_warn,
               f"{price_crit + price_warn} pricing issues" if (price_crit + price_warn) else "prices aligned"),
        _stage("04 · Content", svg_content, max(total - content_crit - content_warn, 0), content_crit, content_warn,
               f"{content_crit + content_warn} content gaps" if (content_crit + content_warn) else "ready"),
        _stage("05 · Inventory", svg_inventory, max(total - stock_crit - stock_warn, 0), stock_crit, stock_warn,
               f"{stock_crit + stock_warn} below forecast" if (stock_crit + stock_warn) else "stock ok"),
        _stage("06 · Channel", svg_channel, max(total - channel_crit - channel_warn, 0), channel_crit, channel_warn,
               f"{channel_crit + channel_warn} channel issues" if (channel_crit + channel_warn) else "live"),
    ]
    return stages


# ============= top bar =============
def render_topbar(selected_slug: str, view_mode: str) -> str:
    crumb = f'<span class="cur">{selected_slug}</span>'
    sync_text = f"Synced just now · {ANCHOR.strftime('%b %d, %Y')}"
    html = f"""
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark"></span>
        <span class="brand-name">Campaign Readiness</span>
        <span class="brand-tag">Ops · v2</span>
      </div>
      <div class="crumbs">
        <span>workspace</span><span class="sep">/</span>
        <span>operations</span><span class="sep">/</span>
        {crumb}
      </div>
      <div class="top-spacer"></div>
      <div class="sync-pill"><span class="pulse"></span>{sync_text}</div>
      <div class="topbar-view-anchor"></div>
    </header>
    """
    _md(html)
    # Functional view-mode toggle, rendered just below the visual topbar
    cols = st.columns([10, 2])
    with cols[1]:
        new_mode = st.segmented_control(
            "View",
            options=["Business", "Technical"],
            default=view_mode,
            key="view_mode_toggle",
            label_visibility="collapsed",
        )
    if new_mode and new_mode != view_mode:
        st.session_state.view_mode = new_mode
        st.rerun()
    return new_mode or view_mode


# ============= inspector header =============
def render_inspector_all(plan: pd.DataFrame, campaigns_df: pd.DataFrame, exceptions: list[dict]):
    n_campaigns = len(campaigns_df)
    total_items = plan["item_id"].nunique()
    crit = sum(1 for e in exceptions if e["severity"] == "Critical")
    warn = sum(1 for e in exceptions if e["severity"] == "Warning")
    if crit > 0:
        status_color = "var(--red)"
        status_text = f"● {crit} critical issues across the portfolio"
    elif warn > 0:
        status_color = "var(--amber)"
        status_text = f"● {warn} warnings, no criticals"
    else:
        status_color = "var(--green)"
        status_text = "● All campaigns ready"
    first_start = pd.Timestamp(campaigns_df["planned_start"].min()).date()
    last_end = pd.Timestamp(campaigns_df["planned_end"].max()).date()
    html = f"""
    <section class="inspector">
      <div class="insp-left">
        <div class="insp-eyebrow">
          <span>ALL</span><span class="dot"></span>
          <span>Portfolio view</span><span class="dot"></span>
          <span>{ANCHOR.strftime('%a %b %d, %Y')}</span>
        </div>
        <h1 class="insp-title">
          All campaigns
          <span class="id">{n_campaigns} campaigns</span>
        </h1>
        <div class="insp-meta">
          <span><label>Window</label>{first_start.strftime('%b %d')} → {last_end.strftime('%b %d')}</span>
          <span><label>Items</label>{total_items} SKUs</span>
          <span><label>Status</label><span style="color:{status_color};font-weight:500">{status_text}</span></span>
        </div>
      </div>
    </section>
    """
    _md(html)


def render_inspector(campaign_row, exceptions: list[dict]):
    cid = campaign_row["campaign_id"]
    crit = int(campaign_row.get("critical_count", 0))
    warn = int(campaign_row.get("warning_count", 0))
    days_left = _days_to(campaign_row["planned_start"])
    p_start = pd.Timestamp(campaign_row["planned_start"]).date()
    p_end = pd.Timestamp(campaign_row["planned_end"]).date()
    if crit > 0:
        status_color = "var(--red)"
        if days_left > 0:
            status_text = f"● Critical · {days_left:.0f} days to launch"
        else:
            status_text = f"● Critical · running now"
    elif warn > 0:
        status_color = "var(--amber)"
        status_text = f"● Needs attention · {warn} warnings"
    else:
        status_color = "var(--green)"
        status_text = "● Ready"
    item_count = int(campaign_row["item_count"])
    owner_field = "Mixed owners"
    c_exc = [e for e in exceptions if e["campaign_id"] == cid]
    if c_exc:
        owners = [e.get("owner", "") for e in c_exc if e.get("owner")]
        if owners:
            owner_field = max(set(owners), key=owners.count)
    src = campaign_row["campaign_source"]
    html = f"""
    <section class="inspector">
      <div class="insp-left">
        <div class="insp-eyebrow">
          <span>{cid}</span><span class="dot"></span>
          <span>{src}</span><span class="dot"></span>
          <span>{ANCHOR.strftime('%a %b %d, %Y')}</span>
        </div>
        <h1 class="insp-title">
          {campaign_row['campaign_name']}
          <span class="id">{_channel_short(campaign_row['channel'])}</span>
        </h1>
        <div class="insp-meta">
          <span><label>Window</label>{p_start.strftime('%b %d')} → {p_end.strftime('%b %d')}</span>
          <span><label>Items</label>{item_count} SKUs</span>
          <span><label>Owner</label>{owner_field}</span>
          <span><label>Status</label><span style="color:{status_color};font-weight:500">{status_text}</span></span>
        </div>
      </div>
    </section>
    """
    _md(html)


# ============= pipeline =============
def render_pipeline(plan: pd.DataFrame, system: pd.DataFrame, exceptions: list[dict], campaign_id: str):
    stages = compute_pipeline_stages(plan, system, exceptions, campaign_id)
    total = stages[0]["of"]
    total_crit = sum(s["crit"] for s in stages[1:])
    total_warn = sum(s["warn"] for s in stages[1:])
    total_exc = total_crit + total_warn
    ready_count = max(total - total_exc, 0)
    scope_label = campaign_id if campaign_id and campaign_id != "ALL" else "All campaigns"

    stage_html_parts = []
    for stage in stages:
        node_cls = stage["status"]
        badge_html = ""
        badge_total = stage["crit"] + stage["warn"]
        if badge_total > 0:
            badge_html = f'<span class="badge">{badge_total}</span>'
        rows = []
        if stage["crit"] > 0:
            rows.append(f'<div class="row"><span class="d crit"></span>{stage["crit"]} critical</div>')
        if stage["warn"] > 0:
            rows.append(f'<div class="row"><span class="d warn"></span>{stage["warn"]} warning</div>')
        if not rows:
            rows.append(f'<div class="row"><span class="d ok"></span>{stage["hint"]}</div>')
        rows_html = "".join(rows)
        stage_html_parts.append(f"""
        <div class="pipe-stage">
          <span class="pipe-node {node_cls}">{stage['glyph']}{badge_html}</span>
          <span class="stage-lbl">{stage['label']}</span>
          <span class="stage-count">{stage['ok']}<span class="of"> / {stage['of']}</span></span>
          <div class="stage-status">{rows_html}</div>
        </div>
        """)
    html = f"""
    <div class="pipeline">
      <div class="pipe-head">
        <div class="lhs">
          <h3>Data flow · Plan → Customer</h3>
          <span class="eyebrow">{scope_label} · {total} items traced</span>
        </div>
        <div class="rhs">
          <span><b>{total}</b> items in</span>
          <span class="ok">● <b>{ready_count}</b> ready</span>
          <span class="warn">● <b>{total_warn}</b> warning</span>
          <span class="crit">● <b>{total_crit}</b> critical</span>
          <span>{total_exc} exceptions to resolve</span>
        </div>
      </div>
      <div class="pipe-track">
        <div class="pipe-connector"></div>
        {''.join(stage_html_parts)}
      </div>
    </div>
    """
    _md(html)


# ============= KPIs =============
def render_kpis(plan: pd.DataFrame, exceptions: list[dict], campaigns_df: pd.DataFrame):
    today = pd.Timestamp(ANCHOR)
    campaign_windows = plan.groupby("campaign_id").agg(
        planned_start=("planned_start", "first"),
        planned_end=("planned_end", "first"),
        campaign_name=("campaign_name", "first"),
    )
    starting_soon_names = [
        r["campaign_name"]
        for _, r in campaign_windows.iterrows()
        if pd.Timestamp(r["planned_start"]) > today
        and (pd.Timestamp(r["planned_start"]) - today).days <= 7
    ]
    starting_soon = len(starting_soon_names)
    active_now_rows = [
        r
        for _, r in campaign_windows.iterrows()
        if pd.Timestamp(r["planned_start"]) <= today <= pd.Timestamp(r["planned_end"])
    ]
    active_now = len(active_now_rows)
    total_planned = plan["item_id"].nunique()
    crit_count = sum(1 for e in exceptions if e["severity"] == "Critical")
    warn_count = sum(1 for e in exceptions if e["severity"] == "Warning")
    planned_in_scope = [
        e for e in exceptions if e["campaign_id"] != "SYSTEM-DETECTED"
    ]
    items_with_issues = {e["item_id"] for e in planned_in_scope}
    ready = max(total_planned - len(items_with_issues), 0)
    ready_pct = int(round(ready / total_planned * 100)) if total_planned else 0

    starting_foot = ", ".join(starting_soon_names[:2]) if starting_soon_names else "—"
    if active_now_rows:
        active_foot = active_now_rows[0]["campaign_name"]
    else:
        active_foot = "none in window"

    html = f"""
    <section class="section">
      <div class="section-head">
        <div class="left">
          <span class="eyebrow">01 — Health</span>
          <h2>This week's window <span class="muted">· {ANCHOR.strftime('%a %b %d, %Y')}</span></h2>
        </div>
        <div class="right"><span>across all campaigns</span></div>
      </div>
      <div class="kpis">
        <div class="kpi">
          <div class="top"><span class="lbl">Starting soon</span></div>
          <div class="val">{starting_soon}</div>
          <div class="foot">≤ 7 days · {starting_foot}</div>
        </div>
        <div class="kpi">
          <div class="top"><span class="lbl">Active now</span></div>
          <div class="val">{active_now}</div>
          <div class="foot">{active_foot}</div>
        </div>
        <div class="kpi">
          <div class="top"><span class="lbl">Planned items</span></div>
          <div class="val">{total_planned}</div>
          <div class="foot">across {len(campaign_windows)} campaigns</div>
        </div>
        <div class="kpi k-ok">
          <div class="top"><span class="lbl">Ready</span></div>
          <div class="val">{ready}<span class="unit">/ {total_planned}</span></div>
          <div class="foot">{ready_pct}% pipeline complete</div>
        </div>
        <div class="kpi k-crit">
          <div class="top"><span class="lbl">Critical</span></div>
          <div class="val">{crit_count}</div>
          <div class="foot">must resolve before launch</div>
        </div>
        <div class="kpi k-warn">
          <div class="top"><span class="lbl">Warnings</span></div>
          <div class="val">{warn_count}</div>
          <div class="foot">accept · fix · defer</div>
        </div>
      </div>
    </section>
    """
    _md(html)


# ============= campaign cards =============
def render_campaign_cards(campaigns_df: pd.DataFrame, selected_id: str):
    today = pd.Timestamp(ANCHOR)
    sorted_df = campaigns_df.copy()
    sorted_df = sorted_df.sort_values("planned_start").reset_index(drop=True)

    cards_html = []
    for _, row in sorted_df.iterrows():
        cid = row["campaign_id"]
        total = int(row["item_count"])
        crit = int(row.get("critical_count", 0))
        warn = int(row.get("warning_count", 0))
        ready = int(row.get("ready_items", 0))
        pct = int(row.get("readiness_pct", 0))
        p_start = pd.Timestamp(row["planned_start"])
        p_end = pd.Timestamp(row["planned_end"])
        ok_pct = round(ready / total * 100, 1) if total else 0
        warn_pct = round(warn / total * 100, 1) if total else 0
        crit_pct = max(round(100 - ok_pct - warn_pct, 1), 0)
        days = (p_start - today).days
        if days > 0:
            urgency_label = f"{days}d"
            urgency_color = "var(--red)" if crit > 0 else ("var(--amber)" if days <= 7 else "var(--ink-3)")
        elif today <= p_end:
            urgency_label = "live"
            urgency_color = "var(--green)"
        else:
            urgency_label = "done"
            urgency_color = "var(--ink-4)"
        selected_class = " selected" if cid == selected_id else ""
        src_short = CAMPAIGN_SOURCE_SHORT.get(row["campaign_source"], row["campaign_source"])
        owner_short = row.get("owner", "")
        if not owner_short:
            owner_short = "—"
        else:
            owner_short = str(owner_short).split(" (")[0]
        cards_html.append(f"""
        <article class="camp{selected_class}">
          <div class="camp-top">
            <span class="camp-id">{cid} · {src_short}</span>
            <span class="sel-tag">In focus</span>
          </div>
          <div class="camp-name">{row['campaign_name']}</div>
          <div class="camp-meta">
            <span><label>Ch</label>{_channel_short(row['channel'])}</span>
            <span><label>Win</label>{p_start.strftime('%b %d')} → {p_end.strftime('%b %d')}</span>
            <span><label>Own</label>{owner_short}</span>
          </div>
          <div class="camp-bar">
            <span class="bar-ok"   style="width:{ok_pct}%"></span>
            <span class="bar-warn" style="width:{warn_pct}%"></span>
            <span class="bar-crit" style="width:{crit_pct}%"></span>
          </div>
          <div class="camp-foot">
            <span class="pct">{pct}%</span>
            <span class="camp-stats">
              <span class="s"><span class="d d-ok"></span>{ready}</span>
              <span class="s"><span class="d d-warn"></span>{warn}</span>
              <span class="s"><span class="d d-crit"></span>{crit}</span>
              <span style="color:{urgency_color};font-weight:500">{urgency_label}</span>
            </span>
          </div>
        </article>
        """)

    # Portfolio (All campaigns) pseudo-card
    portfolio_total = int(sorted_df["item_count"].sum())
    portfolio_crit = int(sorted_df["critical_count"].sum())
    portfolio_warn = int(sorted_df["warning_count"].sum())
    portfolio_ready = int(sorted_df["ready_items"].sum())
    portfolio_pct = (
        int(round(portfolio_ready / portfolio_total * 100)) if portfolio_total else 0
    )
    portfolio_ok_pct = round(portfolio_ready / portfolio_total * 100, 1) if portfolio_total else 0
    portfolio_warn_pct = round(portfolio_warn / portfolio_total * 100, 1) if portfolio_total else 0
    portfolio_crit_pct = max(round(100 - portfolio_ok_pct - portfolio_warn_pct, 1), 0)
    all_selected = " selected" if selected_id == "ALL" else ""
    portfolio_card = f"""
    <article class="camp camp-all{all_selected}">
      <div class="camp-top">
        <span class="camp-id">ALL · Portfolio</span>
        <span class="sel-tag">In focus</span>
      </div>
      <div class="camp-name">All campaigns</div>
      <div class="camp-meta">
        <span><label>N</label>{len(sorted_df)} campaigns</span>
        <span><label>SKUs</label>{portfolio_total}</span>
      </div>
      <div class="camp-bar">
        <span class="bar-ok"   style="width:{portfolio_ok_pct}%"></span>
        <span class="bar-warn" style="width:{portfolio_warn_pct}%"></span>
        <span class="bar-crit" style="width:{portfolio_crit_pct}%"></span>
      </div>
      <div class="camp-foot">
        <span class="pct">{portfolio_pct}%</span>
        <span class="camp-stats">
          <span class="s"><span class="d d-ok"></span>{portfolio_ready}</span>
          <span class="s"><span class="d d-warn"></span>{portfolio_warn}</span>
          <span class="s"><span class="d d-crit"></span>{portfolio_crit}</span>
        </span>
      </div>
    </article>
    """

    section_head = """
    <section class="section">
      <div class="section-head">
        <div class="left">
          <span class="eyebrow">02 — Campaigns</span>
          <h2>{n} in flight or queued</h2>
        </div>
        <div class="right">
          <span>Sorted by start date · click to focus</span>
        </div>
      </div>
    """.replace("{n}", str(len(sorted_df)))

    _md(section_head + f'<div class="campaigns">{portfolio_card}{"".join(cards_html)}</div></section>')

    # Functional buttons row beneath the cards for selection
    _md('<div class="invisible-btn-row" style="margin-top:8px">')
    n_cols = len(sorted_df) + 1
    cols = st.columns(n_cols)
    with cols[0]:
        label = "● All in focus" if selected_id == "ALL" else "Show all"
        if st.button(label, key="camp_select_ALL", use_container_width=True):
            st.session_state.selected_campaign = "ALL"
            st.rerun()
    for ci, (_, row) in enumerate(sorted_df.iterrows(), start=1):
        with cols[ci]:
            label = "● In focus" if row["campaign_id"] == selected_id else f"Focus {row['campaign_id']}"
            if st.button(label, key=f"camp_select_{row['campaign_id']}", use_container_width=True):
                st.session_state.selected_campaign = row["campaign_id"]
                st.rerun()
    _md("</div>")


# ============= exceptions =============
def _pick_focus_exception(camp_exc: list[dict]) -> dict | None:
    if not camp_exc:
        return None
    critical = [e for e in camp_exc if e["severity"] == "Critical"]
    pool = critical if critical else camp_exc
    item_counts: dict[str, int] = {}
    for e in pool:
        item_counts[e["item_id"]] = item_counts.get(e["item_id"], 0) + 1
    top_item = max(item_counts, key=item_counts.get)
    top_item_excs = [e for e in pool if e["item_id"] == top_item]
    return top_item_excs[0]


def _build_diff_rows(focus: dict, plan_row, sys_row) -> list[dict]:
    rows = []
    p_visible = bool(plan_row.get("planned_visibility", True))
    if sys_row is not None and focus["channel"] == "webshop":
        sys_vis = bool(sys_row["webshop_visible"])
        rows.append({
            "field": "Visibility",
            "category": "channel",
            "plan_v": "visible" if p_visible else "hidden",
            "plan_src": f"planned_visibility · {str(p_visible).lower()}",
            "sys_v": "hidden" if not sys_vis else "visible",
            "sys_src": f"webshop_visible · {str(sys_vis).lower()}",
            "sys_status": "bad" if (p_visible and not sys_vis) else "ok",
        })
    if sys_row is not None:
        img_ready = bool(sys_row["image_ready"])
        content_ready = bool(sys_row["content_ready"])
        missing = []
        if not img_ready: missing.append("image")
        if not content_ready: missing.append("content")
        rows.append({
            "field": "Content",
            "category": "content",
            "plan_v": "ready expected",
            "plan_src": "required for launch",
            "sys_v": f"missing {', '.join(missing)}" if missing else "ready",
            "sys_src": f"image_ready · {str(img_ready).lower()}",
            "sys_status": "warn" if missing else "ok",
        })
    if sys_row is not None:
        stock = int(sys_row["stock_on_hand"]) if pd.notna(sys_row["stock_on_hand"]) else 0
        forecast = int(sys_row["forecast_demand"]) if pd.notna(sys_row["forecast_demand"]) else 0
        if forecast > 0:
            status = "warn" if stock < forecast else "ok"
            rows.append({
                "field": "Stock",
                "category": "stock",
                "plan_v": f"{forecast} forecast",
                "plan_src": f"forecast_demand · {forecast}",
                "sys_v": f"{stock} on hand",
                "sys_src": f"stock_on_hand · {stock}",
                "sys_status": status,
            })
    planned_price = float(plan_row["planned_price"]) if pd.notna(plan_row["planned_price"]) else 0.0
    if sys_row is not None:
        sys_price = float(sys_row["system_price"]) if pd.notna(sys_row["system_price"]) else 0.0
        if sys_price > 0:
            status = "ok" if abs(sys_price - planned_price) <= planned_price * 0.01 else "warn"
            rows.append({
                "field": "Price",
                "category": "price",
                "plan_v": f"{planned_price:.2f} €",
                "plan_src": "planned_price",
                "sys_v": f"{sys_price:.2f} €",
                "sys_src": "system_price" + (" · in sync" if status == "ok" else " · mismatch"),
                "sys_status": status,
            })
        else:
            rows.append({
                "field": "Price",
                "category": "price",
                "plan_v": f"{planned_price:.2f} €",
                "plan_src": "planned_price",
                "sys_v": "no record",
                "sys_src": "system_price · missing",
                "sys_status": "bad",
            })
    else:
        rows.append({
            "field": "SKU",
            "category": "pim",
            "plan_v": focus["item_id"],
            "plan_src": "planned in campaign",
            "sys_v": "not found",
            "sys_src": "no system record",
            "sys_status": "bad",
        })

    # Prioritize: focus category first, then any row that's not ok, then the rest.
    focus_cat = focus.get("issue_category", "other")
    def _priority(row):
        if row["category"] == focus_cat:
            return 0
        if row["sys_status"] != "ok":
            return 1
        return 2
    rows.sort(key=_priority)
    # Drop rows that are ok and unrelated to focus, to cut noise (keep first 4)
    pruned = [r for r in rows if (r["category"] == focus_cat or r["sys_status"] != "ok")]
    if not pruned:
        pruned = rows[:1]
    return pruned[:4]


def _suggested_step(focus: dict, sys_row) -> str:
    issue = focus["issue_type"].lower()
    if "not visible in webshop" in issue:
        return "Toggle <code>webshop_visible = true</code> in PIM, then verify image + stock are ready."
    if "missing from system" in issue:
        return f"Create <code>{focus['item_id']}</code> in PIM and configure pricing, or remove from the plan."
    if "duplicate" in issue:
        return "Resolve duplicate price records to one canonical entry per channel."
    if "price mismatch" in issue:
        return f"Align system price with planned <code>{focus['plan_value']}</code>, or update the plan."
    if "starts too late" in issue:
        return f"Move <code>price_start</code> to match campaign start date."
    if "ends too early" in issue:
        return "Extend <code>price_end</code> to cover the full campaign window."
    if "missing image" in issue or "missing content" in issue:
        return "Upload hero + thumbnail and content blocks before launch."
    if "below forecast" in issue:
        return "Replenish stock, or notify Inventory to adjust the forecast."
    if "owner missing" in issue:
        return "Assign an owner in the campaign plan."
    return focus.get("action", "Review and decide on next step.")


def render_focus_card(focus: dict | None, plan: pd.DataFrame, system: pd.DataFrame, queue_remaining: int, view_mode: str = "Business"):
    if focus is None:
        _md("""
        <article class="focus">
          <div class="focus-bar ok"><span>● All clear</span><span class="sep">·</span><span>No critical exceptions on this campaign</span></div>
          <div class="focus-body" style="padding-bottom:22px">
            <div class="focus-titleblock">
              <h3>Ready to ship</h3>
              <p class="issue-line">All system data agrees with the campaign plan. Spot-check the timeline below and route the handoff packet to confirm.</p>
            </div>
          </div>
        </article>
        """)
        return

    plan_match = plan[(plan["campaign_id"] == focus["campaign_id"]) & (plan["item_id"] == focus["item_id"])]
    plan_row = plan_match.iloc[0] if not plan_match.empty else plan.iloc[0]
    sys_match = system[(system["item_id"] == focus["item_id"]) & (system["system_channel"] == focus["channel"])]
    sys_row = sys_match.iloc[0] if not sys_match.empty else None

    sev = focus["severity"]
    bar_cls = "warn" if sev == "Warning" else ""
    days_left = _days_to(plan_row["planned_start"])
    if days_left > 0:
        pressure_label, pressure_sub = f"{days_left:.1f}", f"{pd.Timestamp(plan_row['planned_start']).strftime('%b %d, 00:00 CET')}"
        pressure_lbl_text = "Days to start"
    elif pd.Timestamp(ANCHOR) <= pd.Timestamp(plan_row["planned_end"]):
        pressure_label, pressure_sub = "live", "active now"
        pressure_lbl_text = "Status"
    else:
        pressure_label, pressure_sub = "ended", f"{pd.Timestamp(plan_row['planned_end']).strftime('%b %d')}"
        pressure_lbl_text = "Status"

    stacked = sum(1 for _ in [None])
    p_start = pd.Timestamp(plan_row["planned_start"])
    days_to_str = "live" if days_left <= 0 else f"{int(days_left)}d {int((days_left % 1) * 24):02d}h"

    bar_label = f"{sev} · {focus.get('issue_origin', 'Issue')}"
    bar_right_lbl = "Active" if days_left <= 0 else "Launches in"
    diff_rows = _build_diff_rows(focus, plan_row, sys_row)
    diff_html_rows = []
    for r in diff_rows:
        diff_html_rows.append(f"""
        <div class="diff-row">
          <div class="diff-field">{r['field']}</div>
          <div class="diff-cell plan">
            <span class="v">{r['plan_v']}</span>
            <span class="src">{r['plan_src']}</span>
          </div>
          <div class="diff-arrow">→</div>
          <div class="diff-cell sys {r['sys_status']}">
            <span class="v">{r['sys_v']}</span>
            <span class="src">{r['sys_src']}</span>
          </div>
        </div>
        """)
    product_name = focus.get("product_name") or (sys_row["product_name"] if sys_row is not None else focus["item_id"])

    short_issue_line = focus.get("risk", "")
    suggested = _suggested_step(focus, sys_row)
    owner = focus.get("owner", "Unassigned")
    owner_initial = (owner[:1] or "?").upper()

    html = f"""
    <article class="focus {bar_cls}">
      <div class="focus-bar {bar_cls}">
        <span>{bar_label}</span>
        <span class="sep">·</span>
        <span>{_channel_short(focus['channel'])} channel</span>
        <span class="sep">·</span>
        <span>{focus['campaign_name']}</span>
        <span class="right">{bar_right_lbl} <b>{days_to_str}</b></span>
      </div>
      <div class="focus-body">
        <div class="focus-head">
          <div class="focus-titleblock">
            <div class="breadcrumb">
              <span class="sku">{focus['item_id']}</span><span class="sep">·</span>
              <span>{focus['campaign_id']} {focus['campaign_name']}</span><span class="sep">·</span>
              <span>{_channel_short(focus['channel'])}</span>
            </div>
            <h3>{product_name} <span class="muted">— {focus['issue_type'].lower()}</span></h3>
            <p class="issue-line">{short_issue_line}</p>
          </div>
          <div class="focus-pressure">
            <span class="lbl">{pressure_lbl_text}</span>
            <span class="val">{pressure_label}</span>
            <span class="sub">{pressure_sub}</span>
          </div>
        </div>
        <div class="diff">
          <div class="diff-row head">
            <div></div>
            <div class="src"><span class="d"></span>Plan</div>
            <div></div>
            <div class="src sys"><span class="d"></span>System</div>
          </div>
          {''.join(diff_html_rows)}
        </div>
        <div class="suggested">
          <span class="icon-circle">✓</span>
          <div class="body">
            <span class="lbl">Suggested next step</span>
            <span class="text">{suggested}</span>
          </div>
        </div>
      </div>
      <div class="focus-foot">
        <div class="owner">
          <span class="avatar">{owner_initial}</span>
          <div class="owner-text">
            <span class="l">Suggested owner</span>
            <span class="n">{owner}</span>
          </div>
        </div>
        <div class="actions" style="font-family:var(--mono);font-size:11px;color:var(--ink-3)">
          {queue_remaining} more in queue
        </div>
      </div>
    </article>
    """
    _md(html)

    if view_mode == "Technical":
        tech_rows = [
            ("issue_type", focus.get("issue_type")),
            ("issue_category", focus.get("issue_category")),
            ("issue_origin", focus.get("issue_origin")),
            ("severity", focus.get("severity")),
            ("campaign_id", focus.get("campaign_id")),
            ("channel", focus.get("channel")),
            ("item_id", focus.get("item_id")),
            ("plan_value", focus.get("plan_value")),
            ("system_value", focus.get("system_value")),
            ("recommended_action", focus.get("action")),
        ]
        tech_html = "".join(
            f'<div class="tech-row"><span class="tech-key">{k}</span><span class="tech-val">{v}</span></div>'
            for k, v in tech_rows if v is not None
        )
        _md(f'<div class="tech-panel"><div class="tech-head">Technical detail · raw exception payload</div>{tech_html}</div>')


def render_action_buttons(focus: dict | None, view_mode: str = "Business"):
    if focus is None:
        return
    decision_key = f"decision::{focus.get('campaign_id')}::{focus.get('item_id')}::{focus.get('issue_category', 'other')}"
    current = st.session_state.get(decision_key, "")
    options = [
        ("fix", "Fix", "primary"),
        ("accept", "Accept risk", ""),
        ("reassign", "Reassign", ""),
        ("resolved", "Mark resolved", ""),
        ("remove", "Remove", "danger"),
    ]
    if current:
        _md(f'<div class="decision-tag decision-{current}">● Decision: {current}</div>')
    cols = st.columns(len(options))
    for ci, (slug, label, kind) in enumerate(options):
        with cols[ci]:
            btn_type = "primary" if (kind == "primary" and not current) else "secondary"
            if st.button(label, key=f"{decision_key}::{slug}", type=btn_type, use_container_width=True):
                st.session_state[decision_key] = slug
                st.rerun()


def render_queue_cards(queue: list[dict]):
    items_html = []
    for exc in queue:
        sev_cls = "crit" if exc["severity"] == "Critical" else "warn"
        days = _days_to(_resolve_date(exc.get("date_window", "")))
        if days is None or days != days:  # NaN check via inequality
            urg = "—"
        elif days > 0:
            urg = f"{days:.1f}d"
        else:
            urg = "live"
        owner = (exc.get("owner") or "—").split(" (")[0]
        items_html.append(f"""
        <article class="qc {sev_cls}">
          <span class="sev"></span>
          <div class="qc-body">
            <div class="qc-top">
              <span class="sku">{exc['item_id']}</span>
              <span>{exc['campaign_id']}</span>
              <span class="sev-pill {sev_cls}"><span class="d"></span>{exc['severity']}</span>
            </div>
            <div class="qc-title">{exc.get('product_name', exc['item_id'])} <span class="muted">— {exc['issue_type'].lower()}</span></div>
            <div class="qc-issue">{exc.get('risk', '')}</div>
            <div class="qc-act"><span class="ar">→</span>{exc.get('action', '')}</div>
          </div>
          <div class="qc-meta">
            <span class="urg">{urg}</span>
            <span class="who">{owner}</span>
          </div>
        </article>
        """)
    head = '<div class="queue-head"><span>Up next</span><span>Ordered by urgency</span></div>'
    _md(f'<div class="queue">{head}{"".join(items_html)}</div>')


def _resolve_date(date_window: str):
    if not date_window:
        return None
    try:
        start = date_window.split(" - ")[0]
        return pd.Timestamp(start).date()
    except Exception:
        return None


def render_exception_rail(exceptions: list[dict], focus_item: str | None):
    exceptions = [e for e in exceptions if e.get("item_id") not in ("MISSING", "N/A", None, "")]
    if not exceptions:
        return
    minis = []
    for exc in exceptions:
        sev_cls = "crit" if exc["severity"] == "Critical" else ("warn" if exc["severity"] == "Warning" else "ok")
        focus_cls = " focus-mini" if focus_item and exc["item_id"] == focus_item else ""
        owner = (exc.get("owner") or "—").split(" (")[0]
        d = _days_to(_resolve_date(exc.get("date_window", "")))
        urg = f"{d:.1f}d" if d and d > 0 else ("live" if d is not None else "—")
        focus_label = " · in focus" if focus_item and exc["item_id"] == focus_item else ""
        minis.append(f"""
        <article class="mini {sev_cls}{focus_cls}">
          <span class="sku">{exc['item_id']}{focus_label}</span>
          <span class="nm">{exc.get('product_name', exc['item_id'])}</span>
          <span class="iss">{exc['issue_type']}</span>
          <span class="meta"><span>{urg}</span><span>{owner}</span></span>
        </article>
        """)
    html = f"""
    <div class="exc-rail-wrap">
      <div class="exc-rail-head">
        <span class="lbl">All remaining · scroll for the full queue</span>
        <span class="lbl"><b>{len(exceptions)}</b> total</span>
      </div>
      <div class="exc-rail">{''.join(minis)}</div>
    </div>
    """
    _md(html)


def render_exceptions_section(
    exceptions_all: list[dict],
    plan: pd.DataFrame,
    system: pd.DataFrame,
    focused_campaign_id: str,
    severity_filter: list[str],
    origin_filter: list[str],
    view_mode: str = "Business",
):
    cid_filter = lambda e: (focused_campaign_id == "ALL") or (e["campaign_id"] == focused_campaign_id)
    in_scope = [
        e for e in exceptions_all
        if cid_filter(e) and e.get("item_id") not in ("MISSING", "N/A", None, "")
    ]
    in_scope.sort(key=lambda e: (SEVERITY_ORDER.get(e["severity"], 9), e.get("item_id", "")))

    filtered = [
        e for e in in_scope
        if e["severity"] in severity_filter and e.get("issue_origin", "") in origin_filter
    ]

    crit_n = sum(1 for e in in_scope if e["severity"] == "Critical")
    warn_n = sum(1 for e in in_scope if e["severity"] == "Warning")
    origins = {
        "Plan issue": sum(1 for e in in_scope if e.get("issue_origin") == "Plan issue"),
        "System issue": sum(1 for e in in_scope if e.get("issue_origin") == "System issue"),
        "Cross-system mismatch": sum(1 for e in in_scope if e.get("issue_origin") == "Cross-system mismatch"),
        "Inferred/unplanned activity": sum(1 for e in in_scope if e.get("issue_origin") == "Inferred/unplanned activity"),
    }

    section_head = f"""
    <section class="section">
      <div class="section-head">
        <div class="left">
          <span class="eyebrow">03 — Exception queue</span>
          <h2>{len(in_scope)} to resolve <span class="muted">· ordered by pressure</span></h2>
        </div>
        <div class="right"><span>Showing {len(filtered)} / {len(in_scope)}</span></div>
      </div>
    """
    _md(section_head)

    # Functional chip filters via segmented_control (multi)
    _md('<div class="chip-row">')
    fc1, fc2 = st.columns([1, 2])
    with fc1:
        sev_options = [f"Critical · {crit_n}", f"Warning · {warn_n}"]
        sev_label_to_value = {f"Critical · {crit_n}": "Critical", f"Warning · {warn_n}": "Warning"}
        current_sev_labels = [lbl for lbl, val in sev_label_to_value.items() if val in severity_filter]
        new_sev_labels = st.segmented_control(
            "Severity",
            options=sev_options,
            default=current_sev_labels,
            selection_mode="multi",
            key="sev_chip_filter",
            label_visibility="collapsed",
        ) or []
        new_sev = [sev_label_to_value[lbl] for lbl in new_sev_labels]
        if "OK" in severity_filter:
            new_sev.append("OK")
    with fc2:
        origin_options = [
            f"Plan · {origins['Plan issue']}",
            f"System · {origins['System issue']}",
            f"Cross-system · {origins['Cross-system mismatch']}",
            f"Inferred · {origins['Inferred/unplanned activity']}",
        ]
        origin_label_to_value = {
            origin_options[0]: "Plan issue",
            origin_options[1]: "System issue",
            origin_options[2]: "Cross-system mismatch",
            origin_options[3]: "Inferred/unplanned activity",
        }
        current_origin_labels = [lbl for lbl, val in origin_label_to_value.items() if val in origin_filter]
        new_origin_labels = st.segmented_control(
            "Origin",
            options=origin_options,
            default=current_origin_labels,
            selection_mode="multi",
            key="origin_chip_filter",
            label_visibility="collapsed",
        ) or []
        new_origin = [origin_label_to_value[lbl] for lbl in new_origin_labels]
    _md('</div>')

    # Empty filter selection means "show all", to match natural chip UX
    if not new_sev:
        new_sev = ["Critical", "Warning", "OK"]
    if not new_origin:
        new_origin = ["Plan issue", "System issue", "Cross-system mismatch", "Inferred/unplanned activity"]

    if sorted(new_sev) != sorted(severity_filter) or sorted(new_origin) != sorted(origin_filter):
        st.session_state.severity_filter_state = new_sev
        st.session_state.origin_filter_state = new_origin
        st.rerun()

    # Re-apply filtering using updated state so the current frame already reflects clicks
    filtered = [
        e for e in in_scope
        if e["severity"] in new_sev and e.get("issue_origin", "") in new_origin
    ]

    if not filtered:
        _md('<div class="queue-more">No exceptions match the current filters.</div>')
        _md('</section>')
        return

    focus = _pick_focus_exception(filtered)
    queue = [e for e in filtered if e is not focus][:4]
    queue_remaining = max(len(filtered) - 1 - len(queue), 0)

    _md('<div class="exc-grid">')
    col_focus, col_queue = st.columns([3, 2], gap="small")
    with col_focus:
        render_focus_card(focus, plan, system, queue_remaining + len(queue), view_mode=view_mode)
        render_action_buttons(focus, view_mode=view_mode)
    with col_queue:
        render_queue_cards(queue)
        if queue_remaining > 0:
            _md(f'<div class="queue-more">+ <b>{queue_remaining}</b> more in the queue</div>')
    _md('</div>')

    render_exception_rail(filtered, focus["item_id"] if focus else None)
    _md('</section>')


# ============= timeline =============
def render_timeline(plan: pd.DataFrame, system: pd.DataFrame, exceptions: list[dict], campaign_id: str):
    camp_plan = plan[plan["campaign_id"] == campaign_id] if campaign_id != "ALL" else plan
    if camp_plan.empty:
        return

    starts = pd.to_datetime(camp_plan["planned_start"])
    ends = pd.to_datetime(camp_plan["planned_end"])
    timeline_start = (starts.min() - timedelta(days=2)).normalize()
    timeline_end = (ends.max() + timedelta(days=2)).normalize()
    total_days = max((timeline_end - timeline_start).days, 1)

    def pct_left(d):
        if d is None or pd.isna(d):
            return None
        d = pd.Timestamp(d)
        return round(max(0, min(100, (d - timeline_start).days / total_days * 100)), 1)

    def pct_width(s, e):
        l = pct_left(s)
        r = pct_left(e)
        if l is None or r is None:
            return 0, 0
        return l, max(round(r - l, 1), 0)

    today_pct = pct_left(pd.Timestamp(ANCHOR))

    exc_by_item: dict[str, list[dict]] = {}
    scope_exc = [e for e in exceptions if e["campaign_id"] == campaign_id] if campaign_id != "ALL" else exceptions
    for e in scope_exc:
        exc_by_item.setdefault(e["item_id"], []).append(e)

    rows_html = []
    for _, row in camp_plan.iterrows():
        item_id = row["item_id"]
        channel = row["channel"]
        sys_rows = system[(system["item_id"] == item_id) & (system["system_channel"] == channel)]
        sys_row = sys_rows.iloc[0] if not sys_rows.empty else None
        product_name = sys_row["product_name"] if sys_row is not None else "—"
        item_exc = exc_by_item.get(item_id, [])
        crit_count = sum(1 for e in item_exc if e["severity"] == "Critical")
        warn_count = sum(1 for e in item_exc if e["severity"] == "Warning")
        severity = "crit" if crit_count else ("warn" if warn_count else "ok")
        pct_complete = 100 if severity == "ok" else (25 if severity == "crit" else 75)
        status_label = "Ready" if severity == "ok" else ("Critical" if severity == "crit" else "Needs work")

        p_start = pd.Timestamp(row["planned_start"])
        p_end = pd.Timestamp(row["planned_end"])
        plan_left, plan_w = pct_width(p_start, p_end)

        price_status = "ok"
        price_left, price_w = plan_left, plan_w
        if sys_row is None or not sys_row["product_exists"]:
            price_status = "missing"
        else:
            price_s = sys_row["price_start"]
            price_e = sys_row["price_end"]
            sys_price = sys_row["system_price"]
            if pd.isna(price_s) or sys_price == 0:
                price_status = "missing"
            else:
                price_left, price_w = pct_width(price_s, price_e)
                planned_price = float(row["planned_price"])
                if price_s > p_start or price_e < p_end:
                    price_status = "warn"
                elif abs(sys_price - planned_price) > planned_price * 0.01:
                    price_status = "warn"

        tracks = [f'<div class="tl-track"><span class="lane-lbl">Plan</span><span class="tl-bar bar-plan" style="left:{plan_left}%;width:{plan_w}%"></span><span class="tl-today" style="left:{today_pct}%;"></span></div>']
        if price_status == "missing":
            tracks.append(f'<div class="tl-track"><span class="lane-lbl">System · missing</span><span class="tl-bar bar-missing" style="left:{plan_left}%;width:{plan_w}%"></span><span class="tl-today" style="left:{today_pct}%;"></span></div>')
        else:
            cls = "bar-price-ok" if price_status == "ok" else "bar-price-warn"
            lbl = "Price · ok" if price_status == "ok" else "Price · gap"
            tracks.append(f'<div class="tl-track"><span class="lane-lbl">{lbl}</span><span class="tl-bar {cls}" style="left:{price_left}%;width:{price_w}%"></span><span class="tl-today" style="left:{today_pct}%;"></span></div>')

        if channel == "webshop" and sys_row is not None and not sys_row["webshop_visible"]:
            tracks.append(f'<div class="tl-track"><span class="lane-lbl">Visibility · hidden</span><span class="tl-bar bar-missing" style="left:{plan_left}%;width:{plan_w}%"></span><span class="tl-today" style="left:{today_pct}%;"></span></div>')

        if sys_row is not None:
            stock = float(sys_row["stock_on_hand"]) if pd.notna(sys_row["stock_on_hand"]) else 0
            forecast = float(sys_row["forecast_demand"]) if pd.notna(sys_row["forecast_demand"]) else 0
            if forecast > 0 and stock < forecast:
                stock_cls = "bar-stock-crit" if sys_row["stock_risk"] == "high" else "bar-stock-warn"
                tracks.append(f'<div class="tl-track"><span class="lane-lbl">Stock · short</span><span class="tl-bar {stock_cls}" style="left:{plan_left}%;width:{plan_w}%"></span><span class="tl-today" style="left:{today_pct}%;"></span></div>')

        rows_html.append(f"""
        <div class="tl-row-wrap">
          <div class="sku-cell"><span class="sku">{item_id} · {_channel_short(channel)}</span><span class="nm">{product_name}</span></div>
          <div class="tl-tracks">{''.join(tracks)}</div>
          <div class="tl-status {severity}"><span class="pct">{pct_complete}%</span><span class="lbl">{status_label}</span></div>
        </div>
        """)

    axis_marks = []
    for i in range(0, 6):
        pct = i * 20
        d = timeline_start + timedelta(days=int(total_days * pct / 100))
        if i == 0 or abs(pct - today_pct) > 8:
            axis_marks.append(f'<span style="left:{pct}%">{d.strftime("%b %d")}</span>')
    axis_marks.append(f'<span style="left:{today_pct}%" class="today-mark">{ANCHOR.strftime("%b %d")} · today</span>')

    html = f"""
    <section class="section">
      <div class="section-head">
        <div class="left">
          <span class="eyebrow">04 — Timeline</span>
          <h2>Items · plan vs system</h2>
        </div>
        <div class="right">
          <span>Window · {timeline_start.strftime('%b %d')} → {timeline_end.strftime('%b %d')}</span>
        </div>
      </div>
      <div class="timeline">
        <div class="tl-header">
          <div>SKU · product</div>
          <div class="tl-axis">{''.join(axis_marks)}</div>
          <div style="text-align:right">Readiness</div>
        </div>
        {''.join(rows_html)}
        <div class="tl-legend">
          <span><span class="sw" style="background: rgba(15,17,22,.12);"></span>Plan window</span>
          <span><span class="sw" style="background: var(--teal);"></span>Price ok</span>
          <span><span class="sw" style="background: var(--amber);"></span>Price warning</span>
          <span><span class="sw" style="background: var(--red);"></span>Critical</span>
          <span><span class="sw" style="background: var(--green);"></span>Stock ok</span>
          <span><span class="sw" style="background: repeating-linear-gradient(-45deg, var(--red-tint), var(--red-tint) 4px, var(--red-soft) 4px, var(--red-soft) 8px); border: 1px dashed var(--red);"></span>Missing</span>
        </div>
      </div>
    </section>
    """
    _md(html)


# ============= handoff =============
CATEGORY_TO_TEAM = {
    "pim": "Product Data",
    "content": "E-commerce",
    "channel": "E-commerce",
    "stock": "Inventory",
    "owner": "Campaign Owners",
    "price": "Pricing",
    "plan": "Campaign Owners",
    "unplanned": "Campaign Owners",
    "other": "Campaign Owners",
}


def _team_for(exc: dict) -> str:
    return CATEGORY_TO_TEAM.get(exc.get("issue_category", "other"), "Campaign Owners")


TEAM_ICONS = {
    "Pricing": "€",
    "Product Data": "▦",
    "Inventory": "◫",
    "E-commerce": "◉",
    "Campaign Owners": "◐",
}
TEAM_ETAS = {
    "Pricing": "~ 30m",
    "Product Data": "~ 1h",
    "Inventory": "~ 24h",
    "E-commerce": "~ 2h",
    "Campaign Owners": "~ 15m",
}


def render_handoff(exceptions: list[dict], focused_campaign_id: str):
    in_scope = [e for e in exceptions if (focused_campaign_id == "ALL") or (e["campaign_id"] == focused_campaign_id)]
    teams: dict[str, list[dict]] = {t: [] for t in ["Pricing", "Product Data", "Inventory", "E-commerce", "Campaign Owners"]}
    for exc in in_scope:
        teams[_team_for(exc)].append(exc)

    cards = []
    for team_name, items in teams.items():
        crit = sum(1 for e in items if e["severity"] == "Critical")
        sev_cls = "crit" if crit > 0 else ("warn" if items else "ok")
        unit = "items to<br>fix" if team_name != "Campaign Owners" else "decisions<br>needed"
        rows = []
        for exc in items[:5]:
            short_action = exc.get("action", "").split(" / ")[0]
            rows.append(f"<li><span class=\"sku\">{exc['item_id']}</span><span>{short_action}</span></li>")
        if not rows:
            rows.append('<li><span class="sku">—</span><span style="color:var(--ink-4)">no items</span></li>')
        more = ""
        if len(items) > 5:
            more = f'<li><span class="sku">+</span><span>{len(items) - 5} more</span></li>'
        cards.append(f"""
        <article class="team">
          <div class="team-head">
            <h4 class="team-name">{team_name}</h4>
            <span class="team-icon">{TEAM_ICONS[team_name]}</span>
          </div>
          <div class="team-count {sev_cls}"><span class="num">{len(items)}</span><span class="unit">{unit}</span></div>
          <ul class="team-list">{''.join(rows)}{more}</ul>
          <div class="team-cta"><a href="#">→ Route to {team_name}</a><span>{TEAM_ETAS[team_name]}</span></div>
        </article>
        """)

    html = f"""
    <section class="section">
      <div class="section-head">
        <div class="left">
          <span class="eyebrow">05 — Routing</span>
          <h2>Handoff payload <span class="muted">· by team</span></h2>
        </div>
        <div class="right"><span>{sum(len(v) for v in teams.values())} items total</span></div>
      </div>
      <div class="handoff">{''.join(cards)}</div>
    </section>
    """
    _md(html)


# ============= footer =============
def render_footer(plan: pd.DataFrame):
    n_campaigns = plan["campaign_id"].nunique()
    n_items = plan["item_id"].nunique()
    html = f"""
    <footer class="footer">
      <div>Campaign Readiness · v2 · Streamlit</div>
      <div>Plan vs System · {n_campaigns} campaigns · {n_items} SKUs</div>
      <div>{ANCHOR.strftime('%a %d %b %Y')}</div>
    </footer>
    """
    _md(html)


# ============= main =============
def main():
    st.set_page_config(page_title="Campaign Readiness Monitor", layout="wide", initial_sidebar_state="collapsed")
    _md(load_design_css())

    plan = generate_campaign_plan()
    system = generate_system_truth()
    plan_issues = check_plan_quality(plan)
    exceptions = compare_plan_vs_system(plan, system)
    attach_categories(exceptions)
    attach_categories(plan_issues)
    all_issues = exceptions + plan_issues
    campaigns_df = build_campaign_summary(plan, all_issues)
    real_skus = set(plan["item_id"].dropna().astype(str).unique())

    if "selected_campaign" not in st.session_state:
        ranked = campaigns_df.copy()
        ranked["_days_to_start"] = (pd.to_datetime(ranked["planned_start"]) - pd.Timestamp(ANCHOR)).dt.days
        ranked = ranked.sort_values(
            by=["critical_count", "_days_to_start"],
            ascending=[False, True],
        )
        st.session_state.selected_campaign = ranked.iloc[0]["campaign_id"]
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "Business"
    if "severity_filter_state" not in st.session_state:
        st.session_state.severity_filter_state = ["Critical", "Warning"]
    if "origin_filter_state" not in st.session_state:
        st.session_state.origin_filter_state = [
            "Plan issue", "System issue", "Cross-system mismatch", "Inferred/unplanned activity",
        ]

    selected_id = st.session_state.selected_campaign
    is_portfolio = selected_id == "ALL"
    if is_portfolio:
        selected_slug = "all-campaigns"
        campaign_row = None
    else:
        match = campaigns_df[campaigns_df["campaign_id"] == selected_id]
        if match.empty:
            # Selection became stale; fall back to portfolio view
            st.session_state.selected_campaign = "ALL"
            st.rerun()
        campaign_row = match.iloc[0]
        selected_slug = _campaign_slug(campaign_row["campaign_name"])

    view_mode = render_topbar(selected_slug, st.session_state.view_mode)
    if is_portfolio:
        render_inspector_all(plan, campaigns_df, all_issues)
    else:
        render_inspector(campaign_row, all_issues)
    render_pipeline(plan, system, all_issues, selected_id)
    render_kpis(plan, all_issues, campaigns_df)
    render_campaign_cards(campaigns_df, selected_id)
    render_exceptions_section(
        all_issues,
        plan,
        system,
        selected_id,
        st.session_state.severity_filter_state,
        st.session_state.origin_filter_state,
        view_mode=view_mode,
    )
    render_timeline(plan, system, all_issues, selected_id)
    render_handoff(all_issues, selected_id)
    render_footer(plan)


if __name__ == "__main__":
    main()
