from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings
import json
import os

load_dotenv()

@lru_cache(maxsize=1)
def _model_types() -> dict:

    """Loads and caches the model_types json data."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'model_types.json')

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    

class Config(BaseSettings):
    app_name: str = "AIA: Artificial Intelligence API"
    app_maintainer: str = "Toasted-ctrl"
    app_version: str = "0.1.0"

    OLLAMA_1_BASE_URL: str = ""
    OLLAMA_1_MAC: str = ""
    OLLAMA_1_HOSTNAME: str = ""

    REDIS_USER: str = ""
    REDIS_HOSTNAME: str = ""
    REDIS_PASSWORD: str = ""
    REDIS_PREFIX: str = ""
    REDIS_PORT: int
    
    @property
    def LOCAL_SERVER_CONFIGURATION(self) -> dict:

        """Returns a dictionary of local server configurations"""

        return {
            "Ollama-1": {
                "mac_address": self.OLLAMA_1_MAC,
                "base_url": self.OLLAMA_1_BASE_URL,
                "hostname": self.OLLAMA_1_HOSTNAME
            }
        }
    

    @property
    def SUPPORTED_PROVIDERS(self) -> list[str]:

        """Returns a list of supported Providers (e.g., Ollama, Anthropic)."""

        return [
            "Ollama-1"
        ]
    

    @property
    def MODEL_TYPES(self) -> dict:
        
        """Returns a dictionary of model types, categorized by their expertise
        (e.g., llms, translations, vector-embeddings)"""

        return _model_types()
    

    @property
    def TRANSLATION_MODELS(self) -> list:

        """Returns a list of models suitable for translation tasks."""

        return _model_types().get("translation", [])
    
    
    @property
    def VECTOR_EMBEDDING_MODELS(self) -> list:

        """Returns a list of models suitable for vector embeddings."""

        return _model_types().get("vector_embedding", [])
    

    @property
    def CHAT_COMPLETION_MODELS(self) -> list:

        """Returns a list of chat completion models"""

        return _model_types().get("chat_completion", [])

config = Config()