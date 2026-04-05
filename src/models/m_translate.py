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