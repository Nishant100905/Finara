"""
Input Security Pipeline
"""

from app.security.llm_guard import validate_input
from app.security.moderation import moderate
from app.security.pii import detect_pii, mask_pii


def secure_input(text: str):

    valid, reason = validate_input(text)

    if not valid:

        raise ValueError(reason)

    moderation = moderate(text)

    if not moderation["safe"]:

        raise ValueError(
            moderation["reason"]
        )

    pii = detect_pii(text)

    sanitized = mask_pii(text)

    return {
        "original": text,
        "sanitized": sanitized,
        "pii": pii,
    }