"""Accounting quality factors."""
from __future__ import annotations

import numpy as np
import pandas as pd


def _divide(a: pd.Series, b: pd.Series) -> pd.Series:
    return (a / b.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan)


def return_on_equity(net_income: pd.Series, shareholders_equity: pd.Series) -> pd.Series:
    """ROE: net income divided by average/period shareholder equity."""
    return _divide(net_income, shareholders_equity)


def gross_profitability(gross_profit: pd.Series, total_assets: pd.Series) -> pd.Series:
    """Gross profitability: gross profit divided by total assets."""
    return _divide(gross_profit, total_assets)


def accruals(net_income: pd.Series, operating_cash_flow: pd.Series, total_assets: pd.Series) -> pd.Series:
    """Accrual intensity; lower values generally indicate higher earnings quality."""
    return _divide(net_income - operating_cash_flow, total_assets)
