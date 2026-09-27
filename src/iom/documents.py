from pydantic import BaseModel


class ResponseDocuments(BaseModel):
    documents_scope: str
    documents: list[str]