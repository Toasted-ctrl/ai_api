from pydantic import BaseModel

class TranslationParameters(BaseModel):
    temperature: float = 0.1

class PostTranslation(BaseModel):
    from_lang_code: str
    to_lang_code: str
    parameters: TranslationParameters
    provider: str
    model: str
    prompt: str

class ResponseTranslation(BaseModel):
    prompt: str
    translation: str
    from_lang_code: str
    to_lang_code: str