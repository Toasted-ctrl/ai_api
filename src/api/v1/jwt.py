from fastapi import APIRouter, Depends

from io_models.jwt import ResponseJWT, PayloadJWT
from middleware.jwt_auth import jwt_auth

router = APIRouter()

@router.post(
    "/jwt",
    tags=["JWT"],
    response_model=ResponseJWT,
    dependencies=[Depends(jwt_auth)]
)
def post_authentication(payload: PayloadJWT):
    return {
        "jwt": "test-jwt"
    }