from pydantic import BaseModel
import uuid


class Metadata(BaseModel):
    document_name: str


class PayloadSaveDocuments(BaseModel):
    texts: list[str]
    metadata: list[Metadata]
    collection_name: str


class ResponseSavedDocuments(BaseModel):
    added_docs: list[uuid.UUID]