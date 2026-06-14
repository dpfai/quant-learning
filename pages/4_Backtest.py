"""Interactive educational backtesting page."""
from __future__ import annotations

import math

import plotly.graph_objects as go
import streamlit as st

from backtest.engine import BacktestEngine
from backtest.strategies import (
    bollinger_band_signal,
    ma_crossover_signal,
    rsi_mean_reversion_signal,
)
from utils.data_loader import DataLoader


def metric_value(value: float, percent: bool = False) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value:.1%}" if percent else f"{value:.2f}"


st.title("Backtesting")
st.caption(
    "Signals execute on the following bar and include configurable costs. "
    "Results are educational, not trading advice."
)

ticker = st.text_input("Ticker", "SPY").strip().upper()
strategy = st.selectbox(
    "Strategy",
    ["MA Crossover", "RSI Mean Reversion", "Bollinger Band"],
)
period = st.selectbox("History", ["2y", "5y", "10y"], index=1)
commission = st.number_input(
    "Commission per unit turnover",
    min_value=0.0,
    max_value=0.02,
    value=0.001,
    format="%.4f",
)
slippage = st.number_input(
    "Slippage per unit turnover",
    min_value=0.0,
    max_value=0.02,
    value=0.0005,
    format="%.4f",
)

if strategy == "MA Crossover":
    fast_period = st.slider("Fast Period", 5, 50, 20)
    slow_period = st.slider("Slow Period", 20, 200, 50)

if st.button("Run Backtest", type="primary"):
    try:
        with st.spinner("Running backtest..."):
            data = DataLoader().download(ticker, period=period)
            if strategy == "MA Crossover":
                signals = ma_crossover_signal(data, fast_period, slow_period)
            elif strategy == "RSI Mean Reversion":
                signals = rsi_mean_reversion_signal(data)
            else:
                signals = bollinger_band_signal(data)
            result = BacktestEngine(commission, slippage).run(data["Close"], signals)

        metrics = result["metrics"]
        columns = st.columns(4)
        columns[0].metric("Total Return", metric_value(metrics["total_return"], True))
        columns[1].metric("Sharpe Ratio", metric_value(metrics["sharpe_ratio"]))
        columns[2].metric("Max Drawdown", metric_value(metrics["max_drawdown"], True))
        columns[3].metric("Trades", str(metrics["num_trades"]))

        figure = go.Figure()
        figure.add_trace(
            go.Scatter(
                x=result["equity_curve"].index,
                y=result["equity_curve"],
                name="Strategy Equity",
            )
        )
        figure.update_layout(title=f"{ticker} Strategy Equity Curve", yaxis_title="Equity")
        st.plotly_chart(figure, use_container_width=True)

        if not result["trades"].empty:
            st.subheader("Trades")
            st.dataframe(result["trades"], use_container_width=True)
            st.download_button(
                "Download Trades CSV",
                result["trades"].to_csv().encode("utf-8"),
                file_name=f"{ticker.lower()}_backtest_trades.csv",
                mime="text/csv",
            )
    except Exception as exc:
        st.error(f"Backtest failed: {exc}")
