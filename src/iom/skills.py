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


class ResponseGetSkill(BaseModel):
    skill_id: uuid.UUID
    name: str
    description: str
    instructions: str
    parameter_schema: Optional[dict] = None


class PayloadPatchSkill(BaseModel):
    skill_id: uuid.UUID
    instructions: str


class ResponsePatchSkill(BaseModel):
    skill_id: uuid.UUID
    name: str
    description: str
    instructions: str
    parameter_schema: Optional[dict] = None