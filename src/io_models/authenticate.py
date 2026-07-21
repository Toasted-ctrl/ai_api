from pydantic import BaseModel

class PayloadAuthenticate(BaseModel):
    sub: str
    email: str

class ResponseAuthenticate(BaseModel):
    jwt: str