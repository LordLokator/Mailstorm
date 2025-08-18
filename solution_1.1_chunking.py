# Solution 1 is the most naive approach:
# simply give the sanitized emails as inputs.
# Some prompt engineering and setting the temperature to 0
# were necessary to get consistently good outputs.

from helpers import get_sanitized_data
from config import model_name, ollama_url
from langchain_ollama.llms import OllamaLLM

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
)


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

    print(f"Email n.o {num} ({filename}):")

    # Split thread into chunks
    chunks = splitter.split_text(conversation)

    # Collect results across chunks
    blockers = []
    for chunk in chunks:
        out = model.invoke([system_prompt, chunk])
        if "Yes" in out:   # crude but works if format is enforced
            blockers.append(out)

    # Aggregate to one output per email
    if blockers:
        print("- Blocker found: Yes")
        # Combine justifications into a single line
        reasons = "; ".join(b.split("Justification:", 1)[-1].strip() for b in blockers)
        print(f"- Justification: {reasons}")
    else:
        print("- Blocker found: No")

    print()
    print("##" * 30)
    print()

    # break
