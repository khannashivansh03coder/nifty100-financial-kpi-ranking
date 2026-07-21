import os
import pandas as pd

os.makedirs("output", exist_ok=True)
df = pd.read_excel(
    "output/investment_recommendations.xlsx"
)
recommendation_distribution = (
    df["recommendation"]
    .value_counts()
    .reset_index()
)

recommendation_distribution.columns = [
    "Recommendation",
    "Count"
]
grade_distribution = (
    df["investment_grade"]
    .value_counts()
    .reset_index()
)

grade_distribution.columns = [
    "Grade",
    "Count"
]
top_buy = (
    df.sort_values(
        "investment_score",
        ascending=False
    )
    .head(10)
)
high_risk = (
    df.sort_values(
        "risk_score",
        ascending=False
    )
    .head(10)
)
recommendation_distribution.to_csv(
    "output/recommendation_distribution.csv",
    index=False
)

grade_distribution.to_csv(
    "output/grade_distribution.csv",
    index=False
)

top_buy.to_csv(
    "output/top_10_buy.csv",
    index=False
)

high_risk.to_csv(
    "output/high_risk_companies.csv",
    index=False
)

print("recommendation_distribution.csv created")
print("grade_distribution.csv created")
print("top_10_buy.csv created")
print("high_risk_companies.csv created")