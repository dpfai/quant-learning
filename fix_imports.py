"""Fix: re-import ETF + AI Analyst with corrected parsing."""
import json, sqlite3, re
from datetime import datetime, timedelta
from pathlib import Path
import yfinance as yf
import pandas as pd

DB_PATH = Path("~/AI-workplace/quant-learning/data/trading_arena.db").expanduser()
ETF_FILE = Path("~/.openclaw/workspace-explorer/investments/portfolio_data/portfolio_tracking.json").expanduser()
HAIYAN_DIR = Path("~/.openclaw/workspace-explorer/investments").expanduser()
START_DATE = "2026-06-15"
INITIAL_CASH = 10000.0
WEEKLY = 500.0
DCA_DAY = 1  # Tuesday

HAIYAN_STOCKS = ["META", "GOOGL", "AMZN", "NFLX", "RKLB", "ACHR", "JOBY"]
ETF_CONFIGS = {
    "etf_aggressive": {"VOO": 0.425, "VGT": 0.425, "SMH": 0.15},
    "etf_balanced":   {"VOO": 0.50, "VGT": 0.40, "SMH": 0.10},
    "etf_conservative":{"VOO": 0.60, "VGT": 0.35, "SMH": 0.05},
}
ETF_MAP = {"组合A-激进型": "etf_aggressive", "组合B-平衡型": "etf_balanced", "组合C-稳健型": "etf_conservative"}

def get_price_on(prices, ticker, date_str):
    try:
        ts = pd.Timestamp(date_str)
        if ts in prices.index and ticker in prices.columns:
            v = prices.loc[ts, ticker]
            if not pd.isna(v): return float(v)
        mask = prices.index <= ts
        if mask.any() and ticker in prices.columns:
            v = prices.loc[mask, ticker].iloc[-1]
            if not pd.isna(v): return float(v)
        mask = prices.index >= ts
        if mask.any() and ticker in prices.columns:
            v = prices.loc[mask, ticker].iloc[0]
            if not pd.isna(v): return float(v)
    except: pass
    return None

def import_etfs(conn, prices):
    with open(ETF_FILE) as f:
        raw = json.load(f)
    portfolios = raw.get("portfolios", raw)
    
    for cn_name, source in ETF_MAP.items():
        if cn_name not in portfolios: continue
        conn.execute("DELETE FROM signals WHERE source=?", (source,))
        conn.execute("DELETE FROM equity_curve WHERE source=?", (source,))
        conn.execute("DELETE FROM holdings WHERE source=?", (source,))
        
        p = portfolios[cn_name]
        alloc = ETF_CONFIGS[source]
        holdings = {}
        cash = INITIAL_CASH
        total_cost = INITIAL_CASH
        
        # Use actual transactions from the tracking file
        for tx in p.get("transactions", []):
            d = tx["date"]
            ticker = tx["etf"]
            price = tx["price"]
            shares = tx["shares"]
            amount = tx["amount"]
            tx_type = tx["type"]
            
            if "initial" in tx_type:
                cash -= amount
            elif "weekly" in tx_type:
                cash += WEEKLY
                cash -= amount
                total_cost += WEEKLY
            
            if ticker not in holdings:
                holdings[ticker] = {"shares": 0, "total_cost": 0}
            holdings[ticker]["shares"] += shares
            holdings[ticker]["total_cost"] += amount
            
            conn.execute("INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (f"{source}_{d}_{ticker}_buy", d, source, "dca", "buy", ticker,
                 price, shares, amount, cash, f"DCA {'initial' if 'initial' in tx_type else 'weekly'} {alloc[ticker]*100:.1f}%"))
        
        # Record equity and holdings for each trading day
        for day in prices.index:
            if day < pd.Timestamp(START_DATE): continue
            day_str = day.strftime("%Y-%m-%d")
            pv = 0
            for ticker, h in holdings.items():
                if h["shares"] <= 0: continue
                if ticker in prices.columns and not pd.isna(prices.loc[day, ticker]):
                    price = float(prices.loc[day, ticker])
                    val = h["shares"] * price
                    pv += val
                    pl = val - h["total_cost"]
                    ret = pl / h["total_cost"] if h["total_cost"] > 0 else 0
                    conn.execute("INSERT OR REPLACE INTO holdings VALUES (?,?,?,?,?,?,?,?,?)",
                        (day_str, source, ticker, h["shares"],
                         h["total_cost"]/h["shares"] if h["shares"]>0 else 0,
                         price, val, pl, ret))
            tv = cash + pv
            rp = (tv - total_cost) / total_cost if total_cost > 0 else 0
            conn.execute("INSERT OR REPLACE INTO equity_curve VALUES (?,?,?,?,?,?,?)",
                (day_str, source, tv, cash, pv, total_cost, rp))
        print(f"  ETF {source}: done")

