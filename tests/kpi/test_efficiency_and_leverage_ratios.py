from typing import Optional


# =========================
# PROFITABILITY RATIOS
# =========================

def gross_profit_margin(revenue: float, cost_of_goods_sold: float) -> float:
    if revenue == 0:
        return 0.0
    return (revenue - cost_of_goods_sold) / revenue


def net_profit_margin(net_profit: float, revenue: float) -> float:
    if revenue == 0:
        return 0.0
    return net_profit / revenue


def operating_profit_margin(operating_profit: float, revenue: float) -> float:
    if revenue == 0:
        return 0.0
    return operating_profit / revenue


# =========================
# RETURN RATIOS
# =========================

def return_on_equity(net_profit: float, equity: float) -> float:
    if equity == 0:
        return 0.0
    return net_profit / equity


def return_on_assets(net_profit: float, total_assets: float) -> float:
    if total_assets == 0:
        return 0.0
    return net_profit / total_assets


def return_on_capital_employed(ebit: float, capital_employed: float) -> float:
    if capital_employed == 0:
        return 0.0
    return ebit / capital_employed


# =========================
# LIQUIDITY RATIOS
# =========================

def current_ratio(current_assets: float, current_liabilities: float) -> float:
    if current_liabilities == 0:
        return 0.0
    return current_assets / current_liabilities


def quick_ratio(
    current_assets: float,
    inventory: float,
    current_liabilities: float
) -> float:
    if current_liabilities == 0:
        return 0.0
    return (current_assets - inventory) / current_liabilities


def cash_ratio(
    cash_and_equivalents: float,
    current_liabilities: float
) -> float:
    if current_liabilities == 0:
        return 0.0
    return cash_and_equivalents / current_liabilities


# =========================
# LEVERAGE & EFFICIENCY
# =========================

def debt_to_equity(total_debt: float, equity: float) -> float:
    if equity == 0:
        return 0.0
    return total_debt / equity


def interest_coverage(ebit: float, interest: float) -> float:
    if interest == 0:
        return 0.0
    return ebit / interest


def asset_turnover(revenue: float, total_assets: float) -> float:
    if total_assets == 0:
        return 0.0
    return revenue / total_assets