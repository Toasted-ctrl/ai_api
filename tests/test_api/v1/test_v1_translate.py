import pytest

from unittest.mock import patch

class TestGetTranslationModels:

    def test_success(self, monkeypatch, client):
        monkeypatch.setattr(
            "api.v1.translate.is_ollama_server_online",
            lambda base_url: True)

        monkeypatch.setattr(
            "api.v1.translate.get_translators",
            lambda base_url: [
                {
                    "model_name": "test_model_name",
                    "language_codes": [
                        "test_language"
                    ]
                }
            ]
        )

        response = client.get("/api/v1/translate")
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Success",
            "models": [
                {
                    "model_name": "test_model_name",
                    "language_codes": [
                        "test_language"
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

    def test_translation_models_unavailable(self, mock_no_translators, client):
        response = client.get("/api/v1/translate")
        assert response.status_code == 500
        assert response.json() == {
            "detail": "No translation models"
        }

class TestPostTranslationRequest:

    def test_success(self, monkeypatch, client):
        monkeypatch.setattr(
            "api.v1.translate.is_ollama_server_online",
            lambda base_url: True)
        
        payload = {
            "from_language": "test",
            "to_language": "test",
            "text_input": "test"
        }
        response = client.post("/api/v1/translate", json=payload)
        assert response.status_code == 200

    def test_ollama_server_offline(self, monkeypatch, client):
        monkeypatch.setattr(
            "api.v1.translate.is_ollama_server_online",
            lambda base_url: False)
        
        payload = {
            "from_language": "test",
            "to_language": "test",
            "text_input": "test"
        }

        response = client.post("/api/v1/translate", json=payload)
        assert response.status_code == 500
        assert response.json() == {
            "detail": "Ollama server offline"
        }