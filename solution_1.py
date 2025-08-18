# Solution 1 is the most naive approach:
# simply give the sanitized emails as inputs.
# Some prompt engineering and setting the temperature to 0
# were necessary to get consistently good outputs.

from langchain_ollama.llms import OllamaLLM

from config import model_name, ollama_url, system_prompt

from helpers import get_sanitized_data
emails, colleagues = get_sanitized_data("data/content.zip")

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
