from unittest.mock import AsyncMock, patch
from dataclasses import dataclass

import pytest

from providers.ollama.models import get_models


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

@dataclass
class _FakeModel:
    """Mimics the object returned per-model by the Ollama SDK."""
    model: str


class _FakeListResponse:
    """Mimics the response object returned by `client.list()`."""
    def __init__(self, model_names: list[str]):
        self.models = [_FakeModel(model=name) for name in model_names]


def _make_list_response(model_names: list[str]) -> _FakeListResponse:
    """Helper to create a mock response from `client.list()`."""
    return _FakeListResponse(model_names)


# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------

@pytest.fixture
def mock_config():
    with patch("providers.ollama.models.config") as cfg:
        cfg.CHAT_COMPLETION_MODELS = ["llama3", "mistral", "codellama"]
        cfg.TRANSLATION_MODELS = ["argos-translate"]
        cfg.VECTOR_EMBEDDING_MODELS = ["nomic-embed-text", "all-minilm"]
        yield cfg


@pytest.fixture
def mock_client(mock_config):
    with patch("providers.ollama.models.AsyncClient") as MockAsyncClient:
        client_instance = AsyncMock()

        # Support `async with AsyncClient(...) as client:`
        MockAsyncClient.return_value.__aenter__ = AsyncMock(return_value=client_instance)
        MockAsyncClient.return_value.__aexit__ = AsyncMock(return_value=False)

        yield client_instance


# -------------------------------------------------------------------
# Happy-path tests
# -------------------------------------------------------------------

@pytest.mark.asyncio
async def test_models_are_categorised_correctly(mock_client):
    mock_client.list.return_value = _make_list_response([
        "llama3", "mistral", "nomic-embed-text", "argos-translate"
    ])

    result = await get_models(base_url="http://localhost:11434")

    assert result == {
        "chat_completion": ["llama3", "mistral"],
        "translation": ["argos-translate"],
        "vector_embedding": ["nomic-embed-text"],
    }


@pytest.mark.asyncio
async def test_all_chat_completion_when_no_special_models(mock_client):
    mock_client.list.return_value = _make_list_response([
        "llama3", "mistral", "codellama"
    ])

    result = await get_models(base_url="http://localhost:11434")

    assert result["chat_completion"] == ["llama3", "mistral", "codellama"]
    assert result["translation"] == []
    assert result["vector_embedding"] == []


@pytest.mark.asyncio
async def test_empty_model_list(mock_client):
    mock_client.list.return_value = _make_list_response([])

    result = await get_models(base_url="http://localhost:11434")

    assert result == {
        "chat_completion": [],
        "translation": [],
        "vector_embedding": [],
    }


@pytest.mark.asyncio
async def test_only_embedding_models(mock_client):
    mock_client.list.return_value = _make_list_response([
        "nomic-embed-text", "all-minilm"
    ])

    result = await get_models(base_url="http://localhost:11434")

    assert result["chat_completion"] == []
    assert result["vector_embedding"] == ["nomic-embed-text", "all-minilm"]


@pytest.mark.asyncio
async def test_only_translation_models(mock_client):
    mock_client.list.return_value = _make_list_response(["argos-translate"])

    result = await get_models(base_url="http://localhost:11434")

    assert result["chat_completion"] == []
    assert result["translation"] == ["argos-translate"]


# -------------------------------------------------------------------
# Client instantiation
# -------------------------------------------------------------------

@pytest.mark.asyncio
async def test_client_receives_correct_base_url(mock_config):
    with patch("providers.ollama.models.AsyncClient") as MockAsyncClient:
        client_instance = AsyncMock()
        client_instance.list.return_value = _make_list_response([])
        MockAsyncClient.return_value.__aenter__ = AsyncMock(return_value=client_instance)
        MockAsyncClient.return_value.__aexit__ = AsyncMock(return_value=False)

        await get_models(base_url="http://my-ollama:11434")

        MockAsyncClient.assert_called_once_with(host="http://my-ollama:11434")


# -------------------------------------------------------------------
# Error propagation
# -------------------------------------------------------------------

@pytest.mark.asyncio
async def test_propagates_connection_error(mock_client):
    mock_client.list.side_effect = ConnectionError("Connection refused")

    with pytest.raises(ConnectionError, match="Connection refused"):
        await get_models(base_url="http://localhost:11434")