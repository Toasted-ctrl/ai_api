from fastapi import HTTPException, Depends, status

from auth.client import get_client_from_key, VerifiedClient

def get_jwt_path_client(
    client: VerifiedClient = Depends(get_client_from_key)
) -> VerifiedClient:
    
    if client.key_type == "Application":
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Method only allowed for frontend application."
        )

    return client