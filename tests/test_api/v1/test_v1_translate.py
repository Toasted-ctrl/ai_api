import pytest
import requests

# Route specific fixtures

@pytest.fixture
def mock_ollama_server_offline(monkeypatch):
    def mock_get_models(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Ollama server is offline")
    monkeypatch.setattr(
        "api.v1.translate.get_models",
        mock_get_models
    )

@pytest.fixture
def mock_no_models(monkeypatch):

    def mock_get_models(*args, **kwargs):
        return []
    
    monkeypatch.setattr(
        "api.v1.translate.get_models",
        mock_get_models
    )
    
@pytest.fixture
def mock_no_translators(monkeypatch):

    def mock_get_models(*args, **kwargs):
        return [
            {
                "name": "test_model_name"
            }
        ]
    
    def mock_get_translators(*args, **kwargs):
        return []
    
    monkeypatch.setattr(
        "api.v1.translate.get_models",
        mock_get_models
    )
    
    monkeypatch.setattr(
        "api.v1.translate.get_translators",
        mock_get_translators
    )
    
# Tests

class TestGetTranslationModels:

    def test_success(self, monkeypatch, client):
        monkeypatch.setattr(
            "api.v1.translate.get_models",
            lambda base_url: [
                {
                    "name": "translategemma:latest"
                }
            ])

        response = client.get("/api/v1/translate")
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Success",
            "models": [
                {
                    "model_name": "translategemma:latest",
                    "language_codes": [
                        "en-GB", "nl", "de-DE", "pt-PT"
                    ]
                }
            ]
        }

    def test_ollama_server_offline(self, mock_ollama_server_offline, client):
        response = client.get("/api/v1/translate")
        assert response.status_code == 503
        assert response.json() == {
            "detail": "Could not connect to Ollama server"
        }

    def test_models_unavailable(self, mock_no_models, client):
        response = client.get("/api/v1/translate")
        assert response.status_code == 500
        assert response.json() == {
            "detail": "No models"
        }

    def test_translation_models_unavailable(self, mock_no_translators, client):
        response = client.get("/api/v1/translate")
        assert response.status_code == 500
        assert response.json() == {
            "detail": "No translation models"
        }