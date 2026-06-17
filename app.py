"""
Market Research Dashboard
Main entry point.
"""
import streamlit as st


st.set_page_config(
    page_title="Market Research Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Market Research Dashboard")
st.caption(
    "AI-assisted stock research and trading decision support. "
    "The app helps you analyze, test, and learn; it does not place trades."
)

st.markdown(
    """
    This platform is designed for three kinds of users:

    - **Stock users** who want a clear workflow for reading market conditions,
      comparing tickers, testing trade ideas, and managing risk.
    - **Code learners** who want to understand how a Streamlit quant dashboard is
      built from data loading, feature engineering, backtesting, and AI summaries.
    - **Model learners** who want to study feature design, model selection,
      validation, metrics, and the limits of machine-learning trading signals.

    The goal is not to outsource judgment to a model. The goal is to turn market
    data into a repeatable research process that can support better discretionary
    trading decisions.
    """
)

st.subheader("Recommended Workflow")
workflow_columns = st.columns(5)
workflow_steps = [
    (
        "1. Market",
        "Start with Market Overview to understand regime, VIX, and sector rotation.",
    ),
    (
        "2. Stock",
        "Open Stock Detail to inspect trend, indicators, risk, and relative strength.",
    ),
    (
        "3. Compare",
        "Use Watchlist to rank candidates and compare risk-return profiles.",
    ),
    (
        "4. Test",
        "Run Backtesting to check whether a rule-based setup worked historically.",
    ),
    (
        "5. Model",
        "Use Prediction to test ML features, models, metrics, and feature importance.",
    ),
]

for column, (title, body) in zip(workflow_columns, workflow_steps):
    with column:
        st.markdown(f"**{title}**")
        st.write(body)

st.subheader("What Each Page Is For")
st.dataframe(
    [
        {
            "Page": "Market Overview",
            "Trading Question": "Is the broad market risk-on, neutral, or risk-off?",
            "Learning Focus": "Regime rules, VIX, SPY trend, sector rotation",
        },
        {
            "Page": "Stock Detail",
            "Trading Question": "Is this ticker trending, extended, risky, or outperforming SPY?",
            "Learning Focus": "OHLCV charts, indicators, alpha, beta, drawdown",
        },
        {
            "Page": "Watchlist",
            "Trading Question": "Which candidates deserve attention first?",
            "Learning Focus": "Ranking, comparison, diversification, relative performance",
        },
        {
            "Page": "Backtesting",
            "Trading Question": "Would this rule have survived costs and drawdowns?",
            "Learning Focus": "Signals, execution timing, slippage, performance metrics",
        },
        {
            "Page": "Prediction",
            "Trading Question": "Do historical features contain useful directional signal?",
            "Learning Focus": "Feature engineering, model selection, validation metrics",
        },
        {
            "Page": "Learning Center",
            "Trading Question": "How does the app work under the hood?",
            "Learning Focus": "Code map, AI calls, features, metrics, model comparison",
        },
    ],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Trading Decision Checklist")
st.markdown(
    """
    Before turning an idea into a real trade, use the app to answer these questions:

    - **Market context:** Is the current market regime supportive or defensive?
    - **Ticker quality:** Is the stock stronger than SPY over multiple time frames?
    - **Risk:** What is the max drawdown, volatility, beta, and downside risk?
    - **Setup:** Is the entry idea based on a clear rule or just a chart impression?
    - **Backtest:** Did similar signals work after commission and slippage?
    - **Model evidence:** Do ML metrics hold up on out-of-sample time periods?
    - **Invalidation:** What condition would prove the trade thesis wrong?
    - **Position sizing:** Is the expected risk small enough to survive being wrong?
    """
)

st.subheader("AI And Safety Boundary")
st.markdown(
    """
    AI summaries are used as a research assistant. They can explain market snapshots,
    point out risks, and suggest follow-up questions. They should not be treated as
    orders to buy or sell.

    The default LLM provider is Baidu Qianfan Coding through an OpenAI-compatible
    API. The default model is `glm-5`, and you can override it with `LLM_MODEL`.
    API keys stay in environment variables such as `BAIDU_API_KEY` or `LLM_API_KEY`.
    """
)

st.info(
    "Open the Learning Center page when you want to understand the code, features, "
    "models, metrics, and AI integration behind the dashboard."
)
