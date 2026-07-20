import streamlit as st

from src.dashboard.utils.db import (
    get_master,
    get_companies
)

st.set_page_config(layout="wide")

st.title("📄 Annual Reports")

master = get_master()

companies = get_companies()

company = st.selectbox(
    "Select Company",
    sorted(master["company_name"].dropna().unique())
)

company_df = master[
    master["company_name"] == company
]

years = sorted(
    company_df["year"].unique(),
    reverse=True
)

st.subheader("Available Reports")

for yr in years:

    st.markdown(
        f"✅ Annual Report {yr}"
    )

st.info(
    "PDF integration can be connected once report URLs are available."
)