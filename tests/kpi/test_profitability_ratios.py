import math

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets
)

def test_net_profit_margin_normal():
    assert math.isclose(net_profit_margin(100, 1000), 10.0)

def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None

def test_operating_profit_margin_normal():
    assert math.isclose(operating_profit_margin(200, 1000), 20.0)

def test_return_on_equity_negative_equity():
    assert return_on_equity(100, -50, 10) is None

def test_return_on_capital_employed_normal():
    assert math.isclose(
        return_on_capital_employed(200, 500, 300, 200),
        20.0
    )

def test_return_on_assets_zero_assets():
    assert return_on_assets(100, 0) is None