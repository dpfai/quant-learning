"""Simple year-over-year comparison of 10-K risk-factor language."""
from __future__ import annotations

import re


def _sentences(text: str) -> set[str]:
    return {part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if len(part.strip()) >= 40}


def compare_risk_factors(current_text: str, previous_text: str) -> dict:
    """Identify added/removed risk sentences and a transparent change score.

    Production use should first extract SEC Item 1A and normalize boilerplate.
    """
    current, previous = _sentences(current_text), _sentences(previous_text)
    added, removed = sorted(current - previous), sorted(previous - current)
    union = len(current | previous)
    return {"added": added, "removed": removed, "change_score": (len(added) + len(removed)) / union if union else 0.0}
