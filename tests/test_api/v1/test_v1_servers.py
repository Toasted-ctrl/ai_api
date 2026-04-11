class TestGetLlmServers:

    def test_success(self, client):
        response = client.get("/api/v1/servers")
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Success",
            "servers": ["ollama"]
        }

class TestWakeServer:

    def test_success(self, monkeypatch, client):
        monkeypatch.setattr(
            "api.v1.servers.boot_server",
            lambda mac_address: True
        )
        response = client.get("/api/v1/servers/ollama/wake")
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Sent magic packet to 'ollama' server. Please verify the server is online."
        }

    def test_server_not_found(self, client):
        response = client.get("/api/v1/servers/test/wake")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Server not found: test"
        }

class TestGetServerStatus:

    # TODO: Update success case to allow for more flexible testing, i.e:
    # make test independent from Ollama server > mock config.

    def test_server_online_available(self, monkeypatch, client):
        monkeypatch.setattr(
            "api.v1.servers.is_server_online",
            lambda url: True
        )
        response = client.get("/api/v1/servers/ollama/status")
        assert response.status_code == 200
        assert response.json() == {
            "server_name": "ollama",
            "status": "Online",
            "available": True
        }

    # TODO: Update success case to allow for more flexible testing, i.e:
    # make test independent from Ollama server > mock config.

    def test_server_online_unavailable(self, monkeypatch, client):
        monkeypatch.setattr(
            "api.v1.servers.is_server_online",
            lambda url: False
        )
        response = client.get("/api/v1/servers/ollama/status")
        assert response.status_code == 200
        assert response.json() == {
            "server_name": "ollama",
            "status": "Online",
            "available": False
        }

    def test_server_not_found(self, client):
        response = client.get("/api/v1/servers/test/status")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Server not found: test"
        }

    