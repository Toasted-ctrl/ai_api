from pydantic import BaseModel
import uuid


class ResponseAuthenticatedUser(BaseModel):
    id: uuid.UUID