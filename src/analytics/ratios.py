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