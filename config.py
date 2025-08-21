from textwrap import dedent
from langchain_ollama.llms import OllamaLLM

# Ollama params.
# Set model here.
# If remote Ollama server, set URL here.
ollama_url = "http://localhost:11434/"
model_name = "llama3.1:latest"


# NOTE: for other LLMs (e.g OpenAI),
# use other LangChain classes.
# These usually require API keys.
# e.g use this import:
# from langchain_community.llms.openai import OpenAIChat
model = OllamaLLM(
    # specified in config
    model=model_name,
    base_url=ollama_url,

    temperature=0  # reproducibility
)


async def invoke_async(llm, prompt):
    result = await llm.ainvoke(prompt)
    print(result)
