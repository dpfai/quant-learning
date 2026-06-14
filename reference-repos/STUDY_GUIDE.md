# Study & Work Guide

This document maps out which reference repositories to consult at different stages of the project development.

---

## Key Design Patterns from Reference Repos

### 1. Data Provider Pattern (TradingAgents)

**Location:** `reference-repos/TradingAgents/tradingagents/dataflows/`

**Structure:**
```
dataflows/
├── __init__.py
├── interface.py           # Abstract interface
├── y_finance.py          # Yahoo Finance provider
├── alpha_vantage.py      # Alpha Vantage provider
├── alpha_vantage_stock.py
├── alpha_vantage_fundamentals.py
├── fred.py               # FRED economic data
├── stocktwits.py         # Social sentiment
├── reddit.py             # Reddit sentiment
└── polymarket.py         # Prediction markets
```

**When to use:** Adding new data sources (Phase 1.5, Phase 3.5)

---

### 2. Pydantic Data Models (ai-hedge-fund)

**Location:** `reference-repos/ai-hedge-fund/src/data/models.py`

**Purpose:** Type-safe data validation

**Example:**
```python
from pydantic import BaseModel
from datetime import date

class Price(BaseModel):
    ticker: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

class FinancialMetrics(BaseModel):
    ticker: str
    report_date: date
    revenue: float
    net_income: float
    pe_ratio: float | None = None
```

**When to use:** Data validation, API responses, Phase 3.5 fundamentals

---

### 3. Agent Architecture (TradingAgents)

**Location:** `reference-repos/TradingAgents/tradingagents/agents/`

**Agent Types:**
- `fundamentals_analyst.py` - Financial analysis
- `sentiment_analyst.py` - News/social sentiment
- `news_analyst.py` - News processing
- `technical_analyst.py` - Technical indicators
- `researcher_bull.py` / `researcher_bear.py` - Debate
- `trader.py` - Decision making
- `risk_manager.py` - Risk assessment
- `portfolio_manager.py` - Final approval

**When to use:** Phase 10+ AI agents

---

### 4. Multi-Agent System Design (Detailed)

#### TradingAgents Agent Structure

```
tradingagents/agents/
├── analysts/
│   ├── fundamentals_analyst.py   # Company financials, performance metrics
│   ├── sentiment_analyst.py      # News, StockTwits, Reddit sentiment
│   ├── news_analyst.py           # Global news, macro indicators
│   └── technical_analyst.py      # MACD, RSI, technical patterns
├── researchers/
│   ├── researcher_bull.py        # Bullish argument construction
│   └── researcher_bear.py        # Bearish argument construction
├── trader/
│   └── trader.py                 # Trade decision making
├── risk_mgmt/
│   ├── risk_manager.py           # Risk evaluation
│   └── ...
├── managers/
│   └── portfolio_manager.py      # Final approval
└── schemas.py                    # Agent data schemas
```

#### ai-hedge-fund Agent Structure (19 Agents)

**Investor Persona Agents:**
| Agent | Investment Style |
|-------|-----------------|
| `warren_buffett.py` | Value investing, wonderful companies at fair price |
| `charlie_munger.py` | Wonderful businesses, mental models |
| `ben_graham.py` | Deep value, margin of safety |
| `peter_lynch.py` | Growth at reasonable price, "ten-baggers" |
| `phil_fisher.py` | Growth investing, scuttlebutt research |
| `cathie_wood.py` | Innovation, disruption, growth |
| `bill_ackman.py` | Activist investing, concentrated positions |
| `michael_burry.py` | Deep value, contrarian, special situations |
| `nassim_taleb.py` | Tail risk, antifragility, black swans |
| `stanley_druckenmiller.py` | Macro, asymmetric opportunities |
| `aswath_damodaran.py` | Valuation-focused, story + numbers |
| `mohnish_pabrai.py` | Dhandho investor, low-risk doubles |
| `rakesh_jhunjhunwala.py` | Growth investing, India-focused |

