import pytest

from unittest.mock import Mock

@pytest.fixture
def mock_ollama_server_online():
    mock = Mock()
    mock.status_code = 200
    return mock

@pytest.fixture
def mock_ollama_server_offline():
    mock = Mock()
    mock.status_code = 500
    return mock