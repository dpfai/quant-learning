"""Tests for market regime and sector ranking helpers."""

import pandas as pd
import pytest

from utils.market_regime import get_market_regime, get_sector_performance


def price_frame(values) -> pd.DataFrame:
    index = pd.date_range("2024-01-01", periods=len(values), freq="D")
    return pd.DataFrame({"Close": values, "Adj Close": values}, index=index)


def test_risk_on_requires_low_vix_and_both_positive_trends():
    spy = price_frame(range(100, 320))

    regime = get_market_regime(spy, vix_value=15)

    assert regime["regime"] == "RISK-ON"
    assert regime["spy_above_ma50"]
    assert regime["spy_above_ma200"]


def test_high_vix_is_risk_off_even_with_positive_trend():
    spy = price_frame(range(100, 320))

    regime = get_market_regime(spy, vix_value=30)

    assert regime["regime"] == "RISK-OFF"


def test_mixed_signals_are_neutral():
    prices = list(range(100, 319)) + [250]
    spy = price_frame(prices)

    regime = get_market_regime(spy, vix_value=22)

    assert regime["regime"] == "NEUTRAL"


def test_sector_performance_ranks_highest_return_first():
    class FakeLoader:
        def download(self, ticker, period):
            returns = {
                "XLK": 0.20,
                "XLF": 0.10,
            }
            if ticker not in returns:
                raise ValueError("No fixture")
            return price_frame([100, 100 * (1 + returns[ticker])])

    performance = get_sector_performance(loader=FakeLoader())

    assert list(performance["Ticker"]) == ["XLK", "XLF"]
    assert list(performance["Rank"]) == [1, 2]
    assert performance.iloc[0]["Return"] == pytest.approx(0.20)
