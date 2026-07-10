"""
Market overview page.
"""
import pandas as pd
import plotly.express as px
import streamlit as st

from config.settings import DEFAULT_PERIOD, DEFAULT_TICKERS
from utils.chart_builder import ChartBuilder
from utils.data_loader import DataLoader
from utils.export import dataframe_to_csv
from utils.market_regime import get_market_regime, get_sector_performance


st.title("Market Overview")

tickers = st.multiselect("Select tickers", DEFAULT_TICKERS, default=DEFAULT_TICKERS[:3])
period = st.selectbox("History", ["6mo", "1y", "2y", "5y"], index=2)

loader = DataLoader()
data = {}
regime = None
sector_df = pd.DataFrame()
spy_df = None

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
    latest_prices = pd.DataFrame(rows)
    st.dataframe(latest_prices, use_container_width=True, hide_index=True)
    st.download_button(
        "Download Latest Prices CSV",
        dataframe_to_csv(latest_prices, include_index=False),
        file_name="market_overview_prices.csv",
        mime="text/csv",
    )
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

if regime is not None and spy_df is not None and not sector_df.empty:
    st.subheader("AI Analysis")
    if st.button("Generate Market Summary"):
        try:
            with st.spinner("Generating educational market summary..."):
                from agents.market_summarizer import MarketSummarizer

                spy_prices = spy_df[
                    "Adj Close" if "Adj Close" in spy_df.columns else "Close"
                ].dropna()
                spy_ma50 = float(spy_prices.tail(50).mean())
                summary = MarketSummarizer().summarize_market(
                    {
                        "regime": regime["regime"],
                        "vix": regime["vix_level"],
                        "spy_price": float(spy_prices.iloc[-1]),
                        "spy_change": float(spy_prices.iloc[-1] / spy_ma50 - 1),
                        "sector_performance": sector_df[
                            ["Name", "Return"]
                        ].to_string(index=False),
                        "top_sector": sector_df.iloc[0]["Name"],
                        "weak_sector": sector_df.iloc[-1]["Name"],
                        "volatility_level": (
                            "high" if regime["vix_level"] > 25 else "normal"
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
