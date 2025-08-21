import json
from loguru import logger
from pathlib import Path

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def save_json_safe(model_output):
    """
    Safely parse the model output as JSON and save to file.
    """
    try:
        # Attempt to parse output
        data = json.loads(model_output)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON. Saving raw output instead.")
        data = {"raw_output": model_output}

    # Save to a file named after the email
    out_path = OUTPUT_DIR / "summary.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved parsed output to {out_path}")
    return data
