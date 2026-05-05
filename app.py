import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta

"""
Mock verification dashboard
Replaces the previous price calculator with a simple synthetic verification dashboard.
"""

def build_mock_items():
    data = [
        {"item_id": "P001", "name": "Widget Pro", "category": "Gadgets",
         "expected_price": 199.0, "system_price": 210.0,
         "expected_start": "2026-05-01", "expected_end": "2026-12-31",
         "system_start": "2026-04-28", "system_end": "2027-01-15",
         "margin": 0.15, "status": "Active"},
        {"item_id": "P002", "name": "Widget Lite", "category": "Gadgets",
         "expected_price": 149.0, "system_price": 145.0,
         "expected_start": "2026-05-15", "expected_end": "2026-11-30",
         "system_start": "2026-05-15", "system_end": "2026-11-30",
         "margin": 0.18, "status": "Active"},
        {"item_id": "P003", "name": "Panel X", "category": "Displays",
         "expected_price": 299.0, "system_price": 320.0,
         "expected_start": "2026-04-01", "expected_end": "2026-10-15",
         "system_start": "2026-04-03", "system_end": "2026-10-15",
         "margin": 0.12, "status": "Active"},
        {"item_id": "P004", "name": "Dock Station", "category": "Accessories",
         "expected_price": 89.0, "system_price": 95.0,
         "expected_start": "2026-04-20", "expected_end": "2026-09-20",
         "system_start": "2026-04-20", "system_end": "2026-09-20",
         "margin": 0.14, "status": "Active"},
        {"item_id": "P005", "name": "Battery Pack", "category": "Power",
         "expected_price": 49.0, "system_price": 52.0,
         "expected_start": "2026-03-01", "expected_end": "2026-08-31",
         "system_start": "2026-03-01", "system_end": "2026-08-31",
         "margin": 0.18, "status": "Active"},
        {"item_id": "P006", "name": "Camera Module", "category": "Imaging",
         "expected_price": 129.0, "system_price": 120.0,
         "expected_start": "2026-05-01", "expected_end": "2026-12-31",
         "system_start": "2026-05-02", "system_end": "2027-01-31",
         "margin": 0.16, "status": "Active"},
    ]
    df = pd.DataFrame(data)
    for col in ["expected_start","expected_end","system_start","system_end"]:
        df[col] = pd.to_datetime(df[col]).dt.date
    return df

def validate_items(df: pd.DataFrame) -> pd.DataFrame:
    now = date.today()
    df = df.copy()
    df['start_date_matches'] = df['system_start'] == df['expected_start']
    df['end_date_matches'] = df['system_end'] == df['expected_end']
    df['price_matches'] = (df['system_price'] - df['expected_price']).abs() <= (df['expected_price'] * 0.05)
    df['active_today'] = (pd.to_datetime(now) >= pd.to_datetime(df['system_start'])) & (pd.to_datetime(now) <= pd.to_datetime(df['system_end']))
    df['margin_ok'] = df['margin'] >= 0.10
    df['validation_status'] = 'OK'
    df.loc[~df['active_today'], 'validation_status'] = 'Critical'
    cond = df['validation_status'] != 'Critical'
    df.loc[cond & (~df[['price_matches','start_date_matches','end_date_matches']].all(axis=1)), 'validation_status'] = 'Warning'
    df['issue'] = ''
    df.loc[df['validation_status'] == 'Critical', 'issue'] = 'Item not active today'
    df.loc[df['validation_status'] == 'Warning', 'issue'] = 'Mismatch in pricing or dates'
    return df

def build_weekly_specials() -> pd.DataFrame:
    # Simple weekly specials with dates relative to today for demonstration
    today = date.today()
    start = today - timedelta(days=1)
    end = today + timedelta(days=7)
    data = [
        {
            "item_id": "WS-01",
            "name": "Weekly Special A",
            "category": "Specials",
            "expected_price": 150.0,
            "system_price": 150.0,
            "expected_start": start,
            "expected_end": end,
            "system_start": start,
            "system_end": end,
            "margin": 0.15,
        },
        {
            "item_id": "WS-02",
            "name": "Weekly Special B",
            "category": "Specials",
            "expected_price": 180.0,
            "system_price": 180.0,
            "expected_start": start,
            "expected_end": end,
            "system_start": start,
            "system_end": end,
            "margin": 0.12,
        },
        {
            "item_id": "WS-03",
            "name": "Weekly Special C",
            "category": "Gadgets",
            "expected_price": 99.0,
            "system_price": 99.0,
            "expected_start": start,
            "expected_end": end,
            "system_start": start,
            "system_end": end,
            "margin": 0.20,
        },
    ]
    df = pd.DataFrame(data)
    for col in ["expected_start", "expected_end", "system_start", "system_end"]:
        df[col] = pd.to_datetime(df[col]).dt.date
    return df

