import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dep_verify_user import depends_verify_user, VerifiedUser
from database.documents_users import get_user_documents_by_scope, delete_user_document_by_document_id
from database.session import get_db_session
from iom.documents import ResponseDocuments, ResponseDeleteDocument


router = APIRouter(prefix="/documents")


@router.get(
    "/user/{scope}",
    tags=["Documents"],
    description="Retrieve a list of User stored documents by scope.",
    response_model=ResponseDocuments
)
async def get_user_documents(
    scope: str,
    user: VerifiedUser = Depends(depends_verify_user),
    session: AsyncSession = Depends(get_db_session)
) -> ResponseDocuments:
    return ResponseDocuments(
        documents_scope=scope,
        documents=await get_user_documents_by_scope(
            session=session,
            user_id=user.id,
            scope=scope
        )
    )


@router.delete(
    "/user/{document_id}",
    tags=["Documents"],
    description="Delete a User provided document by document_id",
    response_model=ResponseDeleteDocument
)
async def delete_user_document(
    document_id: str,
    user: VerifiedUser = Depends(depends_verify_user),
    session: AsyncSession = Depends(get_db_session)
) -> ResponseDeleteDocument:

    # TODO: Work on error handling. What if no document for the specified user and document id exists?

    user_document_id = uuid.UUID(document_id)
    docid = await delete_user_document_by_document_id(
        session=session,
        user_id=user.id,
        document_id=user_document_id
    )

    return ResponseDeleteDocument(
        id=docid,
        is_deleted=True
    )
