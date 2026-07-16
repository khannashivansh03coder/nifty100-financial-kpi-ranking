import os
import streamlit as st
import pandas as pd

# Project root
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

DATA_DIR = os.path.join(BASE_DIR, "data")

MASTER = os.path.join(DATA_DIR, "processed", "master_dataset.csv")
COMPANIES = os.path.join(DATA_DIR, "raw", "companies.xlsx")
SECTORS = os.path.join(DATA_DIR, "raw", "sectors.xlsx")
PROSCONS = os.path.join(DATA_DIR, "raw", "prosandcons.xlsx")


@st.cache_data(ttl=600)
def get_master():
    return pd.read_csv(MASTER)


@st.cache_data(ttl=600)
def get_companies():
    return pd.read_excel(COMPANIES, header=1)


@st.cache_data(ttl=600)
def get_sectors():
    return pd.read_excel(SECTORS)


@st.cache_data(ttl=600)
def get_proscons():
    return pd.read_excel(PROSCONS, header=1)