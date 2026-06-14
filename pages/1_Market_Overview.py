"""
Market overview page.
"""
import plotly.express as px
import streamlit as st

from config.settings import DEFAULT_PERIOD, DEFAULT_TICKERS
from utils.chart_builder import ChartBuilder
from utils.data_loader import DataLoader
from utils.market_regime import get_market_regime, get_sector_performance


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

st.divider()

try:
    with st.spinner("Loading market regime data..."):
        spy_df = data.get("SPY")
        if spy_df is None:
            spy_df = loader.download("SPY", period=period or DEFAULT_PERIOD)

        vix_df = data.get("VIX")
        if vix_df is None:
            vix_df = loader.download("VIX", period=period or DEFAULT_PERIOD)

    vix_column = "Adj Close" if "Adj Close" in vix_df.columns else "Close"
    vix_prices = vix_df[vix_column].dropna()
    vix_value = float(vix_prices.iloc[-1])
    regime = get_market_regime(spy_df, vix_value)

    st.subheader("Market Regime")
    regime_message = f"{regime['regime']} - {regime['description']}"
    if regime["regime"] == "RISK-ON":
        st.success(regime_message)
    elif regime["regime"] == "RISK-OFF":
        st.error(regime_message)
    else:
        st.warning(regime_message)

    regime_col1, regime_col2, regime_col3 = st.columns(3)
    regime_col1.metric("VIX", f"{regime['vix_level']:.1f}")
    regime_col2.metric(
        "SPY > MA50",
        "Yes" if regime["spy_above_ma50"] else "No",
    )
    regime_col3.metric(
        "SPY > MA200",
        "Yes" if regime["spy_above_ma200"] else "No",
    )

    st.subheader("VIX Risk Panel")
    st.plotly_chart(
        ChartBuilder.create_vix_gauge(vix_value),
        use_container_width=True,
    )
    vix_52_week = vix_prices.tail(252)
    st.caption(
        f"VIX 52-week range: {vix_52_week.min():.1f} - {vix_52_week.max():.1f}"
    )
except Exception as exc:
    st.warning(f"Market regime unavailable: {exc}")

st.subheader("Sector Performance")
try:
    with st.spinner("Loading sector performance..."):
        sector_df = get_sector_performance("3mo", loader=loader)

    if sector_df.empty:
        st.info("Sector performance data is currently unavailable.")
    else:
        sector_chart_data = sector_df.sort_values("Return")
        sector_fig = px.bar(
            sector_chart_data,
            x="Return",
            y="Name",
            orientation="h",
            color="Return",
            color_continuous_scale="RdYlGn",
            labels={"Return": "3-Month Return", "Name": "Sector"},
            hover_data={"Ticker": True, "Rank": True, "Return": ":.2%"},
        )
        sector_fig.update_xaxes(tickformat=".1%")
        sector_fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(sector_fig, use_container_width=True)

        sector_table = sector_df.copy()
        sector_table["Return"] = sector_table["Return"].map(lambda value: f"{value:.2%}")
        st.dataframe(sector_table, use_container_width=True, hide_index=True)
except Exception as exc:
    st.warning(f"Sector performance unavailable: {exc}")
