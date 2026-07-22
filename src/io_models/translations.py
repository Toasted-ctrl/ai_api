from pydantic import BaseModel

class TranslationParameters(BaseModel):
    temperature: float = 0.1


class PayloadTranslation(BaseModel):
    from_lang_code: str
    to_lang_code: str
    parameters: TranslationParameters
    prompt: str


class ResponseTranslation(BaseModel):
    prompt: str
    translation: str
    from_lang_code: str
    to_lang_code: str


class ResponseTranslationLanguages(BaseModel):
    languages: list[str]