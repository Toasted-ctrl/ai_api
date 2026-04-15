from langchain_ollama import ChatOllama

def llm_stream_ollama(query: str, url: str, model: str):

    llm = ChatOllama(
        model=model,
        base_url=url
    )

    # TODO: Just a test, update later.
    # TODO: Write tests.

    for chunk in llm.stream(query):
        yield chunk.content
