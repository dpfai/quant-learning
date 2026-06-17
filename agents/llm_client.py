"""Small OpenAI-compatible LLM client wrapper."""
from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from config.loader import load_config


class LLMClient:
    """Generate optional educational summaries through OpenAI-compatible APIs."""

    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        api_format: Optional[str] = None,
        client=None,
    ) -> None:
        config = load_config()
        llm_config = config.get("llm", {})
        self.provider = (
            provider
            or os.getenv("LLM_PROVIDER")
            or llm_config.get("provider")
            or "qianfan"
        )
        self.model = model or os.getenv("LLM_MODEL") or llm_config.get("model", "glm-5")
        self.base_url = (
            base_url
            or os.getenv("LLM_BASE_URL")
            or llm_config.get("base_url")
        )
        self.api_format = (
            api_format
            or os.getenv("LLM_API_FORMAT")
            or llm_config.get("api_format")
            or "chat_completions"
        )
        if client is not None:
            self.client = client
            return

        api_key = self._resolve_api_key()
        if not api_key:
            raise RuntimeError(
                "LLM API key is not configured. Set LLM_API_KEY, BAIDU_API_KEY, "
                "QIANFAN_API_KEY, or OPENAI_API_KEY before generating AI summaries."
            )
        client_kwargs = {"api_key": api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
        self.client = OpenAI(**client_kwargs)

    def _resolve_api_key(self) -> Optional[str]:
        """Resolve a provider-specific API key without storing secrets in config."""
        env_names = ["LLM_API_KEY"]
        if self.provider == "qianfan":
            env_names.extend(["BAIDU_API_KEY", "QIANFAN_API_KEY"])
        if self.provider == "openai":
            env_names.append("OPENAI_API_KEY")
        env_names.append("OPENAI_API_KEY")

        for name in dict.fromkeys(env_names):
            value = os.getenv(name)
            if value:
                return value
        return None

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Generate text using a configured OpenAI-compatible API format."""
        if self.api_format == "responses":
            return self._generate_responses(prompt, system_prompt)
        if self.api_format in {"chat", "chat_completions"}:
            return self._generate_chat_completion(prompt, system_prompt)
        raise ValueError(f"Unknown LLM API format: {self.api_format}")

    def _generate_responses(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=prompt,
        )
        return response.output_text

    def _generate_chat_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content or ""
