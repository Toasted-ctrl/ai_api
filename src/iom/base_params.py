from pydantic import BaseModel


class ModelParamaters(BaseModel):
    temperature: float | None = None
    top_k: int | None = None
    top_p: float | None = None