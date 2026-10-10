import uuid
from pydantic import BaseModel


class Document(BaseModel):
    name: str
    id: uuid.UUID


class ResponseGetDocuments(BaseModel):
    documents_scope: str
    documents: list[Document]


class ResponseDeleteDocument(BaseModel):
    id: uuid.UUID
    is_deleted: bool