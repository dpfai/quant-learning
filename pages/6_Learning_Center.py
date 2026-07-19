"""Learning center for trading workflow, code architecture, and ML concepts."""
from __future__ import annotations

import pandas as pd
import streamlit as st


st.title("Learning Center")
st.caption(
    "A practical guide to using the app for stock research, trading decisions, "
    "code learning, and machine-learning experiments."
)

(
    trading_tab,
    code_tab,
    ai_tab,
    features_tab,
    models_tab,
    metrics_tab,
    experiments_tab,
) = st.tabs(
    [
        "Trading Workflow",
        "Code Map",
        "AI Calls",
        "Features",
        "Models",
        "Metrics",
        "Experiments",
    ]
)

with trading_tab:
    st.subheader("How To Use The Platform For Trading Decisions")
    st.markdown(
        """
        The app is a decision-support system. It helps you form and test a trade
        thesis, but the final decision remains human.

        A beginner-friendly workflow:

        1. **Check the market first.** A strong individual stock can still fail in
           a risk-off market. Start with SPY trend, VIX level, and sector rotation.
        2. **Analyze one ticker.** Look for trend, RSI, MACD, Bollinger position,
           drawdown, beta, and whether it is outperforming SPY.
        3. **Compare candidates.** A watchlist helps you avoid tunnel vision.
           Choose the strongest setup from a group instead of forcing one ticker.
        4. **Define the trade setup.** Write the rule in plain language, such as
           "price above MA50, RSI not overbought, stock outperforming SPY."
        5. **Backtest the rule.** A setup that cannot survive historical testing,
           costs, and drawdowns should be treated carefully.
        6. **Run ML as evidence, not authority.** Model output is one more signal.
           It is not a guarantee and not a trading order.
        7. **Record the thesis.** Note why the trade makes sense, what would
           invalidate it, and what risk you are accepting.
        """
    )

    st.subheader("Decision Output Template")
    st.markdown(
        """
        Use this structure before placing any real trade outside the app:

        - **Market:** risk-on, neutral, or risk-off
        - **Ticker:** trend, relative strength, volatility, and drawdown profile
        - **Setup:** exact rule or condition being tested
        - **Evidence:** indicator state, backtest result, ML metrics, AI summary
        - **Risk:** max acceptable loss, invalidation level, position size
        - **Review date:** when to reassess the thesis
        """
    )

    st.warning(
        "This app does not connect to a broker and does not execute trades. "
        "Use it for research, learning, and decision support."
    )

with code_tab:
    st.subheader("How The App Is Organized")
    st.markdown(
        """
        The codebase is intentionally modular so each concept is easy to study.
        Streamlit pages handle user interaction. Shared modules handle data,
        indicators, risk calculations, backtesting, ML, and AI summaries.
        """
    )
    st.dataframe(
        pd.DataFrame(
            [
                ["app.py", "Home page and high-level workflow"],
                ["pages/1_Market_Overview.py", "Market regime, VIX, sector rotation, AI market summary"],
                ["pages/2_Stock_Detail.py", "Ticker chart, indicators, risk metrics, relative performance"],
                ["pages/3_Watchlist.py", "Watchlist management, ranking, comparison charts"],
                ["pages/4_Backtest.py", "Strategy selection, costs, equity curve, trades"],
                ["pages/5_Prediction.py", "Feature creation, model training, metrics, feature importance"],
                ["utils/data_loader.py", "Single entry point for market data downloads"],
                ["utils/data_providers/yfinance_provider.py", "Yahoo Finance provider implementation"],
                ["features/indicators.py", "RSI, MACD, Bollinger Bands, ATR, moving averages"],
                ["features/risk_metrics.py", "Return, volatility, Sharpe, Sortino, beta, drawdown"],
                ["utils/relative_performance.py", "Alpha, tracking error, information ratio"],
                ["backtest/strategies.py", "Signal rules for MA, RSI, and Bollinger strategies"],
                ["backtest/engine.py", "Execution timing, transaction costs, equity curve, metrics"],
                ["ml/features.py", "Trailing features and forward target construction"],
                ["ml/models.py", "Logistic regression, random forest, gradient boosting"],
                ["ml/validation.py", "Walk-forward time-series validation"],
                ["agents/llm_client.py", "OpenAI-compatible LLM client"],
                ["agents/market_summarizer.py", "Formats market and stock data for AI summaries"],
                ["agents/prompts.py", "System and user prompt templates"],
                ["config/config.yaml", "Data, risk, UI, and LLM defaults"],
            ],
            columns=["File", "What It Teaches"],
        ),
        use_container_width=True,
        hide_index=True,
    )

    with st.expander("A typical request flow"):
        st.code(
            """
User selects ticker in Streamlit page
    -> DataLoader downloads or reads cached OHLCV data
    -> features/ modules calculate indicators and risk metrics
    -> page displays charts, tables, and metrics
    -> optional: MarketSummarizer formats data into a prompt
    -> LLMClient calls the configured OpenAI-compatible model
    -> summary is displayed as research context
            """.strip(),
            language="text",
        )

