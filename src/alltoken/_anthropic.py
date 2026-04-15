"""Anthropic-compatible client.

Backed by ``anthropic.yml``. Base URL: ``https://api.alltoken.ai/anthropic``.
"""
from __future__ import annotations

import httpx

from ._client import AllTokenConfig, build_headers, join_base_url

_ANTHROPIC_PATH = "/anthropic"


class AnthropicClient:
    """Anthropic-compatible client.

    The underlying pre-configured ``httpx.Client`` is exposed as ``.raw``:

        >>> resp = client.anthropic.raw.post(
        ...     "/messages",
        ...     json={
        ...         "model": "claude-sonnet-4",
        ...         "max_tokens": 1024,
        ...         "messages": [{"role": "user", "content": "Hi"}],
        ...     },
        ... )
    """

    raw: httpx.Client

    def __init__(self, config: AllTokenConfig) -> None:
        self.raw = httpx.Client(
            base_url=join_base_url(config.base_url, _ANTHROPIC_PATH),
            headers=build_headers(config),
            timeout=httpx.Timeout(60.0, connect=10.0),
        )

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self.raw.close()

    def __enter__(self) -> AnthropicClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
