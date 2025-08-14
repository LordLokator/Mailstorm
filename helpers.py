from pathlib import Path
from zipfile import ZipFile, BadZipFile
from loguru import logger
import re


def get_files_from_zip(path: str, suffix: str = '.txt') -> dict[str, str]:
    """Return {filename: text_content} for all .txt files in a ZIP."""
    files = {}
    zip_path = Path(path)

    if not zip_path.is_file():
        logger.error(f"Invalid path or not a file: {zip_path}")
        return files

    try:
        with ZipFile(zip_path, 'r') as zf:
            for name in zf.namelist():
                if not Path(name).suffix.casefold() == suffix.casefold():
                    continue
                try:
                    with zf.open(name) as f:
                        files[name] = f.read().decode('utf-8', errors='replace')
                        logger.debug(f"Loaded {name}")
                except Exception as e:
                    logger.warning(f"Failed to read {name}: {e}")
                    continue  # log the error but don't stop processing.

    except BadZipFile:
        logger.exception(f"Bad ZIP file: {zip_path}.")

    except Exception as e:
        logger.exception(f"Error opening {zip_path}.")
        raise

    return files


def parse(txt_files: dict[str, str]) -> tuple[str, dict[int, str]]:
    """Extract colleagues and emails from {filename: content} dict."""
    # Pass extracted txt files for testability (allows for DI style unittesting later).

    emails = {}
    colleagues = ""

    for filename, content in txt_files.items():
        match = re.fullmatch(r"email(\d+)\.txt", filename, re.IGNORECASE)

        if match:
            emails[int(match.group(1))] = content

        elif filename == "Colleagues.txt":
            colleagues = content

        else:
            logger.warning(f"Ignored unexpected file: {filename}")

    return colleagues, emails


if __name__ == '__main__':

    path = "data/content.zip"
    txt_files = get_files_from_zip(path)
    colleagues, emails = parse(txt_files)

    for key, item in emails.items():
        print(f"{key}: {type(key)} | {type(item)}")
