"""Value factors. Lower valuation multiples represent stronger value."""
from __future__ import annotations

import numpy as np
import pandas as pd


def _safe_ratio(numerator, denominator):
    result = numerator / denominator.replace(0, np.nan) if isinstance(denominator, pd.Series) else numerator / denominator
    return result.replace([np.inf, -np.inf], np.nan) if hasattr(result, "replace") else result


def price_to_book(price: pd.Series, book_value_per_share: pd.Series) -> pd.Series:
    """Return price/book; invalid or zero book values become missing."""
    return _safe_ratio(price, book_value_per_share)


def price_to_earnings(price: pd.Series, earnings_per_share: pd.Series) -> pd.Series:
    """Return price/earnings; non-positive earnings are treated as missing."""
    return _safe_ratio(price, earnings_per_share.where(earnings_per_share > 0))


def ev_to_ebitda(enterprise_value: pd.Series, ebitda: pd.Series) -> pd.Series:
    """Return enterprise value/EBITDA; non-positive EBITDA is missing."""
    return _safe_ratio(enterprise_value, ebitda.where(ebitda > 0))
