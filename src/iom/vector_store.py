from pydantic import BaseModel
import uuid


class Metadata(BaseModel):
    document_name: str


class PayloadSaveDocuments(BaseModel):
    texts: list[str]
    metadatas: list[Metadata]


class ResponseSavedDocuments(BaseModel):
    added_documents: list[uuid.UUID]


class PayloadSearchDocuments(BaseModel):
    query: str