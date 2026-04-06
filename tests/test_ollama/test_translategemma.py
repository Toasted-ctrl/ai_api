from ollama.translategemma import get_language_settings, get_languages

def test_get_languages():
    result = get_languages()
    assert len(result) == 4
    assert isinstance(result[0], str)

def test_get_language_settings():
    result = get_language_settings(lang_code="en-GB")
    assert isinstance(result, tuple)
    assert result[0] == "en-GB"
    assert result[1] == "English"