from langchain_ollama import ChatOllama

from core.config import config

# TODO: Rework into a proper callable chain.

llm = ChatOllama(
    model="translategemma",
    temperature=0,
    base_url=config.OLLAMA_BASE_URL
)

llm_instruction = f"""You are a professional English (en-GB) to Dutch (nl) translator. Your goal is to accurately convey the meaning and nuances of the original English text while adhering to Dutch grammar, vocabulary, and cultural sensitivities.
Produce only the Dutch translation, without any additional explanations or commentary. Please translate the following English text into Dutch:\n\n"""

message = [
    (
        "system",
        llm_instruction
    ),
    (
        "human",
        "How is it going? I will be flying to Amsterdam tomorrow. Would you like to meet for a coffee?"

    )
]

response = llm.invoke(message)
print(response)