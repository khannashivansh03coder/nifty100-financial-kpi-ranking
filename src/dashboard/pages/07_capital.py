import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import get_master

st.set_page_config(layout="wide")

st.title("💰 Capital Allocation")

master = get_master()

# -----------------------------
# Check Required Columns
# -----------------------------

required = [
    "company_name",
    "market_cap_crore",
    "debt_to_equity"
]

for col in required:
    if col not in master.columns:
        st.error(f"{col} column not found.")
        st.stop()

# -----------------------------
# Capital Pattern
# -----------------------------

master = master.copy()

master["capital_pattern"] = "Balanced"

master.loc[
    master["debt_to_equity"] < 0.5,
    "capital_pattern"
] = "Debt Light"

master.loc[
    master["debt_to_equity"] > 1.5,
    "capital_pattern"
] = "Debt Heavy"

# -----------------------------
# Clean Data
# -----------------------------

master = master.dropna(
    subset=[
        "company_name",
        "market_cap_crore"
    ]
)

master = master[
    master["company_name"].astype(str).str.strip() != ""
]

master = master[
    master["market_cap_crore"] > 0
]

# -----------------------------
# Treemap
# -----------------------------

fig = px.treemap(
    master,
    path=["capital_pattern", "company_name"],
    values="market_cap_crore",
    color="debt_to_equity",
    color_continuous_scale="RdYlGn_r",
    title="Capital Allocation Treemap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -----------------------------
# Summary
# -----------------------------

summary = (
    master.groupby("capital_pattern")
    .agg(
        Companies=("company_name", "count"),
        Avg_Debt=("debt_to_equity", "mean"),
        Avg_MarketCap=("market_cap_crore", "mean")
    )
    .reset_index()
)

st.subheader("Capital Structure Summary")

st.dataframe(
    summary,
    use_container_width=True
)