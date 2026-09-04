from pydantic import BaseModel


class ProviderSettings(BaseModel):
    name: str
    model: str