#!/bin/bash
# AI Trading Arena - Daily Update Script
# Runs all strategies, updates DB, exports JSON, pushes to GitHub
# Scheduled: every weekday after market close (1:00 PM PDT = 13:00)

set -e

# ── Setup ──
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
QL_DIR="$HOME/AI-workplace/quant-learning"
ARENA_DIR="$HOME/AI-workplace/ai-trading-arena"
LOG_FILE="$QL_DIR/data/daily_update.log"
PYTHON="$QL_DIR/venv/bin/python"

echo "$(date): === Daily Update Start ===" >> "$LOG_FILE"

cd "$QL_DIR"
source venv/bin/activate

# ── Step 1: Quant Learning daily runner ──
echo "$(date): Running Quant Learning daily_runner..." >> "$LOG_FILE"
python daily_runner.py --end "$(date +%Y-%m-%d)" 2>> "$LOG_FILE" || echo "$(date): QL daily_runner FAILED" >> "$LOG_FILE"

# ── Step 2: Import AI Analyst (海岩) signals ──
# Parse latest stock_analysis JSON and write signals to DB
echo "$(date): Importing AI Analyst signals..." >> "$LOG_FILE"
python -c "
import json, sqlite3, re, os, sys
from pathlib import Path
from datetime import datetime

DB_PATH = Path('$QL_DIR/data/trading_arena.db')
HAIYAN_DIR = Path('$HOME/.openclaw/workspace-explorer/investments')
SOURCE = 'ai_analyst'
INITIAL_CASH = 10000.0
WEEKLY = 500.0
HAIYAN_STOCKS = ['META', 'GOOGL', 'AMZN', 'NFLX', 'RKLB', 'ACHR', 'JOBY']

# Find latest analysis file
files = sorted(HAIYAN_DIR.glob('stock_analysis_*.json'))
if not files:
    print('No analysis files found, skipping.')
    sys.exit(0)

latest_file = files[-1]
m = re.search(r'(\d{4}-\d{2}-\d{2})', latest_file.name)
file_date = m.group(1) if m else datetime.now().strftime('%Y-%m-%d')

# Check if already imported
with sqlite3.connect(DB_PATH) as conn:
    existing = conn.execute(
        'SELECT COUNT(*) FROM signals WHERE source=? AND date=?',
        (SOURCE, file_date)
    ).fetchone()[0]

if existing > 0:
    print(f'AI Analyst signals for {file_date} already imported ({existing} records). Skipping.')
    sys.exit(0)

# Load analysis
with open(latest_file) as f:
    data = json.load(f)

if not isinstance(data, list):
    print('Unexpected format, skipping.')
    sys.exit(0)

