from fastapi import APIRouter, Depends

from auth.dep_verify_user import depends_verify_user, VerifiedUser
from iom.user import ResponseAuthenticatedUser

router = APIRouter()

tags = ["Auth"]


@router.get(
    "/auth/me",
    tags=tags,
    response_model=ResponseAuthenticatedUser,
    description=f"Returns the user_id of the authenticated User."
)
def auth_me(
    user: VerifiedUser = Depends(depends_verify_user)
) -> ResponseAuthenticatedUser:
    return ResponseAuthenticatedUser(
        id=user.id
    )