from data_transformers import get_sanitized_data
from config import model, system_prompt


emails, colleagues = get_sanitized_data("data/content.zip")


for email in emails:
    conversation = email['conversation']
    filename = email['filename']
    num = email['num']

    print(f"Email n.o {num} ({filename}):")

    # Split thread into chunks
    chunks = conversation.split('\n\n')

    # Collect results across chunks
    blockers = []
    for chunk in chunks:
        out = model.invoke([system_prompt, chunk])
        # print(f"\t>> {out}")
        if "Yes" in out:   # crude but works if format is enforced
            blockers.append(out)

    # Aggregate to one output per email
    if blockers:
        print("\t>> Blocker found: Yes")

        reasons = "; ".join(b.split("Justification:", 1)[-1].strip() for b in blockers)
        print(f"\t>> Justification: {reasons}")
    else:
        print("\t>> Blocker found: No")

    print()
    print("##" * 30)
    print()
