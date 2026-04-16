"""Convenience dataclass types for chat completions."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ChatCompletionMessage:
    role: str
    content: str | None = None
    tool_calls: list[Any] | None = None


@dataclass
class ChatCompletionChoice:
    index: int
    message: ChatCompletionMessage
    finish_reason: str | None = None


@dataclass
class ChatCompletionUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ChatCompletion:
    id: str
    object: str
    created: int
    model: str
    choices: list[ChatCompletionChoice]
    usage: ChatCompletionUsage | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChatCompletion:
        choices = [
            ChatCompletionChoice(
                index=c["index"],
                message=ChatCompletionMessage(**c["message"]),
                finish_reason=c.get("finish_reason"),
            )
            for c in data["choices"]
        ]
        usage = ChatCompletionUsage(**data["usage"]) if data.get("usage") else None
        return cls(
            id=data["id"],
            object=data["object"],
            created=data["created"],
            model=data["model"],
            choices=choices,
            usage=usage,
        )


# Streaming chunk types


@dataclass
class ChatCompletionChunkDelta:
    role: str | None = None
    content: str | None = None


@dataclass
class ChatCompletionChunkChoice:
    index: int
    delta: ChatCompletionChunkDelta
    finish_reason: str | None = None


@dataclass
class ChatCompletionChunk:
    id: str
    object: str
    created: int
    model: str
    choices: list[ChatCompletionChunkChoice]
    usage: ChatCompletionUsage | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChatCompletionChunk:
        choices = [
            ChatCompletionChunkChoice(
                index=c["index"],
                delta=ChatCompletionChunkDelta(**c.get("delta", {})),
                finish_reason=c.get("finish_reason"),
            )
            for c in data["choices"]
        ]
        usage = ChatCompletionUsage(**data["usage"]) if data.get("usage") else None
        return cls(
            id=data["id"],
            object=data["object"],
            created=data["created"],
            model=data["model"],
            choices=choices,
            usage=usage,
        )
