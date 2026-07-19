"""Company size factor."""
from __future__ import annotations

import numpy as np
import pandas as pd


def market_cap_factor(market_cap: pd.DataFrame | pd.Series, small_is_high: bool = True):
    """Log market-cap exposure, optionally signed so smaller firms score higher."""
    exposure = np.log(market_cap.where(market_cap > 0))
    return -exposure if small_is_high else exposure
