"""SSE stream iterator for AllToken streaming responses."""
from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any, Generic, Protocol, TypeVar

import httpx

T = TypeVar("T")


class _FromDict(Protocol):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Any: ...


class AllTokenStream(Generic[T]):
    """Wraps an httpx streaming response, parses SSE lines into typed objects."""

    def __init__(self, response: httpx.Response, parser: _FromDict) -> None:
        self._response = response
        self._parser = parser

    def __iter__(self) -> Iterator[T]:
        for line in self._response.iter_lines():
            if not line.startswith("data: "):
                continue
            data = line[len("data: "):]
            if data.strip() == "[DONE]":
                break
            obj = json.loads(data)
            yield self._parser.from_dict(obj)

    def close(self) -> None:
        self._response.close()

    def __enter__(self) -> AllTokenStream[T]:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
