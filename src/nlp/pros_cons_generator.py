import pandas as pd
import numpy as np
from pathlib import Path

# ------------------------------------
# Paths
# ------------------------------------

ROOT = Path(__file__).resolve().parents[2]

MASTER = ROOT / "data" / "processed" / "master_dataset.csv"

OUTPUT = ROOT / "output"

OUTPUT.mkdir(exist_ok=True)

# ------------------------------------
# Load Dataset
# ------------------------------------

master = pd.read_csv(MASTER)

master = master.sort_values(
    ["company_id", "year"]
)

results = []

# ------------------------------------
# Helper
# ------------------------------------

def add_rule(company,
             rule_type,
             rule_id,
             text,
             confidence):

    results.append({

        "company_id": company,

        "type": rule_type,

        "rule_id": rule_id,

        "text": text,

        "confidence_pct": confidence

    })


# ------------------------------------
# Companies
# ------------------------------------

companies = master["company_id"].unique()

# ====================================
# PRO RULE 1
# ROE >20%
# ====================================

def pro_rule_1(df):

    latest = df.iloc[-1]

    if latest["return_on_equity_pct"] > 20:

        add_rule(

            latest["company_id"],

            "pro",

            "P1",

            "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",

            95

        )

# ====================================
# PRO RULE 2
# Positive FCF
# ====================================

def pro_rule_2(df):

    latest = df.iloc[-1]

    if latest["free_cash_flow_cr"] > 0:

        add_rule(

            latest["company_id"],

            "pro",

            "P2",

            "Strong positive free cash flow reflects healthy cash generation from business operations.",

            90

        )

# ====================================
# PRO RULE 3
# Debt Free
# ====================================

def pro_rule_3(df):

    latest = df.iloc[-1]

    if latest["debt_to_equity"] == 0:

        add_rule(

            latest["company_id"],

            "pro",

            "P3",

            "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",

            100

        )

# ====================================
# PRO RULE 4
# OPM
# ====================================

def pro_rule_4(df):

    latest = df.iloc[-1]

    if latest["operating_profit_margin_pct"] > 25:

        add_rule(

            latest["company_id"],

            "pro",

            "P4",

            "Operating profit margin above 25% indicates strong pricing power and cost discipline.",

            92

        )

# ====================================
# PRO RULE 5
# Interest Coverage
# ====================================

def pro_rule_5(df):

    latest = df.iloc[-1]

    if latest["interest_coverage"] > 10:

        add_rule(

            latest["company_id"],

            "pro",

            "P5",

            "Very high interest coverage reflects negligible financial stress from debt servicing.",

            93

        )

# ====================================
# PRO RULE 6
# Dividend + FCF
# ====================================

def pro_rule_6(df):

    latest = df.iloc[-1]

    if (

        latest["dividend_yield_pct"] > 2

        and

        latest["free_cash_flow_cr"] > 0

    ):

        add_rule(

            latest["company_id"],

            "pro",

            "P6",

            "Dividend yield above 2% supported by positive free cash flow reflects sustainable shareholder returns.",

            88

        )

# ====================================
# PRO RULE 7
# ROE improving
# ====================================

def pro_rule_7(df):

    if len(df) < 3:

        return

    roe = df["return_on_equity_pct"].tail(3).values

    if roe[0] < roe[1] < roe[2]:

        add_rule(

            df.iloc[-1]["company_id"],

            "pro",

            "P7",

            "Return on equity has improved for three consecutive years indicating strengthening business quality.",

            87

        )

# ====================================
# PRO RULE 8
# Borrowings reducing
# ====================================

def pro_rule_8(df):

    if len(df) < 3:

        return

    debt = df["borrowings"].tail(3).values

    if debt[0] > debt[1] > debt[2]:

        add_rule(

            df.iloc[-1]["company_id"],

            "pro",

            "P8",

            "Borrowings have reduced consistently over recent years indicating improving balance sheet strength.",

            86

        )
# ====================================
# CON RULE 1
# Debt / Equity > 2
# ====================================

def con_rule_1(df):

    latest = df.iloc[-1]

    if latest["debt_to_equity"] > 2:

        add_rule(

            latest["company_id"],

            "con",

            "C1",

            f"Debt-to-equity ratio of {latest['debt_to_equity']:.2f} is elevated and warrants monitoring.",

            94

        )

# ====================================
# CON RULE 2
# Negative FCF
# ====================================

def con_rule_2(df):

    latest = df.iloc[-1]

    if latest["free_cash_flow_cr"] < 0:

        add_rule(

            latest["company_id"],

            "con",

            "C2",

            "Negative free cash flow raises concern regarding cash generation quality.",

            92

        )

# ====================================
# CON RULE 3
# Net Loss
# ====================================

def con_rule_3(df):

    latest = df.iloc[-1]

    if latest["net_profit"] < 0:

        add_rule(

            latest["company_id"],

            "con",

            "C3",

            "Company reported a net loss in the latest financial year.",

            98

        )

