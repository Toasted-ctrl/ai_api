from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    app_name: str = "AIA: Artificial Intelligence API"
    app_maintainer: str = "Toasted-ctrl"
    app_version: str = "0.0.4"

    OLLAMA_BASE_URL: str = ""
    OLLAMA_MAC: str = ""

    @property
    def get_server_configuration(self) -> dict:

        """Returns server configurations, which includes for each server:
        \n- MAC address
        \n- Base URL"""

        # NOTE: Add more servers below if available.

        return {
            "ollama": {
                "mac_address": self.OLLAMA_MAC,
                "base_url": self.OLLAMA_BASE_URL,
                "url_ext_list_models": "/api/tags"
            }
        }
    
    @property
    def get_model_configuration(self) -> list[dict]:

        """Returns dictionary of configured servers and models."""

        return [
            {
                "server": "ollama",
                "model_types": {
                    "vector_embeddings": [
                        {
                            "name": "mxbai-embed-large:latest",
                            "dimensions": 1024
                        }
                    ],
                    "translations": [
                        {
                            "name": "translategemma:latest"
                        }
                    ],
                    "llms": [
                        {
                            "name": "llama3.1:latest",
                            "stream_enabled": False
                        },
                        {
                            "name": "llama2:latest",
                            "stream_enabled": False
                        }
                    ]
                }
            }
        ]

config = Config()