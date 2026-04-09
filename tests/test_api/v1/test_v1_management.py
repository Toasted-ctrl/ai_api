class TestWakeServer:

    def test_success(self, monkeypatch, client):
        monkeypatch.setattr(
            "api.v1.management.boot_server",
            lambda mac_address: True
        )
        response = client.get("/api/v1/management/wake_server/ollama")
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Sent magic packet to 'ollama' server. Please verify the server is online."
        }

    def test_invalid_parameter(self, client):
        response = client.get("/api/v1/management/wake_server/test")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Server 'test' does not exist"
        }

    def test_missing_parameter(self, client):
        response = client.get("/api/v1/management/waker_server/")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Not Found"
        }