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
        for server in response.json()['servers']:
            if 'model_types' in server.keys():
                model_types = server.get('model_types').keys()
                assert 'translations' in model_types
                assert 'vector_embeddings' not in model_types
                assert 'llms' not in model_types
                
class TestGetVectorEmbeddingModels:

    def test_success(self, client):
        response = client.get("/api/v1/models/vector-embeddings")
        json: dict = response.json()
        assert response.status_code == 200
        assert 'detail' in json.keys()
        assert isinstance(json.get('servers'), list)
        for server in response.json()['servers']:
            if 'model_types' in server.keys():
                model_types = server.get('model_types').keys()
                assert 'vector_embeddings' in model_types
                assert 'llms' not in model_types
                assert 'translations' not in model_types

class TestGetLLMs:

    def test_success(self, client):
        response = client.get("/api/v1/models/llms")
        json: dict = response.json()
        assert response.status_code == 200
        assert 'detail' in json.keys()
        assert isinstance(json.get('servers'), list)
        for server in response.json()['servers']:
            if 'model_types' in server.keys():
                model_types = server.get('model_types').keys()
                assert 'llms' in model_types
                assert 'vector_embeddings' not in model_types
                assert 'translations' not in model_types