from config import model_name, template, ollama_url

# SETUP
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from config import model_name, template, system_prompt

# SETUP

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
