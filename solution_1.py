# Solution 1 is the most naive approach:
# simply give the sanitized emails as inputs.
# Some prompt engineering and setting the temperature to 0
# were necessary to get consistently good outputs.
# Using langchain's PromptTemplate class made
# the model follow output rules much more closely.

from prompts import prompts
from config import model, template
from data_transformers import get_sanitized_data

emails, colleagues = get_sanitized_data("data/content.zip")


for email in emails:
    conversation = email['conversation']
    filename = email['filename']
    num = email['num']

    print(f"Email n.o {num} ({filename}):")

    messages = [
        prompts['system_prompt'],
        conversation,
    ]

    prompt = template.format(
        system=prompts['unified']['system_prompt'],
        conversation=conversation,
        output_format=prompts['unified']['output_format']
    )
    model_output = model.invoke(prompt)
    print(model_output)

    # Prototype -> misusing loguru for formatting is totally allowed
    print('\n', f"##" * 30, '\n')
