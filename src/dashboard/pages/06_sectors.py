import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import get_master

st.set_page_config(layout="wide")

st.title("🏭 Sector Analysis")

master = get_master()

# -----------------------------
# Check Required Column
# -----------------------------

if "peer_group_name" not in master.columns:
    st.error("peer_group_name column not found in master dataset.")
    st.stop()

# -----------------------------
# Peer Group Selector
# -----------------------------

groups = sorted(master["peer_group_name"].dropna().unique())

selected_group = st.selectbox(
    "Select Peer Group",
    groups
)

df = master[
    master["peer_group_name"] == selected_group
].copy()

# -----------------------------
# Clean Missing Values
# -----------------------------

required_cols = [
    "sales",
    "return_on_equity_pct",
    "market_cap_crore"
]

for col in required_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# Remove rows with zero market cap so Plotly won't crash
df = df[df["market_cap_crore"] > 0]

# -----------------------------
# Bubble Chart
# -----------------------------

if len(df) == 0:

    st.warning("No companies available for this peer group.")

else:

    fig = px.scatter(

        df,

        x="sales",

        y="return_on_equity_pct",

        size="market_cap_crore",

        color="company_name",

        hover_name="company_name",

        title="Revenue vs ROE",

        height=650

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -----------------------------
# Median KPI Chart
# -----------------------------

kpis = {

    "ROE": df["return_on_equity_pct"].median(),

    "Net Profit Margin": df["net_profit_margin_pct"].median(),

    "Operating Margin": df["operating_profit_margin_pct"].median(),

    "Debt / Equity": df["debt_to_equity"].median(),

    "P/E": df["pe_ratio"].median(),

    "P/B": df["pb_ratio"].median()

}

kpi_df = {

    "Metric": list(kpis.keys()),

    "Median": list(kpis.values())

}

bar = px.bar(

    kpi_df,

    x="Metric",

    y="Median",

    title="Median KPIs",

    text_auto=".2f"

)

st.plotly_chart(
    bar,
    use_container_width=True
)

st.divider()

# -----------------------------
# Company Table
# -----------------------------

st.subheader("Companies")

cols = [

    "company_name",

    "sales",

    "return_on_equity_pct",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "market_cap_crore",

    "pe_ratio",

    "pb_ratio"

]

cols = [c for c in cols if c in df.columns]

st.dataframe(
    df[cols],
    use_container_width=True
)