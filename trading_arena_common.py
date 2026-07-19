"""Shared helpers for exporting Quant Learning data to AI Trading Arena."""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable

import numpy as np
import pandas as pd


DB_PATH = Path("data/trading_arena.db")
ARENA_DATA_DIR = Path("~/AI-workplace/ai-trading-arena/data").expanduser()
TRADE_TICKERS = ["SPY", "QQQ", "VOO", "VGT", "SMH"]
SOURCE_NAME = "quant_learning"
INITIAL_CASH = 10_000.0
WEEKLY_CONTRIBUTION = 500.0
BACKFILL_START = date(2026, 6, 15)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS signals (
  id TEXT PRIMARY KEY,
  date TEXT NOT NULL,
  source TEXT NOT NULL,
  strategy TEXT NOT NULL,
  action TEXT NOT NULL,
  ticker TEXT NOT NULL,
  price REAL,
  shares REAL,
  amount REAL,
  cash_after REAL,
  reason TEXT
);

CREATE TABLE IF NOT EXISTS equity_curve (
  date TEXT NOT NULL,
  source TEXT NOT NULL,
  total_value REAL,
  cash REAL,
  positions_value REAL,
  total_cost REAL,
  return_pct REAL,
  PRIMARY KEY (date, source)
);

CREATE TABLE IF NOT EXISTS holdings (
  date TEXT NOT NULL,
  source TEXT NOT NULL,
  ticker TEXT NOT NULL,
  shares REAL,
  cost_price REAL,
  current_price REAL,
  value REAL,
  profit_loss REAL,
  return_pct REAL,
  PRIMARY KEY (date, source, ticker)
);
"""


@dataclass
class Position:
    shares: float = 0.0
    total_cost: float = 0.0

    @property
    def cost_price(self) -> float:
        if self.shares <= 0:
            return 0.0
        return self.total_cost / self.shares


def initialize_database(db_path: Path = DB_PATH) -> None:
    """Create the SQLite database and required tables if needed."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)


def clear_source_data(source: str = SOURCE_NAME, db_path: Path = DB_PATH) -> None:
    """Remove generated rows for one source before a deterministic backfill."""
    initialize_database(db_path)
    with sqlite3.connect(db_path) as conn:
        for table in ["signals", "equity_curve", "holdings"]:
            conn.execute(f"DELETE FROM {table} WHERE source = ?", (source,))


def normalize_ohlcv(data: pd.DataFrame) -> pd.DataFrame:
    """Return a standard OHLCV frame from yfinance output."""
    if data.empty:
        return data
    if isinstance(data.columns, pd.MultiIndex):
        ohlcv_names = {"Open", "High", "Low", "Close", "Adj Close", "Volume"}
        level_zero = data.columns.get_level_values(0)
        level_last = data.columns.get_level_values(-1)
        if set(level_zero).intersection(ohlcv_names):
            data.columns = level_zero
        elif set(level_last).intersection(ohlcv_names):
            data.columns = level_last
        else:
            data.columns = level_zero
    normalized = data.copy()
    normalized.index = pd.to_datetime(normalized.index).tz_localize(None).normalize()
    if "Adj Close" in normalized.columns and "Close" not in normalized.columns:
        normalized["Close"] = normalized["Adj Close"]
    columns = ["Open", "High", "Low", "Close", "Volume"]
    return normalized[[col for col in columns if col in normalized.columns]].dropna()


def download_history(
    tickers: Iterable[str],
    start: date,
    end: date,
    warmup_days: int = 420,
) -> Dict[str, pd.DataFrame]:
    """Download daily OHLCV data with enough warmup for indicators and ML."""
    import yfinance as yf

    download_start = start - timedelta(days=warmup_days)
    download_end = end + timedelta(days=1)
    results: Dict[str, pd.DataFrame] = {}
    for ticker in tickers:
        raw = yf.download(
            ticker,
            start=download_start.isoformat(),
            end=download_end.isoformat(),
            auto_adjust=False,
            progress=False,
            group_by="column",
        )
        frame = normalize_ohlcv(raw)
        if frame.empty:
            raise RuntimeError(f"No yfinance data returned for {ticker}")
        results[ticker] = frame
    return results


