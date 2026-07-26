from dataclasses import dataclass
from fastapi import HTTPException, Depends, status
import uuid

from auth.client import get_client_from_key, VerifiedClient

@dataclass
class VerifiedClientID:
    id: uuid.UUID


def get_jwt_path_client(
    client: VerifiedClient = Depends(get_client_from_key)
) -> VerifiedClientID:
    
    if client.key_type != "Application":
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Method only allowed for frontend applications"
        )

    return VerifiedClientID(
        id=client.id
    )