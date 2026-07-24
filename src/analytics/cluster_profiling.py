import os
import pandas as pd

os.makedirs("output", exist_ok=True)
clusters = pd.read_csv(
    "output/company_clusters.csv"
)
metrics = [

    "return_on_equity_pct",

    "debt_to_equity",

    "operating_profit_margin_pct",

    "asset_turnover",

    "free_cash_flow_cr"

]
cluster_profile = (

    clusters

    .groupby("cluster_name")[metrics]

    .mean()

    .round(2)

)

print(cluster_profile)
cluster_count = (

    clusters

    .groupby("cluster_name")

    .size()

    .reset_index(name="companies")

)

print(cluster_count)
cluster_profile.to_csv(

    "output/cluster_profile.csv"

)

cluster_count.to_csv(

    "output/cluster_company_count.csv",

    index=False

)

print("cluster_profile.csv created")

print("cluster_company_count.csv created")
representatives = (

    clusters

    .sort_values("distance_from_centroid")

    .groupby("cluster_name")

    .first()

    .reset_index()

)
representatives = representatives[
    [
        "cluster_name",
        "company_id",
        "company_name",
        "distance_from_centroid",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "asset_turnover",
        "free_cash_flow_cr"
    ]
]
representatives.to_csv(

    "output/cluster_representatives.csv",

    index=False

)

print("cluster_representatives.csv created")
insights = []

for cluster in cluster_profile.index:

    row = cluster_profile.loc[cluster]

    text = (
        f"{cluster}: "
        f"ROE={row['return_on_equity_pct']:.2f}%, "
        f"Debt/Equity={row['debt_to_equity']:.2f}, "
        f"OPM={row['operating_profit_margin_pct']:.2f}%, "
        f"Asset Turnover={row['asset_turnover']:.2f}, "
        f"FCF={row['free_cash_flow_cr']:.2f}"
    )

    insights.append(text)
    pd.DataFrame(

    {"Cluster Insight": insights}

).to_csv(

    "output/cluster_insights.csv",

    index=False

)

print("cluster_insights.csv created")
import matplotlib.pyplot as plt
plt.figure(figsize=(7,5))

cluster_count.plot(
    kind="bar",
    x="cluster_name",
    y="companies",
    legend=False,
    color="steelblue"
)

plt.title("Companies per Cluster")

plt.xlabel("Cluster")

plt.ylabel("Number of Companies")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "reports/cluster_size.png"
)

plt.close()

print("cluster_size.png created")
plt.figure(figsize=(7,5))

cluster_profile["return_on_equity_pct"].plot(
    kind="bar",
    color="green"
)

plt.title("Average ROE by Cluster")

plt.ylabel("ROE %")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "reports/cluster_roe.png"
)

plt.close()

print("cluster_roe.png created")
plt.figure(figsize=(7,5))

cluster_profile["debt_to_equity"].plot(
    kind="bar",
    color="orange"
)

plt.title("Average Debt to Equity")

plt.ylabel("Debt/Equity")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "reports/cluster_debt.png"
)

plt.close()

print("cluster_debt.png created")
dashboard = clusters.merge(

    cluster_count,

    on="cluster_name",

    how="left"

)

dashboard.to_csv(

    "output/dashboard_clusters.csv",

    index=False

)

print("dashboard_clusters.csv created")
print("\nDay 37 Completed Successfully")