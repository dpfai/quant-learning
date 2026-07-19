"""Signal-driven portfolio construction page."""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

from portfolio.optimizer import PortfolioOptimizer

st.set_page_config(page_title="Portfolio Builder", page_icon="⚖️", layout="wide")
st.title("Portfolio Builder")
st.caption("Turn research signals into constrained paper portfolios; no broker connection.")

symbols = st.text_input("Tickers", "SPY,QQQ,IWM,DIA").upper().replace(" ", "").split(",")
signal_text = st.text_input("Factor signals (comma separated, same order)", "0.5,0.8,0.3,0.2")
max_weight = st.slider("Maximum asset weight", 0.10, 1.00, 0.50, 0.05)
risk_aversion = st.slider("Risk aversion", 0.1, 10.0, 3.0, 0.1)

if st.button("Run optimization", type="primary"):
    try:
        signals = np.asarray([float(value) for value in signal_text.split(",")])
        if len(signals) != len(symbols):
            raise ValueError("Provide exactly one signal per ticker")
        raw = yf.download(symbols, period="2y", auto_adjust=True, progress=False)
        prices = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].rename(columns={"Close": symbols[0]})
        returns = prices.pct_change().dropna()
        expected = pd.Series(signals, index=symbols).rank(pct=True) * 0.10
        covariance = returns.cov() * 252
        optimizer = PortfolioOptimizer(expected, covariance)
        weights = optimizer.optimize(risk_aversion=risk_aversion, max_weight=max_weight)
        report = optimizer.risk_report(weights)
        col1, col2 = st.columns(2)
        col1.subheader("Optimized Weights")
        col1.bar_chart(weights)
        col2.subheader("Risk Report")
        col2.metric("Expected annual return", f"{report['expected_return']:.1%}")
        col2.metric("Annual volatility", f"{report['volatility']:.1%}")
        col2.metric("Normal 95% one-day VaR", f"{report['var_1d']:.2%}")
        st.dataframe(weights.rename("Weight").to_frame(), use_container_width=True)
    except Exception as exc:
        st.error(f"Optimization could not run: {exc}")
