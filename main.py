from config import model
from prompts import (
    SINGLE_MAIL_SUMMARY_SYS_PROMPT,
    SINGLE_MAIL_OUTPUT_FORMAT,

    MASTER_SUMMARIZATION_SYS_PROMPT,
    MASTER_SUMMARIZATION_OUTPUT_FORMAT,

    template
)

from data_transformers import get_sanitized_data

if __name__ == "__main__":

    emails, colleagues = get_sanitized_data("data/content.zip")

    model_outputs = []
    for i, email in enumerate(emails):
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
        model_outputs.append(model_output)
        print(model_output)

        print('\n', "##" * 30, '\n')

        # For quicker iteration:
        if i > 2:
            break

    final_prompt = template.format(
        system=MASTER_SUMMARIZATION_SYS_PROMPT,
        conversation="\n".join(model_outputs),  # combine all outputs
        output_format=MASTER_SUMMARIZATION_OUTPUT_FORMAT
    )

    print(final_prompt)
    summary = model.invoke(final_prompt)

    print(summary)
