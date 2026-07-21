from typing import Optional

from core.config import config

def get_application(api_key: str) -> Optional[str]:
    for key, app in config.APPLICATIONS.items():
        if app.api_key == api_key:
            return key
    return None