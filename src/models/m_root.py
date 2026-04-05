from pydantic import BaseModel

class Contact(BaseModel):
    maintainer: str

class ReturnRoot(BaseModel):
    detail: str
    version: str
    application_name: str
    contact: Contact