**Functional Agents:**
| Agent | Purpose |
|-------|---------|
| `fundamentals.py` | Financial statement analysis |
| `valuation.py` | Intrinsic value calculation |
| `sentiment.py` | Market sentiment analysis |
| `news_sentiment.py` | News-based sentiment |
| `technicals.py` | Technical indicator analysis |
| `risk_manager.py` | Risk metrics, position limits |
| `portfolio_manager.py` | Final trading decisions |
| `growth_agent.py` | Growth analysis |

#### Graph Orchestration (TradingAgents)

```
tradingagents/graph/
├── trading_graph.py      # Main graph definition
├── analyst_execution.py  # Parallel analyst execution
├── signal_processing.py  # Signal aggregation
├── propagation.py        # Agent propagation logic
├── reflection.py         # Reflection/feedback loops
├── conditional_logic.py  # Conditional routing
└── checkpointer.py       # State persistence
```

**Workflow:**
```
1. Analyst Team (parallel)
   ↓
2. Researcher Debate (bull vs bear)
   ↓
3. Trader Decision
   ↓
4. Risk Management Review
   ↓
5. Portfolio Manager Approval
```

#### Agent Communication Patterns

**Pattern 1: Sequential Pipeline**
```
Analyst → Researcher → Trader → Risk → PM
```

**Pattern 2: Parallel + Aggregation**
```
         ┌→ Fundamentals ─┐
         ├→ Sentiment ────┤
Data ─→  ├→ News ─────────┼→ Aggregator → Decision
         ├→ Technical ────┤
         └→ ... ──────────┘
```

**Pattern 3: Debate + Consensus**
```
Bullish ←── Debates ──→ Bearish
    │                    │
    └──→ Consensus ←────┘
```

**When to use:** Phase 10-12 AI agent implementation

---

### 4. Feature Engineering Pipeline (Qlib)

**Location:** `reference-repos/qlib/qlib/contrib/data/handler.py`

**Key classes:** `Alpha158`, `Alpha360`

**Features included in Alpha158:**
- Price features (OPEN, HIGH, LOW, VWAP)
- K-bar features
- Rolling statistics
- Time-based features

**When to use:** Phase 9 ML/Prediction

---

### 6. RD-Agent (Qlib)

**Location:** Separate repo at https://github.com/microsoft/RD-Agent

**Purpose:** LLM-based autonomous evolving agents for quant R&D

**Key Features:**
- Automated factor mining from data
- Model optimization
- Data-centric factor and model joint optimization
- Reads research papers and generates code

**When to use:** Advanced Phase - automated research

---

### 7. Multi-Provider LLM Support (TradingAgents)

**Location:** `reference-repos/TradingAgents/tradingagents/llm_clients/`

**Supported providers:**
- OpenAI (GPT)
- Anthropic (Claude)
- Google (Gemini)
- xAI (Grok)
- DeepSeek
- Qwen
- Ollama (local)

**When to use:** Phase 10+ AI integration

---

## Project Phases & Reference Repositories

### Phase 1: Data Infrastructure

**When working on:**
- Building data pipelines
- API integration for market data
- Data normalization and storage
- Real-time data fetching

**Primary Reference:** `TradingAgents/tradingagents/dataflows/`
- Study `interface.py` for abstract provider pattern
- Check `y_finance.py` for Yahoo Finance implementation
- Study `alpha_vantage_*.py` for multi-source pattern

**Secondary Reference:** `Qlib/`
- Study `qlib/data/` for efficient data storage
- Check `scripts/data_collector/` for data crawling patterns

**Specific files to study:**
| File | Purpose |
|------|---------|
| `dataflows/interface.py` | Abstract data provider interface |
| `dataflows/y_finance.py` | YFinance implementation with caching |
| `dataflows/alpha_vantage_stock.py` | Alternative data source example |
| `dataflows/utils.py` | Common utilities |

---

### Phase 2: Dashboard UI Development

**When working on:**
- Building Streamlit pages
- Data visualization
- User interaction patterns
- Multi-page app structure

**Primary Reference:** `ai-hedge-fund/app/`
- Streamlit web application implementation
- UI layout and interaction patterns
- Real-time updates and progress display

**Secondary Reference:** `OpenBB/`
- Workspace UI patterns (if applicable)

---

