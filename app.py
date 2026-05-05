import pandas as pd
import streamlit as st

# Simple pricing dashboard for products using a rule-based model

# Helpers: pricing model constants
REGION_MULTIPLIERS = {
    "North America": 1.15,
    "Europe": 1.10,
    "Asia": 1.20,
    "South America": 1.05,
}
SEASON_MULTIPLIERS = {
    "Off-peak": 1.00,
    "Peak": 1.07,
}


class CatalogPrice:
    def __init__(self, subtotal, regional_adjustment, seasonal_adjustment,
                 complexity_premium, risk_buffer, margin, total):
        self.subtotal = subtotal
        self.regional_adjustment = regional_adjustment
        self.seasonal_adjustment = seasonal_adjustment
        self.complexity_premium = complexity_premium
        self.risk_buffer = risk_buffer
        self.margin = margin
        self.total = total


def build_product_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"product_type": "Laptop", "base_fee": 500, "hourly_rate": 30, "material_markup": 1.25, "risk_rate": 0.04},
            {"product_type": "Smartphone", "base_fee": 300, "hourly_rate": 25, "material_markup": 1.22, "risk_rate": 0.03},
            {"product_type": "Monitor", "base_fee": 250, "hourly_rate": 20, "material_markup": 1.20, "risk_rate": 0.05},
            {"product_type": "Tablet", "base_fee": 320, "hourly_rate": 22, "material_markup": 1.23, "risk_rate": 0.04},
        ]
    )


def calculate_catalog_price(
    catalog: pd.DataFrame,
    product_type: str,
    region: str,
    season: str,
    complexity: float,
    materials: float,
    labour: float,
    target_margin: float,
) -> CatalogPrice:
    item = catalog.loc[catalog["product_type"] == product_type].iloc[0]
    base_and_work = (
        item["base_fee"]
        + materials * item["material_markup"]
        + labour * item["hourly_rate"]
    )
    regional_adjustment = base_and_work * (REGION_MULTIPLIERS[region] - 1)
    seasonal_adjustment = base_and_work * (SEASON_MULTIPLIERS[season] - 1)
    complexity_premium = base_and_work * max(complexity - 5, 0) * 0.035
    risk_buffer = base_and_work * item["risk_rate"] * (1 + complexity / 12)
    subtotal = (
        base_and_work
        + regional_adjustment
        + seasonal_adjustment
        + complexity_premium
        + risk_buffer
    )
    margin = subtotal * target_margin
    return CatalogPrice(
        subtotal=float(subtotal),
        regional_adjustment=float(regional_adjustment),
        seasonal_adjustment=float(seasonal_adjustment),
        complexity_premium=float(complexity_premium),
        risk_buffer=float(risk_buffer),
        margin=float(margin),
        total=float(subtotal + margin),
    )


def main():
    st.set_page_config(page_title="Product Pricing Dashboard", layout="wide")
    st.title("Product Pricing Dashboard")

    catalog = build_product_catalog()

    with st.sidebar:
        st.header("Inputs")
        product_type = st.selectbox("Product", catalog["product_type"].tolist())
        region = st.selectbox("Region", list(REGION_MULTIPLIERS.keys()))
        season = st.selectbox("Season", list(SEASON_MULTIPLIERS.keys()))
        complexity = st.slider("Complexity", 0.0, 10.0, 3.0, 0.5)
        materials = st.slider("Materials (cost)", 0.0, 2000.0, 400.0, 50.0)
        labour = st.slider("Labour (hours)", 0.0, 200.0, 40.0, 5.0)
        target_margin = st.slider("Target Margin", 0.0, 0.5, 0.15, 0.01)

    price = calculate_catalog_price(
        catalog,
        product_type,
        region,
        season,
        complexity,
        materials,
        labour,
        target_margin,
    )

    # Summary cards
    st.metric(label="Subtotal", value=f"{price.subtotal:,.2f}")
    st.metric(label="Regional Adj.", value=f"{price.regional_adjustment:,.2f}")
    st.metric(label="Seasonal Adj.", value=f"{price.seasonal_adjustment:,.2f}")
    st.metric(label="Complexity Premium", value=f"{price.complexity_premium:,.2f}")
    st.metric(label="Risk Buffer", value=f"{price.risk_buffer:,.2f}")
    st.metric(label="Margin", value=f"{price.margin:,.2f}")
    st.metric(label="Total", value=f"{price.total:,.2f}")

    # Detailed breakdown
    breakdown = {
        "Component": ["Subtotal", "Regional Adj.", "Seasonal Adj.",
                      "Complexity Premium", "Risk Buffer", "Margin", "Total"],
        "Value": [price.subtotal, price.regional_adjustment, price.seasonal_adjustment,
                  price.complexity_premium, price.risk_buffer, price.margin, price.total],
    }
    df = pd.DataFrame(breakdown)
    st.dataframe(df.style.format({"Value": "{:.2f}"}))

    # Simple visualization
    viz = pd.DataFrame({
        "Component": ["Subtotal", "Margin"],
        "Amount": [price.subtotal, price.margin],
    })
    st.bar_chart(viz.set_index("Component"))

if __name__ == "__main__":
    main()
