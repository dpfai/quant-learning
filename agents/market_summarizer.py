"""Market and stock summary generation."""
from __future__ import annotations

from typing import Dict, Optional

from agents.llm_client import LLMClient
from agents.prompts import (
    MARKET_SUMMARY_PROMPT,
    MARKET_SUMMARY_SYSTEM,
    STOCK_ANALYSIS_PROMPT,
)


class MarketSummarizer:
    """Format market data and request an objective LLM summary."""

    def __init__(self, llm_client: Optional[LLMClient] = None) -> None:
        self.llm = llm_client or LLMClient()

    def summarize_market(self, market_data: Dict) -> str:
        """Generate a market overview."""
        prompt = MARKET_SUMMARY_PROMPT.format(**market_data)
        return self.llm.generate(prompt, MARKET_SUMMARY_SYSTEM)

    def analyze_stock(self, stock_data: Dict) -> str:
        """Generate a stock research snapshot."""
        prompt = STOCK_ANALYSIS_PROMPT.format(**stock_data)
        return self.llm.generate(prompt, MARKET_SUMMARY_SYSTEM)
