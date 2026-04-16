from alltoken import AllToken


def test_creates_client() -> None:
    client = AllToken(api_key="test-key")
    assert client.openai is not None
    assert client.anthropic is not None


def test_default_base_url() -> None:
    client = AllToken(api_key="test-key")
    assert "alltoken.ai" in str(client.openai.raw.base_url)
    assert "alltoken.ai" in str(client.anthropic.raw.base_url)
