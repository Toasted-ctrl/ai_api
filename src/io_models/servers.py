from pydantic import BaseModel

class ResponseWakeServer(BaseModel):
    detail: str

class LocalServer(BaseModel):
    server_name: str
    online: bool
    available: bool

class ResponseLocalServers(BaseModel):
    on_prem: list[LocalServer]