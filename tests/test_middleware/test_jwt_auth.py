from fastapi import HTTPException, status
import pytest

from middleware.get_client import get_jwt_path_client

def test_invalid_user():
    with pytest.raises(HTTPException) as exc_info:
        get_jwt_path_client(client = 'admin')

    assert exc_info.value.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert exc_info.value.detail == "Method only allowed for frontend apps, e.g.: JELAIME, etc."


def test_valid():
    result = get_jwt_path_client(client = 'jelaime')
    assert result == 'jelaime'