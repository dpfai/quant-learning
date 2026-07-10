# Finance AI Agent Repositories Reference

## Overview

This document summarizes 5 major open-source Finance AI Agent repositories cloned for reference and learning purposes.

---

## 1. TradingAgents (TauricResearch)

**GitHub:** https://github.com/TauricResearch/TradingAgents
**Stars:** 81,368
**Local Path:** `./TradingAgents/`

### What It Is
A multi-agent LLM trading framework that mimics real-world trading firms. Built on LangGraph with support for multiple LLM providers.

### Key Features
- **Analyst Team:** Fundamentals Analyst, Sentiment Analyst, News Analyst, Technical Analyst
- **Researcher Team:** Bullish and bearish researchers for structured debate
- **Trader Agent:** Composes reports and makes trading decisions
- **Risk Management & Portfolio Manager:** Evaluates portfolio risk, approves/rejects transactions
- **Persistence:** Decision log, checkpoint resume

### Tech Stack
- LangGraph for workflow orchestration
- Multi-provider LLM support (OpenAI, Google, Anthropic, xAI, DeepSeek, Qwen, GLM, MiniMax, Ollama)
- CLI and Python package interface

### Key Files to Study
- `tradingagents/graph/trading_graph.py` - Main graph orchestration
- `tradingagents/agents/` - Individual agent implementations
- `tradingagents/default_config.py` - Configuration patterns

---

## 2. ai-hedge-fund (virattt)

**GitHub:** https://github.com/virattt/ai-hedge-fund
**Stars:** 59,596
**Local Path:** `./ai-hedge-fund/`

### What It Is
An AI-powered hedge fund proof-of-concept with multiple investor personas working together.

### Key Features
- **19 specialized agents** including:
  - Famous investor personas (Warren Buffett, Michael Burry, Cathie Wood, Bill Ackman, etc.)
  - Functional agents (Valuation, Sentiment, Fundamentals, Technicals)
  - Risk Manager and Portfolio Manager
- CLI and Web Application interfaces
- Backtesting capability
- Multi-date analysis support

### Tech Stack
- Poetry for dependency management
- OpenAI/GROQ/Anthropic/DeepSeek API support
- Financial Datasets API for data
- Streamlit for web UI

### Key Files to Study
- `src/agents/` - Agent implementations
- `src/main.py` - Main workflow
- `src/backtester.py` - Backtesting logic
- `app/` - Streamlit web application

---

## 3. FinGPT (AI4Finance-Foundation)

**GitHub:** https://github.com/AI4Finance-Foundation/FinGPT
**Stars:** 20,356
**Local Path:** `./FinGPT/`

### What It Is
Open-source financial large language models for financial NLP tasks. Democratizes financial LLM development.

### Key Features
- **FinGPT-Forecaster:** Stock price movement prediction based on news
- **Financial Sentiment Analysis:** Best-in-class performance (outperforms GPT-4)
- **Multi-task LLMs:** Sentiment, relation extraction, headline classification, NER
- **RAG Framework:** Retrieval-augmented generation for finance
- **Low-cost fine-tuning:** ~$300 vs BloombergGPT's $3M

### Tech Stack
- LoRA/QLoRA for efficient fine-tuning
- Hugging Face transformers
- Multiple base models (Llama-2, Falcon, ChatGLM2, Qwen)

### Key Files to Study
- `fingpt/FinGPT_Forecaster/` - Stock prediction model
- `fingpt/FinGPT_Sentiment_Analysis_v3/` - Sentiment analysis
- `fingpt/FinGPT_Benchmark/` - Instruction tuning benchmark
- `fingpt/FinGPT_RAG/` - RAG implementation

---

## 4. Qlib (Microsoft)

**GitHub:** https://github.com/microsoft/qlib
**Stars:** 43,854
**Local Path:** `./qlib/`

### What It Is
Microsoft's AI-oriented quantitative investment platform covering the full ML pipeline from data to trading.

### Key Features
- **Full ML Pipeline:** Data processing, model training, backtesting, serving
- **Model Zoo:** 20+ SOTA models (LightGBM, LSTM, GRU, Transformer, GAT, TFT, etc.)
- **Learning Paradigms:** Supervised learning, reinforcement learning, meta-learning
- **High-frequency Trading:** 1-minute data support
- **RD-Agent:** LLM-based autonomous factor mining

### Tech Stack
- PyTorch for deep learning
- Custom data server (high performance)
- Reinforcement learning framework
- Point-in-Time database

### Key Files to Study
- `qlib/contrib/model/` - Model implementations
- `qlib/contrib/strategy/` - Trading strategies
- `qlib/contrib/data/` - Data handlers
- `examples/benchmarks/` - Model examples
- `examples/rl_order_execution/` - RL examples

---

## 5. OpenBB (OpenBB-finance)

**GitHub:** https://github.com/OpenBB-finance/OpenBB
**Stars:** 68,360
**Local Path:** `./OpenBB/`

### What It Is
Open Data Platform for financial data integration. "Connect once, consume everywhere" infrastructure.

### Key Features
- **100+ Data Integrations:** Market data, fundamentals, alternative data
- **Multiple Interfaces:** Python SDK, CLI, REST API, Workspace UI
- **MCP Servers:** For AI agent integration
- **Data Normalization:** Consistent format across sources
- **Extensible:** Easy to add custom data sources

### Tech Stack
- FastAPI for REST API
- Python SDK (`pip install openbb`)
- Streamlit-based Workspace UI

### Key Files to Study
- `openbb/core/` - Core SDK
- `openbb/providers/` - Data provider implementations
- `openbb/cli/` - CLI implementation
- `examples/` - Usage examples

---

## Comparison Matrix

| Feature | TradingAgents | ai-hedge-fund | FinGPT | Qlib | OpenBB |
|---------|---------------|---------------|--------|------|--------|
| Multi-Agent System | ✅ | ✅ | ❌ | ❌ | ❌ |
| LLM Integration | ✅ | ✅ | ✅ | ✅ (RD-Agent) | ✅ (MCP) |
| Trading Decisions | ✅ | ✅ | ❌ | ✅ | ❌ |
| Sentiment Analysis | ✅ | ✅ | ✅ | ❌ | ✅ |
| Backtesting | ❌ | ✅ | ❌ | ✅ | ❌ |
| RL Support | ❌ | ❌ | ❌ | ✅ | ❌ |
| Data Integration | ✅ | ✅ | ✅ | ✅ | ✅✅ |
| Fine-tuning LLMs | ❌ | ❌ | ✅ | ❌ | ❌ |
| Web UI | CLI only | ✅ | Demo | ❌ | ✅ |

---

## Quick Start Commands

```bash
# TradingAgents
cd TradingAgents
pip install .
tradingagents

# ai-hedge-fund
cd ai-hedge-fund
poetry install
poetry run python src/main.py --ticker AAPL

# FinGPT
pip install fingpt

# Qlib
pip install pyqlib

# OpenBB
pip install openbb
python -c "from openbb import obb; print(obb.equity.price.historical('AAPL').to_dataframe())"
```
