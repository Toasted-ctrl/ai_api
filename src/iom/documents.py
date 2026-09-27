import uuid
from pydantic import BaseModel


class Document(BaseModel):
    name: str
    id: uuid.UUID


class ResponseDocuments(BaseModel):
    documents_scope: str
    documents: list[Document]


class ResponseDeleteDocument(BaseModel):
    id: uuid.UUID
    is_deleted: bool