from functools import lru_cache, cached_property
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import json
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
_env_file = BASE_DIR / ".env"

class ApplicationConfig(BaseModel):
    name: str
    api_key: str
    hmac_secret: bytes
    require_google_id: bool
    require_jwt: bool


@lru_cache(maxsize=1)
def _model_types() -> dict:

    """Loads and caches the model_types json data."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'model_types.json')

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    

class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=_env_file if _env_file.exists() else None,
        extra="ignore"
    )

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

    ADMIN_HMAC: str = ""
    ADMIN_API_KEY: str = ""
    ADMIN_REQUIRE_GOOGLE_ID: bool = False
    ADMIN_REQUIRE_JWT: bool = False

    JELAIME_HMAC: str = ""
    JELAIME_API_KEY: str = ""
    JELAIME_REQUIRE_GOOGLE_ID: bool = True
    JELAIME_REQUIRE_JWT: bool = True

    PG_HOSTNAME: str = ""
    PG_DATABASE: str = ""
    PG_USERNAME: str = ""
    PG_PASSWORD: str = ""
    PG_DIALECT: str = ""
    PG_DRIVER: str = ""
    PG_PORT: int

    # NOTE: Update _APP_REGISTRY if new applications are added.
    _CLIENT_REGISTRY = [
        {"key": "jelaime", "env_prefix": "JELAIME", "name": "LEJAIME App"},
        {"key": "admin", "env_prefix": "ADMIN", "name": "ADMIN Key"}
    ]

    
    @cached_property
    def LOCAL_SERVER_CONFIGURATION(self) -> dict:

        """Returns a dictionary of local server configurations"""

        return {
            "Ollama-1": {
                "mac_address": self.OLLAMA_1_MAC,
                "base_url": self.OLLAMA_1_BASE_URL,
                "hostname": self.OLLAMA_1_HOSTNAME
            }
        }


    @cached_property
    def PG_DB_URL(self) -> str:

        """Returns the database url"""

        return (
            f"{self.PG_DIALECT}+{self.PG_DRIVER}://"
            f"{self.PG_USERNAME}:{self.PG_PASSWORD}@"
            f"{self.PG_HOSTNAME}:{self.PG_PORT}/{self.PG_DATABASE}"
        )
    

    @cached_property
    def APPLICATIONS(self) -> dict[str, ApplicationConfig]:
        return {
            app["key"]: ApplicationConfig(
                name=app["name"],
                api_key=getattr(self, f"{app['env_prefix']}_API_KEY"),
                hmac_secret=getattr(self, f"{app['env_prefix']}_HMAC").encode(encoding="utf-8"),
                require_google_id=getattr(self, f"{app['env_prefix']}_REQUIRE_GOOGLE_ID"),
                require_jwt=getattr(self, f"{app['env_prefix']}_REQUIRE_JWT")
            )
            for app in self._CLIENT_REGISTRY
        }


    @cached_property
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