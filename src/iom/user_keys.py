import uuid
from datetime import datetime
from pydantic import BaseModel


class PayloadUserKeys(BaseModel):
    provider: str
    api_key: str


class ResponseUserKey(BaseModel):
    user_id: uuid.UUID
    provider: str
    api_key_short: str
    expires: datetime