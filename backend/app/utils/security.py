import re
from typing import Optional

# Security utilities for input sanitization

DANGEROUS_PATTERNS = [
    r"(?i)(union|select|insert|update|delete|drop|create|alter|exec|execute)\s",
    r"(?i)(script|iframe|onload|onerror|onclick)\s*=",
    r"(\.\./|~\)+",
    r"(?i)(etc/passwd|etc/shadow|proc/self)",
    r"(?i)(cmd\.exe|powershell|bash|sh)\s",
]

def sanitize_input(value: str, max_length: int = 1000) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not isinstance(value, str):
        return ""
    # Truncate
    value = value[:max_length]
    # Remove null bytes
    value = value.replace("\x00", "")
    # Remove control characters except newlines and tabs
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", value)
    return value

def validate_path(path: str, allowed_base: str = "/app/data") -> bool:
    """Validate that a path is within allowed boundaries."""
    try:
        resolved = os.path.realpath(path)
        base = os.path.realpath(allowed_base)
        return resolved.startswith(base)
    except Exception:
        return False

def is_safe_command(command: str) -> bool:
    """Check if a command is in the allowlist."""
    allowed = {"ls", "cat", "echo", "pwd", "whoami", "date", "uname", "df", "ps"}
    return command in allowed

import os
