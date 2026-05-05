import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta
import os

def load_design_css():
    css_path = os.path.join(os.path.dirname(__file__), "design", "design.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        return f"<style>\n{css}\n</style>"
    except Exception:
        return ""

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

def render_overview():
    # Overview KPI using the design system
    weekly = build_weekly_specials()
    weekly = validate_items(weekly)
    total = len(weekly)
    ok = int((weekly.get('overall_status') == 'OK').sum())
    warn = int((weekly.get('overall_status') == 'Warning').sum())
    crit = int((weekly.get('overall_status') == 'Critical').sum())
    html_kpi = f'''
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-label">Total</div><div class="kpi-value">{total}</div></div>
      <div class="kpi-card"><div class="kpi-label">OK</div><div class="kpi-value">{int(ok)}</div></div>
      <div class="kpi-card"><div class="kpi-label">Warnings</div><div class="kpi-value">{int(warn)}</div></div>
      <div class="kpi-card"><div class="kpi-label">Critical</div><div class="kpi-value">{int(crit)}</div></div>
    </div>
    '''
    st.markdown(html_kpi, unsafe_allow_html=True)
    st.subheader("Weekly Specials Preview")
    preview = weekly[["item_id","name","overall_status"]].rename(columns={"item_id":"ID","name":"Name","overall_status":"Status"})
    st.dataframe(preview)

def render_weekly_specials():
    weekly = build_weekly_specials()
    weekly = validate_items(weekly)
    today = date.today()
    # Compute per-system statuses
    for idx, row in weekly.iterrows():
        local = _verify_system(row["local_price"], row["local_expected_price"], row["local_start"], row["local_expected_start"], row["local_end"], row["local_expected_end"], today)
        bin_ = _verify_system(row["bin_price"], row["bin_expected_price"], row["bin_start"], row["bin_expected_start"], row["bin_end"], row["bin_expected_end"], today)
        online = _verify_system(row["online_price"], row["online_expected_price"], row["online_start"], row["online_expected_start"], row["online_end"], row["online_expected_end"], today)
        weekly.at[idx, "local_status"] = local["status"]
        weekly.at[idx, "bin_status"] = bin_["status"]
        weekly.at[idx, "online_status"] = online["status"]
        statuses = [local["status"], bin_["status"], online["status"]]
        if any(s == "Critical" for s in statuses):
            weekly.at[idx, "overall_status"] = "Critical"
        elif any(s == "Warning" for s in statuses):
            weekly.at[idx, "overall_status"] = "Warning"
        else:
            weekly.at[idx, "overall_status"] = "OK"

    # Render per-item collapsibles
    for _, row in weekly.iterrows():
        label = f"{row['name']} ({row['item_id']}) - Overall: {row.get('overall_status','OK')}"
        with st.expander(label, expanded=False):
            html = []
            html.append("<table class='weekly'>")
            html.append("<thead><tr><th>System</th><th>Price</th><th>Window</th><th>Expected Price</th><th>Expected Window</th><th>Status</th></tr></thead>")
            html.append("<tbody>")
            def add(system, price, win, exp_price, exp_win, status):
                html.append(f"<tr><td>{system}</td><td>{price:.2f}</td><td>{win}</td><td>{exp_price:.2f}</td><td>{exp_win}</td><td>{status}</td></tr>")
            add("Local", row['local_price'], f"{row['local_start']}-{row['local_end']}", row['local_expected_price'], f"{row['local_expected_start']}-{row['local_expected_end']}", row.get('local_status','OK'))
            add("Bin", row['bin_price'], f"{row['bin_start']}-{row['bin_end']}", row['bin_expected_price'], f"{row['bin_expected_start']}-{row['bin_expected_end']}", row.get('bin_status','OK'))
            add("Online", row['online_price'], f"{row['online_start']}-{row['online_end']}", row['online_expected_price'], f"{row['online_expected_start']}-{row['online_expected_end']}", row.get('online_status','OK'))
            html.append("</tbody></table>")
            st.markdown("".join(html), unsafe_allow_html=True)

def validate_items(df: pd.DataFrame) -> pd.DataFrame:
    # Robust validator: only runs if expected columns exist
    now = date.today()
    df = df.copy()
    required = {'system_start','system_end','expected_start','expected_end'}
    if required.issubset(set(df.columns)):
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
    else:
        # Missing schema for weekly specials; skip complex validation
        df['validation_status'] = df.get('validation_status', 'OK')
        df['issue'] = df.get('issue', '')
    return df

def _verify_system(price, price_exp, start, start_exp, end, end_exp, today):
    price_ok = abs(price - price_exp) <= price_exp * 0.05
    start_ok = start == start_exp
    end_ok = end == end_exp
    active_today = (pd.to_datetime(today) >= pd.to_datetime(start)) and (pd.to_datetime(today) <= pd.to_datetime(end))
    if not active_today:
        status = "Critical"
    elif price_ok and start_ok and end_ok:
        status = "OK"
    else:
        status = "Warning"
    return {"price_ok": price_ok, "start_ok": start_ok, "end_ok": end_ok, "active_today": active_today, "status": status}

def _system_statuses_for_row(row, today: date):
    systems = ["local", "bin", "online"]
    statuses = {}
    for s in systems:
        price = row.get(f"{s}_price")
        price_exp = row.get(f"{s}_expected_price")
        start = row.get(f"{s}_start")
        start_exp = row.get(f"{s}_expected_start")
        end = row.get(f"{s}_end")
        end_exp = row.get(f"{s}_expected_end")
        verify = _verify_system(price, price_exp, start, start_exp, end, end_exp, today)
        statuses[f"{s}_status"] = verify["status"]
    # overall can be derived outside
    return statuses

def build_weekly_specials() -> pd.DataFrame:
    # Weekly specials with three systems: local, bin, online
    today = date.today()
    base_start = today - timedelta(days=2)
    base_end = today + timedelta(days=5)
    data = [
        {
            "item_id": "WS-01",
            "name": "Weekly Special A",
            "category": "Specials",
            # Local
            "local_price": 150.0,
            "local_start": today - timedelta(days=2),
            "local_end": today + timedelta(days=3),
            "local_expected_price": 150.0,
            "local_expected_start": today - timedelta(days=1),
            "local_expected_end": today + timedelta(days=6),
            # Bin
            "bin_price": 148.0,
            "bin_start": today - timedelta(days=1),
            "bin_end": today + timedelta(days=4),
            "bin_expected_price": 150.0,
            "bin_expected_start": today - timedelta(days=1),
            "bin_expected_end": today + timedelta(days=6),
            # Online
            "online_price": 155.0,
            "online_start": today,
            "online_end": today + timedelta(days=7),
            "online_expected_price": 155.0,
            "online_expected_start": today,
            "online_expected_end": today + timedelta(days=7),
            "margin": 0.15,
        },
        {
            "item_id": "WS-02",
            "name": "Weekly Special B",
            "category": "Specials",
            "local_price": 180.0,
            "local_start": today - timedelta(days=2),
            "local_end": today + timedelta(days=6),
            "local_expected_price": 185.0,
            "local_expected_start": today - timedelta(days=2),
            "local_expected_end": today + timedelta(days=6),
            "bin_price": 178.0,
            "bin_start": today - timedelta(days=1),
            "bin_end": today + timedelta(days=4),
            "bin_expected_price": 180.0,
            "bin_expected_start": today - timedelta(days=1),
            "bin_expected_end": today + timedelta(days=4),
            "online_price": 182.0,
            "online_start": today,
            "online_end": today + timedelta(days=5),
            "online_expected_price": 180.0,
            "online_expected_start": today,
            "online_expected_end": today + timedelta(days=5),
            "margin": 0.12,
        },
        {
            "item_id": "WS-03",
            "name": "Weekly Special C",
            "category": "Gadgets",
            "local_price": 99.0,
            "local_start": today - timedelta(days=2),
            "local_end": today + timedelta(days=3),
            "local_expected_price": 100.0,
            "local_expected_start": today - timedelta(days=1),
            "local_expected_end": today + timedelta(days=4),
            "bin_price": 99.0,
            "bin_start": today - timedelta(days=2),
            "bin_end": today + timedelta(days=3),
            "bin_expected_price": 99.0,
            "bin_expected_start": today - timedelta(days=2),
            "bin_expected_end": today + timedelta(days=5),
            "online_price": 100.0,
            "online_start": today,
            "online_end": today + timedelta(days=6),
            "online_expected_price": 100.0,
            "online_expected_start": today,
            "online_expected_end": today + timedelta(days=6),
            "margin": 0.18,
        },
    ]
    df = pd.DataFrame(data)
    # keep dates as date objects
    for col in ["local_start","local_end","local_expected_start","local_expected_end",
                "bin_start","bin_end","bin_expected_start","bin_expected_end",
                "online_start","online_end","online_expected_start","online_expected_end"]:
        df[col] = pd.to_datetime(df[col]).dt.date
    return df

def main():
    st.set_page_config(page_title="Product Setup Verification Dashboard", layout="wide")
    # Load and apply design CSS from design/design.css (Step 1)
    css = load_design_css()
    if css:
        st.markdown(css, unsafe_allow_html=True)
    # Design port with safe fallback for mixed environments
    design_html = """
      <div class='band-container' style='height:80px; background: linear-gradient(to right, #f4f1ea 0%, #f4f1ea 8%, #ccfbf1 22%, #14b8a6 50%, #ccfbf1 78%, #f4f1ea 92%); border-top:1px solid #0a1f24; border-bottom:1px solid #0a1f24; margin:8px 0 24px;'></div>
      <div class='brand-wrap' style='padding:6px 12px;'><span class='brand-mark' style='font-family: Geister, serif; font-size:22px;'>Product Setup Verification Dashboard</span></div>
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

    # Weekly Specials Section: collapsible per-item view with per-system verification
    weekly = build_weekly_specials()
    weekly = validate_items(weekly)
    today = date.today()
    # Compute per-system statuses for each row
    for idx, row in weekly.iterrows():
        local = _verify_system(row["local_price"], row["local_expected_price"], row["local_start"], row["local_expected_start"], row["local_end"], row["local_expected_end"], today)
        bin_ = _verify_system(row["bin_price"], row["bin_expected_price"], row["bin_start"], row["bin_expected_start"], row["bin_end"], row["bin_expected_end"], today)
        online = _verify_system(row["online_price"], row["online_expected_price"], row["online_start"], row["online_expected_start"], row["online_end"], row["online_expected_end"], today)
        weekly.at[idx, "local_status"] = local["status"]
        weekly.at[idx, "bin_status"] = bin_["status"]
        weekly.at[idx, "online_status"] = online["status"]
        # overall
        statuses = [local["status"], bin_["status"], online["status"]]
        if any(s == "Critical" for s in statuses):
            weekly.at[idx, "overall_status"] = "Critical"
        elif any(s == "Warning" for s in statuses):
            weekly.at[idx, "overall_status"] = "Warning"
        else:
            weekly.at[idx, "overall_status"] = "OK"

    # Health banner and export controls for weekly specials
    try:
        ok_count = int((weekly.get('overall_status') == 'OK').sum())
        warn_count = int((weekly.get('overall_status') == 'Warning').sum())
        crit_count = int((weekly.get('overall_status') == 'Critical').sum())
        total_weekly = int(len(weekly))
        if crit_count > 0:
            color = '#dc2626'
        elif warn_count > 0:
            color = '#f59e0b'
        else:
            color = '#16a34a'
        banner = f"<div style='padding:8px 12px; background:{color}; color:white; border-radius:6px; display:inline-block; font-weight:600;'>Weekly Health: OK {ok_count} / {total_weekly} | Warnings {warn_count} | Critical {crit_count}</div>"
        st.markdown(banner, unsafe_allow_html=True)
    except Exception:
        pass

    # Export weekly specials to CSV
    export_rows = []
    for _, rr in weekly.iterrows():
        export_rows.append({
            'item_id': rr.get('item_id'),
            'name': rr.get('name'),
            'category': rr.get('category'),
            'local_price': rr.get('local_price'),
            'local_start': str(rr.get('local_start')) if rr.get('local_start') else '',
            'local_end': str(rr.get('local_end')) if rr.get('local_end') else '',
            'local_expected_price': rr.get('local_expected_price'),
            'local_expected_start': str(rr.get('local_expected_start')) if rr.get('local_expected_start') else '',
            'local_expected_end': str(rr.get('local_expected_end')) if rr.get('local_expected_end') else '',
            'bin_price': rr.get('bin_price'),
            'bin_start': str(rr.get('bin_start')) if rr.get('bin_start') else '',
            'bin_end': str(rr.get('bin_end')) if rr.get('bin_end') else '',
            'bin_expected_price': rr.get('bin_expected_price'),
            'bin_expected_start': str(rr.get('bin_expected_start')) if rr.get('bin_expected_start') else '',
            'bin_expected_end': str(rr.get('bin_expected_end')) if rr.get('bin_expected_end') else '',
            'online_price': rr.get('online_price'),
            'online_start': str(rr.get('online_start')) if rr.get('online_start') else '',
            'online_end': str(rr.get('online_end')) if rr.get('online_end') else '',
            'online_expected_price': rr.get('online_expected_price'),
            'online_expected_start': str(rr.get('online_expected_start')) if rr.get('online_expected_start') else '',
            'online_expected_end': str(rr.get('online_expected_end')) if rr.get('online_expected_end') else '',
            'margin': rr.get('margin'),
            'local_status': rr.get('local_status'),
            'bin_status': rr.get('bin_status'),
            'online_status': rr.get('online_status'),
            'overall_status': rr.get('overall_status'),
        })
    if export_rows:
        weekly_export_df = pd.DataFrame(export_rows)
        csv_text = weekly_export_df.to_csv(index=False)
        st.download_button(label='Download Weekly CSV', data=csv_text, file_name='weekly_specials.csv', mime='text/csv')

    # Render collapsible per weekly item with per-system table
    for idx, row in weekly.iterrows():
        label = f"{row['name']} ({row['item_id']}) - Overall: {row.get('overall_status','OK')}"
        with st.expander(label, expanded=False):
            inner = []
            inner.append("<table class='weekly'>")
            inner.append("<thead><tr><th>System</th><th>Price</th><th>Window</th><th>Expected Price</th><th>Expected Window</th><th>Status</th></tr></thead>")
            inner.append("<tbody>")
            # Local
            local_tip = (
                f"Price: {row['local_price']:.2f} (exp {row['local_expected_price']:.2f})\\n"
                f"Dates: {row['local_start']} - {row['local_end']} / {row['local_expected_start']} - {row['local_expected_end']}\\n"
                f"Active: {row.get('local_status','OK')}"
            )
            inner.append(
                f"<tr><td title=\"{local_tip}\">Local</td>"
                f"<td>{row['local_price']:.2f}</td>"
                f"<td>{row['local_start']}-{row['local_end']}</td>"
                f"<td>{row['local_expected_price']:.2f}</td>"
                f"<td>{row['local_expected_start']}-{row['local_expected_end']}</td>"
                f"<td>{row.get('local_status','OK')}</td></tr>"
            )
            # Bin
            bin_tip = (
                f"Price: {row['bin_price']:.2f} (exp {row['bin_expected_price']:.2f})\\n"
                f"Dates: {row['bin_start']} - {row['bin_end']} / {row['bin_expected_start']} - {row['bin_expected_end']}\\n"
                f"Active: {row.get('bin_status','OK')}"
            )
            inner.append(
                f"<tr><td title=\"{bin_tip}\">Bin</td>"
                f"<td>{row['bin_price']:.2f}</td>"
                f"<td>{row['bin_start']}-{row['bin_end']}</td>"
                f"<td>{row['bin_expected_price']:.2f}</td>"
                f"<td>{row['bin_expected_start']}-{row['bin_expected_end']}</td>"
                f"<td>{row.get('bin_status','OK')}</td></tr>"
            )
            # Online
            online_tip = (
                f"Price: {row['online_price']:.2f} (exp {row['online_expected_price']:.2f})\\n"
                f"Dates: {row['online_start']} - {row['online_end']} / {row['online_expected_start']} - {row['online_expected_end']}\\n"
                f"Active: {row.get('online_status','OK')}"
            )
            inner.append(
                f"<tr><td title=\"{online_tip}\">Online</td>"
                f"<td>{row['online_price']:.2f}</td>"
                f"<td>{row['online_start']}-{row['online_end']}</td>"
                f"<td>{row['online_expected_price']:.2f}</td>"
                f"<td>{row['online_expected_start']}-{row['online_expected_end']}</td>"
                f"<td>{row.get('online_status','OK')}</td></tr>"
            )
            inner.append("</tbody></table>")
            st.markdown("".join(inner), unsafe_allow_html=True)

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
