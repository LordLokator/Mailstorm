from data_transformers.email_handling import remove_mail_addresses_inplace
from data_transformers.role_handling import add_roles_to_names_inplace
from data_transformers.date_handling import replace_dates_with_deltas
from helpers import get_files_from_zip, parse


def get_sanitized_data(path: str) -> tuple[list[dict[str, str]], dict[str, dict]]:
    """Access sanitized data through this function. Expose only this function."""

    txt_files = get_files_from_zip(path)
    colleagues, emails = parse(txt_files)

    # region data transformers
    remove_mail_addresses_inplace(emails)
    add_roles_to_names_inplace(emails, colleagues)

    for mail in emails:
        mail['conversation'] = replace_dates_with_deltas(mail['conversation'])

    # endregion

    return emails, colleagues


if __name__ == '__main__':
    import json

    path = "data/content.zip"
    emails, colleagues = get_sanitized_data(path)

    print(json.dumps(colleagues, indent=4, ensure_ascii=False))

    print('--' * 30)

    print(emails[0].keys())

    print('--' * 30)

    print(emails[0]['conversation'])
