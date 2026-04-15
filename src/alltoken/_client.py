"""Shared base configuration for the OpenAI and Anthropic sub-clients.

Both sub-clients share the same API key and base URL; only the path suffix
differs (/v1 vs /anthropic).
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AllTokenConfig:
    """Configuration for AllToken sub-clients."""

    api_key: str
    """API key from alltoken.ai. Found in Settings → API Keys."""

    base_url: str = "https://api.alltoken.ai"
    """Override the API base URL. Each sub-client appends its own path."""

    default_headers: dict[str, str] = field(default_factory=dict)
    """Extra headers sent on every request."""


def build_headers(config: AllTokenConfig) -> dict[str, str]:
    """Build the auth + default headers for every request."""
    return {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
        **config.default_headers,
    }


def join_base_url(base_url: str, path: str) -> str:
    """Join base URL + path, normalising trailing slashes."""
    return base_url.rstrip("/") + path
