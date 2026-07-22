from fastapi import HTTPException, Depends, status
from fastapi.security import APIKeyHeader

from auth.verify import get_application, require_google_id

api_key_header = APIKeyHeader(name="X-API-Key")

def jwt_auth(
    api_key: str = Depends(api_key_header)
) -> None:
    
    # Checking if API Key is valid.
    client = get_application(api_key=api_key)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    # Checking if the API Key belongs to a frontend application user.
    # If frontend application user: Require Google data, e.g.: sub, email, given name, family name
    if not require_google_id(client=client):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Method only allowed for frontend apps, e.g.: JELAIME, etc."
        )

    return None