from pydantic import BaseModel, model_validator
import uuid


class ModelParamaters(BaseModel):
    temperature: float | None = None
    top_k: int | None = None
    top_p: float | None = None


class PayloadAgentStream(BaseModel):
    prompt: str
    agent_id: uuid.UUID | None = None
    thread_id: uuid.UUID | None = None
    provider: str
    model: str | None = None
    tools: list[str] | None = None
    parameters: ModelParamaters | None = None

    @model_validator(mode='after')
    def validate_without_agent_id(self):
        if self.agent_id is None:
            missing = []
            if not self.provider:
                missing.append("provider")
            if not self.model:
                missing.append("model")
            if missing:
                raise ValueError(
                    f"When agent_id is not provided, the following fields "
                    f"are required: {', '.join(missing)}"
                )
        return self