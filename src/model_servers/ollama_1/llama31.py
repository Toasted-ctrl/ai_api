from langchain_ollama import ChatOllama

from core.config import config

def llm_stream():

    llm = ChatOllama(
        model="llama3.1",
        base_url=config.OLLAMA_BASE_URL

    )

    # TODO: Just a test, update later.
    # TODO: Write tests.

    query = "What do you think about the current state of the world?"

    for chunk in llm.stream(query):
        yield chunk.content
