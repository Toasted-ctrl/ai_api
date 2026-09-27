from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.dep_verify_user import depends_verify_user, VerifiedUser
from database.documents_users import get_user_documents_by_scope
from database.session import get_db_session
from iom.documents import ResponseDocuments


router = APIRouter()


@router.get(
    "/documents/user/{scope}",
    tags=["Documents"],
    description="Retrieve a list of User stored documents by scope.",
    response_model=ResponseDocuments
)
def get_user_documents(
    scope: str,
    user: VerifiedUser = Depends(depends_verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseDocuments:
    return {
        "documents_scope": scope,
        "documents": get_user_documents_by_scope(
            session=session,
            user_id=user.id,
            scope=scope
        )
    }


#TODO: Implement feature to remove a document if requested.