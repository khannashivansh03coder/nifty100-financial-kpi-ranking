import streamlit as st
import pandas as pd

from src.dashboard.utils.db import get_master

st.title("🔍 Nifty 100 Stock Screener")

master = get_master()

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

# ---------------- Presets ---------------- #

preset = st.sidebar.selectbox(
    "Preset",
    [
        "Custom",
        "Quality",
        "Value",
        "Growth",
        "Dividend",
        "Debt-Free",
        "Turnaround"
    ]
)

# ---------------- Default Values ---------------- #

roe = 15.0
de = 1.0
fcf = 0
sales = 0
npm = 5.0
opm = 10.0
pe = 40.0
pb = 5.0
dividend = 0.0
icr = 1.0

# ---------------- Apply Presets ---------------- #

if preset == "Quality":
    roe = 20
    de = 1
    pe = 40

elif preset == "Value":
    pe = 20
    pb = 3

elif preset == "Growth":
    sales = 10000
    npm = 10
    opm = 15

elif preset == "Dividend":
    dividend = 2

elif preset == "Debt-Free":
    de = 0

elif preset == "Turnaround":
    fcf = 0
    icr = 2

# ---------------- Sliders ---------------- #

roe = st.sidebar.slider(
    "Minimum ROE %",
    0.0,
    50.0,
    float(roe)
)

de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    float(de)
)

fcf = st.sidebar.slider(
    "Minimum Free Cash Flow",
    0,
    50000,
    int(fcf)
)

sales = st.sidebar.slider(
    "Minimum Revenue",
    0,
    1000000,
    int(sales)
)

npm = st.sidebar.slider(
    "Minimum Net Profit Margin",
    0.0,
    50.0,
    float(npm)
)

opm = st.sidebar.slider(
    "Minimum Operating Margin",
    0.0,
    60.0,
    float(opm)
)

pe = st.sidebar.slider(
    "Maximum P/E",
    0.0,
    150.0,
    float(pe)
)

pb = st.sidebar.slider(
    "Maximum P/B",
    0.0,
    20.0,
    float(pb)
)

dividend = st.sidebar.slider(
    "Minimum Dividend Yield %",
    0.0,
    10.0,
    float(dividend)
)

icr = st.sidebar.slider(
    "Minimum Interest Coverage",
    0.0,
    50.0,
    float(icr)
)

# ---------------- Filter ---------------- #

filtered = master.copy()

filtered = filtered[
    (filtered["return_on_equity_pct"].fillna(0) >= roe) &
    (filtered["debt_to_equity"].fillna(999) <= de) &
    (filtered["free_cash_flow_cr"].fillna(0) >= fcf) &
    (filtered["sales"].fillna(0) >= sales) &
    (filtered["net_profit_margin_pct"].fillna(0) >= npm) &
    (filtered["operating_profit_margin_pct"].fillna(0) >= opm) &
    (filtered["pe_ratio"].fillna(9999) <= pe) &
    (filtered["pb_ratio"].fillna(9999) <= pb) &
    (filtered["dividend_yield_pct"].fillna(0) >= dividend) &
    (filtered["interest_coverage"].fillna(0) >= icr)
]

# ---------------- Result Count ---------------- #

st.success(
    f"{len(filtered)} companies match your filters."
)

# ---------------- Table ---------------- #

display_cols = [
    "company_id",
    "company_name",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "sales",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",
    "interest_coverage"
]

display_cols = [
    c for c in display_cols
    if c in filtered.columns
]

st.dataframe(
    filtered[display_cols],
    use_container_width=True
)

# ---------------- Download ---------------- #

csv = filtered[display_cols].to_csv(index=False)

st.download_button(
    "📥 Download CSV",
    csv,
    "screener_results.csv",
    "text/csv"
)