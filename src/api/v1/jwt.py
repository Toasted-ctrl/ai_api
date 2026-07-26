from fastapi import APIRouter, Depends

from auth.client import VerifiedClient
from io_models.jwt import ResponseJWT, PayloadJWT
from middleware.issue_jwt import get_jwt_path_client

router = APIRouter()

@router.post(
    "/jwt",
    tags=["JWT"],
    response_model=ResponseJWT
)
def post_authentication(
    payload: PayloadJWT,
    client: VerifiedClient = Depends(get_jwt_path_client)
) -> ResponseJWT:
    return {
        "jwt": "test-jwt"
    }