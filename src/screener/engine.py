import pandas as pd


class ScreenerEngine:

    def __init__(self, df):
        self.df = df.copy()

    def compute_quality_score(self):

        df = self.df.copy()

        score = (
            df["return_on_equity_pct"].fillna(0) * 0.35
            + df["operating_profit_margin_pct"].fillna(0) * 0.20
            + df["net_profit_margin_pct"].fillna(0) * 0.15
            + df["asset_turnover"].fillna(0) * 10 * 0.10
            + df["interest_coverage"].fillna(0) * 0.10
            + (100 - df["debt_to_equity"].fillna(100)) * 0.10
        )

        df["composite_quality_score"] = score

        return df

    def apply_filters(self, filters):

        screened = self.compute_quality_score()

        for metric, value in filters.items():

            if metric not in screened.columns:
                continue

            if metric in [
                "debt_to_equity",
                "pe_ratio",
                "pb_ratio"
            ]:

                screened = screened[
                    screened[metric] <= value
                ]

            else:

                screened = screened[
                    screened[metric] >= value
                ]

        screened = screened.sort_values(
            "composite_quality_score",
            ascending=False
        )

        return screened.reset_index(drop=True)