"""Transparent market regime and sector performance helpers."""
from __future__ import annotations

from typing import Dict, Optional

import pandas as pd

from config.settings import SECTOR_ETFS
from utils.data_loader import DataLoader


def get_market_regime(spy_df: pd.DataFrame, vix_value: float) -> Dict[str, object]:
    """Classify the market using VIX and SPY 50/200-day moving averages."""
    if spy_df.empty:
        raise ValueError("SPY data is required to calculate market regime")

    price_column = "Adj Close" if "Adj Close" in spy_df.columns else "Close"
    prices = pd.to_numeric(spy_df[price_column], errors="coerce").dropna()
    if prices.empty:
        raise ValueError("SPY data does not contain valid closing prices")

    latest_price = float(prices.iloc[-1])
    ma50 = float(prices.tail(50).mean()) if len(prices) >= 50 else float("nan")
    ma200 = float(prices.tail(200).mean()) if len(prices) >= 200 else float("nan")
    above_ma50 = bool(pd.notna(ma50) and latest_price > ma50)
    above_ma200 = bool(pd.notna(ma200) and latest_price > ma200)
    below_ma50 = bool(pd.notna(ma50) and latest_price < ma50)
    below_ma200 = bool(pd.notna(ma200) and latest_price < ma200)

    if vix_value < 20 and above_ma50 and above_ma200:
        regime = "RISK-ON"
        description = "Low volatility with SPY above its 50-day and 200-day averages."
    elif vix_value > 25 or (below_ma50 and below_ma200):
        regime = "RISK-OFF"
        description = "Elevated volatility or SPY below both major trend averages."
    else:
        regime = "NEUTRAL"
        description = "Volatility and trend signals are mixed."

    return {
        "regime": regime,
        "vix_level": float(vix_value),
        "spy_above_ma50": above_ma50,
        "spy_above_ma200": above_ma200,
        "description": description,
    }


def get_sector_performance(
    period: str = "3mo",
    loader: Optional[DataLoader] = None,
) -> pd.DataFrame:
    """Download sector ETFs and rank their total return over the period."""
    data_loader = loader or DataLoader()
    rows = []

    for ticker, name in SECTOR_ETFS.items():
        try:
            data = data_loader.download(ticker, period=period)
            price_column = "Adj Close" if "Adj Close" in data.columns else "Close"
            prices = pd.to_numeric(data[price_column], errors="coerce").dropna()
            if len(prices) < 2 or prices.iloc[0] == 0:
                continue
            sector_return = float(prices.iloc[-1] / prices.iloc[0] - 1)
            rows.append({"Ticker": ticker, "Name": name, "Return": sector_return})
        except (ValueError, KeyError):
            continue

    if not rows:
        return pd.DataFrame(columns=["Ticker", "Name", "Return", "Rank"])

    performance = pd.DataFrame(rows)
    performance["Rank"] = (
        performance["Return"].rank(method="min", ascending=False).astype(int)
    )
    return performance.sort_values("Rank").reset_index(drop=True)
