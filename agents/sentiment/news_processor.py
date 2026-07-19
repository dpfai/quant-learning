"""News-event classification and impact scoring."""
from __future__ import annotations

import json
import logging

LOGGER = logging.getLogger(__name__)


class NewsProcessor:
    """Classify headlines through LLMClient, with a deterministic neutral fallback."""

    def __init__(self, llm_client=None):
        try:
            if llm_client is None:
                from agents.llm_client import LLMClient
                llm_client = LLMClient()
            self.llm_client = llm_client
        except Exception as exc:
            LOGGER.warning("LLM unavailable; news scores will be neutral: %s", exc)
            self.llm_client = None

    def process(self, headline: str, body: str = "", ticker: str | None = None) -> dict:
        fallback = {"ticker": ticker, "event_type": "other", "sentiment": 0.0, "impact": 0.0}
        if not headline or self.llm_client is None:
            return fallback
        prompt = "Return JSON only: event_type (earnings, product, regulation, macro, management, other), sentiment [-1,1], impact [0,1].\n" + headline + "\n" + body[:10000]
        try:
            raw = self.llm_client.generate(prompt).strip().removeprefix("```json").removesuffix("```").strip()
            data = json.loads(raw)
            return {"ticker": ticker, "event_type": str(data.get("event_type", "other")), "sentiment": max(-1.0, min(1.0, float(data.get("sentiment", 0)))), "impact": max(0.0, min(1.0, float(data.get("impact", 0))))}
        except Exception as exc:
            LOGGER.warning("News classification failed; using neutral score: %s", exc)
            return fallback

    @staticmethod
    def score_impact(event: dict) -> float:
        """Combine direction and expected materiality into a signed signal."""
        return float(event.get("sentiment", 0.0)) * float(event.get("impact", 0.0))
