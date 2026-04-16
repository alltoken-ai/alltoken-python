# alltoken

Official Python SDK for [AllToken](https://alltoken.ai) — one API for OpenAI, Anthropic, and 100+ models.

```bash
pip install alltoken
```

Requires **Python 3.10+**.

## Quick start

```python
from alltoken import AllToken

client = AllToken(api_key="...")  # or os.environ["ALLTOKEN_API_KEY"]

# OpenAI-compatible surface (maps to /v1)
resp = client.openai.raw.post(
    "/chat/completions",
    json={
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "Hello!"}],
    },
)
print(resp.json())

# Anthropic-compatible surface (maps to /anthropic)
resp = client.anthropic.raw.post(
    "/messages",
    json={
        "model": "claude-sonnet-4",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "Hello!"}],
    },
)
print(resp.json())
```

The same API key works for both surfaces. Model catalog: [alltoken.ai/models](https://alltoken.ai/models).

## Configuration

```python
AllToken(
    api_key="...",                      # required
    base_url="https://api.alltoken.ai", # optional, defaults to production
    default_headers={"X-My-Tag": "a"},  # optional, merged into every request
)
```

## API surface

| Field | Spec | Base URL |
|---|---|---|
| `client.openai.raw` | `chat.yml` (OpenAI-compatible) | `https://api.alltoken.ai/v1` |
| `client.anthropic.raw` | `anthropic.yml` | `https://api.alltoken.ai/anthropic` |

`.raw` is a pre-configured [httpx.Client](https://www.python-httpx.org/api/#client) — base URL + auth are set, call `.get()` / `.post()` / `.stream()` directly. Pydantic models for request/response bodies are generated from the OpenAPI specs into `alltoken.generated.chat` and `alltoken.generated.anthropic`.

## Status

**v0.1.0 — Scaffold.** Pydantic models are generated from the spec, the wrapper surface is minimal. Expect breaking changes in 0.x. Ergonomic helpers (`client.chat.completions.create(...)`, async streaming iterators, retries, etc.) are coming in 0.2.x.

## Contributing / Local development

```bash
# Clone megaopenrouter as a sibling (for the OpenAPI specs)
git clone git@gitlab.53site.com:ai-innovation-lab/megaopenrouter.git ../megaopenrouter

# Install with dev deps
pip install -e ".[dev]"

# Regenerate pydantic models from specs
python scripts/generate.py

# Test + lint
pytest
ruff check
mypy .
```

Generated models live in `src/alltoken/generated/{chat,anthropic}.py` — these are **committed** so users who install from PyPI don't need to run codegen.

## License

[MIT](./LICENSE)
