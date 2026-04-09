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

    def test_connection_error(self, mock_ollama_server_offline, client):
        response = client.get("/api/v1/models")
        assert response.status_code == 503
        assert response.json() == {
            "detail": "Could not connect to Ollama server"
        }