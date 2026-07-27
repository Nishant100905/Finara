"""
PII Detection & Masking
"""

import re

EMAIL = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE = r"\b(?:\+91[- ]?)?[6-9]\d{9}\b"
AADHAAR = r"\b\d{4}\s?\d{4}\s?\d{4}\b"
PAN = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
CARD = r"\b(?:\d[ -]*?){13,16}\b"
IP = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
API_KEY = r"AIza[0-9A-Za-z\-_]{35}"


def detect_pii(text: str):

    findings = {
        "email": re.findall(EMAIL, text),
        "phone": re.findall(PHONE, text),
        "aadhaar": re.findall(AADHAAR, text),
        "pan": re.findall(PAN, text),
        "credit_card": re.findall(CARD, text),
        "ip": re.findall(IP, text),
        "api_key": re.findall(API_KEY, text),
    }

    findings = {
        k: v
        for k, v in findings.items()
        if v
    }

    return findings


def mask_pii(text: str):

    text = re.sub(EMAIL, "[EMAIL]", text)
    text = re.sub(PHONE, "[PHONE]", text)
    text = re.sub(AADHAAR, "[AADHAAR]", text)
    text = re.sub(PAN, "[PAN]", text)
    text = re.sub(CARD, "[CARD]", text)
    text = re.sub(IP, "[IP]", text)
    text = re.sub(API_KEY, "[API_KEY]", text)

    return text