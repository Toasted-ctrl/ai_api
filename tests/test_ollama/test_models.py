import pytest
import requests

from unittest.mock import patch, Mock

from ollama_server.models import get_models, get_translators

# Test fixtures

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

# Tests

class TestGetOllamaModels:

    def test_success(self, mock_get_running_ollama_models):
        with patch(
            "requests.get",
            return_value=mock_get_running_ollama_models 
        ):
            result = get_models(base_url="TEST_URL")
            assert isinstance(result, list)

    def test_offline(self, mock_get_running_ollama_models_offline):
        with patch(
            "requests.get",
            side_effect=mock_get_running_ollama_models_offline
        ):
            with pytest.raises(requests.exceptions.ConnectionError):
                get_models(base_url="TEST_URL")

class TestGetTranslationModels:

    def test_success(self):
            
            models = [
                {
                    "name": "test_name"
                },
                {
                    "name": "translategemma:latest"
                }
            ]

            result = get_translators(models=models)
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]['model_name'] == "translategemma:latest"
            assert result[0]['language_codes'] == [
                "en-GB",
                "nl",
                "de-DE",
                "pt-PT"
            ]

    # TODO: Build test for if no translation models were located.