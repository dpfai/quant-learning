# Quant Learning Dashboard - User Guide

A comprehensive guide to using your AI-powered market research dashboard for
stock research, trading decision support, and code/model learning.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Dashboard Overview](#dashboard-overview)
3. [Page-by-Page Tutorial](#page-by-page-tutorial)
4. [Understanding the Metrics](#understanding-the-metrics)
5. [Machine Learning Features](#machine-learning-features)
6. [Backtesting Strategies](#backtesting-strategies)
7. [AI Analysis Features](#ai-analysis-features)
8. [Data Management](#data-management)
9. [Tips for Learning](#tips-for-learning)
10. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

- Python 3.8+
- Internet connection (for market data)

### Installation

```bash
# Navigate to project directory
cd quant-learning

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Optional: Enable AI Features

To use AI-generated analysis:

```bash
export BAIDU_API_KEY="your-baidu-qianfan-api-key"
```

The project defaults to Baidu Qianfan Coding with model `glm-5`. Keep your API
key in an environment variable or local `.env` file so it is not committed to
GitHub. Optional overrides:

```bash
export LLM_MODEL="deepseek-v3.2"      # or kimi-k2.5
export LLM_API_KEY="your-provider-key" # provider-neutral alternative
```

---

## Dashboard Overview

Your dashboard has **6 main pages**, accessible from the sidebar:

| Page | Purpose | Learning Focus |
|------|---------|---------------|
| **Market Overview** | Macro market analysis | Market regimes, sector rotation |
| **Stock Detail** | Individual stock analysis | Technical analysis, risk metrics |
| **Watchlist** | Multi-stock tracking | Portfolio construction, comparison |
| **Backtesting** | Strategy testing | Systematic trading, performance |
| **Prediction** | ML experiments | Feature engineering, model validation |
| **Learning Center** | Platform explanation | Trading workflow, code map, AI calls, features, models, metrics |

---

## Page-by-Page Tutorial

### Page 1: Market Overview

**What you'll learn:** How to read market conditions and identify risk levels.

#### Step 1: Understand Market Regime

The dashboard shows one of three market states:

| Regime | Meaning | Typical Behavior |
|--------|---------|-----------------|
| 🟢 **RISK-ON** | Low volatility, bullish | Stocks rising, sectors leading |
| 🟡 **NEUTRAL** | Mixed signals | Cautious, selective positioning |
| 🔴 **RISK-OFF** | High volatility, bearish | Defensive assets preferred |

**Rules used:**
```
RISK-ON:  VIX < 20 AND SPY > MA50 AND SPY > MA200
RISK-OFF: VIX > 25 OR (SPY < MA50 AND SPY < MA200)
NEUTRAL:  Everything else
```

#### Step 2: Read the VIX Gauge

The VIX (Volatility Index) gauge shows market fear:

| VIX Level | Interpretation | Action |
|-----------|---------------|--------|
| 0-15 | Low fear | Risk assets can perform well |
| 15-20 | Normal | Standard risk tolerance |
| 20-25 | Elevated | Reduce position sizes |
| 25+ | High fear | Consider defensive positions |

#### Step 3: Analyze Sector Performance

The sector chart shows 3-month returns for 10 major sectors:

```
XLK - Technology
XLF - Financials
XLV - Healthcare
XLE - Energy
XLY - Consumer Discretionary
XLP - Consumer Staples
XLI - Industrials
XLB - Materials
XLU - Utilities
XLRE - Real Estate
```

**Learning exercise:**
1. Identify the top 3 performing sectors
2. Identify the bottom 3 sectors
3. Note any defensive sectors (XLP, XLU) outperforming
4. This can indicate risk sentiment

#### Step 4: AI Summary (Optional)

Click "Generate AI Summary" for a natural language market analysis.

**Important:** This requires `BAIDU_API_KEY` or `LLM_API_KEY` to be set.

---

### Home Page: Trading Decision Support Guide

**What you'll learn:** How to use the whole platform as a repeatable research
process before making an outside-the-app trading decision.

The Home page explains:

- The platform's purpose: research and decision support, not broker execution
- A recommended workflow from market overview to stock detail, watchlist,
  backtesting, prediction, and review
- What each page helps answer as a trading question
- A checklist for market context, ticker quality, risk, setup, backtest evidence,
  model evidence, invalidation, and position sizing

Use the Home page when you feel lost and want to know what to do next.

---

### Learning Center

**What you'll learn:** How the app works under the hood.

The Learning Center is for users who want more than stock charts. It explains:

- How to use the platform for trading decision support
- Which files implement each part of the app
- How the Baidu Qianfan/OpenAI-compatible AI call works
- Which features the ML page creates
- Why models are compared with accuracy, precision, recall, and F1
- Why backtesting metrics like Sharpe ratio, max drawdown, win rate, and profit
  factor matter
- How to run cleaner experiments by changing one variable at a time

Good use cases:

- You are new to trading and need a structured workflow
- You are a data scientist and want to inspect the model pipeline
- You want to understand feature importance and metric tradeoffs
- You want to learn how the Streamlit pages connect to Python modules

---

### Page 2: Stock Detail

**What you'll learn:** Complete stock analysis workflow.

#### Step 1: Enter a Ticker

Type any valid ticker (e.g., `AAPL`, `NVDA`, `MSFT`) and press Enter.

**Pro tips:**
- Use Yahoo Finance format for international stocks:
  - Hong Kong: `0700.HK` (Tencent)
  - London: `AZN.L` (AstraZeneca)
  - Tokyo: `7203.T` (Toyota)

#### Step 2: Read the Candlestick Chart

The main chart shows:
- **Candles**: Open, High, Low, Close (OHLC)
- **Volume bars**: Trading volume
- **Moving averages**: MA20, MA50, MA200

**Candlestick basics:**
```
🟢 Green candle: Close > Open (bullish)
🔴 Red candle: Close < Open (bearish)

Upper shadow: High price
Body: Open to Close range
Lower shadow: Low price
```

#### Step 3: Analyze Technical Indicators

**RSI (Relative Strength Index):**
| RSI | Signal | Interpretation |
|-----|--------|----------------|
| > 70 | Overbought | Potential reversal down |
| 50-70 | Bullish | Uptrend |
| 30-50 | Bearish | Downtrend |
| < 30 | Oversold | Potential reversal up |

**MACD (Moving Average Convergence Divergence):**
```
MACD > Signal: Bullish momentum
MACD < Signal: Bearish momentum
Histogram > 0: Momentum increasing
Histogram < 0: Momentum decreasing
```

**Bollinger Bands:**
```
Price at Upper Band: Potentially overbought
Price at Lower Band: Potentially oversold
Wide Bands: High volatility
Narrow Bands: Low volatility (breakout coming?)
```

#### Step 4: Understand Risk Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Annualized Return** | `(1 + total_return)^(252/days) - 1` | Yearly equivalent return |
| **Volatility** | `std(daily_returns) × √252` | Yearly price fluctuation |
| **Max Drawdown** | `min(peak_to_trough)` | Worst peak-to-trough loss |
| **Sharpe Ratio** | `(return - risk_free) / volatility` | Risk-adjusted return (>1 good, >2 excellent) |
| **Sortino Ratio** | `(return - risk_free) / downside_vol` | Penalizes only downside |
| **Beta** | `cov(stock, market) / var(market)` | Sensitivity to market moves |
| **Win Rate** | `positive_days / total_days` | % of positive days |

#### Step 5: Relative Performance

Shows how the stock performs vs SPY (S&P 500):

```
Alpha = Stock Return - SPY Return

Positive Alpha: Outperforming the market
Negative Alpha: Underperforming the market
```

#### Step 6: Export Data

Click "Export to CSV" to download:
- Price history
- All technical indicators
- Risk metrics

---

### Page 3: Watchlist

**What you'll learn:** Portfolio tracking and comparison.

#### Step 1: Select a Watchlist

Default watchlists are provided:
- **Tech Growth**: AAPL, MSFT, GOOGL, AMZN, NVDA, META
- **ETFs**: SPY, QQQ, DIA, IWM
- **Sectors**: XLK, XLF, XLV, XLE, XLY

#### Step 2: Add/Remove Tickers

```
To add: Type ticker in "Add Ticker" box and click "Add"
To remove: Click "Remove" next to any ticker
```

#### Step 3: Create Custom Watchlist

1. Click "Create New Watchlist"
2. Enter a name (e.g., "My Dividend Stocks")
3. Add tickers one by one

#### Step 4: Analyze the Metrics Table

| Column | Meaning | Use Case |
|--------|---------|----------|
| Price | Latest close | Entry point reference |
| 5d/20d/60d/YTD | Returns | Momentum assessment |
| Volatility | Annualized volatility | Risk comparison |
| Max DD | Maximum drawdown | Worst-case scenario |
| Sharpe | Sharpe ratio | Risk-adjusted ranking |
| Alpha 20d | 20-day alpha | Recent outperformance |

#### Step 5: Risk-Return Scatter Plot

The scatter plot shows:
- **X-axis**: Volatility (risk)
- **Y-axis**: Return (reward)
- **Position**: Top-left = best (high return, low risk)

**Learning exercise:**
1. Find stocks in the top-left quadrant
2. Find stocks in the bottom-right quadrant
3. Discuss the risk-return tradeoff

---

### Page 4: Backtesting

**What you'll learn:** Testing trading strategies historically.

#### Step 1: Select Parameters

```
Ticker: Stock to test (e.g., SPY)
Strategy: Choose from 3 options
Start Date: Backtest start
Initial Capital: Starting money (e.g., $100,000)
Commission: Trading cost (default 0.1%)
```

#### Step 2: Choose a Strategy

**Strategy 1: MA Crossover**
```
Signal: Fast MA crosses Slow MA
Buy when: Fast MA > Slow MA
Sell when: Fast MA < Slow MA

Parameters:
- Fast Period: 20 (shorter trend)
- Slow Period: 50 (longer trend)
```

**Strategy 2: RSI Mean Reversion**
```
Signal: RSI enters extreme zones
Buy when: RSI < 30 (oversold)
Sell when: RSI > 70 (overbought)

Parameters:
- RSI Period: 14
- Oversold threshold: 30
- Overbought threshold: 70
```

**Strategy 3: Bollinger Band**
```
Signal: Price touches bands
Buy when: Price < Lower Band
Sell when: Price > Upper Band

Parameters:
- Period: 20
- Std Dev: 2
```

#### Step 3: Run and Interpret Results

| Metric | Meaning | Good Range |
|--------|---------|-----------|
| Total Return | Total profit/loss | Varies by market |
| Sharpe Ratio | Risk-adjusted return | >1 acceptable, >2 good |
| Max Drawdown | Worst peak-to-trough | Lower is better |
| Win Rate | % profitable trades | >50% for mean reversion |
| # Trades | Number of round trips | Depends on strategy |

#### Step 4: Important Backtesting Concepts

**Look-ahead Bias Prevention:**
- Trades execute at the **next bar's open** after signal
- This prevents "cheating" by using same-bar information

**Transaction Costs:**
```
Real cost = Commission + Slippage

Commission: Explicit fee per trade
Slippage: Price difference between order and execution
```

**Overfitting Warning:**
```
Don't optimize parameters to maximize past returns!
This is called "curve fitting" and doesn't work on new data.

Instead:
1. Test on one time period
2. Validate on a different time period
3. Use robust, simple strategies
```

---

### Page 5: Prediction

**What you'll learn:** Machine learning for trading.

#### Step 1: Configure the Experiment

```
Ticker: Stock to analyze
Forward Days: How far ahead to predict (1-20)
Model Type: Choose algorithm
Test Ratio: % data for testing (default 20%)
```

#### Step 2: Choose a Model

| Model | Strengths | Weaknesses |
|-------|-----------|------------|
| **Random Forest** | Handles non-linear patterns | Can overfit |
| **Logistic Regression** | Simple, interpretable | Linear only |
| **Gradient Boosting** | Often best performance | More complex |

#### Step 3: Run Training

Click "Train Model" to:
1. Generate features from historical data
2. Split data chronologically (no random shuffle!)
3. Train the model
4. Evaluate on test set

#### Step 4: Interpret Results

**Performance Metrics:**
```
Accuracy: % correct predictions
Precision: % of "UP" predictions that were correct
Recall: % of actual UP days correctly predicted
F1 Score: Balance of precision and recall
```

**Feature Importance:**
Shows which factors the model relies on most:
```
Common important features:
- return_20d: 20-day momentum
- volatility_20d: Recent volatility
- rsi_14: RSI indicator
- ma_dist_20: Distance from MA
```

#### Step 5: Understand the Prediction

The model outputs a **probability**, not a guarantee:

```
Probability = 70% UP means:
"The model believes there's a 70% chance the price will go up"

This does NOT mean:
- It will definitely go up
- The model is always right
- You should blindly follow it
```

#### Step 6: Critical ML Concepts

**Data Leakage Prevention:**
```python
# WRONG: Random split
X_train, X_test = train_test_split(X, test_size=0.2)

# CORRECT: Time-series split
X_train = X[:int(0.8 * len(X))]  # First 80% for training
X_test = X[int(0.8 * len(X)):]   # Last 20% for testing
```

**Feature Engineering:**
```
Good features use ONLY past information:
✓ return_5d (past 5 days return)
✓ rsi_14 (calculated from past 14 days)
✗ future_return (target, not a feature!)
```

**Model Drift:**
```
Models trained on 2020-2023 data may not work in 2024+
Markets change! Periodically retrain.
```

---

## Understanding the Metrics

### Risk Metrics Explained

#### Sharpe Ratio
```
Sharpe = (Portfolio Return - Risk-Free Rate) / Portfolio Volatility

Example:
Return = 15%, Risk-Free = 5%, Volatility = 10%
Sharpe = (15% - 5%) / 10% = 1.0

Interpretation:
< 1: Sub-par risk-adjusted return
1-2: Good
> 2: Excellent
> 3: Outstanding (rare)
```

#### Sortino Ratio
```
Sortino = (Return - Risk-Free) / Downside Volatility

Only penalizes negative returns, not all volatility.
Higher is better. Useful for asymmetric return distributions.
```

#### Maximum Drawdown
```
MDD = (Peak Value - Trough Value) / Peak Value

Example:
Stock goes: $100 → $150 → $80 → $120
MDD = ($150 - $80) / $150 = 46.7%

Interpretation: You lost 46.7% at worst.
```

#### Beta
```
Beta = Covariance(Stock, Market) / Variance(Market)

Beta = 1.0: Moves with market
Beta > 1: More volatile than market (e.g., 1.5 = 50% more volatile)
Beta < 1: Less volatile than market (e.g., 0.5 = 50% less volatile)
Beta < 0: Moves opposite to market (rare, inverse ETFs)
```

### Performance Metrics Explained

#### Alpha
```
Alpha = Stock Return - (Risk-Free + Beta × Market Risk Premium)

Alpha > 0: Outperformed risk-adjusted benchmark
Alpha < 0: Underperformed risk-adjusted benchmark
```

#### Information Ratio
```
IR = (Portfolio Return - Benchmark Return) / Tracking Error

Measures consistency of outperformance.
IR > 0.5 is good, IR > 1.0 is excellent.
```

#### Tracking Error
```
TE = Standard Deviation of (Portfolio Return - Benchmark Return)

How much the portfolio deviates from benchmark.
Lower = more similar to benchmark.
```

---

## Machine Learning Features

### Feature Engineering

The dashboard automatically generates these features:

**Momentum Features:**
- `return_5d`, `return_10d`, `return_20d`, `return_60d`
- Lagged returns (past performance)

**Volatility Features:**
- `volatility_5d`, `volatility_10d`, `volatility_20d`, `volatility_60d`
- Rolling standard deviation of returns

**Technical Features:**
- `rsi_14`: Relative Strength Index
- `macd`: MACD line
- `macd_signal`: MACD signal line
- `macd_hist`: MACD histogram
- `bb_position`: Position within Bollinger Bands
- `atr_ratio`: ATR as % of price

**Price Features:**
- `ma_dist_20`, `ma_dist_50`: Distance from moving averages
- `high_low_ratio`: High/Low ratio over window
- `volume_change`: Volume change over window

### Target Variables

The model can predict:

**Binary Classification:**
```
Target = 1 if future_return > 0
Target = 0 if future_return <= 0
```

**Multi-class (Future):**
```
Target = 0: Bottom 20% of returns
Target = 1: 20-40% of returns
Target = 2: 40-60% of returns
Target = 3: 60-80% of returns
Target = 4: Top 20% of returns
```

---

## Backtesting Strategies

### Strategy Comparison

| Strategy | Market Conditions | Pros | Cons |
|----------|------------------|------|------|
| **MA Crossover** | Trending | Captures big moves | Whipsaws in sideways |
| **RSI Mean Reversion** | Range-bound | Buys low, sells high | Misses trends |
| **Bollinger Band** | Range-bound | Clear entry/exit | Lag in fast moves |

### Performance Expectations

**Realistic expectations:**
```
Sharpe Ratio: 0.5 - 1.5 is realistic
Win Rate: 40-60% is normal
Max Drawdown: 20-40% is common

Don't expect:
- Sharpe > 2 (very rare)
- Win Rate > 70% (usually means overfitting)
- Max DD < 10% (too conservative, low returns)
```

### Common Pitfalls

**1. Survivorship Bias**
```
Testing only stocks that exist today ignores those that went bankrupt.
Use broad indices or include delisted stocks when possible.
```

**2. Look-Ahead Bias**
```
Using future information to make past decisions.
Always trade at next bar's open after signal.
```

**3. Overfitting**
```
Adding too many parameters to maximize past performance.
Simple strategies often work better out-of-sample.
```

**4. Ignoring Costs**
```
Commissions and slippage eat into returns.
High-frequency strategies need low costs to be profitable.
```

---

## AI Analysis Features

### What AI Provides

**Market Summary:**
- Overall market regime analysis
- Key risk factors
- Sector rotation insights
- Unusual conditions

**Stock Analysis:**
- Multi-factor synthesis
- Risk/reward assessment
- Key catalysts
- Warning signs

### Using AI Responsibly

**DO:**
- Use as a research starting point
- Consider multiple perspectives
- Cross-reference with your own analysis
- Understand the reasoning

**DON'T:**
- Follow blindly
- Treat as financial advice
- Ignore your own judgment
- Expect perfect predictions

### Prompt Engineering Tips

The AI uses carefully designed prompts. If you want to modify:

```
Good prompts:
✓ "Analyze the risk factors for NVDA given current valuation"
✓ "What are the key catalysts for AAPL this quarter?"
✓ "Compare MSFT and GOOGL on growth vs value metrics"

Poor prompts:
✗ "Should I buy NVDA?" (Too specific, risky)
✗ "Predict tomorrow's price" (Impossible, misleading)
✗ "What's the best stock?" (Too subjective)
```

---

## Data Management

### Cache System

**Location:** `data/cache/`

**How it works:**
1. First download: Fetches from Yahoo Finance, saves to cache
2. Subsequent downloads: Reads from cache if not expired
3. Cache expiry: 24 hours by default

**Clear cache:**
```bash
rm -rf data/cache/*.parquet
```

### Watchlist Storage

**Location:** `data/watchlists.json`

**Format:**
```json
{
  "Tech Growth": ["AAPL", "MSFT", "GOOGL"],
  "My Portfolio": ["SPY", "QQQ", "VWO"]
}
```

### Experiment Logs

**Location:** `data/experiments.jsonl`

**Format:**
```json
{"ticker": "AAPL", "model": "random_forest", "accuracy": 0.55, "timestamp": "2026-06-14T12:00:00"}
```

---

## Tips for Learning

### Learning Path Recommendation

**Week 1-2: Fundamentals**
1. Use Market Overview daily
2. Observe regime changes
3. Track sector rotation
4. Understand VIX interpretation

**Week 3-4: Technical Analysis**
1. Analyze different stocks on Stock Detail
2. Compare indicator signals
3. Notice divergences between price and indicators
4. Practice identifying support/resistance

**Week 5-6: Risk Management**
1. Calculate position sizes from volatility
2. Compare risk metrics across stocks
3. Understand drawdown recovery
4. Practice portfolio construction

**Week 7-8: Backtesting**
1. Test strategies on different time periods
2. Compare results across tickers
3. Understand why strategies fail
4. Learn about parameter sensitivity

**Week 9-10: Machine Learning**
1. Run experiments on familiar stocks
2. Study feature importance
3. Compare model types
4. Understand overfitting signs

**Week 11-12: Integration**
1. Combine all tools for complete analysis
2. Build your own research workflow
3. Document what works for you
4. Share insights with others

### Study Exercises

**Exercise 1: Market Regime**
```
1. Record today's market regime
2. Note VIX level and sector performance
3. Check back in 1 week - did regime change?
4. What caused the change?
```

**Exercise 2: Indicator Divergence**
```
1. Find a stock where RSI shows oversold (< 30)
2. Is price still falling? (bearish divergence)
3. Wait 5 days and check what happened
4. Did RSI predict a reversal?
```

**Exercise 3: Strategy Comparison**
```
1. Backtest MA Crossover on SPY (5 years)
2. Backtest RSI Mean Reversion on SPY (5 years)
3. Which performed better? Why?
4. What market conditions favor each?
```

**Exercise 4: ML Experiment**
```
1. Train a model on AAPL
2. Note top 3 important features
3. Train on MSFT
4. Are the same features important?
5. What does this tell you about each stock?
```

---

## Troubleshooting

### Common Issues

**"No data returned for ticker"**
```
Solutions:
1. Check ticker symbol (use Yahoo Finance format)
2. Check internet connection
3. Try a more liquid ticker (e.g., SPY)
```

**"Module not found"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**"Cache expired"**
```bash
# Clear cache
rm -rf data/cache/*.parquet
```

**AI Summary not working**
```bash
# Set API key
export BAIDU_API_KEY="your-key"

# Verify
echo $BAIDU_API_KEY
```

**Slow data loading**
```
This is normal on first run. Data is cached locally.
Subsequent loads should be faster.
```

### Getting Help

1. Check this user guide
2. Review the code documentation
3. Check reference repositories in `reference-repos/`
4. Read `docs/AI_Agents_vs_Traditional_ML.md` for concepts

---

## Appendix: Project Structure

```
quant-learning/
├── app.py                    # Main entry point
├── requirements.txt          # Dependencies
├── README.md                 # Project overview
├── USER_GUIDE.md            # This file
│
├── config/
│   ├── settings.py          # Configuration
│   ├── config.yaml          # YAML config
│   └── loader.py            # Config loader
│
├── data/
│   ├── cache/               # Cached price data
│   ├── watchlists.json      # Saved watchlists
│   └── experiments.jsonl    # ML experiment logs
│
├── pages/
│   ├── 1_Market_Overview.py
│   ├── 2_Stock_Detail.py
│   ├── 3_Watchlist.py
│   ├── 4_Backtest.py
│   └── 5_Prediction.py
│
├── features/
│   ├── indicators.py        # Technical indicators
│   ├── risk_metrics.py      # Risk calculations
│   └── ...
│
├── utils/
│   ├── data_loader.py       # Data fetching
│   ├── data_providers/      # Multi-source support
│   ├── chart_builder.py     # Chart creation
│   ├── market_regime.py     # Market state
│   ├── relative_performance.py
│   ├── watchlist_manager.py
│   └── ...
│
├── backtest/
│   ├── engine.py            # Backtest engine
│   └── strategies.py        # Trading strategies
│
├── ml/
│   ├── features.py          # Feature engineering
│   ├── models.py            # ML models
│   ├── validation.py        # Walk-forward validation
│   └── experiments.py       # Experiment tracking
│
├── agents/
│   ├── llm_client.py        # LLM API client
│   ├── market_summarizer.py # AI analysis
│   └── prompts.py           # Prompt templates
│
├── tests/                   # Unit tests
│
├── docs/
│   └── AI_Agents_vs_Traditional_ML.md
│
└── reference-repos/         # Reference implementations
    ├── TradingAgents/
    ├── ai-hedge-fund/
    ├── FinGPT/
    ├── qlib/
    └── OpenBB/
```

---

## Disclaimer

**IMPORTANT:** This dashboard is for **educational and research purposes only**.

- NOT financial advice
- NOT investment recommendations
- NOT guaranteed predictions
- Past performance does not indicate future results
- Always do your own research before making investment decisions
- Consider consulting a qualified financial advisor

**Use at your own risk.**

---

*Last updated: 2026-06-14*
*Version: 1.0*
