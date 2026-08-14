from pydantic import BaseModel

class Contact(BaseModel):
    maintainer: str


class ResponseRoot(BaseModel):
    version: str
    application_name: str
    contact: Contact