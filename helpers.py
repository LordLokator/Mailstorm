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
                        logger.trace(f"Loaded {name}")
                except Exception as e:
                    logger.warning(f"Failed to read {name}: {e}")
                    continue  # log the error but don't stop processing.

    except BadZipFile:
        logger.exception(f"Bad ZIP file: {zip_path}.")

    except Exception as e:
        logger.exception(f"Error opening {zip_path}.")
        raise

    return files


def parse(txt_files: dict[str, str]) -> tuple[dict, list[dict]]:
    """Extract colleagues and emails from {filename: content} dict."""
    # Pass extracted txt files for testability (allows for DI style unittesting later).

    emails = []
    _colleagues = ""

    for filename, content in txt_files.items():
        match = re.fullmatch(r"email(\d+)\.txt", filename, re.IGNORECASE)

        if match:

            emails.append({
                "filename": match.group(0),
                "conversation": content
            })

        elif filename == "Colleagues.txt":
            _colleagues = content

        else:
            logger.warning(f"Ignored unexpected file: {filename}")

    colleagues = load_colleagues(_colleagues)
    return colleagues, emails


def load_colleagues(data: str):
    colleagues = {}
    pattern = re.compile(r"^(.*?)\s*:\s*(.*?)\s*\((.*?)\)$")
    # regex breakdown:
    #   ^               -> Start of Line
    #   (.*?)\s*:\s*    -> capture text before a ':' character, disregard whitespace
    #   (.*?)\s*\(      -> capture text until a '(' character
    #   (.*?)\)         -> capture until a ')'
    #   $               -> End of Line
    # example inputs:
    # "Project Manager (PM): Péter Kovács (kovacs.peter@...)"
    # "Account Manager (AM): Zoltán Kiss (zoltan.kiss@kisjozsitech.hu)""

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        match = pattern.match(line)
        if match:
            role, name, email = match.groups()
            colleagues[name] = {"role": role, "email": email}
    return colleagues


def remove_mail_addresses(emails: list) -> None:
    pattern = re.compile(r"\([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\)")
    # used regexr to check this regex selector.
    # It matches for mails with arbitrarily long TLDs.

    for i in range(len(emails)):
        # Modify in-place
        emails[i]['conversation'] = pattern.sub("", emails[i]['conversation']).strip()


def add_role_to_name(emails: list[dict[str, str]], colleagues: dict) -> None:
    for i, email in enumerate(emails):
        for name, info in colleagues.items():
            # Replace full name with role
            designation = f"{name} ({info["role"]})"
            email['conversation'] = email['conversation'].replace(name, designation)
        emails[i] = email


def get_sanitized_data(path: str) -> tuple[list[dict[str, str]], dict[str, dict]]:
    """Accesssanitized data through this function. Expose only this function."""

    txt_files = get_files_from_zip(path)
    colleagues, emails = parse(txt_files)

    remove_mail_addresses(emails)
    add_role_to_name(emails, colleagues)

    return emails, colleagues
