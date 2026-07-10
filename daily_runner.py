"""Run the Quant Learning Trading Arena update after the market close."""
from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

from trading_arena_common import (
    BACKFILL_START,
    DB_PATH,
    TRADE_TICKERS,
    download_history,
    latest_market_date,
    parse_date,
    simulate_portfolio,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Update Trading Arena data through today.")
    parser.add_argument("--end", default=date.today().isoformat())
    parser.add_argument("--db", default=str(DB_PATH))
    args = parser.parse_args()

    db_path = Path(args.db)
    stored_latest = latest_market_date(db_path)
    start = BACKFILL_START
    if stored_latest:
        start = parse_date(stored_latest, BACKFILL_START) + timedelta(days=1)
    end = parse_date(args.end, date.today())
    if start > end:
        print(f"No update needed. Latest stored date is {stored_latest}.")
        return

    history = download_history(TRADE_TICKERS, start=BACKFILL_START, end=end)
    simulate_portfolio(history, start=BACKFILL_START, end=end, db_path=db_path, reset_source=True)
    print(f"Updated Trading Arena data through {end} in {db_path}")


if __name__ == "__main__":
    main()
