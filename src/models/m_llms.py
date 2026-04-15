from pydantic import BaseModel

class PayloadLLM(BaseModel):
    model_name: str = "llama3.1"
    query: str = "Test, test, is anyone there?"