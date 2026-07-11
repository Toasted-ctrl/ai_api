from langchain_ollama import ChatOllama

from core.config import config
from providers.ollama.translategemma import get_language, get_language_code

def get_translation_translategemma(
    from_lang: str,
    to_lang: str,
    prompt: str,
    temperature: float
) -> dict:

    """Invokes a translation from translategemma 4B"""

    llm = ChatOllama(
        model="translategemma:latest",
        temperature=temperature,
        base_url=config.OLLAMA_1_BASE_URL,
        disable_streaming=True
    )

    from_language = get_language(from_lang)
    to_language = get_language(to_lang)
    from_lang_code = get_language_code(from_lang)
    to_lang_code = get_language_code(to_lang)

    instruction = f"""
    You are a professional {from_language} ({from_lang_code}) to {to_language} ({to_lang_code}) translator.
    Your goal is to accurately convey the meaning and nuances of the original {from_language} text while adhering to {to_language} grammar, vocabulary, and cultural sensitivities.
    Produce only the {to_language} translation, without any additional explanations or commentary.
    Please translate the following {from_language} text into {to_language}:\n\n{prompt}"""

    translation = llm.invoke(instruction)

    return {
        "prompt": prompt,
        "translation": translation.content,
        "from_lang_code": from_lang,
        "to_lang_code": to_lang
    }