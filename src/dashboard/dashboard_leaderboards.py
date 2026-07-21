import os
import pandas as pd

os.makedirs("output/dashboard", exist_ok=True)
master = pd.read_csv(
    "data/processed/master_dataset.csv"
)

recommendation = pd.read_excel(
    "output/investment_recommendations.xlsx"
)

latest = (
    master
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)
top_marketcap = (
    latest[
        [
            "company_id",
            "company_name",
            "market_cap_crore"
        ]
    ]
    .sort_values(
        "market_cap_crore",
        ascending=False
    )
    .head(10)
)
top_roe = (
    latest[
        [
            "company_id",
            "company_name",
            "return_on_equity_pct"
        ]
    ]
    .sort_values(
        "return_on_equity_pct",
        ascending=False
    )
    .head(10)
)
top_dividend = (
    latest[
        [
            "company_id",
            "company_name",
            "dividend_yield_pct"
        ]
    ]
    .sort_values(
        "dividend_yield_pct",
        ascending=False
    )
    .head(10)
)
top_buy = (
    recommendation
    .sort_values(
        "investment_score",
        ascending=False
    )
    .head(10)
)
high_risk = (
    recommendation
    .sort_values(
        "risk_score",
        ascending=False
    )
    .head(10)
)
top_marketcap.to_csv(
    "output/dashboard/top_marketcap.csv",
    index=False
)

top_roe.to_csv(
    "output/dashboard/top_roe.csv",
    index=False
)

top_dividend.to_csv(
    "output/dashboard/top_dividend.csv",
    index=False
)

top_buy.to_csv(
    "output/dashboard/top_buy.csv",
    index=False
)

high_risk.to_csv(
    "output/dashboard/high_risk.csv",
    index=False
)

print("Dashboard leaderboard files created.")
