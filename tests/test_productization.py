"""Tests for configuration, logging, exports, and AI summary formatting."""

import logging

import pandas as pd

from agents.llm_client import LLMClient
from agents.market_summarizer import MarketSummarizer
from config.loader import load_config
from utils.export import dataframe_to_csv
from utils.logger import setup_logger


def test_load_config_reads_yaml(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("risk:\n  risk_free_rate: 0.04\n", encoding="utf-8")

    config = load_config(str(path))

    assert config["risk"]["risk_free_rate"] == 0.04


def test_logger_does_not_duplicate_handlers():
    logger = setup_logger("quant-learning-test", "DEBUG")
    original_count = len(logger.handlers)

    same_logger = setup_logger("quant-learning-test", "INFO")

    assert logger is same_logger
    assert len(logger.handlers) == original_count
    assert logger.level == logging.INFO


def test_dataframe_export_returns_csv_bytes():
    exported = dataframe_to_csv(pd.DataFrame({"Close": [100.0]}))

    assert isinstance(exported, bytes)
    assert b"Close" in exported


def test_llm_client_uses_responses_api():
    class FakeResponse:
        output_text = "Summary"

    class FakeResponses:
        def __init__(self):
            self.request = None

        def create(self, **kwargs):
            self.request = kwargs
            return FakeResponse()

    class FakeClient:
        def __init__(self):
            self.responses = FakeResponses()

    fake = FakeClient()
    client = LLMClient(model="test-model", client=fake)

    result = client.generate("Prompt", "Instructions")

    assert result == "Summary"
    assert fake.responses.request["model"] == "test-model"
    assert fake.responses.request["input"] == "Prompt"


def test_market_summarizer_formats_prompt():
    class FakeLLM:
        def generate(self, prompt, system_prompt):
            assert "RISK-ON" in prompt
            assert "educational" in system_prompt.lower()
            return "Analysis"

    result = MarketSummarizer(FakeLLM()).summarize_market(
        {
            "regime": "RISK-ON",
            "vix": 15.0,
            "spy_price": 500.0,
            "spy_change": 0.02,
            "sector_performance": "Technology +5%",
            "top_sector": "Technology",
            "weak_sector": "Utilities",
            "volatility_level": "low",
        }
    )

    assert result == "Analysis"
