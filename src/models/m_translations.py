from pydantic import BaseModel

class PayloadTranslation(BaseModel):
    from_language: str
    from_lang_code: str
    to_language: str
    to_lang_code: str
    temperature: float
    query: str

class Translation(BaseModel):
    from_lang_code: str
    to_lang_code: str
    input: str
    output: str
    temperature: float

class ReturnTranslation(BaseModel):
    detail: str
    translation: Translation