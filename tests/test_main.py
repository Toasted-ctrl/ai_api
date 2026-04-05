import pytest

def test_app_starts(client):
    """
    Ensure the FastAPI application starts.
    """
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi_schema(client):
    """
    Ensure OpenAPI schema is available.
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "paths" in response.json()