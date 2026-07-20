import pandas as pd
import os

MASTER = "data/processed/master_dataset.csv"

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------
# Load Dataset
# -----------------------------------

master = pd.read_csv(MASTER)

# -----------------------------------
# Latest Financial Year
# -----------------------------------

latest_year = master["year"].max()

latest = master[
    master["year"] == latest_year
].copy()

# -----------------------------------
# FCF Yield
# -----------------------------------

latest["FCF_yield_pct"] = (
    latest["free_cash_flow_cr"]
    / latest["market_cap_crore"]
) * 100

# -----------------------------------
# Sector Median PE
# -----------------------------------

sector_pe = (

    latest

    .groupby("peer_group_name")["pe_ratio"]

    .median()

    .reset_index()

    .rename(
        columns={
            "pe_ratio": "sector_median_pe"
        }
    )

)

latest = latest.merge(

    sector_pe,

    on="peer_group_name",

    how="left"

)

# -----------------------------------
# PE Difference
# -----------------------------------

latest["PE_vs_sector_median_pct"] = (

    (

        latest["pe_ratio"]

        - latest["sector_median_pe"]

    )

    / latest["sector_median_pe"]

) * 100

# -----------------------------------
# Valuation Flag
# -----------------------------------

def valuation_flag(row):

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    elif row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    else:
        return "Fair"

latest["flag"] = latest.apply(
    valuation_flag,
    axis=1
)

# -----------------------------------
# Output Columns
# -----------------------------------

valuation = latest[
    [
        "company_id",
        "company_name",
        "peer_group_name",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "FCF_yield_pct",
        "sector_median_pe",
        "PE_vs_sector_median_pct",
        "flag"
    ]
]

valuation.rename(
    columns={
        "peer_group_name": "sector",
        "sector_median_pe": "5yr_median_PE"
    },
    inplace=True
)

# -----------------------------------
# Save Excel
# -----------------------------------

valuation.to_excel(
    "output/valuation_summary.xlsx",
    index=False
)

# -----------------------------------
# Save Flags
# -----------------------------------

flags = valuation[
    valuation["flag"] != "Fair"
]

flags.to_csv(
    "output/valuation_flags.csv",
    index=False
)

print("valuation_summary.xlsx created")

print("valuation_flags.csv created")