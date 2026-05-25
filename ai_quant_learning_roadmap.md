# AI Quant Learning Roadmap

## Project Vision

Build a research-oriented market intelligence platform instead of an automatic trading AI.

Core philosophy:

- Data-driven market research
- Visualization first
- Risk analysis first
- Prediction later
- AI as research assistant
- No real-money auto trading
- Learn while building

---

# Recommended Direction

You are NOT trying to build:

- “AI predicts tomorrow’s stock price”

You ARE trying to build:

- Market Research Dashboard
- Quant Research Assistant
- AI-Augmented Investment Research Platform

This is a much more realistic and professional direction.

---

# Recommended Learning Path

## Phase 0 — Project Initialization

Goal:

Create a local runnable dashboard project.

Tech stack:

- Python
- Streamlit
- pandas
- numpy
- Plotly
- yfinance

Project structure:

```text
market-research-dashboard/
    app.py
    requirements.txt
    README.md
    config/
        settings.py
        config.yaml
    data/
        raw/
        processed/
        cache/
    features/
    pages/
    utils/
        __init__.py
    notebooks/
    tests/
        __init__.py
```

Learn:

- virtual environments
- Streamlit basics
- modular project structure
- configuration management

Phase 完成标准：

- 能运行 `streamlit run app.py` 看到空白页面
- 项目结构完整
- 虚拟环境配置正确

---

# Phase 1 — Data Layer

Learn:

- OHLCV data
- ETF vs stock
- adjusted close
- time series basics

Implement:

- Download SPY, QQQ, DIA, IWM, VIX
- Watchlist support
- Data caching
- Historical price storage

Libraries:

```python
yfinance
pandas
```

---

# Phase 2 — Visualization

Goal:

Create strong visual intuition about markets.

Implement:

- Candlestick chart
- Volume chart
- Return chart
- Multi-stock comparison
- Moving averages

Libraries:

```python
Plotly
Streamlit
```

Learn:

- trend
- momentum
- volatility
- support/resistance intuition

---

# Phase 3 — Technical Indicators

Implement:

- MA20 / MA50 / MA200
- RSI
- MACD
- Bollinger Bands
- ATR

Learn:

- trend following
- mean reversion
- volatility expansion
- indicator limitations

Important:

Indicators are NOT magic prediction tools.

Phase 完成标准：

- Dashboard 能展示任意股票的上述指标
- 指标计算模块独立可测试

---

# Phase 3.5 — Fundamental Data (Optional but Recommended)

Goal:

Add fundamental context alongside technical analysis.

Implement:

- PE / PB / EV-EBITDA
- Revenue growth / Earnings growth
- Sector / Industry classification
- Market cap categories

Libraries:

```python
yfinance (basic)
# Future: Polygon, Alpha Vantage for richer data
```

Learn:

- fundamental vs technical analysis
- value investing basics
- sector rotation logic

Phase 完成标准：

- 能展示股票的基本面快照
- 能按行业/市值筛选股票

---

# Phase 4 — Risk Analysis

This is more important than prediction.

Implement:

- Daily returns
- Annualized return
- Volatility
- Max drawdown
- Sharpe ratio
- Beta vs SPY
- Correlation matrix

Learn:

- risk-adjusted return
- diversification
- downside risk

Phase 完成标准：

- 能计算并展示单只股票的全部风险指标
- 能对比多只股票的风险特征

---

# Phase 5 — Market Overview Dashboard

Build:

- market overview page
- ETF performance
- sector rotation
- VIX risk panel
- market breadth indicators

Simple market regime system:

- Risk-On
- Neutral
- Risk-Off

Use transparent rules first.

---

# Phase 6 — Stock Detail Page

Features:

- User ticker input
- Candlestick chart
- Technical indicators
- Risk metrics
- Relative performance vs SPY
- AI-generated trend summary

Avoid:

- direct buy/sell recommendations

---

# Phase 7 — Watchlist System

Build:

- Multi-ticker watchlist
- Ranking system
- Performance comparison

Metrics:

- 5d return
- 20d return
- 60d return
- YTD return
- volatility
- drawdown

---

# Phase 8 — Backtesting

Recommended library:

- vectorbt

