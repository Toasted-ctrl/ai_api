import uuid
from pydantic import BaseModel
from typing import Optional


class PayloadCreateSkill(BaseModel):
    name: str
    description: str
    skill_text: str
    parameters_schema: Optional[dict] = None


class ResponseCreateSkill(BaseModel):
    skill_id: uuid.UUID
    name: str
    message: str