def import_haiyan(conn, prices):
    source = "ai_analyst"
    conn.execute("DELETE FROM signals WHERE source=?", (source,))
    conn.execute("DELETE FROM equity_curve WHERE source=?", (source,))
    conn.execute("DELETE FROM holdings WHERE source=?", (source,))
    
    # Download extra tickers
    extra = [t for t in HAIYAN_STOCKS if t not in prices.columns]
    if extra:
        e = yf.download(extra, start=START_DATE, end="2026-06-28", progress=False)
        if isinstance(e.columns, pd.MultiIndex): e = e["Close"]
        prices = prices.join(e, how="outer")
    
    cash = INITIAL_CASH
    total_cost = INITIAL_CASH
    holdings = {}
    
    # Parse analysis files - use filename for date if no date field
    files = sorted(HAIYAN_DIR.glob("stock_analysis_*.json"))
    for f in files:
        # Extract date from filename
        m = re.search(r'(\d{4}-\d{2}-\d{2})', f.name)
        file_date = m.group(1) if m else None
        if not file_date or file_date < START_DATE: continue
        
        with open(f) as fh:
            data = json.load(fh)
        if not isinstance(data, list): continue
        
        # Weekly deposit
        day_ts = pd.Timestamp(file_date)
        if day_ts.weekday() == DCA_DAY:
            cash += WEEKLY
            total_cost += WEEKLY
        
        for stock in data:
            if not isinstance(stock, dict): continue
            ticker = stock.get("code", "")
            if ticker not in HAIYAN_STOCKS: continue
            
            ai = stock.get("ai_analysis", {})
            tech = stock.get("technical_indicators", {})
            
            advice = ai.get("operation_advice", "")
            buy_signal = tech.get("buy_signal", "")
            score = tech.get("signal_score", 0)
            
            # Old format: current_price is top-level; new format: in tech
            price = stock.get("current_price") or tech.get("current_price", 0)
            if not price:
                price = get_price_on(prices, ticker, file_date)
            if not price: continue
            
            # Map to action
            action = None
            # Check buy_signal first (newer format)
            if buy_signal:
                if "买入" in buy_signal or "加仓" in buy_signal:
                    action = "buy"
                elif "卖出" in buy_signal:
                    action = "sell"
                elif "持有" in buy_signal:
                    action = "hold"
            # Fallback to operation_advice
            if not action:
                if any(k in advice for k in ["买入", "强烈买入", "加仓"]):
                    action = "buy"
                elif any(k in advice for k in ["卖出", "减仓", "清仓"]):
                    action = "sell"
                elif "观望" in advice or "持有" in advice:
                    action = "hold"
            
            if not action or action == "hold": continue
            
            reason = ai.get("reason", "") or ai.get("analysis_summary", "") or f"Score: {score}"
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
                    (f"ai_analyst_{file_date}_{ticker}_buy", file_date, source,
                     "llm_analysis", "buy", ticker, price, shares, buy_amount, cash, reason))
            elif action == "sell" and ticker in holdings and holdings[ticker]["shares"] > 0:
                shares = holdings[ticker]["shares"]
                amount = shares * price
                cash += amount
                conn.execute("INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (f"ai_analyst_{file_date}_{ticker}_sell", file_date, source,
                     "llm_analysis", "sell", ticker, price, shares, amount, cash, reason))
                holdings[ticker] = {"shares": 0, "total_cost": 0}
    
    # Record equity curve
    for day in prices.index:
        if day < pd.Timestamp(START_DATE): continue
        day_str = day.strftime("%Y-%m-%d")
        if day.weekday() == DCA_DAY:
            cash += WEEKLY
            total_cost += WEEKLY
        pv = 0
        for ticker, h in holdings.items():
            if h["shares"] <= 0: continue
            if ticker in prices.columns and not pd.isna(prices.loc[day, ticker]):
                price = float(prices.loc[day, ticker])
                val = h["shares"] * price
                pv += val
                pl = val - h["total_cost"]
                ret = pl / h["total_cost"] if h["total_cost"] > 0 else 0
                conn.execute("INSERT OR REPLACE INTO holdings VALUES (?,?,?,?,?,?,?,?,?)",
                    (day_str, source, ticker, h["shares"],
                     h["total_cost"]/h["shares"] if h["shares"]>0 else 0,
                     price, val, pl, ret))
        tv = cash + pv
        rp = (tv - total_cost) / total_cost if total_cost > 0 else 0
        conn.execute("INSERT OR REPLACE INTO equity_curve VALUES (?,?,?,?,?,?,?)",
            (day_str, source, tv, cash, pv, total_cost, rp))
    print(f"  AI Analyst: done")

def main():
    print("Re-importing ETF + AI Analyst...")
    all_tickers = ["SPY", "QQQ", "VOO", "VGT", "SMH"] + HAIYAN_STOCKS
    prices = yf.download(all_tickers, start=START_DATE, end="2026-06-28", progress=False)
    if isinstance(prices.columns, pd.MultiIndex): prices = prices["Close"]
    
    with sqlite3.connect(DB_PATH) as conn:
        import_etfs(conn, prices)
        import_haiyan(conn, prices)
    
    with sqlite3.connect(DB_PATH) as conn:
        for table in ["signals", "equity_curve", "holdings"]:
            rows = conn.execute(f"SELECT source, COUNT(*) FROM {table} GROUP BY source ORDER BY source").fetchall()
            print(f"\n  {table}:")
            for source, count in rows:
                print(f"    {source}: {count}")
    print("\nDone!")

if __name__ == "__main__":
    main()
