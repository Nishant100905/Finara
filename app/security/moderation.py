"""
Content Moderation

Detects:
- Hate Speech
- Violence
- Self Harm
- Sexual Content
- Toxicity
"""

import logging
import re

logger = logging.getLogger(__name__)

# ==========================================================
# Keyword Lists
# ==========================================================

HATE_PATTERNS = [

    r"\bkill all\b",

    r"\bhate\b",

    r"\bterrorist\b",

    r"\bgenocide\b",

]

VIOLENCE_PATTERNS = [

    r"\bmurder\b",

    r"\bkill\b",

    r"\bstab\b",

    r"\bshoot\b",

    r"\bexplode\b",

]

SELF_HARM_PATTERNS = [

    r"\bsuicide\b",

    r"\bself harm\b",

    r"\bcut myself\b",

    r"\bend my life\b",

]

SEXUAL_PATTERNS = [

    r"\bporn\b",

    r"\bexplicit\b",

    r"\bsexual\b",

    r"\bnude\b",

]

TOXIC_PATTERNS = [

    r"\bstupid\b",

    r"\bidiot\b",

    r"\bdumb\b",

]


# ==========================================================
# Generic Pattern Checker
# ==========================================================

def contains_pattern(text: str, patterns: list) -> bool:

    text = text.lower()

    for pattern in patterns:

        if re.search(pattern, text):

            return True

    return False


# ==========================================================
# Individual Checks
# ==========================================================

def detect_hate(text: str):

    return contains_pattern(
        text,
        HATE_PATTERNS,
    )


def detect_violence(text: str):

    return contains_pattern(
        text,
        VIOLENCE_PATTERNS,
    )


def detect_self_harm(text: str):

    return contains_pattern(
        text,
        SELF_HARM_PATTERNS,
    )


def detect_sexual(text: str):

    return contains_pattern(
        text,
        SEXUAL_PATTERNS,
    )


def detect_toxicity(text: str):

    return contains_pattern(
        text,
        TOXIC_PATTERNS,
    )


# ==========================================================
# Overall Moderation
# ==========================================================

def moderate(text: str):
    """
    Returns:
        {
            "safe": bool,
            "category": str,
            "reason": str,
        }
    """

    if not text:

        return {
            "safe": True,
            "category": None,
            "reason": None,
        }

    if detect_hate(text):

        logger.warning("Hate speech detected")

        return {
            "safe": False,
            "category": "hate",
            "reason": "Hate speech detected.",
        }

    if detect_violence(text):

        logger.warning("Violence detected")

        return {
            "safe": False,
            "category": "violence",
            "reason": "Violent content detected.",
        }

    if detect_self_harm(text):

        logger.warning("Self-harm detected")

        return {
            "safe": False,
            "category": "self_harm",
            "reason": "Self-harm related content detected.",
        }

    if detect_sexual(text):

        logger.warning("Sexual content detected")

        return {
            "safe": False,
            "category": "sexual",
            "reason": "Explicit sexual content detected.",
        }

    if detect_toxicity(text):

        logger.warning("Toxic language detected")

        return {
            "safe": False,
            "category": "toxicity",
            "reason": "Toxic language detected.",
        }

    return {
        "safe": True,
        "category": None,
        "reason": None,
    }