# ====================================
# CON RULE 4
# Interest Coverage
# ====================================

def con_rule_4(df):

    latest = df.iloc[-1]

    if latest["interest_coverage"] < 1.5:

        add_rule(

            latest["company_id"],

            "con",

            "C4",

            "Interest coverage below 1.5x indicates elevated debt servicing risk.",

            95

        )

# ====================================
# CON RULE 5
# Dividend Payout
# ====================================

def con_rule_5(df):

    latest = df.iloc[-1]

    if latest["dividend_payout_ratio_pct"] > 100:

        add_rule(

            latest["company_id"],

            "con",

            "C5",

            "Dividend payout above 100% may not be sustainable over the long term.",

            90

        )

# ====================================
# CON RULE 6
# Debt Increasing
# ====================================

def con_rule_6(df):

    if len(df) < 3:

        return

    debt = df["borrowings"].tail(3).values

    if debt[0] < debt[1] < debt[2]:

        add_rule(

            df.iloc[-1]["company_id"],

            "con",

            "C6",

            "Borrowings have increased continuously over recent years indicating rising financial leverage.",

            88

        )

# ====================================
# CON RULE 7
# ROE Declining
# ====================================

def con_rule_7(df):

    if len(df) < 3:

        return

    roe = df["return_on_equity_pct"].tail(3).values

    if roe[0] > roe[1] > roe[2]:

        add_rule(

            df.iloc[-1]["company_id"],

            "con",

            "C7",

            "Return on equity has declined for three consecutive years.",

            86

        )

# ====================================
# CON RULE 8
# OPM Declining
# ====================================

def con_rule_8(df):

    if len(df) < 3:

        return

    opm = df["operating_profit_margin_pct"].tail(3).values

    if opm[0] > opm[1] > opm[2]:

        add_rule(

            df.iloc[-1]["company_id"],

            "con",

            "C8",

            "Operating margins have declined for three consecutive years indicating pressure on profitability.",

            87

        )

# ====================================
# FALLBACK RULES
# ====================================

def ensure_minimum_rules(company):

    company_rows = [

        r for r in results

        if r["company_id"] == company

    ]

    pros = [

        r for r in company_rows

        if r["type"] == "pro"

    ]

    cons = [

        r for r in company_rows

        if r["type"] == "con"

    ]

    if len(pros) == 0:

        add_rule(

            company,

            "pro",

            "PF",

            "Business continues to maintain stable operations based on available financial information.",

            65

        )

    if len(cons) == 0:

        add_rule(

            company,

            "con",

            "CF",

            "Continuous monitoring of future financial performance is recommended.",

            65

        )
    # ====================================
# Execute Rules
# ====================================

for company in companies:

    df = master[
        master["company_id"] == company
    ].copy()

    df = df.sort_values("year")

    # ---------- Pro Rules ----------

    pro_rule_1(df)
    pro_rule_2(df)
    pro_rule_3(df)
    pro_rule_4(df)
    pro_rule_5(df)
    pro_rule_6(df)
    pro_rule_7(df)
    pro_rule_8(df)

    # ---------- Con Rules ----------

    con_rule_1(df)
    con_rule_2(df)
    con_rule_3(df)
    con_rule_4(df)
    con_rule_5(df)
    con_rule_6(df)
    con_rule_7(df)
    con_rule_8(df)

    # Ensure every company has at least
    # one Pro and one Con

    ensure_minimum_rules(company)

# ====================================
# Create DataFrame
# ====================================

pros_cons = pd.DataFrame(results)

# Keep confidence > 60 only

pros_cons = pros_cons[
    pros_cons["confidence_pct"] > 60
]

# Remove duplicates

pros_cons = pros_cons.drop_duplicates(
    subset=[
        "company_id",
        "rule_id"
    ]
)

# Sort nicely

pros_cons = pros_cons.sort_values(
    [
        "company_id",
        "type",
        "confidence_pct"
    ],
    ascending=[
        True,
        True,
        False
    ]
)

# ====================================
# Save CSV
# ====================================

pros_cons.to_csv(

    OUTPUT / "pros_cons_generated.csv",

    index=False

)

# ====================================
# Validation
# ====================================

validation = (

    pros_cons

    .groupby(
        ["company_id", "type"]
    )

    .size()

    .unstack(fill_value=0)

)

missing = validation[
    (validation.get("pro", 0) == 0)
    |
    (validation.get("con", 0) == 0)
]

print("=" * 60)
print("Pros/Cons Generation Complete")
print("=" * 60)

print(f"Total Rules Generated : {len(pros_cons)}")
print(f"Companies Covered     : {pros_cons['company_id'].nunique()}")

if len(missing) == 0:

    print("✅ Every company has at least one Pro and one Con.")

else:

    print("⚠ Companies Missing Rules:")
    print(missing)

print("\nFile Saved:")
print(OUTPUT / "pros_cons_generated.csv")