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
                            "name": "mxbai-embed-large",
                            "dimensions": 1024
                        }
                    ],
                    "translations": [
                        {
                            "name": "translategemma",
                            "languages": {
                                "en-GB": "English",
                                "de-DE": "German",
                                "pt-PT": "Portuguese",
                                "nl": "Dutch",
                                "sl": "Slovenian"
                            }
                        }
                    ],
                    "llms": [
                        {
                            "name": "llama3.1",
                            "stream_enabled": False
                        },
                        {
                            "name": "llama2",
                            "stream_enabled": False
                        }
                    ]
                }
            }
        ]
    
    def supported_models(self, type: str) -> dict[str, str]:

        """Returns all supported models for the specified type,
        and consequently which server / service the model is hosted on."""

        if not type in ["translations", "llms", "vector_embeddings"]:
            raise ValueError("Invalid type")

        servers = self.get_model_configuration
        supported = {}
        for server in servers:
            models: list = server.get('model_types').get(type)
            if not models:
                continue
            for model in models:
                supported[model.get('name')] = server.get('server')

        return supported

config = Config()