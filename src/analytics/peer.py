import pandas as pd


class PeerRanking:

    def __init__(self, financial_df, peer_df):
        self.financial_df = financial_df.copy()
        self.peer_df = peer_df.copy()

    def calculate(self):

        # Merge financial data with peer groups
        df = self.financial_df.merge(
            self.peer_df,
            on="company_id",
            how="left"
        )

        metrics = [
            "return_on_equity_pct",
            "operating_profit_margin_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "interest_coverage",
            "asset_turnover",
            "market_cap_crore",
            "pe_ratio",
            "dividend_yield_pct"
        ]

        # Convert metrics to numeric
        for metric in metrics:
            if metric in df.columns:
                df[metric] = pd.to_numeric(df[metric], errors="coerce")

        # Fill missing peer groups
        df["peer_group"] = df["peer_group"].fillna("No peer group assigned")

        # Calculate percentile ranks
        for metric in metrics:

            if metric not in df.columns:
                continue

            if metric == "debt_to_equity":

                df[f"{metric}_percentile"] = (
                    1
                    - df.groupby("peer_group")[metric]
                    .rank(method="average", pct=True)
                )

            else:

                df[f"{metric}_percentile"] = (
                    df.groupby("peer_group")[metric]
                    .rank(method="average", pct=True)
                )

        return df