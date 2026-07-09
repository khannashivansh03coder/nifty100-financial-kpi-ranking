import os
import numpy as np
import matplotlib.pyplot as plt


class RadarChart:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def create(self):

        metrics = [
            "return_on_equity_pct",
            "operating_profit_margin_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "interest_coverage",
            "asset_turnover",
            "composite_quality_score"
        ]

        # Ensure required columns exist
        for col in metrics:
            if col not in self.df.columns:
                self.df[col] = 0

        if "peer_group" not in self.df.columns:
            raise ValueError(
                "peer_group column not found in dataframe."
            )

        if "company_name" not in self.df.columns:
            raise ValueError(
                "company_name column not found in dataframe."
            )

        os.makedirs(
            "reports/radar_charts",
            exist_ok=True
        )

        self.df = self.df.dropna(
            subset=["company_name", "peer_group"]
        )

        companies = sorted(
            self.df["company_name"].unique()
        )

        for company in companies:

            company_df = self.df[
                self.df["company_name"] == company
            ]

            if company_df.empty:
                continue

            peer = company_df.iloc[0]["peer_group"]

            peer_df = self.df[
                self.df["peer_group"] == peer
            ]

            company_values = []

            peer_values = []

            for metric in metrics:

                company_values.append(
                    company_df[metric].fillna(0).mean()
                )

                peer_values.append(
                    peer_df[metric].fillna(0).mean()
                )

            angles = np.linspace(
                0,
                2 * np.pi,
                len(metrics),
                endpoint=False
            ).tolist()

            company_values += company_values[:1]
            peer_values += peer_values[:1]
            angles += angles[:1]

            fig = plt.figure(figsize=(7, 7))

            ax = plt.subplot(
                111,
                polar=True
            )

            ax.plot(
                angles,
                company_values,
                linewidth=2,
                label=company
            )

            ax.fill(
                angles,
                company_values,
                alpha=0.25
            )

            ax.plot(
                angles,
                peer_values,
                linewidth=2,
                linestyle="--",
                label="Peer Average"
            )

            ax.fill(
                angles,
                peer_values,
                alpha=0.10
            )

            ax.set_xticks(angles[:-1])

            ax.set_xticklabels([
                "ROE",
                "OPM",
                "NPM",
                "Debt/Equity",
                "FCF",
                "Interest",
                "Asset Turnover",
                "Quality Score"
            ])

            plt.title(company)

            plt.legend(
                loc="upper right",
                bbox_to_anchor=(1.3, 1.1)
            )

            filename = (
                company.replace("/", "_")
                       .replace(" ", "_")
            )

            plt.savefig(
                f"reports/radar_charts/{filename}.png",
                dpi=200,
                bbox_inches="tight"
            )

            plt.close()

        print(
            f"Generated {len(companies)} radar charts."
        )