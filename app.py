import streamlit as st
import pandas as pd
import os

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Nifty100 Financial KPI Ranking",
    page_icon="📈",
    layout="wide"
)

# -------------------------------
# Load Dataset
# -------------------------------
DATA_PATH = "data/processed/final_company_rankings.csv"

if not os.path.exists(DATA_PATH):
    st.error(f"Dataset not found:\n{DATA_PATH}")
    st.stop()

df = pd.read_csv(DATA_PATH)

# -------------------------------
# Title
# -------------------------------
st.title("📈 Nifty100 Financial KPI Ranking Dashboard")

st.markdown(
    """
This dashboard ranks Nifty100 companies using financial KPIs
and a composite quality score.
"""
)

# -------------------------------
# Metrics
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Companies", len(df))
col2.metric("Highest Score", round(df["composite_quality_score"].max(), 2))
col3.metric("Average Score", round(df["composite_quality_score"].mean(), 2))

st.divider()

# -------------------------------
# Top 10 Chart
# -------------------------------
st.subheader("Top 10 Companies")

top10 = df.sort_values(
    "composite_quality_score",
    ascending=False
).head(10)

st.bar_chart(
    top10.set_index("company_name")[
        "composite_quality_score"
    ]
)

# -------------------------------
# Full Ranking Table
# -------------------------------
st.subheader("Company Rankings")

st.dataframe(
    df.sort_values(
        "composite_quality_score",
        ascending=False
    ),
    use_container_width=True
)

# -------------------------------
# Company Details
# -------------------------------
st.subheader("Company Details")

company = st.selectbox(
    "Select Company",
    sorted(df["company_name"].unique())
)

selected = df[df["company_name"] == company]

st.write(selected)

# -------------------------------
# Radar Chart
# -------------------------------
radar_path = f"reports/radar_charts/{company}_radar.png"

if os.path.exists(radar_path):
    st.subheader("Radar Chart")
    st.image(radar_path, use_container_width=True)
else:
    st.info("Radar chart not found for this company.")