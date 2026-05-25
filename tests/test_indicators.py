import pandas as pd

from features.indicators import (
    add_all_indicators,
    add_atr,
    add_bollinger_bands,
    add_macd,
    add_moving_averages,
    add_rsi,
)


def sample_prices(rows: int = 260) -> pd.DataFrame:
    index = pd.date_range("2024-01-01", periods=rows, freq="D")
    close = pd.Series(range(100, 100 + rows), index=index, dtype=float)
    return pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": 1000,
        },
        index=index,
    )


def test_moving_averages_add_expected_columns():
    df = add_moving_averages(sample_prices(), periods=[20, 50])

    assert "MA20" in df.columns
    assert "MA50" in df.columns
    assert df["MA20"].notna().sum() > 0


def test_rsi_stays_between_zero_and_one_hundred():
    df = add_rsi(sample_prices(), period=14)
    rsi = df["RSI14"].dropna()

    assert not rsi.empty
    assert rsi.between(0, 100).all()


def test_macd_adds_signal_and_histogram():
    df = add_macd(sample_prices())

    assert {"MACD", "MACD_signal", "MACD_hist"}.issubset(df.columns)


def test_bollinger_bands_have_ordered_bounds():
    df = add_bollinger_bands(sample_prices())
    valid = df.dropna(subset=["BB_upper", "BB_middle", "BB_lower"])

    assert not valid.empty
    assert (valid["BB_upper"] >= valid["BB_middle"]).all()
    assert (valid["BB_middle"] >= valid["BB_lower"]).all()


def test_atr_is_positive():
    df = add_atr(sample_prices())
    atr = df["ATR14"].dropna()

    assert not atr.empty
    assert (atr > 0).all()


def test_add_all_indicators_combines_core_columns():
    df = add_all_indicators(sample_prices())

    expected = {"MA20", "MA50", "MA200", "RSI14", "MACD", "BB_upper", "ATR14"}
    assert expected.issubset(df.columns)
