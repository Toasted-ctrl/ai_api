from pydantic import BaseModel

class PayloadTranslation(BaseModel):
    from_language: str
    to_language: str
    text_input: str

class ReturnTranslation(BaseModel):
    detail: str
    from_language: str
    to_language: str
    text_input: str
    text_output: str

class Model(BaseModel):
    model_name: str
    language_codes: list[str]

class ReturnTranslationModels(BaseModel):
    detail: str
    models: list[Model]