"""
Output Validation
"""

import re


def contains_secret(text: str) -> bool:

    patterns = [

        r"AIza[0-9A-Za-z\-_]{35}",

        r"sk-[A-Za-z0-9]{20,}",

        r"BEGIN PRIVATE KEY",

        r"password",

        r"secret",

        r"token",

    ]

    for pattern in patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE,
        ):

            return True

    return False


def validate_output(answer: str) -> str:
    """
    Validate the output answer.

    Returns the answer string if safe.
    Returns a sanitized message if secrets are detected.
    """

    if not answer:
        return "I'm sorry, I couldn't generate an answer."

    if contains_secret(answer):
        return "I'm sorry, the generated response was filtered for security reasons."

    return answer