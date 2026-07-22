from fastapi import APIRouter, Depends

from auth.hmac import verify_hmac_signature
from io_models.jwt import ResponseJWT, PayloadJWT
from middleware.get_client import get_jwt_path_client

router = APIRouter()

@router.post(
    "/jwt",
    tags=["JWT"],
    response_model=ResponseJWT,
    dependencies=[Depends(verify_hmac_signature)]
)
def post_authentication(payload: PayloadJWT, client: str = Depends(get_jwt_path_client)):
    return {
        "jwt": "test-jwt"
    }