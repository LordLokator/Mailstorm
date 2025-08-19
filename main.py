# Solution 1 is the most naive approach:
# simply give the sanitized emails as inputs.
# Some prompt engineering and setting the temperature to 0
# were necessary to get consistently good outputs.

from textwrap import dedent
from helpers import get_sanitized_data
from config import model, system_prompt

from langchain.prompts import PromptTemplate

from config import model_name, ollama_url

from helpers import get_sanitized_data
emails, colleagues = get_sanitized_data("data/content.zip")

template = PromptTemplate(
    input_variables=["system", "conversation"],
    template=dedent(
        """
        [SYSTEM]
        {system}

        [CONVERSATION]
        {conversation}

        [OUTPUT]
        Respond with exactly ONE line in this format:
        Blocker found: [Yes/No] - [short explanation]
        """
    )
)


for email in emails:
    conversation = email['conversation']
    filename = email['filename']
    num = email['num']

    print(f"Email n.o {num} ({filename}):")

    messages = [
        system_prompt,
        conversation,
    ]

    prompt = template.format(system=system_prompt, conversation=conversation)
    print(model.invoke(prompt))

    # Prototype -> misusing loguru for formatting is totally allowed
    print()
    print(f"##" * 30)
    print()
