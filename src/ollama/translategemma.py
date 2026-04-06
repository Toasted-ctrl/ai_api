# NOTE: List all languages we want to support
languages = {
    "en-GB": "English",
    "nl": "Dutch",
    "de-DE": "German",
    "pt-PT": "Portuguese"
}

def get_languages(languages: dict=languages) -> list[str]:
    return [lang_code for lang_code, _ in languages.items()]

def get_language_settings(lang_code: str, languages: dict=languages) -> tuple[str, str]:
    if lang_code not in languages.keys():
        raise ValueError("Unavailable language code")
    return lang_code, languages[lang_code]