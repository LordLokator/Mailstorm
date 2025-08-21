import re


def remove_mail_addresses(emails: list) -> None:
    pattern = re.compile(r"\([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\)")
    # used regexr to check this regex selector.
    # It matches for mails with arbitrarily long TLDs.

    for i in range(len(emails)):
        # Modify in-place
        emails[i]['conversation'] = pattern.sub("", emails[i]['conversation']).strip()
