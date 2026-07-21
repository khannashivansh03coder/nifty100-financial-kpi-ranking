import pandas as pd
import numpy as np
import os

os.makedirs("output", exist_ok=True)
master = pd.read_csv(
    "data/processed/master_dataset.csv"
)

latest = (
    master
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
    .copy()
)
latest["investment_score"] = 0
latest.loc[
    latest["return_on_equity_pct"] >= 20,
    "investment_score"
] += 20
latest.loc[
    latest["net_profit_margin_pct"] >= 10,
    "investment_score"
] += 15
latest.loc[
    latest["debt_to_equity"] <= 0.5,
    "investment_score"
] += 15
latest.loc[
    latest["free_cash_flow_cr"] > 0,
    "investment_score"
] += 20
latest.loc[
    latest["cash_from_operations_cr"] > 0,
    "investment_score"
] += 15

latest.loc[
    latest["dividend_yield_pct"] >= 1,
    "investment_score"
] += 5
latest.loc[
    latest["pe_ratio"] <= 25,
    "investment_score"
] += 10
latest["recommendation"] = "SELL"

latest.loc[
    latest["investment_score"] >= 70,
    "recommendation"
] = "BUY"

latest.loc[
    (latest["investment_score"] >= 45) &
    (latest["investment_score"] < 70),
    "recommendation"
] = "HOLD"
latest = latest.sort_values(
    "investment_score",
    ascending=False
)

latest["rank"] = range(
    1,
    len(latest) + 1
)
latest.to_excel(
    "output/investment_recommendations.xlsx",
    index=False
)

latest[
    [
        "rank",
        "company_id",
        "company_name",
        "investment_score",
        "recommendation"
    ]
].to_csv(
    "output/top_recommendations.csv",
    index=False
)

print("investment_recommendations.xlsx created")
print("top_recommendations.csv created")
latest["risk_score"] = 0
latest.loc[
    latest["debt_to_equity"] > 1,
    "risk_score"
] += 30
latest.loc[
    latest["free_cash_flow_cr"] < 0,
    "risk_score"
] += 25

latest.loc[
    latest["cash_from_operations_cr"] < 0,
    "risk_score"
] += 25
latest.loc[
    latest["return_on_equity_pct"] < 10,
    "risk_score"
] += 20

latest.loc[
    latest["net_profit_margin_pct"] < 5,
    "risk_score"
] += 15
latest.loc[
    latest["pe_ratio"] > 40,
    "risk_score"
] += 10
latest["confidence_score"] = (
    latest["investment_score"] -
    latest["risk_score"] * 0.5
)

latest["confidence_score"] = (
    latest["confidence_score"]
    .clip(0, 100)
    .round(1)
)
latest["investment_grade"] = "D"

latest.loc[
    latest["confidence_score"] >= 85,
    "investment_grade"
] = "A+"

latest.loc[
    (latest["confidence_score"] >= 75) &
    (latest["confidence_score"] < 85),
    "investment_grade"
] = "A"

latest.loc[
    (latest["confidence_score"] >= 65) &
    (latest["confidence_score"] < 75),
    "investment_grade"
] = "B"

latest.loc[
    (latest["confidence_score"] >= 50) &
    (latest["confidence_score"] < 65),
    "investment_grade"
] = "C"
latest = latest[
    [
        "rank",
        "company_id",
        "company_name",
        "investment_score",
        "risk_score",
        "confidence_score",
        "investment_grade",
        "recommendation"
    ]
]
latest.to_excel(
    "output/investment_recommendations.xlsx",
    index=False
)

latest.to_csv(
    "output/investment_recommendations.csv",
    index=False
)

print("investment_recommendations.xlsx created")
print("investment_recommendations.csv created")