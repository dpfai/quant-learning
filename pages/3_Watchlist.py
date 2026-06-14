"""Watchlist management and cross-asset comparison page."""
from __future__ import annotations

import math

import pandas as pd
import plotly.express as px
import streamlit as st

from features.risk_metrics import calculate_all_risk_metrics
from utils.data_loader import DataLoader
from utils.relative_performance import calculate_relative_performance
from utils.watchlist_manager import WatchlistManager


@st.cache_data(ttl=3600)
def get_watchlist_metrics(tickers: tuple[str, ...]) -> tuple[pd.DataFrame, list[str]]:
    """Load watchlist data and return metrics plus user-facing errors."""
    loader = DataLoader()
    benchmark = loader.download("SPY")
    benchmark_column = "Adj Close" if "Adj Close" in benchmark.columns else "Close"
    results = []
    errors = []

    for ticker in tickers:
        try:
            data = loader.download(ticker)
            price_column = "Adj Close" if "Adj Close" in data.columns else "Close"
            metrics = calculate_all_risk_metrics(
                data[price_column],
                benchmark[benchmark_column],
            )
            relative = calculate_relative_performance(
                data[price_column],
                benchmark[benchmark_column],
            )
            results.append(
                {
                    "Ticker": ticker,
                    "Price": float(data["Close"].iloc[-1]),
                    "5d": relative["stock_5d"],
                    "20d": relative["stock_20d"],
                    "60d": relative["stock_60d"],
                    "YTD": relative["stock_ytd"],
                    "Volatility": metrics["ann_volatility"],
                    "Max DD": metrics["max_drawdown"],
                    "Sharpe": metrics["sharpe_ratio"],
                    "Alpha 20d": relative["alpha_20d"],
                }
            )
        except Exception as exc:
            errors.append(f"{ticker}: {exc}")

    return pd.DataFrame(results), errors


st.title("Watchlist")

manager = WatchlistManager()
watchlists = manager.list_watchlists()

with st.sidebar:
    st.subheader("Manage Watchlists")
    new_watchlist = st.text_input("New watchlist name")
    if st.button("Create Watchlist", use_container_width=True):
        try:
            manager.create_watchlist(new_watchlist)
            st.rerun()
        except (ValueError, KeyError) as exc:
            st.error(str(exc))

if not watchlists:
    st.info("Create a watchlist to begin.")
    st.stop()

selected_watchlist = st.selectbox("Select Watchlist", watchlists)
tickers = manager.get_watchlist(selected_watchlist)

control_col1, control_col2, control_col3 = st.columns([2, 2, 1])
new_ticker = control_col1.text_input("Add Ticker").strip().upper()
if control_col1.button("Add", use_container_width=True) and new_ticker:
    manager.add_ticker(selected_watchlist, new_ticker)
    st.cache_data.clear()
    st.rerun()

remove_ticker = control_col2.selectbox(
    "Remove Ticker",
    tickers,
    index=None,
    placeholder="Select ticker",
)
if control_col2.button("Remove", use_container_width=True) and remove_ticker:
    manager.remove_ticker(selected_watchlist, remove_ticker)
    st.cache_data.clear()
    st.rerun()

if control_col3.button("Delete List", use_container_width=True):
    manager.delete_watchlist(selected_watchlist)
    st.cache_data.clear()
    st.rerun()

if not tickers:
    st.info("Add at least one ticker to calculate watchlist metrics.")
    st.stop()

with st.spinner("Loading watchlist metrics..."):
    metrics_df, load_errors = get_watchlist_metrics(tuple(tickers))

for error in load_errors:
    st.warning(error)

if metrics_df.empty:
    st.warning("No watchlist data could be loaded.")
    st.stop()

sort_options = [column for column in metrics_df.columns if column != "Ticker"]
sort_column = st.selectbox("Sort by", sort_options, index=sort_options.index("YTD"))
ascending = st.checkbox("Ascending", value=False)
sorted_df = metrics_df.sort_values(
    sort_column,
    ascending=ascending,
    na_position="last",
)

formatters = {
    "Price": "${:.2f}",
    "5d": "{:.1%}",
    "20d": "{:.1%}",
    "60d": "{:.1%}",
    "YTD": "{:.1%}",
    "Volatility": "{:.1%}",
    "Max DD": "{:.1%}",
    "Sharpe": "{:.2f}",
    "Alpha 20d": "{:.1%}",
}
st.dataframe(
    sorted_df.style.format(formatters, na_rep="N/A"),
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    "Download Metrics CSV",
    sorted_df.to_csv(index=False).encode("utf-8"),
    file_name=f"{selected_watchlist.lower().replace(' ', '_')}_metrics.csv",
    mime="text/csv",
)

st.subheader("Risk-Return Scatter")
chart_data = metrics_df[
    metrics_df["Volatility"].map(math.isfinite)
    & metrics_df["YTD"].map(math.isfinite)
]
if chart_data.empty:
    st.info("More price history is required for the risk-return chart.")
else:
    figure = px.scatter(
        chart_data,
        x="Volatility",
        y="YTD",
        text="Ticker",
        hover_data=["Sharpe", "Max DD", "Alpha 20d"],
    )
    figure.update_traces(textposition="top center")
    figure.update_xaxes(tickformat=".1%")
    figure.update_yaxes(tickformat=".1%")
    st.plotly_chart(figure, use_container_width=True)
