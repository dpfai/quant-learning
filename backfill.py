"""Backfill Quant Learning data into data/trading_arena.db."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from trading_arena_common import (
    BACKFILL_START,
    DB_PATH,
    TRADE_TICKERS,
    download_history,
    initialize_database,
    parse_date,
    simulate_portfolio,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill Trading Arena SQLite data.")
    parser.add_argument("--start", default=BACKFILL_START.isoformat())
    parser.add_argument("--end", default=date.today().isoformat())
    parser.add_argument("--db", default=str(DB_PATH))
    args = parser.parse_args()

    start = parse_date(args.start, BACKFILL_START)
    end = parse_date(args.end, date.today())
    db_path = Path(args.db)

    initialize_database(db_path)
    history = download_history(TRADE_TICKERS, start=start, end=end)
    simulate_portfolio(history, start=start, end=end, db_path=db_path, reset_source=True)
    print(f"Backfilled {len(TRADE_TICKERS)} tickers from {start} to {end} into {db_path}")


if __name__ == "__main__":
    main()
