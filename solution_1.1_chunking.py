from langchain_text_splitters import RecursiveCharacterTextSplitter
from data_transformers import get_sanitized_data
from config import model

from prompts import (
    SINGLE_MAIL_SUMMARY_SYS_PROMPT,
    SINGLE_MAIL_OUTPUT_FORMAT,

    template
)


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
)


emails, colleagues = get_sanitized_data("data/content.zip")

for email in emails:
    conversation = email['conversation']
    filename = email['filename']
    num = email['num']

    print(f"Email n.o {num} ({filename}):")

    # Split thread into chunks
    chunks = splitter.split_text(conversation)

    # Collect results across chunks
    blockers = []
    for chunk in chunks:

        prompt = template.format(
            system=SINGLE_MAIL_SUMMARY_SYS_PROMPT,
            conversation=conversation,
            output_format=SINGLE_MAIL_OUTPUT_FORMAT
        )
        model_output = model.invoke(prompt)
        print(model_output)

        if "Yes" in model_output:   # crude but works if format is enforced
            blockers.append(model_output)

    # Aggregate to one output per email
    if blockers:
        print("- Blocker found: Yes")
        # Combine justifications into a single line
        reasons = "; ".join(b.split("Justification:", 1)[-1].strip() for b in blockers)
        print(f"- Justification: {reasons}")
    else:
        print("- Blocker found: No")

    print('\n', f"##" * 30, '\n')

    # break
