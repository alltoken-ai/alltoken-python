"""Chat completions resource with typed convenience methods."""
from __future__ import annotations

from typing import Any, Literal, overload

import httpx

from .._error import AllTokenError
from .._streaming import AllTokenStream
from .._types import ChatCompletion, ChatCompletionChunk


class ChatCompletions:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    @overload
    def create(
        self, *, stream: Literal[True], **kwargs: Any
    ) -> AllTokenStream[ChatCompletionChunk]: ...

    @overload
    def create(
        self, *, stream: Literal[False] = ..., **kwargs: Any
    ) -> ChatCompletion: ...

    def create(
        self, *, stream: bool = False, **kwargs: Any
    ) -> ChatCompletion | AllTokenStream[ChatCompletionChunk]:
        body = {**kwargs, "stream": stream}
        if stream:
            request = self._client.build_request(
                "POST", "/chat/completions", json=body
            )
            response = self._client.send(request, stream=True)
            if response.status_code != 200:
                body_text = response.read().decode()
                response.close()
                raise AllTokenError(response.status_code, body_text)
            return AllTokenStream(response, ChatCompletionChunk)
        else:
            response = self._client.post("/chat/completions", json=body)
            if response.status_code != 200:
                raise AllTokenError(response.status_code, response.text)
            return ChatCompletion.from_dict(response.json())


class Chat:
    def __init__(self, client: httpx.Client) -> None:
        self.completions = ChatCompletions(client)
