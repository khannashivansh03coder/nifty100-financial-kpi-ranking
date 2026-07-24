import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
os.makedirs("output", exist_ok=True)
os.makedirs("reports", exist_ok=True)
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
features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "asset_turnover",
    "free_cash_flow_cr"
]
cluster_df = latest[
    [
        "company_id",
        "company_name"
    ] + features
].copy()
print(cluster_df[features].isna().sum())

cluster_df.to_csv(
    "output/cluster_input.csv",
    index=False
)

print("cluster_input.csv created")
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
imputer = SimpleImputer(
    strategy="median"
)

cluster_df[features] = imputer.fit_transform(
    cluster_df[features]
)
scaler = StandardScaler()

X = scaler.fit_transform(
    cluster_df[features]
)
inertia = []

for k in range(2, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X)

    inertia.append(model.inertia_)
    plt.figure(figsize=(6,4))

plt.plot(
    range(2,11),
    inertia,
    marker="o"
)

plt.xlabel("Number of Clusters")

plt.ylabel("Inertia")

plt.title("Elbow Method")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "reports/elbow_curve.png"
)

plt.close()
print("elbow_curve.png created")
kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

cluster_df["cluster"] = kmeans.fit_predict(X)
import numpy as np

distances = kmeans.transform(X)

cluster_df["distance_from_centroid"] = [

    distances[i][cluster]

    for i, cluster in enumerate(cluster_df["cluster"])

]
cluster_names = {

    0: "High Growth",

    1: "Value",

    2: "Stable",

    3: "Turnaround",

    4: "High Risk"

}

cluster_df["cluster_name"] = (
    cluster_df["cluster"]
    .map(cluster_names)
)
cluster_df.to_csv(
    "output/company_clusters.csv",
    index=False
)

print("company_clusters.csv created")
cluster_summary = (

    cluster_df

    .groupby("cluster_name")[features]

    .mean()

    .round(2)

)

cluster_summary.to_csv(

    "output/cluster_summary.csv"

)

print("cluster_summary.csv created")
cluster_size = (

    cluster_df["cluster_name"]

    .value_counts()

    .reset_index()

)

cluster_size.columns = [

    "Cluster",

    "Companies"

]

cluster_size.to_csv(

    "output/cluster_size.csv",

    index=False

)

print("cluster_size.csv created")