with ai_tab:
    st.subheader("How The AI Model Is Called")
    st.markdown(
        """
        AI is used for explanation and research summaries. It is not the same as
        the ML classifier on the Prediction page.

        The app currently defaults to:

        - **Provider:** Baidu Qianfan Coding
        - **Base URL:** `https://ark.cn-beijing.volces.com/api/coding/v3`
        - **API format:** OpenAI-compatible chat completions
        - **Default model:** `glm-5.2`
        - **Alternative models:** `deepseek-v3.2`, `kimi-k2.6`
        """
    )
    st.code(
        """
export BAIDU_API_KEY="your-key"
export LLM_MODEL="glm-5.2"

# Optional alternatives
export LLM_MODEL="deepseek-v3.2"
export LLM_MODEL="kimi-k2.6"
        """.strip(),
        language="bash",
    )
    st.markdown(
        """
        The key implementation is `agents/llm_client.py`. It reads configuration
        from `config/config.yaml`, then lets environment variables override local
        defaults. The API key is never stored in Git.
        """
    )
    st.code(
        """
summary = MarketSummarizer().summarize_market(
    {
        "regime": "RISK-ON",
        "vix": 15.0,
        "spy_price": 500.0,
        "spy_change": 0.02,
        "sector_performance": "Technology +5%",
        "top_sector": "Technology",
        "weak_sector": "Utilities",
        "volatility_level": "normal",
    }
)
        """.strip(),
        language="python",
    )
    st.markdown(
        """
        Good use cases for the LLM:

        - Explain what the dashboard metrics mean together
        - Identify risks that deserve follow-up research
        - Turn raw metrics into a readable market note
        - Help you compare competing trade theses

        Weak use cases:

        - Asking for guaranteed price predictions
        - Treating a generated summary as a buy or sell command
        - Ignoring the data and only reading the narrative
        """
    )

