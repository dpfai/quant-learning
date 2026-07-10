"""Vectorized backtest engine with transaction costs."""
from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd

from features.risk_metrics import (
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)


class BacktestEngine:
    """Run close-to-close signal backtests without same-bar look-ahead."""

    def __init__(
        self,
        commission: float = 0.001,
        slippage: float = 0.0005,
    ) -> None:
        if commission < 0 or slippage < 0:
            raise ValueError("Trading costs cannot be negative")
        self.commission = commission
        self.slippage = slippage

    def run(
        self,
        prices: pd.Series,
        signals: pd.Series,
        initial_capital: float = 100_000,
    ) -> Dict[str, object]:
        """Run a backtest using signals shifted one bar before execution."""
        if initial_capital <= 0:
            raise ValueError("initial_capital must be positive")

        data = pd.concat(
            [
                pd.to_numeric(prices, errors="coerce").rename("price"),
                pd.to_numeric(signals, errors="coerce").rename("signal"),
            ],
            axis=1,
            join="inner",
        ).dropna()
        if len(data) < 2:
            raise ValueError("At least two aligned price observations are required")

        data["signal"] = data["signal"].clip(-1, 1)
        positions = data["signal"].shift(1).fillna(0)
        asset_returns = data["price"].pct_change(fill_method=None).fillna(0)
        turnover = positions.diff().abs().fillna(positions.abs())
        costs = turnover * (self.commission + self.slippage)
        strategy_returns = positions * asset_returns - costs
        equity_curve = initial_capital * (1 + strategy_returns).cumprod()

        trade_mask = turnover > 0
        trades = pd.DataFrame(
            {
                "Price": data.loc[trade_mask, "price"],
                "Position": positions.loc[trade_mask],
                "Turnover": turnover.loc[trade_mask],
                "Cost": (
                    initial_capital
                    * turnover.loc[trade_mask]
                    * (self.commission + self.slippage)
                ),
            }
        )
        trades.index.name = "Date"

        return {
            "equity_curve": equity_curve.rename("Equity"),
            "positions": positions.rename("Position"),
            "strategy_returns": strategy_returns.rename("Strategy Return"),
            "trades": trades,
            "metrics": self.calculate_metrics(equity_curve, trades),
        }

    def calculate_metrics(
        self,
        equity_curve: pd.Series,
        trades: pd.DataFrame | None = None,
    ) -> Dict[str, float | int]:
        """Calculate standard performance metrics from an equity curve."""
        returns = equity_curve.pct_change(fill_method=None).dropna()
        max_drawdown, _, _ = calculate_max_drawdown(equity_curve)
        gains = returns[returns > 0]
        losses = returns[returns < 0]
        loss_sum = abs(float(losses.sum()))
        profit_factor = (
            float(gains.sum()) / loss_sum if not np.isclose(loss_sum, 0) else float("nan")
        )
        return {
            "total_return": float(equity_curve.iloc[-1] / equity_curve.iloc[0] - 1),
            "annualized_return": calculate_annualized_return(returns),
            "annualized_volatility": calculate_annualized_volatility(returns),
            "sharpe_ratio": calculate_sharpe_ratio(returns, risk_free_rate=0),
            "max_drawdown": max_drawdown,
            "win_rate": float((returns > 0).mean()) if not returns.empty else float("nan"),
            "profit_factor": profit_factor,
            "num_trades": 0 if trades is None else len(trades),
        }
