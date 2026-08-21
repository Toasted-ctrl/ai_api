from functools import lru_cache, cached_property
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar, Set
import json
import os

from core.logging import get_logger

log = get_logger()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
_env_file = BASE_DIR / ".env"


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

    _SKIP_EMPTY_CHECK: ClassVar[Set[str]] = {
        "_SKIP_EMPTY_CHECK",
        "APP_NAME",
        "APP_VERSION",
        "APP_MAINTAINER",
        "_GOOGLE_ENV_VARS"
    }

    APP_NAME: str = "AIA: Artificial Intelligence API"
    APP_MAINTAINER: str = "Toasted-ctrl"
    APP_VERSION: str = ""

    REDIS_USER: str = ""
    REDIS_HOSTNAME: str = ""
    REDIS_PASSWORD: str = ""
    REDIS_PREFIX: str = ""
    REDIS_PORT: int

    PG_HOSTNAME: str = ""
    PG_DATABASE: str = ""
    PG_USERNAME: str = ""
    PG_PASSWORD: str = ""
    PG_DIALECT: str = ""
    PG_DRIVER: str = ""
    PG_PORT: int

    ENCRYPTION_KEY: str = ""

    BLIND_INDEX_KEY: str = ""

    JWT_SECRET: str = ""

    LOG_LEVEL: str = ""

    COOKIE_SECURE: bool = True
    COOKIE_MAX_AGE: int

    ENABLE_GOOGLE_LOGIN: bool = False
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_REDIRECT_URI: str = ""
    GOOGLE_AUTH_URL: str = ""
    GOOGLE_HMAC: str = ""
    GOOGLE_TOKEN_URL: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # Required to exclude Google variables from startup check,
    # if Google Login is disabled. 
    _GOOGLE_ENV_VARS: ClassVar[set[str]] = {
        "GOOGLE_CLIENT_ID",
        "GOOGLE_REDIRECT_URI",
        "GOOGLE_AUTH_URL",
        "GOOGLE_HMAC",
        "GOOGLE_TOKEN_URL",
        "GOOGLE_CLIENT_SECRET"
    }


    def model_post_init(self, context) -> None:
        all_fields = set(self.__class__.__annotations__.keys())

        unpopulated = all_fields - self._SKIP_EMPTY_CHECK
        unset = all_fields - self.model_fields_set - self._SKIP_EMPTY_CHECK

        if self.ENABLE_GOOGLE_LOGIN == False:
            log.debug(f"Google Login disabled. Skipping environment variables: {' ,'.join(sorted(self._GOOGLE_ENV_VARS))}...")
            unset - self._GOOGLE_ENV_VARS
            unpopulated - self._GOOGLE_ENV_VARS
        
        empty = {
            name
            for name in (unpopulated)
            if isinstance(getattr(self, name, None), str)
            and not getattr(self, name).strip()
        }
        problems = unset | empty
        if problems:
            msgs = []
            if unset:
                msgs.append(f"Missing: {', '.join(sorted(unset))}")
            if empty:
                msgs.append(f"Empty: {', '.join(sorted(empty))}")
            log.warning(
                "The following fields have problems in the .env:\n"
                + "\n".join(msgs)
                + "\nShutting down"
            )
            raise SystemExit(1)
        log.info("Environment variables loaded")


    @cached_property
    def GOOGLE_HMAC_SECRET(self) -> bytes:
        """Returns Google HMAC secret"""
        return self.GOOGLE_HMAC.encode('utf-8')


    @cached_property
    def BLIND_INDEX_HMAC_KEY(self) -> bytes:
        """Returns blind index key."""
        return self.BLIND_INDEX_KEY.encode('utf-8')


    @cached_property
    def PG_DB_URL(self) -> str:

        """Returns the database url"""

        return (
            f"{self.PG_DIALECT}+{self.PG_DRIVER}://"
            f"{self.PG_USERNAME}:{self.PG_PASSWORD}@"
            f"{self.PG_HOSTNAME}:{self.PG_PORT}/{self.PG_DATABASE}"
        )
    

    @cached_property
    def MODEL_TYPES(self) -> dict:
        """Returns a dictionary of model types, categorized by their expertise
        (e.g., llms, translations, vector-embeddings)"""
        return _model_types()
    

    @cached_property
    def TRANSLATION_MODELS(self) -> list:
        """Returns a list of models suitable for translation tasks."""
        return _model_types().get("translation", [])
    
    
    @cached_property
    def VECTOR_EMBEDDING_MODELS(self) -> list:
        """Returns a list of models suitable for vector embeddings."""
        return _model_types().get("vector_embedding", [])
    

    @cached_property
    def CHAT_COMPLETION_MODELS(self) -> list:
        """Returns a list of chat completion models"""
        return _model_types().get("chat_completion", [])

config = Config()