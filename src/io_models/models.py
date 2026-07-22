from pydantic import BaseModel

class ProviderModelsAll(BaseModel):
    chat_completion: list[str]
    translation: list[str]
    vector_embedding: list[str]


class ResponseProviderModelsAll(BaseModel):
    provider: dict[str, ProviderModelsAll]


class ProviderModelsChatCompletions(BaseModel):
    chat_completion: list[str]


class ResponseProviderModelsChatCompletions(BaseModel):
    provider: dict[str, ProviderModelsChatCompletions]


class ProviderModelsTranslations(BaseModel):
    translation: list[str]


class ResponseProviderModelsTranslation(BaseModel):
    provider: dict[str, ProviderModelsTranslations]


class ProviderModelsVectorEmbedding(BaseModel):
    vector_embedding: list[str]


class ResponseProviderModelsVectorEmbedding(BaseModel):
    provider: dict[str, ProviderModelsVectorEmbedding]