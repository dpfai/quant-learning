"""Reusable cross-sectional factor evaluation tools."""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


def _aligned_frames(factor, returns):
    factor, returns = factor.align(returns, join="inner", axis=0)
    if isinstance(factor, pd.DataFrame) and isinstance(returns, pd.DataFrame):
        factor, returns = factor.align(returns, join="inner", axis=1)
    return factor, returns


def calc_ic(factor: pd.DataFrame, forward_returns: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily Pearson IC and Spearman rank IC across securities."""
    factor, forward_returns = _aligned_frames(factor, forward_returns)
    rows = []
    for date in factor.index:
        sample = pd.concat([factor.loc[date], forward_returns.loc[date]], axis=1).dropna()
        rows.append((date, sample.iloc[:, 0].corr(sample.iloc[:, 1]), sample.iloc[:, 0].corr(sample.iloc[:, 1], method="spearman")))
    return pd.DataFrame(rows, columns=["date", "ic", "rank_ic"]).set_index("date")


def quantile_portfolio(factor: pd.DataFrame, returns: pd.DataFrame, n_quantiles: int = 5) -> pd.DataFrame:
    """Return equal-weight returns for factor quantiles on every date."""
    if n_quantiles < 2:
        raise ValueError("n_quantiles must be at least 2")
    factor, returns = _aligned_frames(factor, returns)
    output = []
    for date in factor.index:
        sample = pd.DataFrame({"factor": factor.loc[date], "return": returns.loc[date]}).dropna()
        row = {f"Q{i}": np.nan for i in range(1, n_quantiles + 1)}
        if len(sample) >= n_quantiles:
            ranks = sample["factor"].rank(method="first")
            labels = pd.qcut(ranks, n_quantiles, labels=False) + 1
            row.update(sample.groupby(labels)["return"].mean().rename(lambda q: f"Q{q}").to_dict())
        output.append(pd.Series(row, name=date))
    return pd.DataFrame(output)


def fama_macbeth(factor: pd.DataFrame, returns: pd.DataFrame) -> dict:
    """Run cross-sectional regressions by date and summarize coefficient means."""
    factor, returns = _aligned_frames(factor, returns)
    coefficients = []
    for date in factor.index:
        sample = pd.DataFrame({"factor": factor.loc[date], "return": returns.loc[date]}).dropna()
        if len(sample) >= 3 and sample["factor"].nunique() > 1:
            coefficients.append(sm.OLS(sample["return"], sm.add_constant(sample["factor"])).fit().params.rename(date))
    estimates = pd.DataFrame(coefficients)
    mean = estimates.mean()
    standard_error = estimates.std(ddof=1) / np.sqrt(len(estimates))
    return {"period_coefficients": estimates, "mean_coefficients": mean, "t_stats": mean / standard_error, "n_periods": len(estimates)}
