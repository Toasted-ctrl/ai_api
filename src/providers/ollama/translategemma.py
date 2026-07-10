from functools import lru_cache
import json
import os

@lru_cache(maxsize=1)
def _load_translategemma_data() -> dict:

    """Loads and caches the Translategemma.json data."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'translategemma.json')

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    

def supported_languages() -> list[str]:

    """Returns a list of languages supported by Translategemma."""

    data = _load_translategemma_data()
    return [key for key in data['supported'].keys()]


def get_language_code(lang_code: str) -> str:

    """Returns the appropriate language code to be used with Translategemma.
    This method is used to comply with the Translategemma documentation, but to keep
    the general language code set-up the same across translation models."""

    data = _load_translategemma_data()
    return data['short_code_remap'].get(lang_code, lang_code)


def get_language(lang_code: str) -> str:

    """Returns the language in accordance with the provided language code for Translategemma."""

    data = _load_translategemma_data()
    return data['supported'][lang_code]