# Get current state from DB
with sqlite3.connect(DB_PATH) as conn:
    # Get latest cash and holdings
    latest_equity = conn.execute(
        'SELECT cash, total_cost FROM equity_curve WHERE source=? ORDER BY date DESC LIMIT 1',
        (SOURCE,)
    ).fetchone()
    
    if latest_equity:
        cash = latest_equity[0]
        total_cost = latest_equity[1]
    else:
        cash = INITIAL_CASH
        total_cost = INITIAL_CASH
    
    # Get current holdings
    holdings = {}
    rows = conn.execute(
        'SELECT ticker, shares, cost_price FROM holdings WHERE source=? AND date=(
            SELECT MAX(date) FROM holdings WHERE source=?
        )', (SOURCE, SOURCE)
    ).fetchall()
    for ticker, shares, cost_price in rows:
        if shares > 0:
            holdings[ticker] = {'shares': shares, 'total_cost': shares * cost_price}
    
    # Weekly deposit (Tuesday)
    from pandas import Timestamp
    day_ts = Timestamp(file_date)
    if day_ts.weekday() == 1:  # Tuesday
        cash += WEEKLY
        total_cost += WEEKLY
    
    # Process each stock
    import yfinance as yf
    import pandas as pd
    
    prices = yf.download(HAIYAN_STOCKS, start=file_date, end=datetime.now().strftime('%Y-%m-%d'), progress=False)
    if isinstance(prices.columns, pd.MultiIndex):
        prices = prices['Close']
    
    for stock in data:
        if not isinstance(stock, dict): continue
        ticker = stock.get('code', '')
        if ticker not in HAIYAN_STOCKS: continue
        
        ai = stock.get('ai_analysis', {})
        tech = stock.get('technical_indicators', {})
        advice = ai.get('operation_advice', '')
        buy_signal = tech.get('buy_signal', '')
        
        price = stock.get('current_price') or tech.get('current_price', 0)
        if not price:
            try:
                price = float(prices.loc[file_date, ticker])
            except:
                continue
        if not price: continue
        
        # Determine action
        action = None
        if buy_signal:
            if '买入' in buy_signal or '加仓' in buy_signal: action = 'buy'
            elif '卖出' in buy_signal: action = 'sell'
            elif '持有' in buy_signal: action = 'hold'
        if not action:
            if any(k in advice for k in ['买入', '强烈买入', '加仓']): action = 'buy'
            elif any(k in advice for k in ['卖出', '减仓', '清仓']): action = 'sell'
            elif '观望' in advice or '持有' in advice: action = 'hold'
        
        if not action or action == 'hold': continue
        
        reason = ai.get('reason', '') or ai.get('analysis_summary', '') or f'Score: {tech.get(\"signal_score\", 0)}'
        reason = reason[:200]
        
        if action == 'buy' and cash > 0:
            buy_amount = cash * 0.30
            shares = buy_amount / price
            if ticker not in holdings:
                holdings[ticker] = {'shares': 0, 'total_cost': 0}
            holdings[ticker]['shares'] += shares
            holdings[ticker]['total_cost'] += buy_amount
            cash -= buy_amount
            conn.execute('INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                (f'ai_analyst_{file_date}_{ticker}_buy', file_date, SOURCE,
                 'llm_analysis', 'buy', ticker, price, shares, buy_amount, cash, reason))
        elif action == 'sell' and ticker in holdings and holdings[ticker]['shares'] > 0:
            shares = holdings[ticker]['shares']
            amount = shares * price
            cash += amount
            conn.execute('INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                (f'ai_analyst_{file_date}_{ticker}_sell', file_date, SOURCE,
                 'llm_analysis', 'sell', ticker, price, shares, amount, cash, reason))
            holdings[ticker] = {'shares': 0, 'total_cost': 0}
    
    # Update equity curve for today
    import yfinance as yf
    all_tickers = list(holdings.keys())
    positions_value = 0
    today = datetime.now().strftime('%Y-%m-%d')
    
    for ticker, h in holdings.items():
        if h['shares'] <= 0: continue
        try:
            t = yf.Ticker(ticker)
            current_price = t.fast_info.get('last_price', 0)
            if current_price:
                value = h['shares'] * current_price
                positions_value += value
                pl = value - h['total_cost']
                ret = pl / h['total_cost'] if h['total_cost'] > 0 else 0
                conn.execute('INSERT OR REPLACE INTO holdings VALUES (?,?,?,?,?,?,?,?,?)',
                    (today, SOURCE, ticker, h['shares'],
                     h['total_cost']/h['shares'] if h['shares']>0 else 0,
                     current_price, value, pl, ret))
        except Exception as e:
            print(f'Error getting price for {ticker}: {e}')
    
    total_value = cash + positions_value
    ret_pct = (total_value - total_cost) / total_cost if total_cost > 0 else 0
    conn.execute('INSERT OR REPLACE INTO equity_curve VALUES (?,?,?,?,?,?,?)',
        (today, SOURCE, total_value, cash, positions_value, total_cost, ret_pct))
    
    print(f'AI Analyst: imported {file_date} signals')

" 2>> "$LOG_FILE" || echo "$(date): AI Analyst import FAILED" >> "$LOG_FILE"

# ── Step 3: Export JSON ──
echo "$(date): Exporting JSON..." >> "$LOG_FILE"
python export_json.py 2>> "$LOG_FILE" || echo "$(date): Export FAILED" >> "$LOG_FILE"

# ── Step 4: Git push ──
echo "$(date): Pushing to GitHub..." >> "$LOG_FILE"
cd "$ARENA_DIR"
git add -A 2>> "$LOG_FILE"
git commit -m "data: daily update $(date +%Y-%m-%d)" 2>> "$LOG_FILE" || echo "$(date): No changes to commit" >> "$LOG_FILE"
git push origin main 2>> "$LOG_FILE" || echo "$(date): Git push FAILED" >> "$LOG_FILE"

echo "$(date): === Daily Update Complete ===" >> "$LOG_FILE"
