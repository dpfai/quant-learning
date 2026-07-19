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

# Phase 12 — Factor Framework (因子框架)

Goal:

从技术指标驱动的单股票分析，升级到因子驱动的 cross-sectional 研究框架。

这是 quant research 的核心语言。技术指标（MA/RSI/MACD）是单股票时序工具，因子是 cross-sectional 的选股逻辑。Phase 12 之后，项目的重心从"看图"转向"选股"。

Learn:

- CAPM / Fama-French 三因子、五因子模型
- factor exposure / loading（β）
- cross-sectional vs time-series 分析的区别
- value / momentum / quality / low-volatility / size 因子的经济学逻辑
- IC (Information Coefficient) 和 rank IC
- 分层回测 (quantile portfolio / decile spread)
- Fama-MacBeth 回归

Implement:

```text
features/factors/
├── value.py          # PB, PE, EV/EBITDA
├── momentum.py       # 12-1 momentum, 6-1, cross-sectional rank
├── quality.py        # ROE, gross profitability, accruals
├── volatility.py     # realized vol, beta
└── size.py           # market cap

backtest/
└── factor_analysis.py
    ├── calc_ic()           # IC 和 rank IC 时间序列
    ├── quantile_portfolio() # 分层回测（5/10 分位）
    └── fama_macbeth()      # Fama-MacBeth 回归

pages/
└── 7_Factor_Research.py    # 因子研究页面
```

Libraries:

```text
statsmodels
alphalens (参考，可自实现)
```

Phase 完成标准：

- 能计算至少 5 个经典因子
- 能对任意因子跑 IC 分析和分层回测
- 能输出因子报告（IC 时间序列、分位组收益、单调性检验）
- 能理解因子收益和因子暴露的区别

---

# Phase 13 — Alpha Research Discipline (Alpha 验证纪律)

Goal:

建立严格验证 alpha 真实性的工作流，避免自我欺骗。

这是个人量化最容易忽视、但最致命的环节。Phase 9 的 ML prediction 如果没有 Phase 13 的纪律，几乎必然在回测里过拟合。

Learn:

- multiple testing problem（Bonferroni / Holm 校正）
- deflated Sharpe ratio (Bailey & López de Prado)
- walk-forward validation 严格化
- factor orthogonalization（对已知因子做 neutralization 后看纯 alpha）
- lookahead bias / survivorship bias 的系统性防范
- turnover 和 transaction cost 建模
- factor decay / half-life 分析

Implement:

```text
backtest/
└── alpha_validation.py
    ├── bonferroni_correction()
    ├── deflated_sharpe()
    ├── orthogonalize_factor()  # 对 market/size/value neutralize
    ├── factor_turnover()
    └── factor_halflife()
```

- 完善 walk-forward 流程（已有 retrain.py，扩展到因子层）
- config 里加入 transaction cost 模型
- 任何新因子必须走完整验证 pipeline

Phase 完成标准：

- 任何新因子必须通过：IC 稳定性 + 分层单调 + 正交化后仍显著 + 样本外有效
- 有 multiple testing 校正报告
- 能回答"这个因子是真 alpha 还是已知因子的衍生暴露"

---

# Phase 14 — LLM Sentiment Factor (NLP 情绪因子) ⭐ 差异化机会

Goal:

用 DeepSeek / LLM 把非结构化文本变成结构化交易信号。

这是个人能用最低成本获取信息优势的路径，也是本项目最现实的 alpha 来源。机构在另类数据上砸几十万美金，个人用 LLM + 免费文本数据可以做出有差异的因子。

Learn:

- earnings call transcript 分析（管理层语气、前瞻性措辞变化）
- 10-K / 10-Q 风险因子变化检测
- 新闻事件分类与影响量化
- aspect-based sentiment（不是简单正负面，而是按维度：语气、确定性、前瞻性）
- LLM prompt engineering for structured extraction
- NLP 因子的 IC 检验和 decay 特征

Implement:

```text
agents/sentiment/
├── transcript_analyzer.py  # DeepSeek 分析 earnings call
├── news_processor.py       # 新闻事件分类 + 影响打分
└── filing_diff.py          # 10-K 年度对比，提取新增风险

features/factors/
└── sentiment.py            # LLM 输出转成因子值
```

- 数据源：SEC EDGAR（免费）、earnings call transcript（免费 API）、新闻 RSS
- 集成到 Phase 12 的 factor framework 做 IC 检验
- 用 Phase 13 的纪律验证

Libraries:

```text
DeepSeek API (或本地 Ollama)
requests
beautifulsoup4
```

Phase 完成标准：

- 至少一个 NLP 因子通过 Phase 13 的 alpha 验证流程
- 有完整的 prompt 模板和批量处理 pipeline
- 能对比 NLP 因子 vs 经典因子的 IC 表现

---

# Phase 15 — Portfolio Construction (组合构建)

Goal:

从单股票 / 单策略，升级到组合层面的构建和优化。

量化的最终输出是组合，不是个股推荐。Phase 12-14 产出的是因子信号，Phase 15 把信号变成可执行的组合。

Learn:

- mean-variance optimization (Markowitz)
- 因子暴露约束下的优化
- risk budget / risk parity
- transaction cost aware optimization
- rebalancing 频率和 turnover 控制
- portfolio 层面的风险分解（风险归因到因子）

Implement:

```text
portfolio/
├── optimizer.py       # PyPortfolioOpt 封装
├── constraints.py     # 因子暴露约束、行业约束、权重上限
└── risk_budget.py     # 风险预算分配

pages/
└── 8_Portfolio_Builder.py
```

- 集成因子暴露（Phase 12）做约束优化
- 集成 transaction cost 模型（Phase 13）

Libraries:

```text
PyPortfolioOpt
cvxpy
```

Phase 完成标准：

- 能基于因子信号构建优化组合
- 能控制因子暴露和行业集中度
- 能输出组合层面的风险报告（波动率、VaR、因子归因）

---

# Phase 16 — Sector Edge (行业护城河) ⭐ 个人差异化

Goal:

把你的广告 / 营销 / 消费者行为领域知识，编码成 sector-specific 因子。

这是你作为个人唯一可能赢机构的角落。在你懂的 sector 上（ad-tech / digital advertising / consumer marketing），你比通用分析师更懂业务逻辑。你的广告测量背景（理解 incrementality、attribution、causal）在这里是真正的优势。

Learn:

- sector rotation 逻辑
- ad-tech / marketing / digital advertising 行业的关键指标
- 如何把领域知识转化为可量化的因子
- sector-neutral vs sector-specific 因子的区别
- 产业链传导因子（上游 / 下游信号传导）

Implement:

```text
features/factors/sector/
├── ad_tech_signals.py     # 广告行业专用因子
│                          # (数字广告 spend 增长、eCPM 趋势、platform mix 变化)
├── consumer_signals.py    # 消费者行为因子
└── supply_chain_factor.py # 供应链传导

pages/
└── 9_Sector_Research.py   # sector 研究页面
```

- 用 Phase 12-13 的框架做严格验证
- 监控你覆盖的 sector 的关键数据源和事件
- 因子逻辑必须有领域知识支撑，不是纯数据挖掘

Phase 完成标准：

- 至少 2 个 sector-specific 因子通过 alpha 验证
- 因子逻辑可解释（有领域知识支撑，不是 spurious correlation）
- 能持续监控和迭代这些因子

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

