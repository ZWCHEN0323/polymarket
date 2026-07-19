"""Security helpers for credential handling and log redaction."""

from app.core.constants import MASKED_SECRET_VISIBLE_CHARS


def mask_secret(value: str, visible_chars: int = MASKED_SECRET_VISIBLE_CHARS) -> str:
    """Return a redacted representation of a sensitive string for safe logging."""
    if not value:
        return ""
    if len(value) <= visible_chars:
        return "*" * len(value)
    return f"{value[:visible_chars]}{'*' * (len(value) - visible_chars)}"
