from unittest.mock import AsyncMock, patch, MagicMock
import pytest

from providers.anthropic.models import get_models
from security.encryption import encrypt


def _make_model(display_name: str) -> MagicMock:
    """Helper to create a mock model object with a `display_name` attribute."""
    model = MagicMock()
    model.display_name = display_name
    return model


def _make_models_response(display_names: list[str]) -> MagicMock:
    """Helper to create a mock response from `client.models.list()`."""
    response = MagicMock()
    response.data = [_make_model(name) for name in display_names]
    return response


@pytest.fixture
def mock_client():
    """Patches AsyncAnthropic as an async context manager and exposes the mock client instance."""
    with patch("providers.anthropic.models.AsyncAnthropic") as MockAsyncAnthropic:
        client_instance = AsyncMock()
        MockAsyncAnthropic.return_value.__aenter__ = AsyncMock(return_value=client_instance)
        MockAsyncAnthropic.return_value.__aexit__ = AsyncMock(return_value=False)
        yield client_instance, MockAsyncAnthropic


# -------------------------------------------------------------------
# Happy-path tests
# -------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_models_returns_expected_structure(mock_client):
    client_instance, _ = mock_client
    client_instance.models.list.return_value = _make_models_response(
        ["Claude 3.5 Sonnet", "Claude 3 Opus"]
    )

    result = await get_models(encrypted_api_key=encrypt("sk-ant-test-key-123"))

    assert result == {
        "chat_completion": ["Claude 3.5 Sonnet", "Claude 3 Opus"],
        "translation": [],
        "vector_embedding": [],
    }


@pytest.mark.asyncio
async def test_get_models_empty_list(mock_client):
    client_instance, _ = mock_client
    client_instance.models.list.return_value = _make_models_response([])

    result = await get_models(encrypted_api_key=encrypt("sk-ant-test-key-123"))

    assert result == {
        "chat_completion": [],
        "translation": [],
        "vector_embedding": [],
    }


@pytest.mark.asyncio
async def test_get_models_single_model(mock_client):
    client_instance, _ = mock_client
    client_instance.models.list.return_value = _make_models_response(["Claude 3.5 Haiku"])

    result = await get_models(encrypted_api_key=encrypt("sk-ant-test-key-123"))

    assert result["chat_completion"] == ["Claude 3.5 Haiku"]


# -------------------------------------------------------------------
# Client instantiation
# -------------------------------------------------------------------

@pytest.mark.asyncio
async def test_client_receives_correct_api_key(mock_client):
    client_instance, MockAsyncAnthropic = mock_client
    client_instance.models.list.return_value = _make_models_response([])

    key = encrypt("sk-ant-my-key")

    await get_models(encrypted_api_key=key)

    MockAsyncAnthropic.assert_called_once_with(api_key="sk-ant-my-key")


# -------------------------------------------------------------------
# Error propagation
# -------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_models_propagates_api_error(mock_client):
    client_instance, _ = mock_client
    client_instance.models.list.side_effect = Exception("Authentication error")

    with pytest.raises(Exception, match="Authentication error"):
        await get_models(encrypted_api_key=encrypt("sk-ant-bad-key"))