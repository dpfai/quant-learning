"""Consumer-behavior factor prototypes."""
from __future__ import annotations


def consumer_demand_momentum(current_activity, baseline_activity):
    """Compare recent searches, visits, transactions, or app use with a baseline.

    The intended pipeline combines standardized high-frequency proxies and removes
    seasonality before measuring acceleration. It must use only observations that
    were available on each historical research date.
    """
    return current_activity / baseline_activity - 1


def discretionary_pressure(discretionary_spend, essential_spend):
    """Track discretionary spending relative to essential spending.

    A falling ratio can flag household budget pressure and should generally be
    evaluated within income cohorts and sectors rather than as a broad market call.
    """
    return discretionary_spend / essential_spend
