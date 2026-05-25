"""
Market overview page.
"""
import streamlit as st

from config.settings import DEFAULT_PERIOD, DEFAULT_TICKERS
from utils.chart_builder import ChartBuilder
from utils.data_loader import DataLoader


st.title("Market Overview")

tickers = st.multiselect("Select tickers", DEFAULT_TICKERS, default=DEFAULT_TICKERS[:3])
period = st.selectbox("History", ["6mo", "1y", "2y", "5y"], index=2)

loader = DataLoader()
data = {}

if tickers:
    with st.spinner("Loading market data..."):
        for ticker in tickers:
            try:
                data[ticker] = loader.download(ticker, period=period or DEFAULT_PERIOD)
            except Exception as exc:
                st.warning(f"{ticker}: {exc}")

if data:
    fig = ChartBuilder.multi_comparison(data, normalize=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Latest Prices")
    rows = []
    for ticker, df in data.items():
        latest = df.iloc[-1]
        rows.append(
            {
                "Ticker": ticker,
                "Close": round(float(latest["Close"]), 2),
                "Volume": int(latest["Volume"]) if "Volume" in latest else None,
                "Last Date": df.index[-1].date(),
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.info("Select at least one ticker to view market data.")
