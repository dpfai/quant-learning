"""Prompt templates for objective educational summaries."""

MARKET_SUMMARY_SYSTEM = """You are a professional market research assistant.
Provide concise, objective analysis based only on the supplied data.
Do not give investment advice or buy/sell recommendations.
State uncertainty and finish with an educational-use disclaimer."""

MARKET_SUMMARY_PROMPT = """Analyze this market snapshot:

Market regime: {regime}
VIX: {vix:.1f}
SPY price: {spy_price:.2f}
SPY distance from MA50: {spy_change:+.1%}

Sector performance:
{sector_performance}

Top sector: {top_sector}
Weakest sector: {weak_sector}
Volatility condition: {volatility_level}

Provide:
1. A 2-3 sentence overview
2. Key risks to monitor
3. Research themes worth investigating
"""

STOCK_ANALYSIS_PROMPT = """Analyze this stock snapshot:

Ticker: {ticker}
Current price: {price:.2f}
5-day return: {return_5d:+.1%}
20-day return: {return_20d:+.1%}
YTD return: {return_ytd:+.1%}
Annualized volatility: {volatility:.1%}
Maximum drawdown: {max_dd:.1%}
Sharpe ratio: {sharpe:.2f}
Beta versus SPY: {beta:.2f}
RSI(14): {rsi:.1f}
MACD: {macd:.2f}
Above MA50: {above_ma50}
Above MA200: {above_ma200}

Provide a brief objective analysis in 3-4 sentences. Identify one strength,
one risk, and one follow-up research question. Do not recommend buying or selling.
"""
