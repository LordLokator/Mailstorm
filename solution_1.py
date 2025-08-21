from config import model
from data_transformers import get_sanitized_data

from prompts import (
    SINGLE_MAIL_SUMMARY_SYS_PROMPT,
    SINGLE_MAIL_OUTPUT_FORMAT,

    template
)

emails, colleagues = get_sanitized_data("data/content.zip")


for email in emails:
    conversation = email['conversation']
    filename = email['filename']
    num = email['num']

    print(f"Email n.o {num} ({filename}):")

    prompt = template.format(
        system=SINGLE_MAIL_SUMMARY_SYS_PROMPT,
        conversation=conversation,
        output_format=SINGLE_MAIL_OUTPUT_FORMAT
    )
    model_output = model.invoke(prompt)
    print(model_output)

    # Prototype -> misusing loguru for formatting is totally allowed
    print('\n', f"##" * 30, '\n')
