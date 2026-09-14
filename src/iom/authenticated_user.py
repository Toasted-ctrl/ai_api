import uuid
from pydantic import BaseModel


class ResponseAuthenticatedUser(BaseModel):
    user_id: uuid.UUID
    first_name: str
    last_name: str
    email: str