Implement:

- MA crossover strategy
- RSI mean reversion strategy

Learn:

- lookahead bias
- overfitting
- transaction costs
- survivorship bias

Important:

Backtest != real profitability

---

# Phase 9 — Prediction System

DO NOT predict “tomorrow will go up”.

Instead:

Predict probabilistic future outcomes.

Examples:

- future 5-day return
- future 20-day return bucket
- outperform vs SPY

Features:

- past returns
- volatility
- RSI
- MACD
- MA distance
- volume change

Feature Engineering (重要):

- lagged features (滞后特征)
- rolling statistics (滚动统计：mean, std, min, max)
- feature selection methods
- 防止数据泄露的训练流程：
  1. 先划分时间范围
  2. 再做特征工程
  3. fit/transform 只在训练集上

Models:

- Logistic Regression
- RandomForest
- LightGBM (later)

Learn:

- walk-forward validation
- time-series split
- model drift

Experiment Tracking:

- 使用 MLflow 或 Weights & Biases 记录每次实验
- 记录：参数、指标、特征重要性、模型版本
- 避免”跑了很多但不知道哪个好”

Phase 完成标准：

- 能用历史数据训练模型并验证
- 有完整的实验记录
- 清楚知道当前最佳模型的性能

---

# Phase 10 — AI Summary System

Goal:

AI explains market conditions.

AI should summarize:

- market state
- risk environment
- strong sectors
- weak sectors
- unusual conditions

AI should NOT:

- guarantee profits
- issue financial advice

---

# Phase 11 — Productization

Improve:

- UI
- logging
- config system
- testing
- error handling
- documentation

Possible future features:

- paper trading
- alert system
- Discord notifications
- AI research reports
- agent workflows

---

# Recommended GitHub Projects

## 1. VectorBT

Purpose:

Quant research and backtesting framework.

Learn from:

- research workflow
- portfolio analysis
- signal systems
- parameter sweeps

Do NOT:

Blindly copy strategies.

---

## 2. Qlib

Purpose:

AI-oriented quant research platform.

Learn from:

- feature pipelines
- experiment management
- ML workflows

Use later.

Too heavy for beginners.

---

## 3. QuantConnect LEAN

Purpose:

Professional-grade quant engine.

Learn from:

- event engine
- execution system
- portfolio engine

Mostly architecture learning.

---

## 4. Freqtrade

Purpose:

Crypto trading framework.

Learn from:

- config systems
- strategy plugins
- scheduling
- notifications

Useful later.

---

## 5. Backtrader

Purpose:

Simple Python backtesting framework.

Good for:

Understanding backtesting fundamentals.

---

# Recommended Tech Stack

## Core

```text
Python
pandas
numpy
Plotly
Streamlit
```

## Quant

```text
vectorbt
Backtrader
PyPortfolioOpt
```

## ML

```text
scikit-learn
LightGBM
XGBoost
PyTorch (later)
```

## Data

```text
yfinance
Polygon
Finnhub
Alpha Vantage
```

## Future Infrastructure

```text
DuckDB
Postgres
FastAPI
Redis
```

---

# Important Principles

## 1. Start simple

Do NOT begin with:

- deep learning
- high frequency trading
- automatic execution

---

## 2. Build research capability

Your goal is NOT:

- finding one magical strategy

Your goal IS:

- learning how to evaluate ideas systematically

---

## 3. Visualization matters

Good visualization creates market intuition.

---

## 4. Risk management is core

Many strategies make money before eventually blowing up.

Risk management matters more than prediction accuracy.

---

# Suggested Development Workflow

## Step 1

Build dashboard MVP.

## Step 2

Add indicators.

## Step 3

Add risk analysis.

## Step 4

Add watchlists.

## Step 5

Add backtesting.

## Step 6

Add ML prediction.

## Step 7

Add AI summaries.

## Step 8

Add research automation.

---

# Long-Term Vision

Future system idea:

```text
Market Data
    ↓
Feature Engine
    ↓
Research Layer
    ↓
Risk Layer
    ↓
Prediction Layer
    ↓
AI Explanation Layer
    ↓
Research Dashboard
```

This is a sustainable and realistic direction.

