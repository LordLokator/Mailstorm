from config import model
from data_transformers import get_sanitized_data
from control import Mode
from json_handler import save_json_safe
from loguru import logger
from prompts import (
    SINGLE_MAIL_SUMMARY_SYS_PROMPT,
    SINGLE_MAIL_OUTPUT_FORMAT,

    MASTER_SUMMARIZATION_SYS_PROMPT,
    MASTER_SUMMARIZATION_OUTPUT_FORMAT,

    template
)


def main(mode: Mode, path = None):
    path = path or "data/content.zip"

    match mode:
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

    emails, _ = get_sanitized_data(path)

    model_outputs = []
    for i, email in enumerate(emails):
        conversation = email['conversation']
        filename = email['filename']
        num = email['num']

        logger.info(f"Analysing e-mail n.o {num} ({filename}).")

        match mode:
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
                    # TODO: write more chunk-specific prompts!
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

    combined_reports = "\n".join(model_outputs)  # bit naive
    final_prompt = template.format(
        system=MASTER_SUMMARIZATION_SYS_PROMPT,
        conversation=combined_reports,  # combine all outputs
        output_format=MASTER_SUMMARIZATION_OUTPUT_FORMAT
    )

    logger.info(final_prompt)
    summary = model.invoke(final_prompt)
    save_json_safe(summary)

    logger.info(summary)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LLM powered Portfolio Health Report generator (with chunking strategy).")
    parser.add_argument(
        "--chunking_strategy",
        choices=["manual", "automatic", "none"],
        default="none",
        help="Set the chunking strategy (default: none)."
    )

    parser.add_argument(
        "--path",
        type=str,
        default="./data/content.zip",
        help="Path to the .zip file (default: ./data/content.zip)."
    )


    args = parser.parse_args()
    logger.info(f"Selected chunking strategy: {args.chunking_strategy}")
    logger.info(f"Path to zip: {args.path}")

    if args.chunking_strategy == 'manual':
        # For splitting the convo along emails (split along '\n\n' substring):
        mode = Mode.MANUAL_SPLIT

    if args.chunking_strategy == 'automatic':
        # Use langChain's RecursiveCharacterTextSplitter:
        mode = Mode.AUTO_SPLIT

    if args.chunking_strategy == 'none':
        # Pass whole email conversation as context:
        mode = Mode.FULL_CONVERSATION

    main(mode, args.path)
