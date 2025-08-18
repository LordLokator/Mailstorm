from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from config import model_name, template, ollama_url, system_prompt

from helpers import get_sanitized_data
emails, colleagues = get_sanitized_data("data/content.zip")

chat_model = OllamaLLM(
    model=model_name,
    base_url=ollama_url
)

Human_Question = input("What do you want to ask Ollama? ")


messages = [
    system_prompt,
    Human_Question,
]

print(chat_model.invoke(messages))
