from pydantic import BaseModel


class PayloadSingleVectorEmbedding(BaseModel):
    prompt: str
    provider: str
    model: str
    dimensions: int | None = None


class ResponseSingleVectorEmbedding(BaseModel):
    prompt: str
    provider: str
    model: str
    dimensions: int
    embedding: list[float]