from config import model_name, template, ollama_url

# SETUP
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from config import model_name, template

# SETUP

chat_model = OllamaLLM(
    model=model_name,
    base_url=ollama_url
)

Human_Question = input("What do you want to ask Ollama? ")

SystemMessage = "You are a assistant knowledgable in space. \
                Only answer questions related to space. \
                If the question is not related to space \
                then reply with 'I don't know'."

messages = [
    SystemMessage,
    Human_Question,
]

print(chat_model.invoke(messages))
