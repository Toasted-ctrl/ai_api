from fastapi import Request, HTTPException, Depends, status
from fastapi.security import APIKeyHeader

from auth.verify import get_application

api_key_header = APIKeyHeader(name="X-API-Key")

def require_authentication(
    request: Request,
    api_key: str = Depends(api_key_header)
):
    
    # Checking if API Key is valid
    client = get_application(api_key=api_key)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    