def ml_vote_series(df: pd.DataFrame, prediction_start: date) -> pd.Series:
    """Train a pre-period classifier and convert predictions to bull/bear votes."""
    from ml.features import create_price_features, create_technical_features, prepare_ml_data
    from ml.models import get_model

    neutral = pd.Series(0.0, index=df.index)
    training_data = df.loc[df.index.date < prediction_start]
    if len(training_data) < 140:
        return neutral
    try:
        X_train, _, y_train, _ = prepare_ml_data(training_data, forward_days=5, test_ratio=0.2)
        model = get_model("random_forest")
        model.fit(X_train, y_train)
        features = pd.concat(
            [create_price_features(df), create_technical_features(df)],
            axis=1,
        ).replace([np.inf, -np.inf], np.nan).dropna()
        if features.empty:
            return neutral
        predictions = pd.Series(model.predict(features), index=features.index)
        neutral.loc[predictions.index] = np.where(predictions > 0, 1.0, -1.0)
        return neutral
    except ValueError:
        return neutral


def build_strategy_votes(df: pd.DataFrame, prediction_start: date) -> pd.DataFrame:
    """Create the four sub-strategy vote columns used by the arena portfolio."""
    from backtest.strategies import (
        bollinger_band_signal,
        ma_crossover_signal,
        rsi_mean_reversion_signal,
    )

    votes = pd.DataFrame(index=df.index)
    votes["ma20_50"] = ma_crossover_signal(df, fast_period=20, slow_period=50)
    votes["rsi_30_70"] = rsi_mean_reversion_signal(df, oversold=30, overbought=70)
    votes["bollinger_2std"] = bollinger_band_signal(df, period=20, std_dev=2)
    votes["ml_direction"] = ml_vote_series(df, prediction_start)
    return votes.fillna(0.0)


def decide_trade(votes: pd.Series) -> tuple[str, float]:
    """Translate four votes into the requested composite action."""
    bullish = int((votes > 0).sum())
    bearish = int((votes < 0).sum())
    if bullish >= 3:
        return "buy", 0.50
    if bullish == 2:
        return "buy", 0.25
    if bearish >= 3:
        return "sell", 1.00
    if bearish == 2:
        return "sell", 0.50
    return "hold", 0.0


def signal_id(trade_date: pd.Timestamp, ticker: str, action: str) -> str:
    """Create the Trading Arena signal ID format."""
    return f"ql_{trade_date.strftime('%Y%m%d')}_{ticker}_{action}"


