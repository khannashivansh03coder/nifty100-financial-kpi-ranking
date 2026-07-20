import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.dashboard.utils.db import get_master

st.set_page_config(layout="wide")

st.title("📈 Trend Analysis")

master = get_master()

# -----------------------------
# Company Selector
# -----------------------------

companies = sorted(master["company_name"].dropna().unique())

company = st.selectbox(
    "Select Company",
    companies
)

company_df = (
    master[
        master["company_name"] == company
    ]
    .sort_values("year")
    .copy()
)

# -----------------------------
# Metric Selector
# -----------------------------

metric_options = {
    "Sales": "sales",
    "Net Profit": "net_profit",
    "Operating Profit": "operating_profit",
    "ROE %": "return_on_equity_pct",
    "Net Profit Margin %": "net_profit_margin_pct",
    "Operating Margin %": "operating_profit_margin_pct",
    "Free Cash Flow": "free_cash_flow_cr",
    "Debt to Equity": "debt_to_equity",
    "Interest Coverage": "interest_coverage",
    "Market Cap": "market_cap_crore",
    "Enterprise Value": "enterprise_value_crore",
    "P/E Ratio": "pe_ratio",
    "P/B Ratio": "pb_ratio",
    "Dividend Yield %": "dividend_yield_pct",
    "EPS": "eps",
    "Book Value Per Share": "book_value_per_share"
}

selected_metrics = st.multiselect(
    "Choose up to 3 metrics",
    options=list(metric_options.keys()),
    default=["Sales"],
    max_selections=3
)

if len(selected_metrics) == 0:

    st.warning("Please select at least one metric.")

    st.stop()

fig = go.Figure()

colors = [
    "#1f77b4",
    "#2ca02c",
    "#d62728"
]

for i, metric_name in enumerate(selected_metrics):

    column = metric_options[metric_name]

    if column not in company_df.columns:
        continue

    df = company_df[
        ["year", column]
    ].dropna()

    fig.add_trace(

        go.Scatter(

            x=df["year"],

            y=df[column],

            mode="lines+markers",

            name=metric_name,

            line=dict(
                width=3,
                color=colors[i]
            )

        )

    )
# -----------------------------
# YoY Growth Annotation
# -----------------------------

for metric_name in selected_metrics:

    column = metric_options[metric_name]

    if column not in company_df.columns:
        continue

    df = company_df[
        ["year", column]
    ].dropna().copy()

    if len(df) < 2:
        continue

    df["YoY"] = df[column].pct_change() * 100

    for _, row in df.iterrows():

        if pd.isna(row["YoY"]):
            continue

        fig.add_annotation(
            x=row["year"],
            y=row[column],
            text=f"{row['YoY']:.1f}%",
            showarrow=False,
            font=dict(size=9)
        )

# -----------------------------
# Layout
# -----------------------------

fig.update_layout(

    title=f"{company} Financial Trends",

    template="plotly_white",

    height=650,

    hovermode="x unified",

    legend_title="Metrics",

    xaxis_title="Financial Year",

    yaxis_title="Value"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -----------------------------
# Latest Year KPIs
# -----------------------------

latest = company_df.sort_values(
    "year"
).iloc[-1]

st.subheader("Latest Financial Snapshot")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Revenue",
    f"{latest['sales']:,.0f}"
)

c2.metric(
    "Net Profit",
    f"{latest['net_profit']:,.0f}"
)

c3.metric(
    "ROE %",
    round(latest["return_on_equity_pct"], 2)
)

c4.metric(
    "P/E",
    round(latest["pe_ratio"], 2)
)

c5, c6, c7, c8 = st.columns(4)

c5.metric(
    "Debt / Equity",
    round(latest["debt_to_equity"], 2)
)

c6.metric(
    "Interest Coverage",
    round(latest["interest_coverage"], 2)
)

c7.metric(
    "FCF",
    f"{latest['free_cash_flow_cr']:,.0f}"
)

c8.metric(
    "Dividend Yield %",
    round(latest["dividend_yield_pct"], 2)
)

st.divider()

# -----------------------------
# Historical Data
# -----------------------------

st.subheader("Historical Financial Data")

display_cols = [
    "year",
    "sales",
    "net_profit",
    "operating_profit",
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "free_cash_flow_cr",
    "debt_to_equity",
    "interest_coverage",
    "market_cap_crore",
    "enterprise_value_crore",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct"
]

display_cols = [
    c for c in display_cols
    if c in company_df.columns
]

st.dataframe(
    company_df[display_cols].sort_values(
        "year",
        ascending=False
    ),
    use_container_width=True
)

st.success("Trend Analysis loaded successfully.")