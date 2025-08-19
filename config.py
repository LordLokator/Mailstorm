from langchain_ollama.llms import OllamaLLM

ollama_url = "http://localhost:11434/"

model_name = "llama3.2:1b"

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

model = OllamaLLM(
    # specified in config
    model=model_name,
    base_url=ollama_url,

    temperature=0  # reproducibility
)
