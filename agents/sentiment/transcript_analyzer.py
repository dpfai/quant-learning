"""Earnings-call transcript sentiment extraction."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Callable

LOGGER = logging.getLogger(__name__)
NEUTRAL = {"sentiment": 0.0, "confidence": 0.0, "forward_looking": 0.0, "certainty": 0.0}


class TranscriptAnalyzer:
    """Read transcript text and ask the configured LLM for structured scores."""

    def __init__(self, ticker: str, llm_client=None, transcript_fetcher: Callable[[str], str] | None = None):
        self.ticker = ticker.upper()
        self.transcript_fetcher = transcript_fetcher
        try:
            if llm_client is None:
                from agents.llm_client import LLMClient
                llm_client = LLMClient()
            self.llm_client = llm_client
        except Exception as exc:
            LOGGER.warning("LLM unavailable for %s; returning neutral transcript scores: %s", self.ticker, exc)
            self.llm_client = None

    def read_transcript(self, source: str | Path | None = None) -> str:
        """Read a local transcript, accept raw text, or call an injected fetcher."""
        if source is None:
            return self.transcript_fetcher(self.ticker) if self.transcript_fetcher else ""
        path = Path(source)
        return path.read_text(encoding="utf-8") if path.exists() else str(source)

    def analyze(self, source: str | Path | None = None) -> dict:
        """Return sentiment, certainty and forward-looking scores in [-1, 1]."""
        text = self.read_transcript(source)
        if not text or self.llm_client is None:
            LOGGER.warning("No transcript or configured LLM for %s; using neutral scores", self.ticker)
            return {"ticker": self.ticker, **NEUTRAL}
        prompt = f"Analyze this {self.ticker} earnings call. Return JSON only with numeric keys sentiment, confidence, forward_looking, certainty, each from -1 to 1.\n\n{text[:30000]}"
        try:
            raw = self.llm_client.generate(prompt, system_prompt="You extract cautious, structured financial-text signals; you do not give investment advice.")
            raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
            parsed = json.loads(raw)
            scores = {key: float(np_clip(parsed.get(key, 0.0))) for key in NEUTRAL}
            return {"ticker": self.ticker, **scores}
        except Exception as exc:
            LOGGER.warning("Transcript analysis failed for %s; using neutral scores: %s", self.ticker, exc)
            return {"ticker": self.ticker, **NEUTRAL}


def np_clip(value):
    return max(-1.0, min(1.0, float(value)))
