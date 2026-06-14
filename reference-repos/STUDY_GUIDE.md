# Study & Work Guide

This document maps out which reference repositories to consult at different stages of the project development.

---

## Project Phases & Reference Repositories

### Phase 1: Data Infrastructure

**When working on:**
- Building data pipelines
- API integration for market data
- Data normalization and storage
- Real-time data fetching

**Primary Reference:** `OpenBB/`
- Study `openbb/providers/` for data provider patterns
- Check `openbb/core/` for data handling architecture
- Example: How to normalize different data sources into unified format

**Secondary Reference:** `Qlib/`
- Study `qlib/data/` for efficient data storage
- Check `scripts/data_collector/` for data crawling patterns

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
| Add new data source | `OpenBB/openbb/providers/` |
| Build a new agent | `TradingAgents/tradingagents/agents/` |
| Design agent workflow | `TradingAgents/tradingagents/graph/` |
| Create technical indicators | `Qlib/qlib/contrib/data/handler.py` |
| Implement sentiment analysis | `FinGPT/fingpt/FinGPT_Sentiment_Analysis_v3/` |
| Build backtesting | `Qlib/examples/benchmarks/` |
| Design UI components | `ai-hedge-fund/app/` |
| LLM integration | `TradingAgents/tradingagents/llm/` |
| Risk management | `ai-hedge-fund/src/agents/risk_manager.py` |
| Fine-tune financial LLM | `FinGPT/fingpt/` |

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
