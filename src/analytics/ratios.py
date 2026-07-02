# src/analytics/ratios.py

from typing import Optional

def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    if sales == 0:
        return None
    return (net_profit / sales) * 100
def operating_profit_margin(operating_profit: float, sales: float) -> Optional[float]:
    if sales == 0:
        return None
    return (operating_profit / sales) * 100
def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:
    denominator = equity_capital + reserves
    if denominator <= 0:
        return None
    return (net_profit / denominator) * 100
def return_on_capital_employed(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> Optional[float]:
    capital_employed = equity_capital + reserves + borrowings
    if capital_employed <= 0:
        return None
    return (ebit / capital_employed) * 100
def return_on_assets(net_profit: float, total_assets: float) -> Optional[float]:
    if total_assets == 0:
        return None
    return (net_profit / total_assets) * 100
def current_ratio(current_assets, current_liabilities):
    if current_liabilities == 0:
        return None
    return current_assets / current_liabilities


def quick_ratio(current_assets, inventory, current_liabilities):
    if current_liabilities == 0:
        return None
    return (current_assets - inventory) / current_liabilities


def gross_profit_margin(gross_profit, sales):
    """
    Gross Profit Margin = (Gross Profit / Sales) * 100
    Return None if sales is zero or None
    """
    if sales is None or sales == 0:
        return None
    return (gross_profit / sales) * 100


def cash_ratio(cash_and_equivalents, current_liabilities):
    if current_liabilities == 0:
        return None
    return cash_and_equivalents / current_liabilities
def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Debt to Equity Ratio
    borrowings / (equity_capital + reserves)

    Rules:
    - If borrowings = 0 → return 0
    - If equity + reserves <= 0 → return None
    """
    if borrowings == 0:
        return 0

    denominator = equity_capital + reserves
    if denominator <= 0:
        return None

    return borrowings / denominator
def interest_coverage(operating_profit, other_income, interest):
    """
    Interest Coverage Ratio = (Operating Profit + Other Income) / Interest
    """
    if interest == 0:
        return None
    return (operating_profit + other_income) / interest
def asset_turnover(revenue, total_assets):
    """
    Asset Turnover Ratio = Revenue / Total Assets
    """
    if total_assets == 0:
        return None
    return revenue / total_assets