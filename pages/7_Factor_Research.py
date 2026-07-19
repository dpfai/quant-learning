"""Interactive factor IC and quantile research page."""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

from backtest.factor_analysis import calc_ic, quantile_portfolio
from features.factors.momentum import momentum_12_1, momentum_6_1
from features.factors.volatility import realized_volatility

st.set_page_config(page_title="Factor Research", page_icon="🧪", layout="wide")
st.title("Factor Research")
st.caption("Cross-sectional factor diagnostics for learning—not investment advice.")

tickers = st.text_input("Universe", "AAPL,MSFT,NVDA,AMZN,META,GOOGL,JPM,XOM,JNJ,WMT").upper().replace(" ", "").split(",")
factor_name = st.selectbox("Factor", ["12-1 Momentum", "6-1 Momentum", "Low Volatility"])

@st.cache_data(ttl=3600)
def load_prices(symbols):
    raw = yf.download(list(symbols), period="3y", auto_adjust=True, progress=False)
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].rename(columns={"Close": symbols[0]})
    return close.dropna(how="all")

try:
    prices = load_prices(tuple(tickers))
    returns = prices.pct_change()
    if factor_name == "12-1 Momentum":
        factor = momentum_12_1(prices)
    elif factor_name == "6-1 Momentum":
        factor = momentum_6_1(prices)
    else:
        factor = -realized_volatility(returns, 21)
    forward_returns = returns.shift(-1)
    ic = calc_ic(factor, forward_returns).dropna(how="all")
    quantiles = quantile_portfolio(factor, forward_returns).dropna(how="all")
    left, right = st.columns(2)
    left.subheader("Information Coefficient")
    left.line_chart(ic)
    right.subheader("Cumulative Quantile Returns")
    right.line_chart((1 + quantiles.fillna(0)).cumprod() - 1)
    summary = pd.DataFrame({"Mean": ic.mean(), "Std": ic.std(), "Positive Rate": (ic > 0).mean()})
    summary.loc["Q5 minus Q1", "Mean"] = (quantiles.iloc[:, -1] - quantiles.iloc[:, 0]).mean()
    st.subheader("Factor Summary")
    st.dataframe(summary, use_container_width=True)
except Exception as exc:
    st.warning(f"Factor data could not be loaded: {exc}")
