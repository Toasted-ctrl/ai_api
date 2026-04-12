class TestGetAllModels:

    def test_success(self, client):
        response = client.get("/api/v1/models")
        json: dict = response.json()
        assert response.status_code == 200
        assert 'detail' in json.keys()
        assert 'servers' in json.keys()
        assert isinstance(json.get('servers'), list)

class TestGetTranslationModels:

    def test_success(self, client):
        response = client.get("/api/v1/models/translation-models")
        json: dict = response.json()
        assert response.status_code == 200
        assert 'detail' in json.keys()
        assert isinstance(json.get('servers'), list)

class TestGetVectorEmbeddingModels:

    def test_success(self, client):
        response = client.get("/api/v1/models/vector-embeddings")
        json: dict = response.json()
        assert response.status_code == 200
        assert 'detail' in json.keys()
        assert isinstance(json.get('servers'), list)

class TestGetLLMs:

    def test_success(self, client):
        response = client.get("/api/v1/models/llms")
        json: dict = response.json()
        assert response.status_code == 200
        assert 'detail' in json.keys()
        assert isinstance(json.get('servers'), list)