import re

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def normalize_email(email):
    if not isinstance(email, str):
        return None
    return email.strip().lower()


def valid_email(email):
    return bool(email and EMAIL_PATTERN.fullmatch(email))


def required_string(value):
    return isinstance(value, str) and bool(value.strip())
