from pydantic import BaseModel, model_validator
import uuid

from .base_params import ModelParamaters
from .base_prov import ProviderSettings


class PayloadAgent(BaseModel):
    agent_id: uuid.UUID | None = None
    thread_id: uuid.UUID | None = None

    provider_settings: ProviderSettings | None = None
    parameters: ModelParamaters | None = None

    prompt: str
    mcp_tools: list[uuid.UUID] | None = None

    @model_validator(mode='after')
    def validate_without_agent_id(self):
        if self.agent_id is None:
            if not self.provider_settings:
                raise ValueError(
                    "When agent_id is not provided, the following fields "
                    "are required: provider_settings.provider, provider_settings.model."
                )
        return self


class ResponseAgentRun(BaseModel):
    thread_id: uuid.UUID
    messages: list