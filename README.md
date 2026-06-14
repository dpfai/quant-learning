# Quant Learning Dashboard

An AI-powered market research platform for learning quantitative trading concepts.

## Features

### 📊 5 Dashboard Pages

| Page | Description |
|------|-------------|
| **Market Overview** | Market regime detection, VIX analysis, sector performance |
| **Stock Detail** | Technical indicators, risk metrics, relative performance |
| **Watchlist** | Multi-stock tracking, ranking, risk-return analysis |
| **Backtesting** | Strategy testing with MA Crossover, RSI, Bollinger Bands |
| **Prediction** | ML experiments with feature engineering and validation |

### 📈 40+ Metrics & Indicators

- **Technical**: RSI, MACD, Bollinger Bands, ATR, Moving Averages
- **Risk**: Sharpe Ratio, Sortino Ratio, Max Drawdown, Beta, Volatility
- **Performance**: Alpha, Information Ratio, Tracking Error
- **ML Features**: Momentum, volatility, price patterns

### 🤖 AI Analysis (Optional)

- Natural language market summaries
- Stock analysis explanations
- Requires OpenAI API key

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
export OPENAI_API_KEY="your-openai-api-key"
```

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
│   └── watchlists.json      # User watchlists
├── pages/                    # Streamlit pages
│   ├── 1_Market_Overview.py
│   ├── 2_Stock_Detail.py
│   ├── 3_Watchlist.py
│   ├── 4_Backtest.py
│   └── 5_Prediction.py
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
│   └── AI_Agents_vs_Traditional_ML.md
└── reference-repos/          # Reference implementations
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [USER_GUIDE.md](USER_GUIDE.md) | Complete usage tutorial |
| [ai_quant_learning_roadmap.md](ai_quant_learning_roadmap.md) | Learning roadmap |
| [docs/AI_Agents_vs_Traditional_ML.md](docs/AI_Agents_vs_Traditional_ML.md) | AI agents deep dive |
| [reference-repos/README.md](reference-repos/README.md) | Reference repos summary |
| [reference-repos/STUDY_GUIDE.md](reference-repos/STUDY_GUIDE.md) | Phase-by-phase references |

---

## Learning Path

### Phase 1-3: Data & Visualization
- Market data fetching with yfinance
- Candlestick charts and indicators
- Moving averages (MA20, MA50, MA200)

### Phase 4-5: Risk Analysis
- Risk metrics (Sharpe, Sortino, Max DD, Beta)
- Market regime detection
- Sector performance analysis

### Phase 6-7: Portfolio Tools
- Relative performance vs benchmark
- Watchlist management
- Multi-stock comparison

### Phase 8-9: Quantitative Analysis
- Backtesting strategies
- Transaction costs and slippage
- ML feature engineering
- Time-series validation

### Phase 10-12: Advanced Features
- AI-powered analysis
- Configuration management
- Data export

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
1. **MA Crossover**: Trend following
2. **RSI Mean Reversion**: Buy oversold, sell overbought
3. **Bollinger Band**: Price band breakouts

All strategies use next-bar execution to prevent look-ahead bias.

### Machine Learning

Features:
- Price momentum (5d, 10d, 20d, 60d returns)
- Volatility measures
- Technical indicators (RSI, MACD, BB)

Models:
- Random Forest
- Logistic Regression
- Gradient Boosting

Time-series split prevents data leakage.

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit, Plotly |
| **Data** | yfinance, pandas, numpy |
| **ML** | scikit-learn |
| **Backtesting** | Custom engine |
| **AI** | OpenAI API (optional) |

---

## Disclaimer

**This is for educational purposes only.**

- NOT financial advice
- NOT investment recommendations
- NOT a guarantee of any returns
- Backtests are not indicative of future performance
- Always do your own research

---

## Credits

Built with reference to:
- [TradingAgents](https://github.com/TauricResearch/TradingAgents)
- [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund)
- [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT)
- [Qlib](https://github.com/microsoft/qlib)
- [OpenBB](https://github.com/OpenBB-finance/OpenBB)

---

## License

MIT License
