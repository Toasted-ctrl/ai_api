def test_endpoint_root(client):
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Success",
        "application_name": "AIA: Artificial Intelligence API",
        "contact": {
            "maintainer": "Toasted-ctrl"
        },
        "version": "0.0.4"
    }