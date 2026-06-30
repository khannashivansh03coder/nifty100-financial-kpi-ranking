from src.analytics.ratios import (
    current_ratio,
    quick_ratio,
    cash_ratio
)


def test_current_ratio():
    assert current_ratio(200, 100) == 2
    assert current_ratio(200, 0) is None


def test_quick_ratio():
    assert quick_ratio(200, 50, 100) == 1.5
    assert quick_ratio(200, 50, 0) is None


def test_cash_ratio():
    assert cash_ratio(80, 100) == 0.8
    assert cash_ratio(80, 0) is None