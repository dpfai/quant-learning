"""Export Trading Arena SQLite tables to JSON files."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from trading_arena_common import (
    ARENA_DATA_DIR,
    DB_PATH,
    INITIAL_CASH,
    SOURCE_NAME,
    TRADE_TICKERS,
    WEEKLY_CONTRIBUTION,
    initialize_database,
    table_to_records,
    write_json,
)


def strategy_payload() -> list[dict]:
    """Return static strategy metadata for the Trading Arena site."""
    return [
        {
            "source": SOURCE_NAME,
            "name": "Quant Learning Four-Vote Composite",
            "tickers": TRADE_TICKERS,
            "initial_cash": INITIAL_CASH,
            "weekly_contribution": WEEKLY_CONTRIBUTION,
            "sub_strategies": [
                "MA20/MA50 crossover",
                "RSI mean reversion 30/70",
                "Bollinger Band 2 std",
                "ML direction classifier",
            ],
            "rules": {
                "buy_50_pct_cash": "3-4 bullish votes",
                "buy_25_pct_cash": "2 bullish votes",
                "sell_50_pct_position": "2 bearish votes",
                "sell_100_pct_position": "3-4 bearish votes",
            },
        }
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Trading Arena JSON data.")
    parser.add_argument("--db", default=str(DB_PATH))
    parser.add_argument("--out", default=str(ARENA_DATA_DIR))
    args = parser.parse_args()

    db_path = Path(args.db)
    out_dir = Path(args.out).expanduser()
    initialize_database(db_path)

    local_exports = {
        "strategies.json": strategy_payload(),
        "signals.json": table_to_records(db_path, "signals"),
        "equity_curve.json": table_to_records(db_path, "equity_curve"),
        "holdings.json": table_to_records(db_path, "holdings"),
    }
    for filename, records in local_exports.items():
        write_json(out_dir / filename, records)

    if out_dir != ARENA_DATA_DIR:
        ARENA_DATA_DIR.mkdir(parents=True, exist_ok=True)
        for filename in local_exports:
            shutil.copy2(out_dir / filename, ARENA_DATA_DIR / filename)
    print(f"Exported Trading Arena JSON files to {out_dir}")


if __name__ == "__main__":
    main()
