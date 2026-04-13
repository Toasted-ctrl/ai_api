from pydantic import BaseModel

# Components

class VectorEmbeddingModel(BaseModel):
    name: str
    dimensions: int

class TranslationModel_withLanguages(BaseModel):
    name: str
    languages: dict[str, str]

class TranslationModel_withoutLanguages(BaseModel):
    name: str

class LLM(BaseModel):
    name: str
    stream_enabled: bool

# All models

class AllType(BaseModel):
    vector_embeddings: list[VectorEmbeddingModel]
    translations: list[TranslationModel_withoutLanguages]
    llms: list[LLM]

class AllServer(BaseModel):
    server: str
    model_types: AllType

class ReturnAllModels(BaseModel):
    detail: str
    servers: list[AllServer]

# Vector embedding models

class VEType(BaseModel):
    vector_embeddings: list[VectorEmbeddingModel]

class VEServer(BaseModel):
    server: str
    model_types: VEType

class ReturnVecterEmbeddingsServerLayout(BaseModel):
    detail: str
    servers: list[VEServer]

# Translation models

class TMType(BaseModel):
    translations: list[TranslationModel_withLanguages]

class TMServer(BaseModel):
    server: str
    model_types: TMType

class ReturnTranslationModelsServerLayout(BaseModel):
    detail: str
    servers: list[TMServer]

# LLMs

class LLMType(BaseModel):
    llms: list[LLM]

class LLMServer(BaseModel):
    server: str
    model_types: LLMType

class ReturnLLMServerLayout(BaseModel):
    detail: str
    servers: list[LLMServer]