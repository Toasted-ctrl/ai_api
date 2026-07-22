from pydantic import BaseModel

class PayloadJWT(BaseModel):
    sub: str
    email: str
    given_name: str
    family_name: str


class ResponseJWT(BaseModel):
    jwt: str