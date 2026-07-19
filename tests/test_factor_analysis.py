import numpy as np
import pandas as pd

from backtest.factor_analysis import calc_ic, quantile_portfolio


def test_calc_ic_perfect_cross_sectional_relationship():
    factor = pd.DataFrame([[1, 2, 3], [3, 2, 1]], index=pd.date_range("2024-01-01", periods=2), columns=list("ABC"))
    returns = factor * 0.01
    result = calc_ic(factor, returns)
    assert np.allclose(result["ic"], 1.0)
    assert np.allclose(result["rank_ic"], 1.0)


def test_quantile_portfolio_assigns_low_to_high_groups():
    factor = pd.DataFrame([range(1, 11)], index=[pd.Timestamp("2024-01-01")], columns=list("ABCDEFGHIJ"))
    returns = factor / 100
    result = quantile_portfolio(factor, returns, n_quantiles=5)
    assert np.isclose(result.loc[result.index[0], "Q1"], 0.015)
    assert np.isclose(result.loc[result.index[0], "Q5"], 0.095)
    assert result.loc[result.index[0], "Q5"] > result.loc[result.index[0], "Q1"]
