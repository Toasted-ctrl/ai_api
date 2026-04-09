from pydantic import BaseModel

class Model(BaseModel):
    name: str
    size: int

class ReturnModels(BaseModel):
    detail: str
    models: list[Model]