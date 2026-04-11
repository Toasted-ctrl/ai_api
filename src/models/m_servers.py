from pydantic import BaseModel

class ReturnWakeServer(BaseModel):
    detail: str

class ReturnServers(BaseModel):
    detail: str
    servers: list[str]

class ReturnServerStatus(BaseModel):
    server_name: str
    status: str
    available: bool