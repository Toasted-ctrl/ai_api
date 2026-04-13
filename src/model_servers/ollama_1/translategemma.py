from langchain_ollama import ChatOllama

# TODO: Build test for below function

def get_translation_translategemma(
    from_language: str,
    from_lang_code: str,
    to_language: str,
    to_lang_code: str,
    query: str,
    server_url: str,
    temperature: float=0.1):

    """Invokes a translation from translategemma 8B"""

    llm = ChatOllama(
        model="translategemma",
        temperature=temperature,
        base_url=server_url
    )

    instruction = f"""
    You are a professional {from_language} ({from_lang_code}) to {to_language} ({to_lang_code}) translator.
    Your goal is to accurately convey the meaning and nuances of the original {from_language} text while adhering to {to_language} grammar, vocabulary, and cultural sensitivities.
    Produce only the {to_language} translation, without any additional explanations or commentary.
    Please translate the following {from_language} text into {to_language}:\n\n{query}"""

    translation = llm.invoke(instruction)

    return {
        "input": query,
        "output": translation.content,
        "from_lang_code": from_lang_code,
        "to_lang_code": to_lang_code,
        "temperature": temperature
    }