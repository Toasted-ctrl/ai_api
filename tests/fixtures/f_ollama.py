import pytest
import requests

from unittest.mock import Mock

@pytest.fixture
def mock_ollama_server_online():
    mock = Mock()
    mock.status_code = 200
    return mock

@pytest.fixture
def mock_ollama_server_offline():
    return requests.exceptions.ConnectionError("Server is offline")

@pytest.fixture
def mock_get_running_ollama_models():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
        "models": [
            {
                "name": "translategemma:latest"
            },
            {
                "name": "llama2:latest"
            }
        ]
    }
    return mock

@pytest.fixture
def mock_get_running_ollama_models_offline():
    return requests.exceptions.ConnectionError("Could not retrieve running models")