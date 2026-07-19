"""Interpretable ad-tech sector signal prototypes."""
from __future__ import annotations


def digital_ad_spend_growth(current_spend, prior_spend):
    """Measure year-over-year digital ad spend growth.

    Business logic: accelerating advertiser budgets should benefit platforms and
    intermediaries, but production research should separate organic demand from
    acquisitions, currency effects, and changes in reported gross versus net spend.
    """
    return current_spend / prior_spend - 1


def ecpm_trend(current_ecpm, prior_ecpm):
    """Measure pricing power through effective cost per thousand impressions.

    Rising eCPM may indicate stronger advertiser demand or better inventory quality;
    interpret alongside impression volume because scarcity can raise eCPM while
    reducing total revenue opportunity.
    """
    return current_ecpm / prior_ecpm - 1


def platform_mix(high_margin_revenue, total_revenue):
    """Estimate exposure to higher-margin owned/platform revenue.

    A rising owned-platform mix can improve gross margin and control over data, but
    definitions must be normalized across firms before cross-sectional ranking.
    """
    return high_margin_revenue / total_revenue
