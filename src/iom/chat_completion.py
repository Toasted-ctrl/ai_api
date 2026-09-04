from pydantic import BaseModel

from .base_params import ModelParamaters


class PayloadChatCompletion(BaseModel):
    provider: str
    model: str | None = None
    stream: bool | None = True
    context: list | None = None
    prompt: str
    parameters: ModelParamaters