### Phase 3: Feature Engineering

**When working on:**
- Technical indicators
- Factor construction
- Feature transformation
- Alpha generation

**Primary Reference:** `Qlib/`
- Study `qlib/contrib/data/handler.py` for Alpha158/Alpha360 features
- Check `examples/` for feature engineering examples
- Study `qlib/data/ops.py` for expression-based feature construction

**Secondary Reference:** `TradingAgents/`
- Check `tradingagents/agents/technical_analyst.py` for indicator usage

---

### Phase 4: Sentiment Analysis & NLP

**When working on:**
- News sentiment analysis
- Social media analysis
- Financial text processing
- LLM-based analysis

**Primary Reference:** `FinGPT/`
- Study `fingpt/FinGPT_Sentiment_Analysis_v3/` for sentiment models
- Check `fingpt/FinGPT_RAG/` for RAG implementation
- Study `fingpt/FinGPT_Forecaster/` for news-based prediction

**Secondary Reference:** `TradingAgents/`
- Check `tradingagents/agents/sentiment_analyst.py` for sentiment integration

---

### Phase 5: Multi-Agent System Design

**When working on:**
- Agent architecture
- Agent communication
- Decision aggregation
- Multi-perspective analysis

**Primary Reference:** `TradingAgents/`
- Study `tradingagents/graph/trading_graph.py` for graph orchestration
- Check `tradingagents/agents/` for individual agent implementations
- Study researcher debate mechanism

**Secondary Reference:** `ai-hedge-fund/`
- Study `src/agents/` for agent persona patterns
- Check how multiple agents contribute to final decision
- Study investor persona implementation

---

### Phase 6: LLM Integration

**When working on:**
- LLM API integration
- Prompt engineering
- Multi-provider support
- Response parsing

**Primary Reference:** `TradingAgents/`
- Study `tradingagents/llm/` for multi-provider LLM support
- Check `tradingagents/default_config.py` for configuration patterns
- Study prompt templates in agent implementations

**Secondary Reference:** `ai-hedge-fund/`
- Check `src/agents/` for prompt patterns
- Study LLM API usage patterns

---

### Phase 7: Portfolio Management & Risk

**When working on:**
- Position sizing
- Risk metrics calculation
- Portfolio optimization
- Risk management

**Primary Reference:** `ai-hedge-fund/`
- Study `src/agents/risk_manager.py` for risk metrics
- Check `src/agents/portfolio_manager.py` for portfolio decisions

**Secondary Reference:** `TradingAgents/`
- Check `tradingagents/agents/risk_manager.py` for risk patterns

---

### Phase 8: Backtesting

**When working on:**
- Strategy backtesting
- Performance metrics
- Historical simulation
- Strategy evaluation

**Primary Reference:** `Qlib/`
- Study `qlib/contrib/strategy/` for strategy patterns
- Check `qlib/contrib/report/` for analysis reports
- Study `examples/benchmarks/` for complete workflows

**Secondary Reference:** `ai-hedge-fund/`
- Check `src/backtester.py` for backtesting implementation

---

### Phase 9: Reinforcement Learning (Advanced)

**When working on:**
- RL-based trading
- Order execution optimization
- Continuous decision making

**Primary Reference:** `Qlib/`
- Study `examples/rl_order_execution/` for RL examples
- Check `qlib/rl/` for RL framework
- Study `examples/benchmarks_dynamic/` for adaptive models

---

## Quick Reference by Task

