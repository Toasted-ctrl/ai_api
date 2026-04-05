from unittest.mock import patch

from ollama.server_status import is_ollama_server_online

class TestIsOllamaServerOnline:

    def test_success(self, mock_ollama_server_online):
        with patch("requests.get", return_value=mock_ollama_server_online):
            assert is_ollama_server_online(base_url="TEST_URL") is True

    def test_offline(self, mock_ollama_server_offline):
        with patch("requests.get", return_value=mock_ollama_server_offline):
            assert is_ollama_server_online(base_url="TEST_URL") is False