from langchain_ollama import ChatOllama

def complete_chat_ollama(
    prompt: str,
    url: str,
    model: str,
    stream: bool = True,
    temperature: float | None = None,
    top_k: int | None = None,
    top_p: float | None = None
):

    """Returns a response from an LLM hosted on the Ollama server."""

    llm = ChatOllama(
        model=model,
        base_url=url,
        disable_streaming=True if stream == False else False,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p
    )

    for chunk in llm.stream(prompt):
        yield chunk.content
