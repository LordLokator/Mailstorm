# Solution 1 is the most naive approach:
# simply give the sanitized emails as inputs.
# Some prompt engineering and setting the temperature to 0
# were necessary to get consistently good outputs.

from textwrap import dedent
from config import model, output_format, system_prompt

from langchain.prompts import PromptTemplate

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
        {output_format}
        """
    )
)

system_prompt = """
You are a summarization agent helping a Project Manager by summarizing email conversation chains.
Summarize the email convesation below!
Follow these principles:
Relevant — the summary retains important points and details from the source text;
Concise — the summary is information-dense, does not repeat the same point multiple times, and is not unnecessarily verbose;
Coherent — the summary is well-structured and easy to follow, not just a jumble of condensed facts;
Faithful — the summary does not hallucinate information that is not supported by the source text.

Focus on capturing / identifying issues like below:

1. Unresolved High-Priority Action Items (UHPAI): Questions or tasks that have gone \
unanswered or unaddressed for a significant period.
2. Emerging Risks/Blockers: Potential problems or obstacles identified in \
communications that lack a clear resolution path.
"""

model_outputs = []
for i, email in enumerate(emails):
    conversation = email['conversation']
    filename = email['filename']
    num = email['num']

    print(f"Email n.o {num} ({filename}):")

    messages = [
        system_prompt,
        conversation,
    ]

    prompt = template.format(
        system=system_prompt,
        conversation=conversation,
        output_format="""
        Be brief, do not write greeting or intros,
        reply only with the relevant summarization!
        Disregard and do not mention anything not work related,
        e.g parties or holliday plans!
        Answer without any introductory or conclusion text.
        """
    )

    model_output = model.invoke(prompt)
    model_outputs.append(model_output)
    print(model_output)

    # Prototype -> misusing loguru for formatting is totally allowed

    print('\n', f"##" * 30, '\n')

    if i > 2:
        break

final_prompt = template.format(
    system=system_prompt,
    conversation="\n".join(model_outputs),  # combine all outputs
    output_format="""
    Given the following input, list every instance of the following two issue types:
    1. Unresolved High-Priority Action Items (UHPAI): Questions or tasks that have gone \
unanswered or unaddressed for a significant period.
    2. Emerging Risks/Blockers: Potential problems or obstacles identified in \
communications that lack a clear resolution path.
"""
)

print(final_prompt)
summary = model.invoke(final_prompt)

print(summary)
