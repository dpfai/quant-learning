"""Statistical checks for candidate alpha factors."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def bonferroni_correction(pvalues):
    """Return family-wise-error corrected p-values, preserving pandas labels."""
    corrected = np.minimum(np.asarray(pvalues, dtype=float) * np.asarray(pvalues).size, 1.0)
    return pd.Series(corrected, index=pvalues.index, name=pvalues.name) if isinstance(pvalues, pd.Series) else corrected


def deflated_sharpe(sharpe: float, n_trials: int, n_obs: int, skew: float = 0.0, kurt: float = 3.0) -> float:
    """Approximate probability that Sharpe exceeds the multiple-trial benchmark."""
    if n_trials < 1 or n_obs < 2:
        raise ValueError("n_trials must be positive and n_obs must exceed one")
    expected_max = stats.norm.ppf(1 - 1 / (max(n_trials, 2) * np.e)) / np.sqrt(n_obs)
    variance = max(1 - skew * sharpe + ((kurt - 1) / 4) * sharpe**2, 1e-12)
    z_score = (sharpe - expected_max) * np.sqrt(n_obs - 1) / np.sqrt(variance)
    return float(stats.norm.cdf(z_score))


def orthogonalize_factor(factor, known_factors):
    """Residualize a factor against known exposures using OLS with an intercept."""
    y = factor.rename("factor")
    x = known_factors.to_frame() if isinstance(known_factors, pd.Series) else known_factors.copy()
    sample = pd.concat([y, x], axis=1).dropna()
    design = np.column_stack([np.ones(len(sample)), sample[x.columns].to_numpy()])
    fitted = design @ np.linalg.lstsq(design, sample["factor"].to_numpy(), rcond=None)[0]
    residual = pd.Series(np.nan, index=factor.index, name=factor.name)
    residual.loc[sample.index] = sample["factor"] - fitted
    return residual


def factor_turnover(factor_series):
    """Mean absolute change in cross-sectional percentile ranks."""
    if isinstance(factor_series, pd.DataFrame):
        ranks = factor_series.rank(axis=1, pct=True)
        return ranks.diff().abs().mean(axis=1)
    return factor_series.rank(pct=True).diff().abs()


def factor_halflife(factor: pd.DataFrame, forward_returns: pd.DataFrame) -> float:
    """Estimate IC decay half-life from exponentially decaying lag correlations."""
    from backtest.factor_analysis import calc_ic
    decay = []
    for lag in range(1, min(21, len(factor))):
        decay.append(calc_ic(factor, forward_returns.shift(-lag))["rank_ic"].mean())
    values = np.abs(np.asarray(decay))
    valid = np.isfinite(values) & (values > 0)
    if valid.sum() < 2:
        return float("nan")
    slope = np.polyfit(np.arange(1, len(values) + 1)[valid], np.log(values[valid]), 1)[0]
    return float(-np.log(2) / slope) if slope < 0 else float("inf")
