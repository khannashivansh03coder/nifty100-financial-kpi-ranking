import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_master,
    get_sectors
)

st.set_page_config(layout="wide")

st.title("🏠 Nifty 100 Analytics Dashboard")

master = get_master()
sector_df = get_sectors()

# ---------------- Sidebar ---------------- #

st.sidebar.header("Filters")

years = sorted(master["year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Financial Year",
    years,
    index=len(years)-1
)

master = master[
    master["year"] == selected_year
]

# ---------------- KPI Tiles ---------------- #

st.subheader("Market Summary")

avg_roe = round(
    master["return_on_equity_pct"].mean(),
    2
)

median_pe = round(
    master["pe_ratio"].median(),
    2
)

median_de = round(
    master["debt_to_equity"].median(),
    2
)

total_companies = master["company_id"].nunique()

median_sales = round(
    master["sales"].median(),
    2
)

debt_free = len(
    master[
        master["debt_to_equity"] <= 0
    ]
)

c1,c2,c3 = st.columns(3)
c4,c5,c6 = st.columns(3)

c1.metric(
    "Average ROE",
    avg_roe
)

c2.metric(
    "Median P/E",
    median_pe
)

c3.metric(
    "Median D/E",
    median_de
)

c4.metric(
    "Companies",
    total_companies
)

c5.metric(
    "Median Revenue",
    median_sales
)

c6.metric(
    "Debt Free",
    debt_free
)

st.divider()

# ---------------- Sector Chart ---------------- #

st.subheader("Sector Distribution")

if "sector_name" in sector_df.columns:

    sector_chart = (
        sector_df
        .groupby("sector_name")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector_chart,
        names="sector_name",
        values="Companies",
        hole=0.5,
        title="Companies by Sector"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "sector_name column not found in sectors.xlsx"
    )

st.divider()

# ---------------- Top Companies ---------------- #

st.subheader("Top 5 Companies")

master["composite_score"] = (

    master["return_on_equity_pct"].fillna(0)*0.30 +

    master["operating_profit_margin_pct"].fillna(0)*0.20 +

    master["net_profit_margin_pct"].fillna(0)*0.20 +

    master["free_cash_flow_cr"].fillna(0)*0.15 -

    master["debt_to_equity"].fillna(0)*0.15

)

top5 = (

    master

    .sort_values(
        "composite_score",
        ascending=False
    )

    [[
        "company_name",
        "return_on_equity_pct",
        "pe_ratio",
        "debt_to_equity",
        "composite_score"
    ]]

    .head(5)

)

st.dataframe(
    top5,
    use_container_width=True
)