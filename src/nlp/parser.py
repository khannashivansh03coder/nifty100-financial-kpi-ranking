import re
import pandas as pd
from pathlib import Path

# ----------------------------
# Paths
# ----------------------------

ROOT = Path(__file__).resolve().parents[2]

RAW = ROOT / "data" / "raw" / "analysis.xlsx"
OUTPUT = ROOT / "output"

OUTPUT.mkdir(exist_ok=True)

# ----------------------------
# Read Excel
# ----------------------------

analysis = pd.read_excel(RAW)

# Fix header row
analysis.columns = analysis.iloc[0]
analysis = analysis.iloc[1:].reset_index(drop=True)

# ----------------------------
# Regex
# ----------------------------

pattern = re.compile(r"(\d+)\s*Years?:?\s*([-\d.]+)%")

metrics = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

parsed_rows = []
failed_rows = []

# ----------------------------
# Parse
# ----------------------------

for _, row in analysis.iterrows():

    company = row["company_id"]

    for metric in metrics:

        value = str(row[metric]).strip()

        match = pattern.search(value)

        if match:

            parsed_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric,
                    "period_years": int(match.group(1)),
                    "value_pct": float(match.group(2)),
                }
            )

        else:

            failed_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric,
                    "raw_text": value,
                }
            )

# ----------------------------
# Save
# ----------------------------

parsed = pd.DataFrame(parsed_rows)

failures = pd.DataFrame(failed_rows)

parsed.to_csv(
    OUTPUT / "analysis_parsed.csv",
    index=False,
)

failures.to_csv(
    OUTPUT / "parse_failures.csv",
    index=False,
)

print("analysis_parsed.csv created")
print("parse_failures.csv created")
print("Parsed:", len(parsed))
print("Failures:", len(failures))