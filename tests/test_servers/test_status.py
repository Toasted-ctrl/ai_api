import pytest

from unittest.mock import patch, Mock

from servers.status import is_server_online

# Test fixtures

@pytest.fixture
def ts_mock_ollama_server_available():
    mock = Mock()
    mock.status_code = 200
    return mock

@pytest.fixture
def ts_mock_ollama_server_unavailable():
    mock = Mock()
    mock.status_code = 400
    return mock

# Tests

def test_success(ts_mock_ollama_server_available):
    with patch(
        "requests.get",
        return_value=ts_mock_ollama_server_available
    ):
        assert is_server_online(url="TEST_URL") is True

def test_offline(ts_mock_ollama_server_unavailable):
    with patch(
        "requests.get",
        side_effect=ts_mock_ollama_server_unavailable
    ):
        assert is_server_online(url="TEST_URL") is False