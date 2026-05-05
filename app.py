import pandas as pd
import numpy as np
import streamlit as st
from datetime import date

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

def main():
    st.set_page_config(page_title="Product Setup Verification Dashboard", layout="wide")
    # Inject a lightweight design system similar to pricing-tool-demo
    st.html(
        """
        <style>
        :root {
          --ink: #0A1F24;
          --paper: #F4F1EA;
          --ink-2: #122E35;
          --ink-3: #1B3F47;
          --teal: #14B8A6;
          --teal-soft: #CCFBF1;
        }
        .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1px; background: var(--ink); border: 1px solid var(--ink); margin: 16px 0 32px; }
        .card-item { background: var(--paper); padding: 20px; }
        .card-sub { font-family: sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: .12em; color: #1f1f1f; }
        .card-num { font-family: serif; font-size: 28px; color: var(--ink); margin-top: 6px; }
        </style>
        """,
        height=0,
    )
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
