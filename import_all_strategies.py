"""
Import ETF portfolios, SPY benchmark, and AI Analyst (海岩) historical signals
into the unified trading_arena.db.
"""
import json
import sqlite3
import os
from datetime import date, datetime, timedelta
from pathlib import Path

import yfinance as yf
import pandas as pd

DB_PATH = Path("~/AI-workplace/quant-learning/data/trading_arena.db").expanduser()
ETF_TRACKING = Path("~/.openclaw/workspace-explorer/investments/portfolio_data/portfolio_tracking.json").expanduser()
HAIYAN_DIR = Path("~/.openclaw/workspace-explorer/investments").expanduser()
START_DATE = "2026-06-15"
INITIAL_CASH = 10000.0
WEEKLY_DEPOSIT = 500.0
DCA_DAY = 1  # Tuesday=1

SCHEMA = """
CREATE TABLE IF NOT EXISTS signals (
  id TEXT PRIMARY KEY, date TEXT NOT NULL, source TEXT NOT NULL,
  strategy TEXT NOT NULL, action TEXT NOT NULL, ticker TEXT NOT NULL,
  price REAL, shares REAL, amount REAL, cash_after REAL, reason TEXT
);
CREATE TABLE IF NOT EXISTS equity_curve (
  date TEXT NOT NULL, source TEXT NOT NULL,
  total_value REAL, cash REAL, positions_value REAL,
  total_cost REAL, return_pct REAL,
  PRIMARY KEY (date, source)
);
CREATE TABLE IF NOT EXISTS holdings (
  date TEXT NOT NULL, source TEXT NOT NULL, ticker TEXT NOT NULL,
  shares REAL, cost_price REAL, current_price REAL, value REAL,
  profit_loss REAL, return_pct REAL,
  PRIMARY KEY (date, source, ticker)
);
"""

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)

def clear_source(conn, source):
    for table in ["signals", "equity_curve", "holdings"]:
        conn.execute(f"DELETE FROM {table} WHERE source = ?", (source,))

def get_tuesday_deposits(start, end):
    """Get all Tuesday dates between start and end."""
    dates = []
    d = datetime.strptime(start, "%Y-%m-%d").date()
    end_d = datetime.strptime(end, "%Y-%m-%d").date()
    while d <= end_d:
        if d.weekday() == DCA_DAY:
            dates.append(d.isoformat())
        d += timedelta(days=1)
    return dates

