import pandas as pd
import os

os.makedirs("output", exist_ok=True)

cashflow = pd.read_excel(
    "output/cashflow_intelligence.xlsx"
)

print(cashflow.head())
# =====================================
# Distribution Summary
# =====================================

distribution = (

    cashflow["capital_allocation_label"]

    .value_counts()

    .reset_index()

)

distribution.columns = [

    "Capital Allocation Pattern",

    "Company Count"

]

distribution.to_csv(

    "output/capital_allocation_distribution.csv",

    index=False

)

print("capital_allocation_distribution.csv created")
# =====================================
# Pattern Changes
# =====================================
#
# Since year data is unavailable,
# create placeholder report.
# Replace after ETL repair.
# =====================================

pattern_changes = cashflow[

    [

        "company_id",

        "company_name",

        "capital_allocation_label"

    ]

].copy()

pattern_changes["previous_pattern"] = "Unknown"

pattern_changes["current_pattern"] = pattern_changes[
    "capital_allocation_label"
]

pattern_changes["changed"] = "Pending Year Fix"

pattern_changes.to_csv(

    "output/pattern_changes.csv",

    index=False

)

print("pattern_changes.csv created")