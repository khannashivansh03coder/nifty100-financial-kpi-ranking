import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.dashboard.utils.db import (
    get_master,
    get_companies
)

st.title("🤝 Peer Comparison")

master = get_master()
companies = get_companies()

# ---------------- Year ---------------- #

years = sorted(master["year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Financial Year",
    years,
    index=len(years)-1
)

master = master[
    master["year"] == selected_year
]

# ---------------- Peer Group ---------------- #

if "peer_group" not in master.columns:

    st.error(
        "peer_group column not found in master dataset."
    )

    st.stop()

peer_groups = sorted(
    master["peer_group"].dropna().unique()
)

selected_group = st.selectbox(
    "Peer Group",
    peer_groups
)

peer_df = master[
    master["peer_group"] == selected_group
]

# ---------------- Company ---------------- #

company = st.selectbox(
    "Company",
    sorted(peer_df["company_name"].unique())
)

company_df = peer_df[
    peer_df["company_name"] == company
]

if company_df.empty:

    st.warning("No data available.")

    st.stop()

company_df = company_df.iloc[0]

# ---------------- Radar Chart ---------------- #

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "interest_coverage",
    "pe_ratio",
    "pb_ratio"
]

metrics = [
    m for m in metrics
    if m in peer_df.columns
]

company_values = []

peer_values = []

for metric in metrics:

    company_values.append(
        company_df[metric]
    )

    peer_values.append(
        peer_df[metric].mean()
    )

company_values.append(company_values[0])
peer_values.append(peer_values[0])

labels = metrics + [metrics[0]]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=labels,
        fill="toself",
        name=company
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_values,
        theta=labels,
        fill="toself",
        name="Peer Average"
    )
)

fig.update_layout(

    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),

    showlegend=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------- Table ---------------- #

st.subheader("Peer Comparison")

cols = [

    "company_name",

    "return_on_equity_pct",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "interest_coverage",

    "pe_ratio",

    "pb_ratio"

]

cols = [
    c for c in cols
    if c in peer_df.columns
]

table = peer_df[cols]

def highlight(row):

    if row["company_name"] == company:

        return [
            "background-color:#D6F5D6"
        ] * len(row)

    return [
        ""
    ] * len(row)

st.dataframe(

    table.style.apply(

        highlight,

        axis=1

    ),

    use_container_width=True

)