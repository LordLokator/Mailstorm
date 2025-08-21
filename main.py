from config import model
from data_transformers import get_sanitized_data
from control import Mode
from loguru import logger
from prompts import (
    SINGLE_MAIL_SUMMARY_SYS_PROMPT,
    SINGLE_MAIL_OUTPUT_FORMAT,

    MASTER_SUMMARIZATION_SYS_PROMPT,
    MASTER_SUMMARIZATION_OUTPUT_FORMAT,

    template
)

# Set chunking strategy here!

# Pass whole email conversation as context:
chunking_strategy = Mode.FULL_CONVERSATION

# Use langChain's RecursiveCharacterTextSplitter:
# chunking_strategy = Mode.AUTO_SPLIT

# For splitting the convo along emails (split along '\n\n' substring):
# chunking_strategy = Mode.MANUAL_SPLIT

match chunking_strategy:
    case Mode.FULL_CONVERSATION:
        logger.info("Processing full email conversation")

    case Mode.AUTO_SPLIT:
        logger.info("Splitting with RecursiveCharacterTextSplitter")
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=100,
        )

    case Mode.MANUAL_SPLIT:
        logger.info("Using manual chunking")


if __name__ == "__main__":

    emails, colleagues = get_sanitized_data("data/content.zip")

    model_outputs = []
    for i, email in enumerate(emails):
        conversation = email['conversation']
        filename = email['filename']
        num = email['num']

        logger.info(f"Analysing e-mail n.o {num} ({filename}).")

        match chunking_strategy:
            case Mode.FULL_CONVERSATION:
                prompt = template.format(
                    system=SINGLE_MAIL_SUMMARY_SYS_PROMPT,
                    conversation=conversation,
                    output_format=SINGLE_MAIL_OUTPUT_FORMAT
                )

                model_output = model.invoke(prompt)
                logger.trace(f"e-mail n.o {num} | ", model_output)
                model_outputs.append(model_output)

            case Mode.AUTO_SPLIT:
                chunks = splitter.split_text(conversation)

                # Collect results across chunks
                chunk_inference_outputs = []
                for chunk in chunks:

                    prompt = template.format(
                        # TODO: write more chunk-specific prompts!
                        system=SINGLE_MAIL_SUMMARY_SYS_PROMPT,
                        conversation=chunk,
                        # TODO: write more chunk-specific prompts!
                        output_format=SINGLE_MAIL_OUTPUT_FORMAT
                    )
                    model_output = model.invoke(prompt)
                    chunk_inference_outputs.append(model_output)

                # Inference / summary over all chunks for a given e-mail:
                final_prompt = template.format(
                    system=MASTER_SUMMARIZATION_SYS_PROMPT,
                    conversation="\n".join(chunk_inference_outputs),  # combine all outputs
                    output_format=MASTER_SUMMARIZATION_OUTPUT_FORMAT
                )

                model_output = model.invoke(final_prompt)
                logger.trace(f"e-mail n.o {num} | ", model_output)
                model_outputs.append(model_output)

            case Mode.MANUAL_SPLIT:
                # data / domain specific knowledge:
                # emails have 2 newlines between them.
                chunks = conversation.split('\n\n')

                chunk_inference_outputs = []
                for chunk in chunks:
                    out = model.invoke([SINGLE_MAIL_SUMMARY_SYS_PROMPT, chunk])
                    chunk_inference_outputs.append(out)

                # Inference / summary over all parts a given e-mail:
                final_prompt = template.format(
                    system=MASTER_SUMMARIZATION_SYS_PROMPT,
                    conversation="\n".join(chunk_inference_outputs),  # combine all outputs
                    output_format=MASTER_SUMMARIZATION_OUTPUT_FORMAT
                )

                model_output = model.invoke(final_prompt)
                logger.trace(f"e-mail n.o {num} | ", model_output)
                model_outputs.append(model_output)

        # For quicker iteration:
        # if i > 2:
        #     break

    final_prompt = template.format(
        system=MASTER_SUMMARIZATION_SYS_PROMPT,
        conversation="\n".join(model_outputs),  # combine all outputs
        output_format=MASTER_SUMMARIZATION_OUTPUT_FORMAT
    )

    logger.info(final_prompt)
    summary = model.invoke(final_prompt)

    logger.info(summary)
