# Solution 1 is the most naive approach:
# simply give the sanitized emails as inputs.
# Some prompt engineering and setting the temperature to 0
# were necessary to get consistently good outputs.

from langchain_ollama.llms import OllamaLLM

from config import model_name, ollama_url

from helpers import get_sanitized_data
emails, colleagues = get_sanitized_data("data/content.zip")

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

for email in emails:
    conversation = email['conversation']
    filename = email['filename']
    num = email['num']

    messages = [
        system_prompt,
        conversation,
    ]

    print(f"Email n.o {num}:")

    print(model.invoke(messages))

    # Prototype -> misusing loguru for formatting is totally allowed
    print()
    print(f"##" * 30)
    print()
