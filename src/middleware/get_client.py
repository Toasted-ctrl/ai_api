from fastapi import HTTPException, Depends, status

from auth.verify import get_client_from_key, require_google_id

def get_jwt_path_client(
    client: str = Depends(get_client_from_key)
) -> None:
    
    # Checking if the API Key belongs to a frontend application user.
    # If frontend application user: Require Google data, e.g.: sub, email, given name, family name
    if not require_google_id(client=client):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Method only allowed for frontend apps, e.g.: JELAIME, etc."
        )

    return client