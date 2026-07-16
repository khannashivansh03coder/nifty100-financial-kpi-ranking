import os
import sys

import streamlit as st

# -----------------------------
# Add project root to Python path
# -----------------------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -----------------------------
# Streamlit Configuration
# -----------------------------
st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Nifty 100 Analytics Dashboard")

st.write("Welcome to the Nifty 100 Analytics Dashboard.")

st.sidebar.title("Navigation")
st.sidebar.success("Select a page from the sidebar.")