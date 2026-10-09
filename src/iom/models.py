from pydantic import BaseModel


class ResponseProviderModels(BaseModel):
    providers: dict[str, dict[str, list[str]]]


class ModelSampling(BaseModel):
    temperature: bool
    top_k: bool
    top_p: bool


class ResponseModelSampling(BaseModel):
    provider: str
    model: str
    sampling: ModelSampling