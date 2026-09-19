import uuid
from pydantic import BaseModel


class MCP(BaseModel):
    id: uuid.UUID
    name: str


class ResponseMCP(BaseModel):
    mcps: list[MCP]