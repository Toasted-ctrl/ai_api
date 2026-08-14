from pydantic import BaseModel

class ProviderModelsAll(BaseModel):
    chat_completion: list[str]
    translation: list[str]
    vector_embedding: list[str]


class ResponseProviderModelsAll(BaseModel):
    providers: dict[str, ProviderModelsAll]


class ProviderModelsChatCompletions(BaseModel):
    chat_completion: list[str]


class ResponseProviderModelsChatCompletions(BaseModel):
    providers: dict[str, ProviderModelsChatCompletions]


class ProviderModelsTranslations(BaseModel):
    translation: list[str]


class ResponseProviderModelsTranslation(BaseModel):
    providers: dict[str, ProviderModelsTranslations]


class ProviderModelsVectorEmbedding(BaseModel):
    vector_embedding: list[str]


class ResponseProviderModelsVectorEmbedding(BaseModel):
    providers: dict[str, ProviderModelsVectorEmbedding]