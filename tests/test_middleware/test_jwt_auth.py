from dataclasses import dataclass
from fastapi import HTTPException, status
import pytest
import uuid

from middleware.issue_jwt import get_jwt_path_client, VerifiedClientID

@dataclass
class MockClientObject:
    key_type: str
    id: uuid.UUID


def test_invalid_user():

    test_client = MockClientObject(
        key_type="User",
        id=uuid.uuid4()
    )

    with pytest.raises(HTTPException) as exc_info:
        get_jwt_path_client(client = test_client)

    assert exc_info.value.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert exc_info.value.detail == "Method only allowed for frontend applications"


def test_valid():

    test_client = MockClientObject(
        key_type="Application",
        id=uuid.uuid4()
    )

    result = get_jwt_path_client(client = test_client)
    assert isinstance(result, VerifiedClientID)
    assert isinstance(result.id, uuid.UUID)