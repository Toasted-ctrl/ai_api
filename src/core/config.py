from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    app_name: str = "AIA: Artificial Intelligence API"
    app_maintainer: str = "Toasted-ctrl"
    app_version: str = "0.0.1"

    OLLAMA_BASE_URL: str = ""

config = Config()