def get_prices(tickers, start, end):
    """Download historical prices."""
    data = yf.download(tickers, start=start, end=end, progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        data = data["Close"]
    return data

# ─── ETF Portfolios ───
ETF_CONFIGS = {
    "etf_aggressive": {"name": "DCA Aggressive", "alloc": {"VOO": 0.425, "VGT": 0.425, "SMH": 0.15}},
    "etf_balanced":   {"name": "DCA Balanced",   "alloc": {"VOO": 0.50, "VGT": 0.40, "SMH": 0.10}},
    "etf_conservative":{"name": "DCA Conservative","alloc": {"VOO": 0.60, "VGT": 0.35, "SMH": 0.05}},
}

def import_etf(conn, prices_df):
    """Import ETF DCA portfolios from portfolio_tracking.json."""
    with open(ETF_TRACKING) as f:
        raw = json.load(f)

    mapping = {
        "组合A-激进型": "etf_aggressive",
        "组合B-平衡型": "etf_balanced",
        "组合C-稳健型": "etf_conservative",
    }

    for cn_name, source in mapping.items():
        if cn_name not in raw:
            continue
        clear_source(conn, source)
        portfolio = raw[cn_name]
        alloc = ETF_CONFIGS[source]["alloc"]

        # Build holdings and equity from transactions
        holdings = {}  # ticker -> {shares, total_cost}
        cash = INITIAL_CASH
        total_cost = INITIAL_CASH

        # Initial investment on 6/15
        init_date = "2026-06-15"
        for ticker, ratio in alloc.items():
            amount = INITIAL_CASH * ratio
            # Find closest price
            price = get_price_on(prices_df, ticker, init_date)
            if price is None:
                continue
            shares = amount / price
            holdings[ticker] = {"shares": shares, "total_cost": amount}
            cash -= amount
            conn.execute(
                "INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (f"{source}_{init_date}_{ticker}_buy", init_date, source, "dca",
                 "buy", ticker, price, shares, amount, cash,
                 f"Initial investment {ratio*100:.1f}% allocation")
            )

        # Weekly deposits on Tuesdays
        tuesdays = get_tuesday_deposits("2026-06-16", "2026-06-27")
        for tuesday in tuesdays:
            for ticker, ratio in alloc.items():
                amount = WEEKLY_DEPOSIT * ratio
                price = get_price_on(prices_df, ticker, tuesday)
                if price is None:
                    continue
                shares = amount / price
                holdings[ticker]["shares"] += shares
                holdings[ticker]["total_cost"] += amount
                cash += WEEKLY_DEPOSIT  # deposit comes in
                cash -= amount  # spent
                total_cost += WEEKLY_DEPOSIT
                conn.execute(
                    "INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (f"{source}_{tuesday}_{ticker}_buy", tuesday, source, "dca",
                     "buy", ticker, price, shares, amount, cash,
                     f"Weekly DCA {ratio*100:.1f}% allocation")
                )

        # Record equity curve and holdings for each trading day
        trading_days = [d for d in prices_df.index if d >= pd.Timestamp(START_DATE)]
        for day in trading_days:
            day_str = day.strftime("%Y-%m-%d")
            positions_value = 0
            for ticker, h in holdings.items():
                if ticker in prices_df.columns and not pd.isna(prices_df.loc[day, ticker]):
                    price = float(prices_df.loc[day, ticker])
                    value = h["shares"] * price
                    positions_value += value
                    pl = value - h["total_cost"]
                    ret = pl / h["total_cost"] if h["total_cost"] > 0 else 0
                    conn.execute(
                        "INSERT OR REPLACE INTO holdings VALUES (?,?,?,?,?,?,?,?,?)",
                        (day_str, source, ticker, h["shares"],
                         h["total_cost"] / h["shares"], price, value, pl, ret)
                    )
            total_value = cash + positions_value
            ret_pct = (total_value - total_cost) / total_cost if total_cost > 0 else 0
            conn.execute(
                "INSERT OR REPLACE INTO equity_curve VALUES (?,?,?,?,?,?,?)",
                (day_str, source, total_value, cash, positions_value, total_cost, ret_pct)
            )
        print(f"  ETF {source}: imported")

def get_price_on(prices_df, ticker, date_str):
    """Get price for ticker on a specific date, fallback to nearest."""
    try:
        ts = pd.Timestamp(date_str)
        if ts in prices_df.index and ticker in prices_df.columns:
            val = prices_df.loc[ts, ticker]
            if not pd.isna(val):
                return float(val)
        # Find nearest trading day
        mask = prices_df.index <= ts
        if mask.any():
            val = prices_df.loc[mask, ticker].iloc[-1]
            if not pd.isna(val):
                return float(val)
        mask = prices_df.index >= ts
        if mask.any():
            val = prices_df.loc[mask, ticker].iloc[0]
            if not pd.isna(val):
                return float(val)
    except Exception:
        pass
    return None

# ─── SPY Benchmark ───
def import_spy(conn, prices_df):
    """Import SPY buy-and-hold benchmark."""
    source = "spy"
    clear_source(conn, source)

    cash = INITIAL_CASH
    total_cost = INITIAL_CASH
    spy_shares = 0
    spy_cost = 0

    trading_days = [d for d in prices_df.index if d >= pd.Timestamp(START_DATE)]

    for i, day in enumerate(trading_days):
        day_str = day.strftime("%Y-%m-%d")
        price = float(prices_df.loc[day, "SPY"]) if "SPY" in prices_df.columns else None
        if price is None:
            continue

        # Initial buy on first day
        if i == 0:
            spy_shares = cash / price
            spy_cost = cash
            cash = 0
            conn.execute(
                "INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (f"spy_{day_str}_buy", day_str, source, "buy_hold",
                 "buy", "SPY", price, spy_shares, spy_cost, cash,
                 "Initial buy-and-hold")
            )

        # Weekly deposit on Tuesdays
        if day.weekday() == DCA_DAY and i > 0:
            shares = WEEKLY_DEPOSIT / price
            spy_shares += shares
            spy_cost += WEEKLY_DEPOSIT
            total_cost += WEEKLY_DEPOSIT
            conn.execute(
                "INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (f"spy_{day_str}_buy", day_str, source, "buy_hold",
                 "buy", "SPY", price, shares, WEEKLY_DEPOSIT, cash,
                 "Weekly deposit buy")
            )

        value = spy_shares * price
        total_value = cash + value
        pl = value - spy_cost
        ret = pl / spy_cost if spy_cost > 0 else 0
        conn.execute(
            "INSERT OR REPLACE INTO holdings VALUES (?,?,?,?,?,?,?,?,?)",
            (day_str, source, "SPY", spy_shares, spy_cost / spy_shares, price, value, pl, ret)
        )
        ret_pct = (total_value - total_cost) / total_cost if total_cost > 0 else 0
        conn.execute(
            "INSERT OR REPLACE INTO equity_curve VALUES (?,?,?,?,?,?,?)",
            (day_str, source, total_value, cash, value, total_cost, ret_pct)
        )
    print(f"  SPY benchmark: imported")

