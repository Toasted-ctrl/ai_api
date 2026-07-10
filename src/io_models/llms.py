from pydantic import BaseModel

class LLMParameters(BaseModel):
    temperature: float | None = None
    top_k: int | None = None
    top_p: float | None = None

class PostLLM(BaseModel):
    provider: str
    model: str | None = None
    agent: str | None = None
    stream: bool | None = True
    context: list | None = None
    prompt: str
    parameters: LLMParameters