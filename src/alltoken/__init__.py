"""alltoken-ai — Official Python SDK for AllToken.

One API for OpenAI, Anthropic, and 100+ models.

Example:
    >>> from alltoken import AllToken
    >>> client = AllToken(api_key="...")
    >>> resp = client.openai.raw.post(
    ...     "/chat/completions",
    ...     json={"model": "gpt-4o", "messages": [{"role": "user", "content": "Hi"}]},
    ... )
    >>> print(resp.json())
"""
from __future__ import annotations

from ._anthropic import AnthropicClient
from ._client import AllTokenConfig
from ._openai import OpenAIClient

__version__ = "0.1.0"


class AllToken:
    """Unified client exposing both OpenAI-compatible and Anthropic-compatible surfaces.

    Both sub-clients share the same API key and base URL; only the path suffix differs
    (/v1 vs /anthropic).
    """

    openai: OpenAIClient
    anthropic: AnthropicClient

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://api.alltoken.ai",
        default_headers: dict[str, str] | None = None,
    ) -> None:
        config = AllTokenConfig(
            api_key=api_key,
            base_url=base_url,
            default_headers=default_headers or {},
        )
        self.openai = OpenAIClient(config)
        self.anthropic = AnthropicClient(config)


__all__ = ["AllToken", "AllTokenConfig", "AnthropicClient", "OpenAIClient", "__version__"]
