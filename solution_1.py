# Solution 1 is the most naive approach:
# simply give the sanitized emails as inputs.
# Some prompt engineering and setting the temperature to 0
# were necessary to get consistently good outputs.
# Using langchain's PromptTemplate class made
# the model follow output rules much more closely.

from textwrap import dedent

from langchain.prompts import PromptTemplate

from config import model, system_prompt
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
    model_output = model.invoke(prompt)
    print(model_output)

    # Prototype -> misusing loguru for formatting is totally allowed
    print()
    print(f"##" * 30)
    print()
