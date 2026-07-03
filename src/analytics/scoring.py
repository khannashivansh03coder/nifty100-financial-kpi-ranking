def score_company(row):
    """
    Simple composite score using financial ratios.
    Higher score = better company
    """

    score = 0

    # Profitability
    score += row.get("net_profit_margin", 0) * 30
    score += row.get("operating_profit_margin", 0) * 25

    # Returns
    score += row.get("return_on_equity", 0) * 20
    score += row.get("return_on_assets", 0) * 15

    # Leverage (penalty)
    score -= row.get("debt_to_equity", 0) * 10

    # Efficiency
    score += row.get("asset_turnover", 0) * 10

    return round(score, 2)