| Task | Go To |
|------|-------|
| Add new data source | `TradingAgents/tradingagents/dataflows/interface.py` |
| Implement data provider | `TradingAgents/tradingagents/dataflows/y_finance.py` |
| Data model validation | `ai-hedge-fund/src/data/models.py` |
| Build a new agent | `TradingAgents/tradingagents/agents/` |
| Design agent workflow | `TradingAgents/tradingagents/graph/trading_graph.py` |
| Agent orchestration | `TradingAgents/tradingagents/graph/analyst_execution.py` |
| Investor persona agent | `ai-hedge-fund/src/agents/warren_buffett.py` |
| Risk manager agent | `ai-hedge-fund/src/agents/risk_manager.py` |
| Portfolio manager agent | `ai-hedge-fund/src/agents/portfolio_manager.py` |
| Create technical indicators | `Qlib/qlib/contrib/data/handler.py` |
| Implement sentiment analysis | `FinGPT/fingpt/FinGPT_Sentiment_Analysis_v3/` |
| Build backtesting | `Qlib/examples/benchmarks/` |
| Design UI components | `ai-hedge-fund/app/` |
| LLM integration | `TradingAgents/tradingagents/llm_clients/` |
| Risk management | `ai-hedge-fund/src/agents/risk_manager.py` |
| Fine-tune financial LLM | `FinGPT/fingpt/` |
| Feature engineering | `Qlib/qlib/contrib/data/handler.py` (Alpha158) |
| Cache implementation | `ai-hedge-fund/src/data/cache.py` |
| Agent schemas | `TradingAgents/tradingagents/agents/schemas.py` |
| Debate mechanism | `TradingAgents/tradingagents/agents/researchers/` |
| Signal processing | `TradingAgents/tradingagents/graph/signal_processing.py` |

---

## Study Order Recommendation

For developers new to AI-based trading systems:

1. **Start with OpenBB** - Understand data infrastructure
2. **Then ai-hedge-fund** - Simple multi-agent architecture, good for learning
3. **Move to TradingAgents** - More sophisticated agent design
4. **Study FinGPT** - When you need financial NLP/sentiment
5. **Deep dive Qlib** - For quantitative modeling and backtesting

---

## API Keys Required

When you're ready to run these repos, you'll need:

| Service | Usage | Repositories |
|---------|-------|--------------|
| OpenAI API | LLM inference | TradingAgents, ai-hedge-fund, FinGPT |
| Anthropic API | Claude models | TradingAgents |
| Google API | Gemini models | TradingAgents |
| Alpha Vantage | Market data | TradingAgents |
| Financial Datasets API | Financial data | ai-hedge-fund |
| Hugging Face | Model downloads | FinGPT |

---

## Notes

- Keep this guide updated as the project progresses
- Add your own notes and learnings in this file
- When stuck on a specific problem, check the relevant reference repo first

---

## Additional Resources by Repo

### TradingAgents - Key Files

| File | Purpose |
|------|---------|
| `tradingagents/dataflows/interface.py` | Data provider abstract interface |
| `tradingagents/dataflows/y_finance.py` | YFinance implementation |
| `tradingagents/agents/*.py` | Individual agent implementations |
| `tradingagents/graph/trading_graph.py` | Multi-agent orchestration |
| `tradingagents/llm_clients/` | Multi-provider LLM support |
| `tradingagents/default_config.py` | Configuration patterns |

### ai-hedge-fund - Key Files

| File | Purpose |
|------|---------|
| `src/data/models.py` | Pydantic data models |
| `src/data/cache.py` | Caching implementation |
| `src/api.py` | Data API integration |
| `src/agents/risk_manager.py` | Risk metrics calculation |
| `src/agents/portfolio_manager.py` | Portfolio decisions |
| `src/backtester.py` | Backtesting framework |
| `app/` | Streamlit web application |

### FinGPT - Key Files

| File | Purpose |
|------|---------|
| `fingpt/FinGPT_Sentiment_Analysis_v3/` | Sentiment analysis models |
| `fingpt/FinGPT_Forecaster/` | Stock prediction model |
| `fingpt/FinGPT_RAG/` | RAG implementation |
| `fingpt/FinGPT_Benchmark/` | Instruction tuning benchmark |

### Qlib - Key Files

| File | Purpose |
|------|---------|
| `qlib/contrib/data/handler.py` | Alpha158/Alpha360 features |
| `qlib/contrib/model/` | Model implementations |
| `qlib/contrib/strategy/` | Trading strategies |
| `qlib/contrib/report/` | Analysis reports |
| `examples/benchmarks/` | Complete workflow examples |
| `examples/rl_order_execution/` | RL examples |

### OpenBB - Key Files

| File | Purpose |
|------|---------|
| `openbb/` | Python SDK |
| `openbb/providers/` | Data provider implementations |
