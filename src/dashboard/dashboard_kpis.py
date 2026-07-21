import os
import pandas as pd

os.makedirs("output/dashboard", exist_ok=True)
master = pd.read_csv(
    "data/processed/master_dataset.csv"
)

recommendation = pd.read_excel(
    "output/investment_recommendations.xlsx"
)

cashflow = pd.read_excel(
    "output/cashflow_intelligence.xlsx"
)

capital = pd.read_csv(
    "output/capital_allocation_distribution.csv"
)
latest = (
    master
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)
dashboard = pd.DataFrame({

    "Total Companies":[
        latest["company_id"].nunique()
    ],

    "Total Market Cap":[
        latest["market_cap_crore"].sum()
    ],

    "Average PE":[
        latest["pe_ratio"].mean()
    ],

    "Average ROE":[
        latest["return_on_equity_pct"].mean()
    ],

    "Average Dividend Yield":[
        latest["dividend_yield_pct"].mean()
    ],

    "Positive Free Cash Flow":[
        (latest["free_cash_flow_cr"]>0).sum()
    ],

    "BUY Companies":[
        (recommendation["recommendation"]=="BUY").sum()
    ],

    "HOLD Companies":[
        (recommendation["recommendation"]=="HOLD").sum()
    ],

    "SELL Companies":[
        (recommendation["recommendation"]=="SELL").sum()
    ]

})
dashboard.to_csv(
    "output/dashboard/dashboard_kpis.csv",
    index=False
)

print("dashboard_kpis.csv created")