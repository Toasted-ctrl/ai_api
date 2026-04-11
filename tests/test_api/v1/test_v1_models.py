import pytest
import requests

# Test fixtures

@pytest.fixture
def mock_ollama_server_offline(monkeypatch):
    def mock_get_models(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Ollama server is offline")
    monkeypatch.setattr(
        "api.v1.models.get_models",
        mock_get_models
    )
    
@pytest.fixture
def mock_no_models(monkeypatch):
    def mock_get_models(*args, **kwargs):
        return []
    monkeypatch.setattr(
        "api.v1.models.get_models",
        mock_get_models
    )

# Tests

class TestGetAllModels:

    def test_success(self, monkeypatch, client):
        monkeypatch.setattr(
            "api.v1.models.get_models",
            lambda base_url: [
                {
                    "name": "Test Name",
                    "size": 12345
                }
            ]
        )
        response = client.get("/api/v1/models")
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Success",
            "models": [
                {
                    "name": "Test Name",
                    "size": 12345
                }
            ]
        }

    def test_connection_error(self, mock_ollama_server_offline, client):
        response = client.get("/api/v1/models")
        assert response.status_code == 503
        assert response.json() == {
            "detail": "Could not connect to Ollama server"
        }

    def test_no_models(self, mock_no_models, client):
        response = client.get("/api/v1/models")
        assert response.status_code == 500
        assert response.json() == {
            "detail": "No models"
        }