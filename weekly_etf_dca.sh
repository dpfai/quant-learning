#!/bin/bash
# AI Trading Arena - Weekly ETF DCA Update
# Runs every Tuesday after market close (1:00 PM PDT)
# Injects $500 into each ETF portfolio and updates DB

export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
QL_DIR="$HOME/AI-workplace/quant-learning"
LOG_FILE="$QL_DIR/data/daily_update.log"
PYTHON="$QL_DIR/venv/bin/python"

echo "$(date): === Weekly ETF DCA ===" >> "$LOG_FILE"

cd "$QL_DIR"
source venv/bin/activate

python -c "
import json, sqlite3, yfinance as yf, pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path('$QL_DIR/data/trading_arena.db')
ETF_FILE = Path('$HOME/.openclaw/workspace-explorer/investments/portfolio_data/portfolio_tracking.json')
WEEKLY = 500.0
ETF_CONFIGS = {
    'etf_aggressive': {'VOO': 0.425, 'VGT': 0.425, 'SMH': 0.15},
    'etf_balanced':   {'VOO': 0.50, 'VGT': 0.40, 'SMH': 0.10},
    'etf_conservative':{'VOO': 0.60, 'VGT': 0.35, 'SMH': 0.05},
}
ETF_MAP = {'组合A-激进型': 'etf_aggressive', '组合B-平衡型': 'etf_balanced', '组合C-稳健型': 'etf_conservative'}

today = datetime.now().strftime('%Y-%m-%d')
tickers = ['VOO', 'VGT', 'SMH']
prices = yf.download(tickers, period='5d', progress=False)
if isinstance(prices.columns, pd.MultiIndex): prices = prices['Close']

# Get latest trading day price
latest_prices = {}
for t in tickers:
    if t in prices.columns:
        latest_prices[t] = float(prices[t].dropna().iloc[-1])

with sqlite3.connect(DB_PATH) as conn:
    for cn_name, source in ETF_MAP.items():
        alloc = ETF_CONFIGS[source]
        
        # Get current cash and total_cost
        row = conn.execute('SELECT cash, total_cost FROM equity_curve WHERE source=? ORDER BY date DESC LIMIT 1', (source,)).fetchone()
        cash = row[0] if row else 10000.0
        total_cost = row[1] if row else 10000.0
        
        cash += WEEKLY
        total_cost += WEEKLY
        
        for ticker, ratio in alloc.items():
            price = latest_prices.get(ticker)
            if not price: continue
            amount = WEEKLY * ratio
            shares = amount / price
            
            # Update holdings
            h_row = conn.execute('SELECT shares, total_cost FROM holdings WHERE source=? AND ticker=? AND date=(SELECT MAX(date) FROM holdings WHERE source=? AND ticker=?)', (source, ticker, source, ticker)).fetchone()
            old_shares = h_row[0] if h_row else 0
            old_cost = h_row[1] if h_row else 0
            new_shares = old_shares + shares
            new_cost = old_cost + amount
            
            conn.execute('INSERT OR REPLACE INTO holdings VALUES (?,?,?,?,?,?,?,?,?)',
                (today, source, ticker, new_shares, new_cost/new_shares if new_shares>0 else 0, price, new_shares*price, 0, 0))
            
            conn.execute('INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                (f'{source}_{today}_{ticker}_buy', today, source, 'dca', 'buy', ticker, price, shares, amount, cash, f'Weekly DCA {ratio*100:.1f}%'))
        
        # Update equity
        pv = 0
        for ticker in alloc:
            h = conn.execute('SELECT shares FROM holdings WHERE source=? AND ticker=? AND date=?', (source, ticker, today)).fetchone()
            if h and h[0] > 0:
                price = latest_prices.get(ticker, 0)
                pv += h[0] * price
        
        tv = cash + pv
        rp = (tv - total_cost) / total_cost if total_cost > 0 else 0
        conn.execute('INSERT OR REPLACE INTO equity_curve VALUES (?,?,?,?,?,?,?)',
            (today, source, tv, cash, pv, total_cost, rp))
    
    print(f'ETF DCA: updated {today} for all 3 portfolios')
" 2>> "$LOG_FILE" || echo "$(date): ETF DCA FAILED" >> "$LOG_FILE"

echo "$(date): === Weekly ETF DCA Done ===" >> "$LOG_FILE"
