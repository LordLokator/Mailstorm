from langchain_ollama.llms import OllamaLLM

# Ollama params.
# Set model here.
# If remote Ollama server, set URL here.
ollama_url = "http://localhost:11434/"
model_name = "llama3.2:1b"

# Initial prompt for the LLM.
system_prompt = "You are a senior project manager specializing in risk detection in project communications. \
                Your only task: detect potential blockers in the conversation. \
                Disregard anything non-work related.\
                A blocker is anything that delays progress, causes confusion, or requires escalation.  \
                Examples: waiting on missing requirements, unresolved dependencies, unclear ownership,  \
                resource constraints, lack of approvals, misaligned deadlines etc. \
                Do NOT generate more messages, your role is only to evaluate the conversation! \
                Output format (always): \
                - Blocker found: [Yes/No] \
                - Justification: [short text]"

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
