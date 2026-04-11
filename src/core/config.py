from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    app_name: str = "AIA: Artificial Intelligence API"
    app_maintainer: str = "Toasted-ctrl"
    app_version: str = "0.0.2"

    OLLAMA_BASE_URL: str = ""
    OLLAMA_MAC: str = ""

    @property
    def get_servers(self) -> dict[str]:

        """Returns dictionary of configured servers"""

        # NOTE: Add more servers below if available.

        return {
            "ollama": {
                "mac_address": self.OLLAMA_MAC,
                "base_url": self.OLLAMA_BASE_URL,
                "url_ext_list_models": "/api/tags"
            }
        }

config = Config()