# ─── AI Analyst (海岩) ───
HAIYAN_STOCKS = ["META", "GOOGL", "AMZN", "NFLX", "RKLB", "ACHR", "JOBY"]

def import_haiyan(conn, prices_df):
    """Import AI Analyst signals from historical analysis JSONs."""
    source = "ai_analyst"
    clear_source(conn, source)

    # Find all historical analysis files
    analysis_files = sorted(HAIYAN_DIR.glob("stock_analysis_*.json"))
    # Also check the results file
    results_file = HAIYAN_DIR.parent / "stock_analysis_results.json"
    if results_file.exists():
        analysis_files.insert(0, results_file)

    # Download prices for haiyan stocks if not in prices_df
    haiyan_tickers = [t for t in HAIYAN_STOCKS if t not in prices_df.columns]
    if haiyan_tickers:
        extra = yf.download(haiyan_tickers, start=START_DATE, end="2026-06-28", progress=False)
        if isinstance(extra.columns, pd.MultiIndex):
            extra = extra["Close"]
        prices_df = prices_df.join(extra, how="outer")

    cash = INITIAL_CASH
    total_cost = INITIAL_CASH
    holdings = {}  # ticker -> {shares, total_cost}

    # Track all analysis dates
    all_analyses = []

    for f in analysis_files:
        try:
            with open(f) as fh:
                data = json.load(fh)
            if isinstance(data, list):
                for item in data:
                    all_analyses.append(item)
        except Exception as e:
            print(f"  Warning: could not parse {f}: {e}")

    # Sort by date
    all_analyses.sort(key=lambda x: x.get("date", ""))

    # Process each analysis day
    processed_dates = set()
    for item in all_analyses:
        analysis_date = item.get("date", "")
        if not analysis_date or analysis_date < START_DATE:
            continue
        if analysis_date in processed_dates:
            continue
        processed_dates.add(analysis_date)

        # Weekly deposit on Tuesdays
        day_ts = pd.Timestamp(analysis_date)
        if day_ts.weekday() == DCA_DAY:
            cash += WEEKLY_DEPOSIT
            total_cost += WEEKLY_DEPOSIT

        # Process each stock in the analysis
        stocks = item.get("stocks", item) if isinstance(item, dict) else item
        if isinstance(item, list):
            stocks = item

        for stock in stocks if isinstance(stocks, list) else [stocks]:
            if not isinstance(stock, dict):
                continue
            ticker = stock.get("code", "")
            if ticker not in HAIYAN_STOCKS:
                continue

            # Get analysis recommendation
            ai = stock.get("ai_analysis", {})
            tech = stock.get("technical_indicators", {})

            advice = ai.get("operation_advice", "")
            buy_signal = tech.get("buy_signal", "")
            score = tech.get("signal_score", 0)
            price = tech.get("current_price", 0)
            target = ai.get("target_price", "")
            stop_loss = ai.get("stop_loss", "")
            confidence = ai.get("confidence_level", "")

            # Map Chinese advice to action
            action = None
            if any(k in advice for k in ["买入", "强烈买入", "加仓"]):
                action = "buy"
            elif any(k in advice for k in ["卖出", "减仓", "清仓"]):
                action = "sell"
            elif any(k in buy_signal for k in ["买入", "加仓"]):
                action = "buy"
            elif any(k in buy_signal for k in ["卖出"]):
                action = "sell"
            elif "持有" in buy_signal or "观望" in advice:
                action = "hold"

            if action is None or action == "hold":
                continue

            # Get price
            if not price or price == 0:
                price = get_price_on(prices_df, ticker, analysis_date)
            if not price:
                continue

            reason_parts = []
            if ai.get("analysis_summary"):
                reason_parts.append(ai["analysis_summary"][:100])
            if tech.get("signal_reasons"):
                reason_parts.append("; ".join(tech["signal_reasons"][:2]))
            reason = " | ".join(reason_parts)[:200] if reason_parts else f"Score: {score}"

            if action == "buy" and cash > 0:
                # Use 30% of cash per buy (conservative)
                buy_amount = min(cash * 0.30, cash)
                shares = buy_amount / price
                if ticker not in holdings:
                    holdings[ticker] = {"shares": 0, "total_cost": 0}
                holdings[ticker]["shares"] += shares
                holdings[ticker]["total_cost"] += buy_amount
                cash -= buy_amount
                conn.execute(
                    "INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (f"ai_analyst_{analysis_date}_{ticker}_buy", analysis_date, source,
                     "llm_analysis", "buy", ticker, price, shares, buy_amount, cash, reason)
                )
            elif action == "sell" and ticker in holdings and holdings[ticker]["shares"] > 0:
                shares = holdings[ticker]["shares"]
                amount = shares * price
                cash += amount
                conn.execute(
                    "INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (f"ai_analyst_{analysis_date}_{ticker}_sell", analysis_date, source,
                     "llm_analysis", "sell", ticker, price, shares, amount, cash, reason)
                )
                holdings[ticker] = {"shares": 0, "total_cost": 0}

    # Record equity curve and holdings for each trading day
    trading_days = [d for d in prices_df.index if d >= pd.Timestamp(START_DATE)]
    for day in trading_days:
        day_str = day.strftime("%Y-%m-%d")

        # Weekly deposit
        if day.weekday() == DCA_DAY:
            cash += WEEKLY_DEPOSIT
            total_cost += WEEKLY_DEPOSIT

        positions_value = 0
        for ticker, h in holdings.items():
            if h["shares"] <= 0:
                continue
            if ticker in prices_df.columns and not pd.isna(prices_df.loc[day, ticker]):
                price = float(prices_df.loc[day, ticker])
                value = h["shares"] * price
                positions_value += value
                pl = value - h["total_cost"]
                ret = pl / h["total_cost"] if h["total_cost"] > 0 else 0
                conn.execute(
                    "INSERT OR REPLACE INTO holdings VALUES (?,?,?,?,?,?,?,?,?)",
                    (day_str, source, ticker, h["shares"],
                     h["total_cost"] / h["shares"] if h["shares"] > 0 else 0,
                     price, value, pl, ret)
                )
        total_value = cash + positions_value
        ret_pct = (total_value - total_cost) / total_cost if total_cost > 0 else 0
        conn.execute(
            "INSERT OR REPLACE INTO equity_curve VALUES (?,?,?,?,?,?,?)",
            (day_str, source, total_value, cash, positions_value, total_cost, ret_pct)
        )
    print(f"  AI Analyst: imported {len(processed_dates)} analysis days")

# ─── Main ───
def main():
    print("Importing all strategies into trading_arena.db...")
    init_db()

    all_tickers = ["SPY", "QQQ", "VOO", "VGT", "SMH"] + HAIYAN_STOCKS
    print(f"  Downloading prices for {all_tickers}...")
    prices_df = get_prices(all_tickers, START_DATE, "2026-06-28")

    with sqlite3.connect(DB_PATH) as conn:
        import_etf(conn, prices_df)
        import_spy(conn, prices_df)
        import_haiyan(conn, prices_df)

    # Count results
    with sqlite3.connect(DB_PATH) as conn:
        for table in ["signals", "equity_curve", "holdings"]:
            rows = conn.execute(f"SELECT source, COUNT(*) FROM {table} GROUP BY source").fetchall()
            print(f"\n  {table}:")
            for source, count in rows:
                print(f"    {source}: {count}")

    print("\nDone! Run export_json.py to update website data.")

if __name__ == "__main__":
    main()