with features_tab:
    st.subheader("How Features Are Selected")
    st.markdown(
        """
        A feature is an input column used by a model. In trading, features should
        be based only on information that would have been known at the time.
        This app uses trailing features to reduce look-ahead bias.
        """
    )
    st.dataframe(
        pd.DataFrame(
            [
                ["return_5d, return_10d, return_20d, return_60d", "Momentum", "Has the stock been rising or falling recently?"],
                ["volatility_5d, volatility_10d, volatility_20d, volatility_60d", "Risk", "How unstable are recent returns?"],
                ["ma_dist_5d, ma_dist_10d, ma_dist_20d, ma_dist_60d", "Trend extension", "How far is price from its moving average?"],
                ["high_low_ratio_*", "Range expansion", "Is the trading range widening?"],
                ["volume_change_*", "Participation", "Is volume changing with the move?"],
                ["rsi_14", "Momentum oscillator", "Is price stretched up or down?"],
                ["macd, macd_signal, macd_hist", "Trend momentum", "Is trend momentum improving or weakening?"],
                ["bb_position", "Volatility band position", "Where is price relative to Bollinger Bands?"],
                ["atr_ratio", "Volatility normalized by price", "How large is recent true range?"],
            ],
            columns=["Feature", "Category", "Plain-English Meaning"],
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Feature Selection Principles")
    st.markdown(
        """
        Use features that are:

        - **Causal in time:** calculated from past and current data only
        - **Interpretable:** connected to trend, risk, volatility, or participation
        - **Not duplicated too heavily:** many versions of the same idea can
          overstate confidence
        - **Stable across tickers:** a useful feature should not only work for
          one lucky stock
        - **Validated out of sample:** useful features should help on test data,
          not only training data
        """
    )

with models_tab:
    st.subheader("Models In The Platform")
    st.dataframe(
        pd.DataFrame(
            [
                [
                    "Logistic Regression",
                    "Linear classification with scaling",
                    "Good baseline; coefficients are easier to reason about",
                    "May miss nonlinear relationships",
                ],
                [
                    "Random Forest",
                    "Many decision trees voting together",
                    "Handles nonlinear feature interactions and ranks features",
                    "Can overfit if depth is too high",
                ],
                [
                    "Gradient Boosting",
                    "Sequential trees that correct prior mistakes",
                    "Often strong on tabular data",
                    "Can overfit and needs careful validation",
                ],
            ],
            columns=["Model", "Idea", "Why Use It", "Main Risk"],
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("How To Compare Models")
    st.markdown(
        """
        Do not choose a model because it has the best single run. Compare models
        across multiple tickers, horizons, and time periods.

        Practical comparison checklist:

        - Same ticker, same date range, same prediction horizon
        - Compare accuracy, precision, recall, and F1 together
        - Inspect feature importance for plausibility
        - Prefer stable out-of-sample behavior over one high score
        - Re-run on different tickers to see whether the model generalizes
        - Treat very high scores with suspicion in financial data
        """
    )

    st.code(
        """
model = get_model("random_forest")
model.fit(X_train, y_train)
metrics = evaluate_model(model, X_test, y_test)
importance = get_feature_importance(model, X_train.columns.tolist())
        """.strip(),
        language="python",
    )

with metrics_tab:
    st.subheader("Metrics For Trading Research")
    st.markdown(
        """
        Metrics answer different questions. No single metric is enough.
        """
    )
    st.dataframe(
        pd.DataFrame(
            [
                ["Accuracy", "How often was the class prediction correct?", "Can be misleading when classes are imbalanced"],
                ["Precision", "When the model predicted UP, how often was it right?", "Useful when false positives are costly"],
                ["Recall", "Of all actual UP periods, how many did the model catch?", "Useful when missing opportunities matters"],
                ["F1 Score", "Balance between precision and recall", "Helpful single summary, but still not profit"],
                ["Sharpe Ratio", "Return per unit of volatility", "Risk-adjusted strategy quality"],
                ["Max Drawdown", "Worst peak-to-trough loss", "Survivability and emotional pressure"],
                ["Profit Factor", "Gross gains divided by gross losses", "Can be distorted by few trades"],
                ["Win Rate", "Percent of positive return periods", "High win rate can still lose money if losses are large"],
                ["Tracking Error", "Volatility of excess returns vs benchmark", "How unstable relative performance is"],
                ["Information Ratio", "Alpha divided by tracking error", "Risk-adjusted outperformance vs benchmark"],
            ],
            columns=["Metric", "Question It Answers", "How To Read It"],
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Important Distinction")
    st.markdown(
        """
        A classification metric is not the same as trading profit.

        A model can have decent accuracy but still be hard to trade if:

        - Correct predictions are small moves and wrong predictions are large moves
        - Transaction costs erase the edge
        - Signals arrive during high-volatility periods
        - The model works only in one market regime

        That is why Prediction and Backtesting should be used together.
        """
    )

with experiments_tab:
    st.subheader("How To Run Better Experiments")
    st.markdown(
        """
        A good experiment changes one thing at a time. If you change ticker,
        model, horizon, and date range all at once, you will not know what caused
        the result.
        """
    )
    st.dataframe(
        pd.DataFrame(
            [
                ["Ticker", "SPY, QQQ, NVDA, AAPL", "Does the signal work across assets?"],
                ["Horizon", "1, 5, 10, 20 trading days", "Is the model short-term or medium-term?"],
                ["Model", "logistic, random_forest, gradient_boost", "Does complexity help or overfit?"],
                ["Feature set", "price only vs price plus technical", "Which information adds value?"],
                ["Costs", "commission and slippage", "Does the setup survive real frictions?"],
                ["Market regime", "risk-on vs risk-off periods", "When does the model fail?"],
            ],
            columns=["Experiment Lever", "Examples", "Question"],
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Recommended Research Loop")
    st.markdown(
        """
        1. Start with a simple hypothesis.
        2. Pick one ticker and one horizon.
        3. Train two or three models using the same split.
        4. Compare test metrics, not training performance.
        5. Inspect feature importance and ask whether it makes market sense.
        6. Run a related backtest with realistic costs.
        7. Write down what worked, what failed, and what to test next.
        """
    )

    st.info(
        "The purpose of experiments is not to find a perfect model. It is to build "
        "a disciplined process for discovering, rejecting, and improving trading ideas."
    )