def main():
    st.set_page_config(page_title="Product Setup Verification Dashboard", layout="wide")
    # Design port with safe fallback for mixed environments
    design_html = """
      <div class="band-container" style="height:80px; background: linear-gradient(to right, #f4f1ea 0%, #f4f1ea 8%, #ccfbf1 22%, #14b8a6 50%, #ccfbf1 78%, #f4f1ea 92%); border-top:1px solid #0a1f24; border-bottom:1px solid #0a1f24; margin:8px 0 24px;"></div>
      <div class="brand-wrap" style="padding:6px 12px;"><span class="brand-mark" style="font-family: Geister, serif; font-size:22px;">Product Setup Verification Dashboard</span></div>
    """
    try:
        st.html(design_html)
    except TypeError:
        st.markdown(design_html, unsafe_allow_html=True)
    st.title("Product Setup Verification Dashboard")

    df = build_mock_items()
    df = validate_items(df)
    total = len(df)
    ok = (df['validation_status'] == 'OK').sum()
    warn = (df['validation_status'] == 'Warning').sum()
    crit = (df['validation_status'] == 'Critical').sum()
    # KPI cards via custom HTML design
    html_kpi = f'''
    <div class="card-grid">
      <div class="card-item"><div class="card-sub">Total</div><div class="card-num">{total}</div></div>
      <div class="card-item"><div class="card-sub">OK</div><div class="card-num">{int(ok)}</div></div>
      <div class="card-item"><div class="card-sub">Warnings</div><div class="card-num">{int(warn)}</div></div>
      <div class="card-item"><div class="card-sub">Critical</div><div class="card-num">{int(crit)}</div></div>
    </div>
    '''
    st.markdown(html_kpi, unsafe_allow_html=True)

    # Weekly Specials Section: show items and verification with hover tooltips
    weekly = build_weekly_specials()
    weekly = validate_items(weekly)
    # Build a simple tooltip-enabled HTML table
    tooltip_css = """
    <style>
    table.weekly { border-collapse: collapse; width: 100%; }
    table.weekly th, table.weekly td { border: 1px solid #ccc; padding: 6px 8px; text-align: left; }
    td[data-tooltip] { position: relative; }
    td[data-tooltip]:hover::after {
      content: attr(data-tooltip);
      white-space: pre;
      position: absolute; left: 0; bottom: 100%; transform: translateY(-6px);
      background: #333; color: #fff; padding: 6px; border-radius: 4px; width: 260px; z-index: 9999;
      pointer-events: none;
    }
    </style>
    """
    rows = []
    for _, r in weekly.iterrows():
        tip = (
            f"Price: {r['system_price']:.2f} (exp {r['expected_price']:.2f})\\n"
            f"Dates: {r['expected_start']} - {r['expected_end']} / {r['system_start']} - {r['system_end']}\\n"
            f"Active: {r['active_today']} | Margin OK: {r['margin_ok']} | Price Match: {r['price_matches']}"
        )
        rows.append((r['name'], r['category'], r['system_price'], r['validation_status'], tip))
    weekly_html = tooltip_css + "<table class='weekly'><thead><tr><th>Item</th><th>Category</th><th>System Price</th><th>Status</th></tr></thead><tbody>"
    for name, cat, price, status, tip in rows:
        weekly_html += f"<tr><td data-tooltip='{tip}'>{name}</td><td>{cat}</td><td>{price:.2f}</td><td>{status}</td></tr>"
    weekly_html += "</tbody></table>"
    st.markdown(weekly_html, unsafe_allow_html=True)

    # Filter by status
    selected = st.multiselect("Filter by status", ['OK','Warning','Critical'], default=['OK','Warning','Critical'])
    filtered = df[df['validation_status'].isin(selected)]

    st.subheader("Main Validation")
    display_cols = ['item_id','name','category','expected_price','system_price',
                    'start_date_matches','end_date_matches','price_matches','active_today','margin_ok','validation_status','issue']
    st.dataframe(
        filtered[display_cols].rename(columns={
            'name':'Name','category':'Category','expected_price':'Expected Price','system_price':'System Price',
            'start_date_matches':'Start Match','end_date_matches':'End Match','price_matches':'Price Match',
            'active_today':'Active Today','margin_ok':'Margin OK','validation_status':'Status','issue':'Issue'
        })
    )

    st.subheader("Selected Item Detail")
    if not filtered.empty:
        selected_id = st.selectbox("Select item", filtered['item_id'].tolist())
        detail = filtered[filtered['item_id'] == selected_id].iloc[0]
        detail_table = pd.DataFrame({
            'Field': [
                'Item','Category','Expected Price','System Price',
                'Start (Expected/System)','End (Expected/System)','Margin','Active Today','Status','Issue'
            ],
            'Value': [
                str(detail['name']),
                str(detail['category']),
                str(detail['expected_price']),
                str(detail['system_price']),
                str(detail['expected_start']) + ' / ' + str(detail['system_start']),
                str(detail['expected_end']) + ' / ' + str(detail['system_end']),
                str(detail['margin']),
                str(detail['active_today']),
                str(detail['validation_status']),
                str(detail['issue']),
            ]
        })
        st.table(detail_table)
    else:
        st.write("No items to display.")

if __name__ == "__main__":
    main()
