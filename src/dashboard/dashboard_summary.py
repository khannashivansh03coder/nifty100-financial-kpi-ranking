import os
import pandas as pd

os.makedirs("output/dashboard", exist_ok=True)
recommendation = pd.read_excel(
    "output/investment_recommendations.xlsx"
)

master = pd.read_csv(
    "data/processed/master_dataset.csv"
)

latest = (
    master
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)
recommendation_summary = (
    recommendation["recommendation"]
    .value_counts()
    .reset_index()
)

recommendation_summary.columns = [
    "Recommendation",
    "Count"
]
grade_summary = (
    recommendation["investment_grade"]
    .value_counts()
    .reset_index()
)

grade_summary.columns = [
    "Investment Grade",
    "Count"
]
financial_summary = pd.DataFrame({

    "Average ROE":[
        latest["return_on_equity_pct"].mean()
    ],

    "Average PE":[
        latest["pe_ratio"].mean()
    ],

    "Average Dividend Yield":[
        latest["dividend_yield_pct"].mean()
    ],

    "Average Net Profit Margin":[
        latest["net_profit_margin_pct"].mean()
    ],

    "Average Debt to Equity":[
        latest["debt_to_equity"].mean()
    ]

})
recommendation_summary.to_csv(
    "output/dashboard/recommendation_summary.csv",
    index=False
)

grade_summary.to_csv(
    "output/dashboard/grade_summary.csv",
    index=False
)

financial_summary.to_csv(
    "output/dashboard/financial_summary.csv",
    index=False
)

print("Dashboard summary files created.")
