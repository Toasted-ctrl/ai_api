from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.dep_verify_user import depends_verify_user, VerifiedUser
from database.person import PersonDetails, get_person_by_person_id
from database.session import get_db_session
from database.user import get_user_by_user_id, UserDetails
from iom.authenticated_user import ResponseAuthenticatedUser


router = APIRouter()


@router.get(
    "/auth/me",
    tags=["Auth"],
    response_model=ResponseAuthenticatedUser,
    description=f"Returns the user_id, first name, last name and email address of the authenticated User."
)
def auth_me(
    user: VerifiedUser = Depends(depends_verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseAuthenticatedUser:
    
    u: UserDetails = get_user_by_user_id(
        session=session,
        user_id=user.id
    )
    if u is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    p: PersonDetails = get_person_by_person_id(
        session=session,
        person_id=u.person_id
    )
    if p is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Person not found"
        )
    
    return ResponseAuthenticatedUser(
        user_id=u.user_id,
        first_name=p.first_name,
        last_name=p.last_name,
        email=p.email
    )