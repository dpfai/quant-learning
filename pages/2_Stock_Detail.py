"""
Stock detail page with price chart and technical indicators.
"""
import streamlit as st

from config.settings import DEFAULT_PERIOD
from features.indicators import add_all_indicators
from utils.chart_builder import ChartBuilder
from utils.data_loader import DataLoader


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
    except Exception as exc:
        st.error(f"Unable to load {ticker}: {exc}")
