def add_roles_to_names(emails: list[dict[str, str]], colleagues: dict) -> None:
    for i, email in enumerate(emails):
        for name, info in colleagues.items():
            # Replace full name with role
            designation = f"{name} ({info["role"]})"
            email['conversation'] = email['conversation'].replace(name, designation)
        emails[i] = email
