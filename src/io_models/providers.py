from pydantic import BaseModel


class ProviderResponse(BaseModel):
    id: str
    name: str
    base_url: str
    internal: bool
    requires_api_key: bool
    langchain_con: str
    api_key_configured: bool | None = None


class ProvidersResponse(BaseModel):
    providers: list[ProviderResponse]