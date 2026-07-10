# Quant Learning Dashboard

An AI-assisted stock research and trading decision-support platform for learning
quantitative trading concepts, testing ideas, and understanding the code behind
the workflow.

## Features

### 📊 6 Dashboard Pages

| Page | Description |
|------|-------------|
| **Market Overview** | Market regime detection, VIX analysis, sector performance |
| **Stock Detail** | Technical indicators, risk metrics, relative performance |
| **Watchlist** | Multi-stock tracking, ranking, risk-return analysis |
| **Backtesting** | Strategy testing with MA Crossover, RSI, Bollinger Bands |
| **Prediction** | ML experiments with feature engineering and validation |
| **Learning Center** | Trading workflow, code map, AI calls, features, models, metrics |

### 📈 40+ Metrics & Indicators

- **Technical**: RSI, MACD, Bollinger Bands, ATR, Moving Averages
- **Risk**: Sharpe Ratio, Sortino Ratio, Max Drawdown, Beta, Volatility
- **Performance**: Alpha, Information Ratio, Tracking Error
- **ML Features**: Momentum, volatility, price patterns

### 🤖 AI Analysis (Optional)

- Natural language market summaries
- Stock analysis explanations
- Uses any OpenAI-compatible LLM provider

### 🧠 Learning Center

- Explains how to use the app for trading decision support
- Maps Streamlit pages to the underlying Python modules
- Shows how AI summaries are called and configured
- Explains feature engineering, model comparison, and ML metrics
- Connects Prediction results with Backtesting and risk management

### 🔬 Reference Implementations

5 open-source quant repos included for study:
- TradingAgents (multi-agent trading framework)
- ai-hedge-fund (investor persona agents)
- FinGPT (financial LLMs)
- Qlib (Microsoft's quant platform)
- OpenBB (data integration)

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/dpfai/quant-learning.git
cd quant-learning

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Dashboard

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

### Enable AI Features (Optional)

```bash
export LLM_API_KEY="your-api-key"
# Optionally set LLM_PROVIDER, LLM_MODEL, LLM_BASE_URL
```

The API key should stay in your environment or a local `.env` file, never in code.

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=term-missing
```

Current test coverage: **81%** (44 tests passing)

---

## Project Structure

```
quant-learning/
├── app.py                    # Main Streamlit app
├── config/                   # Configuration
│   ├── settings.py
│   └── config.yaml
├── data/                     # Data storage
│   ├── cache/               # Price data cache
│   └── watchlists.json      # Default watchlists
├── pages/                    # Streamlit pages
│   ├── 1_Market_Overview.py
│   ├── 2_Stock_Detail.py
│   ├── 3_Watchlist.py
│   ├── 4_Backtest.py
│   ├── 5_Prediction.py
│   └── 6_Learning_Center.py
├── features/                 # Feature engineering
│   ├── indicators.py        # Technical indicators
│   └── risk_metrics.py      # Risk calculations
├── utils/                    # Utilities
│   ├── data_loader.py
│   ├── data_providers/      # Multi-source data
│   ├── chart_builder.py
│   └── market_regime.py
├── backtest/                 # Backtesting framework
│   ├── engine.py
│   └── strategies.py
├── ml/                       # Machine learning
│   ├── features.py
│   ├── models.py
│   └── validation.py
├── agents/                   # AI agents
│   ├── llm_client.py
│   └── market_summarizer.py
├── tests/                    # Unit tests
├── docs/                     # Documentation
└── reference-repos/          # Reference repos summary
```

---

## Key Concepts

### Risk Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Sharpe Ratio | (Return - Rf) / Volatility | >1 good, >2 excellent |
| Sortino Ratio | (Return - Rf) / Downside Vol | Penalizes only downside |
| Max Drawdown | (Peak - Trough) / Peak | Worst-case loss |
| Beta | Cov(Stock, Market) / Var(Market) | Market sensitivity |

### Backtesting

Strategies implemented:
1. **MA Crossover**: Trend following (MA20/MA50)
2. **RSI Mean Reversion**: Buy oversold, sell overbought
3. **Bollinger Band**: Price band breakouts

All strategies use next-bar execution to prevent look-ahead bias.

### Machine Learning

Features (24 total):
- Price momentum (5d, 10d, 20d, 60d returns)
- Volatility measures (rolling std)
- MA distance, high-low ratios, volume changes
- Technical indicators (RSI, MACD, Bollinger Bands position, ATR)

Models:
- Random Forest (default)
- Logistic Regression
- Gradient Boosting

Time-series walk-forward validation prevents data leakage.

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit, Plotly |
| **Data** | yfinance, pandas, numpy |
| **ML** | scikit-learn |
| **Backtesting** | Custom engine |
| **AI** | OpenAI-compatible API (optional) |

---

## Disclaimer

**This is for educational purposes only.**

- NOT financial advice
- NOT investment recommendations
- NOT a guarantee of any returns
- Backtests are not indicative of future performance
- Always do your own research

---

## License

MIT License
