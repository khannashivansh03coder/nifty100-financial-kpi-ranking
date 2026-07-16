import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_master,
    get_companies,
    get_proscons
)

st.title("🏢 Company Profile")

master = get_master()
companies = get_companies()
proscons = get_proscons()

# ---------------- Sidebar ---------------- #

years = sorted(master["year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Financial Year",
    years,
    index=len(years) - 1
)

master = master[
    master["year"] == selected_year
]

# ---------------- Company Selection ---------------- #

company_list = sorted(
    master["company_name"].dropna().unique()
)

selected_company = st.selectbox(
    "Select Company",
    company_list
)

company = master[
    master["company_name"] == selected_company
]

if company.empty:
    st.warning("Ticker not found.")
    st.stop()

row = company.iloc[0]

# ---------------- Company Information ---------------- #

st.header(row["company_name"])

info = companies[
    companies["company_name"] == row["company_name"]
]

if not info.empty:

    info = info.iloc[0]

    st.write("### About Company")
    st.write(info["about_company"])

    st.write("**Website:**", info["website"])

# ---------------- KPI Cards ---------------- #

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

c1.metric(
    "ROE %",
    round(row["return_on_equity_pct"], 2)
)

c2.metric(
    "ROCE %",
    round(info["roce_percentage"], 2)
)

c3.metric(
    "Net Profit Margin",
    round(row["net_profit_margin_pct"], 2)
)

c4.metric(
    "Debt / Equity",
    round(row["debt_to_equity"], 2)
)

c5.metric(
    "Revenue",
    round(row["sales"], 2)
)

c6.metric(
    "Free Cash Flow",
    round(row["free_cash_flow_cr"], 2)
)

st.divider()

# ---------------- Historical Data ---------------- #

history = get_master()

history = history[
    history["company_name"] == selected_company
]

# Revenue

st.subheader("Revenue History")

fig = px.bar(
    history,
    x="year",
    y="sales",
    title="Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ROE

st.subheader("ROE Trend")

fig = px.line(
    history,
    x="year",
    y="return_on_equity_pct",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Net Profit Margin

st.subheader("Net Profit Margin")

fig = px.bar(
    history,
    x="year",
    y="net_profit_margin_pct"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ROCE

st.subheader("ROCE Trend")

if "roce_percentage" in history.columns:

    fig = px.line(
        history,
        x="year",
        y="roce_percentage",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ---------------- Pros & Cons ---------------- #

st.subheader("Pros & Cons")

pc = proscons[
    proscons["company_id"] == row["company_id"]
]

if not pc.empty:

    pc = pc.iloc[0]

    if "pros" in pc.index:
        st.success(pc["pros"])

    if "cons" in pc.index:
        st.error(pc["cons"])

else:

    st.info("Pros & Cons not available.")