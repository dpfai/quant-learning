"""Small OpenAI Responses API client wrapper."""
from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from config.loader import load_config


class LLMClient:
    """Generate optional educational summaries through OpenAI."""

    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        client=None,
    ) -> None:
        if provider != "openai":
            raise NotImplementedError(f"Provider {provider} not implemented")
        config = load_config()
        self.provider = provider
        self.model = model or config.get("llm", {}).get("model", "gpt-4o-mini")
        if client is not None:
            self.client = client
            return
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured. Set it before generating AI summaries."
            )
        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Generate text using the Responses API."""
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=prompt,
        )
        return response.output_text
