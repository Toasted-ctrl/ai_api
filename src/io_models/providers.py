from pydantic import BaseModel
import uuid

class ProviderResponse(BaseModel):
    id: uuid.UUID
    name: str
    internal: bool
    requires_api_key: bool
    api_key_configured: bool | None = None


class ProvidersResponse(BaseModel):
    providers: list[ProviderResponse]