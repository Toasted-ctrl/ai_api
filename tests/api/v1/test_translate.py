class TestPostTranslationRequest:

    def test_success(self, client):
        payload = {
            "from_language": "test",
            "to_language": "test",
            "text_input": "test"
        }
        response = client.post("/api/v1/translate", json=payload)
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Success",
            "from_language": "test_from",
            "to_language": "test_to",
            "text_input": "test_input",
            "text_output": "test_output"
        }