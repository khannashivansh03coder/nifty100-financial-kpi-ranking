import pandas as pd
import numpy as np
import os

master = pd.read_csv("data/processed/master_dataset.csv")

os.makedirs("output", exist_ok=True)

master = master.sort_values("company_id")

latest = master.groupby("company_id").tail(1).copy()
# ============================================
# CFO Quality Score
# ============================================

master["cfo_pat_ratio"] = (
    master["cash_from_operations_cr"] /
    master["net_profit"].replace(0, np.nan)
)

cfo_avg = (
    master.groupby("company_id")["cfo_pat_ratio"]
    .mean()
    .reset_index()
)

cfo_avg.rename(
    columns={
        "cfo_pat_ratio": "cfo_quality_score"
    },
    inplace=True
)

def cfo_label(x):

    if pd.isna(x):
        return "Unknown"

    elif x > 1:
        return "High Quality"

    elif x >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"

cfo_avg["cfo_quality_label"] = (
    cfo_avg["cfo_quality_score"]
    .apply(cfo_label)
)

# ============================================
# CapEx Intensity
# ============================================

latest["capex_intensity_pct"] = (
    latest["capex_cr"].abs() /
    latest["sales"].replace(0, np.nan)
) * 100

def capex_label(x):

    if pd.isna(x):
        return "Unknown"

    elif x < 3:
        return "Asset Light"

    elif x <= 8:
        return "Moderate"

    else:
        return "Capital Intensive"

latest["capex_label"] = (
    latest["capex_intensity_pct"]
    .apply(capex_label)
)

# ============================================
# Distress Flag
# ============================================

latest["distress_flag"] = np.where(

    (latest["cash_from_operations_cr"] < 0) &
    (latest["financing_activity"] > 0),

    "YES",

    "NO"

)

# ============================================
# Deleveraging Flag
# ============================================

latest["deleveraging_flag"] = np.where(

    (latest["financing_activity"] < 0),

    "YES",

    "NO"

)
print("Script executed successfully.")
# ============================================
# Merge Results
# ============================================

latest = latest.merge(
    cfo_avg,
    on="company_id",
    how="left"
)

# ============================================
# FCF Conversion
# ============================================

latest["fcf_conversion_pct"] = (
    latest["free_cash_flow_cr"] /
    latest["cash_from_operations_cr"].replace(0, np.nan)
) * 100

# ============================================
# Dummy 5-Year CAGR
# (Will be replaced after year issue is fixed)
# ============================================

latest["fcf_cagr_5yr"] = np.nan

# ============================================
# Capital Allocation Label
# ============================================

def capital_label(row):

    if row["distress_flag"] == "YES":
        return "Distress"

    if row["deleveraging_flag"] == "YES":
        return "Debt Reduction"

    if row["capex_label"] == "Capital Intensive":
        return "Reinvestor"

    return "Balanced"

latest["capital_allocation_label"] = latest.apply(
    capital_label,
    axis=1
)

# ============================================
# Output File
# ============================================

cols = [

    "company_id",

    "company_name",

    "peer_group_name",

    "cfo_quality_score",

    "cfo_quality_label",

    "capex_intensity_pct",

    "capex_label",

    "fcf_cagr_5yr",

    "fcf_conversion_pct",

    "distress_flag",

    "deleveraging_flag",

    "capital_allocation_label"

]

cols = [c for c in cols if c in latest.columns]

latest[cols].to_excel(
    "output/cashflow_intelligence.xlsx",
    index=False
)

print("cashflow_intelligence.xlsx created")

# ============================================
# Distress Alerts
# ============================================

alerts = latest[
    latest["distress_flag"] == "YES"
][
    [
        "company_id",
        "company_name",
        "cash_from_operations_cr",
        "financing_activity",
        "net_profit"
    ]
]

alerts.to_csv(
    "output/distress_alerts.csv",
    index=False
)

print("distress_alerts.csv created")