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


def generate_mock_weekly(today: date | None = None) -> pd.DataFrame:
    # Deterministic today anchor if provided; otherwise use today
    if today is None:
        today = date.today()
    data = [
        {
            "item_id": "WS-01",
            "name": "Weekly Special A",
            "category": "Specials",
            "local_price": 150.0,
            "local_start": today - timedelta(days=2),
            "local_end": today + timedelta(days=3),
            "local_expected_price": 150.0,
            "local_expected_start": today - timedelta(days=1),
            "local_expected_end": today + timedelta(days=6),
            "bin_price": 148.0,
            "bin_start": today - timedelta(days=1),
            "bin_end": today + timedelta(days=4),
            "bin_expected_price": 150.0,
            "bin_expected_start": today - timedelta(days=1),
            
            "bin_expected_end": today + timedelta(days=6),
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
    for col in ["local_start","local_end","local_expected_start","local_expected_end",
                "bin_start","bin_end","bin_expected_start","bin_expected_end",
                "online_start","online_end","online_expected_start","online_expected_end"]:
        df[col] = pd.to_datetime(df[col]).dt.date
    return df


def build_weekly_specials(force_today: date | None = None) -> pd.DataFrame:
    # Return mock weekly data, with optional deterministic anchor date for reproducibility
    return generate_mock_weekly(force_today)

def get_weekly_data() -> pd.DataFrame:
    if "weekly_data" in st.session_state:
        return st.session_state.weekly_data
    weekly = build_weekly_specials()
    st.session_state.weekly_data = weekly
    return weekly

def set_weekly_data(df: pd.DataFrame):
    st.session_state["weekly_data"] = df.copy()

def ensure_weekly_data(force_today: date | None = None) -> pd.DataFrame:
    weekly = get_weekly_data()
    if force_today is not None:
        weekly = generate_mock_weekly(force_today)
        set_weekly_data(weekly)
    return weekly


def render_overview():
    weekly = build_weekly_specials()
    weekly = weekly.copy()
    # Safeguard: compute KPI from existing data only
    if 'overall_status' in weekly.columns:
        ok = int((weekly['overall_status'] == 'OK').sum())
        warn = int((weekly['overall_status'] == 'Warning').sum())
        crit = int((weekly['overall_status'] == 'Critical').sum())
    else:
        ok = 0
        warn = 0
        crit = 0
    total = len(weekly)
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
    if not weekly.empty:
        preview = weekly[["item_id","name","category"]].rename(columns={"item_id":"ID","name":"Name","category":"Category"})
        st.dataframe(preview)
    else:
        st.write("No weekly specials configured.")

def render_weekly_specials():
    # Use session-backed weekly data if available; otherwise generate initial mock
    weekly = None
    try:
        weekly = get_weekly_data()
    except Exception:
        weekly = build_weekly_specials()
        set_weekly_data(weekly)
    if weekly is None or weekly.empty:
        weekly = build_weekly_specials()
        set_weekly_data(weekly)
    weekly = weekly.copy()
    weekly = weekly.fillna(0)
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

    # Render per-item collapsibles with per-system details
    for _, row in weekly.iterrows():
        label = f"{row['name']} ({row['item_id']}) - Overall: {row.get('overall_status','OK')}"
        with st.expander(label, expanded=False):
            html = []
            html.append("<table class='weekly'>")
            html.append("<thead><tr><th>System</th><th>Price</th><th>Window</th><th>Expected Price</th><th>Expected Window</th><th>Status</th></tr></thead>")
            html.append("<tbody>")
            inner = []
            # Build per-system rows with rich tooltips
            local_tip_text = (
                f"Price: {row['local_price']:.2f} (exp {row['local_expected_price']:.2f})\\n"
                f"Dates: {row['local_start']} - {row['local_end']} / {row['local_expected_start']} - {row['local_expected_end']}\\n"
                f"Active: {row.get('local_status','OK')}"
            )
            local_tip_html = local_tip_text.replace("\n", "<br>")
            html.append(
                f"<tr><td class='system-cell'>Local <span class='tooltip'>{local_tip_html}</span></td>"
            )
            html.append(f"<td>{row['local_price']:.2f}</td>")
            html.append(f"<td>{row['local_start']}-{row['local_end']}</td>")
            html.append(f"<td>{row['local_expected_price']:.2f}</td>")
            html.append(f"<td>{row['local_expected_start']}-{row['local_expected_end']}</td>")
            html.append(f"<td>{row.get('local_status','OK')}</td></tr>")
            bin_tip_text = (
                f"Price: {row['bin_price']:.2f} (exp {row['bin_expected_price']:.2f})\\n"
                f"Dates: {row['bin_start']} - {row['bin_end']} / {row['bin_expected_start']} - {row['bin_expected_end']}\\n"
                f"Active: {row.get('bin_status','OK')}"
            )
            bin_tip_html = bin_tip_text.replace("\n", "<br>")
            html.append(
                f"<td class='system-cell'>Bin <span class='tooltip'>{bin_tip_html}</span></td>"
            )
            html.append(f"<td>{row['bin_price']:.2f}</td>")
            html.append(f"<td>{row['bin_start']}-{row['bin_end']}</td>")
            html.append(f"<td>{row['bin_expected_price']:.2f}</td>")
            html.append(f"<td>{row['bin_expected_start']}-{row['bin_expected_end']}</td>")
            html.append(f"<td>{row.get('bin_status','OK')}</td></tr>")
            online_tip_text = (
                f"Price: {row['online_price']:.2f} (exp {row['online_expected_price']:.2f})\\n"
                f"Dates: {row['online_start']} - {row['online_end']} / {row['online_expected_start']} - {row['online_expected_end']}\\n"
                f"Active: {row.get('online_status','OK')}"
            )
            online_tip_html = online_tip_text.replace("\n", "<br>")
            html.append(
                f"<td class='system-cell'>Online <span class='tooltip'>{online_tip_html}</span></td>"
            )
            html.append(f"<td>{row['online_price']:.2f}</td>")
            html.append(f"<td>{row['online_start']}-{row['online_end']}</td>")
            html.append(f"<td>{row['online_expected_price']:.2f}</td>")
            html.append(f"<td>{row['online_expected_start']}-{row['online_expected_end']}</td>")
            html.append(f"<td>{row.get('online_status','OK')}</td></tr>")
            html.append("</tbody></table>")
            st.markdown("".join(html), unsafe_allow_html=True)

    # Corrections panel (mock) – simple, session-persisted corrections for the current session
    # This offers a minimal path to demonstrate a corrections workflow without persisting to disk.
    try:
        weekly  # ensure variable exists
        if not weekly.empty:
            corr_item = st.selectbox("Corrections item", weekly['item_id'].tolist())
            # fetch current row for the selected item
            current = weekly[weekly['item_id'] == corr_item].iloc[0]
            new_local_exp_price = st.number_input("Local expected price", value=current['local_expected_price'], key=f"lc_exp_price_{corr_item}")
            new_local_exp_start = st.date_input("Local expected start", value=current['local_expected_start'], key=f"lc_exp_start_{corr_item}")
            new_local_exp_end = st.date_input("Local expected end", value=current['local_expected_end'], key=f"lc_exp_end_{corr_item}")
            new_bin_exp_price = st.number_input("Bin expected price", value=current['bin_expected_price'], key=f"bc_exp_price_{corr_item}")
            new_bin_exp_start = st.date_input("Bin expected start", value=current['bin_expected_start'], key=f"bc_exp_start_{corr_item}")
            new_bin_exp_end = st.date_input("Bin expected end", value=current['bin_expected_end'], key=f"bc_exp_end_{corr_item}")
            new_online_exp_price = st.number_input("Online expected price", value=current['online_expected_price'], key=f"oc_exp_price_{corr_item}")
            new_online_exp_start = st.date_input("Online expected start", value=current['online_expected_start'], key=f"oc_exp_start_{corr_item}")
            new_online_exp_end = st.date_input("Online expected end", value=current['online_expected_end'], key=f"oc_exp_end_{corr_item}")
            if st.button("Apply Corrections", key=f"apply_corr_{corr_item}"):
                weekly.loc[weekly['item_id']==corr_item, 'local_expected_price'] = new_local_exp_price
                weekly.loc[weekly['item_id']==corr_item, 'local_expected_start'] = new_local_exp_start
                weekly.loc[weekly['item_id']==corr_item, 'local_expected_end'] = new_local_exp_end
                weekly.loc[weekly['item_id']==corr_item, 'bin_expected_price'] = new_bin_exp_price
                weekly.loc[weekly['item_id']==corr_item, 'bin_expected_start'] = new_bin_exp_start
                weekly.loc[weekly['item_id']==corr_item, 'bin_expected_end'] = new_bin_exp_end
                weekly.loc[weekly['item_id']==corr_item, 'online_expected_price'] = new_online_exp_price
                weekly.loc[weekly['item_id']==corr_item, 'online_expected_start'] = new_online_exp_start
                weekly.loc[weekly['item_id']==corr_item, 'online_expected_end'] = new_online_exp_end
                set_weekly_data(weekly)
                st.success("Corrections applied (mock, session)")
                payload = {
                    'item_id': corr_item,
                    'name': weekly.loc[weekly['item_id']==corr_item, 'name'].iloc[0],
                    'corrections': {
                        'local': {'expected_price': new_local_exp_price, 'expected_start': str(new_local_exp_start), 'expected_end': str(new_local_exp_end)},
                        'bin': {'expected_price': new_bin_exp_price, 'expected_start': str(new_bin_exp_start), 'expected_end': str(new_bin_exp_end)},
                        'online': {'expected_price': new_online_exp_price, 'expected_start': str(new_online_exp_start), 'expected_end': str(new_online_exp_end)},
                    },
                    'timestamp': date.today().isoformat()
                }
                st.json(payload, expanded=False)
        else:
            st.write("No weekly specials to correct.")
    except Exception:
        # If any of the session data isn't initialized yet, skip corrections gracefully
        pass

def validate_items(df: pd.DataFrame) -> pd.DataFrame:
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
        df['validation_status'] = df.get('validation_status', 'OK')
        df['issue'] = df.get('issue', '')
    return df


def main():
    st.set_page_config(page_title="Product Setup Verification Dashboard", layout="wide")
    # View switcher in left nav
    view = st.sidebar.radio("View", ["Overview", "Weekly Specials"])
    if view == "Overview":
        render_overview()
    else:
        render_weekly_specials()

if __name__ == "__main__":
    main()
