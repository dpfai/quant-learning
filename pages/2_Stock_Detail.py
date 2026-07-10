"""
Stock detail page with price chart and technical indicators.
"""
import math

import streamlit as st

from config.settings import DEFAULT_PERIOD, RISK_FREE_RATE
from features.indicators import add_all_indicators
from features.risk_metrics import calculate_all_risk_metrics, calculate_returns
from utils.chart_builder import ChartBuilder
from utils.data_loader import DataLoader
from utils.export import dataframe_to_csv
from utils.relative_performance import (
    calculate_information_ratio,
    calculate_relative_performance,
    calculate_tracking_error,
)


def format_metric(value: float, suffix: str = "", decimals: int = 2) -> str:
    """Format finite metrics while keeping undefined values explicit."""
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value:.{decimals}f}{suffix}"


st.title("Stock Detail")

ticker = st.sidebar.text_input("Ticker", value="SPY").strip().upper()
period = st.sidebar.selectbox("History", ["6mo", "1y", "2y", "5y"], index=2)

if ticker:
    loader = DataLoader()
    try:
        with st.spinner(f"Loading {ticker}..."):
            df = loader.download(ticker, period=period or DEFAULT_PERIOD)
            df = add_all_indicators(df)

        fig = ChartBuilder.candlestick(df, title=f"{ticker} Price", show_volume=True)
        fig = ChartBuilder.add_moving_averages(fig, df, periods=[20, 50, 200])
        st.plotly_chart(fig, use_container_width=True)

        latest = df.iloc[-1]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Close", f"{latest['Close']:.2f}")
        col2.metric("RSI14", f"{latest['RSI14']:.1f}" if latest["RSI14"] == latest["RSI14"] else "N/A")
        col3.metric("MACD", f"{latest['MACD']:.2f}")
        col4.metric("ATR14", f"{latest['ATR14']:.2f}" if latest["ATR14"] == latest["ATR14"] else "N/A")

        st.subheader("Indicator Snapshot")
        indicator_cols = [
            "Close",
            "MA20",
            "MA50",
            "MA200",
            "RSI14",
            "MACD",
            "MACD_signal",
            "BB_upper",
            "BB_middle",
            "BB_lower",
            "ATR14",
        ]
        available_cols = [col for col in indicator_cols if col in df.columns]
        st.dataframe(df[available_cols].tail(20), use_container_width=True)
        st.download_button(
            "Download Price And Indicator CSV",
            dataframe_to_csv(df),
            file_name=f"{ticker.lower()}_{period}_analysis.csv",
            mime="text/csv",
        )

        st.subheader("Risk Metrics")
        with st.spinner("Calculating risk metrics..."):
            benchmark = df if ticker == "SPY" else loader.download("SPY", period=period)
            price_column = "Adj Close" if "Adj Close" in df.columns else "Close"
            benchmark_column = (
                "Adj Close" if "Adj Close" in benchmark.columns else "Close"
            )
            metrics = calculate_all_risk_metrics(
                df[price_column],
                benchmark[benchmark_column],
                risk_free_rate=RISK_FREE_RATE,
            )

        risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)
        risk_col1.metric(
            "Ann. Return",
            format_metric(metrics["ann_return"] * 100, "%", 1),
        )
        risk_col2.metric(
            "Ann. Volatility",
            format_metric(metrics["ann_volatility"] * 100, "%", 1),
        )
        risk_col3.metric(
            "Max Drawdown",
            format_metric(metrics["max_drawdown"] * 100, "%", 1),
        )
        risk_col4.metric(
            "Sharpe Ratio",
            format_metric(metrics["sharpe_ratio"]),
        )

        risk_col5, risk_col6, risk_col7 = st.columns(3)
        risk_col5.metric(
            "Sortino Ratio",
            format_metric(metrics["sortino_ratio"]),
        )
        risk_col6.metric(
            "Beta (vs SPY)",
            format_metric(metrics["beta"]),
        )
        risk_col7.metric(
            "Win Rate",
            format_metric(metrics["win_rate"] * 100, "%", 1),
        )

        if metrics["max_dd_start"] is not None and metrics["max_dd_end"] is not None:
            st.caption(
                "Maximum drawdown period: "
                f"{metrics['max_dd_start'].date()} to {metrics['max_dd_end'].date()}"
            )

        st.subheader("Relative Performance vs SPY")
        relative = calculate_relative_performance(
            df[price_column],
            benchmark[benchmark_column],
        )
        relative_columns = st.columns(4)
        for column, label, key in zip(
            relative_columns,
            ["5-Day", "20-Day", "60-Day", "YTD"],
            ["5d", "20d", "60d", "ytd"],
        ):
            column.metric(
                f"{label} Return",
                format_metric(relative[f"stock_{key}"] * 100, "%", 1),
                delta=(
                    f"Alpha {format_metric(relative[f'alpha_{key}'] * 100, '%', 1)}"
                ),
            )

        stock_returns = calculate_returns(df[price_column])
        benchmark_returns = calculate_returns(benchmark[benchmark_column])
        info_ratio = calculate_information_ratio(stock_returns, benchmark_returns)
        tracking_error = calculate_tracking_error(stock_returns, benchmark_returns)
        relative_col1, relative_col2 = st.columns(2)
        relative_col1.metric("Information Ratio", format_metric(info_ratio))
        relative_col2.metric(
            "Tracking Error",
            format_metric(tracking_error * 100, "%", 1),
        )

        st.subheader("AI Analysis")
        if st.button("Generate Stock Summary"):
            try:
                with st.spinner("Generating educational stock summary..."):
                    from agents.market_summarizer import MarketSummarizer

                    summary = MarketSummarizer().analyze_stock(
                        {
                            "ticker": ticker,
                            "price": float(latest["Close"]),
                            "return_5d": relative["stock_5d"],
                            "return_20d": relative["stock_20d"],
                            "return_ytd": relative["stock_ytd"],
                            "volatility": metrics["ann_volatility"],
                            "max_dd": metrics["max_drawdown"],
                            "sharpe": metrics["sharpe_ratio"],
                            "beta": (
                                metrics["beta"]
                                if metrics["beta"] is not None
                                else float("nan")
                            ),
                            "rsi": float(latest["RSI14"]),
                            "macd": float(latest["MACD"]),
                            "above_ma50": bool(
                                latest["Close"] > latest["MA50"]
                            ),
                            "above_ma200": bool(
                                latest["Close"] > latest["MA200"]
                            ),
                        }
                    )
                st.markdown(summary)
                st.caption(
                    "AI-generated analysis for educational purposes only. "
                    "Not financial advice."
                )
            except Exception as exc:
                st.error(f"AI summary unavailable: {exc}")
    except Exception as exc:
        st.error(f"Unable to load {ticker}: {exc}")
