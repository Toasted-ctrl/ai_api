import uuid
from sqlalchemy.orm import Session

from .schemas.documents_user import DocumentsUsersT


def store_user_document(
    session: Session,
    user_id: uuid.UUID,
    name: str,
    scope: str
) -> uuid.UUID:
    exists = (
        session.query(DocumentsUsersT.id)
        .filter(
            DocumentsUsersT.name == name,
            DocumentsUsersT.scope == scope,
            DocumentsUsersT.user_id == user_id
        )
        .all()
    )
    if exists:
        raise ValueError(f"File '{name}' with scope '{scope}' scope already exists.")
    nf = DocumentsUsersT(
        user_id=user_id,
        name=name,
        scope=scope
    )
    session.add(nf)
    session.flush()
    return nf.id