def record_signal(
    conn: sqlite3.Connection,
    trade_date: pd.Timestamp,
    action: str,
    ticker: str,
    price: float,
    shares: float,
    amount: float,
    cash_after: float,
    reason: str,
) -> None:
    """Insert or replace an executed simulated trade signal."""
    conn.execute(
        """
        INSERT OR REPLACE INTO signals (
            id, date, source, strategy, action, ticker, price, shares,
            amount, cash_after, reason
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            signal_id(trade_date, ticker, action),
            trade_date.strftime("%Y-%m-%d"),
            SOURCE_NAME,
            "four_vote_composite",
            action,
            ticker,
            price,
            shares,
            amount,
            cash_after,
            reason,
        ),
    )


def record_equity_and_holdings(
    conn: sqlite3.Connection,
    trade_date: pd.Timestamp,
    cash: float,
    positions: Dict[str, Position],
    prices: Dict[str, float],
) -> None:
    """Persist daily portfolio value and current holdings."""
    positions_value = 0.0
    total_cost = 0.0
    for ticker, position in positions.items():
        price = prices.get(ticker)
        if position.shares <= 0 or price is None or np.isnan(price):
            continue
        value = position.shares * price
        profit_loss = value - position.total_cost
        return_pct = profit_loss / position.total_cost if position.total_cost else 0.0
        positions_value += value
        total_cost += position.total_cost
        conn.execute(
            """
            INSERT OR REPLACE INTO holdings (
                date, source, ticker, shares, cost_price, current_price,
                value, profit_loss, return_pct
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                trade_date.strftime("%Y-%m-%d"),
                SOURCE_NAME,
                ticker,
                position.shares,
                position.cost_price,
                price,
                value,
                profit_loss,
                return_pct,
            ),
        )

    total_value = cash + positions_value
    return_pct = total_value / INITIAL_CASH - 1
    conn.execute(
        """
        INSERT OR REPLACE INTO equity_curve (
            date, source, total_value, cash, positions_value, total_cost, return_pct
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            trade_date.strftime("%Y-%m-%d"),
            SOURCE_NAME,
            total_value,
            cash,
            positions_value,
            total_cost,
            return_pct,
        ),
    )


def simulate_portfolio(
    history: Dict[str, pd.DataFrame],
    start: date,
    end: date,
    db_path: Path = DB_PATH,
    reset_source: bool = True,
) -> None:
    """Run the four-vote strategy and write signals, equity, and holdings."""
    if reset_source:
        clear_source_data(SOURCE_NAME, db_path)
    else:
        initialize_database(db_path)

    votes_by_ticker = {
        ticker: build_strategy_votes(frame, start)
        for ticker, frame in history.items()
    }
    trading_days = sorted(
        {
            idx
            for frame in history.values()
            for idx in frame.loc[
                (frame.index.date >= start) & (frame.index.date <= end)
            ].index
        }
    )
    cash = INITIAL_CASH
    positions = {ticker: Position() for ticker in history}

    with sqlite3.connect(db_path) as conn:
        for trade_date in trading_days:
            if trade_date.weekday() == 1:
                cash += WEEKLY_CONTRIBUTION

            prices = {
                ticker: float(frame.loc[trade_date, "Close"])
                for ticker, frame in history.items()
                if trade_date in frame.index
            }
            for ticker in TRADE_TICKERS:
                if ticker not in prices or ticker not in votes_by_ticker:
                    continue
                votes = votes_by_ticker[ticker].loc[trade_date]
                action, fraction = decide_trade(votes)
                price = prices[ticker]
                bullish = int((votes > 0).sum())
                bearish = int((votes < 0).sum())
                reason = (
                    f"votes bull={bullish} bear={bearish}; "
                    f"{votes.astype(int).to_dict()}"
                )

                if action == "buy" and cash > 0:
                    amount = min(cash, cash * fraction)
                    if amount <= 0:
                        continue
                    shares = amount / price
                    positions[ticker].shares += shares
                    positions[ticker].total_cost += amount
                    cash -= amount
                    record_signal(
                        conn, trade_date, action, ticker, price, shares,
                        amount, cash, reason,
                    )
                elif action == "sell" and positions[ticker].shares > 0:
                    shares = positions[ticker].shares * fraction
                    amount = shares * price
                    cost_reduction = positions[ticker].cost_price * shares
                    positions[ticker].shares -= shares
                    positions[ticker].total_cost -= cost_reduction
                    if positions[ticker].shares < 1e-10:
                        positions[ticker] = Position()
                    cash += amount
                    record_signal(
                        conn, trade_date, action, ticker, price, shares,
                        amount, cash, reason,
                    )

            record_equity_and_holdings(conn, trade_date, cash, positions, prices)


def table_to_records(db_path: Path, table: str) -> list[dict]:
    """Read one DB table as JSON-ready records."""
    with sqlite3.connect(db_path) as conn:
        frame = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    if "date" in frame.columns:
        frame = frame.sort_values("date")
    return frame.to_dict(orient="records")


def write_json(path: Path, records: object) -> None:
    """Write pretty JSON with deterministic key order where possible."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")


def latest_market_date(db_path: Path = DB_PATH) -> str | None:
    """Return the newest equity date already stored."""
    initialize_database(db_path)
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT MAX(date) FROM equity_curve WHERE source = ?",
            (SOURCE_NAME,),
        ).fetchone()
    return row[0] if row else None


def parse_date(value: str | None, default: date) -> date:
    """Parse an ISO date argument."""
    if not value:
        return default
    return datetime.strptime(value, "%Y-%m-%d").date()
