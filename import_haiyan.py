"""
Import AI Analyst (海岩) signals from latest stock_analysis JSON into trading_arena.db.
Runs after weekly_stock_analysis.py produces new output.
"""
import json, sqlite3, re, sys
from pathlib import Path
from datetime import datetime
import yfinance as yf
import pandas as pd

DB_PATH = Path(__file__).parent / "data" / "trading_arena.db"
HAIYAN_DIR = Path.home() / ".openclaw" / "workspace-explorer" / "investments"
SOURCE = "ai_analyst"
INITIAL_CASH = 10000.0
WEEKLY = 500.0
START = "2026-06-15"

def main():
    # Find latest analysis file
    files = sorted(HAIYAN_DIR.glob("stock_analysis_*.json"))
    if not files:
        print("No analysis files found, skipping.")
        return
    
    latest_file = files[-1]
    m = re.search(r'(\d{4}-\d{2}-\d{2})', latest_file.name)
    file_date = m.group(1) if m else datetime.now().strftime('%Y-%m-%d')
    
    # Check if already imported
    with sqlite3.connect(DB_PATH) as conn:
        existing = conn.execute(
            'SELECT COUNT(*) FROM signals WHERE source=? AND date=?', (SOURCE, file_date)
        ).fetchone()[0]
    
    if existing > 0:
        print(f"AI Analyst signals for {file_date} already imported ({existing} records). Skipping.")
        return
    
    with open(latest_file) as f:
        data = json.load(f)
    if not isinstance(data, list):
        print("Unexpected format, skipping.")
        return
    
    # Collect all tickers
    all_tickers = sorted(set(s.get("code") for s in data if isinstance(s, dict) and s.get("code")))
    print(f"Found {len(all_tickers)} tickers in {latest_file.name}")
    
    # Download prices
    prices = yf.download(all_tickers, start=file_date, end=datetime.now().strftime('%Y-%m-%d'), progress=False)
    if isinstance(prices.columns, pd.MultiIndex):
        prices = prices["Close"]
    
    with sqlite3.connect(DB_PATH) as conn:
        # Get current state
        latest_equity = conn.execute(
            'SELECT cash, total_cost FROM equity_curve WHERE source=? ORDER BY date DESC LIMIT 1', (SOURCE,)
        ).fetchone()
        cash = latest_equity[0] if latest_equity else INITIAL_CASH
        total_cost = latest_equity[1] if latest_equity else INITIAL_CASH
        
        # Get current holdings
        holdings = {}
        rows = conn.execute(
            'SELECT ticker, shares FROM holdings WHERE source=? AND date=(SELECT MAX(date) FROM holdings WHERE source=?)',
            (SOURCE, SOURCE)
        ).fetchall()
        for ticker, shares in rows:
            if shares > 0:
                # Get cost from latest
                cost_row = conn.execute(
                    'SELECT cost_price FROM holdings WHERE source=? AND ticker=? AND date=(SELECT MAX(date) FROM holdings WHERE source=? AND ticker=?)',
                    (SOURCE, ticker, SOURCE, ticker)
                ).fetchone()
                cp = cost_row[0] if cost_row else 0
                holdings[ticker] = {"shares": shares, "total_cost": shares * cp}
        
        # Weekly deposit (Tuesday)
        day_ts = pd.Timestamp(file_date)
        if day_ts.weekday() == 1:
            cash += WEEKLY
            total_cost += WEEKLY
        
        # Process signals
        buy_count = 0
        sell_count = 0
        for stock in data:
            if not isinstance(stock, dict): continue
            ticker = stock.get("code", "")
            ai = stock.get("ai_analysis", {})
            tech = stock.get("technical_indicators", {})
            advice = ai.get("operation_advice", "")
            buy_signal = tech.get("buy_signal", "")
            
            price = stock.get("current_price") or tech.get("current_price", 0)
            if not price:
                try: price = float(prices.loc[file_date, ticker])
                except: continue
            if not price or price == 0: continue
            
            # Determine action
            action = None
            if buy_signal:
                if "买入" in buy_signal or "加仓" in buy_signal: action = "buy"
                elif "卖出" in buy_signal: action = "sell"
                elif "持有" in buy_signal: action = "hold"
            if not action:
                if any(k in advice for k in ["买入", "强烈买入", "加仓"]): action = "buy"
                elif any(k in advice for k in ["卖出", "减仓", "清仓"]): action = "sell"
                elif "观望" in advice or "持有" in advice: action = "hold"
            
            if not action or action == "hold": continue
            
            reason = ai.get("reason", "") or ai.get("analysis_summary", "") or f"Score: {tech.get('signal_score', 0)}"
            reason = reason[:200]
            
            if action == "buy" and cash > 0:
                buy_amount = cash * 0.30
                shares = buy_amount / price
                if ticker not in holdings:
                    holdings[ticker] = {"shares": 0, "total_cost": 0}
                holdings[ticker]["shares"] += shares
                holdings[ticker]["total_cost"] += buy_amount
                cash -= buy_amount
                conn.execute("INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (f"ai_analyst_{file_date}_{ticker}_buy", file_date, SOURCE,
                     "llm_analysis", "buy", ticker, price, shares, buy_amount, cash, reason))
                buy_count += 1
                print(f"  BUY {ticker} @ ${price:.2f} x{shares:.4f} = ${buy_amount:.2f}")
            elif action == "sell" and ticker in holdings and holdings[ticker]["shares"] > 0:
                shares = holdings[ticker]["shares"]
                amount = shares * price
                cash += amount
                conn.execute("INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (f"ai_analyst_{file_date}_{ticker}_sell", file_date, SOURCE,
                     "llm_analysis", "sell", ticker, price, shares, amount, cash, reason))
                holdings[ticker] = {"shares": 0, "total_cost": 0}
                sell_count += 1
                print(f"  SELL {ticker} @ ${price:.2f} x{shares:.4f} = ${amount:.2f}")
        
        # Update equity curve for today
        today = datetime.now().strftime('%Y-%m-%d')
        positions_value = 0
        for ticker, h in holdings.items():
            if h["shares"] <= 0: continue
            try:
                t = yf.Ticker(ticker)
                current_price = t.fast_info.get("last_price", 0)
                if current_price:
                    value = h["shares"] * current_price
                    positions_value += value
                    pl = value - h["total_cost"]
                    ret = pl / h["total_cost"] if h["total_cost"] > 0 else 0
                    conn.execute("INSERT OR REPLACE INTO holdings VALUES (?,?,?,?,?,?,?,?,?)",
                        (today, SOURCE, ticker, h["shares"],
                         h["total_cost"]/h["shares"] if h["shares"]>0 else 0,
                         current_price, value, pl, ret))
            except Exception as e:
                print(f"  Warning: could not get price for {ticker}: {e}")
        
        total_value = cash + positions_value
        ret_pct = (total_value - total_cost) / total_cost if total_cost > 0 else 0
        conn.execute("INSERT OR REPLACE INTO equity_curve VALUES (?,?,?,?,?,?,?)",
            (today, SOURCE, total_value, cash, positions_value, total_cost, ret_pct))
        
        print(f"\nImported: {buy_count} buys, {sell_count} sells for {file_date}")

if __name__ == "__main__":
    main()
