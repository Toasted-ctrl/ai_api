from dotenv import load_dotenv
from fastapi import HTTPException, status
import os
import pytest

from middleware.jwt_auth import jwt_auth

def test_invalid_key():
    with pytest.raises(HTTPException) as exc_info:
        jwt_auth(api_key='test-key')

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid API Key"


load_dotenv()
admin_api_key = os.getenv("ADMIN_API_KEY")

def test_invalid_user():
    with pytest.raises(HTTPException) as exc_info:
        jwt_auth(api_key=admin_api_key)

    assert exc_info.value.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert exc_info.value.detail == "Method only allowed for frontend apps, e.g.: JELAIME, etc."


jelaime_api_key = os.getenv("JELAIME_API_KEY")

def test_valid():
    result = jwt_auth(api_key=jelaime_api_key)
    assert result is None