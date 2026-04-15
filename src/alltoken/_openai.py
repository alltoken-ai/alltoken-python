"""OpenAI-compatible client.

Backed by ``chat.yml``. Base URL: ``https://api.alltoken.ai/v1``.
"""
from __future__ import annotations

import httpx

from ._client import AllTokenConfig, build_headers, join_base_url

_OPENAI_PATH = "/v1"


class OpenAIClient:
    """OpenAI-compatible client.

    The underlying pre-configured ``httpx.Client`` is exposed as ``.raw``:

        >>> resp = client.openai.raw.post(
        ...     "/chat/completions",
        ...     json={"model": "gpt-4o", "messages": [{"role": "user", "content": "Hi"}]},
        ... )
    """

    raw: httpx.Client

    def __init__(self, config: AllTokenConfig) -> None:
        self.raw = httpx.Client(
            base_url=join_base_url(config.base_url, _OPENAI_PATH),
            headers=build_headers(config),
            timeout=httpx.Timeout(60.0, connect=10.0),
        )

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self.raw.close()

    def __enter__(self) -> OpenAIClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
