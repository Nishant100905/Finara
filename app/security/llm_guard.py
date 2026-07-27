"""
LLM Guard

Provides protection against:
- Prompt Injection
- Jailbreak Attempts
- Malicious Inputs
- Sensitive Prompt Leakage
"""

import logging
import re

logger = logging.getLogger(__name__)


# ==========================================================
# Prompt Injection Patterns
# ==========================================================

PROMPT_INJECTION_PATTERNS = [

    r"ignore\s+previous\s+instructions",

    r"ignore\s+all\s+instructions",

    r"system\s+prompt",

    r"reveal\s+your\s+prompt",

    r"developer\s+message",

    r"forget\s+everything",

    r"you\s+are\s+now",

    r"bypass",

    r"disable\s+safety",

    r"jailbreak",

    r"act\s+as",

    r"pretend\s+to\s+be",

    r"sudo",

    r"root\s+access",

    r"execute\s+shell",

    r"rm\s+-rf",

    r"<script",

    r"</script>",

    r"drop\s+table",

    r"union\s+select",

    r"insert\s+into",

    r"delete\s+from",

    r"--",

    r";",

]


# ==========================================================
# Prompt Injection Detector
# ==========================================================

def detect_prompt_injection(text: str) -> bool:
    """
    Returns True if prompt injection is detected.
    """

    if not text:
        return False

    text = text.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:

        if re.search(pattern, text):

            logger.warning(
                "Prompt Injection Detected: %s",
                pattern,
            )

            return True

    return False


# ==========================================================
# Jailbreak Detector
# ==========================================================

JAILBREAK_PATTERNS = [

    r"do\s+anything\s+now",

    r"dan",

    r"developer\s+mode",

    r"evil\s+mode",

    r"unfiltered",

    r"no\s+restrictions",

    r"without\s+limitations",

    r"ignore\s+ethics",

    r"ignore\s+policy",

    r"ignore\s+safety",

    r"simulate",

    r"roleplay",

]


def detect_jailbreak(text: str) -> bool:

    if not text:
        return False

    text = text.lower()

    for pattern in JAILBREAK_PATTERNS:

        if re.search(pattern, text):

            logger.warning(
                "Jailbreak Attempt: %s",
                pattern,
            )

            return True

    return False


# ==========================================================
# SQL Injection Detector
# ==========================================================

SQL_PATTERNS = [

    r"drop\s+table",

    r"union\s+select",

    r"insert\s+into",

    r"delete\s+from",

    r"truncate",

    r"alter\s+table",

    r"sleep\(",

]


def detect_sql_injection(text: str) -> bool:

    if not text:
        return False

    text = text.lower()

    for pattern in SQL_PATTERNS:

        if re.search(pattern, text):

            logger.warning(
                "SQL Injection Detected"
            )

            return True

    return False


# ==========================================================
# XSS Detector
# ==========================================================

XSS_PATTERNS = [

    r"<script",

    r"</script>",

    r"javascript:",

    r"onload=",

    r"onclick=",

    r"alert\(",

]


def detect_xss(text: str) -> bool:

    if not text:
        return False

    text = text.lower()

    for pattern in XSS_PATTERNS:

        if re.search(pattern, text):

            logger.warning(
                "XSS Attempt Detected"
            )

            return True

    return False


# ==========================================================
# Main Guard
# ==========================================================

def validate_input(text: str):
    """
    Validate user input against common attack patterns.

    Returns:
        (is_valid, reason)
    """

    if detect_prompt_injection(text):
        return False, "Prompt injection detected."

    if detect_jailbreak(text):
        return False, "Jailbreak attempt detected."

    if detect_sql_injection(text):
        return False, "SQL injection detected."

    if detect_xss(text):
        return False, "XSS attempt detected."

    return True, "Safe"