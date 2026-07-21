from pydantic import BaseModel

class PayloadJWT(BaseModel):
    sub: str
    email: str

class ResponseJWT(BaseModel):
    jwt: str