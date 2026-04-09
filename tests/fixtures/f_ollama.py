import pytest
import requests

from unittest.mock import Mock

@pytest.fixture
def mock_ollama_server_online():
    mock = Mock()
    mock.status_code = 200
    return mock

@pytest.fixture
def mock_ollama_server_offline(monkeypatch):
    def mock_get_models(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Ollama server is offline")
    monkeypatch.setattr(
        "api.v1.models.get_models",
        mock_get_models)

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