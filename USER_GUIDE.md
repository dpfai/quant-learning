# User Guide

## Dashboard Pages

- **Market Overview** compares major ETFs, classifies the market regime, shows
  VIX conditions, ranks sectors, and optionally generates an AI summary.
- **Stock Detail** shows price action, technical indicators, risk metrics,
  relative performance versus SPY, CSV export, and optional AI analysis.
- **Watchlist** manages persistent named ticker groups and compares return/risk
  metrics across assets.
- **Backtesting** evaluates three transparent signal strategies with delayed
  execution, commission, and slippage.
- **Prediction Experiments** trains time-series classification models and reports
  out-of-sample metrics and feature importance.

## Optional AI Setup

Set an API key only when you want to use the AI Summary buttons:

```bash
export OPENAI_API_KEY="your-key"
```

The rest of the dashboard does not require an OpenAI API key. AI-generated text
is for education and research only, not financial advice.

## Data And Models

- Market data comes from Yahoo Finance and is cached in `data/cache/`.
- Watchlists are stored locally in `data/watchlists.json`.
- ML experiments use chronological train/test splits. Reported probabilities are
  experimental model outputs, not calibrated forecasts.
- Backtests use next-bar execution to avoid same-bar look-ahead and include
  configurable costs.
