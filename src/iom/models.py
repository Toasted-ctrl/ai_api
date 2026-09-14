from pydantic import BaseModel


class ResponseProviderModels(BaseModel):
    providers: dict[str, dict[str, list[str]]]