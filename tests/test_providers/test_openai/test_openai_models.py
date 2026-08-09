from unittest.mock import AsyncMock, patch, MagicMock
import pytest

from providers.openai.models import get_models
from security.encryption import encrypt


def _make_model(model_id: str) -> MagicMock:
    """Helper to create a mock model object with an `id` attribute."""
    model = MagicMock()
    model.id = model_id
    return model


def _make_models_response(model_ids: list[str]) -> MagicMock:
    """Helper to create a mock response from `client.models.list()`."""
    response = MagicMock()
    response.data = [_make_model(mid) for mid in model_ids]
    return response


@pytest.fixture
def mock_client():
    """Patches AsyncOpenAI as an async context manager and exposes the mock client instance."""
    with patch("providers.openai.models.AsyncOpenAI") as MockAsyncOpenAI:
        client_instance = AsyncMock()
        MockAsyncOpenAI.return_value.__aenter__ = AsyncMock(return_value=client_instance)
        MockAsyncOpenAI.return_value.__aexit__ = AsyncMock(return_value=False)
        yield client_instance, MockAsyncOpenAI


# -------------------------------------------------------------------
# Happy-path tests
# -------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_models_returns_expected_structure(mock_client):
    client_instance, _ = mock_client
    client_instance.models.list.return_value = _make_models_response(
        ["gpt-4", "gpt-3.5-turbo"]
    )

    result = await get_models(
        encrypted_api_key=encrypt("sk-test-key-123"),
        base_url="https://api.openai.com/v1"
    )

    assert result == {
        "chat_completion": ["gpt-4", "gpt-3.5-turbo"],
        "translation": [],
        "vector_embedding": [],
    }


@pytest.mark.asyncio
async def test_get_models_empty_list(mock_client):
    client_instance, _ = mock_client
    client_instance.models.list.return_value = _make_models_response([])

    result = await get_models(
        encrypted_api_key=encrypt("sk-test-key-123"),
        base_url="https://api.openai.com/v1"
    )

    assert result == {
        "chat_completion": [],
        "translation": [],
        "vector_embedding": [],
    }


@pytest.mark.asyncio
async def test_get_models_single_model(mock_client):
    client_instance, _ = mock_client
    client_instance.models.list.return_value = _make_models_response(["gpt-4o"])

    result = await get_models(
        encrypted_api_key=encrypt("sk-test-key-123"),
        base_url="https://api.openai.com/v1"
    )

    assert result["chat_completion"] == ["gpt-4o"]


# -------------------------------------------------------------------
# Client instantiation
# -------------------------------------------------------------------

@pytest.mark.asyncio
async def test_client_receives_correct_credentials(mock_client):
    client_instance, MockAsyncOpenAI = mock_client
    client_instance.models.list.return_value = _make_models_response([])

    key=encrypt("sk-my-key")

    await get_models(
        encrypted_api_key=key,
        base_url="https://custom.api/v1"
    )

    MockAsyncOpenAI.assert_called_once_with(
        api_key="sk-my-key",
        base_url="https://custom.api/v1",
    )


# -------------------------------------------------------------------
# Error propagation
# -------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_models_propagates_api_error(mock_client):
    client_instance, _ = mock_client
    client_instance.models.list.side_effect = Exception("Unauthorized")

    with pytest.raises(Exception, match="Unauthorized"):
        await get_models(
            encrypted_api_key=encrypt("sk-bad-key"),
            base_url="https://api.openai.com/v1"
        )