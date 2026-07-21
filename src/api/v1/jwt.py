from fastapi import APIRouter, Depends

from io_models.authenticate import ResponseAuthenticate, PayloadAuthenticate
from middleware.authenticate import require_authentication

router = APIRouter()

@router.post(
    "/jwt",
    tags=["JWT"],
    response_model=ResponseAuthenticate,
    dependencies=[Depends(require_authentication)]
)
def post_authentication(payload: PayloadAuthenticate):
    return {
        "jwt": "test-jwt"
    }