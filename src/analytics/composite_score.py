import pandas as pd


def minmax(series):
    return (series - series.min()) / (series.max() - series.min())


def compute_composite_score(df):

    score = (
        0.35 * minmax(df["return_on_equity_pct"].fillna(0))
        + 0.20 * minmax(df["operating_profit_margin_pct"].fillna(0))
        + 0.15 * minmax(df["asset_turnover"].fillna(0))
        + 0.15 * minmax(df["free_cash_flow_cr"].fillna(0))
        + 0.15 * (1 - minmax(df["debt_to_equity"].fillna(df["debt_to_equity"].max())))
    )

    df["composite_quality_score"] = (score * 100).round(2)

    return df